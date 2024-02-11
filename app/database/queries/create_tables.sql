create database if not exists csc400_ads;
use csc400_ads;

-- create users table
create table if not exists users (
	user_id int not null auto_increment,
    username varchar(32) not null unique,
    user_password varchar(255) not null,
    first_name varchar(32) default null, 
    last_name varchar(32) default null,
    email varchar(64) not null,
    account_type enum ('Admin', 'User') default null,
    facebook_account Boolean not null,
    tiktok_account Boolean not null,
    instagram_account Boolean not null,
    
    constraint min_length_password check (char_length(user_password) >= 8),
    primary key (user_id)
);

-- create admin view
create or replace view v_admin as (
	select * from users as U
		where U.account_type = 'Admin'
);

-- create regular user view
create or replace view v_user as (
	select * from users as U
		where U.account_type = 'User'
);

-- create campaigns table
create table if not exists campaigns (
    campaign_id int not null auto_increment,
    user_id int not null,
    campaign_name varchar(32) not null,
    links varchar(2048) default null,
    summarization varchar(2048) default null,
    advertisement_text varchar(2048) default null,
    advertisement_image varchar(255) default null,
    
    foreign key (user_id) references users(user_id)
		on delete cascade,
    primary key (campaign_id)
);
