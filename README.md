# Sette opp prosjektet
1. Navigér til den mappen du vil klone repositorien i
2. Skriv `git clone url`
3. navigér inn i den mappen med `cd` og inn i ShareBNB med cd `cd ShareBNB`
4. Åpne denne mappen i PyCharm og sette opp et virtualenv der. Settings -> Project interpreter -> add... -> velg python3
5. Skriv `pip install -r requirements.txt` i PyCharm-terminalen
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8. `python manage.py createsuperuser`
9. `python manage.py runserver`


# Hvordan branche
`git checkout -b "Branch-navn"`