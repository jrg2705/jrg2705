# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, redirect, url_for, flash, request
import data_models as dm
import datetime
from flask_wtf import FlaskForm
import babel.numbers
from wtforms import StringField, SelectField, BooleanField, TextAreaField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

app = Flask(__name__)
# Necesitamos una SECRET_KEY para que Flask-WTF funcione (protección CSRF)
# En una aplicación real, esto debería ser un valor aleatorio y seguro, y no estar hardcodeado.
app.config['SECRET_KEY'] = 'una-clave-secreta-muy-dificil-de-adivinar'

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
    categorias_nav = dm.obtener_categorias_jerarquia()
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


# Lista temporal para "almacenar" solicitudes de crédito (solo para simulación)
solicitudes_credito_simuladas = []

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


@app.route('/sucursales')
def mostrar_sucursales():
    """Página que lista las sucursales."""
    sucursales = dm.sucursales_data
    return render_template('sucursales.html', sucursales=sucursales)

@app.route('/catalogo/')
def catalogo_general():
    """Página que muestra todos los productos del catálogo."""
    productos = dm.obtener_productos_con_detalles() # Sin filtro de categoría
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Todos los Productos")

@app.route('/categoria/<path:cat_principal_slug>/')
def catalogo_por_categoria_principal(cat_principal_slug):
    """Página que muestra productos de una categoría principal."""
    nombre_cat_principal, _ = dm.obtener_nombre_categoria(id_cat_principal_slug=cat_principal_slug)
    if not nombre_cat_principal:
        abort(404)

    # Obtener el ID de la categoría principal a partir del slug
    id_cat_principal = None
    for cat_info in dm.categorias_structure:
        if dm.slugify(cat_info["nombre_cat_principal"]) == cat_principal_slug:
            id_cat_principal = cat_info["id_cat_principal"]
            break

    productos = dm.obtener_productos_con_detalles(id_cat_principal_slug=cat_principal_slug)
    sugerencias_outlet = []
    if id_cat_principal: # Solo buscar sugerencias si encontramos el ID
        sugerencias_outlet = dm.obtener_sugerencias_especiales_para_categoria(
            id_cat_principal_actual=id_cat_principal,
            etiqueta_sugerencia="outlet",
            limite=3
        )

    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo=nombre_cat_principal,
                           breadcrumbs=[{"nombre": nombre_cat_principal, "url": None}],
                           sugerencias_outlet=sugerencias_outlet,
                           titulo_sugerencias="De Nuestro Outlet También Te Podría Interesar:")


@app.route('/categoria/<path:cat_principal_slug>/<path:sub_cat_slug>/')
def catalogo_por_subcategoria(cat_principal_slug, sub_cat_slug):
    """Página que muestra productos de una subcategoría."""
    nombre_cat_principal, nombre_sub_cat = dm.obtener_nombre_categoria(
        id_cat_principal_slug=cat_principal_slug,
        id_sub_cat_slug=sub_cat_slug
    )

    if not nombre_cat_principal or not nombre_sub_cat:
        abort(404)

    # Obtener IDs de categoría y subcategoría
    id_cat_principal = None
    id_subcategoria = None
    for cat_info in dm.categorias_structure:
        if dm.slugify(cat_info["nombre_cat_principal"]) == cat_principal_slug:
            id_cat_principal = cat_info["id_cat_principal"]
            for sub_info in cat_info.get("subcategorias", []):
                if dm.slugify(sub_info["nombre_subcategoria"]) == sub_cat_slug:
                    id_subcategoria = sub_info["id_subcategoria"]
                    break
            break

    productos = dm.obtener_productos_con_detalles(
        id_cat_principal_slug=cat_principal_slug,
        id_sub_cat_slug=sub_cat_slug
    )

    sugerencias_outlet = []
    if id_cat_principal and id_subcategoria: # Solo buscar si tenemos ambos IDs
        sugerencias_outlet = dm.obtener_sugerencias_especiales_para_categoria(
            id_cat_principal_actual=id_cat_principal,
            id_subcategoria_actual=id_subcategoria,
            etiqueta_sugerencia="outlet",
            limite=3
        )

    url_cat_principal = url_for('catalogo_por_categoria_principal', cat_principal_slug=cat_principal_slug)

    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo=f"{nombre_cat_principal} > {nombre_sub_cat}",
                           breadcrumbs=[
                               {"nombre": nombre_cat_principal, "url": url_cat_principal},
                               {"nombre": nombre_sub_cat, "url": None}
                           ],
                           sugerencias_outlet=sugerencias_outlet,
                           titulo_sugerencias="De Nuestro Outlet También Te Podría Interesar:")

@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    """Página de detalles de un producto específico."""
    # Usar la nueva función para obtener el producto ya enriquecido
    producto_enriquecido = dm.obtener_producto_enriquecido_por_id(producto_id)

    if not producto_enriquecido:
        abort(404, description="Producto no encontrado")

    # El producto ya viene con 'inicial' y 'disponibilidad_sucursales' y 'estado_disponibilidad_general'
    # y también 'imagenes_secundarias'

    # Breadcrumbs para el detalle del producto
    cat_principal_slug_producto = None
    sub_cat_slug_producto = None
    nombre_cat_principal_prod = None
    nombre_sub_cat_prod = None

    # Encontrar los slugs de categoría del producto
    for cat_hierarquia in dm.obtener_categorias_jerarquia():
        if cat_hierarquia['id_cat_principal'] == producto_enriquecido.get('id_cat_principal'):
            cat_principal_slug_producto = cat_hierarquia['slug_cat_principal']
            nombre_cat_principal_prod = cat_hierarquia['nombre_cat_principal']
            if producto_enriquecido.get('id_subcategoria'):
                for sub_cat_hierarquia in cat_hierarquia.get('subcategorias', []):
                    if sub_cat_hierarquia['id_subcategoria'] == producto_enriquecido.get('id_subcategoria'):
                        sub_cat_slug_producto = sub_cat_hierarquia['slug_subcategoria']
                        nombre_sub_cat_prod = sub_cat_hierarquia['nombre_subcategoria']
                        break
            break

    breadcrumbs_producto = []
    if nombre_cat_principal_prod and cat_principal_slug_producto:
        breadcrumbs_producto.append({
            "nombre": nombre_cat_principal_prod,
            "url": app.url_for('catalogo_por_categoria_principal', cat_principal_slug=cat_principal_slug_producto)
        })
        if nombre_sub_cat_prod and sub_cat_slug_producto:
            breadcrumbs_producto.append({
                "nombre": nombre_sub_cat_prod,
                "url": app.url_for('catalogo_por_subcategoria', cat_principal_slug=cat_principal_slug_producto, sub_cat_slug=sub_cat_slug_producto)
            })
    breadcrumbs_producto.append({"nombre": producto_enriquecido['nombre'], "url": None})


    return render_template('producto_detalle.html',
                           producto=producto_enriquecido, # Usar el producto enriquecido
                           # 'inicial' y 'disponibilidad_sucursales' ya están en producto_enriquecido
                           breadcrumbs_producto=breadcrumbs_producto)

# --- Rutas para las Secciones Especiales del Carrusel ---
@app.route('/ofertas-temporada/')
def ofertas_temporada():
    productos = dm.obtener_productos_por_etiqueta_especial("oferta_temporada")
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Ofertas de Temporada",
                           breadcrumbs=[{"nombre": "Ofertas de Temporada", "url": None}])

@app.route('/productos-destacados/')
def productos_destacados():
    productos = dm.obtener_productos_por_etiqueta_especial("destacado")
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Productos Destacados",
                           breadcrumbs=[{"nombre": "Productos Destacados", "url": None}])

@app.route('/outlet/')
def outlet():
    productos = dm.obtener_productos_por_etiqueta_especial("outlet")
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Outlet",
                           breadcrumbs=[{"nombre": "Outlet", "url": None}])

@app.route('/promociones/')
def promociones():
    productos = dm.obtener_productos_por_etiqueta_especial("promocion")
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Promociones",
                           breadcrumbs=[{"nombre": "Promociones", "url": None}])

@app.route('/nuevos-ingresos/')
def nuevos_ingresos():
    productos = dm.obtener_productos_por_etiqueta_especial("nuevo_ingreso")
    return render_template('catalogo.html',
                           productos=productos,
                           titulo_catalogo="Nuevos Ingresos",
                           breadcrumbs=[{"nombre": "Nuevos Ingresos", "url": None}])


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
