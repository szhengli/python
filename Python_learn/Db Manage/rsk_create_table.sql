create table %s(id int auto_increment not null primary key
,rankid int
,company_code varchar(100)
,company_name varchar(100)
,company_id bigint
,buy_product varchar(500)
,sell_product varchar(500)
,limits varchar(500)
,final_rsk varchar(50)
,rsk_id int
,expired_date datetime
,key idx_company_name(company_name)
);