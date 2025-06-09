# README.md

# MoviWebApp

Eine einfache Flask-Webanwendung zum Verwalten von Users, Movies und Reviews mit SQLite und SQLAlchemy.

## Features

- **User Management**  
  - Benutzer anlegen und auflisten  
- **Movie Management**  
  - Filme für jeden User hinzufügen, anzeigen, bearbeiten und löschen  
- **Review System**  
  - Reviews zu Filmen erstellen und anzeigen  
- **REST-API** unter `/api/...` (JSON)

## Projektstruktur

MoviWebApp/
├── app.py # Haupt-Flask-App
├── datamanager/
│ ├── sqlite_data_manager.py # SQLAlchemy-Modelle & DataManager
│ ├── api.py # Blueprint für REST-API
│ └── data_manager_interface.py
├── templates/ # Jinja2-Templates
├── static/CSS/style.css # Stylesheet
├── moviwebapp.db # SQLite-Datenbank
├── requirements.txt
├── .gitignore
└── test_app.py # Pytest-Tests


## Installation & Setup

1. Repository klonen
   ```bash
   git clone git@github.com:DeinUser/MoviWebApp.git
   cd MoviWebApp
2. Virtuelle Umgebung erstellen & aktivieren 
   python3 -m venv .venv
   source .venv/bin/activate
3. Abhängigkeiten installieren
   pip install -r requirements.txt 

   Anwendung starten
   -Per Flask-CLI:
   flask run
   python app.py

Besuche dann im Browser http://127.0.0.1:5000/

REST-API

| Methode | Endpoint                         | Beschreibung              |
| ------- | -------------------------------- | ------------------------- |
| GET     | `/api/users`                     | Liste aller Users         |
| POST    | `/api/users`                     | Neuen User anlegen        |
| GET     | `/api/users/<user_id>/movies`    | Filme eines Users listen  |
| POST    | `/api/users/<user_id>/movies`    | Film zu User hinzufügen   |
| GET     | `/api/movies/<movie_id>/reviews` | Reviews eines Films holen |
| POST    | `/api/movies/<movie_id>/reviews` | Review hinzufügen         |

Testing:
1. In test_app.py den DataManager auf :memory: setzen und reset_database() aufrufen.

2. Tests ausführen:
   pytest

No Lizenz
