Temat: Prognoza oceny jakości usług AirBnB

Zespół: Joanna Kwiatkowska, Hanna Obracht-Prondzyńska, Wojciech Bonna, Maciej Gadaj

Przyjęte założenia:
Chcemy dostarczyć właścicielom wynajmujących swoje mieszkania za pośrednictwem portalu AirBnB wskazówek, na co szczególnie powinni zwrócić uwagę, aby utrzymać lub poprawić oraz ocenę pobytu oraz zwiększyć zainteresowanie krótkim najmem korzystających z usług AirBnB. 
Dodatkowo, w wymiarze poznawczym, interesuje nas przewidywanie cen oraz rentowności z inwestowania w usługi krótkiego najmu. Np. jakiego typu mieszkania cieszą się największym zainteresowaniem.

Baza danych:
https://www.kaggle.com/airbnb/seattle?select=listings.csv

Cele analizy:
Prognozowanie popytu na mieszkania pod krótki najem w zależności od obecnych opinii użytkowników, typów mieszkań, ich lokalizacji itp. (cel główny - do prezentacji)
Prognozowanie cen wynajmu krótkiego w zależności od czynników, takich jak ocena użytkowników, warunki lokalowe, lokalizacja.
Określenie jakiego typu mieszkania cieszą się największą popularnością i przynoszą największy zysk.

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
Regresja liniowa, logistyczna i wielomianowa (Asia i in.)
Drzewa i lasy (Maciek)
Naive Bayes (Wojtek)
KNN i SVM (Hania)
Xgboost (Asia)
Określenie accuracy 

Porównanie modeli:
Zaprojektowanie systemu do optymalizacji hiper parametrów (zrobienie pipeline)
Wybór optymalnej liczby zmiennych dla regresji i innych modeli ….
Dopracowanie najlepszych dwóch modeli

Prezentacja wyników:
Przedstawienie, który z modeli jest najdokładniejszy
Stworzenie widgecików pozwalających na wybór uwarunkowań, dla których wyświetlą się nasze prognozowane wartości.
Zarządzanie i uporządkowanie plików na gicie
Uporządkowanie prezentacji w jupyterze
