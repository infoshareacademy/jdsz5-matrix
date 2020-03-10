--Na podstawie poniższej analizy SQL dokonałam rozróżnienia abomentów od okazjonalnych przejazdów
--1. Jednorazowe wypożyczenia stanowią 13% wszystkich wypożyczeń, ale w czasie stanowią ok 42% czasu wszystkich przejazdów - więc jest to bardzo ciekawa grupa do analizy.
--2. Szczyt wypożyczeń dla subskrybentów to godziny 8 i 17, a dla wypożyczeń jednorazowych największa aktywność odbywa się między 11 a 17, czyli w standardowych godzinach pracy
--3. Użytkownicy abonamentowi najczęciej wypożyczają rowery od poniedziałku do piątku, przy czym piątek jest zdecydowanie słabszy od pozostaych dni roboczych, 
--   natomiast dla wypożyczeń jednorazowych największa koncentracja jest od piątku do niedzieli
--4. U użytkowników abonamentowych wypożyczenia poniżej 20 minut to 98% wypożyczeń, dla użytkowników jednorazowych 20 minutowe przejazdy to tylko 56% wypożyczeń
--5. Wahania sezonowe są większe dla okazjonalnych wypożyczeń niż dla abonamentów, początek i koniec roku są zdecydowanie słabsze niż w okresie wiosny i lata (miesiące 5-8)
--6. 13% osób wypożyczjących rowery okazjonalnie rozpoczynają i kończą podróż w tym samym miejscu, wśród aboamentów to tylko 1% przejazdów
--7. Wnioskując z powyższych podpunktów - abonamenci wykorzystują rowery przede wszystkim na dojazdy do pracy, a użytkownicy jednorazowi na aktywności turystyczne


--podstawowe różnice między jednorazowymi przejazdami a subskrybcjami: 
--ile jednorazowe wypożyczenia stanowią w całkowitej ilości wypożyczeń i w całkowitej długości przejazdu?
with miary as
(select subscription_type, count(t.id) as ilosc_wypo, avg(duration)/60 as sr_dl_przejazdu, sum(duration/60) as czas_total
from trip_sf t
group by subscription_type)

select subscription_type, ilosc_wypo, ilosc_wypo/sum(ilosc_wypo) over ()::numeric as proc_wypo_cust, 
       sr_dl_przejazdu, czas_total, czas_total/sum(czas_total) over ()::numeric as proc_trwania_cust
from miary

--WNIOSEK: 
-- - jednorzaowe wypożyczenia to 13% wszystkich wypożyczeń, ale są zdecydowanie dłuższe od przejazdów subskrybentów i stanowią ok 42% czasu wszystkich przejazdów.
-- - jeżeli system poboru opłat byłby skonstruuowany w oparciu o długość wypożyczenia to grupa jednorazowych użytkowników byłaby zdecydowanie bardziej dochodowa od subskrybentów

--Jak często odstawiane są rowery na tą samą stację w zależności od typu użytkownika? i jak długo trwają przejazdy?
with miary as
(select subscription_type, case when start_station_id=end_station_id then 'krążowniki' else 'sprinterzy' end as typ,
 count(t.id) as ilosc_wypo, avg(duration)/60 as sr_dl_przejazdu, sum(duration/60) as czas_total
from trip_sf t
group by subscription_type, typ)

select subscription_type, typ, ilosc_wypo, ilosc_wypo/sum(ilosc_wypo) over (partition by subscription_type)::numeric as proc_wypo, 
       sr_dl_przejazdu, czas_total, czas_total/sum(czas_total) over (partition by subscription_type)::numeric as proc_trwania
from miary

--WNIOSKI: 
-- - 13% osób wypożyczjących rowery okazjonalnie rozpoczynają i kończą podróż w tym samym miejscu (późniejsza analiza Hani pokazała, że nie są to dworzec główny)
-- - osoby wypożyczajace rowery okazjonalnie zdecydowanie częściej oddają rowery na stacji wypożczenia niż abonamenci - robi to tylko 1% abonamentów

--Czy godziny szczytu wypożyczeń różnią się w zależności od typu użytkownika? Analiza średnia per dzień
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

--WNIOSKI: 
-- - godziny największych ilości wypożyczeń róźnią się w zależności od typu użytkownika
-- - szczyt wypożyczeń dla subskrybentów to godziny 8 i 17, co wskazuje na podróże do pracy i powrotne z pracy do domu
-- - dla wypożyczeń jednorazowych nie ma aż tak zdecydowanych godzin szczytu, ale największa aktywność odbywa się między 11 a 17, czyli w standardowych godzinach pracy


--Czy rozkład ilości wypożyczeń w ciagu tygodnia (ponidziałek-niedziela) różni się od typu użytkownika?
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

--WNIOSKI: 
-- - dni z największą ilością wypożyczeń zdecydowanie różnią się w zależności od typu użytkownika
-- - użytkownicy abonamentowi najczęściej wypożyczają rowery od poniedziałku do piątku, przy czym piątek jest zdecydowanie słabszy od pozostałych dni roboczych,
--   co wskazuje na dojazdy do pracy
-- - dla wypożyczeń jednorazowych największa koncentracja jest od piątku do niedzieli, wskazuje to na ruch turystyczny


--Czy długość trwania wypożyczenia zależy od typ użytkownika?

-- Rozkład kwantylowy długości trawania wypożczeń w minutach
select t1.rzad_kwantylu, dlugosc_cust, dlugosc_sub
from
(select
unnest(percentile_disc(array[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]) within group (order by duration/60)) as dlugosc_cust,
unnest(array[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]) as rzad_kwantylu
from trip_sf
where subscription_type = 'Customer') as t1
join
(select
unnest(percentile_disc(array[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]) within group (order by duration/60)) as dlugosc_sub,
unnest(array[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]) as rzad_kwantylu
from trip_sf
where subscription_type = 'Subscriber') as t2 on t1.rzad_kwantylu=t2.rzad_kwantylu;

--WNIOSKI: 
-- - rozkład długości trwania jazdy jest zupełnie inny dla abonamentów i okazjonanych użytkowników
-- - użytkownicy abonamentowi zdecydowanie częściej wypożyczają rowery na krótkotrwające przejazdy - 70% przejazdów jest poniżej 10 min, a 90% poniżej 14 min, 
--   mogą to być którkie trasy do pracy
-- - dla wypożyczeń jednorazowych krótkie przejazdy do 14 min to 40%

-- Rozkład ilości wypożyczeń w zależnosci od czasu trawnia przejazdu w minutach, w przedziałach co 5 min do godziny
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

--WNIOSKI: 
-- - u użytkowników abonamentowych wypożyczenia poniżej 20 minut to 98% wypożyczeń
-- - dla użytkowników jednorazowych 20 minutowe przejazdy to tylko 26% wypożyczeń
-- - dłuższe wypożyczenia charkateryzują raczej aktywności w wolnym czasie


--Czy wsytępuje sezonowość w wypożyczeniach rowerów i czy jest zależność między sezonowością, a typem użytkownika? 
--Czy przejazdy abonamenckie charakteryzują się stałym rozkładem w ciągu roku? 
with sezon1 as
(select date_part('month', start_date) as miesiac,
       count(case when date_part('year', start_date )='2013' then t.id end) as rok_2013,
       count(case when date_part('year', start_date )='2014' then t.id end) as rok_2014, 
       count(case when date_part('year', start_date )='2015' then t.id end) as rok_2015
from trip_sf t
where subscription_type = 'Subscriber'
group by miesiac)

select miesiac, rok_2013/sum(rok_2013) over () as rok_2013, rok_2014/sum(rok_2014) over () as rok_2014, rok_2015/sum(rok_2015) over () as rok_2015
from sezon1;

--WNIOSKI: 
-- - wahania sezonowe nie są duże dla subskrybentów - najsłabszy miesiąc w 2014 to luty, nieco lepszy grudzień, w miesiącach 6-10 wypożyczenia na pozimie 9% i wyżej,
--   w 2015 wygląda to inaczej - marzec jest taki sam jak kwiecień czy czerwiec
-- - za mało lat z pełnymi danymi, żeby wywnioskować o stałych charakterystykach sezonowych


--Czy w SF występuje wzmożony sezon trusystyczny?
with sezon2 as
(select date_part('month', start_date) as miesiac,
       count(case when date_part('year', start_date )='2013' then t.id end) as rok_2013,
       count(case when date_part('year', start_date )='2014' then t.id end) as rok_2014, 
       count(case when date_part('year', start_date )='2015' then t.id end) as rok_2015
from trip_sf t
where subscription_type = 'Customer'
group by miesiac)

select miesiac, rok_2013/sum(rok_2013) over () as rok_2013, rok_2014, rok_2014/sum(rok_2014) over () as rok_2014, rok_2015/sum(rok_2015) over () as rok_2015
from sezon2;

--WNIOSKI: 
-- - wahania sezonowe są większe dla okazjonalnych wypożyczeń niż dla abonamentów
-- - początek i koniec roku są zdecydowanie słabsze niż w okresie wiosny i lata (miesiące 5-8)

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


--Do sprawdzenia czy w pobliżu miejsc, gdzie wypożyczenia i odddania rowerów odbywają się na tej same stacji, są blisko punktów komunikacyjnych?
--Ranking stacji dokujących wg procentu oddawania na tej samej tacji
select s.id as id_stacji, name, lat, long, count(case when start_station_id=end_station_id then t.id end) as ilosc_wypo,
       count(case when start_station_id=end_station_id then t.id end)/count(t.id)::numeric as zgodnosc_stacji
from trip_sf t join station_sf s on t.start_station_id=s.id 
where subscription_type = 'Customer'
group by s.id, name, lat, long, dock_count
having count(case when start_station_id=end_station_id then t.id end)/count(t.id)::numeric > 0.13
order by zgodnosc_stacji desc


--Ranking stacji początkowych i końcowych dla wszystkich wypożyczeń
with 
start as 
(
select s.id as id_stacji, name, lat, long, dock_count,
--      count(case when subscription_type = 'Subscriber' then s.id end) as s_ilosc_start, 
       rank() over (order by count(case when subscription_type = 'Subscriber' then s.id end)  desc) as s_rank_start,
--       count(case when subscription_type = 'Customer' then s.id end) as c_ilosc_start, 
       rank() over (order by count(case when subscription_type = 'Customer' then s.id end)  desc) as c_rank_start
from station_sf s 
     join trip_sf t1 on s.id=t1.start_station_id
group by s.id, name, lat, long, dock_count
),
koniec as 
(
select s.id as id_stacji, name, lat, long, dock_count,
--       count(case when subscription_type = 'Subscriber' then s.id end) as s_ilosc_koniec, 
       rank() over (order by count(case when subscription_type = 'Subscriber' then s.id end)  desc) as s_rank_koniec,
--       count(case when subscription_type = 'Customer' then s.id end) as c_ilosc_koniec, 
       rank() over (order by count(case when subscription_type = 'Customer' then s.id end)  desc) as c_rank_koniec
from station_sf s 
     join trip_sf t1 on s.id=t1.end_station_id 
group by s.id, name, lat, long, dock_count
)

select s.id_stacji, s.name, s.lat, s.long, s.dock_count, s_rank_start, c_rank_start, s_rank_koniec, c_rank_koniec
from start s left outer join koniec k on s.id_stacji=k.id_stacji

--WNIOSKI: 
-- - raniking pierwszych trzech najbardziej oblganych stacji dokujących przez okazjonalnych użytkowników jest identyczny dla stacji ropoczynającyh i stacji końcowych
-- - abonamenci korzystają z większą częstotliwością z innych stacji niż jednorazowi użytkownicy


