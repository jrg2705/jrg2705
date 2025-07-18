# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, abort, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_wtf import FlaskForm
import babel.numbers
from wtforms import StringField, SelectField, BooleanField, TextAreaField, SubmitField, TelField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una-clave-secreta-muy-dificil-de-adivinar'
# Configuración de la base de datos SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tienda.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Vista a la que redirigir si se requiere login
admin = Admin(app, name='Electro Hogar Admin', template_mode='bootstrap3')

# --- Modelos de la Base de Datos ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    subcategorias = db.relationship('SubCategoria', backref='categoria', lazy=True)

    def __repr__(self):
        return self.nombre

class SubCategoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    productos = db.relationship('Producto', backref='subcategoria', lazy=True)

    def __repr__(self):
        return f'{self.categoria.nombre} > {self.nombre}'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('sub_categoria.id'), nullable=False)
    # Aquí podríamos añadir más campos como 'stock', 'etiquetas', etc.

    def __repr__(self):
        return self.nombre

# --- Vistas del Panel de Administración ---
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(SubCategoria, db.session))
admin.add_view(MyModelView(Producto, db.session))

# --- Definición del Formulario de Solicitud de Crédito ---
class SolicitudCreditoForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])

    tipo_id = SelectField('Tipo de Identificación',
                          choices=[
                              ('cedula', 'Cédula de Ciudadanía'),
                              ('pasaporte', 'Pasaporte'),
                              ('carnet_extranjeria', 'Carnet de Extranjería'),
                              ('otro', 'Otro')
                          ],
                          validators=[DataRequired()])
    numero_id = StringField('Número de Identificación', validators=[DataRequired(), Length(min=5, max=30)])

    direccion = TextAreaField('Dirección Completa (Calle, Ciudad, Estado, Código Postal)',
                              validators=[DataRequired(), Length(min=10, max=250)])

    telefono_movil = TelField('Teléfono Móvil Principal',
                                validators=[DataRequired(),
                                            Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")])

    tiene_whatsapp = BooleanField('¿Este número tiene WhatsApp?', default=True)
    whatsapp_otro = TelField('Número de WhatsApp (si es diferente)',
                               validators=[Optional(),
                                           Regexp(r'^\+?1?\d{9,15}$', message="Número de WhatsApp inválido.")])

    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])

    ingresos_mensuales = SelectField('Ingresos Mensuales Aproximados (USD)',
                                     choices=[
                                         ('0-500', '$0 - $500'),
                                         ('501-1000', '$501 - $1000'),
                                         ('1001-2000', '$1001 - $2000'),
                                         ('2001-5000', '$2001 - $5000'),
                                         ('5000+', 'Más de $5000')
                                     ], validators=[DataRequired()])

    producto_interes = StringField('Producto de Interés (Opcional)', validators=[Optional(), Length(max=150)])

    # Referencias Personales
    ref1_nombre = StringField('Referencia Personal 1: Nombre Completo', validators=[DataRequired(), Length(max=150)])
    ref1_telefono = TelField('Referencia Personal 1: Teléfono',
                               validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")])

    ref2_nombre = StringField('Referencia Personal 2: Nombre Completo', validators=[DataRequired(), Length(max=150)])
    ref2_telefono = TelField('Referencia Personal 2: Teléfono',
                               validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")])

    ref3_nombre = StringField('Referencia Personal 3: Nombre Completo', validators=[Optional(), Length(max=150)])
    ref3_telefono = TelField('Referencia Personal 3: Teléfono',
                               validators=[Optional(), Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")])

    horario_contacto = SelectField('Horario de Contacto Preferido',
                                   choices=[
                                       ('manana', 'Mañana (9am - 12pm)'),
                                       ('tarde', 'Tarde (2pm - 6pm)'),
                                       ('noche', 'Noche (7pm - 9pm)'),
                                       ('cualquiera', 'Cualquier Horario')
                                   ], validators=[DataRequired()])

    acepta_terminos = BooleanField('Acepto los Términos y Condiciones y la Política de Privacidad.',
                                   validators=[DataRequired(message="Debe aceptar los términos para continuar.")])

    submit = SubmitField('Enviar Solicitud de Crédito')


# Context processor para que las categorías y el año actual estén disponibles en todas las plantillas
@app.context_processor
def inject_global_vars():
    categorias_nav = Categoria.query.order_by(Categoria.nombre).all()
    current_year = datetime.datetime.now().year
    return dict(categorias_nav=categorias_nav, current_year=current_year)

# --- Filtro Jinja2 Personalizado para Formato de Moneda RD$ ---
def format_rd_currency(value):
    """Formatea un valor numérico como moneda en RD$ (Peso Dominicano)."""
    if value is None:
        return ""
    # Locale 'es_DO' para formato dominicano, 'DOP' es el código de la moneda.
    # currency_digits=True asegura que se muestren los decimales (ej. .00)
    # format_type='standard' usa el símbolo de moneda correcto (RD$)
    try:
        return babel.numbers.format_currency(value, 'DOP', locale='es_DO', currency_digits=True, format_type='standard')
    except Exception as e:
        # En caso de algún error con Babel o el valor, retornar el valor original como string
        print(f"Error formateando moneda: {e}")
        return str(value)

app.jinja_env.filters['format_rd'] = format_rd_currency


# --- Definición del Formulario de Contacto ---
class ContactoForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=3, max=100)])
    telefono = TelField('Teléfono de Contacto', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")])
    email = StringField('Correo Electrónico (Opcional)', validators=[Optional(), Email()])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(min=3, max=100)])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Enviar Mensaje')

# Lista temporal para "almacenar" solicitudes de crédito (solo para simulación)
solicitudes_credito_simuladas = []
# Lista temporal para "almacenar" mensajes de contacto
mensajes_contacto_simulados = []

# --- Formulario de Login ---
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# --- Rutas de Autenticación ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('inicio'))

# --- Comando para crear usuario admin y DB ---
@app.cli.command("init-db")
def init_db_command():
    """Crea las tablas de la base de datos y un usuario admin."""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('admin')
            db.session.add(admin_user)
            db.session.commit()
            print('Base de datos inicializada y usuario admin creado.')
        else:
            print('El usuario admin ya existe.')

@app.route('/')
def inicio():
    """Página de inicio."""
    return render_template('index.html')

@app.route('/solicitud-credito', methods=['GET', 'POST'])
def solicitud_credito():
    producto_de_interes = request.args.get('producto_interes', None)
    form = SolicitudCreditoForm(producto_interes=producto_de_interes) # Pre-llenar si viene de producto_detalle

    if form.validate_on_submit():
        # Procesar los datos del formulario
        datos_solicitud = {
            'nombres': form.nombres.data,
            'apellidos': form.apellidos.data,
            'tipo_id': form.tipo_id.data,
            'numero_id': form.numero_id.data,
            'direccion': form.direccion.data,
            'telefono_movil': form.telefono_movil.data,
            'tiene_whatsapp': form.tiene_whatsapp.data,
            'whatsapp_otro': form.whatsapp_otro.data if not form.tiene_whatsapp.data else None,
            'email': form.email.data,
            'ingresos_mensuales': form.ingresos_mensuales.data,
            'producto_interes': form.producto_interes.data,
            'ref1_nombre': form.ref1_nombre.data,
            'ref1_telefono': form.ref1_telefono.data,
            'ref2_nombre': form.ref2_nombre.data,
            'ref2_telefono': form.ref2_telefono.data,
            'ref3_nombre': form.ref3_nombre.data,
            'ref3_telefono': form.ref3_telefono.data,
            'horario_contacto': form.horario_contacto.data,
            'acepta_terminos': form.acepta_terminos.data,
            'fecha_solicitud': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Simulación de almacenamiento
        solicitudes_credito_simuladas.append(datos_solicitud)
        print(f"Nueva solicitud de crédito recibida: {datos_solicitud}") # Para depuración en consola

        flash('¡Su solicitud de crédito ha sido enviada con éxito!', 'success')
        # Opcionalmente, pasar datos a la plantilla de confirmación:
        # return render_template('solicitud_enviada.html', datos_enviados=datos_solicitud)
        return redirect(url_for('solicitud_enviada'))

    # Si hay errores de validación, se mostrarán en el formulario automáticamente
    return render_template('solicitud_credito.html', form=form)

@app.route('/solicitud-enviada')
def solicitud_enviada():
    # Esta ruta es solo para mostrar la página de confirmación después de una redirección.
    # No se pasan datos directamente aquí usualmente si se usa flash para el mensaje.
    return render_template('solicitud_enviada.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        nuevo_mensaje = {
            'nombre': form.nombre.data,
            'telefono': form.telefono.data,
            'email': form.email.data,
            'provincia': form.provincia.data,
            'mensaje': form.mensaje.data,
            'fecha': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        mensajes_contacto_simulados.append(nuevo_mensaje)
        print(f"Nuevo mensaje de contacto: {nuevo_mensaje}") # Para depuración
        flash('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html', form=form)


@app.route('/sucursales')
def mostrar_sucursales():
    """Página que lista las sucursales."""
    sucursales = dm.sucursales_data
    return render_template('sucursales.html', sucursales=sucursales)

@app.route('/catalogo/')
def catalogo_general():
    """Página que muestra las categorías principales del catálogo."""
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('catalogo_categorias.html',
                           categorias=categorias,
                           titulo_catalogo="Explora Nuestras Categorías")

@app.route('/categoria/<path:cat_principal_slug>/')
def catalogo_por_categoria_principal(cat_principal_slug):
    """Página que muestra productos de una categoría principal."""
    categoria = Categoria.query.filter_by(slug=cat_principal_slug).first_or_404()

    # Obtener todos los productos de todas las subcategorías de esta categoría principal
    productos = []
    for subcat in categoria.subcategorias:
        productos.extend(subcat.productos)

    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo=categoria.nombre,
                           breadcrumbs=[{"nombre": categoria.nombre, "url": None}])


@app.route('/categoria/<path:cat_principal_slug>/<path:sub_cat_slug>/')
def catalogo_por_subcategoria(cat_principal_slug, sub_cat_slug):
    """Página que muestra productos de una subcategoría."""
    categoria = Categoria.query.filter_by(slug=cat_principal_slug).first_or_404()
    subcategoria = SubCategoria.query.filter_by(slug=sub_cat_slug, categoria_id=categoria.id).first_or_404()

    productos = subcategoria.productos

    url_cat_principal = url_for('catalogo_por_categoria_principal', cat_principal_slug=categoria.slug)

    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo=f"{categoria.nombre} > {subcategoria.nombre}",
                           breadcrumbs=[
                               {"nombre": categoria.nombre, "url": url_cat_principal},
                               {"nombre": subcategoria.nombre, "url": None}
                           ])

@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """Página de detalles de un producto específico."""
    producto = Producto.query.get_or_404(producto_id)

    # Breadcrumbs para el detalle del producto
    subcategoria = producto.subcategoria
    categoria = subcategoria.categoria

    breadcrumbs_producto = [
        {"nombre": categoria.nombre, "url": url_for('catalogo_por_categoria_principal', cat_principal_slug=categoria.slug)},
        {"nombre": subcategoria.nombre, "url": url_for('catalogo_por_subcategoria', cat_principal_slug=categoria.slug, sub_cat_slug=subcategoria.slug)},
        {"nombre": producto.nombre, "url": None}
    ]

    return render_template('producto_detalle.html',
                           producto=producto,
                           breadcrumbs_producto=breadcrumbs_producto)



# Manejador de errores 404
@app.errorhandler(404)
def pagina_no_encontrada(e):
    mensaje = "Lo sentimos, la página que buscas no existe o el recurso no fue encontrado."
    # Si el error tiene una descripción específica (ej. desde abort(404, description="..."))
    if hasattr(e, 'description') and e.description:
        mensaje = e.description
    return render_template('404.html', mensaje=mensaje), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001) # Asegurar que escuche en todas las interfaces
