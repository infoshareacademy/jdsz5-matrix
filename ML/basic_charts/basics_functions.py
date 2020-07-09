#### Podstawowa wiedza o zbiorze danych


def cena_dzielnica (df_b):
    #get list of neighbourhoods
    neighbourhoods = df_b['neighbourhoodgroupcleansed'].unique()

    #get prices by month and neighbourhood
    price_by_month_neighbourhood = df_b.groupby(['monthno','neighbourhoodgroupcleansed']).mean().reset_index()

    #plot prices for each neighbourhood
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)

    for neighbourhood in neighbourhoods:
        ax.plot(price_by_month_neighbourhood[price_by_month_neighbourhood['neighbourhoodgroupcleansed'] == neighbourhood]['monthno'],
                 price_by_month_neighbourhood[price_by_month_neighbourhood['neighbourhoodgroupcleansed'] == neighbourhood]['Price'],
                 label = neighbourhood)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.ylabel('Średnia cena, $')
    plt.xlabel('Miesiąc')
    plt.title('Średnia cena w dzielnicy, $')

    plt.savefig('average_price_for_neighbourhood')

    plt.show()


def cena_oferta (df_b):
    #get list of neighbourhoods
    properties = df_b['propertytype'].unique()

    #get prices by month and neighbourhood
    price_by_month_property = df_b.groupby(['monthno','propertytype']).mean().reset_index()

    #plot prices for each neighbourhood
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(111)

    for property in properties:
        ax.plot(price_by_month_property[price_by_month_property['propertytype'] == property]['monthno'],
                 price_by_month_property[price_by_month_property['propertytype'] == property]['Price'],
                 label = property)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.ylabel('Średnia cena, $')
    plt.xlabel('Miesiąc')
    plt.title('Średnia cena typu oferty, $')

    plt.savefig('average_price_for_propertytype')

    plt.show()

##### Rozklad przestrzenny ofert AirbnB

def gdzie_najdrozej (df_b):
    
    mapa = folium.Map(location=[47.607612, -122.333515], zoom_start=12)

    #px.set_mapbox_access_token(open(".mapbox_token").read())
    col = df_b.sample(1000)
    fig = px.scatter_mapbox(col, lat="latitude", lon="longitude",     color="Price", size="Price",
                      color_continuous_scale=px.colors.sequential.RdBu, size_max=50, zoom=12)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    print('Mapa przedstawia lokalizację lokali AirBnB, wielkość koła zależna jest od ceny')
    fig.show()

def rozklad_ofert (df_b): #(heatmapa)
    from folium import plugins
    #mapa podstawowa
    m = folium.Map([47.607612, -122.333515], zoom_start=10)
    # punkty na mapie
    for index, row in df_b.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=2,
                            popup=row['propertytype'],
                            fill_color="#ff4650",
                            opacity= 0,
                           ).add_to(m)
    # convert to (n, 2) nd-array format for heatmap
    dfArr = df_b[['latitude', 'longitude']] #.as_matrix()
    # plot heatmap
    m.add_children(plugins.HeatMap(dfArr, radius=12))

    return m

##### podzial zmiennych

varis_gen = ['hostresponserate',
             'hostacceptancerate',
             'hostissuperhost',
             'hostlistingscount',
             'hosttotallistingscount',
             'hosthasprofilepic',
             'hostidentityverified',
             'latitude',
             'longitude',
             'accommodates',
             'bathrooms',
             'bedrooms',
             'beds',
             'Price',
             'weeklyprice',
             'monthlyprice',
             'securitydeposit',
             'cleaningfee',
             'guestsincluded',
             'extrapeople',
             'minimumnights',
             'maximumnights',
             'numberofreviews',
             'reviewscoresrating',
             'reviewscoresaccuracy',
             'reviewscorescleanliness',
             'reviewscorescheckin',
             'reviewscorescommunication',
             'reviewscoreslocation',
             'reviewscoresvalue',
             'instantbookable',
             'requireguestprofilepicture',
             'requireguestphoneverification',
             'calculatedhostlistingscount',
             'hostexperience',
             'demand',
             'hostresponsetimeafewdaysormore',
             'hostresponsetimewithinaday',
             'hostresponsetimewithinafewhours',
             'hostresponsetimewithinanhour',
             'propertytypeApartment',
             'propertytypeBedBreakfast',
             'propertytypeBoat',
             'propertytypeBungalow',
             'propertytypeCabin',
             'propertytypeCamperRV',
             'propertytypeChalet',
             'propertytypeCondominium',
             'propertytypeDorm',
             'propertytypeHouse',
             'propertytypeLoft',
             'propertytypeOther',
             'propertytypeTent',
             'propertytypeTownhouse',
             'propertytypeTreehouse',
             'propertytypeYurt',
             'neighbourhoodgroupcleansedBallard',
             'neighbourhoodgroupcleansedBeaconHill',
             'neighbourhoodgroupcleansedCapitolHill',
             'neighbourhoodgroupcleansedCascade',
             'neighbourhoodgroupcleansedCentralArea',
             'neighbourhoodgroupcleansedDelridge',
             'neighbourhoodgroupcleansedDowntown',
             'neighbourhoodgroupcleansedInterbay',
             'neighbourhoodgroupcleansedLakeCity',
             'neighbourhoodgroupcleansedMagnolia',
             'neighbourhoodgroupcleansedNorthgate',
             'neighbourhoodgroupcleansedOtherneighborhoods',
             'neighbourhoodgroupcleansedQueenAnne',
             'neighbourhoodgroupcleansedRainierValley',
             'neighbourhoodgroupcleansedSewardPark',
             'neighbourhoodgroupcleansedUniversityDistrict',
             'neighbourhoodgroupcleansedWestSeattle',
             'roomtypeEntirehomeapt',
             'roomtypePrivateroom',
             'roomtypeSharedroom',
             'bedtypeAirbed',
             'bedtypeCouch',
             'bedtypeFuton',
             'bedtypePulloutSofa',
             'bedtypeRealBed',
             'cancellationpolicyflexible',
             'cancellationpolicymoderate',
             'cancellationpolicystrict']

varis_type = ['hostresponserate',
             'hostacceptancerate',
             'hostissuperhost',
             'hostlistingscount',
             'hosttotallistingscount',
             'hosthasprofilepic',
             'hostidentityverified',
             'latitude',
             'longitude',
             'accommodates',
             'bathrooms',
             'bedrooms',
             'beds',
             'guestsincluded',
             'extrapeople',
             'minimumnights',
             'maximumnights',
             'instantbookable',
             'requireguestprofilepicture',
             'requireguestphoneverification',
             'calculatedhostlistingscount',
             'hostexperience',
             'hostresponsetimeafewdaysormore',
             'hostresponsetimewithinaday',
             'hostresponsetimewithinafewhours',
             'hostresponsetimewithinanhour',
             'propertytypeApartment',
             'propertytypeBedBreakfast',
             'propertytypeBoat',
             'propertytypeBungalow',
             'propertytypeCabin',
             'propertytypeCamperRV',
             'propertytypeChalet',
             'propertytypeCondominium',
             'propertytypeDorm',
             'propertytypeHouse',
             'propertytypeLoft',
             'propertytypeOther',
             'propertytypeTent',
             'propertytypeTownhouse',
             'propertytypeTreehouse',
             'propertytypeYurt',
             'neighbourhoodgroupcleansedBallard',
             'neighbourhoodgroupcleansedBeaconHill',
             'neighbourhoodgroupcleansedCapitolHill',
             'neighbourhoodgroupcleansedCascade',
             'neighbourhoodgroupcleansedCentralArea',
             'neighbourhoodgroupcleansedDelridge',
             'neighbourhoodgroupcleansedDowntown',
             'neighbourhoodgroupcleansedInterbay',
             'neighbourhoodgroupcleansedLakeCity',
             'neighbourhoodgroupcleansedMagnolia',
             'neighbourhoodgroupcleansedNorthgate',
             'neighbourhoodgroupcleansedOtherneighborhoods',
             'neighbourhoodgroupcleansedQueenAnne',
             'neighbourhoodgroupcleansedRainierValley',
             'neighbourhoodgroupcleansedSewardPark',
             'neighbourhoodgroupcleansedUniversityDistrict',
             'neighbourhoodgroupcleansedWestSeattle',
             'roomtypeEntirehomeapt',
             'roomtypePrivateroom',
             'roomtypeSharedroom',
             'bedtypeAirbed',
             'bedtypeCouch',
             'bedtypeFuton',
             'bedtypePulloutSofa',
             'bedtypeRealBed',
             'cancellationpolicyflexible',
             'cancellationpolicymoderate',
             'cancellationpolicystrict']


varis_demand = ['Price',
             'weeklyprice',
             'monthlyprice',
             'securitydeposit',
             'cleaningfee',
             'numberofreviews',
             'reviewscoresrating',
             'reviewscoresaccuracy',
             'reviewscorescleanliness',
             'reviewscorescheckin',
             'reviewscorescommunication',
             'reviewscoreslocation',
             'reviewscoresvalue',
             'demand']

def klastry_dzielnice (df_b):
    
    import geopandas as gpd
    from sklearn import cluster
    from sklearn.preprocessing import scale
    from sklearn.cluster import KMeans

    abb = gpd.read_file('districts.geojson') 
    aves = df_b.groupby('neighbourhoodcleansed')[varis_gen].mean()
    zdb = abb[['geometry', 'neighbourhoodcleansed']].join(aves, on='neighbourhoodcleansed')\
                                             .dropna()

    print('Optymalna liczba klastrów')

    k_vec = []
    int_vec = []

    for k in range(2,15):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(zdb[varis_type])
        interia = kmeans.inertia_
        k_vec.append(k)
        int_vec.append(interia)

    plt.figure(figsize=(7,5))
    plt.title('Wykres sum wariancji klastów dla typ&cena')
    plt.plot(k_vec,int_vec,'bo-')
    plt.xlabel('liczba klastrów')
    plt.ylabel('Suma wariancji klastrów')
    plt.show()

    #Klastry dzielnic
    print('Klastry dzielnic według typu oferty')

    kmeans5a = cluster.KMeans(n_clusters=5)
    k5acls = kmeans5a.fit(zdb[varis_type])
    zdb['k5acls'] = k5acls.labels_
    f, ax = plt.subplots(1, figsize=(9, 9))
    zdb.plot(column='k5acls', categorical=True, legend=True, linewidth=0, axes=ax)
    ax.set_axis_off()
    plt.axis('equal')
    plt.title('Charakterystyka dzielnic wg typu oferty AirBnb')
    plt.show()
    plt.savefig('map_c1.jpg')

    print('Klastry dzielnic według popytu i ceny')

    kmeans5b = cluster.KMeans(n_clusters=5)
    k5bcls = kmeans5b.fit(zdb[varis_demand])
    zdb['k5bcls'] = k5bcls.labels_
    f, ax = plt.subplots(1, figsize=(9, 9))
    zdb.plot(column='k5bcls', categorical=True, legend=True, linewidth=0, axes=ax)
    ax.set_axis_off()
    plt.axis('equal')
    plt.title('Charakterystyka dzielnic wg popytu & ocen')
    plt.show()
    plt.savefig('map_c2.jpg')

    print('Liczba dzielnic w klasach')

    k5sizes = zdb.groupby('k5acls').size()
    _ = k5sizes.plot(kind='bar')

    
