# Dashboard Routing Fix

Questo branch (`fix-dashboard-routing`) contiene le correzioni per risolvere i problemi di accesso alla dashboard nel branch `dynamic-site-enhancement`.

## Problemi Risolti

### 1. Template Mancante
- ✅ Aggiunto il template mancante `templates/dashboard/users.html`
- Il template è ora completo con paginazione e gestione degli errori

### 2. Gestione Errori Migliorata
- ✅ Aggiunta gestione degli errori in tutte le route della dashboard
- ✅ Messaggi di errore più dettagliati per il debugging
- ✅ Fallback sicuri quando il database non è accessibile

### 3. Route di Debug
- ✅ Aggiunta route `/dashboard/debug/auth` per controllare lo stato di autenticazione
- ✅ Aggiunta route `/dashboard/debug/access` per testare l'accesso alla dashboard
- ✅ Informazioni dettagliate su sessioni e privilegi utente

### 4. Script di Utilità
- ✅ Creato script `utils/create_admin.py` per creare utenti amministratore
- ✅ Supporto per creare, listare e promuovere utenti

## Come Risolvere i Problemi di Accesso

### Passo 1: Verifica la Configurazione

Assicurati che il file `config.py` abbia la `SECRET_KEY` configurata:

```python
SECRET_KEY = 'your-secret-key-here'
```

### Passo 2: Inizializza il Database

Assicurati che il database sia inizializzato e accessibile:

```bash
# Con Docker Compose
docker-compose up -d db

# Controlla i log per errori
docker-compose logs app
```

### Passo 3: Crea un Utente Amministratore

Usa lo script di utilità per creare un utente admin:

```bash
# Crea utente admin predefinito
python utils/create_admin.py create

# Oppure promuovi un utente esistente
python utils/create_admin.py promote username

# Lista tutti gli utenti
python utils/create_admin.py list
```

### Passo 4: Testa l'Accesso

1. **Controlla lo stato di autenticazione:**
   ```
   GET /dashboard/debug/auth
   ```
   Questo ti dirà se sei loggato e hai i privilegi corretti.

2. **Testa l'accesso alla dashboard:**
   ```
   GET /dashboard/debug/access
   ```
   Questo ti dirà se puoi accedere alla dashboard e perché.

3. **Effettua il login:**
   - Vai a `/auth/login`
   - Usa le credenziali dell'utente admin
   - Dovresti essere reindirizzato automaticamente a `/dashboard/`

## Credenziali Admin Predefinite

Se usi lo script `create_admin.py create`, verranno create queste credenziali:

- **Username:** `admin`
- **Email:** `admin@hersel.it`
- **Password:** `admin123`

⚠️ **IMPORTANTE:** Cambia la password predefinita dopo il primo login!

## Troubleshooting

### Problema: "401 Login required"
**Soluzione:** Non sei loggato. Vai a `/auth/login` e effettua il login.

### Problema: "403 Admin access required"
**Soluzione:** Il tuo utente non ha privilegi di amministratore. Usa:
```bash
python utils/create_admin.py promote il_tuo_username
```

### Problema: "500 Internal Server Error"
**Possibili cause:**
1. Database non accessibile
2. Errore nei template
3. Configurazione mancante

**Debug:**
1. Controlla i log dell'applicazione
2. Usa le route di debug: `/dashboard/debug/auth` e `/dashboard/debug/access`
3. Verifica la configurazione del database

### Problema: Template non trovato
**Soluzione:** Assicurati che tutti i template esistano in `templates/dashboard/`:
- `index.html` ✅
- `projects.html` ✅
- `project_form.html` ✅
- `users.html` ✅ (aggiunto in questo fix)
- `base.html` ✅

## URL della Dashboard

Dopo aver risolto i problemi di autenticazione, puoi accedere a:

- **Dashboard principale:** `/dashboard/`
- **Gestione progetti:** `/dashboard/projects`
- **Nuovo progetto:** `/dashboard/projects/new`
- **Gestione utenti:** `/dashboard/users`
- **Debug autenticazione:** `/dashboard/debug/auth`
- **Test accesso:** `/dashboard/debug/access`

## Modifiche Apportate

1. **`templates/dashboard/users.html`** - Nuovo template per la gestione utenti
2. **`routes/dashboard.py`** - Migliorate gestione errori e aggiunte route di debug
3. **`utils/create_admin.py`** - Nuovo script per gestire utenti amministratore
4. **`DASHBOARD_FIX.md`** - Questa documentazione

## Come Applicare i Fix

1. **Merge di questo branch:**
   ```bash
   git checkout dynamic-site-enhancement
   git merge fix-dashboard-routing
   ```

2. **Oppure crea un PR:**
   - Crea una pull request da `fix-dashboard-routing` a `dynamic-site-enhancement`
   - Rivedi le modifiche e fai il merge

3. **Testa l'applicazione:**
   ```bash
   # Restart dell'applicazione
   docker-compose restart app
   
   # Crea utente admin
   docker-compose exec app python utils/create_admin.py create
   
   # Testa l'accesso
   curl http://localhost:5000/dashboard/debug/access
   ```

## Supporto

Se hai ancora problemi dopo aver applicato questi fix:

1. Controlla i log dell'applicazione
2. Usa le route di debug per diagnosticare il problema
3. Verifica che il database sia accessibile
4. Assicurati di avere un utente con privilegi di amministratore

Tutti i fix sono backward-compatible e non dovrebbero causare problemi al codice esistente.