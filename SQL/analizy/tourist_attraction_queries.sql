
--odleglosc od danego miejsca o danych wspolrzednych do atrakcji turystycznych w promieniu 1 mili

select *,
point(-122.394782, 37.776691) <@> point(long, lat)::point as distance
from tourist_attraction
where (point(-122.394782, 37.776691) <@> point(long, lat)) < 1
order by distance;

--wyznaczenie najblższej atrakcji turystycznej i odleglosci od danej stacji (np. Powell at Post (Union Square)) o danych wspolrzednych

select id, name, attraction_type,
point(-122.408499, 37.788446) <@> point(long, lat)::point as distance
from tourist_attraction
where (point(-122.408499, 37.788446) <@> point(long, lat)) = (select min(point(-122.408499, 37.788446) <@> point(long, lat)::point) from tourist_attraction);

--wyznaczenie najblższej atrakcji turystycznej i odleglosci od danej stacji (np. Powell at Post (Union Square)) wykorzystujac nazwe

select ta.id, ta.name, ta.attraction_type,
point(s.long, s.lat) <@> point(ta.long, ta.lat)::point as distance
from tourist_attraction ta, station s
where s.name ilike '%Powell at%' and (point(s.long, s.lat) <@> point(ta.long, ta.lat)) = (select min(point(s.long, s.lat) <@> point(ta.long, ta.lat)::point) from tourist_attraction ta);

--wyznaczenie atrakcji turystycznych i odleglosci od danej stacji (np. Powell at Post (Union Square)) wykorzystujac nazwe

select ta.id, ta.name, ta.attraction_type,
(
point(ta.long, ta.lat)<@>point(s.long, s.lat)) as distance
from tourist_attraction ta,
lateral (
select lat, long from station where name ilike '%Powell at%'
) as s 
order by distance;

--wyznaczenie atrakcji turystycznych i odleglosci od danej stacji (np. Powell at Post (Union Square)) wykorzystujac nazwe, w promieniu 1 mili

select ta.id, ta.name, ta.attraction_type,
point(s.long, s.lat) <@> point(ta.long, ta.lat)::point as distance
from tourist_attraction ta, station s
where s.name ilike '%Powell at%' and point(s.long, s.lat) <@> point(ta.long, ta.lat)::point < 1
order by distance asc;

--wyznaczenie najblższej stacji i odleglosci od danego miejsca na mapie o danych wspolrzednych

select id, name, dock_count,
point(-122.394782, 37.776691) <@> point(long, lat)::point as distance
from station
where (point(-122.394782, 37.776691) <@> point(long, lat)) = (select min(point(-122.394782, 37.776691) <@> point(long, lat)::point) from station) and city = 'San Francisco';

--wyznaczenie najblższej stacji i odleglosci od danej atrakcji turystycznej (np. union square) o danych wspolrzednych

select id, name, dock_count,
point(-122.407484, 37.788041) <@> point(long, lat)::point as distance
from station
where (point(-122.407484, 37.788041) <@> point(long, lat)) = (select min(point(-122.407484, 37.788041) <@> point(long, lat)::point) from station) and city = 'San Francisco';

--wyznaczenie najblższej stacji i odleglosci od danej atrakcji turystycznej (np. Golden Gate Bridge) wykorzysujac nazwe

select s.id, s.name,
point(s.long, s.lat) <@> point(ta.long, ta.lat)::point as distance
from tourist_attraction ta, station s
where ta.name ilike '%Bridge%' and s.city = 'San Francisco' and (point(s.long, s.lat) <@> point(ta.long, ta.lat)) = (select min(point(s.long, s.lat) <@> point(ta.long, ta.lat)::point) from station s);




