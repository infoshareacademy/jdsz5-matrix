Temat: Prognoza ceny usług AirBnB

Zespół: Joanna Kwiatkowska, Hanna Obracht-Prondzyńska, Wojciech Bonna, Maciej Gadaj

Przyjęte założenia:
Chcemy dostarczyć właścicielom informacje jakie są prognozowane ceny ich lokali, zatem ile będą w stanie na nich zarobić. Z drugiej zaś strony chcemy pokazać użytkownikom ofert AirBnB, czy nie przepłacają za usługę, którą wybrali.

Baza danych:
https://www.kaggle.com/airbnb/seattle?select=listings.csv

Cele analizy:
Prognozowanie ceny na mieszkania pod krótki najem w zależności od obecnych opinii użytkowników, typów mieszkań, warunków lokalowych i ich lokalizacji itp. 
Określenie jakiego typu mieszkania i w jakiej lokalizacji cieszą się największą popularnością i przynoszą największy zysk.

Zadania do wykonania:
(lista może ulec zmianie w zależności od odkrytych informacji w trakcie eksploracji danych)

Nabieranie intuicji w danych (przygotowanie podstawowych wykresów):
Wartości odstające.
Autokorelacja featerów.
Istotność featurów.
Średnia cena w zależności od lokalizacji i sezonu
Mapa lokalizacji mieszkań krótkiego najmu w zależności od ich typu.
Mapa sąsiedztwa według zainteresowania najmem.
Obłożenie w zależności od dnia, miesiąca, sezonu
Zwykły wykres - zliczenie dni i miesięcy pod kątem nowych kolumn (cztery sezony, dni powszednie, dni weekendowe - 6 kolumn)

Data cleaning & feature engineering:
Usunięcie rekordów z brakującymi danymi o cenie. 
Redukcja zmiennych
Zmiana typu danych: 
Uporządkowanie  atrybutów dat
Wyliczenie % obłożenia 
Zmiana wartości danych: sąsiedztwo, typ mieszkania etc.
usunięcie outlierów (czym są?)

Model (podstawowe zadania i założenia):
Testowanie modeli, w tym:
Regresja liniowa, logistyczna i wielomianowa
Drzewa i lasy
Naive Bayes
KNN i SVM
Xgboost

Porównanie modeli:
Zaprojektowanie systemu do optymalizacji hiper parametrów (zrobienie pipeline)
Wybór optymalnej liczby zmiennych dla regresji i innych modeli ….
Dopracowanie najlepszych dwóch modeli

Prezentacja wyników:
Przedstawienie, który z modeli jest najdokładniejszy
Stworzenie widgecików pozwalających na wybór uwarunkowań, dla których wyświetlą się nasze prognozowane wartości.
