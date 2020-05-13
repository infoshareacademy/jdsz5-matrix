Temat: Kolizje w Seattle

Autorzy:
  Joanna Kwiatkowska
  Hanna Obracht-Prondzynska
  Maciej Gadaj
  Wojciech Bonna

Baza danych:
  https://www.kaggle.com/jonleon/seattle-sdot-collisions-data

Objaśnienia bazy:
  https://www.seattle.gov/Documents/Departments/SDOT/GIS/Collisions_OD.pdf

Cleaning: 
  Wyrzucenie kolumn z brakiem danych
  Ujednolicenie formatu dat
  Wyrzucenie miejsc gdzie nie znamy uwarunkowań 
  Ujednolicić nazwy w kategoriach
  Podzielić kolumnę z typem wypadku na dwie - typ kolizji do osobnej kolumny (samochód-samochód, samochód-pieszy, rowerzysta-słup itd), i rodzaj zderzenia (przód, tył, bok itd).
  Ujednolicenie typów wypadków
  Dodanie kolumny z dzielnicą

Wykresy do zrobienia:
  Podział na liczbę wypadków w zależności od typu środka transportu
  Liczba wypadków w zależności od pory dnia
  Liczba wypadków w zależności od pory roku
  Liczba poszkodowanych w zależności od typu środka transportu
  Liczba wypadków w zależności od typu (śmiertelny, poważny, etc.)
  Liczba wypadków w zależności od warunków pogodowych
  Determinanty wypadków (uwarunkowania infrastrukturalne, pogodowe etc)
  Warunki pogodowe w zależności od pory roku
  Statystyki według pod wpływem, nieuwaga, warunki pogodowe

Testy do przeprowadzenia:
(wtedy trzeba zaproponować typy testów do przeprowadzenia)
Założenia, które można przyjąć:

Klimatyczne:
  Test istotności dla różnych warunków pogodowych
    Pogoda się poprawia i jest więcej dni słonecznych (chociaż nie wiem czy w Seattle to możliwe) - zmienia się warunek         dotyczący mokrej nawierzchni i warunków pogodowych,
    Poprawia się jakość powietrza, czyli mamy mniej dni z mgłą - zmienia się warunek z warunkami pogodowymi

Infrastrukturalne:
  Test istotności dla uwarunkowań infrastrukturalnych
    Wprowadzamy więcej oświetlenia w mieście i nie ma miejsc nieoświetlonych

Zachowania ludzi:
  Szacowana wypadkowość przy zmianie proporcji różnych typów środków transportu
    Więcej osób przesiada się na transport publiczny więc zmniejsza się ruch w godzinach szczytu,
    Więcej osób korzysta z rowerów, co oznacza, że mamy więcej wypadków z udziałem rowerów, ale jak będzie wyglądała kwestia    szkód, liczby rannych i powagi sytuacji.

Prognozowanie:
  Szacowana wypadkowość na kolejny rok

Scenariusze:
  Ocieplenie klimatu :D - lepsze warunki na drodze
  Zmiana mody na środek transportu - zmiana proporcja uczestników w wypadkach
  Rośnie liczba samochodów na drogach nie poprawiają się warunki - rośnie liczba kolizji 

Interakcja z użytkownikiem:
  Wybór statystyk wg pory dnia, roku
  Wybór statystyk wg uwarunkowań
  Wybór statystyk wg miejsca
  Wybór statystyk wg środka transportu
  Użytkownik wybiera najpierw środek transportu, a potem zmienne do analizy (pogoda, miejsca, pora dnia)
  Stworzenie możliwości wyboru analizowania z wszystkimi przypadkami lub odrzuceniem ekstremalnych przypadków

Przygotowanie widgetów
  Suwaczki: statystyki po miesiącach

Mapy:
  Statystyki dla dzielnic
  Wybór statystyk dla punktu 
  Suwaczki dla kolejnych miesięcy
  Do wyboru mapa wypadków różnych środków transportu
