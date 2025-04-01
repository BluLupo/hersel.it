# Python Server - Hersel.it

Questo progetto è un'applicazione web sviluppata con **Quart** e configurata per essere eseguita tramite **Hypercorn**

## Requisiti

- Python 3.10 o superiore
- Pip (gestore dei pacchetti Python)

# Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/BluLupo/hersel.it.git
   cd hersel.it
   ```

2. Crea Ambiente Virtuale
   ```bash
    python3 -m venv env
   ```

3. Attiva Ambiente Virtuale
    ```bash
    source env/bin/activate
   ```

4. Installa Le Dipendenze
     ```bash
    pip install -r requirements.txt
   ```
   
# Configurazione
Modifica il file <b>hypercorn_config.toml</b> se necessario per adattarlo al tuo ambiente
Esempio di configurazione predefinita (hypercorn_config.toml):

```toml
    bind = "0.0.0.0:5000"
    workers = 1
    reload = true
   ```
# Avvio Applicazione
  ```bash
    hypercorn -c hypercorn_config.toml app:app
   ```


# 🚀 Avvio dell'applicazione con Docker
Questa applicazione utilizza Quart come web framework asincrono e Hypercorn come ASGI server

⚙️ Requisiti
- Docker
- Docker Compose

# 📄 Come avviare l'applicazione
1 - Crea un nuovo file docker-compose.yml nella tua macchina, con il seguente contenuto (oppure copialo direttamente da <a href="https://github.com/BluLupo/hersel.it/blob/master/docker-compose.yml">Qui</a> ):

```yml
    version: "3.9"

   services:
     quartapp:
       image: python:3.10-slim
       container_name: herselquart
       working_dir: /app
       ports:
         - "127.0.0.1:5000:5000"
       command: >
         sh -c "
           apt-get update &&
           apt-get install -y git &&
           git clone https://github.com/BluLupo/hersel.it.git /app &&
           pip install --no-cache-dir -r requirements.txt &&
           hypercorn -c hypercorn_config.toml app:app
         "
       environment:
         - PYTHONUNBUFFERED=1
   ```

2 - Esegui il servizio con Docker Compose:
```bash
    docker-compose up
   ```

# 🔗 Accesso all'applicazione
Una volta avviata, l'applicazione sarà accessibile da:
```bash
    http://127.0.0.1:5000
   ```






