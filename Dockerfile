# Usa un'immagine leggera di Python
FROM python:3.10-slim

# Imposta la working directory
WORKDIR /app

# Copia solo i file necessari per evitare di copiare file inutili
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto dell'applicazione
COPY . .

# Espone la porta usata da Hypercorn (default 5000)
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["hypercorn", "-c", "hypercorn_config.toml", "app:app"]
