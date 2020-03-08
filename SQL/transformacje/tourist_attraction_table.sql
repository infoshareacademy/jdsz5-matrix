create table tourist_attraction (
	id integer primary key,
	name varchar(200) not null,
	attraction_type varchar(200) null,
	lat numeric null,
	long numeric null
);

insert into tourist_attraction
	(id, name, attraction_type, lat, long)
	values
	(1, 'Golden Gate Bridge', 'architecture', 37.808844, -122.474996),
	(2, 'Golden Gate Park', 'nature', 37.769530, -122.486107),
	(3, 'Twin Peaks', 'viewpoint', 37.754240, -122.447118),
	(4, 'Glen Canyon Park', 'nature', 37.741484, -122.443195),
	(5, 'The Palace of Fine Arts', 'art and culture', 37.802079, -122.448339),
	(6, 'Union Square', 'shopping district', 37.788041, -122.407484),
	(7, 'Dragon Gate - Chinatown', 'art and culture', 37.790776, -122.405622),
	(8, 'Coit Tower', 'architecture', 37.802458, -122.405828),
	(9, 'Lombard Street', 'architecture', 37.802170, -122.418695),
	(10, 'Fishermans Wharf', 'shopping district', 37.808365, -122.415750),
	(11, 'Civic Center Plaza', 'architecture', 37.779789, -122.417527),
	(12, 'Asian Art Museum', 'art and culture', 37.780116, -122.416280),
	(13, 'Cable Car Museum', 'art and culture', 37.794668, -122.411486),
	(14, 'Exploratium', 'art and culture', 37.801368, -122.398164),
	(15, 'Pier 24 Photography', 'art and culture', 37.789311, -122.387730),
	(16, 'Pier 14', 'viewpoint', 37.794654, -122.389750),
	(17, 'SF Museum of Modern Art', 'art and culture', 37.785749, -122.401042),
	(18, 'Transamerica Pyramid', 'architecture', 37.795210, -122.402785);

	
	