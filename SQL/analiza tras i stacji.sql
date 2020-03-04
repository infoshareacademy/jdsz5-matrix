select * from trip_sf
select * from station_sf
select * from status_sf

-- Sprawdzenie wszystkich powiązań między stacjami 
-- w zależności czy użytkownik jest użytkownikiem abonmentowym czy jednorazowym

select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type 
from trip_sf t 
group by subscription_type, start_station_id, end_station_id
order by start_station_id desc

--Wybór 10 najpopularniejszych tras dla: 1/ użytkowników abanomentowych, 2/ dla użytkowników jednorazowych
-- do pokazaniu dokładnego przebiegu tras na mapie

-- dla abonamentowców
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Subscriber' and start_station_id != end_station_id
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 10;
-- dla użytkowników jednorazowych
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 10;

-- Wybór po 5 tras dla określonych czasów przejazdów: 30 min, 1h, 2h, 5h

-- dla 30 minutowych przyjazdów
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 1800
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;
-- dla 60 minutowych przyjazdów
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 3600 and duration > 1800
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;
--dla 2 godzinnych przejazdów
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 7200 and duration > 3600
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;
-- dla 5 godzinnych przjeazdów
select  
(sum (duration)/ count(id)) as sr_dl_przejazdu, 
count (id) as l_przejazdow, 
start_station_id, 
end_station_id,
subscription_type
from trip_sf t 
where subscription_type = 'Customer' and start_station_id != end_station_id and duration < 18000 and duration > 7200
group by subscription_type, start_station_id, end_station_id
order by l_przejazdow desc
limit 5;

-- Obliczenie średniej liczby rowerów dostępnych na stacji oraz liczby podróży do tej stacji,
-- żeby następnie porównać
-- z liczbą dostępnych atrakcji w zasięgu 10 min od stacji

select end_station_id,  
count (end_station_id) as l_dojazdow
from trip_sf t
where subscription_type = 'Customer'
group by end_station_id

select station_id ,
round(avg(bikes_available)) as sr_rowerow
from status_sf s
group by station_id 

--- jako jedno zapytanie 

select end_station_id,  
count (end_station_id) as l_dojazdow,
round(avg(bikes_available)) as sr_rowerow
from trip_sf t

full join status_sf s on t.end_station_id = s.station_id
where subscription_type = 'Customer'
group by end_station_id

---

-- Tabela, którą tutaj tworzę pokazuje ile jest jest zabytków i ile restauracji w sąsiedztwie stacji
-- Dane pobrane z OpenStreetMap, agregacja zrobiona w QGis

create table otoczenie_stacji_sf(
	id integer primary key,
	id_stacji integer,
	l_zabytkow integer,
	l_restauracji integer,
	foreign key (id_stacji) references station_sf
);
insert into otoczenie_stacji_sf
	(id, id_stacji, l_zabytkow, l_restauracji)
	values
(1,39,0,15),
(2,41,1,4),
(3,42,1,39),
(4,45,1,59),
(5,46,0,25),
(6,47,2,41),
(7,48,0,2),
(8,49,1,4),
(9,50,9,17),
(10,51,0,14),
(11,54,1,2),
(12,55,0,7),
(13,56,2,11),
(14,57,0,9),
(15,58,2,3),
(16,59,0,14),
(17,60,0,12),
(18,61,0,29),
(19,62,2,8),
(20,63,1,1),
(21,64,0,8),
(22,65,0,6),
(23,66,0,8),
(24,67,0,10),
(25,68,2,21),
(26,69,0,7),
(27,70,0,8),
(28,71,0,30),
(29,72,1,11),
(30,73,0,78),
(31,74,1,7),
(32,75,5,20),
(33,76,2,17),
(34,77,2,18),
(35,82,4,31)

select * from otoczenie_stacji_sf

-- Sprawdzam czy jest jakaś zależność między liczbą dojazdów do danej stacji a zlokalizowanymi w jej sąsiedztwie zabytkami oraz restauracjami

select 
corr(liczba_dojazdow.l_dojazdow, l_zabytkow) as zabytki_dojazdy, -- wynik 0,18
corr(liczba_dojazdow.l_dojazdow, l_restauracji) as restauracje_dojazdy -- wynik -0,004
from otoczenie_stacji_sf o

join
(select end_station_id,  
count (end_station_id) as l_dojazdow
from trip_sf t
where subscription_type = 'Customer'
group by end_station_id) as liczba_dojazdow 
on liczba_dojazdow.end_station_id = o.id_stacji

-- WNIOSEK: Brak wyraznej zależności. 

-- Sprawdzam czy jest jakaś zależność między średnią liczbą rowerów na stacji a zlokalizowanymi w jej sąsiedzwie atrakcjami

select 
corr(srednia_rowerow_dostepnych.sr_rowerow, l_zabytkow) as zabytki_dost_rowery, -- wynik 0,06
corr(srednia_rowerow_dostepnych.sr_rowerow, l_restauracji) as restauracje_dost_rowery -- wynik -0,17
from otoczenie_stacji_sf o

join
(select station_id,
round(avg(bikes_available)) as sr_rowerow
from status_sf s
group by station_id) as srednia_rowerow_dostepnych
on srednia_rowerow_dostepnych.station_id = o.id_stacji

-- WNIOSEK: Przy stacjach w sąsiedztwie nagromadzenia restauracji należałoby zadbać o zwiększenie liczby rowerów.