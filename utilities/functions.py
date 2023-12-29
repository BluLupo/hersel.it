import bcrypt

# Funzione per verificare la password durante il login
def check_password(user_input_password, hashed_password_from_database):
    print(user_input_password)
    print(hashed_password_from_database)
    # Converte la password inserita dall'utente in byte
    user_input_password_bytes = user_input_password.encode('utf-8')
    print(user_input_password_bytes)
    # Confronta l'hash della password inserita dall'utente con l'hash nel database
    return bcrypt.checkpw(user_input_password_bytes, hashed_password_from_database.encode('utf-8'))