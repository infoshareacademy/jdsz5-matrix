---- PODSTAWOWE STATYSTYKI STACJI (do kartodiagramów):

with l_wypozyczen_turystow as
-- liczba wypozyczen przez turystow
(select ss.id as stacja,
count (t.start_station_id) as l_wypozyczen
from station_sf ss 
join trip_sf t on t.start_station_id = ss.id
where subscription_type = 'Customer'
group by ss.id),

l_dojazdow_turystow as
-- liczba dojazdow przez turystow
(select ss.id as stacja,
count (t.end_station_id) as l_dojazdow
from station_sf ss 
join trip_sf t on t.end_station_id = ss.id
where subscription_type = 'Customer'
group by ss.id),

l_krazownikow as
-- liczba wypozyczen przez krążowników turystow
(select ss.id as stacja,
count (ss.id) as l_krazownikow
from station_sf ss 
join trip_sf t on t.end_station_id = ss.id
where subscription_type = 'Customer' and t.end_station_id = t.start_station_id
group by ss.id),

sr_l_rowerow as
-- srednia liczba dostepnych rowerow
(select s.id as stacja,
round(avg(ss.bikes_available)) as sr_dostepnych_rowerow
from station_sf s
join status_sf ss on ss.station_id = s.id
group by s.id),

atrakcje as
-- liczba atrakcji w poblizu stacji
(select 
id_stacji as stacja, 
l_restauracji,
l_atrakcji,
l_zabytkow + l_restauracji + l_atrakcji as atrakcje_all
from otoczenie_stacji_sf oss),

----------

wypozyczenia_srednie as
-- ile jest srednio lacznie wypozyczanych rowerow ze wszystkich stacji
(select count(start_station_id)/count(distinct start_station_id) as sr_wypoz_rowerow
from trip_sf ts),

srednie as
-- jaka jest srednia rowerow lacznie wszedzie na stacjach
(select round(avg(ss.bikes_available)) as sr_rowerow_ogolnie
from status_sf ss),

atrakcji_ogolnie as
--jaka jest srednia atrakcji lacznie przy wszystkich stacjach
(select
(sum(l_zabytkow) + sum(l_restauracji) + sum(l_atrakcji))/(3*count(id_stacji)) as atrakcji_srednio
from otoczenie_stacji_sf oss2) 


select

l_wypozyczen_turystow.stacja,

(case 
when l_wypozyczen > 16781 and sr_dostepnych_rowerow < 9 and atrakcje_all > 6 and l_atrakcji=1 then 'problematyczna, atrakcyjna'
when l_wypozyczen < 16781 and sr_dostepnych_rowerow < 9 and atrakcje_all > 6 and l_atrakcji=1 then 'potencjalnie problematyczna, atrakcyjna'
when l_wypozyczen > 16781 and sr_dostepnych_rowerow < 9 and atrakcje_all < 6 and l_atrakcji=1 then 'problematyczna, ciekawa'
when l_wypozyczen < 16781 and sr_dostepnych_rowerow < 9 and atrakcje_all < 6 and l_atrakcji=1 then 'potencjalnie problematyczna, ciekawa'
when l_wypozyczen > 16781 and sr_dostepnych_rowerow < 9 then 'problematyczna'
when atrakcje_all > 6 and l_atrakcji=1 then 'ok, atrakcyjna'
when atrakcje_all < 6 and l_atrakcji=1 then 'ok, ciekawa'

else '0' end)::text as ocena_stacji,

l_wypozyczen,
l_dojazdow,
l_krazownikow,
sr_dostepnych_rowerow,
atrakcje_all,
l_restauracji,
l_atrakcji
from l_wypozyczen_turystow
join l_dojazdow_turystow on l_dojazdow_turystow.stacja = l_wypozyczen_turystow.stacja
join l_krazownikow on l_krazownikow.stacja = l_wypozyczen_turystow.stacja
join sr_l_rowerow on sr_l_rowerow.stacja = l_wypozyczen_turystow.stacja
join atrakcje on atrakcje.stacja = l_wypozyczen_turystow.stacja

group by l_wypozyczen_turystow.l_wypozyczen, 
sr_l_rowerow.sr_dostepnych_rowerow, 
atrakcje.atrakcje_all, 
atrakcje.l_atrakcji, 
l_wypozyczen_turystow.stacja, 
l_dojazdow_turystow.l_dojazdow, 
l_krazownikow.l_krazownikow,
atrakcje.l_restauracji



--- ANALIZA ZALEZNOSCI

---- PODSTAWOWE STATYSTYKI STACJI (do kartodiagramów):

with l_wypozyczen_turystow as
-- liczba wypozyczen przez turystow
(select ss.id as stacja,
count (t.start_station_id) as l_wypozyczen
from station_sf ss 
join trip_sf t on t.start_station_id = ss.id
where subscription_type = 'Customer'
group by ss.id),

l_dojazdow_turystow as
-- liczba dojazdow przez turystow
(select ss.id as stacja,
count (t.end_station_id) as l_dojazdow
from station_sf ss 
join trip_sf t on t.end_station_id = ss.id
where subscription_type = 'Customer'
group by ss.id),

l_krazownikow as
-- liczba wypozyczen przez krążowników turystow
(select ss.id as stacja,
count (ss.id) as l_krazownikow
from station_sf ss 
join trip_sf t on t.end_station_id = ss.id
where subscription_type = 'Customer' and t.end_station_id = t.start_station_id
group by ss.id),

sr_l_rowerow as
-- srednia liczba dostepnych rowerow
(select s.id as stacja,
round(avg(ss.bikes_available)) as sr_dostepnych_rowerow
from station_sf s
join status_sf ss on ss.station_id = s.id
group by s.id),

atrakcje as
-- liczba atrakcji w poblizu stacji
(select 
id_stacji as stacja,
l_atrakcji,
l_zabytkow,
l_restauracji,
l_zabytkow + l_restauracji + l_atrakcji as atrakcje_all
from otoczenie_stacji_sf oss)

select 

corr(sr_dostepnych_rowerow, atrakcje_all) as atrakcje_all_a_dost_rowery,
corr(sr_dostepnych_rowerow, l_atrakcji) as atrakcje_a_dost_rowery,
corr(sr_dostepnych_rowerow, l_zabytkow) as zabytki_a_dost_rowery,
corr(sr_dostepnych_rowerow, l_restauracji) as resautracje_a_dost_rowery,
corr(sr_dostepnych_rowerow, l_dojazdow) as atrakcje_a_l_dojazdow,
corr(sr_dostepnych_rowerow, l_wypozyczen) as atrakcje_a_l_wypozyczen
OUTP
from l_wypozyczen_turystow
join l_dojazdow_turystow on l_dojazdow_turystow.stacja = l_wypozyczen_turystow.stacja
join l_krazownikow on l_krazownikow.stacja = l_wypozyczen_turystow.stacja
join sr_l_rowerow on sr_l_rowerow.stacja = l_wypozyczen_turystow.stacja
join atrakcje on atrakcje.stacja = l_wypozyczen_turystow.stacja