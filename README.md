# Portfolio Dinamico - Hersel.it

Portfolio personale sviluppato con **Flask** e **MariaDB**, con gestione dinamica dei contenuti tramite API REST.

## 🚀 Caratteristiche

- **Framework**: Flask (migrato da Quart per semplificare l'architettura)
- **Database**: MariaDB per la gestione dinamica dei contenuti
- **ORM**: SQLAlchemy con Flask-SQLAlchemy
- **API REST**: Endpoint per gestire progetti, competenze, profilo e social links
- **Docker**: Configurazione completa con Docker Compose
- **Responsive**: Design responsive con Bootstrap 5

## 📋 Requisiti

- Python 3.10 o superiore
- MariaDB/MySQL 11.2 o superiore (o usa Docker Compose)
- Pip (gestore dei pacchetti Python)

## 🔧 Installazione Locale

### 1. Clona il repository
```bash
git clone https://github.com/BluLupo/hersel.it.git
cd hersel.it
```

### 2. Crea e attiva ambiente virtuale
```bash
python3 -m venv env
source env/bin/activate  # Linux/Mac
# oppure
env\Scripts\activate  # Windows
```

### 3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configura le variabili d'ambiente
```bash
cp .env.example .env
# Modifica .env con le tue credenziali del database
```

### 5. Configura MariaDB
Crea il database e l'utente:
```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portfolio_user'@'localhost' IDENTIFIED BY 'portfolio_password';
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. Inizializza il database
```bash
python init_db.py
```

### 7. Avvia l'applicazione
```bash
# Modalità sviluppo
python app.py

# Modalità produzione con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐳 Installazione con Docker

### Requisiti
- Docker
- Docker Compose

### Avvio rapido
```bash
docker-compose up -d
```

L'applicazione sarà disponibile su `http://localhost:5000`

Docker Compose avvierà automaticamente:
- Container MariaDB sulla porta 3306
- Container Flask sulla porta 5000
- Inizializzazione automatica del database

## 📁 Struttura del Progetto

```
hersel.it/
├── app.py                      # Applicazione Flask principale
├── config.py                   # Configurazione
├── models.py                   # Modelli SQLAlchemy
├── init_db.py                  # Script inizializzazione database
├── requirements.txt            # Dipendenze Python
├── docker-compose.yml          # Configurazione Docker
├── .env.example               # Esempio variabili d'ambiente
├── routes/
│   ├── home.py                # Route homepage
│   └── api.py                 # API REST endpoints
├── templates/                 # Template Jinja2
│   ├── index.html
│   ├── head.html
│   ├── navbar.html
│   └── content/
│       ├── about.html
│       ├── project.html
│       └── links.html
└── static/                    # File statici (CSS, JS, immagini)
```

## 🔌 API REST Endpoints

### Profile
- `GET /api/profile` - Ottieni informazioni profilo
- `PUT /api/profile` - Aggiorna profilo

### Skills
- `GET /api/skills` - Lista competenze
- `POST /api/skills` - Crea competenza
- `PUT /api/skills/<id>` - Aggiorna competenza
- `DELETE /api/skills/<id>` - Elimina competenza

### Projects
- `GET /api/projects` - Lista progetti
- `POST /api/projects` - Crea progetto
- `PUT /api/projects/<id>` - Aggiorna progetto
- `DELETE /api/projects/<id>` - Elimina progetto

### Social Links
- `GET /api/social-links` - Lista link social
- `POST /api/social-links` - Crea link social
- `PUT /api/social-links/<id>` - Aggiorna link social
- `DELETE /api/social-links/<id>` - Elimina link social

## 📊 Schema Database

### Tabelle
- `profile` - Informazioni personali
- `skills` - Competenze tecnologiche
- `projects` - Portfolio progetti
- `project_tags` - Tag/badge progetti
- `social_links` - Link profili social

## 🔄 Migrazione da Quart a Flask

Questo progetto è stato migrato da Quart (framework asincrono) a Flask (framework sincrono) per:
- Semplificare l'architettura
- Migliorare la compatibilità con librerie esistenti
- Facilitare il deployment con server WSGI standard (Gunicorn)
- Ridurre la complessità per un portfolio che non richiede operazioni async intensive

## 🛠️ Sviluppo

### Aggiungere un nuovo progetto via API
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nuovo Progetto",
    "description": "Descrizione del progetto",
    "image_url": "img/project.webp",
    "github_url": "https://github.com/username/repo",
    "tags": [
      {"name": "Python", "color_class": "bg-primary"},
      {"name": "Flask", "color_class": "bg-info"}
    ]
  }'
```

## 📝 Licenza

Copyright Hersel Giannella

## 🔗 Link Utili

- Portfolio Live: [https://hersel.it](https://hersel.it)
- GitHub: [https://github.com/BluLupo](https://github.com/BluLupo)
- LinkedIn: [https://linkedin.com/in/hersel](https://linkedin.com/in/hersel)






