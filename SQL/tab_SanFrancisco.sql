--zaptania tworzące nowe tabele z poprawnymi formatami, dodające klucze obce

CREATE TABLE station_sf (
	id int4 primary key,
	"name" text not NULL,
	lat numeric not NULL,
	long numeric not NULL,
	dock_count int4 not NULL,
	city text not NULL,
	installation_date DATE not NULL
);
INSERT INTO station_sf
select id, name, lat, long, dock_count, city, TO_DATE(installation_date, 'MM/DD/YYYY') as date
from station 
where city = 'San Francisco';
--select * from stationSF;

CREATE TABLE status_sf(
	station_id int4,
	bikes_available int4 not NULL,
	docks_available int4 not NULL,
	status_time timestamp not null,
	foreign key (station_id) references station_sf
);
insert into status_sf --tabela ograniczona do San Francisco
select station_id, bikes_available, docks_available, to_timestamp(time, 'YYYY/MM/DD HH24:MI') as status_time --sekundy nie mają zanczenia, więc je pominełam
from status join station_sf on status.station_id = station_sf.id --join z tabelą station2 zapewnia, że dane w tabeli status2 ogranicznmya tylko do San Francisco
select * from status_sf;

CREATE TABLE status_sf_h(
	station_id int4,
	status_time timestamp not null,
	min_bikes int4 not null,
	max_bikes int4 not null,
	min_docks int4 not null,
	max_docks int4 not null,
	foreign key (station_id) references station_sf
);
insert into status_sf_h --tabela ograniczona do San Francisco i obliczone min i max liczby rowerów i doków per satcja per godzina
select station_id, date_trunc('hour', status_time) as status_time,--sekundy nie mają zanczenia, więc je pominełam
        min(bikes_available) as min_bikes, max(bikes_available) as max_bikes, min(docks_available) as min_docks, max(docks_available) as max_docks
from status_sf
group by station_id, date_trunc('hour', status_time);
--select * from status_sf_h;

CREATE TABLE trip_sf (
	id int4 primary key,
	duration int4 not NULL,
	start_date timestamp not NULL,
	start_station_id int4,
	end_date timestamp not NULL,
	end_station_id int4,
	bike_id int4 not NULL,
	subscription_type text not NULL,
	zip_code int4 not NULL,
	foreign key (start_station_id) references station_sf,
	foreign key (end_station_id) references station_sf	
);
insert into trip_sf --wycieczki zaczynające i kończące w San Franciso
select t.id, duration, to_timestamp(start_date, 'MM/DD/YYYY HH24:MI') as start_date, start_station_id, 
       to_timestamp(end_date, 'MM/DD/YYYY HH24:MI') as end_date, end_station_id, bike_id, subscription_type, zip_code
from trip t join station_sf s on t.start_station_id = s.id 
            join station_sf s2 on t.end_station_id = s2.id
where zip_code is not null;
--select * from trip_sf;

CREATE TABLE weather_sf (
    date DATE,
    max_temperature_c NUMERIC,
    mean_temperature_c NUMERIC,
    min_temperature_c NUMERIC,
    max_dew_point_c INTEGER,
    mean_dew_point_c INTEGER,
    min_dew_point_c INTEGER,
    max_humidity INTEGER,
    mean_humidity INTEGER,
    min_humidity INTEGER,
    max_sea_level_pressure_inches NUMERIC,
    mean_sea_level_pressure_inches NUMERIC,
    min_sea_level_pressure_inches NUMERIC,
    max_visibility_miles INTEGER,
    mean_visibility_miles INTEGER,
    min_visibility_miles INTEGER,
    max_wind_Speed_mph INTEGER,
    mean_wind_speed_mph INTEGER,
    max_gust_speed_mph INTEGER,
    precipitation_inches INTEGER,
    cloud_cover INTEGER,
    events TEXT,
    wind_dir_degrees INTEGER,
    zip_code INTEGER not null);
   
INSERT INTO weather_sf
("date", max_temperature_c, mean_temperature_c, min_temperature_c, max_dew_point_c, mean_dew_point_c, min_dew_point_c, max_humidity, mean_humidity, 
min_humidity, max_sea_level_pressure_inches, mean_sea_level_pressure_inches, min_sea_level_pressure_inches, max_visibility_miles, mean_visibility_miles, 
min_visibility_miles, max_wind_speed_mph, mean_wind_speed_mph, max_gust_speed_mph, precipitation_inches, cloud_cover, events, wind_dir_degrees, zip_code)
select TO_DATE(date, 'MM/DD/YYYY') as date
       ,round(((max_temperature_f - 23)/1.8), 1) as max_temperature_c
       ,round(((mean_temperature_f - 23)/1.8), 1) as mean_temperature_c
       ,round(((min_temperature_f - 23)/1.8), 1) as min_temperature_c
       ,round(((max_dew_point_f - 23)/1.8), 1) as max_dew_point_c
       ,round(((mean_dew_point_f - 23)/1.8), 1) as mean_dew_point_c
       ,round(((min_dew_point_f - 23)/1.8), 1) as min_dew_point_c
       ,max_humidity
       ,mean_humidity
       ,min_humidity
       , max_sea_level_pressure_inches
       , mean_sea_level_pressure_inches
       , min_sea_level_pressure_inches
       , max_visibility_miles
       , mean_visibility_miles
       , min_visibility_miles
       , max_wind_speed_mph
       , mean_wind_speed_mph
       , max_gust_speed_mph
       , precipitation_inches
       , cloud_cover
       , events
       , wind_dir_degrees
       , zip_code
FROM weather w
where zip_code in (select distinct zip_code from trip_sf);
--select * from weather_sf;

