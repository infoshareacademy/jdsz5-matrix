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
