CREATE DATABASE trend2;
USE trend2;
create table dur2_trend(
id int(10) primary key not null auto_increment, 
ma10 float not null,
ma20 float not null,
cur float not null,
ask float not null,
bid float not null,
p_ask float not null,
p_bid float not null,
time timestamp
);

create table ch_rates(
id int(10) primary key not null auto_increment, 
cur float not null,
cur_gap_5s float not null,
cur_gap_10s float not null,
cur_gap_20s float not null,
time timestamp
);

create table standard_quo(
id int(10) primary key not null auto_increment, 
cur float not null,
ma10 float not null,
ma20 float not null,
delta_ma10_ma3 float not null,
delta_ma20_ma3 float not null,
time timestamp
);


create table dur5_trend(
id int(10) primary key not null auto_increment, 
ma10 float not null,
ma20 float not null,
cur float not null,
ask float not null,
bid float not null,
p_ask float not null,
p_bid float not null,
time timestamp
);

CREATE DATABASE day_review_01;
USE day_review_01;
create table day_data(
id               int(10)    primary key,
cur              float      not null,
time             datetime,
zma10            float,
zma20            float,
delta_zma10      float,
delta_zma20      float, 
delta_zma10_ma60 float,
delta_zma20_ma60 float,
ratio            float,
zma_gap          float,
zma_gap_ratio    float
);
alter table day_data add column dalta_zma20_zma60_ratio float;
alter table day_data add column zma20_ratio_ratio float;
delete from dur2_trend where time > '2017-04-25 12:00:00' and time < '2017-04-25 13:00:00';
delete from standard_quo where time > '2017-09-04 11:58:54' and time < '2017-09-04 12:58:54';

delete * from day_data_new_a where time > '2017-09-04 9:20:00' and time < '2017-09-04 16:00:00';
select * from ch_rates where time > '2017-07-06 9:30:00' and time < '2017-07-06 16:00:00' into outfile 'c://ProgramData/MySQL/MySQL Server 5.7/Uploads/ch_rates.csv';
select * from standard_quo where time > '2017-08-25 9:20:00' and time < '2017-08-25 16:00:00' into outfile 'c://ProgramData/MySQL/MySQL Server 5.7/Uploads/standard_0825.csv';
select * from standard_quo where time > '2017-07-04 9:20:00' and time < '2017-07-04 16:00:00' into outfile 'c://ProgramData/MySQL/MySQL Server 5.7/Uploads/standard_0704.csv';
create table day_data_new(
id               int(10)    primary key,
cur              float      not null,
time             datetime,
zma10            float,
zma20            float,
zma10_ratio            float,
zma20_ratio            float,
zma20_ratio_ratio      float,
zma_gap                float,
zma_gap_ratio          float,
zma_gap_ratio_ratio    float,
cur_ratio              float
);

create table day_data_new_a(
id               int(10)    ,
cur              float      not null,
time             datetime,
zma10            float,
ma20            float,
zma10_ratio            float,
zma10_ratio_ratio            float,
zma10_ratio_ratio_ratio      float,
trade_mark      float,
ma20_ratio                float,
zma10_ratio_ratio_short          float
);

create table day_data_new_b(
id                      int(10) primary key,,
cur                     float not null,
time                    datetime,
zmab                    float,
zmab_ratio              float,
zmab_ratio_short        float,
zmab_ratio_ratio        float,
zma1                    float,
zma1_ratio              float,
zma1_ratio_short        float,
zma1_ratio_ratio        float,
zma5                    float,
zma5_ratio              float,
zma5_ratio_ratio        float,
zma10                   float,
zma10_ratio             float,
zma10_ratio_ratio       float,
zma10_ratio_ratio_short float,
zma10_ratio_ratio_ratio float,
ma20                    float,
ma20_ratio              float,
zma50                   float,
zma50_ratio             float,
zma1_zma10_gap          float,
zma1_zma10_gap_scope    float
);


create table adjust_parameters(
para_index int not null primary key not null auto_increment,
zma10_ratio            float,
zma20_ratio            float,
zma10_ratio_ratio      float,
zma20_ratio_ratio      float,
zma_gap_min            float,
zma_gap_max            float,
zma_gap_ratio          float,
zma_gap_ratio_ratio    float
);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.002,             0);







insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.002,             0.000001);






insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.002,             0.000002);



insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000001,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0,                 0.000002,                 5,           15,          0.002,             0.000003);


create table trade_mark(
mark_id int(10) primary key not null auto_increment,
id int(10) not null,
para_index float ,
trade_mark float 
);

create table judge_result(
ret_id int(10) primary key not null auto_increment,
id int(10) not null,
action int,
result float,
turn_pos int,
turn_gap float,
para_index int
);



















insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.002,             0);







insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000001);






insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000002);



insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000001,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000002,                 0.000002,                 5,           15,          0.002,             0.000003);


















insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.002,             0);







insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000001);






insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000002);



insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000001,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000003,                 0.000002,                 5,           15,          0.002,             0.000003);















insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.002,             0);







insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000001);






insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000002);



insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000001,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000004,                 0.000002,                 5,           15,          0.002,             0.000003);
















insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.001,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.001,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.002,             0);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.002,             0);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.002,             0);







insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000001);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000001);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000001);






insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000002);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000002);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000002);



insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.001,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000001,                 5,           15,          0.002,             0.000003);

insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.005,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.004,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000003);
insert into adjust_parameters
(zma10_ratio, zma20_ratio, zma10_ratio_ratio, zma20_ratio_ratio, zma_gap_min, zma_gap_max, zma_gap_ratio, zma_gap_ratio_ratio)values
(0,           0.003,       0.000005,                 0.000002,                 5,           15,          0.002,             0.000003);








