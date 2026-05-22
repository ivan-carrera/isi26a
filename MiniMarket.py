"""
=============================================================
  TPS QuickShop v3.0 — Sistema de Punto de Venta
  MiniMarket QuickShop | Materia: Sistemas de Información
  Python 3 + Tkinter + CSV

  Características:
    - 200 productos en 9 categorías.
    - Catálogo (productos.csv) separado del inventario (inventario.csv).
    - 100 clientes pre‑registrados + CRUD de clientes.
    - Facturas con datos del cliente y vigencia de 1 año.
    - Historial de un año de transacciones (generado automáticamente).
    - Reportes: promedio por N facturas, top productos, ventas por método.
    - Selección de cliente al momento de cobrar (buscar / registrar / consumidor final).
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv, os, random
from datetime import datetime, timedelta

# ══════════════════════════════════════════
#  ARCHIVOS CSV
# ══════════════════════════════════════════
ARCH_PRODUCTOS     = "productos.csv"      # catálogo de productos (sin stock)
ARCH_INVENTARIO    = "inventario.csv"     # solo stock por código
ARCH_USUARIOS      = "usuarios.csv"       # clientes registrados
ARCH_TRANSACCIONES = "transacciones.csv"  # cabecera de cada venta
ARCH_DETALLES      = "detalles_venta.csv" # líneas de cada venta

# ══════════════════════════════════════════
#  TEMA VISUAL
# ══════════════════════════════════════════
BG_OSCURO = "#0d1117"; BG_PANEL = "#161b27"; BG_CARD = "#1e2536"
AZUL = "#4f8ef7";  AZUL_OSC = "#3a6ed8"
VERDE = "#22c55e"; VERDE_OSC = "#16a34a"
ROJO = "#ef4444";  AMARILLO = "#f59e0b"
BLANCO = "#e2e8f0"; GRIS = "#64748b"; BORDE = "#2a3350"; MORADO = "#a855f7"
F_TITULO = ("Consolas",12,"bold")
F_NORMAL = ("Consolas",10)
F_CHICA  = ("Consolas",9)

# ══════════════════════════════════════════
#  CATÁLOGO BASE — 200 PRODUCTOS (sin stock)
# ══════════════════════════════════════════
CATALOGO_BASE = [
    # BEBIDAS (30)
    {"codigo":"B001","nombre":"Agua mineral 500ml",         "precio":0.50,"categoria":"Bebidas","descripcion":"Agua sin gas botella pequeña"},
    {"codigo":"B002","nombre":"Agua con gas 500ml",          "precio":0.65,"categoria":"Bebidas","descripcion":"Agua carbonatada botella pequeña"},
    {"codigo":"B003","nombre":"Agua mineral 1.5L",           "precio":0.90,"categoria":"Bebidas","descripcion":"Agua sin gas botella grande"},
    {"codigo":"B004","nombre":"Coca-Cola 600ml",             "precio":1.25,"categoria":"Bebidas","descripcion":"Gaseosa cola botella mediana"},
    {"codigo":"B005","nombre":"Coca-Cola 1.5L",              "precio":1.80,"categoria":"Bebidas","descripcion":"Gaseosa cola botella familiar"},
    {"codigo":"B006","nombre":"Sprite 600ml",                "precio":1.20,"categoria":"Bebidas","descripcion":"Gaseosa lima-limón botella"},
    {"codigo":"B007","nombre":"Fanta naranja 600ml",         "precio":1.20,"categoria":"Bebidas","descripcion":"Gaseosa sabor naranja"},
    {"codigo":"B008","nombre":"Pepsi 600ml",                 "precio":1.15,"categoria":"Bebidas","descripcion":"Gaseosa cola botella"},
    {"codigo":"B009","nombre":"Big Cola 1.5L",               "precio":1.00,"categoria":"Bebidas","descripcion":"Gaseosa cola economica"},
    {"codigo":"B010","nombre":"Jugo Natura naranja 1L",      "precio":1.50,"categoria":"Bebidas","descripcion":"Jugo natural de naranja"},
    {"codigo":"B011","nombre":"Jugo Natura mango 1L",        "precio":1.50,"categoria":"Bebidas","descripcion":"Jugo natural de mango"},
    {"codigo":"B012","nombre":"Jugo Del Valle 500ml",        "precio":1.10,"categoria":"Bebidas","descripcion":"Nectar de naranja"},
    {"codigo":"B013","nombre":"Jugo de mango 500ml",         "precio":1.10,"categoria":"Bebidas","descripcion":"Nectar de mango"},
    {"codigo":"B014","nombre":"Energizante Monster 473ml",   "precio":2.50,"categoria":"Bebidas","descripcion":"Bebida energizante lata"},
    {"codigo":"B015","nombre":"Energizante Red Bull 250ml",  "precio":2.80,"categoria":"Bebidas","descripcion":"Bebida energizante lata pequeña"},
    {"codigo":"B016","nombre":"Energizante Volt 250ml",      "precio":1.50,"categoria":"Bebidas","descripcion":"Bebida energizante economica"},
    {"codigo":"B017","nombre":"Gatorade naranja 600ml",      "precio":1.30,"categoria":"Bebidas","descripcion":"Bebida isotonica naranja"},
    {"codigo":"B018","nombre":"Gatorade limon 600ml",        "precio":1.30,"categoria":"Bebidas","descripcion":"Bebida isotonica limon"},
    {"codigo":"B019","nombre":"Powerade uva 600ml",          "precio":1.25,"categoria":"Bebidas","descripcion":"Bebida isotonica uva"},
    {"codigo":"B020","nombre":"Te helado limon 500ml",       "precio":1.00,"categoria":"Bebidas","descripcion":"Te frio sabor limon"},
    {"codigo":"B021","nombre":"Te helado durazno 500ml",     "precio":1.00,"categoria":"Bebidas","descripcion":"Te frio sabor durazno"},
    {"codigo":"B022","nombre":"Leche entera 1L",             "precio":0.95,"categoria":"Bebidas","descripcion":"Leche entera pasteurizada"},
    {"codigo":"B023","nombre":"Leche semidescremada 1L",     "precio":1.05,"categoria":"Bebidas","descripcion":"Leche semidescremada"},
    {"codigo":"B024","nombre":"Leche deslactosada 1L",       "precio":1.20,"categoria":"Bebidas","descripcion":"Leche sin lactosa"},
    {"codigo":"B025","nombre":"Leche de chocolate 1L",       "precio":1.30,"categoria":"Bebidas","descripcion":"Leche sabor chocolate"},
    {"codigo":"B026","nombre":"Cocoa en polvo 400g",         "precio":2.50,"categoria":"Bebidas","descripcion":"Cocoa para bebida caliente"},
    {"codigo":"B027","nombre":"Cafe instantaneo 100g",       "precio":2.20,"categoria":"Bebidas","descripcion":"Cafe soluble frasco"},
    {"codigo":"B028","nombre":"Te en sobre x20",             "precio":1.80,"categoria":"Bebidas","descripcion":"Sobres de te variado"},
    {"codigo":"B029","nombre":"Limonada 500ml",              "precio":0.90,"categoria":"Bebidas","descripcion":"Limonada natural embotellada"},
    {"codigo":"B030","nombre":"Jugo de guayaba 500ml",       "precio":1.10,"categoria":"Bebidas","descripcion":"Nectar de guayaba"},
    # SNACKS (25)
    {"codigo":"S001","nombre":"Papas Lays 90g",              "precio":1.10,"categoria":"Snacks","descripcion":"Papas fritas clasicas"},
    {"codigo":"S002","nombre":"Papas Ruffles 90g",           "precio":1.10,"categoria":"Snacks","descripcion":"Papas fritas con ondas"},
    {"codigo":"S003","nombre":"Papas Pringles 124g",         "precio":2.50,"categoria":"Snacks","descripcion":"Papas fritas en tubo"},
    {"codigo":"S004","nombre":"Doritos nachos 90g",          "precio":1.20,"categoria":"Snacks","descripcion":"Tortillas de maiz con queso"},
    {"codigo":"S005","nombre":"Cheetos 80g",                 "precio":1.00,"categoria":"Snacks","descripcion":"Botanas de maiz con queso"},
    {"codigo":"S006","nombre":"Chifles 80g",                 "precio":0.75,"categoria":"Snacks","descripcion":"Platano verde frito"},
    {"codigo":"S007","nombre":"Maiz tostado 100g",           "precio":0.60,"categoria":"Snacks","descripcion":"Maiz tostado con sal"},
    {"codigo":"S008","nombre":"Canguil dulce 50g",           "precio":0.50,"categoria":"Snacks","descripcion":"Palomitas sabor dulce"},
    {"codigo":"S009","nombre":"Galletas Oreo 120g",          "precio":1.50,"categoria":"Snacks","descripcion":"Galletas de chocolate con crema"},
    {"codigo":"S010","nombre":"Galletas Maria 200g",         "precio":1.20,"categoria":"Snacks","descripcion":"Galletas de vainilla clasicas"},
    {"codigo":"S011","nombre":"Galletas Ritz 100g",          "precio":1.30,"categoria":"Snacks","descripcion":"Galletas saladas crujientes"},
    {"codigo":"S012","nombre":"Galletas de coco 100g",       "precio":0.90,"categoria":"Snacks","descripcion":"Galletas sabor coco"},
    {"codigo":"S013","nombre":"Mani con chocolate 50g",      "precio":0.80,"categoria":"Snacks","descripcion":"Mani cubierto de chocolate"},
    {"codigo":"S014","nombre":"Mani salado 100g",            "precio":0.70,"categoria":"Snacks","descripcion":"Mani tostado con sal"},
    {"codigo":"S015","nombre":"Barra de cereal 35g",         "precio":0.60,"categoria":"Snacks","descripcion":"Barra nutritiva de cereal"},
    {"codigo":"S016","nombre":"Chocolatin 40g",              "precio":0.70,"categoria":"Snacks","descripcion":"Chocolate con leche tableta"},
    {"codigo":"S017","nombre":"Kit Kat 42g",                 "precio":1.20,"categoria":"Snacks","descripcion":"Chocolate wafer con leche"},
    {"codigo":"S018","nombre":"Snickers 45g",                "precio":1.30,"categoria":"Snacks","descripcion":"Chocolate con mani y caramelo"},
    {"codigo":"S019","nombre":"M&Ms 45g",                    "precio":1.50,"categoria":"Snacks","descripcion":"Confites de chocolate de colores"},
    {"codigo":"S020","nombre":"Gomas de fresa 100g",         "precio":0.80,"categoria":"Snacks","descripcion":"Gomitas sabor fresa"},
    {"codigo":"S021","nombre":"Chicle Trident x12",          "precio":0.60,"categoria":"Snacks","descripcion":"Chicle sin azucar menta"},
    {"codigo":"S022","nombre":"Caramelos surtidos 100g",     "precio":0.75,"categoria":"Snacks","descripcion":"Caramelos duros variados"},
    {"codigo":"S023","nombre":"Paleta de chocolate",         "precio":0.50,"categoria":"Snacks","descripcion":"Paleta sabor chocolate"},
    {"codigo":"S024","nombre":"Semillas girasol 80g",        "precio":0.65,"categoria":"Snacks","descripcion":"Semillas tostadas con sal"},
    {"codigo":"S025","nombre":"Granola 200g",                "precio":1.80,"categoria":"Snacks","descripcion":"Mezcla de cereales con miel"},
    # LACTEOS (20)
    {"codigo":"L001","nombre":"Yogur natural 200g",          "precio":0.75,"categoria":"Lacteos","descripcion":"Yogur sin sabor con cultivos"},
    {"codigo":"L002","nombre":"Yogur fresa 200g",            "precio":0.80,"categoria":"Lacteos","descripcion":"Yogur sabor fresa"},
    {"codigo":"L003","nombre":"Yogur mora 200g",             "precio":0.80,"categoria":"Lacteos","descripcion":"Yogur sabor mora"},
    {"codigo":"L004","nombre":"Yogur durazno 200g",          "precio":0.80,"categoria":"Lacteos","descripcion":"Yogur sabor durazno"},
    {"codigo":"L005","nombre":"Yogur griego 150g",           "precio":1.20,"categoria":"Lacteos","descripcion":"Yogur griego sin azucar"},
    {"codigo":"L006","nombre":"Queso fresco 250g",           "precio":1.80,"categoria":"Lacteos","descripcion":"Queso fresco ecuatoriano"},
    {"codigo":"L007","nombre":"Queso mozzarella 200g",       "precio":2.20,"categoria":"Lacteos","descripcion":"Queso mozzarella para pizza"},
    {"codigo":"L008","nombre":"Queso cheddar 150g",          "precio":2.50,"categoria":"Lacteos","descripcion":"Queso cheddar en lonchas"},
    {"codigo":"L009","nombre":"Queso parmesano rallado 80g", "precio":2.00,"categoria":"Lacteos","descripcion":"Parmesano rallado en sobre"},
    {"codigo":"L010","nombre":"Mantequilla 100g",            "precio":1.50,"categoria":"Lacteos","descripcion":"Mantequilla sin sal"},
    {"codigo":"L011","nombre":"Margarina 250g",              "precio":1.20,"categoria":"Lacteos","descripcion":"Margarina vegetal para untar"},
    {"codigo":"L012","nombre":"Huevos x6",                   "precio":1.30,"categoria":"Lacteos","descripcion":"Media docena de huevos"},
    {"codigo":"L013","nombre":"Huevos x12",                  "precio":2.50,"categoria":"Lacteos","descripcion":"Docena de huevos"},
    {"codigo":"L014","nombre":"Huevos x30",                  "precio":6.00,"categoria":"Lacteos","descripcion":"Bandeja de huevos"},
    {"codigo":"L015","nombre":"Crema de leche 250ml",        "precio":1.20,"categoria":"Lacteos","descripcion":"Crema para cocinar"},
    {"codigo":"L016","nombre":"Natilla 500ml",               "precio":1.50,"categoria":"Lacteos","descripcion":"Natilla para postres"},
    {"codigo":"L017","nombre":"Leche condensada 397g",       "precio":2.00,"categoria":"Lacteos","descripcion":"Leche condensada azucarada"},
    {"codigo":"L018","nombre":"Leche evaporada 400ml",       "precio":1.80,"categoria":"Lacteos","descripcion":"Leche evaporada sin azucar"},
    {"codigo":"L019","nombre":"Provolone 200g",              "precio":2.80,"categoria":"Lacteos","descripcion":"Queso provolone importado"},
    {"codigo":"L020","nombre":"Ricotta 250g",                "precio":2.20,"categoria":"Lacteos","descripcion":"Queso ricotta para reposteria"},
    # PANADERIA (15)
    {"codigo":"P001","nombre":"Pan de molde integral",       "precio":1.80,"categoria":"Panaderia","descripcion":"Pan integral en rebanadas"},
    {"codigo":"P002","nombre":"Pan de molde blanco",         "precio":1.50,"categoria":"Panaderia","descripcion":"Pan blanco en rebanadas"},
    {"codigo":"P003","nombre":"Pan de molde de ajo",         "precio":2.00,"categoria":"Panaderia","descripcion":"Pan de ajo en rebanadas"},
    {"codigo":"P004","nombre":"Tostadas x20",                "precio":1.30,"categoria":"Panaderia","descripcion":"Tostadas crujientes empacadas"},
    {"codigo":"P005","nombre":"Pan pita x6",                 "precio":1.80,"categoria":"Panaderia","descripcion":"Pan pita para sandwich"},
    {"codigo":"P006","nombre":"Croissant x4",                "precio":2.00,"categoria":"Panaderia","descripcion":"Medialunas de mantequilla"},
    {"codigo":"P007","nombre":"Bagel x4",                    "precio":2.20,"categoria":"Panaderia","descripcion":"Pan bagel para sandwich"},
    {"codigo":"P008","nombre":"Tortillas de harina x8",      "precio":1.50,"categoria":"Panaderia","descripcion":"Tortillas para burritos"},
    {"codigo":"P009","nombre":"Bizcocho 200g",               "precio":1.80,"categoria":"Panaderia","descripcion":"Bizcocho azucarado empacado"},
    {"codigo":"P010","nombre":"Donuts x4",                   "precio":2.00,"categoria":"Panaderia","descripcion":"Rosquillas con glaseado"},
    {"codigo":"P011","nombre":"Muffin de chocolate",         "precio":0.80,"categoria":"Panaderia","descripcion":"Muffin individual de chocolate"},
    {"codigo":"P012","nombre":"Muffin de vainilla",          "precio":0.80,"categoria":"Panaderia","descripcion":"Muffin individual de vainilla"},
    {"codigo":"P013","nombre":"Pan de yuca 6 unid",          "precio":1.50,"categoria":"Panaderia","descripcion":"Pan de queso y yuca"},
    {"codigo":"P014","nombre":"Churros empacados 100g",      "precio":1.20,"categoria":"Panaderia","descripcion":"Churros dulces empacados"},
    {"codigo":"P015","nombre":"Wafer de vainilla 150g",      "precio":1.10,"categoria":"Panaderia","descripcion":"Obleas rellenas de vainilla"},
    # ABARROTES (35)
    {"codigo":"A001","nombre":"Arroz 1kg",                   "precio":0.90,"categoria":"Abarrotes","descripcion":"Arroz blanco de primera"},
    {"codigo":"A002","nombre":"Arroz 2kg",                   "precio":1.75,"categoria":"Abarrotes","descripcion":"Arroz blanco bolsa mediana"},
    {"codigo":"A003","nombre":"Arroz 5kg",                   "precio":4.20,"categoria":"Abarrotes","descripcion":"Arroz blanco bolsa grande"},
    {"codigo":"A004","nombre":"Aceite vegetal 1L",           "precio":2.20,"categoria":"Abarrotes","descripcion":"Aceite para cocinar"},
    {"codigo":"A005","nombre":"Aceite de oliva 500ml",       "precio":5.50,"categoria":"Abarrotes","descripcion":"Aceite de oliva extra virgen"},
    {"codigo":"A006","nombre":"Aceite de girasol 1L",        "precio":2.00,"categoria":"Abarrotes","descripcion":"Aceite de girasol refinado"},
    {"codigo":"A007","nombre":"Azucar blanca 1kg",           "precio":0.75,"categoria":"Abarrotes","descripcion":"Azucar refinada blanca"},
    {"codigo":"A008","nombre":"Azucar morena 1kg",           "precio":0.90,"categoria":"Abarrotes","descripcion":"Azucar morena sin refinar"},
    {"codigo":"A009","nombre":"Panela 1kg",                  "precio":0.70,"categoria":"Abarrotes","descripcion":"Panela de cana de azucar"},
    {"codigo":"A010","nombre":"Sal 500g",                    "precio":0.35,"categoria":"Abarrotes","descripcion":"Sal yodada fina"},
    {"codigo":"A011","nombre":"Atun en lata 180g",           "precio":1.40,"categoria":"Abarrotes","descripcion":"Atun en aceite vegetal"},
    {"codigo":"A012","nombre":"Sardinas en lata 125g",       "precio":1.10,"categoria":"Abarrotes","descripcion":"Sardinas en salsa de tomate"},
    {"codigo":"A013","nombre":"Maiz en lata 400g",           "precio":1.20,"categoria":"Abarrotes","descripcion":"Maiz dulce en conserva"},
    {"codigo":"A014","nombre":"Frijoles en lata 400g",       "precio":1.10,"categoria":"Abarrotes","descripcion":"Frijoles negros en conserva"},
    {"codigo":"A015","nombre":"Tomate en lata 400g",         "precio":1.00,"categoria":"Abarrotes","descripcion":"Tomate triturado en conserva"},
    {"codigo":"A016","nombre":"Pasta espagueti 500g",        "precio":0.85,"categoria":"Abarrotes","descripcion":"Espagueti de trigo durum"},
    {"codigo":"A017","nombre":"Pasta coditos 500g",          "precio":0.85,"categoria":"Abarrotes","descripcion":"Macarrones de codo"},
    {"codigo":"A018","nombre":"Pasta fideos 500g",           "precio":0.80,"categoria":"Abarrotes","descripcion":"Fideos finos para sopa"},
    {"codigo":"A019","nombre":"Salsa de tomate 500g",        "precio":1.30,"categoria":"Abarrotes","descripcion":"Salsa de tomate ketchup"},
    {"codigo":"A020","nombre":"Mayonesa 200g",               "precio":1.00,"categoria":"Abarrotes","descripcion":"Mayonesa clasica sobre"},
    {"codigo":"A021","nombre":"Mayonesa 400g",               "precio":1.80,"categoria":"Abarrotes","descripcion":"Mayonesa clasica frasco"},
    {"codigo":"A022","nombre":"Mostaza 200g",                "precio":0.90,"categoria":"Abarrotes","descripcion":"Mostaza amarilla clasica"},
    {"codigo":"A023","nombre":"Salsa de soya 150ml",         "precio":1.20,"categoria":"Abarrotes","descripcion":"Salsa soya oscura"},
    {"codigo":"A024","nombre":"Vinagre 500ml",               "precio":0.80,"categoria":"Abarrotes","descripcion":"Vinagre blanco de mesa"},
    {"codigo":"A025","nombre":"Comino molido 50g",           "precio":0.60,"categoria":"Abarrotes","descripcion":"Comino en polvo"},
    {"codigo":"A026","nombre":"Oregano 20g",                 "precio":0.50,"categoria":"Abarrotes","descripcion":"Oregano seco molido"},
    {"codigo":"A027","nombre":"Ajo en polvo 50g",            "precio":0.70,"categoria":"Abarrotes","descripcion":"Ajo deshidratado en polvo"},
    {"codigo":"A028","nombre":"Pimienta negra 30g",          "precio":0.80,"categoria":"Abarrotes","descripcion":"Pimienta negra molida"},
    {"codigo":"A029","nombre":"Harina de trigo 1kg",         "precio":0.90,"categoria":"Abarrotes","descripcion":"Harina blanca para reposteria"},
    {"codigo":"A030","nombre":"Avena en hojuelas 500g",      "precio":1.20,"categoria":"Abarrotes","descripcion":"Avena entera para desayuno"},
    {"codigo":"A031","nombre":"Lentejas 500g",               "precio":1.10,"categoria":"Abarrotes","descripcion":"Lentejas secas para cocinar"},
    {"codigo":"A032","nombre":"Arvejas 500g",                "precio":1.00,"categoria":"Abarrotes","descripcion":"Arvejas secas partidas"},
    {"codigo":"A033","nombre":"Miel de abeja 350g",          "precio":3.50,"categoria":"Abarrotes","descripcion":"Miel pura de abeja"},
    {"codigo":"A034","nombre":"Mermelada fresa 300g",        "precio":1.80,"categoria":"Abarrotes","descripcion":"Mermelada de fresa"},
    {"codigo":"A035","nombre":"Mermelada mora 300g",         "precio":1.80,"categoria":"Abarrotes","descripcion":"Mermelada de mora"},
    # LIMPIEZA (25)
    {"codigo":"C001","nombre":"Jabon de manos 250ml",        "precio":1.20,"categoria":"Limpieza","descripcion":"Jabon liquido antibacterial"},
    {"codigo":"C002","nombre":"Jabon de bano x3",            "precio":1.50,"categoria":"Limpieza","descripcion":"Pastillas de jabon corporal"},
    {"codigo":"C003","nombre":"Jabon en barra 150g",         "precio":0.80,"categoria":"Limpieza","descripcion":"Jabon de lavanderia"},
    {"codigo":"C004","nombre":"Shampoo 400ml",               "precio":3.50,"categoria":"Limpieza","descripcion":"Shampoo cabello normal"},
    {"codigo":"C005","nombre":"Shampoo anticaspa 400ml",     "precio":3.80,"categoria":"Limpieza","descripcion":"Shampoo control caspa"},
    {"codigo":"C006","nombre":"Acondicionador 400ml",        "precio":3.50,"categoria":"Limpieza","descripcion":"Acondicionador para cabello"},
    {"codigo":"C007","nombre":"Papel higienico x4",          "precio":1.80,"categoria":"Limpieza","descripcion":"Rollo doble hoja x4"},
    {"codigo":"C008","nombre":"Papel higienico x12",         "precio":4.80,"categoria":"Limpieza","descripcion":"Rollo doble hoja x12"},
    {"codigo":"C009","nombre":"Papel higienico x24",         "precio":9.00,"categoria":"Limpieza","descripcion":"Rollo doble hoja x24"},
    {"codigo":"C010","nombre":"Toallas de cocina x2",        "precio":2.00,"categoria":"Limpieza","descripcion":"Papel absorvente cocina"},
    {"codigo":"C011","nombre":"Servilletas x100",            "precio":1.20,"categoria":"Limpieza","descripcion":"Servilletas de papel"},
    {"codigo":"C012","nombre":"Detergente polvo 500g",       "precio":1.60,"categoria":"Limpieza","descripcion":"Detergente ropa en polvo"},
    {"codigo":"C013","nombre":"Detergente polvo 1kg",        "precio":2.80,"categoria":"Limpieza","descripcion":"Detergente ropa familiar"},
    {"codigo":"C014","nombre":"Detergente liquido 500ml",    "precio":2.00,"categoria":"Limpieza","descripcion":"Detergente ropa liquido"},
    {"codigo":"C015","nombre":"Suavizante ropa 500ml",       "precio":2.00,"categoria":"Limpieza","descripcion":"Suavizante concentrado"},
    {"codigo":"C016","nombre":"Lavavajillas 500ml",          "precio":1.50,"categoria":"Limpieza","descripcion":"Liquido lava platos"},
    {"codigo":"C017","nombre":"Lavavajillas 1L",             "precio":2.50,"categoria":"Limpieza","descripcion":"Liquido lava platos grande"},
    {"codigo":"C018","nombre":"Cloro 1L",                    "precio":1.20,"categoria":"Limpieza","descripcion":"Blanqueador a base de cloro"},
    {"codigo":"C019","nombre":"Desinfectante piso 1L",       "precio":2.00,"categoria":"Limpieza","descripcion":"Desinfectante fragancia lavanda"},
    {"codigo":"C020","nombre":"Limpiador multiusos 500ml",   "precio":1.80,"categoria":"Limpieza","descripcion":"Limpiador para superficies"},
    {"codigo":"C021","nombre":"Esponjas x3",                 "precio":1.00,"categoria":"Limpieza","descripcion":"Esponjas de cocina doble uso"},
    {"codigo":"C022","nombre":"Guantes latex S",             "precio":1.20,"categoria":"Limpieza","descripcion":"Guantes de latex talla S"},
    {"codigo":"C023","nombre":"Guantes latex M",             "precio":1.20,"categoria":"Limpieza","descripcion":"Guantes de latex talla M"},
    {"codigo":"C024","nombre":"Bolsas de basura x10",        "precio":1.50,"categoria":"Limpieza","descripcion":"Bolsas negras 50L"},
    {"codigo":"C025","nombre":"Repelente mosquitos 100ml",   "precio":2.50,"categoria":"Limpieza","descripcion":"Repelente de insectos spray"},
    # PERSONAL (25)
    {"codigo":"G001","nombre":"Desodorante roll-on 50ml",    "precio":2.80,"categoria":"Personal","descripcion":"Desodorante sin alcohol"},
    {"codigo":"G002","nombre":"Desodorante spray 150ml",     "precio":3.00,"categoria":"Personal","descripcion":"Desodorante aerosol"},
    {"codigo":"G003","nombre":"Pasta dental 100ml",          "precio":1.50,"categoria":"Personal","descripcion":"Pasta dental con fluor"},
    {"codigo":"G004","nombre":"Pasta dental blanqueadora",   "precio":1.80,"categoria":"Personal","descripcion":"Pasta dental blanqueadora"},
    {"codigo":"G005","nombre":"Cepillo dental suave",        "precio":1.20,"categoria":"Personal","descripcion":"Cepillo de cerdas suaves"},
    {"codigo":"G006","nombre":"Cepillo dental medio",        "precio":1.20,"categoria":"Personal","descripcion":"Cepillo de cerdas medias"},
    {"codigo":"G007","nombre":"Enjuague bucal 250ml",        "precio":2.50,"categoria":"Personal","descripcion":"Enjuague bucal menta"},
    {"codigo":"G008","nombre":"Hilo dental 50m",             "precio":1.00,"categoria":"Personal","descripcion":"Hilo dental encerado"},
    {"codigo":"G009","nombre":"Afeitadora x2",               "precio":2.50,"categoria":"Personal","descripcion":"Afeitadora desechable doble hoja"},
    {"codigo":"G010","nombre":"Crema de afeitar 100ml",      "precio":1.80,"categoria":"Personal","descripcion":"Espuma para afeitar"},
    {"codigo":"G011","nombre":"Algodon 100g",                "precio":1.00,"categoria":"Personal","descripcion":"Algodon absorbente bolsa"},
    {"codigo":"G012","nombre":"Curitas x20",                 "precio":1.20,"categoria":"Personal","descripcion":"Curitas adhesivas surtidas"},
    {"codigo":"G013","nombre":"Alcohol 70% 250ml",           "precio":1.50,"categoria":"Personal","descripcion":"Alcohol isopropilico"},
    {"codigo":"G014","nombre":"Agua oxigenada 250ml",        "precio":0.90,"categoria":"Personal","descripcion":"Agua oxigenada 10 volumenes"},
    {"codigo":"G015","nombre":"Protector solar FPS50",       "precio":4.50,"categoria":"Personal","descripcion":"Protector solar 100ml"},
    {"codigo":"G016","nombre":"Crema humectante 200ml",      "precio":3.00,"categoria":"Personal","descripcion":"Crema hidratante corporal"},
    {"codigo":"G017","nombre":"Preservativos x3",            "precio":2.00,"categoria":"Personal","descripcion":"Preservativos lubricados"},
    {"codigo":"G018","nombre":"Toallas higienicas x8",       "precio":2.50,"categoria":"Personal","descripcion":"Toallas femeninas con alas"},
    {"codigo":"G019","nombre":"Tampones x8",                 "precio":2.80,"categoria":"Personal","descripcion":"Tampones de insercion"},
    {"codigo":"G020","nombre":"Pañal bebe talla M x10",      "precio":5.00,"categoria":"Personal","descripcion":"Pañales desechables talla M"},
    {"codigo":"G021","nombre":"Toallas humedas x20",         "precio":1.80,"categoria":"Personal","descripcion":"Toallitas humedas"},
    {"codigo":"G022","nombre":"Gel antibacterial 60ml",      "precio":1.20,"categoria":"Personal","descripcion":"Gel de manos sin agua"},
    {"codigo":"G023","nombre":"Peinilla",                    "precio":0.80,"categoria":"Personal","descripcion":"Peinilla de plastico"},
    {"codigo":"G024","nombre":"Cotonetes x50",               "precio":0.90,"categoria":"Personal","descripcion":"Hisopos de algodon"},
    {"codigo":"G025","nombre":"Maquinilla depiladora",       "precio":1.50,"categoria":"Personal","descripcion":"Maquinilla desechable mujer"},
    # FRUTAS Y VERDURAS (15)
    {"codigo":"FV01","nombre":"Papas 1kg",                   "precio":0.80,"categoria":"Frutas/Verduras","descripcion":"Papas frescas para cocinar"},
    {"codigo":"FV02","nombre":"Cebolla 1kg",                 "precio":0.60,"categoria":"Frutas/Verduras","descripcion":"Cebolla paiteña roja"},
    {"codigo":"FV03","nombre":"Tomate riñon 1kg",            "precio":0.70,"categoria":"Frutas/Verduras","descripcion":"Tomate riñon fresco"},
    {"codigo":"FV04","nombre":"Pimiento verde 500g",         "precio":0.60,"categoria":"Frutas/Verduras","descripcion":"Pimientos verdes frescos"},
    {"codigo":"FV05","nombre":"Manzana roja x4",             "precio":1.20,"categoria":"Frutas/Verduras","descripcion":"Manzanas rojas frescas"},
    {"codigo":"FV06","nombre":"Naranja x6",                  "precio":1.00,"categoria":"Frutas/Verduras","descripcion":"Naranjas jugosas para jugo"},
    {"codigo":"FV07","nombre":"Banano x6",                   "precio":0.60,"categoria":"Frutas/Verduras","descripcion":"Bananos maduros frescos"},
    {"codigo":"FV08","nombre":"Pera x4",                     "precio":1.30,"categoria":"Frutas/Verduras","descripcion":"Peras verdes frescas"},
    {"codigo":"FV09","nombre":"Uva roja 500g",               "precio":2.00,"categoria":"Frutas/Verduras","descripcion":"Uvas rojas sin semilla"},
    {"codigo":"FV10","nombre":"Limon x6",                    "precio":0.50,"categoria":"Frutas/Verduras","descripcion":"Limones frescos para jugo"},
    {"codigo":"FV11","nombre":"Mandarina x6",                "precio":0.90,"categoria":"Frutas/Verduras","descripcion":"Mandarinas dulces frescas"},
    {"codigo":"FV12","nombre":"Maracuya 500g",               "precio":1.00,"categoria":"Frutas/Verduras","descripcion":"Maracuyas frescos para jugo"},
    {"codigo":"FV13","nombre":"Frutilla 250g",               "precio":1.20,"categoria":"Frutas/Verduras","descripcion":"Fresas frescas"},
    {"codigo":"FV14","nombre":"Aguacate x2",                 "precio":1.50,"categoria":"Frutas/Verduras","descripcion":"Aguacates medianos maduros"},
    {"codigo":"FV15","nombre":"Brocoli 500g",                "precio":0.80,"categoria":"Frutas/Verduras","descripcion":"Brocoli fresco"},
    # CARNES Y EMBUTIDOS (10)
    {"codigo":"CM01","nombre":"Salchicha 250g",              "precio":1.80,"categoria":"Carnes","descripcion":"Salchicha tipo viena"},
    {"codigo":"CM02","nombre":"Mortadela 200g",              "precio":1.50,"categoria":"Carnes","descripcion":"Mortadela clasica en lonjas"},
    {"codigo":"CM03","nombre":"Jamon de pierna 200g",        "precio":2.00,"categoria":"Carnes","descripcion":"Jamon cocido en lonjas"},
    {"codigo":"CM04","nombre":"Chorizo 250g",                "precio":2.50,"categoria":"Carnes","descripcion":"Chorizo ahumado para asar"},
    {"codigo":"CM05","nombre":"Salami 150g",                 "precio":2.20,"categoria":"Carnes","descripcion":"Salami tipo italiano"},
    {"codigo":"CM06","nombre":"Pernil ahumado 200g",         "precio":2.80,"categoria":"Carnes","descripcion":"Pernil de cerdo ahumado"},
    {"codigo":"CM07","nombre":"Pollo molido 500g",           "precio":2.50,"categoria":"Carnes","descripcion":"Carne de pollo molida"},
    {"codigo":"CM08","nombre":"Carne molida de res 500g",    "precio":3.50,"categoria":"Carnes","descripcion":"Carne de res molida"},
    {"codigo":"CM09","nombre":"Nuggets de pollo 300g",       "precio":3.00,"categoria":"Carnes","descripcion":"Nuggets precocidos de pollo"},
    {"codigo":"CM10","nombre":"Jamon serrano 100g",          "precio":3.50,"categoria":"Carnes","descripcion":"Jamon serrano importado"},
]

# Stock inicial — SEPARADO del catálogo
STOCK_INICIAL = {
    "B001":150,"B002":80,"B003":100,"B004":100,"B005":70,"B006":90,"B007":85,
    "B008":60,"B009":55,"B010":40,"B011":40,"B012":65,"B013":75,"B014":80,
    "B015":50,"B016":60,"B017":30,"B018":65,"B019":60,"B020":50,"B021":75,
    "B022":80,"B023":60,"B024":50,"B025":40,"B026":45,"B027":35,"B028":50,
    "B029":60,"B030":55,
    "S001":90,"S002":85,"S003":40,"S004":95,"S005":70,"S006":80,"S007":60,
    "S008":70,"S009":60,"S010":65,"S011":55,"S012":65,"S013":70,"S014":80,
    "S015":90,"S016":100,"S017":50,"S018":45,"S019":40,"S020":60,"S021":75,
    "S022":80,"S023":100,"S024":70,"S025":35,
    "L001":50,"L002":45,"L003":45,"L004":40,"L005":30,"L006":35,"L007":30,
    "L008":25,"L009":35,"L010":40,"L011":45,"L012":60,"L013":50,"L014":20,
    "L015":35,"L016":30,"L017":25,"L018":25,"L019":20,"L020":20,
    "P001":40,"P002":45,"P003":35,"P004":30,"P005":25,"P006":25,"P007":20,
    "P008":30,"P009":25,"P010":20,"P011":35,"P012":35,"P013":30,"P014":40,"P015":50,
    "A001":100,"A002":60,"A003":40,"A004":60,"A005":45,"A006":50,"A007":90,
    "A008":70,"A009":80,"A010":80,"A011":70,"A012":65,"A013":55,"A014":60,
    "A015":65,"A016":75,"A017":70,"A018":65,"A019":55,"A020":60,"A021":40,
    "A022":55,"A023":50,"A024":70,"A025":80,"A026":75,"A027":65,"A028":70,
    "A029":60,"A030":50,"A031":55,"A032":50,"A033":30,"A034":40,"A035":40,
    "C001":60,"C002":50,"C003":70,"C004":35,"C005":30,"C006":30,"C007":55,
    "C008":30,"C009":15,"C010":40,"C011":60,"C012":45,"C013":30,"C014":35,
    "C015":40,"C016":50,"C017":25,"C018":45,"C019":35,"C020":40,"C021":60,
    "C022":30,"C023":30,"C024":40,"C025":25,
    "G001":40,"G002":35,"G003":55,"G004":50,"G005":60,"G006":60,"G007":35,
    "G008":50,"G009":30,"G010":30,"G011":45,"G012":40,"G013":45,"G014":50,
    "G015":20,"G016":30,"G017":40,"G018":50,"G019":40,"G020":25,"G021":35,
    "G022":60,"G023":70,"G024":55,"G025":35,
    "FV01":100,"FV02":80,"FV03":90,"FV04":70,"FV05":60,"FV06":80,"FV07":100,
    "FV08":50,"FV09":40,"FV10":90,"FV11":70,"FV12":60,"FV13":50,"FV14":45,"FV15":60,
    "CM01":50,"CM02":45,"CM03":40,"CM04":35,"CM05":30,"CM06":25,
    "CM07":40,"CM08":35,"CM09":30,"CM10":20,
}

# ══════════════════════════════════════════
#  GENERACIÓN DE 100 USUARIOS BASE
# ══════════════════════════════════════════
def _generar_usuarios_base():
    random.seed(42)
    _NM = ["Juan Carlos","Luis Miguel","Jose Antonio","Roberto","Eduardo","Fernando",
           "Diego","Pablo","Andres","Santiago","Gabriel","Daniel","Sebastian","Mateo",
           "Nicolas","Ricardo","David","Marco","Cristian","Javier","Victor","Hugo",
           "Raul","Oscar","Felipe","Ivan","Mario","Rodrigo","Alejandro","Manuel"]
    _NF = ["Maria Jose","Ana Lucia","Carmen","Rosa","Patricia","Gabriela","Valeria",
           "Andrea","Isabella","Daniela","Camila","Sofia","Natalia","Fernanda","Paola",
           "Melissa","Katherine","Stephanie","Jessica","Vanessa","Monica","Laura",
           "Diana","Sandra","Claudia","Elena","Beatriz","Silvia","Veronica","Martha"]
    _AP = ["Garcia","Rodriguez","Martinez","Lopez","Gonzalez","Perez","Sanchez",
           "Torres","Ramirez","Flores","Rivera","Morales","Jimenez","Herrera","Mendoza",
           "Ortega","Castro","Vargas","Romero","Guerrero","Suarez","Vega","Molina",
           "Reyes","Cabrera","Pacheco","Delgado","Carrillo","Medina","Aguirre"]
    hoy = datetime(2026, 5, 11)
    cedulas_usadas = set()
    usuarios = []
    for i in range(100):
        es_mujer = (i % 2 == 0)
        nombre_pila = random.choice(_NF if es_mujer else _NM)
        nombre = f"{nombre_pila} {random.choice(_AP)} {random.choice(_AP)}"
        while True:
            prov = f"{random.randint(1,22):02d}"
            d3   = random.randint(0, 5)
            resto = f"{random.randint(0,9999999):07d}"
            ced   = f"{prov}{d3}{resto}"
            if ced not in cedulas_usadas:
                cedulas_usadas.add(ced)
                break
        slug = nombre_pila.lower().replace(" ",".")
        email = f"{slug}{random.randint(1,99)}@gmail.com"
        tel   = f"09{random.randint(10000000,99999999)}"
        dias  = random.randint(0, 365)
        fecha = (hoy - timedelta(days=dias)).strftime("%Y-%m-%d")
        usuarios.append({"cedula":ced,"nombre":nombre,"email":email,
                          "telefono":tel,"fecha_registro":fecha})
    return usuarios

USUARIOS_BASE = _generar_usuarios_base()

# ══════════════════════════════════════════
#  VARIABLES GLOBALES Y FUNCIONES CSV
# ══════════════════════════════════════════
inventario = {}
usuarios   = {}

def inicializar_productos():
    if not os.path.exists(ARCH_PRODUCTOS):
        with open(ARCH_PRODUCTOS,"w",newline="",encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["codigo","nombre","precio","categoria","descripcion"])
            for p in CATALOGO_BASE:
                w.writerow([p["codigo"],p["nombre"],p["precio"],p["categoria"],p["descripcion"]])

def inicializar_inventario():
    global inventario
    catalogo = {}
    inicializar_productos()
    with open(ARCH_PRODUCTOS,"r",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            catalogo[r["codigo"]] = {"codigo":r["codigo"],"nombre":r["nombre"],
                                      "precio":float(r["precio"]),"categoria":r["categoria"],
                                      "descripcion":r["descripcion"]}
    if os.path.exists(ARCH_INVENTARIO):
        with open(ARCH_INVENTARIO,"r",encoding="utf-8") as f:
            stock = {r["codigo"]:int(r["stock"]) for r in csv.DictReader(f)}
    else:
        stock = dict(STOCK_INICIAL)
        _guardar_solo_stock(stock)
    for cod, prod in catalogo.items():
        inventario[cod] = dict(prod)
        inventario[cod]["stock"] = stock.get(cod, 0)

def _guardar_solo_stock(stock_dict):
    with open(ARCH_INVENTARIO,"w",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["codigo","stock"])
        for cod, s in stock_dict.items():
            w.writerow([cod, s])

def guardar_inventario_csv():
    _guardar_solo_stock({cod: p["stock"] for cod, p in inventario.items()})

def descontar_stock(carrito):
    for item in carrito:
        inventario[item["codigo"]]["stock"] -= item["cantidad"]
    guardar_inventario_csv()

def inicializar_usuarios():
    global usuarios
    if os.path.exists(ARCH_USUARIOS):
        with open(ARCH_USUARIOS,"r",encoding="utf-8") as f:
            for r in csv.DictReader(f):
                usuarios[r["cedula"]] = r
    else:
        with open(ARCH_USUARIOS,"w",newline="",encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cedula","nombre","email","telefono","fecha_registro"])
            for u in USUARIOS_BASE:
                w.writerow([u["cedula"],u["nombre"],u["email"],u["telefono"],u["fecha_registro"]])
                usuarios[u["cedula"]] = u

def guardar_usuarios_csv():
    with open(ARCH_USUARIOS,"w",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cedula","nombre","email","telefono","fecha_registro"])
        for u in usuarios.values():
            w.writerow([u["cedula"],u["nombre"],u["email"],u["telefono"],u["fecha_registro"]])

def inicializar_csv_ventas():
    if not os.path.exists(ARCH_TRANSACCIONES):
        with open(ARCH_TRANSACCIONES,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(["id_transaccion","fecha","hora","cajero",
                                    "cedula_cliente","nombre_cliente","subtotal",
                                    "iva","total","metodo_pago","estado","valida_hasta"])
    if not os.path.exists(ARCH_DETALLES):
        with open(ARCH_DETALLES,"w",newline="",encoding="utf-8") as f:
            csv.writer(f).writerow(["id_transaccion","codigo_producto","nombre_producto",
                                    "precio_unitario","cantidad","subtotal_linea"])

def guardar_transaccion(id_tx, cajero, carrito, metodo, cedula_cli, nombre_cli):
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora  = ahora.strftime("%H:%M:%S")
    subtotal = sum(i["precio"]*i["cantidad"] for i in carrito)
    iva      = round(subtotal*0.12, 2)
    total    = round(subtotal+iva, 2)
    valida   = (ahora + timedelta(days=365)).strftime("%Y-%m-%d")
    with open(ARCH_TRANSACCIONES,"a",newline="",encoding="utf-8") as f:
        csv.writer(f).writerow([id_tx,fecha,hora,cajero,cedula_cli,nombre_cli,
                                round(subtotal,2),iva,total,metodo,"COMPLETADA",valida])
    with open(ARCH_DETALLES,"a",newline="",encoding="utf-8") as f:
        ww = csv.writer(f)
        for i in carrito:
            ww.writerow([id_tx,i["codigo"],i["nombre"],i["precio"],i["cantidad"],
                         round(i["precio"]*i["cantidad"],2)])
    return subtotal, iva, total, valida

def cargar_transacciones():
    if not os.path.exists(ARCH_TRANSACCIONES): return []
    with open(ARCH_TRANSACCIONES,"r",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def siguiente_id():
    txs = cargar_transacciones()
    if not txs: return "TX-0001"
    ultimo = txs[-1]["id_transaccion"]
    num = int(ultimo.split("-")[1]) + 1
    return f"TX-{num:04d}"

def generar_historial_anual():
    txs = cargar_transacciones()
    if len(txs) >= 200: return
    random.seed(99)
    hoy      = datetime(2026, 5, 11)
    inicio   = hoy - timedelta(days=365)
    metodos  = ["Efectivo","Efectivo","Efectivo","Tarjeta","Transferencia","QR"]
    cedulas  = list(usuarios.keys())
    codigos  = list(inventario.keys())
    tx_num   = 1
    registros_tx  = []
    registros_det = []
    for _ in range(280):
        dias_offset = random.randint(0, 364)
        hora_h = random.randint(8, 20)
        hora_m = random.randint(0, 59)
        fecha_tx = inicio + timedelta(days=dias_offset)
        fecha_str = fecha_tx.strftime("%Y-%m-%d")
        hora_str  = f"{hora_h:02d}:{hora_m:02d}:{random.randint(0,59):02d}"
        id_tx     = f"TX-{tx_num:04d}"
        tx_num   += 1
        cedula_c  = random.choice(cedulas) if cedulas else "9999999999"
        nombre_c  = usuarios.get(cedula_c,{}).get("nombre","Consumidor Final")
        n_prods   = random.randint(1,5)
        prods_tx  = random.sample(codigos, min(n_prods, len(codigos)))
        subtotal  = 0.0
        for cod in prods_tx:
            prod = inventario[cod]
            cant = random.randint(1,3)
            sub  = round(prod["precio"]*cant, 2)
            subtotal += sub
            registros_det.append([id_tx, cod, prod["nombre"], prod["precio"], cant, sub])
        subtotal = round(subtotal, 2)
        iva      = round(subtotal*0.12, 2)
        total    = round(subtotal+iva, 2)
        valida   = (fecha_tx + timedelta(days=365)).strftime("%Y-%m-%d")
        metodo   = random.choice(metodos)
        registros_tx.append([id_tx,fecha_str,hora_str,"Cajero_01",cedula_c,
                              nombre_c,subtotal,iva,total,metodo,"COMPLETADA",valida])
    registros_tx.sort(key=lambda r: (r[1], r[2]))
    for i, r in enumerate(registros_tx, 1):
        r[0] = f"TX-{i:04d}"
    with open(ARCH_TRANSACCIONES,"w",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_transaccion","fecha","hora","cajero","cedula_cliente",
                    "nombre_cliente","subtotal","iva","total","metodo_pago","estado","valida_hasta"])
        for r in registros_tx: w.writerow(r)
    det_por_id = {}
    for d in registros_det: det_por_id.setdefault(d[0], []).append(d)
    with open(ARCH_DETALLES,"w",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_transaccion","codigo_producto","nombre_producto",
                    "precio_unitario","cantidad","subtotal_linea"])
        for r in registros_tx:
            for d in det_por_id.get(r[0], []):
                w.writerow([r[0]]+d[1:])

def primera_ejecucion():
    if not os.path.exists(ARCH_PRODUCTOS):
        print("✅ Creando productos.csv y inventario.csv...")
    if not os.path.exists(ARCH_USUARIOS):
        print("✅ Creando 100 usuarios pre-registrados...")
    if not os.path.exists(ARCH_TRANSACCIONES) or len(cargar_transacciones()) < 200:
        print("✅ Generando historial de 1 año de transacciones...")

# ══════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════
class TPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TPS QuickShop v3.0 — Punto de Venta")
        self.root.geometry("1600x900")
        self.root.minsize(1400, 800)
        self.root.configure(bg=BG_OSCURO)
        self.root.resizable(True, True)

        primera_ejecucion()
        inicializar_inventario()
        inicializar_usuarios()
        inicializar_csv_ventas()
        generar_historial_anual()

        self.cajero       = "Cajero_01"
        self.carrito      = []
        self.var_id       = tk.StringVar(value=siguiente_id())

        self._estilos()
        self._header()
        self._notebook()

    def _estilos(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=BG_CARD, foreground=BLANCO,
                    fieldbackground=BG_CARD, rowheight=26, font=F_CHICA, borderwidth=0)
        s.configure("Treeview.Heading", background=BG_OSCURO, foreground=AZUL,
                    font=("Consolas",9,"bold"), relief="flat")
        s.map("Treeview", background=[("selected",AZUL_OSC)], foreground=[("selected",BLANCO)])
        s.configure("TNotebook", background=BG_OSCURO, borderwidth=0)
        s.configure("TNotebook.Tab", background=BG_CARD, foreground=GRIS,
                    font=("Consolas",10,"bold"), padding=[14,8])
        s.map("TNotebook.Tab", background=[("selected",AZUL_OSC)], foreground=[("selected",BLANCO)])
        s.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD,
                    foreground=BLANCO, font=F_CHICA)

    def _header(self):
        bar = tk.Frame(self.root, bg=BG_PANEL, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text="🛒  QuickShop — Sistema TPS v3.0",
                 font=("Consolas",14,"bold"), bg=BG_PANEL, fg=AZUL).pack(side="left",padx=18)
        tk.Label(bar, text="Punto de Venta | 200 productos | 100+ clientes",
                 font=F_CHICA, bg=BG_PANEL, fg=GRIS).pack(side="left")
        self.lbl_hora = tk.Label(bar, text="", font=F_NORMAL, bg=BG_PANEL, fg=BLANCO)
        self.lbl_hora.pack(side="right", padx=18)
        tk.Label(bar, text=f"👤 {self.cajero}", font=F_NORMAL,
                 bg=BG_PANEL, fg=AMARILLO).pack(side="right", padx=12)
        self._tick()

    def _tick(self):
        self.lbl_hora.config(text="🕐 "+datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
        self.root.after(1000, self._tick)

    def _notebook(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=10, pady=(4,10))

        tab_venta = tk.Frame(nb, bg=BG_OSCURO)
        nb.add(tab_venta, text="  🧾 Punto de Venta  ")
        self._tab_venta(tab_venta)

        tab_cli = tk.Frame(nb, bg=BG_OSCURO)
        nb.add(tab_cli, text="  👥 Clientes  ")
        self._tab_clientes(tab_cli)

        tab_rep = tk.Frame(nb, bg=BG_OSCURO)
        nb.add(tab_rep, text="  📊 Reportes  ")
        self._tab_reportes(tab_rep)

    # ══════════════════════════════════════
    #  TAB 1: PUNTO DE VENTA
    # ══════════════════════════════════════
    def _tab_venta(self, parent):
        parent.columnconfigure(0, weight=3)
        parent.columnconfigure(1, weight=3)
        parent.columnconfigure(2, weight=2)
        parent.rowconfigure(0, weight=1)
        self._panel_catalogo(parent)
        self._panel_venta(parent)
        self._panel_historial(parent)

    def _panel_catalogo(self, parent):
        f = tk.Frame(parent, bg=BG_PANEL)
        f.grid(row=0, column=0, padx=(0,5), pady=2, sticky="nsew")
        tk.Label(f, text="📦  CATÁLOGO & STOCK", font=F_TITULO, bg=BG_PANEL, fg=AZUL).pack(anchor="w", padx=12, pady=(10,4))
        fil = tk.Frame(f, bg=BG_PANEL)
        fil.pack(fill="x", padx=10, pady=(0,4))
        tk.Label(fil, text="🔍", font=F_NORMAL, bg=BG_PANEL, fg=GRIS).pack(side="left")
        self.var_busq = tk.StringVar()
        self.var_busq.trace("w", lambda *a: self._cargar_catalogo())
        tk.Entry(fil, textvariable=self.var_busq, font=F_NORMAL, bg=BG_CARD, fg=BLANCO,
                 insertbackground=BLANCO, relief="flat", bd=4).pack(side="left", fill="x", expand=True, padx=4)
        cats = ["Todas"] + sorted({p["categoria"] for p in inventario.values()})
        self.var_cat = tk.StringVar(value="Todas")
        self.var_cat.trace("w", lambda *a: self._cargar_catalogo())
        ttk.Combobox(fil, textvariable=self.var_cat, values=cats, state="readonly", width=14, font=F_CHICA).pack(side="left")

        cols = ("codigo","nombre","precio","stock","cat")
        self.tv_cat = ttk.Treeview(f, columns=cols, show="headings")
        for col, txt, w, anch in [("codigo","Cód.",60,"center"),("nombre","Producto",180,"w"),
                                  ("precio","Precio",65,"center"),("stock","Stock",55,"center"),
                                  ("cat","Categ.",90,"center")]:
            self.tv_cat.heading(col, text=txt)
            self.tv_cat.column(col, width=w, anchor=anch)
        self.tv_cat.tag_configure("agotado", foreground=ROJO)
        self.tv_cat.tag_configure("bajo",    foreground=AMARILLO)
        self.tv_cat.tag_configure("normal",  foreground=BLANCO)
        sb = ttk.Scrollbar(f, orient="vertical", command=self.tv_cat.yview)
        self.tv_cat.configure(yscrollcommand=sb.set)
        self.tv_cat.pack(side="left", fill="both", expand=True, padx=(10,0), pady=4)
        sb.pack(side="left", fill="y", pady=4, padx=(0,6))
        self.tv_cat.bind("<Double-1>", lambda e: self._agregar_desde_catalogo())
        self._cargar_catalogo()

    def _panel_venta(self, parent):
        f = tk.Frame(parent, bg=BG_PANEL)
        f.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        enc = tk.Frame(f, bg=BG_CARD)
        enc.pack(fill="x", padx=10, pady=(10,4))
        tk.Label(enc, text="🧾  VENTA EN CURSO", font=F_TITULO, bg=BG_CARD, fg=VERDE).pack(side="left", padx=12, pady=8)
        tk.Label(enc, textvariable=self.var_id, font=("Consolas",11,"bold"), bg=BG_CARD, fg=AMARILLO).pack(side="right", padx=12)

        cols2 = ("nombre","pu","cant","sub")
        self.tv_cart = ttk.Treeview(f, columns=cols2, show="headings")
        for col, txt, w, anch in [("nombre","Producto",200,"w"),("pu","P.Unit.",75,"center"),
                                  ("cant","Cant.",55,"center"),("sub","Subtotal",90,"center")]:
            self.tv_cart.heading(col, text=txt)
            self.tv_cart.column(col, width=w, anchor=anch)
        sb2 = ttk.Scrollbar(f, orient="vertical", command=self.tv_cart.yview)
        self.tv_cart.configure(yscrollcommand=sb2.set)
        self.tv_cart.pack(side="left", fill="both", expand=True, padx=(10,0), pady=4)
        sb2.pack(side="left", fill="y", pady=4, padx=(0,6))
        tk.Button(f, text="🗑️  Quitar producto seleccionado", font=F_CHICA, bg=ROJO, fg="white",
                  activebackground="#c53030", relief="flat", cursor="hand2",
                  command=self._quitar).pack(fill="x", padx=10, pady=(0,4))

        tot = tk.Frame(f, bg=BG_CARD)
        tot.pack(fill="x", padx=10, pady=4)
        self.var_sub   = tk.StringVar(value="$0.00")
        self.var_iva   = tk.StringVar(value="$0.00")
        self.var_total = tk.StringVar(value="$0.00")
        self.var_items = tk.StringVar(value="0 items")
        def fila(lbl, var, color=BLANCO, grande=False):
            r = tk.Frame(tot, bg=BG_CARD); r.pack(fill="x", padx=12, pady=2)
            tk.Label(r, text=lbl, font=F_NORMAL, bg=BG_CARD, fg=GRIS).pack(side="left")
            tk.Label(r, textvariable=var, font=("Consolas",13,"bold") if grande else ("Consolas",10,"bold"),
                     bg=BG_CARD, fg=color).pack(side="right")
        fila("Items en carrito:", self.var_items, GRIS)
        fila("Subtotal:", self.var_sub)
        fila("IVA 12%:",  self.var_iva, AMARILLO)
        tk.Frame(tot, bg=BORDE, height=1).pack(fill="x", padx=10, pady=4)
        fila("TOTAL A PAGAR:", self.var_total, VERDE, grande=True)

        mp = tk.Frame(f, bg=BG_PANEL)
        mp.pack(fill="x", padx=10, pady=6)
        tk.Label(mp, text="Metodo de pago:", font=F_NORMAL, bg=BG_PANEL, fg=GRIS).pack(side="left")
        self.var_metodo = tk.StringVar(value="Efectivo")
        for m in ["Efectivo","Tarjeta","Transferencia","QR"]:
            tk.Radiobutton(mp, text=m, variable=self.var_metodo, value=m, font=F_CHICA, bg=BG_PANEL, fg=BLANCO,
                           selectcolor=BG_CARD, activebackground=BG_PANEL).pack(side="left",padx=5)

        acc = tk.Frame(f, bg=BG_PANEL)
        acc.pack(fill="x", padx=10, pady=8)
        tk.Button(acc, text="✅   COBRAR / PROCESAR VENTA", font=("Consolas",12,"bold"), bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2", height=2,
                  command=self._procesar).pack(fill="x", pady=(0,5))
        tk.Button(acc, text="❌  Cancelar venta", font=F_NORMAL, bg=BG_CARD, fg=ROJO,
                  activebackground=BG_CARD, relief="flat", cursor="hand2",
                  command=self._cancelar).pack(fill="x")

    def _panel_historial(self, parent):
        f = tk.Frame(parent, bg=BG_PANEL)
        f.grid(row=0, column=2, padx=(5,0), pady=2, sticky="nsew")
        tk.Label(f, text="📋  HISTORIAL DEL DIA", font=F_TITULO, bg=BG_PANEL, fg=AZUL).pack(anchor="w", padx=12, pady=(10,6))
        stats = tk.Frame(f, bg=BG_CARD)
        stats.pack(fill="x", padx=10, pady=(0,6))
        self.var_ntx  = tk.StringVar(value="0")
        self.var_tdia = tk.StringVar(value="$0.00")
        self.var_prom = tk.StringVar(value="$0.00")
        def stat_row(lbl, var, color):
            r = tk.Frame(stats, bg=BG_CARD); r.pack(fill="x", padx=10, pady=3)
            tk.Label(r, text=lbl, font=F_CHICA, bg=BG_CARD, fg=GRIS).pack(side="left")
            tk.Label(r, textvariable=var, font=F_TITULO, bg=BG_CARD, fg=color).pack(side="right")
        stat_row("Ventas hoy:",      self.var_ntx,  AMARILLO)
        stat_row("Total recaudado:", self.var_tdia, VERDE)
        stat_row("Ticket promedio:", self.var_prom, AZUL)
        cols3 = ("id","hora","cliente","total","metodo")
        self.tv_hist = ttk.Treeview(f, columns=cols3, show="headings", height=13)
        for col, txt, w, anch in [("id","ID",80,"center"),("hora","Hora",70,"center"),
                                  ("cliente","Cliente",110,"w"),("total","Total",70,"center"),
                                  ("metodo","Pago",80,"center")]:
            self.tv_hist.heading(col, text=txt)
            self.tv_hist.column(col, width=w, anchor=anch)
        sb3 = ttk.Scrollbar(f, orient="vertical", command=self.tv_hist.yview)
        self.tv_hist.configure(yscrollcommand=sb3.set)
        self.tv_hist.pack(fill="both", expand=True, padx=(10,0), pady=4)
        sb3.pack(side="left", fill="y", pady=4, padx=(0,6))
        tk.Button(f, text="🔄 Actualizar historial", font=F_CHICA, bg=BG_CARD, fg=AZUL,
                  activebackground=BG_CARD, relief="flat", cursor="hand2",
                  command=self._cargar_historial).pack(fill="x", padx=10, pady=(0,4))
        tk.Label(f, text="⚠️  STOCK CRITICO (<10 unid.)", font=F_CHICA, bg=BG_PANEL, fg=AMARILLO).pack(anchor="w", padx=12, pady=(4,2))
        cols4 = ("cod","prod","stock")
        self.tv_crit = ttk.Treeview(f, columns=cols4, show="headings", height=5)
        for col, txt, w in [("cod","Cod",50),("prod","Producto",130),("stock","Stock",50)]:
            self.tv_crit.heading(col, text=txt)
            self.tv_crit.column(col, width=w, anchor="center")
        self.tv_crit.tag_configure("agotado", foreground=ROJO)
        self.tv_crit.tag_configure("bajo",    foreground=AMARILLO)
        sb4 = ttk.Scrollbar(f, orient="vertical", command=self.tv_crit.yview)
        self.tv_crit.configure(yscrollcommand=sb4.set)
        self.tv_crit.pack(side="left", fill="both", expand=True, padx=(10,0), pady=4)
        sb4.pack(side="left", fill="y", pady=4, padx=(0,6))
        self._cargar_historial()
        self._actualizar_criticos()

    # ══════════════════════════════════════
    #  LÓGICA DE VENTA
    # ══════════════════════════════════════
    def _cargar_catalogo(self):
        busq = self.var_busq.get().lower()
        cat  = self.var_cat.get()
        for row in self.tv_cat.get_children(): self.tv_cat.delete(row)
        for p in sorted(inventario.values(), key=lambda x: x["codigo"]):
            if busq and busq not in p["nombre"].lower() and busq not in p["codigo"].lower(): continue
            if cat != "Todas" and p["categoria"] != cat: continue
            s = p["stock"]
            tag = "agotado" if s==0 else ("bajo" if s<10 else "normal")
            self.tv_cat.insert("","end",tags=(tag,), values=(
                p["codigo"],p["nombre"],f"${p['precio']:.2f}",
                "AGOTADO" if s==0 else s, p["categoria"]))

    def _agregar_desde_catalogo(self):
        sel = self.tv_cat.selection()
        if not sel: return
        vals   = self.tv_cat.item(sel[0])["values"]
        codigo = vals[0]
        p      = inventario[codigo]
        if p["stock"] == 0:
            messagebox.showerror("Sin stock",f'"{p["nombre"]}" esta agotado.'); return
        cantidad = 1
        ya = next((i["cantidad"] for i in self.carrito if i["codigo"]==codigo), 0)
        if cantidad > p["stock"] - ya:
            messagebox.showwarning("Stock insuficiente",
                f'Solo hay {p["stock"]-ya} unidades disponibles de "{p["nombre"]}".'); return
        for item in self.carrito:
            if item["codigo"] == codigo:
                item["cantidad"] += 1
                self._refresh_carrito(); return
        self.carrito.append({"codigo":codigo,"nombre":p["nombre"],"precio":p["precio"],"cantidad":1})
        self._refresh_carrito()

    def _quitar(self):
        sel = self.tv_cart.selection()
        if not sel: return
        self.carrito.pop(self.tv_cart.index(sel[0]))
        self._refresh_carrito()

    def _refresh_carrito(self):
        for row in self.tv_cart.get_children(): self.tv_cart.delete(row)
        subtotal = 0.0
        for item in self.carrito:
            sub = item["precio"]*item["cantidad"]; subtotal += sub
            self.tv_cart.insert("","end", values=(
                item["nombre"],f"${item['precio']:.2f}",item["cantidad"],f"${sub:.2f}"))
        iva = round(subtotal*0.12,2); total = round(subtotal+iva,2)
        n   = sum(i["cantidad"] for i in self.carrito)
        self.var_sub.set(f"${subtotal:.2f}"); self.var_iva.set(f"${iva:.2f}")
        self.var_total.set(f"${total:.2f}")
        self.var_items.set(f"{n} item{'s' if n!=1 else ''}")

    # ── SELECCIÓN DE CLIENTE (CORREGIDA) ──
    def _seleccionar_cliente_para_factura(self):
        dial = tk.Toplevel(self.root)
        dial.title("Datos del cliente")
        dial.geometry("440x280")
        dial.configure(bg=BG_OSCURO)
        dial.grab_set()
        dial.resizable(False, False)
        tk.Label(dial, text="Seleccione el cliente para la factura", font=F_TITULO, bg=BG_OSCURO, fg=AZUL).pack(pady=(16,10))
        frame_opciones = tk.Frame(dial, bg=BG_OSCURO)
        frame_opciones.pack(pady=10)
        resultado = {"cliente": None}

        def buscar():
            dial.withdraw()
            cliente = self._buscar_cliente_dialogo()
            if cliente is not None:
                resultado["cliente"] = cliente
                dial.destroy()
            else:
                dial.deiconify()

        def registrar():
            dial.withdraw()
            nuevo_cliente = self._registrar_cliente_con_retorno()
            if nuevo_cliente is not None:
                resultado["cliente"] = nuevo_cliente
                dial.destroy()
            else:
                dial.deiconify()

        def consumidor_final():
            dial.destroy()

        tk.Button(frame_opciones, text="🔍 Buscar Cliente Registrado", font=F_NORMAL, bg=AZUL, fg="white",
                  activebackground=AZUL_OSC, relief="flat", cursor="hand2", width=30, height=2,
                  command=buscar).pack(pady=6)
        tk.Button(frame_opciones, text="📝 Registrar Nuevo Cliente", font=F_NORMAL, bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2", width=30, height=2,
                  command=registrar).pack(pady=6)
        tk.Button(frame_opciones, text="🧑 Consumidor Final", font=F_NORMAL, bg=BG_CARD, fg=BLANCO,
                  activebackground=BG_CARD, relief="flat", cursor="hand2", width=30, height=2,
                  command=consumidor_final).pack(pady=6)
        self.root.wait_window(dial)
        return resultado["cliente"]

    def _buscar_cliente_dialogo(self):
        dial_busq = tk.Toplevel(self.root)
        dial_busq.title("Buscar cliente")
        dial_busq.geometry("520x420")
        dial_busq.configure(bg=BG_OSCURO)
        dial_busq.grab_set()
        tk.Label(dial_busq, text="Buscar cliente", font=F_TITULO, bg=BG_OSCURO, fg=AZUL).pack(pady=(12,6))
        busq_f = tk.Frame(dial_busq, bg=BG_OSCURO)
        busq_f.pack(fill="x", padx=14)
        tk.Label(busq_f, text="🔍", bg=BG_OSCURO, fg=GRIS, font=F_NORMAL).pack(side="left")
        var_b = tk.StringVar()
        cols = ("cedula","nombre","email")
        tv = ttk.Treeview(dial_busq, columns=cols, show="headings", height=12)
        for col, txt, w in [("cedula","Cedula",100),("nombre","Nombre",200),("email","Email",160)]:
            tv.heading(col, text=txt); tv.column(col, width=w)
        def refrescar(*a):
            b = var_b.get().lower()
            for r in tv.get_children(): tv.delete(r)
            for u in usuarios.values():
                if b in u["cedula"] or b in u["nombre"].lower() or b in u["email"].lower():
                    tv.insert("","end", values=(u["cedula"],u["nombre"],u["email"]))
        var_b.trace("w", refrescar)
        tk.Entry(busq_f, textvariable=var_b, font=F_NORMAL, bg=BG_CARD, fg=BLANCO,
                 insertbackground=BLANCO, relief="flat", bd=4).pack(side="left", fill="x", expand=True, padx=6)
        tv.pack(fill="both", expand=True, padx=14, pady=8)
        refrescar()
        resultado = {"cliente": None}
        def seleccionar():
            sel = tv.selection()
            if not sel:
                messagebox.showwarning("Aviso","Seleccione un cliente de la lista.", parent=dial_busq); return
            ced = tv.item(sel[0])["values"][0]
            resultado["cliente"] = usuarios.get(str(ced))
            dial_busq.destroy()
        def cancelar():
            dial_busq.destroy()
        bot_frame = tk.Frame(dial_busq, bg=BG_OSCURO)
        bot_frame.pack(pady=10)
        tk.Button(bot_frame, text="✅ Seleccionar cliente", font=F_NORMAL, bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2",
                  command=seleccionar).pack(side="left", padx=5)
        tk.Button(bot_frame, text="❌ Cancelar", font=F_NORMAL, bg=BG_CARD, fg=ROJO,
                  activebackground=BG_CARD, relief="flat", cursor="hand2",
                  command=cancelar).pack(side="left", padx=5)
        self.root.wait_window(dial_busq)
        return resultado["cliente"]

    def _registrar_cliente_con_retorno(self):
        dial_reg = tk.Toplevel(self.root)
        dial_reg.title("Registrar nuevo cliente")
        dial_reg.geometry("420x340")
        dial_reg.configure(bg=BG_OSCURO)
        dial_reg.grab_set()
        tk.Label(dial_reg, text="Registrar nuevo cliente", font=F_TITULO, bg=BG_OSCURO, fg=AZUL).pack(pady=(14,8))
        campos = {}
        for lbl, key in [("Cedula (10 digitos):","cedula"),("Nombre completo:","nombre"),
                          ("Email:","email"),("Telefono (09XXXXXXXX):","telefono")]:
            r = tk.Frame(dial_reg, bg=BG_OSCURO); r.pack(fill="x", padx=20, pady=4)
            tk.Label(r, text=lbl, font=F_CHICA, bg=BG_OSCURO, fg=GRIS, width=24, anchor="w").pack(side="left")
            var = tk.StringVar()
            tk.Entry(r, textvariable=var, font=F_NORMAL, bg=BG_CARD, fg=BLANCO, insertbackground=BLANCO,
                     relief="flat", bd=4).pack(side="left", fill="x", expand=True)
            campos[key] = var
        resultado = {"cliente": None}
        def guardar():
            ced  = campos["cedula"].get().strip()
            nom  = campos["nombre"].get().strip()
            em   = campos["email"].get().strip()
            tel  = campos["telefono"].get().strip()
            if len(ced) != 10 or not ced.isdigit():
                messagebox.showerror("Error","La cedula debe tener 10 digitos numericos.",parent=dial_reg); return
            if ced in usuarios:
                messagebox.showerror("Error","Ya existe un cliente con esa cedula.",parent=dial_reg); return
            if not nom:
                messagebox.showerror("Error","El nombre es obligatorio.",parent=dial_reg); return
            hoy = datetime.now().strftime("%Y-%m-%d")
            nuevo = {"cedula":ced,"nombre":nom,"email":em,"telefono":tel,"fecha_registro":hoy}
            usuarios[ced] = nuevo
            guardar_usuarios_csv()
            self._cargar_tabla_clientes()
            resultado["cliente"] = nuevo
            dial_reg.destroy()
        def cancelar():
            dial_reg.destroy()
        tk.Button(dial_reg, text="💾 Guardar cliente", font=F_NORMAL, bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2",
                  command=guardar).pack(pady=14)
        tk.Button(dial_reg, text="Cancelar", font=F_CHICA, bg=BG_CARD, fg=ROJO,
                  relief="flat", cursor="hand2", command=cancelar).pack()
        self.root.wait_window(dial_reg)
        return resultado["cliente"]

    def _procesar(self):
        if not self.carrito:
            messagebox.showwarning("Carrito vacio","Agrega productos antes de cobrar."); return

        cliente = self._seleccionar_cliente_para_factura()
        if cliente is None:
            cedula_c = "9999999999"
            nombre_c = "Consumidor Final"
            email_c  = "N/A"
            tel_c    = "N/A"
        else:
            cedula_c = cliente["cedula"]
            nombre_c = cliente["nombre"]
            email_c  = cliente["email"]
            tel_c    = cliente["telefono"]

        id_tx  = self.var_id.get()
        metodo = self.var_metodo.get()

        descontar_stock(self.carrito)
        subtotal, iva, total, valida = guardar_transaccion(
            id_tx, self.cajero, self.carrito, metodo, cedula_c, nombre_c)

        lineas = "\n".join(
            f"  {i['nombre'][:26]:<26} x{i['cantidad']:>2}  ${i['precio']*i['cantidad']:.2f}"
            for i in self.carrito)
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        hora_hoy  = datetime.now().strftime("%H:%M:%S")
        msg = (
            f"{'═'*50}\n"
            f"      QUICKSHOP MINIMARKET\n"
            f"      RUC: 1791234567001\n"
            f"      FACTURA ELECTRONICA\n"
            f"{'═'*50}\n"
            f"  N°: {id_tx:<18} Fecha: {fecha_hoy}\n"
            f"  Hora: {hora_hoy:<17} Valida hasta: {valida}\n"
            f"{'─'*50}\n"
            f"  CLIENTE : {nombre_c[:28]}\n"
            f"  CEDULA  : {cedula_c}\n"
            f"  EMAIL   : {email_c}\n"
            f"  TEL     : {tel_c}\n"
            f"{'─'*50}\n"
            f"{lineas}\n"
            f"{'─'*50}\n"
            f"  SUBTOTAL  :           ${subtotal:.2f}\n"
            f"  IVA 12%   :           ${iva:.2f}\n"
            f"  TOTAL     :           ${total:.2f}\n"
            f"{'─'*50}\n"
            f"  METODO DE PAGO: {metodo}\n"
            f"  CAJERO: {self.cajero}\n"
            f"{'═'*50}\n"
            f"       Gracias por su compra!\n"
            f"       www.quickshop.ec\n"
        )
        messagebox.showinfo("FACTURA — Venta procesada", msg)
        self.carrito = []; self._refresh_carrito()
        self.var_id.set(siguiente_id())
        self._cargar_catalogo(); self._cargar_historial(); self._actualizar_criticos()

    def _cancelar(self):
        if not self.carrito: return
        if messagebox.askyesno("Cancelar venta","Cancelar la venta actual?"):
            self.carrito = []; self._refresh_carrito()

    def _cargar_historial(self):
        for row in self.tv_hist.get_children(): self.tv_hist.delete(row)
        txs = cargar_transacciones()
        hoy = datetime.now().strftime("%Y-%m-%d")
        total_dia = 0.0; count = 0
        for tx in reversed(txs):
            t = float(tx["total"])
            nc = tx.get("nombre_cliente","N/A")
            nc_short = nc[:14] if len(nc)>14 else nc
            self.tv_hist.insert("","end", values=(
                tx["id_transaccion"], tx["hora"], nc_short,
                f"${t:.2f}", tx["metodo_pago"]))
            if tx["fecha"] == hoy:
                total_dia += t; count += 1
        self.var_ntx.set(str(count))
        self.var_tdia.set(f"${total_dia:.2f}")
        self.var_prom.set(f"${(total_dia/count):.2f}" if count else "$0.00")

    def _actualizar_criticos(self):
        for row in self.tv_crit.get_children(): self.tv_crit.delete(row)
        criticos = sorted([p for p in inventario.values() if p["stock"]<10],
                          key=lambda x: x["stock"])
        for p in criticos:
            tag = "agotado" if p["stock"]==0 else "bajo"
            self.tv_crit.insert("","end", tags=(tag,), values=(
                p["codigo"], p["nombre"][:18],
                "AGOTADO" if p["stock"]==0 else p["stock"]))

    # ══════════════════════════════════════
    #  TAB 2: CLIENTES
    # ══════════════════════════════════════
    def _tab_clientes(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        top = tk.Frame(parent, bg=BG_PANEL)
        top.grid(row=0, column=0, sticky="ew", padx=8, pady=(8,4))
        tk.Label(top, text="👥  GESTIÓN DE CLIENTES REGISTRADOS", font=F_TITULO, bg=BG_PANEL, fg=AZUL).pack(side="left", padx=12, pady=8)
        self.var_total_cli = tk.StringVar(value="0")
        tk.Label(top, text="Total clientes:", font=F_CHICA, bg=BG_PANEL, fg=GRIS).pack(side="right", padx=4)
        tk.Label(top, textvariable=self.var_total_cli, font=F_TITULO, bg=BG_PANEL, fg=VERDE).pack(side="right", padx=(0,14))
        tools = tk.Frame(parent, bg=BG_OSCURO)
        tools.grid(row=1, column=0, sticky="ew", padx=8)
        tk.Label(tools, text="🔍", font=F_NORMAL, bg=BG_OSCURO, fg=GRIS).pack(side="left", padx=(0,4))
        self.var_busq_cli = tk.StringVar()
        self.var_busq_cli.trace("w", lambda *a: self._cargar_tabla_clientes())
        tk.Entry(tools, textvariable=self.var_busq_cli, font=F_NORMAL, bg=BG_CARD, fg=BLANCO,
                 insertbackground=BLANCO, relief="flat", bd=4, width=30).pack(side="left", padx=4, pady=6)
        tk.Button(tools, text="➕ Nuevo cliente", font=F_NORMAL, bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2",
                  command=self._nuevo_cliente).pack(side="left", padx=6)
        tk.Button(tools, text="🗑️ Eliminar seleccionado", font=F_NORMAL, bg=ROJO, fg="white",
                  activebackground="#c53030", relief="flat", cursor="hand2",
                  command=self._eliminar_cliente).pack(side="left", padx=4)
        tk.Button(tools, text="🔄 Refrescar", font=F_NORMAL, bg=BG_CARD, fg=AZUL,
                  activebackground=BG_CARD, relief="flat", cursor="hand2",
                  command=self._cargar_tabla_clientes).pack(side="left", padx=4)
        tbl_f = tk.Frame(parent, bg=BG_OSCURO)
        tbl_f.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0,8))
        parent.rowconfigure(2, weight=1)
        cols = ("cedula","nombre","email","telefono","fecha_reg")
        self.tv_cli = ttk.Treeview(tbl_f, columns=cols, show="headings")
        for col, txt, w, anch in [("cedula","Cedula",100,"center"),("nombre","Nombre Completo",230,"w"),
                                  ("email","Email",220,"w"),("telefono","Telefono",110,"center"),
                                  ("fecha_reg","Registrado",100,"center")]:
            self.tv_cli.heading(col, text=txt)
            self.tv_cli.column(col, width=w, anchor=anch)
        sb_c = ttk.Scrollbar(tbl_f, orient="vertical", command=self.tv_cli.yview)
        self.tv_cli.configure(yscrollcommand=sb_c.set)
        self.tv_cli.pack(side="left", fill="both", expand=True)
        sb_c.pack(side="left", fill="y")
        self._cargar_tabla_clientes()

    def _cargar_tabla_clientes(self):
        busq = self.var_busq_cli.get().lower()
        for row in self.tv_cli.get_children(): self.tv_cli.delete(row)
        for u in sorted(usuarios.values(), key=lambda x: x["nombre"]):
            if busq and busq not in u["cedula"] and busq not in u["nombre"].lower() \
               and busq not in u["email"].lower(): continue
            self.tv_cli.insert("","end", values=(u["cedula"],u["nombre"],u["email"],u["telefono"],u["fecha_registro"]))
        self.var_total_cli.set(str(len(usuarios)))

    def _nuevo_cliente(self):
        dial = tk.Toplevel(self.root)
        dial.title("Registrar nuevo cliente")
        dial.geometry("420x340")
        dial.configure(bg=BG_OSCURO)
        dial.grab_set()
        tk.Label(dial, text="Registrar nuevo cliente", font=F_TITULO, bg=BG_OSCURO, fg=AZUL).pack(pady=(14,8))
        campos = {}
        for lbl, key in [("Cedula (10 digitos):","cedula"),("Nombre completo:","nombre"),
                          ("Email:","email"),("Telefono (09XXXXXXXX):","telefono")]:
            r = tk.Frame(dial, bg=BG_OSCURO); r.pack(fill="x", padx=20, pady=4)
            tk.Label(r, text=lbl, font=F_CHICA, bg=BG_OSCURO, fg=GRIS, width=24, anchor="w").pack(side="left")
            var = tk.StringVar()
            tk.Entry(r, textvariable=var, font=F_NORMAL, bg=BG_CARD, fg=BLANCO, insertbackground=BLANCO,
                     relief="flat", bd=4).pack(side="left", fill="x", expand=True)
            campos[key] = var
        def guardar():
            ced  = campos["cedula"].get().strip()
            nom  = campos["nombre"].get().strip()
            em   = campos["email"].get().strip()
            tel  = campos["telefono"].get().strip()
            if len(ced) != 10 or not ced.isdigit():
                messagebox.showerror("Error","La cedula debe tener 10 digitos numericos.",parent=dial); return
            if ced in usuarios:
                messagebox.showerror("Error","Ya existe un cliente con esa cedula.",parent=dial); return
            if not nom:
                messagebox.showerror("Error","El nombre es obligatorio.",parent=dial); return
            hoy = datetime.now().strftime("%Y-%m-%d")
            usuarios[ced] = {"cedula":ced,"nombre":nom,"email":em,"telefono":tel,"fecha_registro":hoy}
            guardar_usuarios_csv()
            self._cargar_tabla_clientes()
            messagebox.showinfo("Exito",f"Cliente '{nom}' registrado correctamente.",parent=dial)
            dial.destroy()
        tk.Button(dial, text="💾 Guardar cliente", font=F_NORMAL, bg=VERDE, fg="white",
                  activebackground=VERDE_OSC, relief="flat", cursor="hand2",
                  command=guardar).pack(pady=14)

    def _eliminar_cliente(self):
        sel = self.tv_cli.selection()
        if not sel:
            messagebox.showwarning("Aviso","Selecciona un cliente de la tabla."); return
        ced = self.tv_cli.item(sel[0])["values"][0]
        u   = usuarios.get(str(ced))
        if not u: return
        if messagebox.askyesno("Confirmar",f"Eliminar a '{u['nombre']}'?\nEsta accion no se puede deshacer."):
            del usuarios[str(ced)]
            guardar_usuarios_csv()
            self._cargar_tabla_clientes()
            messagebox.showinfo("Eliminado",f"Cliente eliminado correctamente.")

    # ══════════════════════════════════════
    #  TAB 3: REPORTES
    # ══════════════════════════════════════
    def _tab_reportes(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)
        tk.Label(parent, text="📊  REPORTES Y ESTADÍSTICAS — Últimos 12 meses", font=F_TITULO, bg=BG_OSCURO, fg=AZUL).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(10,6))
        izq = tk.Frame(parent, bg=BG_PANEL)
        izq.grid(row=1, column=0, padx=(8,4), pady=(0,8), sticky="nsew")
        tk.Label(izq, text="Resumen general", font=F_TITULO, bg=BG_PANEL, fg=BLANCO).pack(anchor="w", padx=12, pady=(10,6))
        stats_frame = tk.Frame(izq, bg=BG_CARD)
        stats_frame.pack(fill="x", padx=10, pady=(0,8))
        self.var_rep_total    = tk.StringVar(value="—")
        self.var_rep_ingresos = tk.StringVar(value="—")
        self.var_rep_avg      = tk.StringVar(value="—")
        self.var_rep_cli      = tk.StringVar(value="—")
        def stat(lbl, var, color=BLANCO):
            r = tk.Frame(stats_frame, bg=BG_CARD); r.pack(fill="x", padx=12, pady=4)
            tk.Label(r, text=lbl, font=F_NORMAL, bg=BG_CARD, fg=GRIS).pack(side="left")
            tk.Label(r, textvariable=var, font=F_TITULO, bg=BG_CARD, fg=color).pack(side="right")
        stat("Total transacciones:",   self.var_rep_total,    AMARILLO)
        stat("Ingresos totales:",       self.var_rep_ingresos, VERDE)
        stat("Promedio por factura:",   self.var_rep_avg,      AZUL)
        stat("Clientes registrados:",   self.var_rep_cli,      MORADO)
        tk.Label(izq, text="Promedio de compras por N facturas", font=F_TITULO, bg=BG_PANEL, fg=BLANCO).pack(anchor="w", padx=12, pady=(10,4))
        n_frame = tk.Frame(izq, bg=BG_CARD)
        n_frame.pack(fill="x", padx=10, pady=(0,8))
        tk.Label(n_frame, text="Analizar las últimas", font=F_NORMAL, bg=BG_CARD, fg=GRIS).pack(side="left", padx=12, pady=8)
        self.spin_n = tk.Spinbox(n_frame, from_=1, to=500, width=6, font=F_NORMAL, bg=BG_OSCURO, fg=BLANCO, buttonbackground=BG_OSCURO, relief="flat")
        self.spin_n.pack(side="left", padx=4)
        tk.Label(n_frame, text="facturas", font=F_NORMAL, bg=BG_CARD, fg=GRIS).pack(side="left")
        tk.Button(n_frame, text="Calcular", font=F_NORMAL, bg=AZUL, fg="white", activebackground=AZUL_OSC, relief="flat", cursor="hand2", command=self._calcular_avg_n).pack(side="left", padx=8)
        self.var_avg_n = tk.StringVar(value="")
        tk.Label(izq, textvariable=self.var_avg_n, font=("Consolas",13,"bold"), bg=BG_PANEL, fg=VERDE, wraplength=380, justify="left").pack(anchor="w", padx=14)
        tk.Label(izq, text="Ventas por método de pago", font=F_TITULO, bg=BG_PANEL, fg=BLANCO).pack(anchor="w", padx=12, pady=(14,4))
        cols_mp = ("metodo","cantidad","total")
        self.tv_mp = ttk.Treeview(izq, columns=cols_mp, show="headings", height=6)
        for col, txt, w in [("metodo","Método",120),("cantidad","# Ventas",90),("total","Total $",100)]:
            self.tv_mp.heading(col, text=txt)
            self.tv_mp.column(col, width=w, anchor="center")
        self.tv_mp.pack(fill="x", padx=10, pady=(0,8))
        der = tk.Frame(parent, bg=BG_PANEL)
        der.grid(row=1, column=1, padx=(4,8), pady=(0,8), sticky="nsew")
        tk.Label(der, text="Top 15 productos más vendidos", font=F_TITULO, bg=BG_PANEL, fg=BLANCO).pack(anchor="w", padx=12, pady=(10,6))
        cols_tp = ("pos","producto","cantidad","ingresos")
        self.tv_top = ttk.Treeview(der, columns=cols_tp, show="headings")
        for col, txt, w, anch in [("pos","#",35,"center"),("producto","Producto",220,"w"),
                                  ("cantidad","Unidades",90,"center"),("ingresos","Ingresos",90,"center")]:
            self.tv_top.heading(col, text=txt)
            self.tv_top.column(col, width=w, anchor=anch)
        sb_t = ttk.Scrollbar(der, orient="vertical", command=self.tv_top.yview)
        self.tv_top.configure(yscrollcommand=sb_t.set)
        self.tv_top.pack(side="left", fill="both", expand=True, padx=(10,0), pady=4)
        sb_t.pack(side="left", fill="y", pady=4, padx=(0,6))
        tk.Button(parent, text="🔄  Actualizar reportes", font=F_NORMAL, bg=BG_CARD, fg=AZUL,
                  activebackground=BG_CARD, relief="flat", cursor="hand2",
                  command=self._cargar_reportes).grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=(0,6))
        self._cargar_reportes()

    def _cargar_reportes(self):
        txs = cargar_transacciones()
        if not txs:
            self.var_rep_total.set("0"); self.var_rep_ingresos.set("$0.00")
            self.var_rep_avg.set("$0.00"); self.var_rep_cli.set(str(len(usuarios))); return
        totales  = [float(t["total"]) for t in txs]
        ingresos = sum(totales)
        avg      = ingresos / len(totales) if totales else 0
        self.var_rep_total.set(str(len(txs)))
        self.var_rep_ingresos.set(f"${ingresos:,.2f}")
        self.var_rep_avg.set(f"${avg:.2f}")
        self.var_rep_cli.set(str(len(usuarios)))
        mp_count = {}; mp_total = {}
        for tx in txs:
            m = tx["metodo_pago"]
            mp_count[m] = mp_count.get(m,0) + 1
            mp_total[m] = mp_total.get(m,0.0) + float(tx["total"])
        for row in self.tv_mp.get_children(): self.tv_mp.delete(row)
        for m in sorted(mp_count, key=lambda x: -mp_count[x]):
            self.tv_mp.insert("","end", values=(m, mp_count[m], f"${mp_total[m]:.2f}"))
        if os.path.exists(ARCH_DETALLES):
            prod_ventas = {}; prod_ingresos = {}
            with open(ARCH_DETALLES,"r",encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    cod = r["codigo_producto"]; cant = int(r["cantidad"])
                    prod_ventas[cod]   = prod_ventas.get(cod,0) + cant
                    prod_ingresos[cod] = prod_ingresos.get(cod,0.0) + float(r["subtotal_linea"])
            top = sorted(prod_ventas, key=lambda x: -prod_ventas[x])[:15]
            for row in self.tv_top.get_children(): self.tv_top.delete(row)
            for i, cod in enumerate(top, 1):
                nom = inventario.get(cod,{}).get("nombre", cod)
                self.tv_top.insert("","end", values=(i, nom, prod_ventas[cod], f"${prod_ingresos.get(cod,0):.2f}"))

    def _calcular_avg_n(self):
        try: n = int(self.spin_n.get())
        except: n = 10
        txs = cargar_transacciones()
        if not txs:
            self.var_avg_n.set("No hay transacciones registradas."); return
        ultimas = txs[-n:]
        totales = [float(t["total"]) for t in ultimas]
        avg     = sum(totales)/len(totales) if totales else 0
        self.var_avg_n.set(
            f"Últimas {len(ultimas)} facturas:\n"
            f"  Total vendido: ${sum(totales):.2f}\n"
            f"  Promedio por factura: ${avg:.2f}\n"
            f"  Factura más alta: ${max(totales):.2f}\n"
            f"  Factura más baja: ${min(totales):.2f}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = TPSApp(root)
    root.mainloop()