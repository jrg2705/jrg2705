# -*- coding: utf-8 -*-
# Modelos de datos simulados para la tienda de electrodomésticos
import re
import math

# --- ESTRUCTURA DE CATEGORÍAS ---
# id_cat_principal debe ser único. id_subcategoria debe ser único dentro de su categoría principal.
categorias_structure = [
    {
        "id_cat_principal": "cocina",
        "nombre_cat_principal": "Cocina",
        "subcategorias": [
            {"id_subcategoria": "refrigeradores", "nombre_subcategoria": "Refrigeradores"},
            {"id_subcategoria": "estufas", "nombre_subcategoria": "Estufas"},
            {"id_subcategoria": "microondas", "nombre_subcategoria": "Microondas"},
            {"id_subcategoria": "licuadoras", "nombre_subcategoria": "Licuadoras"},
            {"id_subcategoria": "cafeteras", "nombre_subcategoria": "Cafeteras"},
            {"id_subcategoria": "tostadoras", "nombre_subcategoria": "Tostadoras"},
        ]
    },
    {
        "id_cat_principal": "lavanderia",
        "nombre_cat_principal": "Lavandería",
        "subcategorias": [
            {"id_subcategoria": "lavadoras", "nombre_subcategoria": "Lavadoras"},
            {"id_subcategoria": "secadoras", "nombre_subcategoria": "Secadoras"},
        ]
    },
    {
        "id_cat_principal": "sala",
        "nombre_cat_principal": "Sala",
        "subcategorias": [
            {"id_subcategoria": "televisores", "nombre_subcategoria": "Televisores"},
            {"id_subcategoria": "sistemas-sonido", "nombre_subcategoria": "Sistemas de Sonido"},
            {"id_subcategoria": "muebles-sala", "nombre_subcategoria": "Muebles de Sala"},
            {"id_subcategoria": "mesas-centro", "nombre_subcategoria": "Mesas de Centro"},
        ]
    },
    {
        "id_cat_principal": "comedor",
        "nombre_cat_principal": "Comedor",
        "subcategorias": [
            {"id_subcategoria": "juegos-comedor", "nombre_subcategoria": "Juegos de Comedor"},
            {"id_subcategoria": "sillas-comedor", "nombre_subcategoria": "Sillas de Comedor"},
        ]
    },
    {
        "id_cat_principal": "habitacion",
        "nombre_cat_principal": "Habitación",
        "subcategorias": [
            {"id_subcategoria": "colchones", "nombre_subcategoria": "Colchones"},
            {"id_subcategoria": "juegos-habitacion", "nombre_subcategoria": "Juegos de Habitación"},
            {"id_subcategoria": "mesas-noche", "nombre_subcategoria": "Mesas de Noche"},
        ]
    },
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]+', '', text)
    return text

sucursales_data = [
    {"id": 1, "nombre": "Sucursal Centro", "direccion": "Calle Falsa 123, Ciudad Capital", "horario": "Lunes a Sábado: 9:00 - 20:00", "telefono": "555-1234"},
    {"id": 2, "nombre": "Sucursal Norte", "direccion": "Avenida Siempre Viva 742, Distrito Norte", "horario": "Lunes a Viernes: 10:00 - 19:00, Sábado: 10:00 - 15:00", "telefono": "555-5678"},
    {"id": 3, "nombre": "Sucursal Sur", "direccion": "Boulevard de los Sueños Rotos 45, Sector Sur", "horario": "Lunes a Sábado: 9:30 - 20:30", "telefono": "555-9012"}
]

productos_data = [
    {
        "id": 101, "nombre": "Refrigerador Inteligente 300L", "descripcion": "Refrigerador con tecnología NoFrost, dispensador de agua y hielo, conexión Wi-Fi.",
        "precio": 1200.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Refrigerador",
        "imagenes_secundarias": [
            "https://via.placeholder.com/400x400.png?text=Refrigerador+Vista+Interna",
            "https://via.placeholder.com/400x400.png?text=Refrigerador+Detalle+Dispensador",
            "https://via.placeholder.com/400x400.png?text=Refrigerador+Perfil"
        ],
        "id_cat_principal": "cocina", "id_subcategoria": "refrigeradores",
        "etiquetas_especiales": ["destacado", "nuevo_ingreso"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 102, "nombre": "Lavadora Carga Frontal 15kg", "descripcion": "Lavadora eficiente con múltiples ciclos de lavado y motor Inverter.",
        "precio": 850.50, "imagen_url": "https://via.placeholder.com/300x300.png?text=Lavadora",
        "imagenes_secundarias": [
            "https://via.placeholder.com/400x400.png?text=Lavadora+Panel",
            "https://via.placeholder.com/400x400.png?text=Lavadora+Tambor"
        ],
        "id_cat_principal": "lavanderia", "id_subcategoria": "lavadoras",
        "etiquetas_especiales": ["oferta_temporada"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 103, "nombre": "Televisor LED 4K 55 pulgadas", "descripcion": "Smart TV con resolución 4K UHD, HDR y sistema operativo integrado.",
        "precio": 999.99, "imagen_url": "https://via.placeholder.com/300x300.png?text=Televisor",
        "imagenes_secundarias": [
            "https://via.placeholder.com/400x400.png?text=TV+Pantalla",
            "https://via.placeholder.com/400x400.png?text=TV+Conexiones",
            "https://via.placeholder.com/400x400.png?text=TV+Control+Remoto"
        ],
        "id_cat_principal": "sala", "id_subcategoria": "televisores",
        "etiquetas_especiales": ["destacado", "promocion"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 104, "nombre": "Horno Microondas Usado Modelo X", "descripcion": "Horno de microondas con panel digital. Buen estado, ligeras marcas de uso.",
        "precio": 75.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Microondas+Outlet",
        "imagenes_secundarias": ["https://via.placeholder.com/400x400.png?text=Microondas+Outlet+Detalle"],
        "id_cat_principal": "cocina", "id_subcategoria": "microondas",
        "etiquetas_especiales": ["outlet"],
        "es_item_catalogo_regular": False
    },
    {
        "id": 105, "nombre": "Licuadora de Alta Potencia", "descripcion": "Licuadora con vaso de vidrio, 1000W de potencia y cuchillas de acero inoxidable.",
        "precio": 90.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Licuadora",
        "imagenes_secundarias": ["https://via.placeholder.com/400x400.png?text=Licuadora+Vaso"],
        "id_cat_principal": "cocina", "id_subcategoria": "licuadoras",
        "etiquetas_especiales": ["nuevo_ingreso", "promocion"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 106, "nombre": "Colchón Queen Ortopédico", "descripcion": "Colchón tamaño Queen con soporte ortopédico y tela antiácaros.",
        "precio": 450.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Colchon",
        "imagenes_secundarias": [],
        "id_cat_principal": "habitacion", "id_subcategoria": "colchones",
        "etiquetas_especiales": ["oferta_temporada"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 107, "nombre": "Juego de Comedor 4 Puestos - Descontinuado", "descripcion": "Juego de comedor de madera, modelo anterior. Algunas sillas con detalles.",
        "precio": 150.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Comedor+Outlet",
        "imagenes_secundarias": [],
        "id_cat_principal": "comedor", "id_subcategoria": "juegos-comedor",
        "etiquetas_especiales": ["outlet"],
        "es_item_catalogo_regular": False
    },
    {
        "id": 108, "nombre": "Sofá Modular Esquinero", "descripcion": "Sofá modular de 3 piezas, tapizado en tela gris, ideal para sala.",
        "precio": 780.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Sofa",
        "imagenes_secundarias": [
            "https://via.placeholder.com/400x400.png?text=Sofa+Detalle1",
            "https://via.placeholder.com/400x400.png?text=Sofa+Detalle2"
        ],
        "id_cat_principal": "sala", "id_subcategoria": "muebles-sala",
        "etiquetas_especiales": ["destacado"],
        "es_item_catalogo_regular": True
    },
    {
        "id": 109, "nombre": "Estufa de Gas 4 Quemadores - Outlet", "descripcion": "Estufa de gas con 4 quemadores, horno funcional. Presenta algunos rayones en la superficie. Ideal para repuestos o uso básico.",
        "precio": 95.00, "imagen_url": "https://via.placeholder.com/300x300.png?text=Estufa+Outlet",
        "imagenes_secundarias": [
            "https://via.placeholder.com/400x400.png?text=Estufa+Outlet+Rayon",
            "https://via.placeholder.com/400x400.png?text=Estufa+Outlet+Quemador"
        ],
        "id_cat_principal": "cocina", "id_subcategoria": "estufas",
        "etiquetas_especiales": ["outlet"],
        "es_item_catalogo_regular": False
    },
]

inventario_data = [
    {"producto_id": 101, "sucursal_id": 1, "cantidad_disponible": 5}, {"producto_id": 101, "sucursal_id": 2, "cantidad_disponible": 2}, {"producto_id": 101, "sucursal_id": 3, "cantidad_disponible": 0},
    {"producto_id": 102, "sucursal_id": 1, "cantidad_disponible": 3}, {"producto_id": 102, "sucursal_id": 2, "cantidad_disponible": 4}, {"producto_id": 102, "sucursal_id": 3, "cantidad_disponible": 1},
    {"producto_id": 103, "sucursal_id": 1, "cantidad_disponible": 6}, {"producto_id": 103, "sucursal_id": 2, "cantidad_disponible": 8}, {"producto_id": 103, "sucursal_id": 3, "cantidad_disponible": 3},
    {"producto_id": 104, "sucursal_id": 1, "cantidad_disponible": 10}, {"producto_id": 104, "sucursal_id": 2, "cantidad_disponible": 0}, {"producto_id": 104, "sucursal_id": 3, "cantidad_disponible": 7},
    {"producto_id": 105, "sucursal_id": 1, "cantidad_disponible": 12}, {"producto_id": 105, "sucursal_id": 2, "cantidad_disponible": 5}, {"producto_id": 105, "sucursal_id": 3, "cantidad_disponible": 8},
    {"producto_id": 106, "sucursal_id": 1, "cantidad_disponible": 4}, {"producto_id": 106, "sucursal_id": 2, "cantidad_disponible": 1}, {"producto_id": 106, "sucursal_id": 3, "cantidad_disponible": 3},
    {"producto_id": 107, "sucursal_id": 1, "cantidad_disponible": 2}, {"producto_id": 107, "sucursal_id": 2, "cantidad_disponible": 3}, {"producto_id": 107, "sucursal_id": 3, "cantidad_disponible": 1},
    {"producto_id": 108, "sucursal_id": 1, "cantidad_disponible": 1}, {"producto_id": 108, "sucursal_id": 2, "cantidad_disponible": 0}, {"producto_id": 108, "sucursal_id": 3, "cantidad_disponible": 2},
    {"producto_id": 109, "sucursal_id": 1, "cantidad_disponible": 1},
    {"producto_id": 109, "sucursal_id": 2, "cantidad_disponible": 0},
    {"producto_id": 109, "sucursal_id": 3, "cantidad_disponible": 1},
]

# --- FUNCIONES AUXILIARES ---

def obtener_producto_por_id(producto_id):
    for producto in productos_data:
        if producto["id"] == producto_id:
            return producto
    return None

def obtener_sucursal_por_id(sucursal_id):
    for sucursal in sucursales_data:
        if sucursal["id"] == sucursal_id:
            return sucursal
    return None

def obtener_disponibilidad_producto(producto_id, sucursal_id):
    for item in inventario_data:
        if item["producto_id"] == producto_id and item["sucursal_id"] == sucursal_id:
            return item["cantidad_disponible"]
    return 0

def calcular_inicial(precio_bruto):
    inicial_exacta = precio_bruto * 0.25
    if inicial_exacta <= 0:
        return 0.0
    inicial_redondeada_a_50 = math.ceil(inicial_exacta / 50.0) * 50.0
    return inicial_redondeada_a_50

def obtener_categorias_jerarquia():
    categorias_con_slugs = []
    for cat_principal in categorias_structure:
        cp_slug = slugify(cat_principal["nombre_cat_principal"])
        subcategorias_con_slugs = []
        for sub_cat in cat_principal.get("subcategorias", []):
            subcategorias_con_slugs.append({
                "id_subcategoria": sub_cat["id_subcategoria"],
                "nombre_subcategoria": sub_cat["nombre_subcategoria"],
                "slug_subcategoria": slugify(sub_cat["nombre_subcategoria"])
            })
        categorias_con_slugs.append({
            "id_cat_principal": cat_principal["id_cat_principal"],
            "nombre_cat_principal": cat_principal["nombre_cat_principal"],
            "slug_cat_principal": cp_slug,
            "subcategorias": subcategorias_con_slugs
        })
    return categorias_con_slugs

def obtener_nombre_categoria(id_cat_principal_slug=None, id_sub_cat_slug=None):
    if id_cat_principal_slug:
        for cat_principal in categorias_structure:
            if slugify(cat_principal["nombre_cat_principal"]) == id_cat_principal_slug:
                if id_sub_cat_slug:
                    for sub_cat in cat_principal.get("subcategorias", []):
                        if slugify(sub_cat["nombre_subcategoria"]) == id_sub_cat_slug:
                            return cat_principal["nombre_cat_principal"], sub_cat["nombre_subcategoria"]
                    return cat_principal["nombre_cat_principal"], None
                return cat_principal["nombre_cat_principal"], None
    return None, None

def obtener_productos_con_detalles(id_cat_principal_slug=None, id_sub_cat_slug=None):
    productos_filtrados = []
    id_cat_principal_target = None
    id_sub_cat_target = None

    if id_cat_principal_slug:
        for cat_p in categorias_structure:
            if slugify(cat_p["nombre_cat_principal"]) == id_cat_principal_slug:
                id_cat_principal_target = cat_p["id_cat_principal"]
                if id_sub_cat_slug:
                    for sub_c in cat_p.get("subcategorias", []):
                        if slugify(sub_c["nombre_subcategoria"]) == id_sub_cat_slug:
                            id_sub_cat_target = sub_c["id_subcategoria"]
                            break
                break

    for prod_original in productos_data:
        if (id_cat_principal_slug or id_sub_cat_slug) and not prod_original.get("es_item_catalogo_regular", True):
            continue

        if id_cat_principal_target:
            if prod_original["id_cat_principal"] != id_cat_principal_target:
                continue
            if id_sub_cat_target and prod_original.get("id_subcategoria") != id_sub_cat_target:
                continue

        prod_actual = prod_original.copy()
        prod_actual["inicial"] = calcular_inicial(prod_actual["precio"])

        disponibilidad_sucursales_lista = []
        total_disponible_en_tiendas = 0
        for suc in sucursales_data:
            cantidad = obtener_disponibilidad_producto(prod_actual["id"], suc["id"])
            disponibilidad_sucursales_lista.append({
                "sucursal_nombre": suc["nombre"],
                "cantidad": cantidad
            })
            total_disponible_en_tiendas += cantidad

        prod_actual["disponibilidad_sucursales"] = disponibilidad_sucursales_lista

        if total_disponible_en_tiendas > 0:
            prod_actual["estado_disponibilidad_general"] = "Disponible"
        else:
            prod_actual["estado_disponibilidad_general"] = "Agotado"

        productos_filtrados.append(prod_actual)

    return productos_filtrados

def obtener_productos_con_disponibilidad():
    return obtener_productos_con_detalles()

def obtener_productos_por_etiqueta_especial(etiqueta_buscada):
    productos_filtrados_por_etiqueta = []
    for prod_original in productos_data:
        if etiqueta_buscada in prod_original.get("etiquetas_especiales", []):
            prod_actual = prod_original.copy()
            prod_actual["inicial"] = calcular_inicial(prod_actual["precio"])
            disponibilidad_sucursales_lista = []
            total_disponible_en_tiendas = 0
            for suc in sucursales_data:
                cantidad = obtener_disponibilidad_producto(prod_actual["id"], suc["id"])
                disponibilidad_sucursales_lista.append({
                    "sucursal_nombre": suc["nombre"],
                    "cantidad": cantidad
                })
                total_disponible_en_tiendas += cantidad
            prod_actual["disponibilidad_sucursales"] = disponibilidad_sucursales_lista
            if total_disponible_en_tiendas > 0:
                prod_actual["estado_disponibilidad_general"] = "Disponible"
            else:
                prod_actual["estado_disponibilidad_general"] = "Agotado"
            if "imagenes_secundarias" not in prod_actual:
                prod_actual["imagenes_secundarias"] = []
            productos_filtrados_por_etiqueta.append(prod_actual)
    return productos_filtrados_por_etiqueta

def obtener_sugerencias_especiales_para_categoria(id_cat_principal_actual, id_subcategoria_actual=None, etiqueta_sugerencia="outlet", limite=3):
    sugerencias = []
    count = 0
    for prod_original in productos_data:
        es_sugerible_por_regularidad = False
        if etiqueta_sugerencia == "outlet":
            if not prod_original.get("es_item_catalogo_regular", True):
                es_sugerible_por_regularidad = True
        else:
            if etiqueta_sugerencia in prod_original.get("etiquetas_especiales", []):
                 es_sugerible_por_regularidad = True

        if not es_sugerible_por_regularidad:
            continue

        if prod_original.get("id_cat_principal") != id_cat_principal_actual:
            continue

        if id_subcategoria_actual and prod_original.get("id_subcategoria") != id_subcategoria_actual:
            continue

        if etiqueta_sugerencia != "outlet" and etiqueta_sugerencia not in prod_original.get("etiquetas_especiales", []):
            continue
        elif etiqueta_sugerencia == "outlet" and "outlet" not in prod_original.get("etiquetas_especiales", []):
            continue

        # Enriquecer el producto
        prod_actual = prod_original.copy()
        prod_actual["inicial"] = calcular_inicial(prod_actual["precio"]) # Esta es la línea 411 del traceback original
        total_disponible_en_tiendas = 0
        for suc in sucursales_data:
            total_disponible_en_tiendas += obtener_disponibilidad_producto(prod_actual["id"], suc["id"])

        if total_disponible_en_tiendas > 0:
            prod_actual["estado_disponibilidad_general"] = "Disponible"
        else:
            prod_actual["estado_disponibilidad_general"] = "Agotado"

        if "imagenes_secundarias" not in prod_actual:
            prod_actual["imagenes_secundarias"] = []

        sugerencias.append(prod_actual)
        count += 1
        if count >= limite:
            break
    return sugerencias

def obtener_producto_enriquecido_por_id(producto_id):
    prod_original = obtener_producto_por_id(producto_id)
    if not prod_original:
        return None
    prod_actual = prod_original.copy()
    prod_actual["inicial"] = calcular_inicial(prod_actual["precio"])
    disponibilidad_sucursales_lista = []
    total_disponible_en_tiendas = 0
    for suc in sucursales_data:
        cantidad = obtener_disponibilidad_producto(prod_actual["id"], suc["id"])
        disponibilidad_sucursales_lista.append({
            "sucursal_nombre": suc["nombre"],
            "cantidad": cantidad
        })
        total_disponible_en_tiendas += cantidad
    prod_actual["disponibilidad_sucursales"] = disponibilidad_sucursales_lista
    if total_disponible_en_tiendas > 0:
        prod_actual["estado_disponibilidad_general"] = "Disponible"
    else:
        prod_actual["estado_disponibilidad_general"] = "Agotado"
    if "imagenes_secundarias" not in prod_actual:
        prod_actual["imagenes_secundarias"] = []
    if "etiquetas_especiales" not in prod_actual:
        prod_actual["etiquetas_especiales"] = []
    return prod_actual

if __name__ == '__main__':
    print("--- Jerarquía de Categorías (con Slugs) ---")
    jerarquia = obtener_categorias_jerarquia()
    for cat_p in jerarquia:
        print(f"ID Principal: {cat_p['id_cat_principal']}, Nombre: {cat_p['nombre_cat_principal']}, Slug: {cat_p['slug_cat_principal']}")
        for sub_c in cat_p['subcategorias']:
            print(f"  ID Sub: {sub_c['id_subcategoria']}, Nombre: {sub_c['nombre_subcategoria']}, Slug: {sub_c['slug_subcategoria']}")

    print("\n--- Nombres de Categoría ---")
    print(f"cocina: {obtener_nombre_categoria(id_cat_principal_slug='cocina')}")
    print(f"cocina/refrigeradores: {obtener_nombre_categoria(id_cat_principal_slug='cocina', id_sub_cat_slug='refrigeradores')}")
    print(f"sala/televisores: {obtener_nombre_categoria(id_cat_principal_slug='sala', id_sub_cat_slug='televisores')}")
    print(f"inexistente: {obtener_nombre_categoria(id_cat_principal_slug='inexistente')}")

    print("\n--- Productos (Todos) ---")
    todos_los_productos = obtener_productos_con_detalles() # Debería mostrar solo regulares si no se especifica categoría
    for p in todos_los_productos:
        print(f"{p['nombre']} (Regular: {p.get('es_item_catalogo_regular', 'No Definido')}), Precio: ${p['precio']}, Inicial: ${p['inicial']}")

    print("\n--- Productos de Cocina (Solo Regulares) ---")
    productos_cocina = obtener_productos_con_detalles(id_cat_principal_slug="cocina")
    for p in productos_cocina:
        print(f"{p['nombre']}, Precio: ${p['precio']}, Regular: {p.get('es_item_catalogo_regular', 'No Definido')}")

    print("\n--- Sugerencias Outlet para Cocina > Estufas ---")
    sugerencias_estufas_outlet = obtener_sugerencias_especiales_para_categoria(id_cat_principal_actual="cocina", id_subcategoria_actual="estufas", etiqueta_sugerencia="outlet")
    for p in sugerencias_estufas_outlet:
        print(f"Sugerencia Outlet: {p['nombre']}, Precio: ${p['precio']}, Regular: {p.get('es_item_catalogo_regular')}")

    print("\n--- Productos de Outlet (Todos los de Outlet) ---")
    productos_outlet_todos = obtener_productos_por_etiqueta_especial("outlet")
    for p in productos_outlet_todos:
        print(f"Outlet: {p['nombre']}, Precio: ${p['precio']}, Regular: {p.get('es_item_catalogo_regular')}")

    print("\n--- Producto por ID (101) ---")
    prod101_enriquecido = obtener_producto_enriquecido_por_id(101)
    if prod101_enriquecido:
        print(f"{prod101_enriquecido['nombre']} - Regular: {prod101_enriquecido.get('es_item_catalogo_regular')}")

    print("\n--- Producto por ID (109 - Outlet Estufa) ---")
    prod109_enriquecido = obtener_producto_enriquecido_por_id(109)
    if prod109_enriquecido:
        print(f"{prod109_enriquecido['nombre']} - Regular: {prod109_enriquecido.get('es_item_catalogo_regular')}")

    print("\n--- Producto por ID (104 - Outlet Microondas) ---")
    prod104_enriquecido = obtener_producto_enriquecido_por_id(104)
    if prod104_enriquecido:
        print(f"{prod104_enriquecido['nombre']} - Regular: {prod104_enriquecido.get('es_item_catalogo_regular')}")
        print(f"  Etiquetas: {prod104_enriquecido.get('etiquetas_especiales')}")

    print("\n--- Sugerencias Outlet para Cocina > Microondas ---")
    sugerencias_micro_outlet = obtener_sugerencias_especiales_para_categoria(id_cat_principal_actual="cocina", id_subcategoria_actual="microondas", etiqueta_sugerencia="outlet")
    for p in sugerencias_micro_outlet:
        print(f"Sugerencia Outlet: {p['nombre']}, Precio: ${p['precio']}, Regular: {p.get('es_item_catalogo_regular')}")
