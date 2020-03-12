# **INSTRUKCJA**

## **Zakres**

Dokumentacja projektu znajduje się w pliku README i 3 folderach (transformacje, analizy, output).

Plik README zawiera:
+ temat projektu,
+ cel,
+ założenia,
+ zakres,
+ źródło bazy danych.

Folder "transformacje" zawiera:
+ instrukcję instalacji i przygotowania bazy danych oraz zakres dokumentacji projektowej,
+ polecenia CREATE TABLE oraz INSERT INTO do tworzenia tabel z danymi,
+ polecenia mające na celu uporządkowanie bazy danych, ograniczenie danych do ustalonego zakresu, usunięcie danych odbiegających znacznie od pozostałych, które mogą zafałszować wyniki analizy.

Folder "analizy" zawiera:
+ zapytania SQL do bazy danych wykorzystane w projekcie w celu analizy: tras między stacjami rowerowymi, czasów przejazdów użytkowników, zachowania użytkowników, lokalizacji i odległości stacji od atrakcji.

Folder "output" zawiera:
+ wszystkie zapytania SQL wraz z opisem, wyznaczające wyniki analizy bazy danych przedstawione w prezentacji projektu.

## **Instrukcja instalacji i przygotowania bazy danych**

1. Pobrać bazę danych z [link do bazy danych](https://www.kaggle.com/benhamner/sf-bay-area-bike-share).
2. Stworzyć tabele zgodnie z poleceniami SQL z pliku create_table.sql (folder "transformacje").
3. Zaimportować elementy bazy danych (station, status, trip, weather) do poszczególnych tabel (stworzonych w punkcie 2).
4. Stworzyć tabelę i wprowadzić dane zgodnie z poleceniami z pliku tourist_attraction_table.sql (folder "transformacje")
5. Przygotować i uporządkować bazę danych za pomocą poleceń znajdujących się w pliku tab_SanFrancisco.sql (folder transformacje).

## **Wyniki analizy bazy danych**

Wyniki analizy bazy danych wyznaczyć za pomocą poleceń SQL znajdujących się w pliku output w folderze "output".