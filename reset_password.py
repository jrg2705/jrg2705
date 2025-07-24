# reset_password.py

from app import app, db, User  # Carga la app y los objetos desde app.py
from werkzeug.security import generate_password_hash
import sys

def reset_password(username, new_password):
    with app.app_context():  # Requerido para poder usar db en script externo
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ Usuario '{username}' no encontrado.")
            return
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"✅ Contraseña de '{username}' actualizada correctamente.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python reset_password.py <username> <nueva_contraseña>")
    else:
        reset_password(sys.argv[1], sys.argv[2])
