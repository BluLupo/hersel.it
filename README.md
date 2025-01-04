# Python Server - Hersel.it

Questo progetto è un'applicazione web sviluppata con **Quart** e configurata per essere eseguita tramite **Hypercorn**.

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
Modifica il file <b>hypercorn_config.toml</b> se necessario per adattarlo al tuo ambiente.
Esempio di configurazione predefinita (hypercorn_config.toml):

```toml
    bind = "127.0.0.1:5000"
    workers = 1
    reload = true
   ```
# Avvio Applicazione
  ```bash
    hypercorn -c hypercorn_config.toml app:app
   ```


