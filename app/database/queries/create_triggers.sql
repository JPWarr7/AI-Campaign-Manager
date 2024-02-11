-- Creates a "blank" result when a new request is made
DELIMITER //
create trigger create_request_result after insert on requests
for each row
begin
	insert into results (req_id) values (New.req_id);
end;
// DELIMITER ;

-- Add rows for zero shares when a new stock is brokered
DELIMITER //
create trigger create_stock_shares after insert on stock_brokers
for each row
begin
    declare new_shr_id int;
    insert into shares (stb_id) values (New.stb_id);
    select last_insert_id() into new_shr_id;
    insert into share_amounts (shr_id) values (new_shr_id);
end;
// DELIMITER ;

-- Update share amounts table after successfully approved requests
DELIMITER //
create trigger update_unowned_shares after update on results
for each row
begin
	declare amount int;
    declare type enum ('Buy', 'Sell');
	declare req_shr_id int;
	declare req_stb_id int;
	declare bkr_shr_id int;

	# Select shares, stockbroker ids using request id
	select SH.stb_id, RQ.shr_id, RQ.exchange into req_stb_id, req_shr_id, type
	    from requests as RQ
	    join shares as SH using (shr_id)
	    where RQ.req_id = New.req_id;

    # Select unowned shares for same stockbroker
    select SH.shr_id into bkr_shr_id from shares as SH
        where SH.stb_id = req_stb_id and SH.tdr_id is null;

	if not New.status = 'Not Filled' then
        if not New.final_amount = 0 then
            set amount = IF(type = 'Buy', -1 * New.final_amount, New.final_amount);
            call update_share_count(bkr_shr_id, amount);
            call update_share_count(req_shr_id, amount * -1);
        end if;
	end if;
end;
// DELIMITER ;
