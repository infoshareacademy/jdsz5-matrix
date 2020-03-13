## Autorzy projektu:
+ Joanna Kwiatkowska,
+ Maciej Gadaj,
+ Hanna Obracht-Prondzyńska,
+ Wojciech Bonna.

## Źródło bazy danych:
[link do bazy danych](https://www.kaggle.com/benhamner/sf-bay-area-bike-share)

## Temat: 
Analiza aktywnej turystyki w San Francisco.\
Projekt obejmuje analizę bazy danych dotyczącej wypożyczalni rowerów w San Francisco, za pomocą języka zapytań SQL.

## Cel:
+ Główny: Mapa turystyki aktywnej San Francisco z propozycją tras dla turystów rowerowych.
+ Dodatkowy: Model analizy dla innych miast. 

## Interesariusze:
Zastosowanie modelu analitycznego znajduje zastosowanie wśród grup odbiorców:
+ turyści – gotowa propozycja aktywnego spędzenia czasu w San Francisco, z możliwością dalszego rozbudowania narzędzia,
+ władze miasta – gotowe rekomendacje dla rozwoju infrastruktury rowerowej oraz oferty usługowej w mieście ze wskazaniem lokalizacji, gdzie rzeczy te są niezbędne,
+ biznes z otoczenia turystyki – rekomendacje dla lokalizacji oferty skierowanej dla turystów, dostarczenie danych wejściowych dla dalszych analiz atrakcyjności lokalizacji oferty.

## Dodatkowe dane wejściowe wymagające pozyskania:
+ Atrakcje turystyczne – zabytki, restauracje, hotele, węzły komunikacji publicznej (punkty ze współrzędnymi).
+ Drogi oraz ścieżki rowerowe (linie).
+ Tereny zielone (poligony).
+ Granice miasta SanFrancisco.

## Źródło pozyskania danych:
OpenStreetMap oraz autorskie zestawienie w przygotowanej tabeli.

## Założenia:
+ Skupiamy się na zachowaniach turystów w mieście. Założeniem przyjętym jest więc, że osoba przebywająca w mieście tymczasowo, nie wykupuje abonamentu, a jedynie korzysta z opcji wykupu przejazdów jednorazowych. Nasza analiza więc skupia się jedynie na grupie użytkowników „customers", jednak w ramach weryfikacji zweryfikowaliśmy zachowania użytkowników abonamentów i użytkowników korzystających z systemu jednorazowo. 
+ Ze względu na różnorodność uwarunkowań miast – zlokalizowanych w nich atrakcji turystycznych, ograniczyliśmy nasze analizy do jednego miasta – San Francisco. 

## Harmonogram:
Zadania przygotowujące do analizy:
+ Ograniczenie bazy do samego San Francisco.
+ Stworzenie kluczy obcych.
+ Odrzucenie skrajnych przypadków.
+ Znalezienie atrakcji oraz zbudowanie tabeli zawierającej features: id, typ atrakcji, nazwa atrakcji, współrzędna x, współrzędna y.\
Deadline: 27.03.2020.

Zadania merytoryczne:
+ Zbadanie różnic w przemieszczeniach się po mieście przez użytkowników abonamentów oraz użytkowników korzystających z systemu jednorazowo. 
+ Ocena, które stacje są najpopularniejsze dla użytkowników korzystających z systemu jednorazowo. (Do oceny zbieżności lokalizacji stacji i atrakcji turystycznych).
+ Ocena intensywności wykorzystania stacji najpopularniejszych dla turystów – gdzie brakuje rowerów, gdzie zawsze są zajęte.
+ Ocena długości przejazdów najbardziej charakterystycznych dla krótkoterminowych użytkowników – wytyczna do zaprojektowania długości tras dla przyszłych użytkowników.
+ Zgrupowanie tras na te które mają te same punkty początkowe i punkty końcowe oraz zliczyć liczbę przejazdów na tych trasach.
+ Analiza sezonowości pod kątem: 
    + sezonów turystycznych w roku: czerwiec-wrzesień high season i reszta,
    + turystyka weekendowa a turystyka w tygodniu – różnice w zachowaniach,
    + temperatury - czy wpływa na intensywność ruchu turystycznego.
+ Ocena czy stacje w pobliżu atrakcji są intensywniej wykorzystywane.
+ Wizualizacja mapy tras i lokalizacji atrakcji.
+ Weryfikacja przerw w przejazdach oraz przygotowanie propozycji tras.\
Deadline: 28.02-8.03

Prezentacja wyników:
+ Prezentacja faktów – informacji, które dały wytyczne do sformułowania rekomendacji.
+ Wizualizacja wyników zapytań.
+ Wizualizacja rekomendacji dla odbiorców.
+ Spisanie rozbudowania funkcjonalności modelu analiz w przyszłości.
+ Przygotowanie prezentacji.\
Deadline: 9.03 - 15.03

## Dodatkowe informacje:

Propozycje rozbudowania funkcjonalności modelu analiz w przyszłości: 
+ Turysta wskazuje co chce zobaczyć – wyszukiwarka w odpowiedzi wskazuje mu optymalną trasę rowerową dla zwiedzenia tych punktów.
+ Może zawierać informacje praktyczne: uwaga, w punkcie, który wskazałeś często brakuje rowerów, albo nie ma wolnych docków.
+ Wskazuje propozycje co dodatkowo można zobaczyć: ofertę gastonomiczną, inne zabytki.

