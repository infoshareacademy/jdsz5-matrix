# DANE WYJŚCIOWE

## Slajd: "Najbliższe stacje rowerowe przy atrakcjach turystycznych".
+ zapytanie SQL wyznaczjące odległość między daną atrakcją turystyczną i najbliższą stacją rowerową, wyrażona w jednostce [m]:

```sql
with krok_1 as
(
select s.id as id_station, s.name as name_station, ta.id as id_attraction, ta.name as name_attraction,
point(s.long, s.lat) <@> point(ta.long, ta.lat)::point as distance_mile
from tourist_attraction ta, station s
where s.city = 'San Francisco' and (point(s.long, s.lat) <@> point(ta.long, ta.lat)) = (select min(point(s.long, s.lat) <@> point(ta.long, ta.lat)::point) from station s)
order by ta.id asc
),
krok_2 as 
(select *,
round(distance_mile * 1609.344) as distance_meter
from krok_1
)
select * from krok_2;
```
## Slajd: "Przykładowe trasy rowerowe obejmujące atrakcje turystyczne".
+ zapytanie SQL wyznaczające średni czas przejazdu użytkowników między określonymi dwoma stacjami rowerowymi.
+ odrzucanych jest 5% najkrótszych i najdłuższych przejazdów 
+ pomijane są trasy ropoczynające się i konczące w tym samym punkcie

```sql
with kwantyle as
(select start_station_id, end_station_id,
percentile_disc(0.05) within group (order by duration/60) as poniżej_5_proc,
percentile_disc(0.95) within group (order by duration/60) as powyzej_95_proc
from trip_sf
where subscription_type = 'Customer' and start_station_id <> end_station_id 
group by start_station_id , end_station_id),

srednie_czasy as
(select ts.start_station_id, ts.end_station_id, avg(duration/60) as avg_duration
from trip_sf ts inner join kwantyle k on ts.start_station_id = k.start_station_id and ts.end_station_id = k.end_station_id
where duration/60 between poniżej_5_proc and powyzej_95_proc --and ts.start_station_id=50 and ts.end_station_id=61
group by ts.start_station_id, ts.end_station_id)

select start_station_id, s.name as start_station_name, end_station_id, e.name as end_station_name, avg_duration
from srednie_czasy as ac 
left outer join station_sf as s on ac.start_station_id = s.id 
left outer join station_sf as e on ac.end_station_id = e.id;
```
## SLAJD TYPY UŻYTKOWNIKÓW
+ przedstawia podstawowe różnice między jednorazowymi przejazdami a przejazdami w ramach abonamentu
+ odpowiada na pytanie ile jednorazowe wypożyczenia stanowią w całkowitej ilości wypożyczeń i w całkowitej długości przejazdu

```sql
with miary as
(select subscription_type, count(t.id) as ilosc_wypo, avg(duration)/60 as sr_dl_przejazdu, sum(duration/60) as czas_total
from trip_sf t
group by subscription_type)

select subscription_type, ilosc_wypo, ilosc_wypo/sum(ilosc_wypo) over ()::numeric as proc_wypo_cust, 
       sr_dl_przejazdu, czas_total, czas_total/sum(czas_total) over ()::numeric as proc_trwania_cust
from miary
```

### WNIOSEK: 
+ jednorzaowe wypożyczenia to 13% wszystkich wypożyczeń, ale są zdecydowanie dłuższe od przejazdów subskrybentów i stanowią ok 42% czasu wszystkich przejazdów.
+ jeżeli system poboru opłat byłby skonstruuowany w oparciu o długość wypożyczenia to grupa jednorazowych użytkowników byłaby zdecydowanie bardziej dochodowa od subskrybentów


## SLAJD ZACHOWANA UŻYTKOWNIKÓW OKAZJONALNYCH
+ odpowiada na pytanie jak często odstawiane są rowery na tą samą stację i jak długo trwają przejazdy w zależności od typu użytkownika
```sql
with miary as
(select subscription_type, case when start_station_id=end_station_id then 'krążowniki' else 'sprinterzy' end as typ,
 count(t.id) as ilosc_wypo, avg(duration)/60 as sr_dl_przejazdu, sum(duration/60) as czas_total
from trip_sf t
group by subscription_type, typ)

select subscription_type, typ, ilosc_wypo, ilosc_wypo/sum(ilosc_wypo) over (partition by subscription_type)::numeric as proc_wypo, 
       sr_dl_przejazdu, czas_total, czas_total/sum(czas_total) over (partition by subscription_type)::numeric as proc_trwania
from miary
```
### WNIOSKI: 
+ 13% osób wypożyczjących rowery okazjonalnie rozpoczynają i kończą podróż w tym samym miejscu (późniejsza analiza Hani pokazała, że nie jest to dworzec główny)
+ osoby wypożyczajace rowery okazjonalnie zdecydowanie częściej oddają rowery na stacji wypożczenia niż abonamenci - robi to tylko 1% abonamentów


## SLAJD TYPY UŻYTKOWNIKÓW - GODZINY PRZEJAZDÓW
+ odpowiada na pytanie czy godziny szczytu wypożyczeń różnią się w zależności od typu użytkownika - analiza średnio per dzień
```sql
with wypo1 as 
(select date_part('hour', start_date) as godzina, count(id)/count(distinct EXTRACT(DAY FROM start_date)) as ilosc_wypozyczen,
count(case when subscription_type = 'Subscriber' then id end)/count(distinct EXTRACT(DAY FROM start_date)) as Subscriber,
count(case when subscription_type = 'Customer' then id end)/count(distinct EXTRACT(DAY FROM start_date))  as Customer
from trip_sf
group by godzina)
,
wypo2 as
(select *, Subscriber/sum(Subscriber) over ()::numeric as ds, Customer/sum(Customer) over ()::numeric as dc
from wypo1)
,
wypo3 as
(select *, ln(ds/dc) woe, ds - dc dsdc, ln(ds/dc)*(ds-dc) dsdc_woe
from wypo2)

select *, sum(dsdc_woe) over() iv
from wypo3;
```
### WNIOSKI: 
+ godziny największych ilości wypożyczeń róźnią się w zależności od typu użytkownika
+ szczyt wypożyczeń dla subskrybentów to godziny 8 i 17, co wskazuje na podróże do pracy i powrotne z pracy do domu
+ dla wypożyczeń jednorazowych nie ma aż tak zdecydowanych godzin szczytu, ale największa aktywność odbywa się między 11 a 17, czyli w standardowych godzinach pracy


## SLAJD TYPY UŻYTKOWNIKÓW - ROZKŁAD WG DNI TYGODNIA
+ odpowiada na pytanie czy rozkład ilości wypożyczeń w ciagu tygodnia (ponidziałek-niedziela) różni się od typu użytkownika?
```sql
with wypo1 as 
(select to_char(start_date, 'day') as dzien_tygodnia, count(id)/count(distinct EXTRACT(DAY FROM start_date)) as ilosc_wypozyczen,
count(case when subscription_type = 'Subscriber' then id end)/count(distinct EXTRACT(DAY FROM start_date)) as Subscriber,
count(case when subscription_type = 'Customer' then id end)/count(distinct EXTRACT(DAY FROM start_date)) as Customer
from trip_sf
group by dzien_tygodnia)
,
wypo2 as
(select *, Subscriber/sum(Subscriber) over ()::numeric as ds, Customer/sum(Customer) over ()::numeric as dc
from wypo1)
,
wypo3 as
(select *, ln(ds/dc) woe, ds - dc dsdc, ln(ds/dc)*(ds-dc) dsdc_woe
from wypo2)

select *, sum(dsdc_woe) over() iv
from wypo3
order by customer
```
### WNIOSKI: 
+ dni z największą ilością wypożyczeń zdecydowanie różnią się w zależności od typu użytkownika
+ użytkownicy abonamentowi najczęściej wypożyczają rowery od poniedziałku do piątku, przy czym piątek jest zdecydowanie słabszy od pozostałych dni roboczych, co wskazuje na dojazdy do pracy
+ dla wypożyczeń jednorazowych największa koncentracja jest od piątku do niedzieli, wskazuje to na ruch turystyczny


## SLAJD TYPY UŻYTKOWNIKÓW - SEZONOWOŚĆ
+ za mało lat z pełnymi danymi, żeby wywnioskować o stałych charakterystykach sezonowych, do azalizy wzięłam rok z pełnymi danymi, czyi 2014
+ Czy wsytępuje sezonowość w wypożyczeniach rowerów i czy jest zależność między sezonowością, a typem użytkownika? 
+ Czy przejazdy abonamenckie charakteryzują się stałym rozkładem w ciągu roku? 
+ Czy w SF występuje wzmożony sezon trusystyczny?
```sql
with sezon2014 as
(select date_part('month', start_date) as miesiac,
       count(case when subscription_type = 'Customer' then t.id end) as Customer, 
       count(case when subscription_type = 'Subscriber' then t.id end) as Subscriber
from trip_sf t
where date_part('year', start_date )='2014'
group by miesiac)
,
sezon2 as
(select *, Subscriber/sum(Subscriber) over ()::numeric as ds, Customer/sum(Customer) over ()::numeric as dc
from sezon2014)
,
sezon3 as
(select *, ln(ds/dc) woe, ds - dc dsdc, ln(ds/dc)*(ds-dc) dsdc_woe
from sezon2)

select *, sum(dsdc_woe) over() iv
from sezon3
```
### WNIOSKI: 
+ wahania sezonowe są większe dla okazjonalnych wypożyczeń niż dla abonamentów
+ początek i koniec roku są zdecydowanie słabsze niż w okresie wiosny i lata (miesiące 5-8)


## SLAJD TYPY UŻYTKOWNIKÓW - ROZKAD WG DŁUGOŚCI JAZDY
+ odpowiada na pytanie czy długość trwania wypożyczenia zależy od typ użytkownika
+ poniżej rozkład ilości wypożyczeń w zależnosci od czasu trawnia przejazdu w minutach, w przedziałach co 5 min do godziny
```sql
with wypo1 as 
(select case when duration/60<5 then 5 
             when duration/60<10 then 10 
             when duration/60<15 then 15 
             when duration/60<20 then 20 
             when duration/60<25 then 25 
             when duration/60<30 then 30 
             when duration/60<35 then 35 
             when duration/60<40 then 40 
             when duration/60<45 then 45
             when duration/60<50 then 50
             when duration/60<55 then 55 else 60 end as trwanie, 
count(id) as ilosc_wypozyczen,
count(case when subscription_type = 'Subscriber' then id end) as Subscriber,
count(case when subscription_type = 'Customer' then id end) as Customer
from trip_sf
group by trwanie
order by trwanie )
,
wypo2 as
(select *, Subscriber/sum(Subscriber) over ()::numeric as ds, Customer/sum(Customer) over ()::numeric as dc
from wypo1)
,
wypo3 as
(select *, ln(ds/dc) woe, ds - dc dsdc, ln(ds/dc)*(ds-dc) dsdc_woe
from wypo2)

select *, sum(dsdc_woe) over() iv
from wypo3
```
### WNIOSKI: 
+ rozkład długości trwania jazdy jest zupełnie inny dla abonamentów i okazjonanych użytkowników
+ u użytkowników abonamentowych wypożyczenia poniżej 20 minut to 98% wypożyczeń, są to krótkie trasy do pracy
+ dla użytkowników jednorazowych 20 minutowe przejazdy to tylko 26% wypożyczeń
+ dłuższe wypożyczenia charkateryzują raczej aktywności w wolnym czasie

## PODSTAWOWE STATYSTYKI STACJI (do kartodiagramów):
+ stworzenie map
```sql
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
```


## ANALIZA ZALEŻNOŚCI

+ podstawowe statystyki stacji (do kartodiagramów):
```sql
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
```