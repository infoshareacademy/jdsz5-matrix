-- SLAJD TYPY UŹYTKOWNIKÓW
-- przedstawia podstawowe różnice między jednorazowymi przejazdami a przejazdami w ramach abonamentu
-- odpowiada na pytanie ile jednorazowe wypożyczenia stanowią w całkowitej ilości wypożyczeń i w całkowitej długości przejazdu
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


-- SLAJD ZACHOWANA UŻYTKOWNIKÓW OKAZJONALNYCH
-- odpowiada na pytanie jak często odstawiane są rowery na tą samą stację i jak długo trwają przejazdy w zależności od typu użytkownika
with miary as
(select subscription_type, case when start_station_id=end_station_id then 'krążowniki' else 'sprinterzy' end as typ,
 count(t.id) as ilosc_wypo, avg(duration)/60 as sr_dl_przejazdu, sum(duration/60) as czas_total
from trip_sf t
group by subscription_type, typ)

select subscription_type, typ, ilosc_wypo, ilosc_wypo/sum(ilosc_wypo) over (partition by subscription_type)::numeric as proc_wypo, 
       sr_dl_przejazdu, czas_total, czas_total/sum(czas_total) over (partition by subscription_type)::numeric as proc_trwania
from miary

--WNIOSKI: 
-- - 13% osób wypożyczjących rowery okazjonalnie rozpoczynają i kończą podróż w tym samym miejscu (późniejsza analiza Hani pokazała, że nie jest to dworzec główny)
-- - osoby wypożyczajace rowery okazjonalnie zdecydowanie częściej oddają rowery na stacji wypożczenia niż abonamenci - robi to tylko 1% abonamentów


-- SLAJD TYPY UŻYTKOWNIKÓW - GODZINY PRZEJAZDÓW
-- odpowiada na pytanie czy godziny szczytu wypożyczeń różnią się w zależności od typu użytkownika - analiza średnio per dzień
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


-- SLAJD TYPY UŻYTKOWNIKÓW - ROZKŁAD WG DNI TYGODNIA
-- odpowiada na pytanie czy rozkład ilości wypożyczeń w ciagu tygodnia (ponidziałek-niedziela) różni się od typu użytkownika?
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


-- SLAJD TYPY UŻYTKOWNIKÓW - SEZONOWOŚĆ
-- za mało lat z pełnymi danymi, żeby wywnioskować o stałych charakterystykach sezonowych, do azalizy wzięłam rok z pełnymi danymi, czyi 2014
--Czy wsytępuje sezonowość w wypożyczeniach rowerów i czy jest zależność między sezonowością, a typem użytkownika? 
--Czy przejazdy abonamenckie charakteryzują się stałym rozkładem w ciągu roku? 
--Czy w SF występuje wzmożony sezon trusystyczny?

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

--WNIOSKI: 
-- - wahania sezonowe są większe dla okazjonalnych wypożyczeń niż dla abonamentów
-- - początek i koniec roku są zdecydowanie słabsze niż w okresie wiosny i lata (miesiące 5-8)


-- SLAJD TYPY UŻYTKOWNIKÓW - ROZKAD WG DŁUGOŚCI JAZDY
-- odpowiada na pytanie czy długość trwania wypożyczenia zależy od typ użytkownika
-- poniżej rozkład ilości wypożyczeń w zależnosci od czasu trawnia przejazdu w minutach, w przedziałach co 5 min do godziny
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
-- - rozkład długości trwania jazdy jest zupełnie inny dla abonamentów i okazjonanych użytkowników
-- - u użytkowników abonamentowych wypożyczenia poniżej 20 minut to 98% wypożyczeń, są to krótkie trasy do pracy
-- - dla użytkowników jednorazowych 20 minutowe przejazdy to tylko 26% wypożyczeń
-- - dłuższe wypożyczenia charkateryzują raczej aktywności w wolnym czasie
