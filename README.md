# Task-manager
Backend for the basic CRUD app using Django Rest with PostgreSQL.

# Most important for now
- Przedstawienie filtrowanej listy zadań - opcja pozwalająca wyświetlić wszystkie zadania w systemie, z możliwością filtracji po każdym polu (tj. id, nazwie, opisie, statusie i użytkowniku). Przykładowo, powinna być możliwość wyświetlenia listy:
   * zadań zawierających w opisie lub nazwie dowolne słowo np. 'gotowanie', bez względu na wielkość liter.
- Przedstawienie historii zmian zadań - opcja pozwala wyświetlić historię wszystkich dokonanych zmian dla zadań. Należy zapewnić odpowiednią filtrację pozwalającą wyświetlić np. tylko historię zmian dla danego zadania. Z końcówki powinna być możliwość otrzymania informacji, jakie dane zawierało zadanie w konkretnym czasie (np. jaki status miało dane zadanie kilka dni temu i do kogo było przypisane).
- plik README.md, który będzie zawierać szczegółową instrukcję uruchomienia aplikacji. Powinna zawierać minimum informacje potrzebne do uruchomienia bazy danych i serwera aplikacji.

# Działanie
- zwykły user ma dostęp tylko do swoich przypisanych zadań i tylko on je moze moze usuwac i modfyfikowac
- wyswietlac zwykly user moze wszystkie
- chociaz ja mam superusera to wszystko powinnam moc

# Dodatkowym atutem będzie jeśli:
* Zostanie zaimplementowane logowanie użytkowników i rejestracja użytkowników,
* Aplikacja będzie posiadać system uprawnień,
* Aplikacja będzie posiadać testy z użyciem pytest,
* W pliku README.md zawarta będzie dokumentacja przedstawiająca w jaki sposób można korzystać z API oraz przykładowe odpytania końcówek np. przy użyciu komendy curl.
-> link do curla https://stackabuse.com/creating-a-rest-api-with-django-rest-framework/

## Requirements 
-Python ...
## Installation
1) Clone the repository

## Use
