-- 5 najpopularniejszych tras dla przejazdów w przedziale 10-20 z kwantyli.
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 1200 and duration > 600
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;

-- 5 najpopularniejszych tras dla przejazdów w przedziale 55-65 z kwantyli.

select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 3900 and duration > 3300
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;

-- 
select * from tourist_attraction

--
select end_station_id,  
count (end_station_id) as l_dojazdow
from trip_sf t
where subscription_type = 'Customer'
group by end_station_id



-- dla abonamentowców
select  
((sum (duration)/ count(id)))/60 as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Subscriber' and start_station_id != end_station_id
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 15;
-- dla użytkowników jednorazowych
select  
((sum (duration)/ count(id)))/60 as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 15;

select * from otoczenie_stacji_sf oss 

-- Sprawdzam czy jest jakaś zależność między średnią liczbą rowerów na stacji a zlokalizowanymi w jej sąsiedzwie atrakcjami

select 
corr(srednia_rowerow_dostepnych.sr_rowerow, l_zabytkow) as zabytki_dost_rowery, -- wynik ogolnie: 0,06 | turysci: 0,43
corr(srednia_rowerow_dostepnych.sr_rowerow, l_restauracji) as restauracje_dost_rowery, -- wynik ogolnie: -0,17 |  turysci: -0,05
corr(srednia_rowerow_dostepnych.sr_rowerow, l_atrakcji) as atrakcje_dost_rowery -- wynik ogolnie: -0,26 | turysci: -0,2
from otoczenie_stacji_sf o

join trip_sf t on t.end_station_id = o.id_stacji

join
(select station_id,
round(avg(bikes_available)) as sr_rowerow
from status_sf s
group by station_id) as srednia_rowerow_dostepnych
on srednia_rowerow_dostepnych.station_id = o.id_stacji

where subscription_type = 'Customer'


select * from trip t2 
select * from station_sf

-- podstawowe statystyki stacji
select 
select end_station_id,  
count (end_station_id) as l_dojazdow
from trip_sf t
where subscription_type = 'Customer'
group by end_station_id



---- PODSTAWOWE STATYSTYKI STACJI (do kartodiagramów):

select 
id as stacja,
count (ts.end_station_id) as l_dojazdow,
count (ts.start_station_id) as l_wypozyczen,
oss.l_restauracji,
oss.l_atrakcji,
oss.l_zabytkow,
oss.l_restauracji + oss.l_atrakcji + oss.l_zabytkow as atrakcje_all,
round(avg(ss.bikes_available)) as srednia_l_rowerow

from station_sf ss 

join trip_sf ts on  
join otoczenie_stacji_sf oss  on oss.id_stacji = ts.id
join status_sf ss on ss.station_id = ts.id


where ts.subscription_type = 'Customer'
group by ss.id

select * from status_sf ss 
select * from otoczenie_stacji_sf oss