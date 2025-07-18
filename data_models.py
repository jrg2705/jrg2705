# -*- coding: utf-8 -*-
# Modelos de datos simulados para la tienda de electrodomésticos
import re
import math

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]+', '', text)
    return text

def calcular_inicial(precio_bruto):
    inicial_exacta = precio_bruto * 0.25
    if inicial_exacta <= 0:
        return 0.0
    inicial_redondeada_a_50 = math.ceil(inicial_exacta / 50.0) * 50.0
    return inicial_redondeada_a_50
