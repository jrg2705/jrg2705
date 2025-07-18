# -*- coding: utf-8 -*-
# Modelos de datos simulados para la tienda de electrodomésticos
import re
import math

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]+', '', text)
    return text

sucursales_data = [
    {"id": 1, "nombre": "Sucursal Centro", "direccion": "Calle Falsa 123, Ciudad Capital", "horario": "Lunes a Sábado: 9:00 - 20:00", "telefono": "555-1234", "mapa_iframe_html": ""},
    {"id": 2, "nombre": "Sucursal Norte", "direccion": "Avenida Siempre Viva 742, Distrito Norte", "horario": "Lunes a Viernes: 10:00 - 19:00, Sábado: 10:00 - 15:00", "telefono": "555-5678", "mapa_iframe_html": ""},
    {"id": 3, "nombre": "Sucursal Sur", "direccion": "Boulevard de los Sueños Rotos 45, Sector Sur", "horario": "Lunes a Sábado: 9:30 - 20:30", "telefono": "555-9012", "mapa_iframe_html": ""},
    {"id": 4, "nombre": "Sucursal Este Principal", "direccion": "Avenida del Sol Naciente 88, Zona Este", "horario": "Lunes a Sábado: 9:00 - 19:30", "telefono": "555-3456", "mapa_iframe_html": ""},
    {"id": 5, "nombre": "Sucursal Oeste Comercial", "direccion": "Camino del Ocaso 101, Barrio Oeste", "horario": "Lunes a Viernes: 10:00 - 20:00, Sábado: 10:00 - 16:00", "telefono": "555-7890", "mapa_iframe_html": ""}
]

def calcular_inicial(precio_bruto):
    inicial_exacta = precio_bruto * 0.25
    if inicial_exacta <= 0:
        return 0.0
    inicial_redondeada_a_50 = math.ceil(inicial_exacta / 50.0) * 50.0
    return inicial_redondeada_a_50
