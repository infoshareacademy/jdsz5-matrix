-- Średnie czasy przejazdów pomiędzy różnymi stacjami z odrzuceniem 5% najkrótszych i najdłuższych przejazdów 
-- z pominięciem tras ropoczynających się i konczących w tym samym punkcie

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
where duration/60 between poniżej_5_proc and powyzej_95_proc
group by ts.start_station_id, ts.end_station_id)

select start_station_id, s.name as start_station_name, end_station_id, e.name as end_station_name, avg_duration
from srednie_czasy as ac 
     inner join station_sf as s on ac.start_station_id = s.id 
     inner join station_sf as e on ac.end_station_id = e.id 

