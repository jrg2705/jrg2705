# -*- coding: utf-8 -*-
import os
import datetime
import math
from flask import Flask, render_template, abort, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
import babel.numbers
from wtforms import StringField, SelectField, BooleanField, TextAreaField, SubmitField, TelField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
import uuid
from werkzeug.utils import secure_filename
from flask_admin.form.upload import ImageUploadField
from flask_migrate import Migrate

# --- 1. CONFIGURACIÓN DE LA APP ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'una-clave-secreta-muy-dificil-de-adivinar'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'tienda.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'img', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- 2. INICIALIZACIÓN DE EXTENSIONES ---
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- 3. MODELOS DE LA BASE DE DATOS ---
class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    def __repr__(self): return self.nombre

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    rol = db.relationship('Rol', backref='users')
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    subcategorias = db.relationship('SubCategoria', backref='categoria', lazy='dynamic')
    def __repr__(self): return self.nombre

class SubCategoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    productos = db.relationship('Producto', backref='subcategoria', lazy='dynamic')
    def __repr__(self): return f'{self.categoria.nombre} > {self.nombre}'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True) # <<< CAMBIO AQUÍ
    aplica_financiamiento = db.Column(db.Boolean, default=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    subcategoria_id = db.Column(db.Integer, db.ForeignKey('sub_categoria.id'), nullable=False)
    imagenes_secundarias = db.relationship('ImagenProducto', backref='producto', lazy='dynamic', cascade="all, delete-orphan")
    def __repr__(self): return self.nombre

class ImagenProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    def __repr__(self): return self.url

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    horario = db.Column(db.String(150), nullable=True)
    telefono = db.Column(db.String(100), nullable=True)
    mapa_iframe_html = db.Column(db.Text, nullable=True)
    def __repr__(self): return self.nombre

# --- 4. VISTAS DEL PANEL DE ADMINISTRACIÓN ---
class MyModelView(ModelView):
    def is_accessible(self): return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs): return redirect(url_for('login', next=request.url))

class UserAdminView(MyModelView):
    form_excluded_columns = ('password_hash',)
    form_extra_fields = {'password': PasswordField('Nueva Contraseña (dejar en blanco para no cambiar)')}
    def on_model_change(self, form, model, is_created):
        if form.password.data: model.set_password(form.password.data)
    def is_accessible(self): return current_user.is_authenticated and current_user.rol and current_user.rol.nombre == 'admin'

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = {'productos': Producto.query.count(),'categorias': Categoria.query.count(),'sucursales': Sucursal.query.count(),'usuarios': User.query.count()}
        return self.render('admin/index.html', stats=stats)
class ImagenProductoAdminView(MyModelView):
    def _list_thumbnail(view, context, model, name):
        try:
            if not model.url:
                return ''
            file_path = os.path.join('img/uploads', model.url)
            return f'<img src="{url_for("static", filename=file_path)}" width="100">'
        except Exception as e:
            print(f"Error cargando imagen: {e}")  # Esto lo imprime en consola/log
            return f"<small>Error cargando imagen: {e}</small>"

    column_formatters = {
        'url': _list_thumbnail
    }

    form_extra_fields = {
        'url': ImageUploadField(
            'Seleccionar Imagen',
            base_path=app.config['UPLOAD_FOLDER'],
            namegen=lambda obj, file_data: f"{uuid.uuid4().hex[:10]}-{secure_filename(file_data.filename)}"
        )
    }
    # # def _list_thumbnail(view, context, model, name):
    # #     try:
    # #         if not model.url:
    # #             return ''
    # #         file_path = os.path.join('img/uploads', model.url)
    # #         return f'<img src="{url_for("static", filename=file_path)}" width="100">'
    # #     except Exception as e:
    # #         return f"<small>Error cargando imagen: {e}</small>"
    # def _list_thumbnail(view, context, model, name):
    #     try:
    #         if not model.url:
    #             return ''
    #         # Usa ruta absoluta relativa a /static para evitar errores con url_for en admin
    #         return f'<img src="/static/img/uploads/{model.url}" width="100">'
    #     except Exception as e:
    #         return f"<small>Error cargando imagen: {e}</small>"

    # column_formatters = {
    #     'url': _list_thumbnail
    # }

    # Esto convierte el campo 'url' en un campo de subida de archivos
    form_extra_fields = {
        'url': ImageUploadField('Seleccionar Imagen',
                                base_path=app.config['UPLOAD_FOLDER'],
                                namegen=lambda obj, file_data: f"{uuid.uuid4().hex[:10]}-{secure_filename(file_data.filename)}"
                               )
    }

admin = Admin(app, name='Jabel Muebles - Admin', template_mode='bootstrap3', base_template='admin/my_master.html', index_view=MyAdminIndexView(name='Dashboard', url='/admin'))

admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(SubCategoria, db.session))
admin.add_view(MyModelView(Producto, db.session))
admin.add_view(ImagenProductoAdminView(ImagenProducto, db.session, name="Imagenes Secundarias"))
admin.add_view(MyModelView(Sucursal, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(MyModelView(Rol, db.session))

# --- 5. FORMULARIOS ---
class SolicitudCreditoForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(min=2, max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(min=2, max=100)])
    tipo_id = SelectField('Tipo de Identificación', choices=[('cedula', 'Cédula'), ('pasaporte', 'Pasaporte'), ('otro', 'Otro')], validators=[DataRequired()])
    numero_id = StringField('Número de Identificación', validators=[DataRequired(), Length(min=5, max=30)])
    direccion = TextAreaField('Dirección Completa', validators=[DataRequired(), Length(min=10, max=250)])
    telefono_movil = TelField('Teléfono Móvil', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$')])
    tiene_whatsapp = BooleanField('¿Este número tiene WhatsApp?', default=True)
    whatsapp_otro = TelField('Número de WhatsApp (si es diferente)', validators=[Optional(), Regexp(r'^\+?1?\d{9,15}$')])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    ingresos_mensuales = SelectField('Ingresos Mensuales (USD)', choices=[('0-500', '$0 - $500'), ('501-1000', '$501 - $1000'), ('1001-2000', '$1001 - $2000'), ('5000+', 'Más de $5000')], validators=[DataRequired()])
    producto_interes = StringField('Producto de Interés', validators=[Optional(), Length(max=150)])
    ref1_nombre = StringField('Referencia 1: Nombre', validators=[DataRequired(), Length(max=150)])
    ref1_telefono = TelField('Referencia 1: Teléfono', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$')])
    ref2_nombre = StringField('Referencia 2: Nombre', validators=[DataRequired(), Length(max=150)])
    ref2_telefono = TelField('Referencia 2: Teléfono', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$')])
    ref3_nombre = StringField('Referencia 3: Nombre', validators=[Optional(), Length(max=150)])
    ref3_telefono = TelField('Referencia 3: Teléfono', validators=[Optional(), Regexp(r'^\+?1?\d{9,15}$')])
    horario_contacto = SelectField('Horario de Contacto', choices=[('manana', 'Mañana'), ('tarde', 'Tarde'), ('noche', 'Noche')], validators=[DataRequired()])
    acepta_terminos = BooleanField('Acepto los Términos y Condiciones.', validators=[DataRequired(message="Debe aceptar los términos.")])
    submit = SubmitField('Enviar Solicitud')

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=3, max=100)])
    telefono = TelField('Teléfono', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$')])
    email = StringField('Email (Opcional)', validators=[Optional(), Email()])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(min=3, max=100)])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Enviar Mensaje')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# --- FILTRO JINJA2 PERSONALIZADO ---
def format_rd_currency(value):
    """Formatea un valor numérico como moneda en RD$ (Peso Dominicano)."""
    if value is None:
        return ""
    try:
        return babel.numbers.format_currency(value, 'DOP', locale='es_DO', currency_digits=True, format_type='standard')
    except Exception as e:
        print(f"Error formateando moneda: {e}")
        return str(value)

app.jinja_env.filters['format_rd'] = format_rd_currency

# --- 6. RUTAS DE LA APLICACIÓN ---
@app.context_processor
def inject_global_vars():
    categorias_nav = Categoria.query.order_by(Categoria.nombre).all()
    current_year = datetime.datetime.now().year
    return dict(categorias_nav=categorias_nav, current_year=current_year)

def calcular_y_formatear_inicial(precio):
    if precio is None or precio <= 0:
        return ""
    inicial_exacta = precio * 0.25
    # Redondear hacia arriba al múltiplo de 50 más cercano
    inicial_redondeada = math.ceil(inicial_exacta / 50.0) * 50.0
    # Usar nuestro filtro existente para darle formato de moneda
    return format_rd_currency(inicial_redondeada) # Asumiendo que format_rd_currency ya existe

app.jinja_env.filters['inicial_rd'] = calcular_y_formatear_inicial

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/sucursales')
def mostrar_sucursales():
    sucursales = Sucursal.query.order_by(Sucursal.nombre).all()
    return render_template('sucursales.html', sucursales=sucursales)

@app.route('/catalogo/')
def catalogo_general():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('catalogo_categorias.html', categorias=categorias, titulo_catalogo="Nuestros Departamentos")

@app.route('/categoria/<path:cat_principal_slug>/')
def catalogo_por_categoria_principal(cat_principal_slug):
    categoria = Categoria.query.filter_by(slug=cat_principal_slug).first_or_404()
    subcategorias_ids = [s.id for s in categoria.subcategorias]
    productos = Producto.query.filter(Producto.subcategoria_id.in_(subcategorias_ids)).all()
    return render_template('catalogo.html', productos=productos, titulo_catalogo=categoria.nombre, breadcrumbs=[{"nombre": categoria.nombre, "url": None}])

@app.route('/categoria/<path:cat_principal_slug>/<path:sub_cat_slug>/')
def catalogo_por_subcategoria(cat_principal_slug, sub_cat_slug):
    categoria = Categoria.query.filter_by(slug=cat_principal_slug).first_or_404()
    subcategoria = SubCategoria.query.filter_by(slug=sub_cat_slug, categoria_id=categoria.id).first_or_404()
    productos = subcategoria.productos.all()
    url_cat_principal = url_for('catalogo_por_categoria_principal', cat_principal_slug=categoria.slug)
    return render_template('catalogo.html', productos=productos, titulo_catalogo=subcategoria.nombre, breadcrumbs=[{"nombre": categoria.nombre, "url": url_cat_principal}, {"nombre": subcategoria.nombre, "url": None}])

@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    subcategoria = producto.subcategoria
    categoria = subcategoria.categoria
    breadcrumbs_producto = [
        {"nombre": categoria.nombre, "url": url_for('catalogo_por_categoria_principal', cat_principal_slug=categoria.slug)},
        {"nombre": subcategoria.nombre, "url": url_for('catalogo_por_subcategoria', cat_principal_slug=categoria.slug, sub_cat_slug=subcategoria.slug)},
        {"nombre": producto.nombre, "url": None}
    ]
    return render_template('producto_detalle.html', producto=producto, breadcrumbs_producto=breadcrumbs_producto)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        flash('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('contacto'))
    return render_template('contacto.html', form=form)

@app.route('/solicitud-credito', methods=['GET', 'POST'])
def solicitud_credito():
    form = SolicitudCreditoForm()
    if form.validate_on_submit():
        flash('¡Su solicitud de crédito ha sido enviada con éxito!', 'success')
        return redirect(url_for('solicitud_enviada'))
    return render_template('solicitud_credito.html', form=form)

@app.route('/solicitud-enviada')
def solicitud_enviada():
    return render_template('solicitud_enviada.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Usuario o contraseña inválidos', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)