create table fin (
    id int(12) unsigned not null auto_increment,
    symbol varchar(20) default null,
    month varchar(10) default null,
    year varchar(20) default null,
    key_text varchar(300) default null,
    key_type varchar(50) default null,
    value decimal(10,3),
    primary key(id),
    key idx_symbol (symbol),
    key idx_year (year),
    key idx_key_text (key_text),
    key key_type (key_type),
    unique key idx_symbol,year_month_key_text (symbol,year,month,key_text)
)
