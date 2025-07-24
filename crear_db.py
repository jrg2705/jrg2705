# crear_db.py (Versión Mejorada)
from app import app, db, User, Rol

print("Iniciando la creación/verificación de la base de datos...")

with app.app_context():
    print("Creando todas las tablas si no existen...")
    db.create_all()

    # --- Asegurar que el rol 'admin' exista ---
    admin_rol = Rol.query.filter_by(nombre='admin').first()
    if not admin_rol:
        print("Rol 'admin' no encontrado, creándolo...")
        admin_rol = Rol(nombre='admin')
        db.session.add(admin_rol)
        db.session.commit()
        print("Rol 'admin' creado.")
    else:
        print("Rol 'admin' ya existe.")

    # --- Asegurar que el rol 'editor' exista ---
    editor_rol = Rol.query.filter_by(nombre='editor').first()
    if not editor_rol:
        print("Rol 'editor' no encontrado, creándolo...")
        editor_rol = Rol(nombre='editor')
        db.session.add(editor_rol)
        db.session.commit()
        print("Rol 'editor' creado.")
    else:
        print("Rol 'editor' ya existe.")

    # --- Asegurar que el usuario 'admin' exista y tenga el rol correcto ---
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        print("Usuario 'admin' no encontrado, creándolo...")
        admin_user = User(username='admin', rol=admin_rol)
        admin_user.set_password('admin')
        db.session.add(admin_user)
        print("Usuario 'admin' creado.")
    else:
        print("Usuario 'admin' ya existe. Verificando rol...")
        if admin_user.rol != admin_rol:
            print("Asignando rol 'admin' al usuario 'admin'...")
            admin_user.rol = admin_rol
        else:
            print("Usuario 'admin' ya tiene el rol correcto.")
    
    db.session.commit()
    print("¡Base de datos lista!")