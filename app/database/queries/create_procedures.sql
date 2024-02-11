-- Takes broker id, randomly gives the broker stocks
DELIMITER //
create procedure broker_stocks(in usr_id int)
begin
	declare done int default false;
	declare id int;
	declare stk_cursor cursor for select stk_id from stocks;
    declare continue handler for not found set done = true;
	open stk_cursor;
    fill_loop: loop
		fetch stk_cursor into id;
        if done then 
			leave fill_loop;
        end if;
        if not floor(rand() * 10) = 0 then
			insert into stock_brokers (stk_id, bkr_id) values (id, usr_id);
        end if;
    end loop;
    close stk_cursor;
end;
// DELIMITER ;

-- Loops over brokers with cursor, calls above procedure for each broker
DELIMITER //
create procedure fill_stock_brokers()
begin
	declare done int default false;
	declare id int;
	declare bkr_cursor cursor for select users.usr_id 
		from users where users.account_type = 'Broker';
    declare continue handler for not found set done = true;
	open bkr_cursor;
    fill_loop: loop
		fetch bkr_cursor into id;
        if done then 
			leave fill_loop;
        end if;
		call broker_stocks(id);
    end loop;
    close bkr_cursor;
end;
// DELIMITER ;

# Loops over broker stocks with cursor, randomly gives them shares
DELIMITER //
create procedure fill_broker_shares()
begin
	declare done int default false;
	declare t_stk_id int;
	declare t_bkr_id int;
    declare amount int;
	declare shr_id int;
	declare stb_cursor cursor for 
		select B.stk_id, B.bkr_id from stock_brokers as B;
    declare continue handler for not found set done = true;
	open stb_cursor;
    fill_loop: loop
		fetch stb_cursor into t_stk_id, t_bkr_id;

		if done then leave fill_loop;
        end if;

		select find_shares(t_stk_id, t_bkr_id, null) into shr_id;

		set amount = floor(1 + rand() * 10) * 10;
		call update_share_count(shr_id, amount);
    end loop;
	close stb_cursor;
end;
// DELIMITER ;

# Given stock id and broker id, return a matching stock broker id
DELIMITER //
create function find_stock_broker(stk_id int, bkr_id int) returns int
deterministic
begin
	declare stb_id int;

    select SB.stb_id into stb_id
        from stock_brokers as SB
		where SB.bkr_id = bkr_id and SB.stk_id = stk_id;

	if stb_id is null then
		insert into stock_brokers (stk_id, bkr_id) values (stk_id, bkr_id);
		select last_insert_id() into stb_id;
	end if;

	return stb_id;
end;
// DELIMITER ;

# Given stock id, broker id, (possibly null) trader id, return a matching share id
DELIMITER //
create function find_shares(t_stk_id int, t_bkr_id int, t_tdr_id int) returns int
deterministic
begin
    declare t_stb_id int;
    declare shr_id int;

    select find_stock_broker(t_stk_id, t_bkr_id) into t_stb_id;

    select SH.shr_id into shr_id
        from shares as SH
        join stock_brokers as SB using (stb_id)
        where SB.stb_id = t_stb_id and if(isnull(t_tdr_id), SH.tdr_id is null, SH.tdr_id = t_tdr_id);

    if shr_id is null then
        insert into shares (stb_id, tdr_id) values (t_stb_id, t_tdr_id);
        select last_insert_id() into shr_id;
    end if;
    return shr_id;
end;
DELIMITER ;

-- takes share id and returns the number of shares owned
DELIMITER //
create function find_share_amount(t_shr_id int) returns bigint
deterministic
begin
    declare amount bigint;
    select HA.quantity into amount
        from share_amounts as HA
        where HA.shr_id = t_shr_id;
    return amount;
end;
DELIMITER ;

-- takes request id and (possibly null) broker quantity and updates the status of the request
DELIMITER //
create procedure approve_request(in target_req_id int, in bkr_shr_amount bigint)
begin 
	declare req_shr_id int;
	declare amount bigint;
    declare exchange enum ('Buy', 'Sell');

    declare r_final_amount bigint;

    # Extract request info
    select R.shr_id, R.amount, R.exchange into req_shr_id, amount, exchange
		from requests as R where R.req_id = target_req_id;

	# create share amounts for trader if needed
	if not exists (select * from share_amounts as SHA where SHA.shr_id = req_shr_id) then
        insert into share_amounts (shr_id, quantity) values (req_shr_id, 0);
    end if;

	# calculate final amount
    set r_final_amount = share_amount(req_shr_id, amount, bkr_shr_amount, exchange);

	# approve request
    update results as RS set
        final_amount = r_final_amount,
		status = (
		    case
		        when r_final_amount = 0 then 'Not Filled'
		        when r_final_amount = amount then 'Filled'
		        else 'Partially Filled'
		    end
		)
	where RS.req_id = target_req_id;
end;
// DELIMITER ;

DELIMITER //
create procedure deny_request(in my_req_id int)
begin
    update results as L
        set L.status = 'Not Filled', L.final_amount = 0
        where L.req_id = my_req_id;
end;
DELIMITER ;

-- Takes share id, returns number of available shares that stock broker has
DELIMITER //
create function available_shares(t_shr_id int) returns bigint deterministic
begin
    declare t_stb_id int;
    declare available int;

    select SB.stb_id into t_stb_id
        from shares as SH
        join stock_brokers as SB using (stb_id)
        where SH.shr_id = t_shr_id;

    select SA.quantity into available
        from share_amounts as SA
        join shares as SH using (shr_id)
        join stock_brokers as SB using (stb_id)
        where SB.stb_id = t_stb_id and SH.tdr_id is null;
    return available;
end //
DELIMITER ;

-- takes stock_broker id, requested amount, and broker amount and handles the corresponding logic
DELIMITER //
create function share_amount(t_shr_id int, req_amount bigint, bkr_amount bigint, exchange enum ('Buy', 'Sell')) returns bigint
deterministic
begin
	declare available_amount bigint;
    declare final_amount bigint;
    if exchange = 'Buy' then
	    select available_shares(t_shr_id) into available_amount;
    else
        select SA.quantity into available_amount
            from share_amounts as SA
            where SA.shr_id = t_shr_id;
    end if;
    if bkr_amount is not null then -- broker override
        set final_amount = least(bkr_amount, available_amount);
    else
        set final_amount = least(req_amount, available_amount);
    end if;
	return final_amount;
end;
// DELIMITER ;

-- Calculate the total unowned shares for the given stock
DELIMITER //
CREATE FUNCTION UnownedShares(id INT) RETURNS BIGINT deterministic
BEGIN
  DECLARE total_unowned_shares BIGINT;
SELECT SUM(SHA.quantity)
    INTO total_unowned_shares
  FROM stocks AS S
  JOIN stock_brokers AS SB using (stk_id)
  JOIN shares AS SH using (stb_id)
  JOIN share_amounts AS SHA using (shr_id)
  WHERE S.stk_id = id AND SH.tdr_id IS NULL; -- Count only shares that don't belong to any trader and are therefore unowned
  IF total_unowned_shares IS NULL THEN
    SET total_unowned_shares = 0;
  END IF;
  
  RETURN total_unowned_shares;
END//
DELIMITER ;


DELIMITER //
create procedure create_request(in tdr_id int, in stk_id int, in bkr_id int, in req_amount int, in exchange_type enum ('Buy', 'Sell'))
begin
    declare req_shr_id int;
    select find_shares(stk_id, bkr_id, tdr_id) into req_shr_id;
    insert into requests(shr_id, amount, exchange) values (req_shr_id, req_amount, exchange_type);
end;
DELIMITER ;

DELIMITER //
create procedure create_stock(in new_bkr_id int, in stk_name varchar(32), in stk_code varchar(16))
begin
    declare new_stk_id int;
    insert into stocks (name, code) values (stk_name, stk_code);
    select last_insert_id() into new_stk_id;
    insert into stock_brokers (stk_id, bkr_id) values (new_stk_id, new_bkr_id);
end;
DELIMITER ;

DELIMITER //
create function can_delist(t_stk_id int) returns bool deterministic
begin
    declare shares_available int;
    select sum(SA.quantity) into shares_available
        from share_amounts as SA
        join shares as SH using (shr_id)
        join stock_brokers as SB using (stb_id)
        where SB.stk_id = t_stk_id
        group by SB.stk_id;

    if if(isnull(shares_available), 0, shares_available = 0) then
        return 1;
    else
        return 0;
    end if;
end;
DELIMITER ;

DELIMITER //
create function delistStock(VAR_stk_id int) returns int deterministic
begin
    if can_delist(VAR_stk_id) then
        delete from stocks where stk_id = VAR_stk_id;
    end if;
  return VAR_stk_id;
end//
DELIMITER ;

-- updates share counts for supplied stock broker id, share count, and (possibly null) trader id
DELIMITER //
create procedure update_share_count(in t_shr_id int, in amount bigint)
begin
    update share_amounts as HA
        set quantity = HA.quantity + amount
        where HA.shr_id = t_shr_id;
end;
// DELIMITER ;

# Given a stock id, broker id, and amount of shares, increase the stock brokers share count by the amount
DELIMITER //
create procedure add_shares(in stk_id int, in bkr_id int, in amount bigint)
begin
    declare shr_id int;
    set shr_id = find_shares(stk_id, bkr_id, null);
    call update_share_count(shr_id, greatest(amount, 0)); -- no you cannot have negative shares
end;
DELIMITER ;

# Given a stock id, broker id, and amount of shares, decrease the stock brokers share count by the amount
DELIMITER //
create procedure remove_shares(in stk_id int, in bkr_id int, in amount bigint)
begin
    declare shr_id int;
    declare max_amount bigint;
    set shr_id = find_shares(stk_id, bkr_id, null);
    set max_amount = find_share_amount(shr_id); -- again, you cannot have negative shares
    call update_share_count(shr_id, -1 * least(amount, max_amount));
end;
DELIMITER ;

# Given a broker id, trader id, return the pending requests
DELIMITER //
create procedure view_requests(in t_tdr_id int, in t_bkr_id int, in t_stk_id int, in only_pending bool)
begin
        select R.amount, R.exchange, L.final_amount, L.status, SB.bkr_id, SH.tdr_id, R.req_id,
               available_shares(R.shr_id) as available,
               concat_ws(' ', UB.first_name, UB.last_name) as bkr_name,
               concat_ws(' ', UT.first_name, UT.last_name) as tdr_name,
               S.name as stk_name, S.stk_id as stk_id
        from requests as R
        join results as L using (req_id)
        join shares as SH using (shr_id)
        join stock_brokers as SB using (stb_id)
        join stocks as S using (stk_id)
        join v_traders as UT on UT.usr_id = SH.tdr_id
        join v_brokers as UB on UB.usr_id = SB.bkr_id
        where if(isnull(t_tdr_id), 1, SH.tdr_id = t_tdr_id)
            and if(isnull(t_bkr_id), 1, SB.bkr_id = t_bkr_id)
            and if(isnull(t_stk_id), 1, S.stk_id = t_stk_id)
            and if(isnull(only_pending), 1, L.status = 'Pending');
end;
DELIMITER ;

DELIMITER //
create function max_fill_shares(t_req_id int) returns int deterministic
begin
    declare t_shr_id int;
    declare t_stb_id int;
    declare t_exchange enum ('Buy', 'Sell');
    declare t_r_amount int;
    declare t_b_amount int;

    select R.shr_id, R.amount, SH.stb_id, R.exchange
        into t_shr_id, t_r_amount, t_stb_id, t_exchange
        from requests as R
        join shares as SH using (shr_id)
        where R.req_id = t_req_id;

    if t_exchange = 'Sell' then
        return t_r_amount;
    end if;

    select SA.quantity into t_b_amount
        from share_amounts as SA
        join shares as SH using (shr_id)
        where SH.tdr_id is null and SH.stb_id = t_stb_id;

    return least(t_r_amount, t_b_amount);
end;
DELIMITER //