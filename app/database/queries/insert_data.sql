-- fill users table
insert into users (username, password, first_name, last_name, account_type) values 
	('wolfofwallstreet', 'sellmethispen', 'Jordan', 'Belfort', 'Broker'),
	('moneyneversleeps', 'moneyneversleeps', 'Gordon', 'Gecko', 'Broker'),
	('test1234', 'test1234', 'Test', 'Test', 'Trader'),
    ('john_doe1', 'test1234', 'John', 'Doe', 'Trader'),
    ('jane_doe2', 'test1234', 'John', 'Doe', 'Trader'),
	('real_elon_musk', 'twitterismine', 'Elon', 'Musk', 'Trader'),
    ('not_a_reptile', 'itscalledmetanow', 'Mark', 'Zuckerberg', 'Trader'),
	('primetime', 'iloveamazon', 'Jeff', 'Bezos', 'Trader');
    
-- fill stocks table
insert into stocks (name, code) values
	('Google', 'GOOG'),
    ('Amazon', 'AMZN'),
    ('Tesla', 'TSLA'),
    ('Netflix', 'NFLX'),
    ('M&T Bank', 'MTB'),
	('Meta', 'META'),
	('NVIDIA', 'NVDA'),
	('Apple', 'AAPL'),
	('Visa', 'V'),
	('Walmart', 'WMT');
    
-- fill stock brokers table
call fill_stock_brokers();

-- fill shares table (for brokers)
call fill_broker_shares();
