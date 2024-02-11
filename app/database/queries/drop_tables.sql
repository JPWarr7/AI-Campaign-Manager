drop function if exists share_amount;
drop function if exists UnownedShares;
drop function if exists find_stock_broker;
drop function if exists find_shares;
drop function if exists find_share_amount;
drop function if exists can_delist;
drop function if exists delistStock;
drop function if exists available_shares;
drop function if exists max_fill_shares;


drop procedure if exists fill_broker_shares;
drop procedure if exists fill_stock_brokers;
drop procedure if exists broker_stocks;

drop procedure if exists create_stock;
drop procedure if exists update_share_count;
drop procedure if exists add_shares;
drop procedure if exists remove_shares;
drop procedure if exists create_request;
drop procedure if exists approve_request;
drop procedure if exists deny_request;
drop procedure if exists view_requests;


drop trigger if exists create_request_result;
drop trigger if exists create_stock_shares;
drop trigger if exists update_unowned_shares;


drop table if exists results;
drop table if exists requests;
drop table if exists share_amounts;
drop table if exists shares;
drop table if exists stock_brokers;
drop table if exists stocks;
drop view if exists v_brokers;
drop view if exists v_traders;
drop table if exists users;