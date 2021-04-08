# Galeria
Prosta Galeria z możliwością:
- logowania i rejestracji
- zarządzaniq profilem użytkownika
- dodawania zdjeć za pomocą plików oraz linków
- oceniania i komentowania
## Wymagania
- Python (3.8+)
- mysql (5.7+)
## Instalacja
Utwórz wirtualne środowisko i uruchom je (opcjonalne)
```bash
$ python -m venv env
$ env/Scripts/activate
```


1. Pobierz repozytorium i użyj menadżer pakietów [pip](https://pip.pypa.io/en/stable/) żeby zainstalować zależności z pliku requirements.txt
```bash
$ pip install -r requirements.txt
```
2. (Opcja 1) Przygotuj tabele 'galeria' w bazie danych `mysql`(port:3306) user: 'root' password: '' lub dostosuj ustawiena w pliku galeria/settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'galeria',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

2. (Opcja 2) Alternatywnie jesli nie chcesz konfigurować bazy `mysql` możesz użyć `sqlite` podmieniając powyższe pole w settings.py na:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
3. Wykonaj migracje
```bash
$ python manage.py migrate
```
## Uruchomienie
1. Przejdź do głównego katalogu projektu i wykonaj polecenie
```bash
$ python manage.py runserver
```
## Gotowe

Teraz wystarczy już tylko przejść do http://127.0.0.1:8000/ żeby zobaczyć rezultat