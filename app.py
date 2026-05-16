import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from streamlit_option_menu import option_menu
import io
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from st_aggrid.shared import JsCode
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import altair as alt
import re
import time
from functools import reduce
import streamlit.components.v1 as components

                
st.set_page_config(
    page_title="Esgari 360",
    page_icon="🚚",  # <- icono de camión
    layout="wide"    # <- modo pantalla completa
)

logo_base64 = """
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
"""

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo de la Empresa" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)
# Inicializar claves
def init_session_state():
    defaults = {
        "logged_in": False,
        "username": "",
        "rol": "",
        "proyectos": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def ct(texto):
    st.markdown(f"<h1 style='text-align: center;'>{texto}</h1>", unsafe_allow_html=True)

# Descargar Excel desde Google Drive
EXCEL_URL = st.secrets["urls"]["EXCEL_URL"]
base_2025 = st.secrets["urls"]["base_2025"]
proyectos = st.secrets["urls"]["proyectos"]
base_ly =  st.secrets["urls"]["base_ly"]
base_ppt = st.secrets["urls"]["base_ppt"]
fecha = st.secrets["urls"]["fecha"]
balance_url = st.secrets["urls"]["balance_url"]
balance_ly = st.secrets["urls"]["balance_ly"]
mapeo_url = st.secrets["urls"]["mapeo_url"]
comparables = 'https://docs.google.com/spreadsheets/d/13eS6lIAxijfkss69OuPHezPxHuOdQUJF50duelc0jZ4/export?format=xlsx'
banace_esgari = st.secrets["balance"]["banace_esgari"]
er_esgari = st.secrets["balance"]["banace_esgari"]


EMPRESAS = ["HOLDING", "FWD", "WH", "UBIKARGA", "EHM", "RESA", "GREEN"]
COLUMNAS_CUENTA = ["Cuenta", "Descripción"]
COLUMNAS_MONTO = ["Saldo final", "Saldo"]
CLASIFICACIONES_PRINCIPALES = ["ACTIVO", "PASIVO", "CAPITAL"]


categorias_felx_com = ['COSTO DE PERSONAL', 'GASTO DE PERSONAL', 'NOMINA ADMINISTRATIVOS']
da = ['AMORT ARRENDAMIENTO', 'AMORTIZACION', 'DEPRECIACION']
meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

@st.cache_data
def cargar_datos(url):
    response = requests.get(url)
    response.raise_for_status()
    archivo_excel = BytesIO(response.content)
    return pd.read_excel(archivo_excel, engine="openpyxl")

@st.cache_data
def extra_beta(ticker):
    ticker = str(ticker).strip().upper()
    url = f"https://www.alphaspread.com/security/nyse/{ticker}/discount-rate"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

            # Método principal
        for beta_div in soup.find_all("div", class_="dotted-underline label pointer tooltip"):
            if "Beta" in beta_div.get_text(strip=True):
                value_div = beta_div.find_previous_sibling("div", class_="value weight-700")
                if value_div:
                    raw = value_div.get_text(strip=True).replace(",", ".").strip()
                    match = re.search(r"-?\d+(\.\d+)?", raw)
                    if match:
                        return float(match.group())

            # Fallback: buscar "Beta" en texto cercano
        html_text = soup.get_text(" ", strip=True)
        match_beta = re.search(r"Beta\s*(-?\d+(\.\d+)?)", html_text, re.IGNORECASE)
        if match_beta:
            return float(match_beta.group(1))

        return None

    except Exception:
        return None


@st.cache_data
def info_balance(ticker, campo):
    ticker = str(ticker).strip().upper()
    url = f"https://www.alphaspread.com/security/nyse/{ticker}/financials/balance-sheet"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        html_text = soup.prettify()

        pattern = rf'"{re.escape(campo)}".*?"text":"([\d\s]+)"'
        match = re.search(pattern, html_text)

        if match:
            return float(match.group(1).replace(" ", ""))

        return 0.0

    except Exception:
        return 0.0


@st.cache_data
def des_beta(ticker, tax):
    beta = extra_beta(ticker)

    # usa solo deuda real, no Total Liabilities & Equity
    debt = (
        info_balance(ticker, "Current Portion of Long-Term Debt")
        + info_balance(ticker, "Short-Term Debt")
        + info_balance(ticker, "Long-Term Debt")
    )

    equity = info_balance(ticker, "Total Equity")

    if beta is None:
        return None

    if equity is None or equity == 0:
        return None

    return beta / (1 + (1 - tax) * (debt / equity))


def mean_beta(com_list):
    betas = []

    for x in com_list:
        if pd.isna(x):
            continue

        x = str(x).strip().upper()
        tax = 0.3 if x == "TRAXIONA" else 0.21
        beta = des_beta(x, tax)

        if beta is not None:
            betas.append(beta)

        time.sleep(1)

    if not betas:
        return None

    return sum(betas) / len(betas)


@st.cache_data
def get_cetes_3y():
    TOKEN = 'eef020dafff1667cc5fb4dc1de10cf314857367cbd5c881511679bb2e7a7433a'
    SERIE_ID = "SF43936"
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{SERIE_ID}/datos/oportuno"
    headers = {"Bmx-Token": TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        return float(data['bmx']['series'][0]['datos'][0]['dato'])
    except (KeyError, IndexError, ValueError, requests.RequestException):
        return None


@st.cache_data
def erp():
    url = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx"

    df = pd.read_excel(
        url,
        sheet_name="ERPs by country",
        skiprows=7
    )

    df.columns = df.columns.astype(str).str.strip()

    erp_col = [c for c in df.columns if "Total Equity Risk Premium" in c][0]

    return df.loc[df["Country"] == "Mexico", erp_col].iloc[0]


@st.cache_data
def cargar_datos_hoja(url, nombre_hoja=None):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    archivo_excel = BytesIO(response.content)
    return pd.read_excel(archivo_excel, engine="openpyxl", sheet_name=nombre_hoja)


def apalancar_beta(beta_des, tax, debt, equity):
    if beta_des is None:
        return None
    if tax is None:
        return None
    if debt is None:
        return None
    if equity is None or equity == 0:
        return None

    beta_des = float(beta_des)
    tax = float(tax)
    debt = float(debt)
    equity = float(equity)

    return beta_des * (1 + (1 - tax) * (debt / equity))

def validar_credenciales(df, username, password):
    usuario_row = df[(df["usuario"] == username) & (df["contraseña"] == password)]
    if not usuario_row.empty:
        fila = usuario_row.iloc[0]
        proyectos = [p.strip() for p in str(fila["proyectos"]).split(",")]
        cecos = [c.strip() for c in str(fila["cecos"]).split(",")]
        return fila["usuario"], fila["rol"], proyectos, cecos
    return None, None, None, None

def filtro_pro(col):
    df_visibles = proyectos[proyectos["proyectos"].astype(str).isin(st.session_state["proyectos"])]
    
    # Mapea nombres a códigos (solo los que tiene acceso)
    nombre_a_codigo = dict(zip(df_visibles["nombre"], df_visibles["proyectos"].astype(str)))

    # Caso especial: si solo tiene acceso a "ESGARI"
    if st.session_state["proyectos"] == ["ESGARI"]:
        opciones = ["ESGARI"] + proyectos["nombre"].tolist()
        proyecto_nombre = col.selectbox("Selecciona un proyecto", opciones)

        if proyecto_nombre == "ESGARI":
            proyecto_codigo = proyectos["proyectos"].astype(str).tolist()  # Accede a todos

        else:
            # Buscar código del nombre elegido
            proyecto_codigo = proyectos[proyectos["nombre"] == proyecto_nombre]["proyectos"].astype(str).values.tolist()
    else:
        # Normal: mostrar solo nombres permitidos
        proyecto_nombre = col.selectbox("Selecciona un proyecto", list(nombre_a_codigo.keys()))
        proyecto_codigo = [nombre_a_codigo[proyecto_nombre]]

    return proyecto_codigo, proyecto_nombre

def filtro_meses(col, df_2025):
    meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
    if selected == "Análisis":
        meses_seleccionado = col.selectbox("Selecciona un mes", meses)
        meses_seleccionado = [meses_seleccionado]
    elif selected == "Mes Corregido" or selected == "Proyeccion":
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.","jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        meses_disponibles = [mes for mes in meses_ordenados if mes in df_2025["Mes_A"].unique()]
        mes_act = meses_disponibles[-1] if meses_disponibles else None
        index_default = meses_disponibles.index(mes_act) if mes_act in meses_disponibles else 0

        mes_seleccionado = col.selectbox("Selecciona un mes", meses_disponibles, index=index_default)
        meses_seleccionado = [mes_seleccionado]
    else:
        meses_seleccionado = col.multiselect("Selecciona un mes", meses, default=[meses[0]])
    return meses_seleccionado

def porcentaje_ingresos(df, meses, pro, codigo_pro):
    if pro == "ESGARI":
        por_ingre = 1
    else:
        df_mes = df[df["Mes_A"].isin(meses)]
        df_ingresos = df_mes[df_mes["Categoria_A"] == "INGRESO"]

        ingreso_total = df_ingresos["Neto_A"].sum()
        df_pro = df_ingresos[df_ingresos["Proyecto_A"].isin(codigo_pro)]
        ingreso_proyecto = df_pro["Neto_A"].sum()
        por_ingre = ingreso_proyecto / ingreso_total if ingreso_total != 0 else 0

    return por_ingre

def ingreso (df, meses, codigo_pro, pro):
    if pro == "ESGARI":
        df_mes = df[df['Mes_A'].isin(meses)]
        df_ingresos = df_mes[df_mes['Categoria_A'] == 'INGRESO']
        ingreso_pro = df_ingresos['Neto_A'].sum()
    else:
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_ingresos = df_pro[df_pro['Categoria_A'] == 'INGRESO']
        ingreso_pro = df_ingresos['Neto_A'].sum()
    return ingreso_pro

def coss(df, meses, codigo_pro, pro, lista_proyectos):
    pat_oh = ["8002", "8003", "8004"]
    if pro == "ESGARI":

        df = df[~df['Proyecto_A'].isin(pat_oh)]
        df_mes = df[df['Mes_A'].isin(meses)]
        df_coss = df_mes[df_mes['Clasificacion_A'] == 'COSS']
        coss_pro = df_coss['Neto_A'].sum()
        mal_clasificados = 0
    
    else:
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_coss = df_pro[df_pro['Clasificacion_A'] == 'COSS']
        coss_pro = df_coss['Neto_A'].sum()
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clasificados = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clasificados = mal_clasificados[mal_clasificados["Clasificacion_A"].isin(["COSS"])]["Neto_A"].sum() * por_ingresos
            coss_pro += mal_clasificados
    return coss_pro, mal_clasificados

def patio(df, meses, codigo_pro, proyecto_nombre):
    df['Proyecto_A'] = df['Proyecto_A'].astype(str)
    patio_t = 0
    for x in meses:
        proyectos_patio = ["3201", "3002", "1003", "2003"]

        df_mes = df[df['Mes_A'].isin([x])]

        if proyecto_nombre == "ESGARI":
            df_patio = df_mes[df_mes['Proyecto_A'] == "8003"]
            df_patio = df_patio[df_patio['Clasificacion_A'].isin(['COSS', 'G.ADMN'])]
            patio_t += df_patio['Neto_A'].sum()
        
        elif any(pro in proyectos_patio for pro in codigo_pro):
            df_patio = df_mes[df_mes['Proyecto_A'] == "8003"]
            df_patio = df_patio[df_patio['Clasificacion_A'].isin(['COSS', 'G.ADMN'])]
            patio = df_patio['Neto_A'].sum()

            ingre_pat = df_mes[df_mes['Proyecto_A'].isin(proyectos_patio)]
            ingre_pat = ingre_pat[ingre_pat['Clasificacion_A'] == 'INGRESO']
            ingre_pat = ingre_pat['Neto_A'].sum()

            ingreso_pro = ingreso(df, [x], codigo_pro, proyecto_nombre)
            por_patio = ingreso_pro / ingre_pat if ingre_pat != 0 else 0
            patio_t += por_patio * patio
        else:
            patio_t += 0
    return patio_t

def gadmn(df, meses, codigo_pro, pro, lista_proyectos):
    pat_oh = ["8002", "8003", "8004"]
    if pro == "ESGARI":
        df = df[~df['Proyecto_A'].isin(pat_oh)]
        df_mes = df[df['Mes_A'].isin(meses)]
        df_gadmn = df_mes[df_mes['Clasificacion_A'] == 'G.ADMN']
        gadmn_pro = df_gadmn['Neto_A'].sum()
        mal_clasificados = 0
    elif pro == "FLEX DEDICADO":
        df = df[~df['Proyecto_A'].isin(pat_oh)]
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_gadmn = df_pro[df_pro['Clasificacion_A'] == 'G.ADMN']
        gadmn_pro = df_gadmn['Neto_A'].sum()
        gadmn_flexs = df_pro[df_pro['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum()*.15
        gadmn_pro = gadmn_pro - gadmn_flexs
        mal_clasificados = 0
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clas = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clas = mal_clas[mal_clas["Clasificacion_A"].isin(["G.ADMN"])]["Neto_A"].sum() * por_ingresos
            gadmn_pro += mal_clas
            mal_clasificados += mal_clas
    elif pro == "FLEX SPOT":
        df = df[~df['Proyecto_A'].isin(pat_oh)]
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_gadmn = df_pro[df_pro['Clasificacion_A'] == 'G.ADMN']
        gadmn_pro = df_gadmn['Neto_A'].sum()
        df_pro_flexd = df_mes[df_mes['Proyecto_A'].isin(["2001"])]
        gadmn_flexd = df_pro_flexd[df_pro_flexd['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum() * .15
        gadmn_pro = gadmn_pro + gadmn_flexd
        mal_clasificados = 0
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clas = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clas = mal_clas[mal_clas["Clasificacion_A"].isin(["G.ADMN"])]["Neto_A"].sum() * por_ingresos
            gadmn_pro += mal_clas
            mal_clasificados += mal_clas
    else:
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_gadmn = df_pro[df_pro['Clasificacion_A'] == 'G.ADMN']
        gadmn_pro = df_gadmn['Neto_A'].sum()
        mal_clasificados = 0
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clas = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clas = mal_clas[mal_clas["Clasificacion_A"].isin(["G.ADMN"])]["Neto_A"].sum() * por_ingresos
            gadmn_pro += mal_clas
            mal_clasificados += mal_clas
    return gadmn_pro, mal_clasificados

def oh(df, meses, codigo_pro, nombre_proyecto):
    oh_pro = 0
    for x in meses:
        oh = ["8002", "8004"]
        df_mes = df[df['Mes_A'].isin([x])]
        por_ingre = porcentaje_ingresos(df, [x], nombre_proyecto, codigo_pro)
        df_oh = df_mes[df_mes['Proyecto_A'].isin(oh)]
        df_oh = df_oh[df_oh['Clasificacion_A'].isin(['COSS', 'G.ADMN'])]
        oh_coss = df_oh['Neto_A'].sum()
        oh_pro += oh_coss * por_ingre
    return oh_pro

def gasto_fin (df, meses, codigo_pro, pro, lista_proyectos):
    if pro == "ESGARI":
        df_mes = df[df['Mes_A'].isin(meses)]
        df_gasto_fin = df_mes[df_mes['Clasificacion_A'] == 'GASTOS FINANCIEROS']
        gasto_fin = df_gasto_fin['Neto_A'].sum()
        mal_clasificados = 0
        oh_gasto_fin = 0
    else:
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_gasto_fin = df_pro[df_pro['Clasificacion_A'] == 'GASTOS FINANCIEROS']
        gasto_fin = df_gasto_fin['Neto_A'].sum()
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clasificados = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clasificados = mal_clasificados[mal_clasificados["Clasificacion_A"].isin(["GASTOS FINANCIEROS"])]["Neto_A"].sum() * por_ingresos
            gasto_fin += mal_clasificados
            oh_gasto_fin = df_mes_x[df_mes_x['Proyecto_A'].isin(["8002", "8003","8004"])]
            oh_gasto_fin = oh_gasto_fin[oh_gasto_fin['Clasificacion_A'].isin(["GASTOS FINANCIEROS"])]
            oh_gasto_fin = oh_gasto_fin['Neto_A'].sum() * por_ingresos
            gasto_fin += oh_gasto_fin

    return gasto_fin, mal_clasificados, oh_gasto_fin

def ingreso_fin (df, meses, codigo_pro, pro, lista_proyectos):
    ing_fin_cat = ["INGRESO POR REVALUACION CAMBIARIA", "INGRESO POR FACTORAJE", "INGRESOS POR INTERESES"]
    if pro == "ESGARI":
        df_mes = df[df['Mes_A'].isin(meses)]
        df_ingreso_fin = df_mes[df_mes['Categoria_A'].isin(ing_fin_cat)]
        ingreso_fin = df_ingreso_fin['Neto_A'].sum()
        mal_clasificados = 0
        oh_ingreso_fin = 0
    else:
        df_mes = df[df['Mes_A'].isin(meses)]
        df_pro = df_mes[df_mes['Proyecto_A'].isin(codigo_pro)]
        df_ingreso_fin = df_pro[df_pro['Categoria_A'].isin(ing_fin_cat)]
        ingreso_fin = df_ingreso_fin['Neto_A'].sum()
        for x in meses:
            por_ingresos = porcentaje_ingresos(df, [x], pro, codigo_pro)
            df_mes_x = df[df["Mes_A"] == x]
            mal_clasificados = df_mes_x[~df_mes_x["Proyecto_A"].isin(lista_proyectos)]
            mal_clasificados = mal_clasificados[mal_clasificados["Categoria_A"].isin(ing_fin_cat)]["Neto_A"].sum() * por_ingresos
            ingreso_fin += mal_clasificados
            oh_ingreso_fin = df_mes_x[df_mes_x['Proyecto_A'].isin(["8002", "8003", "8004"])]
            oh_ingreso_fin = oh_ingreso_fin[oh_ingreso_fin['Categoria_A'].isin(ing_fin_cat)]
            oh_ingreso_fin = oh_ingreso_fin['Neto_A'].sum() * por_ingresos
            ingreso_fin += oh_ingreso_fin


    return ingreso_fin, mal_clasificados, oh_ingreso_fin

def estado_resultado(df_2025, meses_seleccionado, proyecto_nombre, proyecto_codigo, lista_proyectos):
    estado_resultado = {}

    por_ingre = porcentaje_ingresos(df_2025, meses_seleccionado, proyecto_nombre, proyecto_codigo)
    ingreso_proyecto = ingreso(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre)
    coss_pro, mal_coss = coss(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, lista_proyectos)
    patio_pro = patio(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre)
    por_patio = patio_pro / ingreso_proyecto if ingreso_proyecto != 0 else 0
    coss_total = coss_pro + patio_pro
    por_coss = coss_total / ingreso_proyecto if ingreso_proyecto != 0 else 0
    utilidad_bruta = ingreso_proyecto - coss_total
    por_ub = utilidad_bruta / ingreso_proyecto if ingreso_proyecto != 0 else 0
    gadmn_pro, mal_gadmn = gadmn(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, lista_proyectos)
    por_gadmn = gadmn_pro / ingreso_proyecto if ingreso_proyecto != 0 else 0
    utilidad_operativa = utilidad_bruta - gadmn_pro
    por_utilidad_operativa = utilidad_operativa / ingreso_proyecto if ingreso_proyecto != 0 else 0
    oh_pro = oh(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre)
    por_oh = oh_pro / ingreso_proyecto if ingreso_proyecto != 0 else 0
    ebit = utilidad_operativa - oh_pro
    por_ebit = ebit / ingreso_proyecto if ingreso_proyecto != 0 else 0
    gasto_fin_pro, mal_gfin, oh_pro_gfin = gasto_fin(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, lista_proyectos)
    por_gasto_fin = gasto_fin_pro / ingreso_proyecto if ingreso_proyecto != 0 else 0
    ingreso_fin_pro, mal_ifin, oh_pro_ifin = ingreso_fin(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, lista_proyectos)
    por_ingreso_fin = ingreso_fin_pro / ingreso_proyecto if ingreso_proyecto != 0 else 0
    resultado_fin = gasto_fin_pro - ingreso_fin_pro
    por_resultado_fin = resultado_fin / ingreso_proyecto if ingreso_proyecto != 0 else 0
    ebt = ebit - resultado_fin
    por_ebt = ebt / ingreso_proyecto if ingreso_proyecto != 0 else 0

    estado_resultado.update({
        'porcentaje_ingresos': por_ingre,
        'ingreso_proyecto': ingreso_proyecto,
        'coss_pro': coss_pro,
        'mal_coss': mal_coss,
        'patio_pro': patio_pro,
        'por_patio': por_patio,
        'coss_total': coss_total,
        'por_coss': por_coss,
        'utilidad_bruta': utilidad_bruta,
        'por_utilidad_bruta': por_ub,
        'gadmn_pro': gadmn_pro,
        'mal_gadmn': mal_gadmn,
        'por_gadmn': por_gadmn,
        'utilidad_operativa': utilidad_operativa,
        'por_utilidad_operativa': por_utilidad_operativa,
        'oh_pro': oh_pro,
        'por_oh': por_oh,
        'ebit': ebit,
        'por_ebit': por_ebit,
        'gasto_fin_pro': gasto_fin_pro,
        'mal_gfin': mal_gfin,
        'oh_pro_gfin': oh_pro_gfin,
        'por_gasto_fin': por_gasto_fin,
        'ingreso_fin_pro': ingreso_fin_pro,
        'por_ingreso_fin': por_ingreso_fin,
        'mal_ifin': mal_ifin,
        'oh_pro_ifin': oh_pro_ifin,
        'resultado_fin': resultado_fin,
        'por_resultado_fin': por_resultado_fin,
        'ebt': ebt,
        'por_ebt': por_ebt
    })

    return estado_resultado

def descargar_excel(df, nombre_archivo="estado_resultado.xlsx"):
    # Crear un buffer en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Hoja1')
        writer.save()
    datos_excel = output.getvalue()

    # Botón de descarga
    st.download_button(
        label="📥 Descargar en Excel",
        data=datos_excel,
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def tabla_expandible(df, cat, mes, pro, proyecto_nombre, key_prefix, ceco):
    ingreso_total = estado_resultado(df, mes, proyecto_nombre, pro, list_pro).get("ingreso_proyecto", None)
    columnas = ['Cuenta_Nombre_A', 'Categoria_A']

    ingreso_fin = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESOS POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']

    if not isinstance(pro, list):
        pro = [pro]

    # Filtrar y agrupar
    if cat == 'INGRESO':
        df_tabla = df[df['Categoria_A'] == cat]
    elif cat == 'INGRESO FINANCIERO':
        df_tabla = df[df['Categoria_A'].isin(ingreso_fin)]
    else:
        df_tabla = df[df['Clasificacion_A'] == cat]

    df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
    df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
    df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

    # Crear columna numérica para % sobre ingreso
    df_tabla['pct_num'] = df_tabla['Neto_A'] / ingreso_total if ingreso_total else 0.0

    # Preparar tabla para AgGrid
    df_tabla = df_tabla.fillna("")
    df_tabla.reset_index(drop=True, inplace=True)

    gb = GridOptionsBuilder.from_dataframe(df_tabla)
    gb.configure_default_column(groupable=True)
    gb.configure_column("Categoria_A", rowGroup=True, hide=True)

    gb.configure_column(
        "Neto_A",
        aggFunc="sum",
        valueFormatter="`$${value.toLocaleString()}`"
    )

    gb.configure_column(
        "pct_num",
        header_name="% sobre Ingreso",
        type=["numericColumn", "numberColumn"],
        aggFunc="sum",
        valueFormatter="(value != null) ? (value * 100).toFixed(2) + ' %' : ''"
    )

    grid_options = gb.build()

    st.write(f"Tabla {cat}")
    AgGrid(
        df_tabla,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        height=400,
        theme="streamlit",
        key=f"{key_prefix}_aggrid_{cat}_{pro}_{mes}_{ceco}"
    )

    # Exportar a Excel
    output = io.BytesIO()
    df_export = df_tabla.rename(columns={"pct_num": "% sobre Ingreso"})
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_export.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
        output.seek(0)

    st.download_button(
        label=f"Descargar tabla {cat}",
        data=output,
        file_name=f"tabla_{cat}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"{key_prefix}_download_{cat}"
    )


def tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, clasificacion, categoria, titulo):
    st.write(titulo)
    columnas = ['Cuenta_Nombre_A', 'Categoria_A']
    df_agrid = df_agrid[df_agrid[clasificacion] == categoria]
    df_agrid = df_agrid.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
    df_agrid.rename(columns={"Neto_A": f"{tipo_com}"}, inplace=True)
    df_actual = df_2025[df_2025['Mes_A'].isin(meses_seleccionado)]
    df_actual = df_actual[df_actual['Proyecto_A'].isin(proyecto_codigo)]
    df_actual = df_actual[df_actual[clasificacion] == categoria]
    df_actual = df_actual.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
    df_actual.rename(columns={"Neto_A": "YTD"}, inplace=True)
    df_compara = pd.merge(df_agrid, df_actual, on=columnas, how="outer").fillna(0)
    df_compara["Variación % "] = np.where(
        df_compara[f"{tipo_com}"] != 0,
        ((df_compara["YTD"] / df_compara[f"{tipo_com}"]) -1 )* 100  ,
        0
    )
    
    columnas = ['Cuenta_Nombre_A', 'Categoria_A', 'YTD', f"{tipo_com}", "Variación % "]
    df_tabla = df_compara[columnas].copy()
    
    df_last = df_tabla.groupby("Categoria_A").sum().reset_index()
    df_last["Variación % "] = np.where(
        df_last[f"{tipo_com}"] != 0,
        ((df_last["YTD"] / df_last[f"{tipo_com}"]) - 1) * 100,
        0
    )
    df_des = df_tabla.copy()
    df_tabla = pd.concat([df_tabla, df_last], ignore_index=True)

    # Asegurar valores numéricos para formateo
    df_tabla["YTD"] = pd.to_numeric(df_tabla["YTD"], errors="coerce")
    df_tabla[tipo_com] = pd.to_numeric(df_tabla[tipo_com], errors="coerce")
    df_tabla["Variación % "] = pd.to_numeric(df_tabla["Variación % "], errors="coerce")

    # Configurar AgGrid con agrupación
    gb = GridOptionsBuilder.from_dataframe(df_tabla)
    gb.configure_default_column(groupable=True)

    # Agrupar por Categoría
    gb.configure_column("Categoria_A", rowGroup=True, hide=True)

    # Formateo de columnas numéricas
    gb.configure_column("YTD", type=["numericColumn"], aggFunc="last", valueFormatter="`$${value.toLocaleString()}`")
    gb.configure_column(f"{tipo_com}", type=["numericColumn"], aggFunc="last", valueFormatter="`$${value.toLocaleString()}`")
    gb.configure_column(
        "Variación % ",
        header_name="Variación % ",
        type=["numericColumn"],
        aggFunc="last",
        valueFormatter="(value != null) ? value.toFixed(2) + ' %' : ''"
    )

    grid_options = gb.build()

    # Mostrar tabla agrupada
    AgGrid(
        df_tabla,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        height=500,
        use_checkbox=False,
        fit_columns_on_grid_load=True,
        theme="streamlit",
        key=f"agrid_comparativa_{tipo_com}_{proyecto_codigo}_{meses_seleccionado}_{categoria}"
    )

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_des.to_excel(writer, index=False, sheet_name="Comparativa")
        writer.save()

    # Preparar el archivo para descarga
    st.download_button(
        label="📥 Descargar Excel",
        data=buffer.getvalue(),
        file_name=f"comparativa_{tipo_com}_{meses_seleccionado}_{categoria}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # === GRÁFICO DE BARRAS COMPARATIVO POR CATEGORIA_A ===

    # Agrupar por Categoria_A para graficar totales
    df_plot = df_compara.groupby("Categoria_A", as_index=False).agg({
        "YTD": "sum",
        tipo_com: "sum"
    })
    df_plot["Variación % "] = np.where(
        df_plot[tipo_com] != 0,
        ((df_plot["YTD"] / df_plot[tipo_com]) - 1) * 100,
        0
    )

    df_plot = df_plot.sort_values(by="YTD", ascending=False)

    # === GRÁFICO DE BARRAS ===
    fig_barras = go.Figure()

    fig_barras.add_trace(go.Bar(
        x=df_plot["Categoria_A"],
        y=df_plot["YTD"],
        name="YTD",
        marker_color="#003366",
        text=df_plot["YTD"].apply(lambda x: f"${x:,.0f}"),
        textposition="auto"
    ))

    fig_barras.add_trace(go.Bar(
        x=df_plot["Categoria_A"],
        y=df_plot[tipo_com],
        name=tipo_com,
        marker_color="#b0b0b0",
        text=df_plot[tipo_com].apply(lambda x: f"${x:,.0f}"),
        textposition="auto"
    ))

    fig_barras.update_layout(
        title=f"{titulo} - Comparativa YTD vs {tipo_com} por Categoría",
        xaxis_title="Categoría",
        yaxis_title="Monto ($)",
        barmode="group",
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig_barras, use_container_width=True)

    # === GRÁFICO DE VARIACIÓN % ===
    fig_var = px.bar(
        df_plot,
        x="Categoria_A",
        y="Variación % ",
        title=f"{titulo} - Variación % por Categoría (YTD vs {tipo_com})",
        color="Variación % ",
        color_continuous_scale="RdBu_r",
        text=df_plot["Variación % "].apply(lambda x: f"{x:.2f}%"),
        height=400
    )
    fig_var.update_layout(yaxis_title="Variación %", xaxis_title="Categoría", template="plotly_white")
    fig_var.update_traces(textposition='outside')

    st.plotly_chart(fig_var, use_container_width=True)
    
ceco = st.secrets["urls"]["ceco"]
cecos = cargar_datos(ceco)
def filtro_ceco(col):
    cecos["ceco"] = cecos["ceco"].astype(str)
    df_visibles = cecos[cecos["ceco"].isin(st.session_state["cecos"])]
    # Mapea nombres a códigos (solo los que tiene acceso)
    nombre_a_codigo = dict(zip(df_visibles["nombre"], df_visibles["ceco"]))

    if st.session_state["cecos"] == ["ESGARI"]:
        opciones = ["ESGARI"] + cecos["nombre"].tolist()
        ceco_nombre = col.selectbox("Selecciona un ceco", opciones)

        if ceco_nombre == "ESGARI":
            ceco_codigo = cecos["ceco"].tolist()  # Accede a todos

        else:
            ceco_codigo = cecos[cecos["nombre"] == ceco_nombre]["ceco"].values.tolist()
    else:
        ceco_nombre = col.selectbox("Selecciona un ceco", list(nombre_a_codigo.keys()))
        ceco_codigo = [nombre_a_codigo[ceco_nombre]]

    return ceco_codigo, ceco_nombre

def estdo_re(df_2025, ceco):
    col1, col2 = st.columns(2)
    meses_seleccionado = filtro_meses(col1, df_2025)
    proyecto_codigo, proyecto_nombre = filtro_pro(col2)
    codi_ceco , nombre_ceco = filtro_ceco(st)
    df_2025["CeCo_A"] = df_2025["CeCo_A"].astype(str)
    if nombre_ceco != "ESGARI":
        df_2025 = df_2025[df_2025["CeCo_A"].isin(codi_ceco)]
    if not meses_seleccionado:
            st.error("Favor de seleccionar por lo menos un mes")
    else:
        
        er = estado_resultado(df_2025, meses_seleccionado, proyecto_nombre, proyecto_codigo, list_pro)

        if st.session_state['rol'] == "gerente":
                        metricas_seleccionadas = [
                ("Ingreso", "ingreso_proyecto"),
                ("COSS", "coss_pro"),
                ("COSS Patio", "patio_pro"),
                ("COSS Total", "coss_total"),
                ("Utilidad Bruta", "utilidad_bruta"),
                ("G.ADMN", "gadmn_pro"),
                ("Utilidad Operativa", "utilidad_operativa"),
            ]
        
        else:
            metricas_seleccionadas = [
                ("Ingreso", "ingreso_proyecto"),
                ("COSS", "coss_pro"),
                ("COSS Patio", "patio_pro"),
                ("COSS Total", "coss_total"),
                ("Utilidad Bruta", "utilidad_bruta"),
                ("G.ADMN", "gadmn_pro"),
                ("Utilidad Operativa", "utilidad_operativa"),
                ("OH", "oh_pro"),
                ("EBIT", "ebit"),
                ("Gasto Fin", "gasto_fin_pro"),
                ("Ingreso Fin", "ingreso_fin_pro"),
                ("EBT", "ebt"),
            ]

        valor_ingreso = er.get("ingreso_proyecto", None)

        df_data = []
        for nombre_metrica, clave in metricas_seleccionadas:
            valor = er.get(clave, None)
            # Paso 2: calcular % sobre ingreso (evitando división por cero)
            porcentaje_sobre_ingreso = valor / valor_ingreso if valor_ingreso and isinstance(valor, (int, float)) else None
            fila = {
                "Concepto": nombre_metrica,
                "Valor": valor,
                "% sobre Ingreso": 1.0 if clave == "ingreso_proyecto" else porcentaje_sobre_ingreso
            }
            df_data.append(fila)

        df_tabla = pd.DataFrame(df_data)

        # Paso 1: Formatear columnas
        df_tabla["Valor"] = df_tabla["Valor"].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) and isinstance(x, (int, float, float)) else x)
        df_tabla["% sobre Ingreso"] = df_tabla["% sobre Ingreso"].apply(lambda x: f"{x:.2%}" if pd.notnull(x) and isinstance(x, (int, float)) else x)

        # Paso 2: Definir identificador único
        i = 1  # puedes cambiarlo si tienes más tablas en la misma vista

        # Paso 3: Estilo CSS personalizado
        st.markdown(f"""
            <style>
            .tab-table-{i} {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
                font-size: 13px;
                text-align: left;
            }}
            .tab-table-{i} th {{
                background-color: #003366;
                color: white;
                text-transform: uppercase;
                text-align: left;
                padding: 10px;
            }}
            .tab-table-{i} td {{
                padding: 8px;
            }}
            .tab-table-{i} tr:nth-child(1), 
            .tab-table-{i} tr:nth-child(5), 
            .tab-table-{i} tr:nth-child(7),
            .tab-table-{i} tr:nth-child(9),

            .tab-table-{i} tr:nth-child(12) {{
                background-color: #003366;
                color: white;
            }}
            
            .tab-table-{i} tr:nth-child(2),
            .tab-table-{i} tr:nth-child(3),
            .tab-table-{i} tr:nth-child(4),
            .tab-table-{i} tr:nth-child(6),
            .tab-table-{i} tr:nth-child(8),
            .tab-table-{i} tr:nth-child(10),
            .tab-table-{i} tr:nth-child(11),
            .tab-table-{i} tr:nth-child(8) {{
                background-color: white;
                color: black;
            }}
            .tab-table-{i} tr:hover {{
                background-color: #00509E;
                color: white;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Paso 4: Convertir a HTML y mostrar
        html_table = df_tabla.to_html(index=False, escape=False, classes=f"tab-table-{i}")
        st.markdown(html_table, unsafe_allow_html=True)

        descargar_excel(df_tabla, nombre_archivo="estado_resultado.xlsx")

        if st.session_state['rol'] == "director" or st.session_state['rol'] == "admin" :
            ventanas = ['INGRESO', 'COSS', 'G.ADMN', 'GASTOS FINANCIEROS', 'INGRESO FINANCIERO']
            tabs = st.tabs(ventanas)
            with tabs[0]:
                tabla_expandible(df_2025, "INGRESO", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_ingresos", codi_ceco)
            with tabs[1]:
                tabla_expandible(df_2025, "COSS", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_coss", codi_ceco)
            with tabs[2]:
                tabla_expandible(df_2025, "G.ADMN", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_g.admn", codi_ceco)
            with tabs[3]:
                tabla_expandible(df_2025, "GASTOS FINANCIEROS", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_gfin", codi_ceco)
            with tabs[4]:
                tabla_expandible(df_2025, "INGRESO FINANCIERO", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_ifin", codi_ceco)
        else:
            ventanas = ['INGRESO', 'COSS', 'G.ADMN']
            tabs = st.tabs(ventanas)
            with tabs[0]:
                tabla_expandible(df_2025, "INGRESO", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_ingresos", codi_ceco)
            with tabs[1]:
                tabla_expandible(df_2025, "COSS", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_coss", codi_ceco)
            with tabs[2]:
                tabla_expandible(df_2025, "G.ADMN", meses_seleccionado, proyecto_codigo, proyecto_nombre, "estado_resultado_g.admn", codi_ceco)


        # ====== GRAFICOS ======
        df_numerico = pd.DataFrame([
            {
                "Concepto": nombre_metrica,
                "Valor": er.get(clave, 0),
                "% sobre Ingreso": er.get(clave, 0) / valor_ingreso if valor_ingreso else 0
            }
            for nombre_metrica, clave in metricas_seleccionadas
        ])

        # Gráfico de barras horizontal
        fig_bar = px.bar(
            df_numerico,
            x="Valor",
            y="Concepto",
            orientation='h',
            text=df_numerico["% sobre Ingreso"].apply(lambda x: f"{x:.2%}"),
            labels={"Valor": "Monto", "Concepto": "Concepto"},
            title="Estado de Resultado (Monto y % sobre Ingreso)"
        )
        fig_bar.update_traces(marker_color="#00509E", textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        # === TABLA HTML CON MESES COMO COLUMNAS Y FILAS ESTILIZADAS ===
        st.markdown("### Estado de Resultado mensual")

        # Construir tabla
        df_mensual_col = pd.DataFrame()

        for nombre_metrica, clave in metricas_seleccionadas:
            fila = {"Concepto": nombre_metrica}
            for mes in meses_ordenados:
                if mes in df_2025["Mes_A"].unique():
                    er_mes = estado_resultado(df_2025, [mes], proyecto_nombre, proyecto_codigo, list_pro)
                    fila[mes] = er_mes.get(clave, 0)
            df_mensual_col = pd.concat([df_mensual_col, pd.DataFrame([fila])])

        # Guardar copia para descarga
        df_mensual_col_excel = df_mensual_col.copy()

        # Aplicar formato moneda para mostrar
        for mes in meses_ordenados:
            if mes in df_mensual_col.columns:
                df_mensual_col[mes] = df_mensual_col[mes].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "")

        # Identificador de tabla
        i += 1

        # Estilos con filas pintadas
        st.markdown(f"""
            <style>
            .tab-table-{i} {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
                font-size: 13px;
                font-family: Arial, sans-serif;
                text-align: left;
            }}
            .tab-table-{i} th {{
                background-color: #003366;
                color: white;
                padding: 10px;
                text-align: center;
            }}
            .tab-table-{i} td {{
                padding: 8px;
                text-align: center;
                background-color: white;
                color: black;
            }}
            .tab-table-{i} tr:hover {{
                background-color: #f0f0f0;
            }}
            .tab-table-{i} tr:nth-child(1),
            .tab-table-{i} tr:nth-child(5),
            .tab-table-{i} tr:nth-child(7),
            .tab-table-{i} tr:nth-child(9),
            .tab-table-{i} tr:nth-child(12) {{
                background-color: #003366;
                color: white;
            }}
            </style>
        """, unsafe_allow_html=True)

        html_mensual_col = df_mensual_col.to_html(index=False, escape=False, classes=f"tab-table-{i}")
        st.markdown(html_mensual_col, unsafe_allow_html=True)

        descargar_excel(df_mensual_col_excel, nombre_archivo="estado_resultado_mensual.xlsx")

def texto_centrado(texto):
    st.markdown(f"<div style='text-align: center;'>{texto}</div>", unsafe_allow_html=True)

def seccion_analisis_especial_porcentual(df_actual, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, funcion, nombre_funcion):
    with st.expander(f"{nombre_funcion.upper()}"):
        # Ingreso actual
        ingreso_total_actual = ingreso(df_actual, meses_seleccionado, proyecto_codigo, proyecto_nombre)
        valor_actual = funcion(df_actual, meses_seleccionado, proyecto_codigo, proyecto_nombre)
        porcentaje_actual = (valor_actual / ingreso_total_actual * 100) if ingreso_total_actual != 0 else 0

        # Históricos
        df_histo = df_ly if meses_seleccionado[0] in ["ene.", "feb."] else df_actual
        meses_completos = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
        indice = meses_completos.index(meses_seleccionado[0])
        meses_historicos = meses_completos if meses_seleccionado[0] in ["ene.", "feb."] else meses_completos[:indice]

        porcentajes_hist = []
        for mes in meses_historicos:
            ingreso_mensual = ingreso(df_histo, [mes], proyecto_codigo, proyecto_nombre)
            valor_funcion = funcion(df_histo, [mes], proyecto_codigo, proyecto_nombre)
            porcentaje = (valor_funcion / ingreso_mensual * 100) if ingreso_mensual != 0 else 0
            porcentajes_hist.append(porcentaje)

        media = np.mean(porcentajes_hist)
        std = np.std(porcentajes_hist)
        lim_inf = media - std
        lim_sup = media + std

        df_resultado = pd.DataFrame([{
            "Indicador": nombre_funcion.upper(),
            "Media": round(media, 2),
            "Desviación_Estándar": round(std, 2),
            "Limite Inferior": round(lim_inf, 2),
            "Limite Superior": round(lim_sup, 2),
            "Porcentaje Actual": round(porcentaje_actual, 2)
        }])

        def resaltar(row):
            if row["Porcentaje Actual"] > row["Limite Superior"]:
                return ['background-color: red; color: white'] * len(row)
            elif row["Porcentaje Actual"] < row["Limite Inferior"]:
                return ['background-color: yellow; color: black'] * len(row)
            else:
                return [''] * len(row)

        st.dataframe(
            df_resultado.style
                .apply(resaltar, axis=1)
                .format({
                    "Media": "{:.2f} %",
                    "Desviación_Estándar": "{:.2f} %",
                    "Limite Inferior": "{:.2f} %",
                    "Limite Superior": "{:.2f} %",
                    "Porcentaje Actual": "{:.2f} %"
                })
        )

def seccion_analisis_por_clasificacion(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, clasificacion_nombre):
    with st.expander(clasificacion_nombre):
        # Filtrar actuales
        df_actual = df_2025[df_2025['Mes_A'].isin(meses_seleccionado)]
        df_actual = df_actual[df_actual['Proyecto_A'].isin(proyecto_codigo)]
        df_actual_cla = df_actual[df_actual["Categoria_A"] != "INGRESO"]
        df_actual_cla = df_actual_cla.groupby(["Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()
        df_actual_cat = df_actual[df_actual["Categoria_A"] != "INGRESO"]
        df_actual_cat = df_actual_cat.groupby(["Categoria_A", "Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()
        df_actual_cuenta = df_actual[df_actual["Categoria_A"] != "INGRESO"]
        df_actual_cuenta = df_actual_cuenta.groupby(["Categoria_A", "Cuenta_Nombre_A", "Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()

        ingreso_actual = ingreso(df_actual, meses_seleccionado, proyecto_codigo, proyecto_nombre)
        for df in [df_actual_cat, df_actual_cuenta, df_actual_cla]:
            df["Porcentaje %"] = df.apply(
                lambda row: (row["Neto_A"] / ingreso_actual) * 100 if row["Neto_A"] != 0 else 0,
                axis=1
            )

        df_actual_cla = df_actual_cla[df_actual_cla["Clasificacion_A"] == clasificacion_nombre]
        df_actual_cat = df_actual_cat[df_actual_cat["Clasificacion_A"] == clasificacion_nombre]
        df_actual_cuenta = df_actual_cuenta[df_actual_cuenta["Clasificacion_A"] == clasificacion_nombre]

        df_actual_junto = pd.concat([df_actual_cuenta, df_actual_cat], ignore_index=True)
        df_actual_junto = df_actual_junto.drop(columns=["Clasificacion_A", "Mes_A", "Neto_A"]).fillna("vacio")

        # Históricos
        df_histo = df_ly if meses_seleccionado[0] in ["ene.", "feb."] else df_2025
        df_histo = df_histo[df_histo["Proyecto_A"].isin(proyecto_codigo)]
        meses_completos = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
        indice = meses_completos.index(meses_seleccionado[0])
        meses_historicos = meses_completos if meses_seleccionado[0] in ["ene.", "feb."] else meses_completos[:indice]

        ingreso_meses = {x: ingreso(df_histo, [x], proyecto_codigo, proyecto_nombre) for x in meses_historicos}

        df_histo = df_histo[df_histo["Categoria_A"] != "INGRESO"]
        df_histo_cuenta = df_histo.groupby(["Categoria_A", "Cuenta_Nombre_A", "Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()
        df_histo_categoria = df_histo.groupby(["Categoria_A", "Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()
        df_histo_cla = df_histo.groupby(["Clasificacion_A", "Mes_A"], as_index=False)["Neto_A"].sum()
        
        for df in [df_histo_cla, df_histo_categoria, df_histo_cuenta]:
            df["Ingreso_Asociado"] = df["Mes_A"].map(ingreso_meses)
            df["Porcentaje %"] = df.apply(
                lambda row: (row["Neto_A"] / row["Ingreso_Asociado"]) * 100 if row["Ingreso_Asociado"] not in [0, None] else 0,
                axis=1
            )
        df_histo_cla = df_histo_cla.groupby("Clasificacion_A").agg(Media=("Porcentaje %", 'mean'), Desviación_Estándar=("Porcentaje %", 'std')).reset_index()
        df_histo_cla = df_histo_cla[df_histo_cla["Clasificacion_A"] == clasificacion_nombre]
        df_histo_cla["Limite Inferior"] = df_histo_cla["Media"] - df_histo_cla["Desviación_Estándar"]
        df_histo_cla["Limite Superior"] = df_histo_cla["Media"] + df_histo_cla["Desviación_Estándar"]

        df_histo_categoria = df_histo_categoria.groupby(['Categoria_A','Clasificacion_A']).agg(Media=("Porcentaje %", 'mean'), Desviación_Estándar=("Porcentaje %", 'std')).reset_index()
        df_histo_cuenta = df_histo_cuenta.groupby(["Cuenta_Nombre_A", 'Categoria_A','Clasificacion_A']).agg(Media=("Porcentaje %", 'mean'), Desviación_Estándar=("Porcentaje %", 'std')).reset_index()

        df_analisis_junto = pd.concat([df_histo_cuenta, df_histo_categoria], ignore_index=True)
        df_analisis_junto["Limite Inferior"] = df_analisis_junto["Media"] - df_analisis_junto["Desviación_Estándar"]
        df_analisis_junto["Limite Superior"] = df_analisis_junto["Media"] + df_analisis_junto["Desviación_Estándar"]
        df_analisis_junto = df_analisis_junto[df_analisis_junto["Clasificacion_A"] == clasificacion_nombre].drop(columns=["Clasificacion_A"]).fillna("vacio")

        df_analsiis_com = pd.merge(df_analisis_junto, df_actual_junto, on=["Categoria_A", "Cuenta_Nombre_A"], how="left")
        df_actual_cla = df_actual_cla.drop(columns=["Mes_A", "Neto_A"])
        df_analsiis_cla = pd.merge(df_histo_cla, df_actual_cla, on=["Clasificacion_A"], how="left")

        df_analsiis_cla[["Media", "Desviación_Estándar", "Limite Inferior", "Limite Superior", "Porcentaje %"]] = (
            df_analsiis_cla[["Media", "Desviación_Estándar", "Limite Inferior", "Limite Superior", "Porcentaje %"]].fillna(0).round(2)
        )

        def resaltar_clasificacion(row):
            if row["Porcentaje %"] > row["Limite Superior"]:
                return ['background-color: red; color: white'] * len(row)
            elif row["Porcentaje %"] < row["Limite Inferior"]:
                return ['background-color: yellow; color: black'] * len(row)
            else:
                return [''] * len(row)

        df_analsiis_cla = df_analsiis_cla.set_index("Clasificacion_A")

        st.dataframe(
            df_analsiis_cla.style
            .apply(resaltar_clasificacion, axis=1)
            .format({
                "Media": "{:.2f} %",
                "Desviación_Estándar": "{:.2f} %",
                "Limite Inferior": "{:.2f} %",
                "Limite Superior": "{:.2f} %",
                "Porcentaje %": "{:.2f} %"
            })
        )

        df_analsiis_com["Porcentaje %"] = df_analsiis_com["Porcentaje %"].fillna(0)
        df_analsiis_com["Cuenta_Nombre_A"] = df_analsiis_com["Cuenta_Nombre_A"].replace("vacio", np.nan)
        df_analsiis_com = df_analsiis_com.replace("vacio", 0)

        columnas_ordenadas = ["Categoria_A", "Cuenta_Nombre_A", "Media", "Desviación_Estándar", "Limite Inferior", "Limite Superior", "Porcentaje %"]
        df_analsiis_com = df_analsiis_com[columnas_ordenadas]

        row_style_js = JsCode("""
        function(params) {
            if (params.node.group) {
                const valor = params.node.aggData["Porcentaje %"];
                const limSup = params.node.aggData["Limite Superior"];
                const limInf = params.node.aggData["Limite Inferior"];
                if (valor != null && limSup != null && limInf != null) {
                    if (valor > limSup) return { backgroundColor: 'red', color: 'white' };
                    else if (valor < limInf) return { backgroundColor: 'yellow', color: 'black' };
                }
            }
            if (params.data) {
                const valor = params.data["Porcentaje %"];
                const limSup = params.data["Limite Superior"];
                const limInf = params.data["Limite Inferior"];
                if (valor != null && limSup != null && limInf != null) {
                    if (valor > limSup) return { backgroundColor: 'red', color: 'white' };
                    else if (valor < limInf) return { backgroundColor: 'yellow', color: 'black' };
                }
            }
            return null;
        }
        """)

        gb = GridOptionsBuilder.from_dataframe(df_analsiis_com)
        gb.configure_default_column(groupable=True)
        gb.configure_column("Categoria_A", rowGroup=True, hide=True)
        gb.configure_grid_options(getRowStyle=row_style_js)
        formatter = "value != null ? value.toFixed(2) + ' %' : ''"
        for col in ["Porcentaje %", "Media", "Desviación_Estándar", "Limite Inferior", "Limite Superior"]:
            gb.configure_column(col, type=["numericColumn"], aggFunc="last", valueFormatter=formatter)

        grid_options = gb.build()
        meses_key = "-".join(sorted(meses_seleccionado))
        grid_key = f"agrid_comparativa_{proyecto_codigo}_{meses_key}_{clasificacion_nombre}"
        AgGrid(
            df_analsiis_com,
            gridOptions=grid_options,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            height=500,
            use_checkbox=False,
            fit_columns_on_grid_load=True,
            theme="streamlit",
            key=grid_key,
        )

def mostrar_tabla_estilizada(df, id=1):
    df_tabla = df.copy()

    # Formato condicional para celdas con $ y %
    df_tabla["Valor"] = df_tabla["Valor"].apply(
        lambda x: f"${float(x.replace('$','').replace(',','')):,.2f}" if "$" in x else x
    )
    df_tabla["Valor"] = df_tabla["Valor"].apply(
        lambda x: f'<span style="color:#003366;">{x}</span>' if "%" in x else x
    )

    # CSS personalizado
    st.markdown(f"""
        <style>
        .tab-table-{id} {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 13px;
            text-align: left;
            border: 1px solid #ccc;
            font-family: sans-serif;
        }}
        .tab-table-{id} th {{
            background-color: #003366;
            color: white;
            text-transform: uppercase;
            text-align: left;
            padding: 10px;
        }}
        .tab-table-{id} td {{
            padding: 8px;
            background-color: white;
            color: black;
        }}
        .tab-table-{id} tr:nth-child(5) td,
        .tab-table-{id} tr:nth-child(10) td {{
            background-color: #003366 !important;
            color: white !important;
            font-weight: bold;
        }}
        .tab-table-{id} tr:nth-child(5) td span,
        .tab-table-{id} tr:nth-child(10) td span {{
            color: white !important;
        }}
        .tab-table-{id} tr td:nth-child(2):has(span) {{
            color: #003366;
            font-weight: bold;
        }}
        .tab-table-{id} tr:hover {{
            background-color: #00509E;
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)

    html_table = df_tabla.to_html(index=False, escape=False, classes=f"tab-table-{id}")
    st.markdown(html_table, unsafe_allow_html=True)
    descargar_excel(df, nombre_archivo=f"proyeccion{id}.xlsx")

def proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro_ori, gadmn_pro_ori, oh_pct_elegido=None):
    variable = df_ext_var["Neto_normalizado"].sum()
    fijos_uo = df_sum[df_sum["Clasificacion_A"].isin(["G.ADMN", "COSS"])]["Neto_A"].sum() + patio_pro

    # OH como porcentaje
    oh_pct = (oh_pct_elegido / 100.0) if oh_pct_elegido is not None else 0.0

    # 👇 Nuevos cálculos de ingreso objetivo según tipo de OH
    ingreso_uo_24 = fijos_uo / (1 - variable - 0.25)  # No cambia

    if oh_pct_elegido is not None:
        ingreso_ebt_0 = (fijos_uo + intereses) / (1 - variable - oh_pct)
        ingreso_ebt_115 = (fijos_uo + intereses) / (1 - variable - 0.115 - oh_pct)
    else:
        fijos_ebt = fijos_uo + oh_pro + intereses
        ingreso_ebt_0 = fijos_ebt / (1 - variable)
        ingreso_ebt_115 = fijos_ebt / (1 - variable - 0.115)

    def calcular_oh_dinamico(ingreso_obj):
        if oh_pct_elegido is not None:
            return ingreso_obj * oh_pct
        return oh_pro

    def construir_tabla(ingreso_obj, coss, gadm, oh, interes, id_tab):
        utilidad_op = ingreso_obj - coss - gadm
        por_util_op = utilidad_op / ingreso_obj if ingreso_obj else 0
        ebit = utilidad_op - oh
        ebt = ebit - interes
        por_ebt = ebt / ingreso_obj if ingreso_obj else 0
        delta = (ingreso_obj - ingreso_pro_fut) / ingreso_pro_fut if ingreso_pro_fut else 0

        resumen_df = pd.DataFrame({
            "Concepto": [
                "Ingresos Proyectados",
                "COSS",
                "Gastos Administrativos",
                "Utilidad Operativa",
                "% Utilidad Operativa",
                "OH",
                "EBIT",
                "Intereses",
                "EBT",
                "% EBT",
                "Δ Ingreso %"
            ],
            "Valor": [
                f"${ingreso_obj:,.2f}",
                f"${coss:,.2f}",
                f"${gadm:,.2f}",
                f"${utilidad_op:,.2f}",
                f"{por_util_op:.2%}",
                f"${oh:,.2f}",
                f"${ebit:,.2f}",
                f"${interes:,.2f}",
                f"${ebt:,.2f}",
                f"{por_ebt:.2%}",
                f"{delta:.2%}"
            ]
        })

        if st.session_state["rol"] == "gerente":
            resumen_df = resumen_df[~resumen_df["Concepto"].isin(["OH", "EBIT", "Intereses", "% EBT", "EBT"])]

        mostrar_tabla_estilizada(resumen_df, id=id_tab)

        valores_bar = [ingreso_obj, coss, gadm, utilidad_op]
        if st.session_state["rol"] != "gerente":
            valores_bar.append(ebt)

        st.bar_chart(pd.DataFrame({
            "Valor ($)": valores_bar,
        }, index=["Ingresos", "COSS", "GADM", "Util. Operativa"] + ([] if st.session_state["rol"] == "gerente" else ["EBT"])))

        if oh_pct_elegido is not None:
            st.caption(f"OH calculado como {oh_pct_elegido:.2f}% del ingreso")

    # 🧩 Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Proyeccion",
        "Utilidad  Minima Esperada (Punto de Equilibrio)",
        "Ingreso Manual",
        "Utilidad esperada",
        "Utilidad Operativa Objetivo (25%)"
    ])

    # Tab: UO = 25%
    with tab5:
        df_ext_var_24 = df_ext_var.copy()
        df_ext_var_24["Neto_A"] = df_ext_var_24["Neto_normalizado"] * ingreso_uo_24
        df_ext_var_24 = df_ext_var_24.drop(columns=["Neto_normalizado"])
        df_junto = pd.concat([df_ext_var_24, df_sum], ignore_index=True)
        coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
        gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()
        nuevo_oh = calcular_oh_dinamico(ingreso_uo_24)
        st.write(f"Ingreso necesario para U. Operativa = 25%: **${ingreso_uo_24:,.2f}**")
        construir_tabla(ingreso_uo_24, coss_pro, gadmn_pro, nuevo_oh, intereses, id_tab=1)

    # Tab: EBT = 0
    with tab2:
        df_ext_var_0 = df_ext_var.copy()
        df_ext_var_0["Neto_A"] = df_ext_var_0["Neto_normalizado"] * ingreso_ebt_0
        df_ext_var_0 = df_ext_var_0.drop(columns=["Neto_normalizado"])
        df_junto = pd.concat([df_ext_var_0, df_sum], ignore_index=True)
        coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
        gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()
        nuevo_oh = calcular_oh_dinamico(ingreso_ebt_0)
        st.write(f"Ingreso necesario para alcanzar Punto de Equilibrio: **${ingreso_ebt_0:,.2f}**")
        construir_tabla(ingreso_ebt_0, coss_pro, gadmn_pro, nuevo_oh, intereses, id_tab=2)

    # Tab: Ingreso manual
    with tab3:
        ingreso_manual = st.number_input("💰 Ingreso Manual", value=float(ingreso_pro_fut), step=500000.0, format="%.2f")
        df_ext_var_manual = df_ext_var.copy()
        df_ext_var_manual["Neto_A"] = df_ext_var_manual["Neto_normalizado"] * ingreso_manual
        df_ext_var_manual = df_ext_var_manual.drop(columns=["Neto_normalizado"])
        df_junto = pd.concat([df_ext_var_manual, df_sum], ignore_index=True)
        coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
        gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()
        nuevo_oh = calcular_oh_dinamico(ingreso_manual)
        construir_tabla(ingreso_manual, coss_pro, gadmn_pro, nuevo_oh, intereses, id_tab=3)

    # Tab: EBT = 11.5%
    with tab4:
        df_ext_var_115 = df_ext_var.copy()
        df_ext_var_115["Neto_A"] = df_ext_var_115["Neto_normalizado"] * ingreso_ebt_115
        df_ext_var_115 = df_ext_var_115.drop(columns=["Neto_normalizado"])
        df_junto = pd.concat([df_ext_var_115, df_sum], ignore_index=True)
        coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
        gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()
        nuevo_oh = calcular_oh_dinamico(ingreso_ebt_115)
        st.write(f"Ingreso necesario para Utilidad Esperada (EBT 11.5%): **${ingreso_ebt_115:,.2f}**")
        construir_tabla(ingreso_ebt_115, coss_pro, gadmn_pro, nuevo_oh, intereses, id_tab=4)

    # Tab: Original
    with tab1:
        st.write("Proyección Original")
        construir_tabla(ingreso_pro_fut, coss_pro_ori, gadmn_pro_ori, oh_pro, intereses, id_tab=5)
def limpiar_cuenta(x):
    """Convierte cuenta a int, quitando comas/espacios/texto (ej: '400,000,006' -> 400000006)."""
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if s.endswith(".0"):
        s = s[:-2]

    s = re.sub(r"[^\d-]", "", s)

    if s == "" or s == "-":
        return pd.NA

    try:
        return int(s)
    except:
        return pd.NA


def _encontrar_columna(df, candidatos):
    return next((c for c in candidatos if c in df.columns), None)

def _to_numeric_money(series):
    s = series.astype(str).replace(r"[\$,]", "", regex=True)
    return pd.to_numeric(s, errors="coerce").fillna(0)

@st.cache_data(show_spinner="Cargando Excel (URL)...")
def load_excel_from_url(url: str) -> pd.DataFrame:
    r = requests.get(url)
    r.raise_for_status()
    file = BytesIO(r.content)
    df = pd.read_excel(file, engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data(show_spinner="Cargando mapeo de cuentas...")
def cargar_mapeo(url: str) -> pd.DataFrame:
    df_mapeo = load_excel_from_url(url)
    if "Cuenta" not in df_mapeo.columns:
        st.error("❌ El mapeo debe contener una columna llamada 'Cuenta'.")
        return pd.DataFrame()

    df_mapeo["Cuenta"] = df_mapeo["Cuenta"].apply(limpiar_cuenta)
    df_mapeo = df_mapeo.dropna(subset=["Cuenta"]).drop_duplicates(subset=["Cuenta"], keep="first")
    return df_mapeo

@st.cache_data(show_spinner="Cargando hojas del balance...")
def cargar_balance_multi_hojas(url: str, hojas: list[str]) -> dict[str, pd.DataFrame]:
    r = requests.get(url)
    r.raise_for_status()
    file = BytesIO(r.content)

    data = {}
    for hoja in hojas:
        try:
            file.seek(0)  
            df = pd.read_excel(file, sheet_name=hoja, engine="openpyxl")
            df.columns = df.columns.str.strip()
            data[hoja] = df
        except Exception as e:
            data[hoja] = pd.DataFrame()
            st.warning(f"⚠️ No se pudo leer la hoja {hoja}: {e}")
    return data


def autoclasificar_resultados(df_merged, col_cuenta):
    """
    Si no viene en mapeo:
    400,000,000 a 499,999,999  -> RESULTADOS / INGRESO
    >= 500,000,000             -> RESULTADOS / GASTO
    """

    df_merged[col_cuenta] = pd.to_numeric(df_merged[col_cuenta], errors="coerce")
    mask_no_map = df_merged["CLASIFICACION"].isna()
    mask_ing = mask_no_map & (df_merged[col_cuenta] >= 400000000) & (df_merged[col_cuenta] < 500000000)
    mask_gas = mask_no_map & (df_merged[col_cuenta] >= 500000000)
    df_merged.loc[mask_ing, "CLASIFICACION"] = "RESULTADOS"
    df_merged.loc[mask_ing, "CATEGORIA"] = "INGRESO"
    df_merged.loc[mask_gas, "CLASIFICACION"] = "RESULTADOS"
    df_merged.loc[mask_gas, "CATEGORIA"] = "GASTO"

    return df_merged

# Cálculos de capital
com = cargar_datos(comparables)
com_list = (
    com["ticket"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .tolist()
)

com = com.set_index("empresa")
beta_pro = mean_beta(com_list)

if beta_pro is None:
    st.error("No se pudo calcular la beta promedio de los comparables.")
    st.stop()

erp_mex = erp()

risk_free_raw = get_cetes_3y()
if risk_free_raw is None:
    st.error("No se pudo obtener CETES a 3 años.")
    st.stop()

risk_free = risk_free_raw / 100
tiie_spread = risk_free + 0.05

df_balance = cargar_datos_hoja(banace_esgari, "2025")
df_balance["NETO 2025"] = df_balance["NETO 2025"] * 1000
df_balance["NETO 2024"] = df_balance["NETO 2024"] * 1000

df_er = cargar_datos_hoja(banace_esgari, "P&l")
df_er["Monto"] = df_er["Monto"]

deuda = (
    df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2025"].values[0]
    + df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2025"].values[0]
    + df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2025"].values[0]
    + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2025"].values[0]
)

equity = df_balance[df_balance["CUENTA"] == "Total Capital Contable"]["NETO 2025"].values[0]
cash = df_balance[df_balance["CUENTA"] == "Bancos"]["NETO 2025"].values[0]
deuda_neta = deuda - cash

beta_esg = apalancar_beta(beta_pro, 0.3, deuda, equity)
if beta_esg is None:
    st.error("No se pudo calcular la beta apalancada.")
    st.stop()

eq = risk_free + (beta_esg * erp_mex)
co_de = 0.1268
kd = co_de * (1 - 0.3)

if (deuda_neta + equity) == 0:
    st.error("La suma de deuda neta y equity es 0, no se puede calcular WACC.")
    st.stop()

wacc = (deuda_neta / (deuda_neta + equity)) * kd + (equity / (deuda_neta + equity)) * eq
debt_weight = deuda_neta / (deuda_neta + equity)


init_session_state()
# App principal
df_usuarios = cargar_datos(EXCEL_URL)

if not st.session_state["logged_in"]:

    st.title("🔐 Inicio de Sesión ESGARI 360")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            user, rol, proyectos_user, cecos_user = validar_credenciales(
                df_usuarios,
                username,
                password
            )

            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user
                st.session_state["rol"] = rol
                st.session_state["proyectos"] = proyectos_user
                st.session_state["cecos"] = cecos_user
                st.success("¡Inicio de sesión exitoso!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

else:

    df_2025 = cargar_datos(base_2025)
    df_2025 = (
        df_2025
        .groupby([
            "Mes_A", "Empresa_A", "CeCo_A", "Proyecto_A", "Cuenta_A",
            "Clasificacion_A", "Cuenta_Nombre_A", "Categoria_A"
        ], as_index=False)["Neto_A"]
        .sum()
    )

    df_ly = cargar_datos(base_ly)
    df_ly = (
        df_ly
        .groupby([
            "Mes_A", "Empresa_A", "CeCo_A", "Proyecto_A", "Cuenta_A",
            "Clasificacion_A", "Cuenta_Nombre_A", "Categoria_A"
        ], as_index=False)["Neto_A"]
        .sum()
    )

    df_ppt = cargar_datos(base_ppt)
    df_ppt = (
        df_ppt
        .groupby([
            "Mes_A", "Empresa_A", "CeCo_A", "Proyecto_A", "Cuenta_A",
            "Clasificacion_A", "Cuenta_Nombre_A", "Categoria_A"
        ], as_index=False)["Neto_A"]
        .sum()
    )

    proyectos = cargar_datos(proyectos)
    fecha_actualizacion = cargar_datos(fecha)

    df_2025["Proyecto_A"] = df_2025["Proyecto_A"].astype(str).str.strip()
    df_ly["Proyecto_A"] = df_ly["Proyecto_A"].astype(str).str.strip()
    df_ppt["Proyecto_A"] = df_ppt["Proyecto_A"].astype(str).str.strip()
    proyectos["proyectos"] = proyectos["proyectos"].astype(str).str.strip()

    list_pro = proyectos["proyectos"].tolist()

    with st.sidebar:

        st.markdown("## Menú Principal")

        if st.session_state["rol"] == "admin":
            menu_principal = option_menu(
                None,
                options=["General", "Empresas", "Análisis"],
                icons=["bar-chart", "building", "gear"],
                default_index=0,
            )
        else:
            menu_principal = option_menu(
                None,
                options=["General"],
                icons=["bar-chart"],
                default_index=0,
            )

        st.markdown("---")

        if st.button("Cerrar sesión"):
            for key in ["logged_in", "username", "rol", "proyectos", "cecos"]:
                st.session_state[key] = "" if key != "logged_in" else False
            st.rerun()

        if st.session_state["rol"] == "admin":
            if st.button("🔄 Recargar datos"):
                st.cache_data.clear()
                st.rerun()

        if st.session_state["username"] in ["gonza", "Octavio", "Karla", "Fernanda"]:

            link_360 = "https://drive.google.com/file/d/1bQnGjeBD6ONI3x7ovhEwNl4F-QXa8GSV/view?usp=sharing"

            def get_direct_link(shareable_link):
                file_id = shareable_link.split("/d/")[1].split("/")[0]
                return f"https://drive.google.com/uc?id={file_id}"

            excel_360 = get_direct_link(link_360)

            @st.cache_data
            def download_file_from_drive(url):
                response = requests.get(url)
                if response.status_code == 200:
                    return response.content
                else:
                    st.error("Error al descargar el archivo.")
                    return None

            def create_download_buttons():
                files = {
                    "Excel P&L 360.xlsm": excel_360,
                }

                for file_name, file_url in files.items():
                    file_data = download_file_from_drive(file_url)

                    if file_data:
                        st.download_button(
                            label=f"Descargar {file_name}",
                            data=file_data,
                            file_name=file_name,
                            mime="application/vnd.ms-excel.sheet.macroEnabled.12",
                        )

            create_download_buttons()

    ct("ESGARI 360")

    fecha_act = fecha_actualizacion["fecha"].iloc[0]

    meses_fecha = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    fecha_texto = f"{fecha_act.day} de {meses_fecha[fecha_act.month]} de {fecha_act.year}"
    texto_centrado(f"Fecha de actualización: {fecha_texto}")

    selected = None

    if menu_principal == "General":

        if st.session_state["rol"] in ["director", "admin"] and "ESGARI" in st.session_state["proyectos"]:

            selected = option_menu(
                menu_title=None,
                options=[
                    "Resumen", "Estado de Resultado", "Comparativa", "Análisis",
                    "Proyeccion", "Meses", "Meses LY/PPT",
                    "CeCo", "Ratios", "Dashboard", "OH"
                ],
                icons=[
                    "house",
                    "clipboard-data",
                    "file-earmark-bar-graph",
                    "bar-chart",
                    "building",
                    "calendar",
                    "clock-history",
                    "person-gear",
                    "percent",
                    "speedometer",
                    "briefcase",
                ],
                default_index=0,
                orientation="horizontal",
            )

        elif st.session_state["rol"] == "director" or st.session_state["rol"] == "admin":

            selected = option_menu(
                menu_title=None,
                options=[
                    "Estado de Resultado", "Comparativa", "Análisis",
                    "Proyeccion", "Meses",
                    "Meses LY/PPT", "CeCo", "Ratios", "Dashboard", "OH"
                ],
                icons=[
                    "clipboard-data",
                    "file-earmark-bar-graph",
                    "bar-chart",
                    "building",
                    "calendar",
                    "clock-history",
                    "person-gear",
                    "percent",
                    "speedometer",
                    "briefcase",
                ],
                default_index=0,
                orientation="horizontal",
            )

        elif st.session_state["rol"] == "gerente":

            selected = option_menu(
                menu_title=None,
                options=[
                    "Estado de Resultado", "Comparativa", "Análisis",
                    "Proyeccion", "Meses", "Meses LY/PPT", "CeCo", "Dashboard"
                ],
                icons=[
                    "clipboard-data",
                    "file-earmark-bar-graph",
                    "bar-chart",
                    "building",
                    "calendar",
                    "clock-history",
                    "person-gear",
                    "speedometer"
                ],
                default_index=0,
                orientation="horizontal",
            )

        elif st.session_state["rol"] == "ceco":

            selected = option_menu(
                menu_title=None,
                options=["CeCo"],
                icons=["person-gear"],
                default_index=0,
                orientation="horizontal",
            )

    elif menu_principal == "Empresas":

        selected = option_menu(
            menu_title=None,
            options=[
                "Balance General",
                "Balance por empresa",
                "E.R por empresa",
                "Escenario EDR"
            ],
            icons=[
                "journal-text",
                "building",
                "clipboard-data",
                "sliders"
            ],
            default_index=0,
            orientation="horizontal",
        )

    elif menu_principal == "Análisis":

        selected = option_menu(
            menu_title=None,
            options=[
                "WACC",
                "Balance",
                "Análisis ratios",
                "E. Resultados",
                "Flujo de efectivo",
                "Ratios",
                "Dupont"
            ],
            icons=[
                "cash-coin",
                "journal-text",
                "percent",
                "clipboard-data",
                "graph-up-arrow",
                "speedometer",
                "diagram-3"
            ],
            default_index=0,
            orientation="horizontal",
        )

        if selected == "WACC":

            selected = option_menu(
                menu_title=None,
                options=[
                    "WACC",
                    "Costo de capital",
                    "Deuda"
                ],
                icons=[
                    "graph-up-arrow",
                    "percent",
                    "bank"
                ],
                default_index=0,
                orientation="horizontal",
            )

    if selected == "Resumen":
        
        st.title("Resumen")
        meses_seleccionado = filtro_meses(st, df_2025)
        if not meses_seleccionado:
            st.error("Favor de seleccionar por lo menos un mes")
        else:
            # Estado de resultado para cada proyecto
            resumen_proyectos = {
                nombre: estado_resultado(df_2025, meses_seleccionado, nombre, [codigo], list_pro)
                for nombre, codigo in zip(proyectos["nombre"], proyectos["proyectos"].astype(str))
                if nombre not in {"OFICINAS LUNA", "PATIO", "OFICINAS ANDARES"}
            }

            # ESGARI con todos los proyectos
            codigos = proyectos["proyectos"].astype(str).tolist()
            resumen_esgari = estado_resultado(df_2025, meses_seleccionado, "ESGARI", codigos, list_pro)
            resumen_proyectos["ESGARI"] = resumen_esgari

            # Proyectos deseadas
            metricas_seleccionadas = [
                ("Ingreso", "ingreso_proyecto"),
                ("COSS Total", "coss_total"),
                ("Utilidad Bruta", "utilidad_bruta"),
                ("Margen U.B. %", "por_utilidad_bruta"),
                ("G.ADMN", "gadmn_pro"),
                ("Utilidad Operativa", "utilidad_operativa"),
                ("Margen U.O. %", "por_utilidad_operativa"),
                ("OH", "oh_pro"),
                ("EBIT", "ebit"),
                ("Margen EBIT %", "por_ebit"),
                ("Gasto Fin", "gasto_fin_pro"),
                ("Ingreso Fin", "ingreso_fin_pro"),
                ("EBT", "ebt"),
                ("Margen EBT %", "por_ebt"),
            ]

            # Construir DataFrame base
            df_data = []
            for nombre_metrica, clave in metricas_seleccionadas:
                fila = {"Proyecto": nombre_metrica}
                for proyecto, datos in resumen_proyectos.items():
                    valor = datos.get(clave, None)
                    fila[proyecto] = valor
                df_data.append(fila)

            df_tabla = pd.DataFrame(df_data)

            # --- Formato de celdas ---
            def formatear_pesos(valor):
                try:
                    return f"${valor:,.0f}"
                except Exception:
                    return valor

            def formatear_porcentaje(valor):
                try:
                    return f"{valor * 100:.2f}%"
                except Exception:
                    return valor

            # --- Aplicar formato por fila ---
            filas_porcentaje = [
                "Margen U.B. %",
                "Margen U.O. %",
                "Margen EBIT %",
                "Margen EBT %",
            ]

            def aplicar_formato_personalizado(fila):
                if fila["Proyecto"] in filas_porcentaje:
                    return fila.apply(formatear_porcentaje)
                else:
                    return fila.apply(formatear_pesos)

            df_formateado = df_tabla.apply(aplicar_formato_personalizado, axis=1)

            # --- Estilo visual ---
            def generar_tabla_con_estilo(df):
                filas_destacadas = filas_porcentaje

                def aplicar_estilos(data):
                    estilos = pd.DataFrame('', index=data.index, columns=data.columns)
                    for i, row in data.iterrows():
                        if row["Proyecto"] in filas_destacadas:
                            estilos.loc[i, :] = 'background-color: #00112B; color: white;'
                        else:
                            estilos.loc[i, :] = (
                                'background-color: white; color: black;'
                                if i % 2 == 0 else
                                'background-color: #f2f2f2; color: black;'
                            )
                    return estilos

                estilos_header = [
                    {'selector': 'thead th', 'props': 'background-color: #00112B; color: white; font-weight: bold; font-size: 14px;'}
                ]

                html = (
                    df.style
                    .apply(aplicar_estilos, axis=None)
                    .set_table_styles(estilos_header)
                    .set_properties(**{'font-size': '12px', 'text-align': 'right'})
                    .hide(axis='index')
                    .render()
                )

                # Hacer la tabla responsive con CSS
                responsive_html = f'<div style="overflow-x: auto; width: 100%;">{html}</div>'

                return responsive_html

            # Mostrar tabla
            tabla_html = generar_tabla_con_estilo(df_formateado)
            
            st.markdown(tabla_html, unsafe_allow_html=True)

            # --- Exportar a Excel (sin estilo visual, solo datos limpios) ---

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_tabla.to_excel(writer, index=False, sheet_name="Resumen")
            output.seek(0)
            st.download_button(
                label="📥 Descargar Excel",
                data=output,
                file_name="resumen_estado_resultado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.subheader("📊 Análisis Visual del Estado de Resultados por Proyecto")
            # --- Filtro de proyecto ---
            proyectos_disponibles = [col for col in df_tabla.columns if col != "Proyecto"]
            proyecto_default = "ESGARI" if "ESGARI" in proyectos_disponibles else proyectos_disponibles[0]
            proyecto_seleccionado = st.selectbox("Selecciona un proyecto para visualizar:", proyectos_disponibles, index=proyectos_disponibles.index(proyecto_default))

            # --- Convertir a formato largo para graficar ---
            df_limpio = df_tabla.set_index("Proyecto").T.reset_index().rename(columns={"index": "Proyecto"})
            df_limpio = df_limpio.dropna(axis=1, how="all")

            # --- Separar métricas monetarias y porcentuales ---
            metricas_pesos = [m for m, k in metricas_seleccionadas if not m.endswith("%")]
            metricas_porcentajes = [m for m, k in metricas_seleccionadas if m.endswith("%")]

            # --- TABs ---
            tabs = st.tabs([
                "💵 Comparativo de Ingresos y Utilidades",
                "📈 Comparativo de Márgenes %",
                "⚙️ Gráfica Personalizada",
                "🥧 Participación por Proyecto"
            ])

            # --- TAB 1 ---
            with tabs[0]:
                st.write("### Ingresos y Utilidades")

                columnas_existentes = [m for m in metricas_pesos if m in df_limpio.columns]
                df_proyecto = df_limpio[df_limpio["Proyecto"] == proyecto_seleccionado]

                if columnas_existentes:
                    fig_montos = px.bar(
                        df_proyecto,
                        x="Proyecto",
                        y=columnas_existentes,
                        barmode="group",
                        title=f"Montos comparativos del proyecto: {proyecto_seleccionado}",
                        labels={"value": "Monto", "variable": "Métrica"},
                        text_auto=".2s"
                    )
                    st.plotly_chart(fig_montos, use_container_width=True)
                else:
                    st.info("No hay métricas monetarias disponibles para graficar.")

            # --- TAB 2 ---
            with tabs[1]:
                st.write("### Márgenes por Proyecto (%)")

                columnas_margen = [m for m in metricas_porcentajes if m in df_limpio.columns]
                df_margen = df_limpio[df_limpio["Proyecto"] == proyecto_seleccionado].copy()

                for col in columnas_margen:
                    try:
                        df_margen[col] = df_margen[col].replace("%", "", regex=True).astype(float)
                    except:
                        df_margen[col] = pd.to_numeric(df_margen[col], errors="coerce")

                if columnas_margen:
                    fig_margenes = px.bar(
                        df_margen,
                        x="Proyecto",
                        y=columnas_margen,
                        barmode="group",
                        title=f"Márgenes del proyecto: {proyecto_seleccionado}",
                        labels={"value": "%", "variable": "Métrica"},
                        text_auto=".2f"
                    )
                    fig_margenes.update_layout(yaxis=dict(tickformat=".0%"))
                    st.plotly_chart(fig_margenes, use_container_width=True)
                else:
                    st.info("No hay métricas de margen disponibles.")

            # --- TAB 3 ---
            with tabs[2]:
                st.write("### Comparación personalizada")

                columnas_disponibles = [col for col in df_limpio.columns if col != "Proyecto"]
                metrica_default = "Ingresos" if "Ingresos" in columnas_disponibles else columnas_disponibles[0]

                seleccion = st.multiselect(
                    "Selecciona métricas:",
                    options=columnas_disponibles,
                    default=[metrica_default]
                )

                if seleccion:
                    df_custom = df_limpio[df_limpio["Proyecto"] == proyecto_seleccionado]
                    fig_custom = px.bar(
                        df_custom,
                        x="Proyecto",
                        y=seleccion,
                        barmode="group",
                        title=f"Comparación personalizada para: {proyecto_seleccionado}",
                        labels={"value": "Valor", "variable": "Métrica"},
                        text_auto=".2s"
                    )
                    st.plotly_chart(fig_custom, use_container_width=True)
                else:
                    st.info("Selecciona al menos una métrica.")

            # --- TAB 4 (Pastel, sin filtro) ---
            with tabs[3]:
                st.write("### Participación por Proyecto")

                metricas_disponibles_pie = [m for m in metricas_pesos if m in df_limpio.columns]

                metrica_pastel = st.selectbox(
                    "Selecciona una métrica para ver participación:",
                    options=metricas_disponibles_pie,
                    index=0 if "Ingresos" in metricas_disponibles_pie else 0
                )

                df_pie = df_limpio[["Proyecto", metrica_pastel]].copy()
                df_pie = df_pie[df_pie["Proyecto"].str.upper() != "ESGARI"]

                try:
                    df_pie[metrica_pastel] = df_pie[metrica_pastel].replace("[\$,]", "", regex=True).astype(float)
                except:
                    df_pie[metrica_pastel] = pd.to_numeric(df_pie[metrica_pastel], errors="coerce")

                fig_pie = px.pie(
                    df_pie,
                    names="Proyecto",
                    values=metrica_pastel,
                    title=f"Participación de {metrica_pastel} por Proyecto",
                    hole=0.3
                )
                st.plotly_chart(fig_pie, use_container_width=True)



    elif selected == "Estado de Resultado":

        estdo_re(df_2025, ceco = "1")


    elif selected == "Comparativa":
        st.write("Bienvenido a la sección de Comparativa. Aquí puedes comparar diferentes fechas.")
        col1, col2 = st.columns(2)
        meses_seleccionado = filtro_meses(col1, df_2025)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)
        if not meses_seleccionado:
            st.error("Favor de seleccionar por lo menos un mes")
        else:
            
            er = estado_resultado(df_2025, meses_seleccionado, proyecto_nombre, proyecto_codigo, list_pro)

            if st.session_state['rol'] == "gerente":
                            metricas_seleccionadas = [
                    ("Ingreso", "ingreso_proyecto"),
                    ("COSS", "coss_pro"),
                    ("COSS Patio", "patio_pro"),
                    ("COSS Total", "coss_total"),
                    ("Utilidad Bruta", "utilidad_bruta"),
                    ("G.ADMN", "gadmn_pro"),
                    ("Utilidad Operativa", "utilidad_operativa"),
                ]
            
            else:
                metricas_seleccionadas = [
                    ("Ingreso", "ingreso_proyecto"),
                    ("COSS", "coss_pro"),
                    ("COSS Patio", "patio_pro"),
                    ("COSS Total", "coss_total"),
                    ("Utilidad Bruta", "utilidad_bruta"),
                    ("G.ADMN", "gadmn_pro"),
                    ("Utilidad Operativa", "utilidad_operativa"),
                    ("OH", "oh_pro"),
                    ("EBIT", "ebit"),
                    ("Gasto Fin", "gasto_fin_pro"),
                    ("Ingreso Fin", "ingreso_fin_pro"),
                    ("EBT", "ebt"),
                ]     

            def tabla_er(metricas_seleccionadas, er, columa):
                valor_ingreso = er.get("ingreso_proyecto", None)
                df_data = []
                for nombre_metrica, clave in metricas_seleccionadas:
                    valor = er.get(clave, None)
                    # Paso 2: calcular % sobre ingreso (evitando división por cero)
                    porcentaje_sobre_ingreso = valor / valor_ingreso if valor_ingreso and isinstance(valor, (int, float)) else None
                    fila = {
                        "Concepto": nombre_metrica,
                        columa: valor,
                        "% sobre Ingreso": 1.0 if clave == "ingreso_proyecto" else porcentaje_sobre_ingreso
                    }
                    df_data.append(fila)

                df_tabla = pd.DataFrame(df_data)
                return df_tabla
            
            meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
            if len(meses_seleccionado) != 1 or meses_seleccionado[0] == "ene.":
                tipo_com = st.selectbox("Seleccione el tipo de comparativa:", ["LY", "PPT"])
            else:
                tipo_com = st.selectbox("Seleccione el tipo de comparativa:", ["LY", "PPT", "LM"])

            if tipo_com == "LY":
                er_ly = estado_resultado(df_ly, meses_seleccionado, proyecto_nombre, proyecto_codigo, list_pro)
                df_compara = tabla_er(metricas_seleccionadas, er_ly, "LY")
                df_compara.drop(columns=["% sobre Ingreso"], inplace=True)
                df_agrid = df_ly[df_ly['Mes_A'].isin(meses_seleccionado)]
                df_agrid = df_agrid[df_agrid['Proyecto_A'].isin(proyecto_codigo)]

            elif tipo_com == "PPT":
                er_ppt = estado_resultado(df_ppt, meses_seleccionado, proyecto_nombre, proyecto_codigo, list_pro)
                df_compara = tabla_er(metricas_seleccionadas, er_ppt, "PPT")
                df_compara.drop(columns=["% sobre Ingreso"], inplace=True)
                df_agrid = df_ppt[df_ppt['Mes_A'].isin(meses_seleccionado)]
                df_agrid = df_agrid[df_agrid['Proyecto_A'].isin(proyecto_codigo)]

            else:
                indice_mes = meses.index(meses_seleccionado[0])
                mes_anterior = meses[indice_mes - 1]
                er_lm = estado_resultado(df_2025, [mes_anterior], proyecto_nombre, proyecto_codigo, list_pro)
                df_compara = tabla_er(metricas_seleccionadas, er_lm, "LM")
                df_compara.drop(columns=["% sobre Ingreso"], inplace=True)
                df_agrid = df_2025[df_2025['Mes_A'] == mes_anterior]
                df_agrid = df_agrid[df_agrid['Proyecto_A'].isin(proyecto_codigo)]

            
            df_tabla = tabla_er(metricas_seleccionadas, er, "YTD")
            df_tabla.drop(columns=["% sobre Ingreso"], inplace=True)
            df_compara = pd.merge(df_tabla, df_compara, on="Concepto", how="outer", suffixes=("", f"_{tipo_com}"))
            # Definir los nombres de las columnas comparadas
            col_ytd = "YTD"
            col_com = tipo_com  # Será "LY", "PPT" o "LM" dependiendo del selectbox

            # Verificar que ambas columnas existen antes de aplicar el cálculo
            if col_ytd in df_compara.columns and col_com in df_compara.columns:
                df_compara["Variación % "] = df_compara.apply(
                    lambda row: ((row[col_ytd] - row[col_com]) / row[col_com]) * 100
                    if pd.notnull(row[col_ytd]) and pd.notnull(row[col_com]) and row[col_com] != 0
                    else 0,
                    axis=1
                )
            df_compara = df_compara.set_index("Concepto", drop=True)
            def formato_monetario(valor):
                return "${:,.0f}".format(valor) if pd.notnull(valor) else ""

            def formato_porcentaje(valor):
                return "{:.2f}%".format(valor) if pd.notnull(valor) else ""

            # --- Formatear columnas ---
            for col in df_compara.columns:
                if col in ["YTD", "LY", "PPT", "LM"]:
                    df_compara[col] = df_compara[col].apply(formato_monetario)
                elif "Variación %" in col:
                    df_compara[col] = df_compara[col].apply(formato_porcentaje)

            # --- Identificador de tabla ---
            i = 1

            # --- Estilo sin bordes y texto alineado a la izquierda ---
            st.markdown(f"""
                <style>
                .tab-table-{i} {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                    font-size: 13px;
                    font-family: Arial, sans-serif;
                    text-align: left;
                }}
                .tab-table-{i} th {{
                    background-color: #003366;
                    color: white;
                    text-transform: uppercase;
                    text-align: left;
                    padding: 10px;
                    border: none;
                }}
                .tab-table-{i} td {{
                    padding: 8px;
                    text-align: left;
                    border: none;
                }}
                .tab-table-{i} tr:nth-child(1),
                .tab-table-{i} tr:nth-child(5),
                .tab-table-{i} tr:nth-child(7),
                .tab-table-{i} tr:nth-child(9),
                .tab-table-{i} tr:nth-child(12) {{
                    background-color: #003366;
                    color: white;
                }}
                .tab-table-{i} tr:nth-child(2),
                .tab-table-{i} tr:nth-child(3),
                .tab-table-{i} tr:nth-child(4),
                .tab-table-{i} tr:nth-child(6),
                .tab-table-{i} tr:nth-child(8),
                .tab-table-{i} tr:nth-child(10),
                .tab-table-{i} tr:nth-child(11) {{
                    background-color: white;
                    color: black;
                }}
                .tab-table-{i} tr:hover {{
                    background-color: #00509E;
                    color: white;
                }}
                </style>
            """, unsafe_allow_html=True)

            # --- Convertir a HTML y mostrar ---
            tabla_html = df_compara.reset_index().to_html(
                index=False,
                escape=False,
                classes=f"tab-table-{i}",
                border=0
            )
            st.markdown(tabla_html, unsafe_allow_html=True)
            df_grafico = df_compara.copy()

            tabs = st.tabs(["📊 Gráfico de barras", "📈 Grafico Mensual"])
            with tabs[1]:
                # === GRÁFICO LINEAL DE COMPARACIÓN MENSUAL POR MÉTRICA ===
                st.markdown("### Evolución mensual de métricas clave")

                # Elegir métrica a graficar
                conceptos_disponibles = df_grafico.index.tolist()
                concepto_elegido = st.selectbox("Selecciona la métrica a graficar:", conceptos_disponibles)

                # Filtrar valores mensuales por proyecto y concepto
                df_linea = pd.DataFrame()

                for mes in meses_seleccionado:
                    ytd_val = df_2025[
                        (df_2025["Mes_A"] == mes) & 
                        (df_2025["Proyecto_A"].isin(proyecto_codigo))
                    ]
                    
                    if tipo_com == "LY":
                        comp_val = df_ly[(df_ly["Mes_A"] == mes) & (df_ly["Proyecto_A"].isin(proyecto_codigo))]
                    elif tipo_com == "PPT":
                        comp_val = df_ppt[(df_ppt["Mes_A"] == mes) & (df_ppt["Proyecto_A"].isin(proyecto_codigo))]
                    else:  # LM
                        comp_val = df_2025[(df_2025["Mes_A"] == mes) & (df_2025["Proyecto_A"].isin(proyecto_codigo))]

                    def get_metrica(df, clave):
                        return estado_resultado(df, [mes], proyecto_nombre, proyecto_codigo, list_pro).get(clave, 0)

                    clave_busqueda = dict(metricas_seleccionadas)[concepto_elegido]
                    ytd_valor = get_metrica(df_2025, clave_busqueda)
                    comp_valor = get_metrica(comp_val, clave_busqueda)

                    df_linea = pd.concat([df_linea, pd.DataFrame({
                        "Mes": [mes] * 2,
                        "Valor": [ytd_valor, comp_valor],
                        "Tipo": ["YTD", tipo_com]
                    })])

                # Ordenar por meses cronológicamente
                df_linea["Mes"] = pd.Categorical(df_linea["Mes"], categories=meses, ordered=True)
                df_linea = df_linea.sort_values("Mes")

                fig_linea = px.line(
                    df_linea,
                    x="Mes",
                    y="Valor",
                    color="Tipo",
                    markers=True,
                    title=f"{concepto_elegido} mensual: YTD vs {tipo_com}",
                    text=df_linea["Valor"].apply(lambda x: f"${x:,.0f}")
                )

                fig_linea.update_traces(textposition="top center")
                fig_linea.update_layout(
                    yaxis_title="Monto ($)",
                    xaxis_title="Mes",
                    height=450,
                    template="plotly_white",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )

                st.plotly_chart(fig_linea, use_container_width=True)
            
            with tabs[0]:

                # Quitar formato monetario para columnas de comparación
                for col in ["YTD", tipo_com]:
                    df_grafico[col] = df_grafico[col].replace('[\$,]', '', regex=True).astype(float)

                # Limpiar porcentaje
                df_grafico["Variación % "] = df_grafico["Variación % "].replace('%', '', regex=True).astype(float)

                # Orden opcional
                df_grafico = df_grafico.sort_values(by="YTD", ascending=False)

                # === GRÁFICO DE BARRAS COMPARATIVO CON FORMATO $ ===
                fig_comp = go.Figure()

                fig_comp.add_trace(go.Bar(
                    x=df_grafico.index,
                    y=df_grafico["YTD"],
                    name="YTD",
                    marker_color="#003366",
                    text=df_grafico["YTD"].apply(lambda x: f"${x:,.0f}"),
                    textposition="auto"
                ))

                fig_comp.add_trace(go.Bar(
                    x=df_grafico.index,
                    y=df_grafico[tipo_com],
                    name=tipo_com,
                    marker_color="#b0b0b0",
                    text=df_grafico[tipo_com].apply(lambda x: f"${x:,.0f}"),
                    textposition="auto"
                ))

                fig_comp.update_layout(
                    title=f"Comparativa YTD vs {tipo_com}",
                    xaxis_title="Concepto",
                    yaxis_title="Monto ($)",
                    barmode='group',
                    height=500,
                    template="plotly_white",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )

                st.plotly_chart(fig_comp, use_container_width=True)


                # === GRÁFICO DE VARIACIÓN % ===
                fig_var = px.bar(
                    df_grafico.reset_index(),
                    x="Concepto",
                    y="Variación % ",
                    title="Variación porcentual entre YTD y " + tipo_com,
                    color="Variación % ",
                    color_continuous_scale="RdBu_r",
                    text="Variación % ",
                    height=400
                )

                fig_var.update_layout(
                    yaxis_title="Variación %",
                    xaxis_title="Concepto",
                    template="plotly_white"
                )
                fig_var.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

                st.plotly_chart(fig_var, use_container_width=True)

            if st.session_state['rol'] == "director" or st.session_state['rol'] == "admin":
                ventanas = ['INGRESO', 'COSS', 'G.ADMN', 'GASTOS FINANCIEROS', 'INGRESO FINANCIERO']
                tabs = st.tabs(ventanas)
                with tabs[0]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Categoria_A", "INGRESO", "Tabla de Ingresos")

                with tabs[1]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Clasificacion_A", "COSS", "Tabla de COSS")
                    
                with tabs[2]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Clasificacion_A", "G.ADMN", "Tabla de G.ADMN")
                    
                with tabs[3]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Clasificacion_A", "GASTOS FINANCIEROS", "Tabla de Gastos Financieros")
                    
                with tabs[4]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Categoria_A", "INGRESO POR REVALUACION CAMBIARIA", "Tabla de Ingreso Financiero")
            else:
                ventanas = ['INGRESO', 'COSS', 'G.ADMN']
                tabs = st.tabs(ventanas)
                with tabs[0]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Categoria_A", "INGRESO", "Tabla de Ingresos")

                with tabs[1]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Clasificacion_A", "COSS", "Tabla de COSS")
                    
                with tabs[2]:
                    tabla_comparativa(tipo_com, df_agrid, df_2025, proyecto_codigo, meses_seleccionado, "Clasificacion_A", "G.ADMN", "Tabla de G.ADMN")  

                

    elif selected == "Análisis":
        st.write("Bienvenido a la sección de Análisis. Aquí puedes realizar un análisis detallado de los datos.")
        col1, col2 = st.columns(2)
        meses_seleccionado = filtro_meses(col1, df_2025)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)
        if proyecto_nombre == "OFICINAS LUNA" or proyecto_nombre == "PATIO" or proyecto_nombre == "OFICINAS ANDARES":
            st.error("Este tipo de análisis no es posible para este Proyecto")
        else:
            seccion_analisis_por_clasificacion(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, "COSS")
            seccion_analisis_especial_porcentual(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, patio, "Patio")
            seccion_analisis_por_clasificacion(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, "G.ADMN")
            
            if st.session_state['rol'] == "director" or st.session_state['rol'] == "admin":
                seccion_analisis_por_clasificacion(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, "GASTOS FINANCIEROS")
                seccion_analisis_especial_porcentual(df_2025, df_ly, ingreso, meses_seleccionado, proyecto_codigo, proyecto_nombre, oh, "OH")

    
    elif selected == "Proyeccion":
        st.write("Bienvenido a la sección de Proyección. Aquí puedes ver las proyecciones de los proyectos.")
        costos_variables = ["FLETES", "CASETAS", "COMBUSTIBLE", "OTROS COSS", "INGRESO"]

        col1, col2 = st.columns(2)
        promedio_fijo = col1.selectbox("Seleciona que promedio usar para los gastos fijos", ["LM", "YTD", "TRES MESES"])
        promedio_variables = col2.selectbox("Seleciona que promedio usar para los gastos variables", ["Mes actual","LM", "YTD", "TRES MESES"])

        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        # ✅ Fecha y meses (una sola vez)
        fecha_completa = pd.to_datetime(fecha_actualizacion["fecha"].iloc[0])
        fecha_act = fecha_completa.day
        ultimo_dia_mes = (fecha_completa + pd.offsets.MonthEnd(0)).day

        idx_mes_act = fecha_completa.month - 1
        mes_act = meses_ordenados[idx_mes_act]                 # mes actual (según fecha real)
        mes_ant_lm = meses_ordenados[(idx_mes_act - 1) % 12]   # LM (mes anterior circular)

        # Filtros
        df_mes = df_2025[df_2025["Mes_A"] == mes_act]
        mes = filtro_meses(col1, df_mes)
        codigo_pro, pro = filtro_pro(col2)

        # Toggle ingresos
        ingreso_pro_fut = 0.0
        ingreso_lineal = st.toggle("ingreso lineal / ingreso por historico", value=True)

        if ingreso_lineal:
            st.write("Proyección lineal")
            df_ing_futu = df_2025[df_2025["Mes_A"] == mes_act]
            if pro != "ESGARI":
                df_ing_futu = df_ing_futu[df_ing_futu["Proyecto_A"].isin(codigo_pro)]
            df_ing_futu = df_ing_futu[df_ing_futu["Categoria_A"] == "INGRESO"]
            ingreso_pro_fut = df_ing_futu["Neto_A"].sum() / fecha_act * ultimo_dia_mes

        else:
            st.write("Proyección con historicos")
            ingreso_sem_url = "https://docs.google.com/spreadsheets/d/14l6QLudSBpqxmfuwRqVxCXzhSFzRL0AqWJqVuIOaFFQ/export?format=xlsx"  #EXCEL ing
            ingreso_ly_url  = "https://docs.google.com/spreadsheets/d/1Mf_7EbzkpmqAJFPtN0-gFrFx3kubQNcsYYJfB2t30g0/export?format=xlsx" #EXCEL ing ly

            df_sem = cargar_datos(ingreso_sem_url)
            df_ly  = cargar_datos(ingreso_ly_url)

            fuente_hist = st.radio(
                "Fuente para histórico de ingresos",
                ["LM", "LY"],
                horizontal=True,
                key="fuente_hist_ing"
            )
            df_hist = df_sem if fuente_hist == "LM" else df_ly
            df_hist = df_hist.copy()
            df_hist["fecha"] = pd.to_datetime(df_hist["fecha"], errors="coerce")
            df_hist = df_hist.dropna(subset=["fecha"])

            df_hist["dia"] = df_hist["fecha"].dt.day
            idx_cercano = (df_hist["dia"] - fecha_act).abs().idxmin()
            dia_cercano = int(df_hist.loc[idx_cercano, "dia"])

            df_va = df_hist[df_hist["dia"] == dia_cercano].copy()
            df_va["ingreso"] = df_va["ingreso"] / dia_cercano * fecha_act
            df_va = df_va.drop(columns=["dia", "semana", "fecha"], errors="ignore")

            df_fin = df_hist[df_hist["semana"] == 4].copy()
            df_fin = df_fin.drop(columns=["dia", "semana", "fecha"], errors="ignore")

            df_merged = pd.merge(df_va, df_fin, on="proyecto", suffixes=("_va", "_fin"), how="inner")
            df_merged["ingreso_dividido"] = df_merged["ingreso_va"] / df_merged["ingreso_fin"]

            df_proyeccion = df_2025[df_2025["Mes_A"] == mes_act].copy()
            df_proyeccion = df_proyeccion.groupby(["Proyecto_A", "Categoria_A"], as_index=False)["Neto_A"].sum()
            df_proyeccion = df_proyeccion[df_proyeccion["Categoria_A"] == "INGRESO"].drop(columns=["Categoria_A"], errors="ignore")

            df_proyeccion["Proyecto_A"] = df_proyeccion["Proyecto_A"].astype(str).str.replace(".0", "", regex=False)
            df_merged["proyecto"] = df_merged["proyecto"].astype(str).str.replace(".0", "", regex=False)

            df_proyeccion = pd.merge(
                df_proyeccion,
                df_merged[["proyecto", "ingreso_dividido"]],
                left_on="Proyecto_A",
                right_on="proyecto",
                how="left"
            )

            df_proyeccion["ingreso_dividido"] = pd.to_numeric(df_proyeccion["ingreso_dividido"], errors="coerce")
            df_proyeccion.loc[df_proyeccion["ingreso_dividido"].isna() | (df_proyeccion["ingreso_dividido"] == 0), "ingreso_dividido"] = 1

            df_proyeccion["Neto_A"] = df_proyeccion["Neto_A"] / df_proyeccion["ingreso_dividido"]
            df_proyeccion = df_proyeccion.drop(columns=["proyecto", "ingreso_dividido"], errors="ignore")

            if pro == "ESGARI":
                ingreso_pro_fut = float(df_proyeccion["Neto_A"].sum())
            else:
                cods = [str(x).replace(".0", "") for x in (codigo_pro or [])]
                ingreso_pro_fut = float(df_proyeccion[df_proyeccion["Proyecto_A"].isin(cods)]["Neto_A"].sum())

        if promedio_fijo == "LM":
            
            df_ext = df_2025[df_2025["Mes_A"] == mes_ant_lm]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            if pro != "ESGARI":
                df_ext = df_ext[df_ext["Proyecto_A"].isin(codigo_pro)]
            df_ext = df_ext[~df_ext["Proyecto_A"].isin(["8002", "8003", "8004"])]
            df_ext["Mes_A"] = mes_act
            df_ext["Neto_A"] = df_ext["Neto_A"]
            df_sum = df_ext
            patio_pro = patio(df_2025, [mes_ant_lm], codigo_pro, pro)
            oh_pro = oh(df_2025, [mes_ant_lm], codigo_pro, pro)
         
        elif promedio_fijo == "YTD":

            df_ext = df_2025[df_2025["Mes_A"] != mes_act]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            if pro != "ESGARI":
                df_ext = df_ext[df_ext["Proyecto_A"].isin(codigo_pro)]
            df_ext = df_ext[~df_ext["Proyecto_A"].isin(["8002", "8003", "8004"])]
            numero_meses = df_ext['Mes_A'].nunique()

            columns = ['Empresa_A', 'CeCo_A', 'Proyecto_A', 'Cuenta_A', 
                    'Clasificacion_A', 'Cuenta_Nombre_A', 'Categoria_A']

            # Paso 1: Agrupamos incluyendo 'Mes_A' y sumamos 'Neto_A'
            df_sum = df_ext.groupby(columns, as_index=False)['Neto_A'].sum()

            df_sum['Neto_A'] = df_sum['Neto_A']/numero_meses
            df_sum["Mes_A"] = mes_act
            df_sum["Neto_A"] = df_sum["Neto_A"]
            meses_previos = df_ext["Mes_A"].unique().tolist()
            patio_pro = patio(df_2025, meses_previos, codigo_pro, pro) / numero_meses
            oh_pro = oh(df_2025, meses_previos, codigo_pro, pro) / numero_meses
  
        elif promedio_fijo == "TRES MESES":

            # Identificamos los 3 meses anteriores al mes actual
            idx_mes_act = meses_ordenados.index(mes_act)
            meses_previos = meses_ordenados[max(0, idx_mes_act - 3):idx_mes_act]

            # Filtramos gastos fijos (no variables) de los 3 meses anteriores
            df_ext = df_2025[df_2025["Mes_A"].isin(meses_previos)]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            if pro != "ESGARI":
                df_ext = df_ext[df_ext["Proyecto_A"].isin(codigo_pro)]
            df_ext = df_ext[~df_ext["Proyecto_A"].isin(["8002", "8003", "8004"])]

            numero_meses = df_ext['Mes_A'].nunique()  # Seguridad por si faltan meses

            columns = ['Empresa_A', 'CeCo_A', 'Proyecto_A', 'Cuenta_A',
                    'Clasificacion_A', 'Cuenta_Nombre_A', 'Categoria_A']

            # Agrupamos y sumamos los gastos fijos por combinación clave
            df_sum = df_ext.groupby(columns, as_index=False)['Neto_A'].sum()

            if numero_meses > 0:
                # Calculamos el promedio mensual de los 3 meses
                df_sum['Neto_A'] = df_sum['Neto_A'] / numero_meses

                # Proyectamos al mes actual, ajustado al día corrido
                df_sum["Mes_A"] = mes_act
                df_sum["Neto_A"] = df_sum["Neto_A"]
                patio_pro = patio(df_2025, meses_previos, codigo_pro, pro) / numero_meses
                oh_pro = oh(df_2025, meses_previos, codigo_pro, pro) / numero_meses

            else:
                st.warning("No hay suficientes meses anteriores para calcular el promedio de 3 meses.")


        # Respalda el cálculo original que ya tienes
        oh_pro_monto = locals().get("oh_pro", 0.0)  # si aún no existe, cae en 0.0

        col_modo, col_dummy = st.columns([2, 1])
        modo_oh_master = col_modo.selectbox(
            "Modo de cálculo de Overhead (OH)",
            ["Usar cálculo original (monto)", "Calcular como % de ingresos"],
            index=0  # default: respeta tu cálculo actual
        )

        # Helpers de rango de meses
        def meses_previos_hasta(mes_act, meses_ordenados):
            idx = meses_ordenados.index(mes_act)
            return meses_ordenados[:idx]

        def ultimos_tres_meses(mes_act, meses_ordenados):
            idx = meses_ordenados.index(mes_act)
            return meses_ordenados[max(0, idx-3):idx]

        # Si eligen % de ingresos, mostramos opciones de periodo y % manual
        oh_pro_pct = None
        if modo_oh_master == "Calcular como % de ingresos":
            col_oh1, col_oh2 = st.columns([2, 1])
            modo_oh = col_oh1.selectbox(
                "OH como % de ingresos (elige el periodo base)",
                ["Manual (fijo)", "Mes pasado (LM)", "Promedio 3 meses", "YTD (año en curso)"],
                index=0  # default manual
            )
            oh_pct_manual = col_oh2.number_input(
                "OH % (manual)",
                min_value=0.0, max_value=100.0, value=11.5, step=0.1,
                help="Porcentaje de OH sobre ingresos cuando el modo es Manual."
            )

            def calcular_pct_oh_hist(meses_sel, df_base, codigo_pro, pro):
                if not meses_sel:
                    return None
                df_hist = df_base[df_base["Mes_A"].isin(meses_sel)].copy()
                if pro != "ESGARI":
                    df_hist = df_hist[df_hist["Proyecto_A"].isin(codigo_pro)]
                ingreso_hist = df_hist.loc[df_hist["Categoria_A"] == "INGRESO", "Neto_A"].sum()
                try:
                    oh_hist = oh(df_base, meses_sel, codigo_pro, pro)
                except Exception:
                    oh_hist = 0.0
                if abs(ingreso_hist) > 1e-9:
                    return max(0.0, float(oh_hist) / float(ingreso_hist)) * 100.0
                return None

            # Selección de meses según modo
            oh_pct_elegido = None
            if modo_oh == "Manual (fijo)":
                oh_pct_elegido = oh_pct_manual
            elif modo_oh == "Mes pasado (LM)":
                meses_sel = [mes_ant_lm] if mes_ant_lm else []
                oh_pct_elegido = calcular_pct_oh_hist(meses_sel, df_2025, codigo_pro, pro)
            elif modo_oh == "Promedio 3 meses":
                meses_sel = ultimos_tres_meses(mes_act, meses_ordenados)
                oh_pct_elegido = calcular_pct_oh_hist(meses_sel, df_2025, codigo_pro, pro)
            elif modo_oh == "YTD (año en curso)":
                meses_sel = [m for m in meses_previos_hasta(mes_act, meses_ordenados)
                            if m in df_2025["Mes_A"].unique().tolist()]
                oh_pct_elegido = calcular_pct_oh_hist(meses_sel, df_2025, codigo_pro, pro)

            # Fallback robusto
            if oh_pct_elegido is None or not np.isfinite(oh_pct_elegido):
                st.info("No fue posible estimar el %OH con el histórico seleccionado. Usando 11.5% por defecto.")
                oh_pct_elegido = 11.5

            # Monto de OH proyectado por % de ingresos
            oh_pro_pct = ingreso_pro_fut * (oh_pct_elegido / 100.0)

        # --- Resultado final de OH a usar en el resto del flujo ---
        oh_pro = oh_pro_monto if modo_oh_master == "Usar cálculo original (monto)" else oh_pro_pct
        
        if promedio_variables == "Mes actual":
            df_ext_var = df_2025[df_2025["Mes_A"] == mes_act]
            df_ext_var = df_ext_var[df_ext_var["Categoria_A"].isin(costos_variables)]
            if pro != "ESGARI":
                df_ext_var = df_ext_var[df_ext_var["Proyecto_A"].isin(codigo_pro)]
            
            ingreso_pro = df_ext_var[df_ext_var["Categoria_A"] == "INGRESO"]["Neto_A"].sum()
            df_ext_var["Neto_normalizado"] = df_ext_var["Neto_A"] / ingreso_pro
            df_ext_var = df_ext_var[~df_ext_var["Categoria_A"].isin(["INGRESO"])]
             
            df_ext_var["Neto_A"] = df_ext_var["Neto_normalizado"] * ingreso_pro_fut
            variable = df_ext_var["Neto_normalizado"].sum()
            df_junto = pd.concat([df_ext_var, df_sum], ignore_index=True)

            coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
            
            gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESOS POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
            intereses = df_junto[df_junto["Clasificacion_A"] == "GASTOS FINANCIEROS"]["Neto_A"].sum() - df_junto[df_junto["Categoria_A"].isin(ingreso_fin_cue)]["Neto_A"].sum()

            utilidad_operativa = ingreso_pro_fut - coss_pro - gadmn_pro
            por_uo = utilidad_operativa / ingreso_pro_fut if ingreso_pro_fut != 0 else 0 
            ebit = utilidad_operativa - oh_pro
            ebt = ebit - intereses
            por_ebt = ebt / ingreso_pro_fut if ingreso_pro_fut != 0 else 0
            
            if modo_oh_master == "Calcular como % de ingresos":
                oh_pct_elegido = oh_pct_elegido  # ya estaba definido arriba
            else:
                oh_pct_elegido = None

            proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro, gadmn_pro, oh_pct_elegido)


        elif promedio_variables == "LM":
            df_ext_var = df_2025[df_2025["Mes_A"] == mes_ant_lm]
            df_ext_var = df_ext_var[df_ext_var["Categoria_A"].isin(costos_variables)]
            if pro != "ESGARI":
                df_ext_var = df_ext_var[df_ext_var["Proyecto_A"].isin(codigo_pro)]
            ingreso_pro = df_ext_var[df_ext_var["Categoria_A"] == "INGRESO"]["Neto_A"].sum()
            df_ext_var["Neto_normalizado"] = df_ext_var["Neto_A"] / ingreso_pro
            df_ext_var = df_ext_var[~df_ext_var["Categoria_A"].isin(["INGRESO"])]
        
            
            df_ext_var["Neto_A"] = df_ext_var["Neto_normalizado"] * ingreso_pro_fut

            variable = df_ext_var["Neto_normalizado"].sum()
            
            df_junto = pd.concat([df_ext_var, df_sum], ignore_index=True)

            coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
            
            gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESOS POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
            intereses = df_junto[df_junto["Clasificacion_A"] == "GASTOS FINANCIEROS"]["Neto_A"].sum() - df_junto[df_junto["Categoria_A"].isin(ingreso_fin_cue)]["Neto_A"].sum()

            utilidad_operativa = ingreso_pro_fut - coss_pro - gadmn_pro
            por_uo = utilidad_operativa / ingreso_pro_fut if ingreso_pro_fut != 0 else 0 
            ebit = utilidad_operativa - oh_pro
            ebt = ebit - intereses
            por_ebt = ebt / ingreso_pro_fut if ingreso_pro_fut != 0 else 0
            
            
            if modo_oh_master == "Calcular como % de ingresos":
                oh_pct_elegido = oh_pct_elegido  # ya estaba definido arriba
            else:
                oh_pct_elegido = None

            proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro, gadmn_pro, oh_pct_elegido)


        elif promedio_variables == "YTD":
            df_ext_var = df_2025[df_2025["Mes_A"] != mes_act]
            df_ext_var = df_ext_var[df_ext_var["Categoria_A"].isin(costos_variables)]
            if pro != "ESGARI":
                df_ext_var = df_ext_var[df_ext_var["Proyecto_A"].isin(codigo_pro)]
            ingreso_pro = df_ext_var[df_ext_var["Categoria_A"] == "INGRESO"]["Neto_A"].sum()
            df_ext_var["Neto_normalizado"] = df_ext_var["Neto_A"] / ingreso_pro
            df_ext_var = df_ext_var[~df_ext_var["Categoria_A"].isin(["INGRESO"])]
             
            df_ext_var["Neto_A"] = df_ext_var["Neto_normalizado"] * ingreso_pro_fut

            variable = df_ext_var["Neto_normalizado"].sum()
            
            df_junto = pd.concat([df_ext_var, df_sum], ignore_index=True)

            coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
            
            gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESOS POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
            intereses = df_junto[df_junto["Clasificacion_A"] == "GASTOS FINANCIEROS"]["Neto_A"].sum() - df_junto[df_junto["Categoria_A"].isin(ingreso_fin_cue)]["Neto_A"].sum()

            utilidad_operativa = ingreso_pro_fut - coss_pro - gadmn_pro
            por_uo = utilidad_operativa / ingreso_pro_fut if ingreso_pro_fut != 0 else 0 
            ebit = utilidad_operativa - oh_pro
            ebt = ebit - intereses
            por_ebt = ebt / ingreso_pro_fut if ingreso_pro_fut != 0 else 0
            
            
            if modo_oh_master == "Calcular como % de ingresos":
                oh_pct_elegido = oh_pct_elegido  # ya estaba definido arriba
            else:
                oh_pct_elegido = None

            proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro, gadmn_pro, oh_pct_elegido)

            
        elif promedio_variables == "TRES MESES":
            # Identificamos los 3 meses anteriores al mes actual
            idx_mes_act = meses_ordenados.index(mes_act)
            meses_previos = meses_ordenados[max(0, idx_mes_act - 3):idx_mes_act]

            # Filtramos gastos variables de los 3 meses anteriores
            df_ext_var = df_2025[df_2025["Mes_A"].isin(meses_previos)]
            df_ext_var = df_ext_var[df_ext_var["Categoria_A"].isin(costos_variables)]
            if pro != "ESGARI":
                df_ext_var = df_ext_var[df_ext_var["Proyecto_A"].isin(codigo_pro)]
            numero_meses = df_ext_var['Mes_A'].nunique()
            if numero_meses > 0:

                ingreso_pro = df_ext_var[df_ext_var["Categoria_A"] == "INGRESO"]["Neto_A"].sum()
                df_ext_var["Neto_normalizado"] = df_ext_var["Neto_A"] / ingreso_pro
                df_ext_var = df_ext_var[~df_ext_var["Categoria_A"].isin(["INGRESO"])]
                
                df_ext_var["Neto_A"] = df_ext_var["Neto_normalizado"] * ingreso_pro_fut

                variable = df_ext_var["Neto_normalizado"].sum()
                
                df_junto = pd.concat([df_ext_var, df_sum], ignore_index=True)

                coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum() + patio_pro
                
                gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

                ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESOS POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
                intereses = df_junto[df_junto["Clasificacion_A"] == "GASTOS FINANCIEROS"]["Neto_A"].sum() - df_junto[df_junto["Categoria_A"].isin(ingreso_fin_cue)]["Neto_A"].sum()

                if modo_oh_master == "Calcular como % de ingresos":
                    oh_pct_elegido = oh_pct_elegido  # ya estaba definido arriba
                else:
                    oh_pct_elegido = None

                proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro, gadmn_pro, oh_pct_elegido)


            else:
                st.warning("No hay suficientes meses anteriores para calcular el promedio de 3 meses.")  
    
    
    elif selected == "Meses":
        ct("P&L MES A MES")
        codigo_pro, pro = filtro_pro(st)
        ceco_codi, ceco_nomb = filtro_ceco(st)
        df_2025["CeCo_A"] = df_2025["CeCo_A"].astype(str)
        if ceco_nomb != "ESGARI":
            df_2025 = df_2025[df_2025["CeCo_A"].isin(ceco_codi)]
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                   "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        meses_disponibles = [mes for mes in meses_ordenados if mes in df_2025["Mes_A"].unique()]
        meses_filtrados = st.multiselect(
            "Selecciona los meses que deseas incluir:",
            options=meses_disponibles,
            default=meses_disponibles,
            key="filtro_meses_est_res"
        )
        if len(meses_filtrados) <2:
            st.error("Selecionar dos meses o más!")
        else:

            # --- Función principal para generar el estado de resultado mensual ---
            def estado_resultado_por_mes(df_2025, proyecto_nombre, proyecto_codigo, lista_proyectos):
                meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                                "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

                meses_disponibles = [mes for mes in meses_ordenados if mes in meses_filtrados]
                resultado_por_mes = {}

                for mes in meses_disponibles:
                    estado_mes = estado_resultado(
                        df_2025,
                        meses_seleccionado=[mes],
                        proyecto_nombre=proyecto_nombre,
                        proyecto_codigo=proyecto_codigo,
                        lista_proyectos=lista_proyectos
                    )
                    resultado_por_mes[mes] = estado_mes

                df_resultado = pd.DataFrame(resultado_por_mes)

                # Diccionario estricto: porcentaje -> métrica base
                porcentajes_base = {
                    "porcentaje_ingresos": "ingreso_proyecto",
                    "por_patio": "patio_pro",
                    "por_coss": "coss_total",
                    "por_utilidad_bruta": "utilidad_bruta",
                    "por_gadmn": "gadmn_pro",
                    "por_utilidad_operativa": "utilidad_operativa",
                    "por_oh": "oh_pro",
                    "por_ebit": "ebit",
                    "por_gasto_fin": "gasto_fin_pro",
                    "por_ingreso_fin": "ingreso_fin_pro",
                    "por_resultado_fin": "resultado_fin",
                    "por_ebt": "ebt"
                }

                # Función para calcular columna Total
                def calcular_total(row):
                    if row.name in porcentajes_base:
                        base_row = porcentajes_base[row.name]
                        ingreso_total = df_resultado.loc["ingreso_proyecto"].sum(skipna=True)
                        if base_row in df_resultado.index and ingreso_total != 0:
                            base_total = df_resultado.loc[base_row].sum(skipna=True)
                            return base_total / ingreso_total
                        else:
                            return np.nan
                    else:
                        return row.sum(skipna=True)

                # Agregar columna Total
                df_resultado["Total"] = df_resultado.apply(calcular_total, axis=1)

                # Agregar columna Promedio
                columnas_meses = [col for col in df_resultado.columns if col != "Total"]
                df_resultado["Promedio"] = df_resultado[columnas_meses].mean(axis=1, skipna=True)



                return df_resultado

            # Ejecutar función
            tabla_mensual = estado_resultado_por_mes(df_2025, pro, codigo_pro, list_pro)

            # Diccionario para formateo
            porcentajes_base = {
                "porcentaje_ingresos": "ingreso_proyecto",
                "por_patio": "patio_pro",
                "por_coss": "coss_total",
                "por_utilidad_bruta": "utilidad_bruta",
                "por_gadmn": "gadmn_pro",
                "por_utilidad_operativa": "utilidad_operativa",
                "por_oh": "oh_pro",
                "por_ebit": "ebit",
                "por_gasto_fin": "gasto_fin_pro",
                "por_ingreso_fin": "ingreso_fin_pro",
                "por_resultado_fin": "resultado_fin",
                "por_ebt": "ebt"
            }

            # Crear copia formateada
            tabla_formateada = tabla_mensual.copy()

            for row in tabla_formateada.index:
                if "por" in row.lower() or row.startswith("%"):
                    tabla_formateada.loc[row] = tabla_formateada.loc[row].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "")
                else:
                    tabla_formateada.loc[row] = tabla_formateada.loc[row].apply(lambda x: f"${x:,.0f}" if pd.notnull(x) else "")

            # Renombrar filas
            nombres_filas = {
                "ingreso_proyecto": "Ingresos",
                "patio_pro": "Patio",            
                "coss_total": "COSS",
                "utilidad_bruta": "Utilidad Bruta",
                "gadmn_pro": "Gastos Admin.",
                "utilidad_operativa": "Utilidad Operativa",
                "oh_pro": "OH",
                "ebit": "EBIT",
                "gasto_fin_pro": "Gastos Financieros",
                "oh_pro_gfin": "Gasto financiero OH",
                "ingreso_fin_pro": "Ingresos Financieros",
                "ebt": "EBT",
                "porcentaje_ingresos": "% de Ingresos",
                "por_patio": "% Patio",
                "por_coss": "% COSS",
                "por_utilidad_bruta": "% Utilidad Bruta",
                "por_gadmn": "% G. Admin",
                "por_utilidad_operativa": "% Utilidad Operativa",
                "por_oh": "% Overhead",
                "por_ebit": "% EBIT",
                "por_gasto_fin": "% Gasto Financiero",
                "por_ingreso_fin": "% Ingreso Financiero",
                "oh_pro_ifin": "Ingreso OH",
                "por_resultado_fin": "% Resultado Financiero",
                "por_ebt": "% EBT",
                
            }
            tabla_mensual_renombrada = tabla_formateada.rename(index=nombres_filas)
            tabla_mensual_renombrada = tabla_mensual_renombrada.drop(
                index=["coss_pro", "mal_coss", "mal_gadmn", "mal_gfin", "mal_ifin", "resultado_fin", "% de Ingresos"],
                errors='ignore'
            )
            if st.session_state["rol"] == "gerente":
                tabla_mensual_renombrada = tabla_mensual_renombrada.drop(
                    index=["OH", "EBIT", "Gastos Financieros", "Gasto financiero OH", "Ingresos Financieros", "EBT", "% Overhead", "% EBIT", "% Gasto Financiero", "% Ingreso Financiero", "Ingreso OH", "% Resultado Financiero", "% EBT"],
                    errors='ignore'
                )    

            # --- Estilo visual profesional para tabla mensual ---
            def generar_tabla_con_estilo_mensual(df):
                df_reset = df.reset_index().rename(columns={"index": "Concepto"})
                filas_porcentaje = [nombre for nombre in df_reset["Concepto"] if nombre.startswith("%") or "por" in nombre.lower()]

                def aplicar_estilos(row):
                    if row["Concepto"] == "Promedio Mensual":
                        return ['background-color: #cccccc; color: black; font-weight: bold;' for _ in row]
                    elif row["Concepto"] in filas_porcentaje:
                        return ['background-color: #00112B; color: white;' for _ in row]
                    else:
                        color_fondo = '#ffffff' if row.name % 2 == 0 else '#f2f2f2'
                        return [f'background-color: {color_fondo}; color: black;' for _ in row]

                estilos_header = [
                    {'selector': 'thead th', 'props': 'background-color: #00112B; color: white; font-weight: bold; font-size: 14px;'}
                ]

                html = (
                    df_reset.style
                    .apply(aplicar_estilos, axis=1)
                    .set_table_styles(estilos_header)
                    .set_properties(**{'font-size': '12px', 'text-align': 'right'})
                    .hide(axis='index')
                    .render()
                )

                responsive_html = f'<div style="overflow-x: auto; width: 100%;">{html}</div>'
                return responsive_html

            # Mostrar en Streamlit
            st.write(f"### Estado de Resultado por Mes '{pro}'")
            tabla_html = generar_tabla_con_estilo_mensual(tabla_mensual_renombrada)
            st.markdown(tabla_html, unsafe_allow_html=True)
            


            # --- Preparar DataFrame ---
            meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                            "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

            meses_disponibles = [mes for mes in meses_ordenados if mes in meses_filtrados]

            df_meses = df_2025[df_2025["Proyecto_A"].isin(codigo_pro)]
            df_meses = df_meses[~(df_meses["Clasificacion_A"].isin(["IMPUESTOS", "OTROS INGRESOS"]))]
            if st.session_state["rol"] == "gerente":
                df_meses = df_meses[~(df_meses["Clasificacion_A"].isin(["GASTOS FINANCIEROS"]))]
            df_meses = df_meses.groupby(
                ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A", "Mes_A"],
                as_index=False
            )["Neto_A"].sum()

            df_pivot = df_meses.pivot_table(
                index=["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"],
                columns="Mes_A",
                values="Neto_A",
                aggfunc="sum"
            )

            for mes in meses_disponibles:
                if mes not in df_pivot.columns:
                    df_pivot[mes] = 0
            
            # Reordenar columnas según meses_disponibles
            df_pivot = df_pivot[meses_disponibles]
            df_pivot = df_pivot.reset_index().fillna(0)

            # --- Agregar columnas de Total y Promedio ---
            columnas_mensuales = [col for col in df_pivot.columns if col not in ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"]]
            df_pivot["Total"] = df_pivot[columnas_mensuales].sum(axis=1)
            df_pivot["Promedio"] = df_pivot[columnas_mensuales].mean(axis=1)


            # --- Configurar AgGrid ---

            gb = GridOptionsBuilder.from_dataframe(df_pivot)

            # Agrupar jerárquicamente
            gb.configure_column("Clasificacion_A", rowGroup=True, hide=True)
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)
            gb.configure_column("Cuenta_Nombre_A", pinned='left')

            # Formateador de moneda usando JavaScript
            currency_formatter = JsCode("""
                function(params) {
                    if (params.value === 0 || params.value === null) {
                        return "$0.00";
                    }
                    return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(params.value);
                }
            """)

            # Aplicar formato visual con el formateador JS
            for col in df_pivot.columns:
                if col not in ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"]:
                    gb.configure_column(
                        col,
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        aggFunc="sum",
                        valueFormatter=currency_formatter,
                        cellStyle={'textAlign': 'right'}
                    )

            gridOptions = gb.build()

            # Mostrar en Streamlit
            st.write("### Tabla Clasificación, Categoría y Cuenta")
            AgGrid(
                df_pivot,
                gridOptions=gridOptions,
                enable_enterprise_modules=True,
                fit_columns_on_grid_load=False,
                allow_unsafe_jscode=True,
                domLayout='normal',
                height=600
            )

            # Convertir a formato largo para graficar
            df_graficas = tabla_mensual_renombrada.T.reset_index().rename(columns={"index": "Mes"})


            # Eliminar filas de Total y Promedio
            df_graficas = df_graficas[~df_graficas["Mes"].isin(["Total", "Promedio"])]
            # Convertir únicamente columnas con % al tipo float si son strings
            columnas_porcentaje = [col for col in df_graficas.columns if col.startswith("%")]
            
            for col in columnas_porcentaje:
                if df_graficas[col].dtype == object or df_graficas[col].dtype == "string":
                    df_graficas[col] = (
                        df_graficas[col]
                        .str.replace("%", "", regex=False)
                        .replace("", np.nan)
                        .astype(float)
                    )

            # Variables por rol
            es_gerente = st.session_state.get("rol") == "gerente"

            # Conceptos a excluir para gerentes
            conceptos_excluir = [
                "OH", "EBIT", "Gastos Financieros", "Gasto financiero OH", "Ingresos Financieros", "EBT",
                "% Overhead", "% EBIT", "% Gasto Financiero", "% Ingreso Financiero", "Ingreso OH", "% Resultado Financiero", "% EBT"
            ]

            # Generar lista limpia de columnas para graficar
            conceptos_disponibles = [col for col in df_graficas.columns if col != "Mes"]
            if es_gerente:
                conceptos_disponibles = [col for col in conceptos_disponibles if col not in conceptos_excluir]

            # Crear tabs
            tabs = st.tabs([
                "📈 Ingresos vs Utilidad Operativa",
                "📉  de Gastos",
                "📊 Márgenes de Rentabilidad",
                "🎛️ Gráfica Personalizada"
            ])

            # --- TAB 1: Ingresos vs Utilidad Operativa ---
            with tabs[0]:
                st.subheader("Ingresos vs Utilidad Operativa")

                columnas_graf1 = [col for col in ["Ingresos", "Utilidad Operativa"] if col in df_graficas.columns]

                if len(columnas_graf1) >= 2:
                    fig1 = px.line(
                        df_graficas,
                        x="Mes",
                        y=columnas_graf1,
                        markers=True,
                        title="Evolución mensual: Ingresos vs Utilidad Operativa",
                        labels={"value": "Monto", "variable": "Concepto"}
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("No hay suficientes datos disponibles para esta gráfica.")


            # --- TAB 2:  de Gastos ---
            with tabs[1]:
                st.subheader("Composición mensual de gastos")

                # Usar tabla_mensual limpia, renombrar filas para mantener coherencia
                tabla_gastos = tabla_mensual.rename(index=nombres_filas)
                if es_gerente:
                    tabla_gastos = tabla_gastos.drop(index=conceptos_excluir, errors='ignore')

                gastos_clave = ["COSS", "Gastos Admin.", "Gastos Financieros"]
                columnas_gastos = [g for g in gastos_clave if g in tabla_gastos.index]

                if columnas_gastos:
                    # Transponer para graficar
                    gastos_data = tabla_gastos.loc[columnas_gastos].T.reset_index().rename(columns={"index": "Mes"})

                    fig2 = px.bar(
                        gastos_data,
                        x="Mes",
                        y=columnas_gastos,
                        barmode="stack",
                        title="Composición de gastos por mes",
                        labels={"value": "Monto", "variable": "Tipo de Gasto"}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No hay columnas de gasto disponibles para graficar.")

            # --- TAB 3: Márgenes de Rentabilidad ---
            with tabs[2]:
                st.subheader("Márgenes de rentabilidad")

                margenes_clave = ["% Utilidad Bruta", "% Utilidad Operativa"]
                columnas_margen = [m for m in margenes_clave if m in df_graficas.columns]

                if columnas_margen:
                    # Convertir strings tipo '25.00%' a float (por si están formateadas)
                    for col in columnas_margen:
                        df_graficas[col] = df_graficas[col].replace("%", "", regex=True).astype(float)

                    fig3 = px.line(
                        df_graficas,
                        x="Mes",
                        y=columnas_margen,
                        markers=True,
                        title="Márgenes: Utilidad Bruta y Operativa",
                        labels={"value": "%", "variable": "Métrica"}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("No hay márgenes disponibles para graficar.")
                
                # --- TAB 4: Gráfica Personalizada con doble eje Y ---
                with tabs[3]:
                    st.subheader("Gráfica personalizada")
                
                    seleccion = st.multiselect(
                        "Selecciona conceptos para graficar:",
                        options=conceptos_disponibles,
                        default=["Ingresos"] if "Ingresos" in conceptos_disponibles else []
                    )
                
                    if seleccion:
                        # Separar métricas monetarias y porcentuales
                        porcentuales = [col for col in seleccion if col.startswith("%")]
                        monetarias = [col for col in seleccion if not col.startswith("%")]
                
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                        # Agregar trazos monetarios
                        for col in monetarias:
                            fig.add_trace(
                                go.Scatter(
                                    x=df_graficas["Mes"],
                                    y=df_graficas[col],
                                    name=col,
                                    mode='lines+markers'
                                ),
                                secondary_y=False
                            )
                
                        # Agregar trazos porcentuales
                        for col in porcentuales:
                            fig.add_trace(
                                go.Scatter(
                                    x=df_graficas["Mes"],
                                    y=df_graficas[col],
                                    name=col,
                                    mode='lines+markers',
                                    line=dict(dash='dot')
                                ),
                                secondary_y=True
                            )
                
                        # Etiquetas de ejes
                        fig.update_yaxes(title_text="Monto ($ MXN)", secondary_y=False)
                        fig.update_yaxes(title_text="Porcentaje (%)", secondary_y=True)
                
                        fig.update_layout(
                            title="Evolución de conceptos seleccionados",
                            xaxis_title="Mes",
                            legend_title="Conceptos",
                            hovermode="x unified"
                        )
                
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Selecciona al menos un concepto para visualizar.")

    elif selected == "Meses LY/PPT":
        ct("P&L MES A MES")

        codigo_pro, pro = filtro_pro(st)
        ceco_codi, ceco_nomb = filtro_ceco(st)
        opcion = st.selectbox("Información:", ["PPT", "LY"], index=0)
        df_base = df_ppt.copy() if opcion == "PPT" else df_ly.copy()

        for col in ["CeCo_A", "Proyecto_A", "Mes_A"]:
            if col in df_base.columns:
                df_base[col] = df_base[col].astype(str).str.strip()

        codigo_pro = [str(x).strip() for x in codigo_pro]
        ceco_codi = [str(x).strip() for x in ceco_codi]
        if ceco_nomb != "ESGARI":
            df_base = df_base[df_base["CeCo_A"].isin(ceco_codi)].copy()

        meses_ordenados = [
            "ene.", "feb.", "mar.", "abr.", "may.", "jun.",
            "jul.", "ago.", "sep.", "oct.", "nov.", "dic."
        ]

        meses_disponibles = [m for m in meses_ordenados if m in df_base["Mes_A"].unique()]
        meses_filtrados = st.multiselect(
            "Selecciona los meses que deseas incluir:",
            options=meses_disponibles,
            default=meses_disponibles,
            key=f"filtro_meses_ly_ppt_{opcion}_{pro}_{ceco_nomb}"
        )

        if len(meses_filtrados) < 2:
            st.error("Seleccionar dos meses o más.")
            st.stop()

        def estado_resultado_por_mes(df, proyecto_nombre, proyecto_codigo, lista_proyectos):
            meses_sel = [m for m in meses_ordenados if m in meses_filtrados]
            resultado_por_mes = {}

            for mes in meses_sel:
                resultado_por_mes[mes] = estado_resultado(
                    df,
                    meses_seleccionado=[mes],
                    proyecto_nombre=proyecto_nombre,
                    proyecto_codigo=proyecto_codigo,
                    lista_proyectos=lista_proyectos
                )

            df_resultado = pd.DataFrame(resultado_por_mes)

            porcentajes_base = {
                "porcentaje_ingresos": "ingreso_proyecto",
                "por_patio": "patio_pro",
                "por_coss": "coss_total",
                "por_utilidad_bruta": "utilidad_bruta",
                "por_gadmn": "gadmn_pro",
                "por_utilidad_operativa": "utilidad_operativa",
                "por_oh": "oh_pro",
                "por_ebit": "ebit",
                "por_gasto_fin": "gasto_fin_pro",
                "por_ingreso_fin": "ingreso_fin_pro",
                "por_resultado_fin": "resultado_fin",
                "por_ebt": "ebt"
            }

            def calcular_total(row):
                if row.name in porcentajes_base:
                    base_row = porcentajes_base[row.name]
                    ingreso_total = df_resultado.loc["ingreso_proyecto"].sum(skipna=True)

                    if base_row in df_resultado.index and ingreso_total != 0:
                        base_total = df_resultado.loc[base_row].sum(skipna=True)
                        return base_total / ingreso_total

                    return np.nan

                return row.sum(skipna=True)

            df_resultado["Total"] = df_resultado.apply(calcular_total, axis=1)

            columnas_meses = [c for c in df_resultado.columns if c != "Total"]
            df_resultado["Promedio"] = df_resultado[columnas_meses].mean(axis=1, skipna=True)

            return df_resultado

        tabla_mensual = estado_resultado_por_mes(df_base, pro, codigo_pro, list_pro)

        nombres_filas = {
            "ingreso_proyecto": "Ingresos",
            "patio_pro": "Patio",
            "coss_total": "COSS",
            "utilidad_bruta": "Utilidad Bruta",
            "gadmn_pro": "Gastos Admin.",
            "utilidad_operativa": "Utilidad Operativa",
            "oh_pro": "OH",
            "ebit": "EBIT",
            "gasto_fin_pro": "Gastos Financieros",
            "oh_pro_gfin": "Gasto financiero OH",
            "ingreso_fin_pro": "Ingresos Financieros",
            "ebt": "EBT",
            "porcentaje_ingresos": "% de Ingresos",
            "por_patio": "% Patio",
            "por_coss": "% COSS",
            "por_utilidad_bruta": "% Utilidad Bruta",
            "por_gadmn": "% G. Admin",
            "por_utilidad_operativa": "% Utilidad Operativa",
            "por_oh": "% Overhead",
            "por_ebit": "% EBIT",
            "por_gasto_fin": "% Gasto Financiero",
            "por_ingreso_fin": "% Ingreso Financiero",
            "oh_pro_ifin": "Ingreso OH",
            "por_resultado_fin": "% Resultado Financiero",
            "por_ebt": "% EBT",
        }

        tabla_mensual_limpia = tabla_mensual.rename(index=nombres_filas)
        tabla_mensual_limpia = tabla_mensual_limpia.drop(
            index=[
                "coss_pro", "mal_coss", "mal_gadmn", "mal_gfin",
                "mal_ifin", "resultado_fin", "% de Ingresos"
            ],
            errors="ignore"
        )

        conceptos_ocultos_gerente = [
            "OH", "EBIT", "Gastos Financieros", "Gasto financiero OH",
            "Ingresos Financieros", "EBT", "% Overhead", "% EBIT",
            "% Gasto Financiero", "% Ingreso Financiero", "Ingreso OH",
            "% Resultado Financiero", "% EBT"
        ]

        if st.session_state.get("rol") == "gerente":
            tabla_mensual_limpia = tabla_mensual_limpia.drop(
                index=conceptos_ocultos_gerente,
                errors="ignore"
            )

        tabla_formateada = tabla_mensual_limpia.copy()
        for row in tabla_formateada.index:
            if row.startswith("%"):
                tabla_formateada.loc[row] = tabla_formateada.loc[row].apply(
                    lambda x: f"{x:.2%}" if pd.notnull(x) else ""
                )
            else:
                tabla_formateada.loc[row] = tabla_formateada.loc[row].apply(
                    lambda x: f"${x:,.0f}" if pd.notnull(x) else ""
                )

        def generar_tabla_con_estilo_mensual(df):
            df_reset = df.reset_index().rename(columns={"index": "Concepto"})
            filas_porcentaje = [
                x for x in df_reset["Concepto"]
                if str(x).startswith("%")
            ]

            def aplicar_estilos(row):
                if row["Concepto"] in filas_porcentaje:
                    return ["background-color: #00112B; color: white;" for _ in row]

                color_fondo = "#ffffff" if row.name % 2 == 0 else "#f2f2f2"
                return [f"background-color: {color_fondo}; color: black;" for _ in row]

            estilos_header = [
                {
                    "selector": "thead th",
                    "props": (
                        "background-color: #00112B; color: white; "
                        "font-weight: bold; font-size: 14px;"
                    )
                }
            ]

            html = (
                df_reset.style
                .apply(aplicar_estilos, axis=1)
                .set_table_styles(estilos_header)
                .set_properties(**{"font-size": "12px", "text-align": "right"})
                .hide(axis="index")
                .to_html()
            )

            return f'<div style="overflow-x: auto; width: 100%;">{html}</div>'

        st.write(f"### Estado de Resultado por Mes '{pro}'")
        st.markdown(generar_tabla_con_estilo_mensual(tabla_formateada), unsafe_allow_html=True)

        meses_sel = [m for m in meses_ordenados if m in meses_filtrados]
        df_meses = df_base.copy()
        if pro != "ESGARI":
            df_meses = df_meses[df_meses["Proyecto_A"].isin(codigo_pro)]

        df_meses = df_meses[
            ~df_meses["Clasificacion_A"].isin(["IMPUESTOS", "OTROS INGRESOS"])
        ]

        if st.session_state.get("rol") == "gerente":
            df_meses = df_meses[
                ~df_meses["Clasificacion_A"].isin(["GASTOS FINANCIEROS"])
            ]

        df_meses = df_meses.groupby(
            ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A", "Mes_A"],
            as_index=False
        )["Neto_A"].sum()

        df_pivot = df_meses.pivot_table(
            index=["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"],
            columns="Mes_A",
            values="Neto_A",
            aggfunc="sum",
            fill_value=0
        )

        for mes in meses_sel:
            if mes not in df_pivot.columns:
                df_pivot[mes] = 0

        df_pivot = df_pivot[meses_sel].reset_index().fillna(0)

        columnas_mensuales = [
            c for c in df_pivot.columns
            if c not in ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"]
        ]

        df_pivot["Total"] = df_pivot[columnas_mensuales].sum(axis=1)
        df_pivot["Promedio"] = df_pivot[columnas_mensuales].mean(axis=1)

        currency_formatter = JsCode("""
            function(params) {
                if (params.value === null || params.value === undefined || isNaN(params.value)) {
                    return "";
                }
                return new Intl.NumberFormat('es-MX', {
                    style: 'currency',
                    currency: 'MXN',
                    maximumFractionDigits: 0
                }).format(params.value);
            }
        """)

        gb = GridOptionsBuilder.from_dataframe(df_pivot)

        gb.configure_default_column(
            resizable=True,
            sortable=True,
            filter=True,
            groupable=True
        )

        gb.configure_column("Clasificacion_A", rowGroup=True, hide=True)
        gb.configure_column("Categoria_A", rowGroup=True, hide=True)
        gb.configure_column("Cuenta_Nombre_A", header_name="Cuenta", pinned="left")

        for col in columnas_mensuales + ["Total", "Promedio"]:
            gb.configure_column(
                col,
                type=["numericColumn", "numberColumnFilter"],
                aggFunc="sum",
                valueFormatter=currency_formatter,
                cellStyle={"textAlign": "right"}
            )

        gridOptions = gb.build()

        st.write("### Tabla Clasificación, Categoría y Cuenta")

        AgGrid(
            df_pivot,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            domLayout="normal",
            height=600,
            theme="streamlit",
            key=f"agrid_meses_ly_ppt_{opcion}_{pro}_{ceco_nomb}_{'-'.join(meses_sel)}"
        )


        df_graficas = tabla_mensual_limpia.T.reset_index().rename(columns={"index": "Mes"})
        df_graficas = df_graficas[~df_graficas["Mes"].isin(["Total", "Promedio"])].copy()

        for col in df_graficas.columns:
            if col != "Mes":
                df_graficas[col] = pd.to_numeric(df_graficas[col], errors="coerce")

        es_gerente = st.session_state.get("rol") == "gerente"

        conceptos_disponibles = [c for c in df_graficas.columns if c != "Mes"]

        if es_gerente:
            conceptos_disponibles = [
                c for c in conceptos_disponibles
                if c not in conceptos_ocultos_gerente
            ]

        tabs = st.tabs([
            "📈 Ingresos vs Utilidad Operativa",
            "📉 Composición de Gastos",
            "📊 Márgenes de Rentabilidad",
            "🎛️ Gráfica Personalizada"
        ])

        with tabs[0]:
            st.subheader("Ingresos vs Utilidad Operativa")

            columnas_graf1 = [
                c for c in ["Ingresos", "Utilidad Operativa"]
                if c in df_graficas.columns
            ]

            if len(columnas_graf1) >= 2:
                fig1 = px.line(
                    df_graficas,
                    x="Mes",
                    y=columnas_graf1,
                    markers=True,
                    title=f"Evolución mensual {opcion}: Ingresos vs Utilidad Operativa",
                    labels={"value": "Monto", "variable": "Concepto"}
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No hay suficientes datos disponibles para esta gráfica.")

        with tabs[1]:
            st.subheader("Composición mensual de gastos")

            gastos_clave = ["COSS", "Gastos Admin.", "Gastos Financieros"]
            columnas_gastos = [g for g in gastos_clave if g in tabla_mensual_limpia.index]

            if columnas_gastos:
                gastos_data = (
                    tabla_mensual_limpia
                    .loc[columnas_gastos]
                    .T
                    .reset_index()
                    .rename(columns={"index": "Mes"})
                )

                gastos_data = gastos_data[
                    ~gastos_data["Mes"].isin(["Total", "Promedio"])
                ]

                fig2 = px.bar(
                    gastos_data,
                    x="Mes",
                    y=columnas_gastos,
                    barmode="stack",
                    title=f"Composición de gastos por mes - {opcion}",
                    labels={"value": "Monto", "variable": "Tipo de Gasto"}
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No hay columnas de gasto disponibles para graficar.")

        with tabs[2]:
            st.subheader("Márgenes de rentabilidad")

            margenes_clave = ["% Utilidad Bruta", "% Utilidad Operativa"]
            columnas_margen = [m for m in margenes_clave if m in df_graficas.columns]

            if columnas_margen:
                fig3 = px.line(
                    df_graficas,
                    x="Mes",
                    y=columnas_margen,
                    markers=True,
                    title=f"Márgenes: Utilidad Bruta y Operativa - {opcion}",
                    labels={"value": "%", "variable": "Métrica"}
                )
                fig3.update_layout(yaxis_tickformat=".0%")
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No hay márgenes disponibles para graficar.")

        with tabs[3]:
            st.subheader("Gráfica personalizada")

            seleccion = st.multiselect(
                "Selecciona conceptos para graficar:",
                options=conceptos_disponibles,
                default=["Ingresos"] if "Ingresos" in conceptos_disponibles else []
            )

            if seleccion:
                porcentuales = [c for c in seleccion if c.startswith("%")]
                monetarias = [c for c in seleccion if not c.startswith("%")]

                fig = make_subplots(specs=[[{"secondary_y": True}]])

                for col in monetarias:
                    fig.add_trace(
                        go.Scatter(
                            x=df_graficas["Mes"],
                            y=df_graficas[col],
                            name=col,
                            mode="lines+markers"
                        ),
                        secondary_y=False
                    )

                for col in porcentuales:
                    fig.add_trace(
                        go.Scatter(
                            x=df_graficas["Mes"],
                            y=df_graficas[col],
                            name=col,
                            mode="lines+markers",
                            line=dict(dash="dot")
                        ),
                        secondary_y=True
                    )

                fig.update_yaxes(title_text="Monto ($ MXN)", secondary_y=False)
                fig.update_yaxes(title_text="Porcentaje (%)", tickformat=".0%", secondary_y=True)

                fig.update_layout(
                    title=f"Evolución de conceptos seleccionados - {opcion}",
                    xaxis_title="Mes",
                    legend_title="Conceptos",
                    hovermode="x unified"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecciona al menos un concepto para visualizar.")
    
    elif selected == "CeCo":
        texto_centrado("GASTOS POR CECO")

        col1, col2, col3 = st.columns(3)
        ceco_codigo, ceco_nombre = filtro_ceco(col1)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)

        comparativo_sel = col3.selectbox(
            "Comparar contra",
            ["LY", "PPT"],
            index=0
        )

        meses_sel = filtro_meses(st, df_2025)

        if not meses_sel:
            st.warning("Selecciona al menos un mes.")
            st.stop()

        ceco_codigo = [str(x).strip() for x in ceco_codigo]
        proyecto_codigo = [str(x).strip() for x in proyecto_codigo]

        df_cecos = df_2025.copy()
        df_cecos["CeCo_A"] = df_cecos["CeCo_A"].astype(str).str.strip()
        df_cecos["Proyecto_A"] = df_cecos["Proyecto_A"].astype(str).str.strip()
        df_cecos = df_cecos[df_cecos["CeCo_A"].isin(ceco_codigo)]
        df_cecos = df_cecos[df_cecos["Proyecto_A"].isin(proyecto_codigo)]

        df_cecos_ly = df_ly.copy()
        df_cecos_ly["CeCo_A"] = df_cecos_ly["CeCo_A"].astype(str).str.strip()
        df_cecos_ly["Proyecto_A"] = df_cecos_ly["Proyecto_A"].astype(str).str.strip()
        df_cecos_ly = df_cecos_ly[df_cecos_ly["CeCo_A"].isin(ceco_codigo)]
        df_cecos_ly = df_cecos_ly[df_cecos_ly["Proyecto_A"].isin(proyecto_codigo)]

        df_cecos_ppt = df_ppt.copy()
        df_cecos_ppt["CeCo_A"] = df_cecos_ppt["CeCo_A"].astype(str).str.strip()
        df_cecos_ppt["Proyecto_A"] = df_cecos_ppt["Proyecto_A"].astype(str).str.strip()
        df_cecos_ppt = df_cecos_ppt[df_cecos_ppt["CeCo_A"].isin(ceco_codigo)]
        df_cecos_ppt = df_cecos_ppt[df_cecos_ppt["Proyecto_A"].isin(proyecto_codigo)]

        df_comp_base = df_cecos_ly if comparativo_sel == "LY" else df_cecos_ppt

        ventanas = ["COSS", "G.ADMN"]
        tab1, tab2 = st.tabs(ventanas)

        def tabla_expandible_comp(df_real, df_comp, cat, meses_sel, key_prefix):
            columnas_merge = ["Categoria_A", "Cuenta_Nombre_A"]

            df_real_f = df_real[
                (df_real["Mes_A"].isin(meses_sel)) &
                (df_real["Clasificacion_A"] == cat)
            ].copy()

            df_comp_f = df_comp[
                (df_comp["Mes_A"].isin(meses_sel)) &
                (df_comp["Clasificacion_A"] == cat)
            ].copy()

            df_real_agg = (
                df_real_f.groupby(columnas_merge, as_index=False)["Neto_A"]
                .sum()
                .rename(columns={"Categoria_A": "Group", "Neto_A": "REAL"})
            )

            df_comp_agg = (
                df_comp_f.groupby(columnas_merge, as_index=False)["Neto_A"]
                .sum()
                .rename(columns={"Categoria_A": "Group", "Neto_A": comparativo_sel})
            )

            df_grid = pd.merge(
                df_real_agg,
                df_comp_agg,
                on=["Group", "Cuenta_Nombre_A"],
                how="outer"
            ).fillna(0)

            df_grid["DIF. NOMINAL"] = df_grid["REAL"] - df_grid[comparativo_sel]
            df_grid["% VARIACION"] = np.where(
                df_grid[comparativo_sel] != 0,
                (df_grid["DIF. NOMINAL"] / df_grid[comparativo_sel]) * 100,
                0
            )

            df_grid = df_grid.sort_values(["Group", "Cuenta_Nombre_A"]).reset_index(drop=True)

            total_real = df_grid["REAL"].sum()
            total_comp = df_grid[comparativo_sel].sum()
            total_diff = df_grid["DIF. NOMINAL"].sum()
            total_pct = (total_diff / total_comp * 100) if total_comp != 0 else 0

            currency_formatter = JsCode("""
            function(params) {
                if (params.value === null || params.value === undefined || isNaN(params.value)) return '';
                return new Intl.NumberFormat('es-MX', {
                    style: 'currency',
                    currency: 'MXN',
                    minimumFractionDigits: 2
                }).format(params.value);
            }
            """)

            percent_formatter = JsCode("""
            function(params) {
                if (params.value === null || params.value === undefined || isNaN(params.value)) return '';
                return params.value.toFixed(0) + '%';
            }
            """)

            # % VARIACION correcto para filas agrupadas
            pct_value_getter = JsCode(f"""
            function(params) {{
                if (params.node && params.node.group) {{
                    const real = params.node.aggData ? params.node.aggData["REAL"] : 0;
                    const comp = params.node.aggData ? params.node.aggData["{comparativo_sel}"] : 0;
                    if (comp && comp !== 0) {{
                        return ((real - comp) / comp) * 100;
                    }}
                    return 0;
                }}
                return params.data ? params.data["% VARIACION"] : 0;
            }}
            """)

            gb = GridOptionsBuilder.from_dataframe(
                df_grid[["Group", "Cuenta_Nombre_A", "REAL", comparativo_sel, "DIF. NOMINAL", "% VARIACION"]]
            )

            gb.configure_default_column(
                sortable=True,
                filter=True,
                resizable=True,
                groupable=True
            )

            # Agrupar como en la primera imagen
            gb.configure_column("Group", rowGroup=True, hide=True)

            gb.configure_grid_options(
                groupDefaultExpanded=0,
                suppressAggFuncInHeader=True,
                groupDisplayType="singleColumn",
                animateRows=True,
                autoGroupColumnDef={
                    "headerName": "Group",
                    "minWidth": 260,
                    "cellRendererParams": {
                        "suppressCount": False
                    }
                }
            )

            gb.configure_column("Cuenta_Nombre_A", header_name="Cuenta_Nombre_A")
            gb.configure_column("REAL", header_name="REAL", type=["numericColumn"], aggFunc="sum", valueFormatter=currency_formatter)
            gb.configure_column(comparativo_sel, header_name=comparativo_sel, type=["numericColumn"], aggFunc="sum", valueFormatter=currency_formatter)
            gb.configure_column("DIF. NOMINAL", header_name="DIF. NOMINAL", type=["numericColumn"], aggFunc="sum", valueFormatter=currency_formatter)
            gb.configure_column(
                "% VARIACION",
                header_name="% VARIACION",
                type=["numericColumn"],
                valueGetter=pct_value_getter,
                valueFormatter=percent_formatter
            )

            AgGrid(
                df_grid[["Group", "Cuenta_Nombre_A", "REAL", comparativo_sel, "DIF. NOMINAL", "% VARIACION"]],
                gridOptions=gb.build(),
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True,
                theme="streamlit",
                height=420,
                fit_columns_on_grid_load=True,
                key=f"agrid_ceco_{key_prefix}_{cat}_{comparativo_sel}_{'_'.join(meses_sel)}_{'_'.join(proyecto_codigo)}_{'_'.join(ceco_codigo)}"
            )

            df_cat_chart = (
                df_grid.groupby("Group", as_index=False)[["REAL", comparativo_sel]]
                .sum()
            )

            fig_cat = go.Figure()
            fig_cat.add_trace(go.Bar(
                x=df_cat_chart["Group"],
                y=df_cat_chart["REAL"],
                name="REAL",
                text=[f"${x:,.0f}" for x in df_cat_chart["REAL"]],
                textposition="outside"
            ))
            fig_cat.add_trace(go.Bar(
                x=df_cat_chart["Group"],
                y=df_cat_chart[comparativo_sel],
                name=comparativo_sel,
                text=[f"${x:,.0f}" for x in df_cat_chart[comparativo_sel]],
                textposition="outside"
            ))
            fig_cat.update_layout(
                title=f"{cat} - Comparativo por Categoría",
                barmode="group",
                xaxis_title="Categoría",
                yaxis_title="Monto",
                uniformtext_minsize=8,
                uniformtext_mode="hide"
            )
            st.plotly_chart(fig_cat, use_container_width=True)

            return {
                "tabla": df_grid,
                "total_real": total_real,
                "total_comp": total_comp,
                "total_diff": total_diff,
                "total_pct": total_pct
            }

        def grafica_por_proyectos(df_real_full, df_comp_full, cat, meses_sel):
            df_real_f = df_real_full[
                (df_real_full["Mes_A"].isin(meses_sel)) &
                (df_real_full["Clasificacion_A"] == cat)
            ].copy()

            df_comp_f = df_comp_full[
                (df_comp_full["Mes_A"].isin(meses_sel)) &
                (df_comp_full["Clasificacion_A"] == cat)
            ].copy()

            mapa_proyecto = dict(zip(proyectos["proyectos"].astype(str), proyectos["nombre"]))

            real_proy = (
                df_real_f.groupby("Proyecto_A", as_index=False)["Neto_A"]
                .sum()
                .rename(columns={"Neto_A": "REAL"})
            )
            comp_proy = (
                df_comp_f.groupby("Proyecto_A", as_index=False)["Neto_A"]
                .sum()
                .rename(columns={"Neto_A": comparativo_sel})
            )

            df_proj = pd.merge(real_proy, comp_proy, on="Proyecto_A", how="outer").fillna(0)
            df_proj["Proyecto"] = df_proj["Proyecto_A"].astype(str).map(mapa_proyecto).fillna(df_proj["Proyecto_A"].astype(str))
            df_proj = df_proj.sort_values("REAL", ascending=False)

            fig_proj = go.Figure()
            fig_proj.add_trace(go.Bar(
                x=df_proj["Proyecto"],
                y=df_proj["REAL"],
                name="REAL",
                text=[f"${x:,.0f}" for x in df_proj["REAL"]],
                textposition="outside"
            ))
            fig_proj.add_trace(go.Bar(
                x=df_proj["Proyecto"],
                y=df_proj[comparativo_sel],
                name=comparativo_sel,
                text=[f"${x:,.0f}" for x in df_proj[comparativo_sel]],
                textposition="outside"
            ))
            fig_proj.update_layout(
                title=f"{cat} - Comparativo por Proyecto",
                barmode="group",
                xaxis_title="Proyecto",
                yaxis_title="Monto",
                uniformtext_minsize=8,
                uniformtext_mode="hide"
            )
            st.plotly_chart(fig_proj, use_container_width=True)

        with tab1:
            st.subheader("COSS")
            resumen_coss = tabla_expandible_comp(
                df_cecos,
                df_comp_base,
                "COSS",
                meses_sel,
                "COSS"
            )
            grafica_por_proyectos(df_cecos, df_comp_base, "COSS", meses_sel)

        with tab2:
            st.subheader("G.ADMN")
            resumen_gadmn = tabla_expandible_comp(
                df_cecos,
                df_comp_base,
                "G.ADMN",
                meses_sel,
                "GADMN"
            )
            grafica_por_proyectos(df_cecos, df_comp_base, "G.ADMN", meses_sel)

        st.markdown("---")
        st.subheader("Resumen Total COSS + G.ADMN")

        total_real_cg = resumen_coss["total_real"] + resumen_gadmn["total_real"]
        total_comp_cg = resumen_coss["total_comp"] + resumen_gadmn["total_comp"]
        total_diff_cg = resumen_coss["total_diff"] + resumen_gadmn["total_diff"]
        total_pct_cg = (total_diff_cg / total_comp_cg * 100) if total_comp_cg != 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("REAL", f"${total_real_cg:,.2f}")
        c2.metric(comparativo_sel, f"${total_comp_cg:,.2f}")
        c3.metric("DIF. NOMINAL", f"${total_diff_cg:,.2f}")
        c4.metric("% VARIACION", f"{total_pct_cg:,.0f}%")

        fig_total = go.Figure()
        fig_total.add_trace(go.Bar(
            x=["COSS + G.ADMN"],
            y=[total_real_cg],
            name="REAL",
            text=[f"${total_real_cg:,.0f}"],
            textposition="outside"
        ))
        fig_total.add_trace(go.Bar(
            x=["COSS + G.ADMN"],
            y=[total_comp_cg],
            name=comparativo_sel,
            text=[f"${total_comp_cg:,.0f}"],
            textposition="outside"
        ))
        fig_total.update_layout(
            title=f"Total COSS + G.ADMN vs {comparativo_sel}",
            barmode="group",
            yaxis_title="Monto",
            uniformtext_minsize=8,
            uniformtext_mode="hide"
        )
        st.plotly_chart(fig_total, use_container_width=True)

    elif selected == "Ratios":

        st.title("📊 Análisis de Ratios Personalizados")
        df_2025["Mes_A"] = df_2025["Mes_A"].astype(str)
        df_ly["Mes_A"] = df_ly["Mes_A"].astype(str)

        # Aseguramos tipos string para comparaciones por proyecto
        df_2025["Proyecto_A"] = df_2025["Proyecto_A"].astype(str)
        df_ly["Proyecto_A"] = df_ly["Proyecto_A"].astype(str)
        df_ly["Cuenta_Nombre_A"] = df_ly["Cuenta_Nombre_A"].astype(str)
        campo_map = {
            "Clasificación": "Clasificacion_A",
            "Categoría": "Categoria_A",
            "Cuenta": "Cuenta_Nombre_A",
            "Estado de Resultado": "ER",
        }

        er_label_to_key = {
            "Ingreso": "ingreso_proyecto",
            "COSS": "coss_pro",
            "PATIO": "patio_pro",
            "COSS total": "coss_total",
            "Utilidad bruta": "utilidad_bruta",
            "G.ADMN": "gadmn_pro",
            "Utilidad operativa": "utilidad_operativa",
            "OH": "oh_pro",
            "EBIT": "ebit",
            "Gastos financieros": "gasto_fin_pro",
            "Ingresos financieros": "ingreso_fin_pro",
            "Resultado financiero": "resultado_fin",
            "EBT": "ebt",
        }
        er_labels = list(er_label_to_key.keys())
        def filtro_pro_ratios(col):
            dfv = proyectos.copy()
            dfv["proyectos"] = dfv["proyectos"].astype(str)
            dfv["nombre"] = dfv["nombre"].astype(str)

            codigo = dict(zip(dfv["nombre"], dfv["proyectos"]))
            opciones = ["ESGARI"] + sorted(dfv["nombre"].unique().tolist())

            sel = col.multiselect("Selecciona proyecto(s)", opciones, default=["ESGARI"])
            out = {}

            # ESGARI = todos los proyectos + "0"
            if "ESGARI" in sel:
                codigos_todos = dfv["proyectos"].tolist()
                codigos_esgari = codigos_todos + ["0"]  # aquí agregamos el proyecto 0
                out["ESGARI"] = codigos_esgari

            # Proyectos individuales -> sólo su código (sin 0)
            for nombre in sel:
                if nombre != "ESGARI":
                    out[nombre] = [codigo[nombre]]

            return out

        dic_proyectos = filtro_pro_ratios(st)
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        meses_disponibles = [m for m in meses_ordenados if m in df_2025["Mes_A"].unique()]
        meses_sel = st.multiselect("Selecciona meses a analizar", meses_disponibles, default=meses_disponibles)
        num_ratios = st.number_input("¿Cuántos ratios deseas analizar?", 1, 10, 1)
        ratio_config = []

        for i in range(num_ratios):
            with st.expander(f"⚙️ Configuración Ratio {i+1}", expanded=(i == 0)):

                nombre = st.text_input(f"Nombre Ratio {i+1}", f"Ratio {i+1}", key=f"ratio_name_{i}")
                col1, col2 = st.columns(2)
                # ===== NUMERADOR =====
                tipo_num = col1.selectbox("Campo Numerador", list(campo_map.keys()), key=f"tipo_num_{i}")
                if tipo_num == "Estado de Resultado":
                    valor_num = col1.selectbox("Valor Numerador", er_labels, key=f"val_num_{i}")
                else:
                    columna = campo_map[tipo_num]
                    valor_num = col1.selectbox(
                        "Valor Numerador",
                        sorted(df_2025[columna].dropna().astype(str).unique()),
                        key=f"val_val_{i}"
                    )
                add_extra_num = col1.checkbox("➕ Agregar otro valor al numerador", key=f"extra_num_check_{i}")
                extra_num = None
                if add_extra_num:
                    tipo2 = col1.selectbox("Campo adicional Numerador", list(campo_map.keys()), key=f"extra_num_tipo_{i}")
                    if tipo2 == "Estado de Resultado":
                        val2 = col1.selectbox("Valor adicional Numerador", er_labels, key=f"extra_num_val_{i}")
                    else:
                        col2map = campo_map[tipo2]
                        val2 = col1.selectbox(
                            "Valor adicional Numerador",
                            sorted(df_2025[col2map].dropna().astype(str).unique()),
                            key=f"extra_num_val2_{i}"
                        )
                    extra_num = {"campo": tipo2, "valor": val2}
                tipo_den = col2.selectbox("Campo Denominador", list(campo_map.keys()), key=f"tipo_den_{i}")

                if tipo_den == "Estado de Resultado":
                    valor_den = col2.selectbox("Valor Denominador", er_labels, key=f"val_den_{i}")
                else:
                    columna = campo_map[tipo_den]
                    valor_den = col2.selectbox(
                        "Valor Denominador",
                        sorted(df_2025[columna].dropna().astype(str).unique()),
                        key=f"val2_val_{i}"
                    )
                add_extra_den = col2.checkbox("➕ Agregar otro valor al denominador", key=f"extra_den_check_{i}")
                extra_den = None
                if add_extra_den:
                    tipo2 = col2.selectbox("Campo adicional Denominador", list(campo_map.keys()), key=f"extra_den_tipo_{i}")
                    if tipo2 == "Estado de Resultado":
                        val2 = col2.selectbox("Valor adicional Denominador", er_labels, key=f"extra_den_val_{i}")
                    else:
                        col2map = campo_map[tipo2]
                        val2 = col2.selectbox(
                            "Valor adicional Denominador",
                            sorted(df_2025[col2map].dropna().astype(str).unique()),
                            key=f"extra_den_val2_{i}"
                        )
                    extra_den = {"campo": tipo2, "valor": val2}

                ratio_config.append({
                    "nombre": nombre,
                    "campo_num": tipo_num,
                    "valor_num": valor_num,
                    "extra_num": extra_num,
                    "campo_den": tipo_den,
                    "valor_den": valor_den,
                    "extra_den": extra_den,
                })

        resultados = []
        lista_proyectos_global = proyectos["proyectos"].astype(str).tolist()

        for nombre_pro, proyecto_codigo in dic_proyectos.items():
            for mes in meses_sel:
                df_mes = df_2025[
                    (df_2025["Mes_A"] == mes) &
                    (df_2025["Proyecto_A"].isin(proyecto_codigo))
                ].copy()

                df_mes_ly = df_ly[
                    (df_ly["Mes_A"] == mes) &
                    (df_ly["Proyecto_A"].isin(proyecto_codigo))
                ].copy()

                df_mes["Cuenta_Nombre_A"] = df_mes["Cuenta_Nombre_A"].astype(str)
                df_mes_ly["Cuenta_Nombre_A"] = df_mes_ly["Cuenta_Nombre_A"].astype(str)
                # Usamos tu estado_resultado original
                er_actual = estado_resultado(
                    df_2025, [mes], nombre_pro, proyecto_codigo, lista_proyectos_global
                )
                er_ly = estado_resultado(
                    df_ly, [mes], nombre_pro, proyecto_codigo, lista_proyectos_global
                )
                for config in ratio_config:

                    # ----- NUMERADOR -----
                    if config["campo_num"] == "Estado de Resultado":
                        num = er_actual.get(er_label_to_key[config["valor_num"]], 0)
                        num_ly = er_ly.get(er_label_to_key[config["valor_num"]], 0)
                    else:
                        colname = campo_map[config["campo_num"]]
                        num = df_mes[df_mes[colname] == config["valor_num"]]["Neto_A"].sum()
                        num_ly = df_mes_ly[df_mes_ly[colname] == config["valor_num"]]["Neto_A"].sum()

                    if config["extra_num"]:
                        tipo2 = config["extra_num"]["campo"]
                        val2 = config["extra_num"]["valor"]

                        if tipo2 == "Estado de Resultado":
                            num += er_actual.get(er_label_to_key[val2], 0)
                            num_ly += er_ly.get(er_label_to_key[val2], 0)
                        else:
                            colname_extra = campo_map[tipo2]
                            num += df_mes[df_mes[colname_extra] == val2]["Neto_A"].sum()
                            num_ly += df_mes_ly[df_mes_ly[colname_extra] == val2]["Neto_A"].sum()

                    # ----- DENOMINADOR -----
                    if config["campo_den"] == "Estado de Resultado":
                        den = er_actual.get(er_label_to_key[config["valor_den"]], 0)
                        den_ly = er_ly.get(er_label_to_key[config["valor_den"]], 0)
                    else:
                        colname = campo_map[config["campo_den"]]
                        den = df_mes[df_mes[colname] == config["valor_den"]]["Neto_A"].sum()
                        den_ly = df_mes_ly[df_mes_ly[colname] == config["valor_den"]]["Neto_A"].sum()

                    if config["extra_den"]:
                        tipo2 = config["extra_den"]["campo"]
                        val2 = config["extra_den"]["valor"]

                        if tipo2 == "Estado de Resultado":
                            den += er_actual.get(er_label_to_key[val2], 0)
                            den_ly += er_ly.get(er_label_to_key[val2], 0)
                        else:
                            colname_extra = campo_map[tipo2]
                            den += df_mes[df_mes[colname_extra] == val2]["Neto_A"].sum()
                            den_ly += df_mes_ly[df_mes_ly[colname_extra] == val2]["Neto_A"].sum()

                    ratio = num / den if den != 0 else 0
                    ratio_ly = num_ly / den_ly if den_ly != 0 else 0

                    resultados.append({
                        "Mes": mes,
                        "Proyecto": nombre_pro,
                        "Nombre": config["nombre"],
                        "Ratio (%)": ratio,
                        "Ratio_LY (%)": ratio_ly,
                        "Δ Ratio (%)": ratio - ratio_ly,
                    })

        df_result = pd.DataFrame(resultados)

        if df_result.empty:
            st.info("Selecciona al menos un mes y un proyecto para calcular ratios.")
            st.stop()

        df_result["Mes"] = pd.Categorical(df_result["Mes"], categories=meses_ordenados, ordered=True)
        df_result = df_result.sort_values(["Nombre", "Proyecto", "Mes"])

        st.subheader("📈 Evolución de Ratios vs LY")

        df_plot = df_result.melt(
            id_vars=["Mes", "Proyecto", "Nombre"],
            value_vars=["Ratio (%)", "Ratio_LY (%)"],
            var_name="Tipo",
            value_name="Valor",
        )

        fig = px.line(
            df_plot,
            x="Mes",
            y="Valor",
            color="Nombre",
            line_dash="Tipo",
            markers=True,
            title="Ratios actuales vs LY (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Tabla de resultados")
        st.dataframe(df_result, use_container_width=True)

    elif selected == "Dashboard":
        st.title("📊 Dashboard Ejecutivo")

        col1, col2 = st.columns(2)
        meses_sel = filtro_meses(col1, df_2025)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)

        if not meses_sel:
            st.warning("Selecciona al menos un mes para continuar.")
        else:
            meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

            meses_graf = [m for m in meses_ordenados if m in meses_sel]
            data_dashboard = []

            for mes in meses_graf:
                er_mes = estado_resultado(df_2025, [mes], proyecto_nombre, proyecto_codigo, list_pro)
                er_ppt_mes = estado_resultado(df_ppt, [mes], proyecto_nombre, proyecto_codigo, list_pro)
                er_ly_mes = estado_resultado(df_ly, [mes], proyecto_nombre, proyecto_codigo, list_pro)

                ingreso_actual = er_mes.get("ingreso_proyecto", 0)
                ingreso_ppt = er_ppt_mes.get("ingreso_proyecto", 0)
                ingreso_ly = er_ly_mes.get("ingreso_proyecto", 0)

                data_dashboard.append({
                    "Mes": mes,

                    "Ingreso Actual": ingreso_actual,
                    "Ingreso PPT": ingreso_ppt,
                    "Ingreso LY": ingreso_ly,
                    "UO Actual %": er_mes.get("por_utilidad_operativa", 0),

                    "COSS Actual": er_mes.get("coss_total", 0),
                    "COSS PPT": er_ppt_mes.get("coss_total", 0),
                    "COSS LY": er_ly_mes.get("coss_total", 0),

                    "G.ADMN Actual": er_mes.get("gadmn_pro", 0),
                    "G.ADMN PPT": er_ppt_mes.get("gadmn_pro", 0),
                    "G.ADMN LY": er_ly_mes.get("gadmn_pro", 0),

                    "Gasto Fin Actual": er_mes.get("gasto_fin_pro", 0),

                    "Var vs PPT": ingreso_actual - ingreso_ppt,
                    "Var vs LY": ingreso_actual - ingreso_ly,
                    "Var % vs PPT": ((ingreso_actual / ingreso_ppt) - 1) if ingreso_ppt != 0 else 0,
                    "Var % vs LY": ((ingreso_actual / ingreso_ly) - 1) if ingreso_ly != 0 else 0,
                })

            df_dash = pd.DataFrame(data_dashboard)

            objetivo_uo = {
                "ARRAYANES": 0.24,
                "CENTRAL OTROS": 0.34,
                "CHALCO": 0.24,
                "CONTINENTAL": 0.30,
                "FLEX DEDICADO": 0.27,
                "FLEX SPOT": 0.24,
                "INTERNACIONAL FWD": 0.24,
                "WH": 0.21,
                "MANZANILLO": 0.25,
                "BAJIO": 0.26,
                "ESGARI": 0.25
            }

            meta_uo = objetivo_uo.get(proyecto_nombre, 0.25)
            er = estado_resultado(df_2025, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)
            er_ppt = estado_resultado(df_ppt, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)
            er_ly = estado_resultado(df_ly, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)

            c1, c2 = st.columns(2)
            c1.metric(
                "Ingreso",
                f"${er['ingreso_proyecto']:,.0f}",
                f"vs PPT: {((er['ingreso_proyecto'] / er_ppt['ingreso_proyecto']) - 1) * 100:.1f}%" if er_ppt["ingreso_proyecto"] != 0 else "N/A"
            )
            c2.metric(
                "Utilidad Operativa",
                f"${er['utilidad_operativa']:,.0f}",
                f"{er['por_utilidad_operativa'] * 100:.1f}%"
            )

            col_g1, col_g2 = st.columns(2)

            with col_g1:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso Actual"],
                    name="Ingreso Actual",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso Actual"]],
                    textposition="outside"
                ))
                fig2.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso PPT"],
                    name="Ingreso Presupuesto",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso PPT"]],
                    textposition="outside"
                ))
                fig2.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso LY"],
                    name="Ingreso LY",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso LY"]],
                    textposition="outside"
                ))
                fig2.update_layout(
                    title="Ingreso vs PPT vs LY",
                    barmode="group",
                    xaxis_title="Mes",
                    yaxis_title="Monto",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col_g2:
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["UO Actual %"],
                    name="Utilidad Operativa Actual",
                    text=[f"{x:.1%}" for x in df_dash["UO Actual %"]],
                    textposition="outside"
                ))
                fig3.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=[meta_uo] * len(df_dash),
                    name="Utilidad Operativa Objetivo",
                    text=[f"{meta_uo:.1%}"] * len(df_dash),
                    textposition="outside"
                ))
                fig3.update_layout(
                    title="Utilidad Operativa vs Objetivo",
                    barmode="group",
                    xaxis_title="Mes",
                    yaxis_title="Margen",
                    yaxis_tickformat=".0%",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig3, use_container_width=True)

            col_g3, col_g4 = st.columns(2)

            with col_g3:
                fig6 = go.Figure()
                fig6.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["COSS Actual"],
                    name="COSS Actual",
                    text=[f"${x:,.0f}" for x in df_dash["COSS Actual"]],
                    textposition="outside"
                ))
                fig6.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["COSS PPT"],
                    name="COSS Presupuesto",
                    text=[f"${x:,.0f}" for x in df_dash["COSS PPT"]],
                    textposition="outside"
                ))
                fig6.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["COSS LY"],
                    name="COSS LY",
                    text=[f"${x:,.0f}" for x in df_dash["COSS LY"]],
                    textposition="outside"
                ))
                fig6.update_layout(
                    title="COSS vs PPT vs LY",
                    barmode="group",
                    xaxis_title="Mes",
                    yaxis_title="Monto",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig6, use_container_width=True)

            with col_g4:
                fig7 = go.Figure()
                fig7.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["G.ADMN Actual"],
                    name="G.ADMN Actual",
                    text=[f"${x:,.0f}" for x in df_dash["G.ADMN Actual"]],
                    textposition="outside"
                ))
                fig7.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["G.ADMN PPT"],
                    name="G.ADMN Presupuesto",
                    text=[f"${x:,.0f}" for x in df_dash["G.ADMN PPT"]],
                    textposition="outside"
                ))
                fig7.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["G.ADMN LY"],
                    name="G.ADMN LY",
                    text=[f"${x:,.0f}" for x in df_dash["G.ADMN LY"]],
                    textposition="outside"
                ))
                fig7.update_layout(
                    title="G.ADMN vs PPT vs LY",
                    barmode="group",
                    xaxis_title="Mes",
                    yaxis_title="Monto",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide"
                )
                st.plotly_chart(fig7, use_container_width=True)

            col_g5, col_g6 = st.columns(2)

            with col_g5:
                fig5 = go.Figure(data=[
                    go.Pie(
                        labels=["COSS", "G.ADMN"],
                        values=[
                            er["coss_total"],
                            er["gadmn_pro"]
                        ],
                        hole=0.4,
                        textinfo="label+percent+value"
                    )
                ])
                fig5.update_layout(title="Composición de los gastos")
                st.plotly_chart(fig5, use_container_width=True)

            with col_g6:
                fig8 = go.Figure()

                fig8.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso Actual"],
                    name="Ingreso Actual",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso Actual"]],
                    textposition="outside"
                ))

                fig8.add_trace(go.Scatter(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso PPT"],
                    name="Ingreso PPT",
                    mode="lines+markers+text",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso PPT"]],
                    textposition="top center"
                ))

                fig8.add_trace(go.Scatter(
                    x=df_dash["Mes"],
                    y=df_dash["Ingreso LY"],
                    name="Ingreso LY",
                    mode="lines+markers+text",
                    text=[f"${x:,.0f}" for x in df_dash["Ingreso LY"]],
                    textposition="bottom center"
                ))

                fig8.update_layout(
                    title="Tendencia de Ingreso: Actual vs PPT vs LY",
                    xaxis_title="Mes",
                    yaxis_title="Monto",
                    barmode="group"
                )

                st.plotly_chart(fig8, use_container_width=True)

            st.subheader("Variación de ingreso")
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                fig9 = go.Figure()
                fig9.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Var vs PPT"],
                    name="Variación $ vs PPT",
                    text=[f"${x:,.0f}" for x in df_dash["Var vs PPT"]],
                    textposition="outside"
                ))
                fig9.update_layout(
                    title="Variación de ingreso vs PPT ($)",
                    xaxis_title="Mes",
                    yaxis_title="Variación $"
                )
                st.plotly_chart(fig9, use_container_width=True)

            with col_v2:
                fig10 = go.Figure()
                fig10.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Var % vs PPT"],
                    name="Variación % vs PPT",
                    text=[f"{x:.1%}" for x in df_dash["Var % vs PPT"]],
                    textposition="outside"
                ))
                fig10.add_trace(go.Bar(
                    x=df_dash["Mes"],
                    y=df_dash["Var % vs LY"],
                    name="Variación % vs LY",
                    text=[f"{x:.1%}" for x in df_dash["Var % vs LY"]],
                    textposition="outside"
                ))
                fig10.update_layout(
                    title="Variación de ingreso vs PPT y LY (%)",
                    barmode="group",
                    xaxis_title="Mes",
                    yaxis_title="Variación %",
                    yaxis_tickformat=".0%"
                )
                st.plotly_chart(fig10, use_container_width=True)

        st.subheader("Ingresos Proyectados")

        def calcular_proyeccion_ingresos(
            df_2025: pd.DataFrame,
            mes_act: str,
            fecha_actualizacion: pd.DataFrame,
            pro: str,
            codigo_pro,                 # list[str] o str
            modo: str = "lineal",       # "lineal" | "historico"
            cargar_datos=None,          # callable(url) -> DataFrame (requerido si modo="historico")
            ingreso_sem_url: str = None
        ) -> float:
            fecha_completa = fecha_actualizacion['fecha'].iloc[0]
            fecha_act = fecha_completa.day
            ultimo_dia_mes = (fecha_completa + pd.offsets.MonthEnd(0)).day

            df_mes = df_2025[(df_2025["Mes_A"] == mes_act) & (df_2025["Categoria_A"] == "INGRESO")]
            if pro != "ESGARI":
                cods = codigo_pro if isinstance(codigo_pro, list) else [codigo_pro]
                df_mes = df_mes[df_mes["Proyecto_A"].isin(cods)]

            if modo == "lineal":
                base = df_mes["Neto_A"].sum()
                return float(base / max(fecha_act, 1) * ultimo_dia_mes)

            if modo == "historico":
                if cargar_datos is None or ingreso_sem_url is None:
                    raise ValueError("Para modo 'historico' debes pasar cargar_datos e ingreso_sem_url.")

                df_hist = cargar_datos(ingreso_sem_url).copy()

                df_hist["fecha"] = pd.to_datetime(df_hist["fecha"], errors="coerce")
                df_hist["dia"] = df_hist["fecha"].dt.day

                df_hist["proyecto"] = (
                    pd.to_numeric(df_hist["proyecto"], errors="coerce")
                    .astype("Int64")
                    .astype(str)
                )

                df_hist["ingreso"] = pd.to_numeric(df_hist["ingreso"], errors="coerce").fillna(0)

                idx = (df_hist["dia"] - fecha_act).abs().idxmin()
                dia_ref = int(df_hist.loc[idx, "dia"])

                df_va = df_hist[df_hist["dia"] == dia_ref].copy()
                df_va["ingreso_va"] = df_va["ingreso"] / max(dia_ref, 1) * fecha_act
                df_va = df_va[["proyecto", "ingreso_va"]]

                df_fin = df_hist[df_hist["semana"] == 4].copy()
                df_fin = df_fin[["proyecto", "ingreso"]].rename(columns={"ingreso": "ingreso_fin"})

                df_merged = pd.merge(df_va, df_fin, on="proyecto", how="inner")

                df_merged["ingreso_dividido"] = np.where(
                    df_merged["ingreso_fin"] != 0,
                    df_merged["ingreso_va"] / df_merged["ingreso_fin"],
                    np.nan
                )

                df_merged["ingreso_dividido"] = (
                    pd.to_numeric(df_merged["ingreso_dividido"], errors="coerce")
                    .replace([np.inf, -np.inf], np.nan)
                )

                df_proy = (
                    df_2025[
                        (df_2025["Mes_A"] == mes_act) &
                        (df_2025["Categoria_A"] == "INGRESO")
                    ]
                    .groupby("Proyecto_A", as_index=False)["Neto_A"]
                    .sum()
                )

                df_proy["Proyecto_A"] = (
                    pd.to_numeric(df_proy["Proyecto_A"], errors="coerce")
                    .astype("Int64")
                    .astype(str)
                )

                df_proy = pd.merge(
                    df_proy,
                    df_merged[["proyecto", "ingreso_dividido"]],
                    left_on="Proyecto_A",
                    right_on="proyecto",
                    how="left"
                )

                df_proy["Neto_A"] = np.where(
                    df_proy["ingreso_dividido"].notna() & (df_proy["ingreso_dividido"] != 0),
                    df_proy["Neto_A"] / df_proy["ingreso_dividido"],
                    df_proy["Neto_A"]
                )

                df_proy["Neto_A"] = (
                    pd.to_numeric(df_proy["Neto_A"], errors="coerce")
                    .replace([np.inf, -np.inf], np.nan)
                    .fillna(0)
                )

                if pro == "ESGARI":
                    return float(df_proy["Neto_A"].sum())

                cods = codigo_pro if isinstance(codigo_pro, list) else [codigo_pro]
                cods = [str(x).strip() for x in cods]

                return float(df_proy[df_proy["Proyecto_A"].isin(cods)]["Neto_A"].sum())

            raise ValueError("modo debe ser 'lineal' o 'historico'")
        def ingre_co(df):
            if proyecto_nombre != "ESGARI":
                df = df[df["Proyecto_A"].isin(proyecto_codigo)]
            df = df[df["Categoria_A"] == "INGRESO"]
            df = df.groupby("Mes_A", as_index=False).agg({"Neto_A": "sum"})
            return df

        df_co_2025 = ingre_co(df_2025)
        df_co_ly = ingre_co(df_ly)
        df_co_ppt = ingre_co(df_ppt)

        # ---------- Mes actual (formato "ene.","feb.",...) ----------
        orden_meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                    "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
        mes_map = {1:"ene.", 2:"feb.", 3:"mar.", 4:"abr.", 5:"may.", 6:"jun.",
                7:"jul.", 8:"ago.", 9:"sep.", 10:"oct.", 11:"nov.", 12:"dic."}
        fecha_hoy = fecha_actualizacion['fecha'].iloc[0]
        mes_act = mes_map[int(fecha_hoy.month)]

        # ---------- UI: Real vs Proyección en el mes actual ----------
        colA, colB = st.columns([1,1])
        vista_mes_actual = colA.radio(
            f"Mes actual ({mes_act})",
            options=["Ver real", "Ver proyección"],
            horizontal=True,
            index=0,
            key="vista_mes_actual_ing"
        )
        tipo_proy = None
        if vista_mes_actual == "Ver proyección":
            tipo_proy = colB.selectbox(
                "Tipo de proyección",
                options=["Lineal", "Histórica"],
                index=0,
                key="tipo_proy_ing"
            )

        # ---------- Asegurar que todos los meses estén presentes ----------
        df_base = pd.DataFrame({"Mes_A": orden_meses})

        def asegurar_meses(df, col_name):
            df = df_base.merge(df, on="Mes_A", how="left")
            df.rename(columns={"Neto_A": col_name}, inplace=True)
            return df

        df_co_2025 = asegurar_meses(df_co_2025, "Actual")
        df_co_ly   = asegurar_meses(df_co_ly,   "Año Anterior")
        df_co_ppt  = asegurar_meses(df_co_ppt,  "Presupuesto")

        # ---------- Si se elige proyección, reemplazar SOLO el mes actual en "Actual" ----------
        ingreso_pro_fut = None
        if vista_mes_actual == "Ver proyección":
            modo = "lineal" if tipo_proy == "Lineal" else "historico"
            ingreso_pro_fut = calcular_proyeccion_ingresos(
                df_2025=df_2025,
                mes_act=mes_act,
                fecha_actualizacion=fecha_actualizacion,
                pro=proyecto_nombre,
                codigo_pro=proyecto_codigo,
                modo=modo,
                cargar_datos=cargar_datos if modo == "historico" else None,
                ingreso_sem_url=("https://docs.google.com/spreadsheets/d/14l6QLudSBpqxmfuwRqVxCXzhSFzRL0AqWJqVuIOaFFQ/export?format=xlsx")
            )
            # Reemplazo in-place del valor del mes actual en la columna "Actual"
            df_co_2025.loc[df_co_2025["Mes_A"] == mes_act, "Actual"] = ingreso_pro_fut

        # ---------- Unir todas las series ----------
        df_final = df_base.copy()
        df_final = df_final.merge(df_co_2025, on="Mes_A", how="left")
        df_final = df_final.merge(df_co_ly,   on="Mes_A", how="left")
        df_final = df_final.merge(df_co_ppt,  on="Mes_A", how="left")

        # ---------- Mostrar métrica del mes actual ----------
        # Si no hay proyección, muestra el real; si hay proyección, la proyección.
        valor_mes_actual = df_final.loc[df_final["Mes_A"] == mes_act, "Actual"].values[0]
        etiqueta = "Ingreso proyectado del mes" if vista_mes_actual == "Ver proyección" else "Ingreso real del mes"
 

        # ---------- Gráfico ----------
        df_melted = df_final.melt(id_vars="Mes_A", var_name="Tipo", value_name="Ingresos")
        df_melted["Ingresos_miles"] = (df_melted["Ingresos"] / 1000).round(0)
        df_melted["Texto"] = df_melted["Ingresos_miles"].apply(lambda x: f"${int(x):,}" if pd.notnull(x) else "")

        fig = px.line(
            df_melted,
            x="Mes_A",
            y="Ingresos_miles",
            color="Tipo",
            markers=True,
            title="Ingresos Comerciales por Mes (en miles de $)"
        )
        for tipo in df_melted["Tipo"].unique():
            fig.update_traces(
                selector=dict(name=tipo),
                text=df_melted[df_melted["Tipo"] == tipo]["Texto"],
                textposition="top center",
                mode="lines+markers+text"
            )
        fig.update_layout(yaxis_tickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)
    

    elif selected == "OH":

        st.title("Composición Overhead (OH)")

        col1, col2 = st.columns(2)
        meses_seleccionado = filtro_meses(col1, df_2025)
        ceco_codigo, ceco_nombre = filtro_ceco(col2)

        tipo_dato = st.selectbox(
            "Selecciona el tipo de información a mostrar:",
            options=["OH", "Presupuesto", "LY"]
        )

        def tabla_OH_2(df_2025, df_ppt, df_ly, meses_seleccionados, titulo, codigos_ceco, tipo_dato, ceco_seleccionado):
            st.subheader(titulo)

            codigos_oh = ["8002", "8004"]
            clasificaciones_validas = ["COSS", "G.ADMN"]
            meses_filtrados = meses_seleccionados
            meses_orden = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

            df_2025_n = df_2025.copy()
            df_ppt_n  = df_ppt.copy()
            df_ly_n   = df_ly.copy()

            def filtrar_datos(df):
                if df is None or df.empty:
                    return pd.DataFrame()

                df = df.copy()
                df["Mes_A"] = df["Mes_A"].astype(str).str.strip()
                df["Proyecto_A"] = df["Proyecto_A"].astype(str).str.strip()
                df["Clasificacion_A"] = df["Clasificacion_A"].astype(str).str.strip()

                if "CeCo_A" in df.columns:
                    df["CeCo_A"] = df["CeCo_A"].astype(str).str.strip()

                # 1) filtro base
                df_filt = df[
                    (df["Mes_A"].isin(meses_filtrados)) &
                    (df["Proyecto_A"].isin(codigos_oh)) &
                    (df["Clasificacion_A"].isin(clasificaciones_validas))
                ].copy()

                # 2) regla CECO
                if "CeCo_A" in df_filt.columns:
                    if str(ceco_seleccionado).strip().upper() == "ESGARI":
                        pass
                    else:
                        if codigos_ceco:
                            cecos_norm = [str(x).strip() for x in codigos_ceco]
                            df_filt = df_filt[df_filt["CeCo_A"].isin(cecos_norm)]

                return df_filt

            df_real     = filtrar_datos(df_2025_n)
            df_ppt_filt = filtrar_datos(df_ppt_n)
            df_ly_filt  = filtrar_datos(df_ly_n)

            if df_real.empty and tipo_dato == "OH":
                st.warning("⚠️ No hay datos reales para los filtros seleccionados.")
                return

            def resumir(df, nombre_col):
                if df.empty:
                    return pd.DataFrame({"Mes_A": meses_filtrados, nombre_col: [0] * len(meses_filtrados)})
                return (
                    df.groupby("Mes_A")["Neto_A"]
                    .sum()
                    .reindex(meses_filtrados, fill_value=0)
                    .reset_index()
                    .rename(columns={"Neto_A": nombre_col})
                )

            resumen_real = resumir(df_real, "OH_Real")
            resumen_ppt  = resumir(df_ppt_filt, "OH_Presupuesto")
            resumen_ly   = resumir(df_ly_filt, "OH_LY")

            tipo = tipo_dato.strip().upper()

            if tipo == "OH":
                comparativo = resumen_ppt
                col_compara = "OH_Presupuesto"
                label_compara = "Presupuesto"
                df_base_grid = df_real.copy()

            elif tipo == "PRESUPUESTO":
                comparativo = resumen_ppt
                col_compara = "OH_Presupuesto"
                label_compara = "Presupuesto"
                df_base_grid = df_ppt_filt.copy()

            elif tipo == "LY":
                comparativo = resumen_ly
                col_compara = "OH_LY"
                label_compara = "Año Anterior (LY)"
                df_base_grid = df_ly_filt.copy()

            else:
                st.warning("Selecciona 'OH', 'Presupuesto' o 'LY'.")
                return

            resumen = resumen_real.merge(comparativo, on="Mes_A", how="outer").fillna(0)
            resumen["Diferencia"] = resumen["OH_Real"] - resumen[col_compara]
            resumen["% Diferencia"] = resumen.apply(
                lambda x: (x["Diferencia"] / x[col_compara]) if x[col_compara] != 0 else 0,
                axis=1
            )

            # --- Tabla resumen con TOTAL ---
            resumen_fmt = resumen.copy()
            for c in ["OH_Real", col_compara, "Diferencia"]:
                resumen_fmt[c] = resumen_fmt[c].apply(lambda x: f"${x:,.2f}")
            resumen_fmt["% Diferencia"] = resumen["% Diferencia"].apply(lambda x: f"{x:.2%}")

            total_real = float(resumen["OH_Real"].sum())
            total_comp = float(resumen[col_compara].sum())
            total_diff = float(resumen["Diferencia"].sum())
            total_pct  = (total_diff / total_comp) if total_comp != 0 else 0

            total_row = pd.DataFrame([{
                "Mes_A": "TOTAL",
                "OH_Real": f"${total_real:,.2f}",
                col_compara: f"${total_comp:,.2f}",
                "Diferencia": f"${total_diff:,.2f}",
                "% Diferencia": f"{total_pct:.2%}",
            }])

            resumen_fmt_total = pd.concat([resumen_fmt, total_row], ignore_index=True)

            st.dataframe(
                resumen_fmt_total.rename(columns={
                    "Mes_A": "Mes",
                    "OH_Real": "Real (MXN)",
                    col_compara: label_compara,
                    "Diferencia": "Diferencia",
                    "% Diferencia": "% Diferencia"
                })[["Mes", "Real (MXN)", label_compara, "Diferencia", "% Diferencia"]],
                use_container_width=True,
                hide_index=True
            )

            # --- Gráfica ---
            fig = px.bar(
                resumen,
                x="Mes_A",
                y=["OH_Real", col_compara],
                barmode="group",
                labels={"value": "Monto (MXN)", "variable": "Tipo"},
                title=f"Comparativa OH: Real vs {label_compara}",
                height=420
            )
            fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
            fig.update_layout(
                template="plotly_white",
                xaxis=dict(title="Mes", tickangle=-45, categoryorder="array", categoryarray=meses_orden),
                yaxis=dict(title="Monto (MXN)", tickformat=","),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- AgGrid detalle ---
            if df_base_grid.empty:
                st.info("No hay detalle para mostrar en la tabla.")
                return

            df_pivot = (
                df_base_grid.groupby(
                    ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A", "Mes_A"],
                    as_index=False
                )["Neto_A"]
                .sum()
            )

            df_pivot = df_pivot.pivot_table(
                index=["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"],
                columns="Mes_A",
                values="Neto_A",
                aggfunc="sum",
                fill_value=0
            ).reset_index()

            columnas_meses = [m for m in meses_orden if m in df_pivot.columns]
            columnas_finales = ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"] + columnas_meses

            df_pivot = df_pivot[columnas_finales].copy()
            df_pivot["Total"] = df_pivot[columnas_meses].sum(axis=1)

            gb = GridOptionsBuilder.from_dataframe(df_pivot)

            gb.configure_column("Clasificacion_A", rowGroup=True, hide=True)
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)
            gb.configure_column("Cuenta_Nombre_A", pinned="left")

            currency_formatter = JsCode("""
                function(params) {
                    if (params.value === 0 || params.value === null || params.value === undefined) {
                        return "$0.00";
                    }
                    return new Intl.NumberFormat('es-MX', {
                        style: 'currency',
                        currency: 'MXN'
                    }).format(params.value);
                }
            """)

            for col in df_pivot.columns:
                if col not in ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"]:
                    gb.configure_column(
                        col,
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        aggFunc="sum",
                        valueFormatter=currency_formatter,
                        cellStyle={"textAlign": "right"}
                    )

            gridOptions = gb.build()

            st.write("### Tabla Clasificación, Categoría y Cuenta")
            AgGrid(
                df_pivot,
                gridOptions=gridOptions,
                enable_enterprise_modules=True,
                fit_columns_on_grid_load=False,
                allow_unsafe_jscode=True,
                domLayout="normal",
                height=600,
                theme="streamlit",
                key=f"agrid_oh_{tipo}_{'_'.join(meses_filtrados)}_{ceco_seleccionado}"
            )

        tabla_OH_2(
            df_2025,
            df_ppt,
            df_ly,
            meses_seleccionado,
            f"Composición de OH - {tipo_dato}",
            ceco_codigo,
            tipo_dato,
            ceco_seleccionado=ceco_nombre
        )

    elif selected == "Balance General":
        def tabla_balance_por_empresa():
            st.subheader("Balance General por Empresa")

            df_mapeo_local = cargar_mapeo(mapeo_url)
            if df_mapeo_local.empty:
                st.stop()

            data_empresas = cargar_balance_multi_hojas(balance_url, EMPRESAS)
            resultados_balance = []
            balances_detallados = {}
            cuentas_no_mapeadas = []

            for empresa in EMPRESAS:
                df = data_empresas.get(empresa, pd.DataFrame()).copy()
                if df.empty:
                    continue

                col_cuenta = _encontrar_columna(df, COLUMNAS_CUENTA)
                col_monto = _encontrar_columna(df, COLUMNAS_MONTO)

                if not col_cuenta or not col_monto:
                    st.warning(f"⚠️ {empresa}: columnas inválidas (Cuenta / Saldo).")
                    continue

                df[col_cuenta] = df[col_cuenta].apply(limpiar_cuenta)
                df[col_monto] = _to_numeric_money(df[col_monto])
                df = df.dropna(subset=[col_cuenta])
                df = df.groupby(col_cuenta, as_index=False)[col_monto].sum()

                df_merged = df.merge(
                    df_mapeo_local[["Cuenta", "CLASIFICACION", "CATEGORIA"]],
                    left_on=col_cuenta,
                    right_on="Cuenta",
                    how="left",
                )

                df_merged["EN_MAPEO"] = df_merged["CLASIFICACION"].notna()
                df_merged = autoclasificar_resultados(df_merged, col_cuenta)

                no_mapeadas = df_merged[~df_merged["EN_MAPEO"]].copy()
                if not no_mapeadas.empty:
                    no_mapeadas["EMPRESA"] = empresa
                    cols_keep = [c for c in [col_cuenta, col_monto, "EMPRESA"] if c in no_mapeadas.columns]
                    cuentas_no_mapeadas.append(
                        no_mapeadas[cols_keep].rename(columns={col_cuenta: "Cuenta", col_monto: "Saldo"})
                    )

                df_merged = df_merged[~df_merged["CLASIFICACION"].isna()].copy()
                if df_merged.empty:
                    st.warning(f"⚠️ {empresa}: sin coincidencias con el mapeo.")
                    continue

                df_balance = df_merged[df_merged["CLASIFICACION"].isin(["ACTIVO", "PASIVO", "CAPITAL"])].copy()
                if df_balance.empty:
                    st.warning(f"⚠️ {empresa}: sin coincidencias para BALANCE (ACTIVO/PASIVO/CAPITAL).")
                    continue

                resumen = (
                    df_balance.groupby(["CLASIFICACION", "CATEGORIA"])[col_monto]
                    .sum()
                    .reset_index()
                    .rename(columns={col_monto: empresa})
                )

                resultados_balance.append(resumen)
                balances_detallados[empresa] = df_merged.copy()

            if not resultados_balance:
                st.error("❌ No se pudo generar información consolidada.")
                return

            data_resultados = []
            for empresa in EMPRESAS:
                df_raw = data_empresas.get(empresa, pd.DataFrame()).copy()
                if df_raw.empty:
                    continue

                col_cuenta_raw = _encontrar_columna(df_raw, COLUMNAS_CUENTA)
                col_monto_raw = _encontrar_columna(df_raw, COLUMNAS_MONTO)

                if not col_cuenta_raw or not col_monto_raw:
                    st.warning(f"⚠️ {empresa}: no encontré columnas de Cuenta/Saldo para resultados.")
                    continue

                df_raw[col_cuenta_raw] = df_raw[col_cuenta_raw].apply(limpiar_cuenta)
                df_raw[col_monto_raw] = _to_numeric_money(df_raw[col_monto_raw])
                df_raw = df_raw.dropna(subset=[col_cuenta_raw])
                df_cta = df_raw.groupby(col_cuenta_raw, as_index=False)[col_monto_raw].sum()

                ingreso = df_cta.loc[
                    (df_cta[col_cuenta_raw] > 400000000) & (df_cta[col_cuenta_raw] < 500000000),
                    col_monto_raw
                ].sum()

                gasto = df_cta.loc[
                    (df_cta[col_cuenta_raw] > 500000000),
                    col_monto_raw
                ].sum()

                utilidad = ingreso + gasto

                data_resultados.append({
                    "EMPRESA": empresa,
                    "INGRESO": float(ingreso),
                    "GASTO": float(gasto),
                    "UTILIDAD": float(utilidad),
                })

            df_resultados = pd.DataFrame(data_resultados)

            st.markdown("### Estado de Resultados por Empresa")
            if df_resultados.empty:
                st.info("No se pudo calcular estado de resultados")
            else:
                df_resultados_t = (
                    df_resultados.set_index("EMPRESA")
                    .T
                    .reset_index()
                    .rename(columns={"index": "CONCEPTO"})
                )

                df_resultados_t["TOTAL"] = df_resultados_t[
                    [c for c in df_resultados_t.columns if c != "CONCEPTO"]
                ].sum(axis=1)

                for col in df_resultados_t.columns:
                    if col != "CONCEPTO":
                        df_resultados_t[col] = df_resultados_t[col].apply(lambda x: f"${x:,.2f}")

                st.dataframe(df_resultados_t, use_container_width=True, hide_index=True)

            utilidad_por_empresa = {}
            utilidad_total = 0.0

            if not df_resultados.empty:
                utilidad_por_empresa = df_resultados.set_index("EMPRESA")["UTILIDAD"].to_dict()
                utilidad_total = float(df_resultados["UTILIDAD"].sum())

            df_final = reduce(
                lambda l, r: pd.merge(l, r, on=["CLASIFICACION", "CATEGORIA"], how="outer"),
                resultados_balance
            ).fillna(0)

            for emp in EMPRESAS:
                if emp not in df_final.columns:
                    df_final[emp] = 0.0

            df_final["TOTAL ACUMULADO"] = df_final[EMPRESAS].sum(axis=1)

            total_capital_con_utilidad = None

            for clasif in CLASIFICACIONES_PRINCIPALES:
                st.markdown(f"### {clasif}")
                df_clasif = df_final[df_final["CLASIFICACION"] == clasif].copy()

                if df_clasif.empty:
                    st.info(f"No hay cuentas clasificadas como {clasif}.")
                    continue

                # Agregar la utilidad como fila visible dentro de CAPITAL
                if clasif == "CAPITAL" and utilidad_por_empresa:
                    fila_utilidad = pd.DataFrame({
                        "CLASIFICACION": [clasif],
                        "CATEGORIA": ["UTILIDAD DEL EJERCICIO"]
                    })

                    for emp in EMPRESAS:
                        fila_utilidad[emp] = float(utilidad_por_empresa.get(emp, 0.0))

                    fila_utilidad["TOTAL ACUMULADO"] = fila_utilidad[EMPRESAS].sum(axis=1)

                    df_clasif = pd.concat([df_clasif, fila_utilidad], ignore_index=True)

                # Subtotal ya incluyendo utilidad
                subtotal = pd.DataFrame({
                    "CLASIFICACION": [clasif],
                    "CATEGORIA": [f"TOTAL {clasif}"]
                })

                for col in EMPRESAS + ["TOTAL ACUMULADO"]:
                    subtotal[col] = df_clasif[col].sum()

                df_clasif = pd.concat([df_clasif, subtotal], ignore_index=True)

                if clasif == "CAPITAL":
                    total_capital_con_utilidad = float(subtotal["TOTAL ACUMULADO"].iloc[0])

                df_show = df_clasif.copy()
                for col in EMPRESAS + ["TOTAL ACUMULADO"]:
                    df_show[col] = df_show[col].apply(lambda x: f"${x:,.2f}")

                with st.expander(f"{clasif}", expanded=(clasif == "CAPITAL")):
                    st.dataframe(
                        df_show.drop(columns=["CLASIFICACION"]),
                        use_container_width=True,
                        hide_index=True
                    )

                    if clasif == "CAPITAL" and utilidad_por_empresa:
                        st.markdown("La utilidad del ejercicio fue integrada y mostrada dentro del capital.")


            totales = {
                c: df_final[df_final["CLASIFICACION"] == c]["TOTAL ACUMULADO"].sum()
                for c in CLASIFICACIONES_PRINCIPALES
            }

            if total_capital_con_utilidad is not None:
                totales["CAPITAL"] = total_capital_con_utilidad

            diferencia = totales["ACTIVO"] + (totales["PASIVO"] + totales["CAPITAL"])

            resumen_final = pd.DataFrame({
                "Concepto": ["TOTAL ACTIVO", "TOTAL PASIVO", "TOTAL CAPITAL", "DIFERENCIA"],
                "Monto Total": [
                    f"${totales['ACTIVO']:,.2f}",
                    f"${totales['PASIVO']:,.2f}",
                    f"${totales['CAPITAL']:,.2f}",
                    f"${diferencia:,.2f}",
                ]
            })

            st.markdown("### Resumen Consolidado")
            st.dataframe(resumen_final, use_container_width=True, hide_index=True)

            if abs(diferencia) < 1:
                st.success("✅ El balance está cuadrado (ACTIVO = PASIVO + CAPITAL).")
            else:
                st.error("❌ El balance no cuadra. Revisa cuentas/mapeo.")

            if cuentas_no_mapeadas:
                st.markdown("## ⚠️ Cuentas NO mapeadas detectadas (NO existen en el mapeo)")
                df_no_map = pd.concat(cuentas_no_mapeadas, ignore_index=True)

                if "Saldo" in df_no_map.columns:
                    df_no_map_res = (
                        df_no_map.groupby("Cuenta", as_index=False)["Saldo"]
                        .sum()
                        .sort_values("Saldo", ascending=False)
                    )

                st.markdown("### Detalle de cuentas no mapeadas")
                cols_orden = [c for c in ["EMPRESA", "Cuenta", "Descripcion", "Saldo"] if c in df_no_map.columns]
                st.dataframe(
                    df_no_map[cols_orden].sort_values(cols_orden[:2]),
                    use_container_width=True,
                    hide_index=True
                )

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                for empresa, df_emp in balances_detallados.items():
                    df_emp.to_excel(writer, index=False, sheet_name=empresa[:31])
                df_final.to_excel(writer, index=False, sheet_name="Consolidado")
                resumen_final.to_excel(writer, index=False, sheet_name="Resumen")
                if not df_resultados.empty:
                    df_resultados.to_excel(writer, index=False, sheet_name="Resultados")

            st.download_button(
                label="💾 Descargar Excel Consolidado",
                data=output.getvalue(),
                file_name="Balance_Consolidado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            return
        tabla_balance_por_empresa()

    elif selected == "Balance por empresa":
        st.markdown("""
        <style>
        .stApp {
            background: #f4f7fb;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        .header-pill{
            background: linear-gradient(90deg, #163a5f 0%, #214a6b 100%);
            color: white;
            padding: 12px 18px;
            border-radius: 12px;
            font-weight: 800;
            display: inline-block;
            box-shadow: 0 8px 18px rgba(20, 58, 95, 0.22);
            margin-bottom: 10px;
        }
        .sub-pill{
            background: #214a6b;
            color: white;
            padding: 8px 12px;
            border-radius: 10px;
            font-weight: 700;
            display: inline-block;
            margin: 6px 0px 10px 0px;
        }
        .card-blue{
            background: white;
            border-radius: 16px;
            padding: 14px 14px;
            box-shadow: 0 8px 20px rgba(16, 24, 40, 0.08);
            border: 1px solid #d8e3f0;
            margin-bottom: 14px;
        }
        </style>
        """, unsafe_allow_html=True)

        def tabla_balance_general_acumulado():
            col1, = st.columns([1])

            OPCIONES_EMPRESA = ["ACUMULADO"] + EMPRESAS
            empresa_sel = col1.selectbox("Empresa", OPCIONES_EMPRESA, index=0)

            df_mapeo_local = cargar_mapeo(mapeo_url)
            if df_mapeo_local.empty:
                st.stop()

            empresas_cargar = EMPRESAS[:] if empresa_sel == "ACUMULADO" else [empresa_sel]

            data_empresas = cargar_balance_multi_hojas(balance_url, empresas_cargar)
            data_empresas_ly = cargar_balance_multi_hojas(balance_ly, empresas_cargar)

            if empresa_sel == "ACUMULADO":
                dfs_act = [data_empresas.get(e, pd.DataFrame()).copy() for e in empresas_cargar]
                dfs_ly = [data_empresas_ly.get(e, pd.DataFrame()).copy() for e in empresas_cargar]

                df_emp = (
                    pd.concat([d for d in dfs_act if not d.empty], ignore_index=True)
                    if any([not d.empty for d in dfs_act])
                    else pd.DataFrame()
                )
                df_emp_ly = (
                    pd.concat([d for d in dfs_ly if not d.empty], ignore_index=True)
                    if any([not d.empty for d in dfs_ly])
                    else pd.DataFrame()
                )
            else:
                df_emp = data_empresas.get(empresa_sel, pd.DataFrame()).copy()
                df_emp_ly = data_empresas_ly.get(empresa_sel, pd.DataFrame()).copy()

            if df_emp.empty:
                st.warning(f"⚠️ No hay datos para {empresa_sel}.")
                st.stop()

            col_cuenta = _encontrar_columna(df_emp, COLUMNAS_CUENTA)
            col_monto = _encontrar_columna(df_emp, COLUMNAS_MONTO)
            col_cuenta_ly = _encontrar_columna(df_emp_ly, COLUMNAS_CUENTA)
            col_monto_ly = _encontrar_columna(df_emp_ly, COLUMNAS_MONTO)

            if not col_cuenta or not col_monto:
                st.error(f"❌ {empresa_sel}: columnas inválidas")
                st.stop()

            data_resultados = []

            for empresa in EMPRESAS:
                df_raw = data_empresas.get(empresa, pd.DataFrame()).copy()
                if df_raw.empty:
                    continue

                col_cuenta_raw = _encontrar_columna(df_raw, COLUMNAS_CUENTA)
                col_monto_raw = _encontrar_columna(df_raw, COLUMNAS_MONTO)

                if not col_cuenta_raw or not col_monto_raw:
                    st.warning(f"⚠️ {empresa}: no encontré columnas de Cuenta/Saldo para resultados.")
                    continue

                df_raw[col_cuenta_raw] = df_raw[col_cuenta_raw].apply(limpiar_cuenta)
                df_raw[col_monto_raw] = _to_numeric_money(df_raw[col_monto_raw])

                df_raw = df_raw.dropna(subset=[col_cuenta_raw])
                df_cta = df_raw.groupby(col_cuenta_raw, as_index=False)[col_monto_raw].sum()

                ingreso = df_cta.loc[
                    (df_cta[col_cuenta_raw] > 400000000) & (df_cta[col_cuenta_raw] < 500000000),
                    col_monto_raw
                ].sum()

                gasto = df_cta.loc[
                    (df_cta[col_cuenta_raw] > 500000000),
                    col_monto_raw
                ].sum()

                utilidad = ingreso + gasto

                data_resultados.append({
                    "EMPRESA": empresa,
                    "INGRESO": float(ingreso),
                    "GASTO": float(gasto),
                    "UTILIDAD": float(utilidad),
                })

            df_resultados = pd.DataFrame(data_resultados)

            if empresa_sel == "ACUMULADO" and not df_resultados.empty:
                df_total = pd.DataFrame([{
                    "EMPRESA": "TOTAL",
                    "INGRESO": float(df_resultados["INGRESO"].sum()),
                    "GASTO": float(df_resultados["GASTO"].sum()),
                    "UTILIDAD": float(df_resultados["UTILIDAD"].sum()),
                }])
                df_resultados = pd.concat([df_resultados, df_total], ignore_index=True)

            data_resultados_ly = []

            for empresa in EMPRESAS:
                df_raw_ly = data_empresas_ly.get(empresa, pd.DataFrame()).copy()
                if df_raw_ly.empty:
                    continue

                col_cuenta_raw_ly = _encontrar_columna(df_raw_ly, COLUMNAS_CUENTA)
                col_monto_raw_ly = _encontrar_columna(df_raw_ly, COLUMNAS_MONTO)

                if not col_cuenta_raw_ly or not col_monto_raw_ly:
                    st.warning(f"⚠️ {empresa} LY: no encontré columnas de Cuenta/Saldo para resultados.")
                    continue

                df_raw_ly[col_cuenta_raw_ly] = df_raw_ly[col_cuenta_raw_ly].apply(limpiar_cuenta)
                df_raw_ly[col_monto_raw_ly] = _to_numeric_money(df_raw_ly[col_monto_raw_ly])

                df_raw_ly = df_raw_ly.dropna(subset=[col_cuenta_raw_ly])
                df_cta_ly = df_raw_ly.groupby(col_cuenta_raw_ly, as_index=False)[col_monto_raw_ly].sum()

                ingreso_ly = df_cta_ly.loc[
                    (df_cta_ly[col_cuenta_raw_ly] > 400000000) & (df_cta_ly[col_cuenta_raw_ly] < 500000000),
                    col_monto_raw_ly
                ].sum()

                gasto_ly = df_cta_ly.loc[
                    (df_cta_ly[col_cuenta_raw_ly] > 500000000),
                    col_monto_raw_ly
                ].sum()

                utilidad_ly = ingreso_ly + gasto_ly

                data_resultados_ly.append({
                    "EMPRESA": empresa,
                    "INGRESO": float(ingreso_ly),
                    "GASTO": float(gasto_ly),
                    "UTILIDAD": float(utilidad_ly),
                })

            df_resultados_ly = pd.DataFrame(data_resultados_ly)

            if empresa_sel == "ACUMULADO" and not df_resultados_ly.empty:
                df_total_ly = pd.DataFrame([{
                    "EMPRESA": "TOTAL",
                    "INGRESO": float(df_resultados_ly["INGRESO"].sum()),
                    "GASTO": float(df_resultados_ly["GASTO"].sum()),
                    "UTILIDAD": float(df_resultados_ly["UTILIDAD"].sum()),
                }])
                df_resultados_ly = pd.concat([df_resultados_ly, df_total_ly], ignore_index=True)

            st.markdown('<div class="header-pill">BALANCE GENERAL POR EMPRESA</div>', unsafe_allow_html=True)
            st.markdown('<div class="sub-pill">Estado de Resultados por Empresa</div>', unsafe_allow_html=True)

            st.dataframe(
                df_resultados.style
                    .format({
                        "INGRESO": "${:,.2f}",
                        "GASTO": "${:,.2f}",
                        "UTILIDAD": "${:,.2f}",
                    })
                    .set_properties(**{
                        "text-align": "right",
                        "border-color": "#d8e3f0"
                    })
                    .set_table_styles([
                        {
                            "selector": "th",
                            "props": [
                                ("background-color", "#214a6b"),
                                ("color", "white"),
                                ("font-weight", "bold"),
                                ("text-align", "center"),
                                ("border", "1px solid #d8e3f0")
                            ]
                        },
                        {
                            "selector": "td",
                            "props": [
                                ("border", "1px solid #e6eef7")
                            ]
                        }
                    ]),
                use_container_width=True,
                hide_index=True
            )

            df_emp[col_cuenta] = df_emp[col_cuenta].apply(limpiar_cuenta)
            df_emp[col_monto] = _to_numeric_money(df_emp[col_monto])
            df_emp = df_emp.dropna(subset=[col_cuenta])
            df_emp = df_emp.groupby(col_cuenta, as_index=False)[col_monto].sum()

            df_emp_ly[col_cuenta_ly] = df_emp_ly[col_cuenta_ly].apply(limpiar_cuenta)
            df_emp_ly[col_monto_ly] = _to_numeric_money(df_emp_ly[col_monto_ly])
            df_emp_ly = df_emp_ly.dropna(subset=[col_cuenta_ly])
            df_emp_ly = df_emp_ly.groupby(col_cuenta_ly, as_index=False)[col_monto_ly].sum()

            df_merged = df_emp.merge(
                df_mapeo_local[["Cuenta", "CLASIFICACION", "CATEGORIA"]],
                left_on=col_cuenta,
                right_on="Cuenta",
                how="left",
            )

            df_merged_ly = df_emp_ly.merge(
                df_mapeo_local[["Cuenta", "CLASIFICACION", "CATEGORIA"]],
                left_on=col_cuenta_ly,
                right_on="Cuenta",
                how="left",
            )

            df_no_mapeadas = df_merged[df_merged["CLASIFICACION"].isna()].copy()
            df_ok = df_merged[~df_merged["CLASIFICACION"].isna()].copy()

            if df_ok.empty:
                st.warning(f"⚠️ {empresa_sel}: sin coincidencias con el mapeo.")
                st.stop()

            ORDEN = ("ACTIVO", "PASIVO", "CAPITAL")

            df_ok["CLASIFICACION"] = df_ok["CLASIFICACION"].astype(str).str.upper().str.strip()
            df_ok["CATEGORIA"] = df_ok["CATEGORIA"].astype(str).str.strip()
            df_ok[col_monto] = pd.to_numeric(df_ok[col_monto], errors="coerce").fillna(0.0)

            df_ok = df_ok[df_ok["CLASIFICACION"].isin(ORDEN)].copy()
            df_ok = df_ok[df_ok["CATEGORIA"].str.upper().ne("MAYOR")].copy()

            df_grp = (
                df_ok.groupby(["CLASIFICACION", "CATEGORIA"], as_index=False)[col_monto]
                .sum()
                .rename(columns={col_monto: "MONTO"})
            )

            df_ok_ly = df_merged_ly[~df_merged_ly["CLASIFICACION"].isna()].copy()
            df_ok_ly["CLASIFICACION"] = df_ok_ly["CLASIFICACION"].astype(str).str.upper().str.strip()
            df_ok_ly["CATEGORIA"] = df_ok_ly["CATEGORIA"].astype(str).str.strip()
            df_ok_ly[col_monto_ly] = pd.to_numeric(df_ok_ly[col_monto_ly], errors="coerce").fillna(0.0)

            df_ok_ly = df_ok_ly[df_ok_ly["CLASIFICACION"].isin(ORDEN)].copy()
            df_ok_ly = df_ok_ly[df_ok_ly["CATEGORIA"].str.upper().ne("MAYOR")].copy()

            df_grp_ly = (
                df_ok_ly.groupby(["CLASIFICACION", "CATEGORIA"], as_index=False)[col_monto_ly]
                .sum()
                .rename(columns={col_monto_ly: "MONTO_LY"})
            )

            df_base = df_grp.merge(df_grp_ly, on=["CLASIFICACION", "CATEGORIA"], how="outer")
            df_base["MONTO"] = pd.to_numeric(df_base["MONTO"], errors="coerce").fillna(0.0)
            df_base["MONTO_LY"] = pd.to_numeric(df_base["MONTO_LY"], errors="coerce").fillna(0.0)

            mask_pc = df_base["CLASIFICACION"].isin(["PASIVO", "CAPITAL"])
            df_base.loc[mask_pc, "MONTO"] *= -1
            df_base.loc[mask_pc, "MONTO_LY"] *= -1

            df_base["% VARIACION"] = np.where(
                df_base["MONTO_LY"].abs() > 1e-9,
                (df_base["MONTO"] / df_base["MONTO_LY"]) - 1.0,
                np.nan
            )

            if df_resultados.empty:
                utilidad_sel = 0.0
            else:
                if empresa_sel == "ACUMULADO":
                    utilidad_sel = float(
                        df_resultados.loc[df_resultados["EMPRESA"] != "TOTAL", "UTILIDAD"].sum()
                    ) * -1
                else:
                    s = df_resultados.loc[df_resultados["EMPRESA"] == empresa_sel, "UTILIDAD"]
                    utilidad_sel = float(s.iloc[0]) * -1 if not s.empty else 0.0

            if df_resultados_ly.empty:
                utilidad_sel_ly = 0.0
            else:
                if empresa_sel == "ACUMULADO":
                    utilidad_sel_ly = float(
                        df_resultados_ly.loc[df_resultados_ly["EMPRESA"] != "TOTAL", "UTILIDAD"].sum()
                    ) * -1
                else:
                    s_ly = df_resultados_ly.loc[df_resultados_ly["EMPRESA"] == empresa_sel, "UTILIDAD"]
                    utilidad_sel_ly = float(s_ly.iloc[0]) * -1 if not s_ly.empty else 0.0

            rows = []
            totales = {}
            totales_ly = {}

            for clasif in ORDEN:
                sub = df_base[df_base["CLASIFICACION"] == clasif].copy()

                total_act = float(sub["MONTO"].sum()) if not sub.empty else 0.0
                total_ly = float(sub["MONTO_LY"].sum()) if not sub.empty else 0.0

                if clasif == "CAPITAL":
                    total_act += utilidad_sel
                    total_ly += utilidad_sel_ly

                totales[clasif] = total_act
                totales_ly[clasif] = total_ly

                rows.append({
                    "SECCION": clasif,
                    "CUENTA": "",
                    "MONTO": total_act,
                    "MONTO_LY": total_ly,
                    "% VARIACION": (total_act / total_ly - 1.0) if abs(total_ly) > 1e-9 else np.nan
                })

                if not sub.empty:
                    sub = sub.sort_values("CATEGORIA")
                    for _, r in sub.iterrows():
                        rows.append({
                            "SECCION": "",
                            "CUENTA": str(r["CATEGORIA"]),
                            "MONTO": float(r["MONTO"]),
                            "MONTO_LY": float(r["MONTO_LY"]),
                            "% VARIACION": float(r["% VARIACION"]) if pd.notna(r["% VARIACION"]) else np.nan
                        })

                if clasif == "CAPITAL":
                    rows.append({
                        "SECCION": "",
                        "CUENTA": "UTILIDAD DEL EJERCICIO",
                        "MONTO": float(utilidad_sel),
                        "MONTO_LY": float(utilidad_sel_ly),
                        "% VARIACION": (
                            (utilidad_sel / utilidad_sel_ly) - 1.0
                            if abs(utilidad_sel_ly) > 1e-9 else np.nan
                        )
                    })

                rows.append({
                    "SECCION": "",
                    "CUENTA": "",
                    "MONTO": None,
                    "MONTO_LY": None,
                    "% VARIACION": None
                })

            dif = float(totales.get("ACTIVO", 0.0) - (totales.get("PASIVO", 0.0) + totales.get("CAPITAL", 0.0)))
            dif_ly = float(totales_ly.get("ACTIVO", 0.0) - (totales_ly.get("PASIVO", 0.0) + totales_ly.get("CAPITAL", 0.0)))

            rows.append({
                "SECCION": "RESUMEN",
                "CUENTA": "DIFERENCIA",
                "MONTO": dif,
                "MONTO_LY": dif_ly,
                "% VARIACION": (dif / dif_ly - 1.0) if abs(dif_ly) > 1e-9 else np.nan
            })

            df_out_raw = pd.DataFrame(rows)

            def fmt_money(x):
                if x is None or (isinstance(x, float) and pd.isna(x)):
                    return ""
                return f"${float(x):,.2f}"

            def fmt_pct(x):
                if x is None or (isinstance(x, float) and pd.isna(x)):
                    return ""
                return f"{x * 100:,.1f}%"

            df_out_show = df_out_raw.copy()
            df_out_show["MONTO"] = df_out_show["MONTO"].apply(fmt_money)
            df_out_show["MONTO_LY"] = df_out_show["MONTO_LY"].apply(fmt_money)
            df_out_show["% VARIACION"] = df_out_show["% VARIACION"].apply(fmt_pct)

            def estilo_reporte(row):
                seccion = str(row.get("SECCION", "")).upper().strip()
                cuenta = str(row.get("CUENTA", "")).upper().strip()

                if seccion in ["ACTIVO", "PASIVO", "CAPITAL"]:
                    return [
                        "font-weight:800; background:#dbe8f6; color:#000000; border-top:2px solid #163a5f; border-bottom:2px solid #163a5f;"
                    ] * len(row)

                if seccion == "RESUMEN" or cuenta == "DIFERENCIA":
                    return [
                        "font-weight:800; background:#dbe8f6; color:#163a5f; border-top:2px solid #214a6b;"
                    ] * len(row)

                if cuenta == "UTILIDAD DEL EJERCICIO":
                    return [
                        "font-weight:700; background:#eef4fb; color:#163a5f;"
                    ] * len(row)

                if cuenta == "":
                    return [
                        "background:#ffffff; color:#ffffff; border:none;"
                    ] * len(row)

                return ["background:#ffffff; color:#000000;"] * len(row)

            st.markdown(f'<div class="sub-pill">{empresa_sel}</div>', unsafe_allow_html=True)

            styled_df = (
                df_out_show[["SECCION", "CUENTA", "MONTO", "MONTO_LY", "% VARIACION"]]
                .style
                .hide(axis="index")
                .apply(estilo_reporte, axis=1)
                .set_properties(**{
                    "border": "1px solid #e6eef7",
                    "font-size": "14px",
                    "color": "#000000"
                })
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#163a5f"),
                            ("color", "white"),
                            ("font-weight", "bold"),
                            ("text-align", "center"),
                            ("border", "1px solid #d8e3f0"),
                            ("padding", "8px")
                        ]
                    },
                    {
                        "selector": "td",
                        "props": [
                            ("padding", "7px"),
                            ("border", "1px solid #e6eef7"),
                            ("color", "#000000")
                        ]
                    }
                ])
            )

            st.table(styled_df)

            if abs(dif) < 1:
                st.success("✅ El balance está cuadrado")
            else:
                st.error("❌ El balance no cuadra. Revisa mapeo/cuentas.")

            if not df_no_mapeadas.empty:
                st.markdown("## ⚠️ Cuentas NO mapeadas")
                cols_show = [col_cuenta, col_monto]
                cols_show = [c for c in cols_show if c in df_no_mapeadas.columns]
                df_nm = (
                    df_no_mapeadas[cols_show]
                    .copy()
                    .rename(columns={col_cuenta: "Cuenta", col_monto: "Saldo"})
                )
                st.dataframe(df_nm, use_container_width=True, hide_index=True)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_ok.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_detalle")
                df_grp.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_agrupado")
                df_ok_ly.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_detalle_LY")
                df_grp_ly.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_agrupado_LY")
                if not df_no_mapeadas.empty:
                    df_no_mapeadas.to_excel(writer, index=False, sheet_name="No_mapeadas")

            nombre_archivo = (
                "Balance_Acumulado_TODAS.xlsx"
                if empresa_sel == "ACUMULADO"
                else f"Balance_Acumulado_{empresa_sel}.xlsx"
            )

            st.download_button(
                label=f"💾 Descargar Excel ({empresa_sel})",
                data=output.getvalue(),
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            return

        tabla_balance_general_acumulado()

    elif selected == "E.R por empresa":
        st.markdown("""
        <style>

        .stApp {
            background: white;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        .header-pill{
            background: linear-gradient(90deg, #163a5f 0%, #214a6b 100%);
            color: white;
            padding: 12px 18px;
            border-radius: 12px;
            font-weight: 800;
            display: inline-block;
            box-shadow: 0 8px 18px rgba(20, 58, 95, 0.22);
            margin-bottom: 10px;
        }

        .sub-pill{
            background: #214a6b;
            color: white;
            padding: 8px 12px;
            border-radius: 10px;
            font-weight: 700;
            display: inline-block;
            margin: 6px 0px 10px 0px;
        }

        .caption-blue{
            color: #214a6b;
            font-weight: 700;
            margin-top: -2px;
            margin-bottom: 8px;
        }

        .card-blue{
            background: white;
            border-radius: 16px;
            padding: 14px 14px;
            box-shadow: none;
            border: 1px solid #d8e3f0;
            margin-bottom: 14px;
        }

        </style>
        """, unsafe_allow_html=True)

        def tabla_estado_resultados():
            st.markdown('<div class="header-pill">ESTADO DE RESULTADOS</div>', unsafe_allow_html=True)

            col1, = st.columns([1])

            OPCIONES_EMPRESA = ["ACUMULADO"] + EMPRESAS
            empresa_sel = col1.selectbox("Empresa", OPCIONES_EMPRESA, index=0)

            df_mapeo_local = cargar_mapeo(mapeo_url)
            if df_mapeo_local.empty:
                st.stop()

            req = {"Cuenta", "CLASIFICACION_A", "CATEGORIA_A"}
            if not req.issubset(df_mapeo_local.columns):
                st.error(f"❌ Al mapeo le faltan columnas: {req - set(df_mapeo_local.columns)}")
                st.stop()

            df_map = df_mapeo_local.copy()
            df_map["Cuenta"] = df_map["Cuenta"].apply(limpiar_cuenta)
            df_map["CLASIFICACION_A"] = df_map["CLASIFICACION_A"].astype("string").str.upper().str.strip()
            df_map["CATEGORIA_A"] = df_map["CATEGORIA_A"].astype("string").str.upper().str.strip()
            df_map = df_map.dropna(subset=["CLASIFICACION_A", "CATEGORIA_A"])
            df_map = df_map[(df_map["CLASIFICACION_A"] != "") & (df_map["CATEGORIA_A"] != "")]
            df_map = df_map.drop_duplicates(subset=["Cuenta"])

            if empresa_sel == "ACUMULADO":
                empresas_cargar = EMPRESAS[:]
            else:
                empresas_cargar = [empresa_sel]

            data_2026 = cargar_balance_multi_hojas(balance_url, empresas_cargar)
            data_2025 = cargar_balance_multi_hojas(balance_ly, empresas_cargar)

            def prep(df_raw, col_cta, col_amt, nombre_monto):
                df = df_raw.copy()
                df[col_cta] = df[col_cta].apply(limpiar_cuenta)
                df[col_amt] = _to_numeric_money(df[col_amt])
                df = df.dropna(subset=[col_cta])
                df = df.groupby(col_cta, as_index=False)[col_amt].sum()
                df = df.rename(columns={col_cta: "Cuenta", col_amt: nombre_monto})
                return df

            def build_df_year(data_dict, nombre_monto):
                partes = []
                for emp in empresas_cargar:
                    df_raw = data_dict.get(emp, pd.DataFrame()).copy()
                    if df_raw.empty:
                        continue

                    col_cta = _encontrar_columna(df_raw, COLUMNAS_CUENTA)
                    col_amt = _encontrar_columna(df_raw, COLUMNAS_MONTO)

                    if not col_cta or not col_amt:
                        st.error(f"❌ {nombre_monto}: columnas inválidas (Cuenta/Saldo) en {emp}.")
                        st.stop()

                    partes.append(prep(df_raw, col_cta, col_amt, nombre_monto))

                if not partes:
                    return pd.DataFrame(columns=["Cuenta", nombre_monto])

                df_year = pd.concat(partes, ignore_index=True)
                df_year = df_year.groupby("Cuenta", as_index=False)[nombre_monto].sum()
                return df_year

            df_26 = build_df_year(data_2026, "2026")
            df_25 = build_df_year(data_2025, "2025")

            if df_26.empty:
                st.warning(f"⚠️ No hay datos 2026 para {empresa_sel}.")
                st.stop()

            if df_25.empty:
                st.warning(f"⚠️ No hay datos 2025 para {empresa_sel}.")
                st.stop()

            df_cta = df_26.merge(df_25, on="Cuenta", how="outer").fillna(0.0)

            df_pl = df_cta.merge(
                df_map[["Cuenta", "CLASIFICACION_A", "CATEGORIA_A"]],
                on="Cuenta",
                how="left",
            )

            df_no_mapeadas = df_pl[df_pl["CLASIFICACION_A"].isna()].copy()
            df_pl = df_pl.dropna(subset=["CLASIFICACION_A"])

            if df_pl.empty:
                st.warning("⚠️ No hay cuentas mapeadas a CLASIFICACION_A para esta selección.")
                st.stop()

            flip_clasif = {
                "INGRESO",
                "OTROS INGRESOS",
                "INGRESO FINANCIERO",
            }
            mask_flip = df_pl["CLASIFICACION_A"].astype(str).str.upper().str.strip().isin(flip_clasif)
            df_pl.loc[mask_flip, ["2026", "2025"]] = df_pl.loc[mask_flip, ["2026", "2025"]] * -1

            df_tot = df_pl.groupby("CLASIFICACION_A", as_index=False)[["2026", "2025"]].sum()


            def tot(*nombres):
                """Suma total por una o varias CLASIFICACION_A (case-insensitive)."""
                if len(nombres) == 1 and isinstance(nombres[0], (list, tuple, set)):
                    nombres = tuple(nombres[0])
                claves = [str(x).upper().strip() for x in nombres]
                sub = df_tot[df_tot["CLASIFICACION_A"].isin(claves)]
                return float(sub["2026"].sum()), float(sub["2025"].sum())

            def tot_cat(*nombres):
                """Suma total por CATEGORIA_A."""
                if len(nombres) == 1 and isinstance(nombres[0], (list, tuple, set)):
                    nombres = tuple(nombres[0])
                claves = [str(x).upper().strip() for x in nombres]
                sub = df_pl[df_pl["CATEGORIA_A"].str.upper().str.strip().isin(claves)]
                return float(sub["2026"].sum()), float(sub["2025"].sum())

            def pct(a, b):
                return (a / b - 1.0) if abs(b) > 1e-9 else None


            ing_26, ing_25 = tot("INGRESO")
            coss_26, coss_25 = tot("COSS")
            gadm_26, gadm_25 = tot("G.ADMN")

            otros_ing_26, otros_ing_25 = tot("OTROS INGRESOS", "OTROS INGRESO")
            gasto_fin_26, gasto_fin_25 = tot("GASTO FIN", "GASTO FINANCIERO")
            ingreso_fin_26, ingreso_fin_25 = tot("INGRESO FIN", "INGRESO FINANCIERO")


            imp_26, imp_25 = tot_cat("IMPUESTOS")
            dep_26, dep_25 = tot_cat("DEPRECIACION")
            amo1_26, amo1_25 = tot_cat("AMORTIZACION")
            amo2_26, amo2_25 = tot_cat("AMORT ARRENDAMIENTO")

            amo_26 = amo1_26 + amo2_26
            amo_25 = amo1_25 + amo2_25

            ub_26 = ing_26 - coss_26
            ub_25 = ing_25 - coss_25

            uo_26 = ub_26 - gadm_26
            uo_25 = ub_25 - gadm_25

            ebit_26 = uo_26 + otros_ing_26
            ebit_25 = uo_25 + otros_ing_25

            ebt_26 = ebit_26 - gasto_fin_26 + ingreso_fin_26
            ebt_25 = ebit_25 - gasto_fin_25 + ingreso_fin_25

            udi_26 = ebt_26 - imp_26
            udi_25 = ebt_25 - imp_25

            ebitda_26 = ebit_26 + dep_26 + amo_26
            ebitda_25 = ebit_25 + dep_25 + amo_25

            panel = [
                ("INGRESO", ing_26, ing_25, "money"),
                ("COSS", coss_26, coss_25, "money"),
                ("UTILIDAD BRUTA", ub_26, ub_25, "money_bold"),
                ("% UB", (ub_26 / ing_26 if abs(ing_26) > 1e-9 else None), (ub_25 / ing_25 if abs(ing_25) > 1e-9 else None), "pct"),
                ("G.ADMN", gadm_26, gadm_25, "money"),
                ("UTILIDAD OPERATIVA", uo_26, uo_25, "money_bold"),
                ("%UO", (uo_26 / ing_26 if abs(ing_26) > 1e-9 else None), (uo_25 / ing_25 if abs(ing_25) > 1e-9 else None), "pct"),
                ("OTROS INGRESOS", otros_ing_26, otros_ing_25, "money"),
                ("EBIT", ebit_26, ebit_25, "money_bold"),
                ("% EBIT", (ebit_26 / ing_26 if abs(ing_26) > 1e-9 else None), (ebit_25 / ing_25 if abs(ing_25) > 1e-9 else None), "pct"),
                ("GASTO FIN", gasto_fin_26, gasto_fin_25, "money"),
                ("INGRESO FIN", ingreso_fin_26, ingreso_fin_25, "money"),
                ("EBT", ebt_26, ebt_25, "money_bold"),
                ("% EBT", (ebt_26 / ing_26 if abs(ing_26) > 1e-9 else None), (ebt_25 / ing_25 if abs(ing_25) > 1e-9 else None), "pct"),
                ("IMPUESTOS", imp_26, imp_25, "money"),
                ("Utilidad D.Imp.", udi_26, udi_25, "money_bold"),
                ("%UDI", (udi_26 / ing_26 if abs(ing_26) > 1e-9 else None), (udi_25 / ing_25 if abs(ing_25) > 1e-9 else None), "pct"),
                ("EBITDA", ebitda_26, ebitda_25, "money_bold"),
            ]

            df_panel = pd.DataFrame(panel, columns=["CONCEPTO", "2026", "2025", "_fmt"])
            df_panel["% CAMBIO"] = df_panel.apply(
                lambda r: pct(r["2026"], r["2025"]) if r["_fmt"] != "pct" else None,
                axis=1,
            )

            def fmt_money(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                return f"$ {float(v):,.0f}"

            def fmt_pct(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                return f"{float(v) * 100:,.2f}%"

            df_show = df_panel.copy()
            is_pct = df_show["_fmt"].eq("pct")

            df_show.loc[~is_pct, "2026"] = df_show.loc[~is_pct, "2026"].apply(fmt_money)
            df_show.loc[~is_pct, "2025"] = df_show.loc[~is_pct, "2025"].apply(fmt_money)
            df_show.loc[~is_pct, "% CAMBIO"] = df_show.loc[~is_pct, "% CAMBIO"].apply(
                lambda x: "" if x is None else f"{x * 100:,.0f}%"
            )

            df_show.loc[is_pct, "2026"] = df_show.loc[is_pct, "2026"].apply(fmt_pct)
            df_show.loc[is_pct, "2025"] = df_show.loc[is_pct, "2025"].apply(fmt_pct)
            df_show.loc[is_pct, "% CAMBIO"] = ""

            def style_panel(row):
                concepto = str(row.get("CONCEPTO", "")).upper().strip()

                if concepto in ["UTILIDAD BRUTA", "UTILIDAD OPERATIVA", "EBIT", "EBT", "UTILIDAD D.IMP.", "EBITDA"]:
                    return ["font-weight:800; background:#dbe8f6; color:#163a5f; border-top:1px solid #b8cde3;"] * len(row)

                if concepto in ["INGRESO", "COSS", "G.ADMN", "OTROS INGRESOS", "GASTO FIN", "INGRESO FIN", "IMPUESTOS"]:
                    return ["font-weight:700; background:#f7fbff; color:#1f2937;"] * len(row)

                if concepto in ["% UB", "%UO", "% EBIT", "% EBT", "%UDI"]:
                    return ["font-weight:700; color:#214a6b; background:#f8fbff;"] * len(row)

                return ["background:#ffffff; color:#1f2937;"] * len(row)
            
            st.markdown(f'<div class="sub-pill">{empresa_sel}</div>', unsafe_allow_html=True)
            st.markdown('<div class="caption-blue">Miles MXN</div>', unsafe_allow_html=True)

            st.dataframe(
                df_show[["CONCEPTO", "2026", "2025", "% CAMBIO"]]
                    .style
                    .apply(style_panel, axis=1)
                    .set_properties(**{
                        "border": "1px solid #e6eef7",
                        "font-size": "14px",
                        "padding": "6px"
                    })
                    .set_table_styles([
                        {
                            "selector": "th",
                            "props": [
                                ("background-color", "#163a5f"),
                                ("color", "white"),
                                ("font-weight", "bold"),
                                ("text-align", "center"),
                                ("border", "1px solid #d8e3f0"),
                                ("padding", "8px")
                            ]
                        },
                        {
                            "selector": "td",
                            "props": [
                                ("border", "1px solid #e6eef7"),
                                ("padding", "7px")
                            ]
                        }
                    ]),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown('<div class="sub-pill">Detalle por Categoría</div>', unsafe_allow_html=True)

            df_cat = (
                df_pl.groupby(["CLASIFICACION_A", "CATEGORIA_A"], as_index=False)[["2026", "2025"]]
                .sum()
            )

            def _pct(a, b):
                return (a / b - 1.0) if abs(b) > 1e-9 else np.nan

            def _fmt_money(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                v = float(v)
                if v < 0:
                    return f"-$ {abs(v):,.0f}"
                return f"$ {v:,.0f}"

            def _fmt_pct(v):
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    return ""
                return f"{float(v) * 100:,.0f}%"

            rows = []

            def add_header(nombre, v26, v25, is_pct=False):
                rows.append({
                    "SECCION": nombre,
                    "CATEGORIA": "",
                    "2026": v26,
                    "CATEGORIA2": "",
                    "2025": v25,
                    "% CAMBIO": (None if is_pct else _pct(v26, v25)),
                    "_t": "header",
                    "_is_pct": bool(is_pct),
                })

            def add_detail(cat, v26, v25):
                rows.append({
                    "SECCION": "",
                    "CATEGORIA": str(cat),
                    "2026": v26,
                    "CATEGORIA2": str(cat),
                    "2025": v25,
                    "% CAMBIO": _pct(v26, v25),
                    "_t": "detail",
                    "_is_pct": False,
                })

            def add_section(clasif_list, header_name, total26, total25):
                add_header(header_name, total26, total25)
                sub = df_cat[
                    df_cat["CLASIFICACION_A"].astype(str).str.upper().str.strip().isin(
                        [str(x).upper().strip() for x in clasif_list]
                    )
                ].copy()

                if not sub.empty:
                    sub = sub.sort_values("CATEGORIA_A")
                    for _, r in sub.iterrows():
                        add_detail(r["CATEGORIA_A"], float(r["2026"]), float(r["2025"]))

            add_section(["INGRESO"], "INGRESO", ing_26, ing_25)
            add_section(["COSS"], "COSS", coss_26, coss_25)

            add_header("UTILIDAD BRUTA", ub_26, ub_25)
            add_header(
                "% UB",
                (ub_26 / ing_26) if abs(ing_26) > 1e-9 else np.nan,
                (ub_25 / ing_25) if abs(ing_25) > 1e-9 else np.nan,
                is_pct=True,
            )

            add_section(["G.ADMN"], "G.ADMN", gadm_26, gadm_25)

            add_header("UTILIDAD OPERATIVA", uo_26, uo_25)
            add_header(
                "%UO",
                (uo_26 / ing_26) if abs(ing_26) > 1e-9 else np.nan,
                (uo_25 / ing_25) if abs(ing_25) > 1e-9 else np.nan,
                is_pct=True,
            )

            add_section(["OTROS INGRESOS", "OTROS INGRESO"], "OTROS INGRESOS", otros_ing_26, otros_ing_25)

            add_header("EBIT", ebit_26, ebit_25)
            add_header(
                "% EBIT",
                (ebit_26 / ing_26) if abs(ing_26) > 1e-9 else np.nan,
                (ebit_25 / ing_25) if abs(ing_25) > 1e-9 else np.nan,
                is_pct=True,
            )

            add_section(["GASTO FIN", "GASTO FINANCIERO"], "GASTO FINANCIERO", gasto_fin_26, gasto_fin_25)
            add_section(["INGRESO FIN", "INGRESO FINANCIERO"], "INGRESO FINANCIERO", ingreso_fin_26, ingreso_fin_25)

            add_header("EBT", ebt_26, ebt_25)
            add_header(
                "% EBT",
                (ebt_26 / ing_26) if abs(ing_26) > 1e-9 else np.nan,
                (ebt_25 / ing_25) if abs(ing_25) > 1e-9 else np.nan,
                is_pct=True,
            )

            add_section(["IMPUESTOS"], "IMPUESTOS", imp_26, imp_25)

            add_header("Uti.D. impuestos", udi_26, udi_25)
            add_header(
                "%UDI",
                (udi_26 / ing_26) if abs(ing_26) > 1e-9 else np.nan,
                (udi_25 / ing_25) if abs(ing_25) > 1e-9 else np.nan,
                is_pct=True,
            )

            add_header("EBITDA", ebitda_26, ebitda_25)

            df_det = pd.DataFrame(rows)
            df_show2 = df_det.copy()

            mask_pct = df_show2["_is_pct"].fillna(False)

            df_show2.loc[~mask_pct, "2026"] = df_show2.loc[~mask_pct, "2026"].apply(_fmt_money)
            df_show2.loc[~mask_pct, "2025"] = df_show2.loc[~mask_pct, "2025"].apply(_fmt_money)
            df_show2.loc[~mask_pct, "% CAMBIO"] = df_show2.loc[~mask_pct, "% CAMBIO"].apply(_fmt_pct)

            df_show2.loc[mask_pct, "2026"] = df_show2.loc[mask_pct, "2026"].apply(_fmt_pct)
            df_show2.loc[mask_pct, "2025"] = df_show2.loc[mask_pct, "2025"].apply(_fmt_pct)
            df_show2.loc[mask_pct, "% CAMBIO"] = ""

            def _style_detalle(row):
                titulo = str(row.get(str(empresa_sel), "")).upper().strip()
                tipo = str(row.get("_t", "")).strip().lower()

                if tipo == "header":
                    return ["font-weight:800; background:#214a6b; color:white; border-top:1px solid #163a5f; border-bottom:1px solid #163a5f;"] * len(row)

                if titulo in ["UTILIDAD BRUTA", "UTILIDAD OPERATIVA", "EBIT", "EBT", "UTI.D. IMPUESTOS", "EBITDA"]:
                    return ["font-weight:800; background:#dbe8f6; color:#163a5f;"] * len(row)

                if titulo in ["% UB", "%UO", "% EBIT", "% EBT", "%UDI"]:
                    return ["font-weight:700; background:#f8fbff; color:#214a6b;"] * len(row)

                return ["background:#ffffff; color:#1f2937;"] * len(row)

            df_show2 = df_show2.rename(columns={"SECCION": str(empresa_sel)})

            st.dataframe(
                df_show2[[str(empresa_sel), "CATEGORIA", "2026", "CATEGORIA2", "2025", "% CAMBIO"]]
                    .style
                    .apply(_style_detalle, axis=1)
                    .set_properties(**{
                        "border": "1px solid #e6eef7",
                        "font-size": "13.5px",
                        "padding": "6px"
                    })
                    .set_table_styles([
                        {
                            "selector": "th",
                            "props": [
                                ("background-color", "#163a5f"),
                                ("color", "white"),
                                ("font-weight", "bold"),
                                ("text-align", "center"),
                                ("border", "1px solid #d8e3f0"),
                                ("padding", "8px")
                            ]
                        },
                        {
                            "selector": "td",
                            "props": [
                                ("border", "1px solid #e6eef7"),
                                ("padding", "7px")
                            ]
                        }
                    ]),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown('<div class="sub-pill">Detalle 360</div>', unsafe_allow_html=True)

            df_grid = df_excel_cuentas.copy()

            df_grid = df_grid.rename(columns={
                "CLASIFICACION_A": "Clasificacion",
                "CATEGORIA_A": "Categoria",
                "Descripcion": "Descripcion",
                "Cuenta": "Cuenta"
            })

            currency_formatter = JsCode("""
            function(params) {

                if (params.value === null || params.value === undefined)
                    return '';

                return new Intl.NumberFormat(
                    'es-MX',
                    {
                        style: 'currency',
                        currency: 'MXN',
                        minimumFractionDigits: 0
                    }
                ).format(params.value);
            }
            """)

            pct_formatter = JsCode("""
            function(params) {

                if (params.value === null || params.value === undefined)
                    return '';

                return (params.value * 100).toFixed(1) + '%';
            }
            """)

            gb = GridOptionsBuilder.from_dataframe(df_grid)

            gb.configure_default_column(
                resizable=True,
                sortable=True,
                filter=True
            )

            gb.configure_column(
                "Clasificacion",
                rowGroup=True,
                hide=True
            )

            gb.configure_column(
                "Categoria",
                rowGroup=True,
                hide=True
            )

            gb.configure_column(
                "Descripcion",
                headerName="Descripcion",
                pinned="left",
                minWidth=320
            )

            gb.configure_column(
                "Cuenta",
                headerName="Cuenta",
                minWidth=130
            )

            gb.configure_column(
                "2026",
                headerName="2026",
                type=["numericColumn"],
                aggFunc="sum",
                valueFormatter=currency_formatter,
                cellStyle={"textAlign": "right"}
            )

            gb.configure_column(
                "2025",
                headerName="2025",
                type=["numericColumn"],
                aggFunc="sum",
                valueFormatter=currency_formatter,
                cellStyle={"textAlign": "right"}
            )

            gb.configure_column(
                "% CAMBIO",
                headerName="% CAMBIO",
                type=["numericColumn"],
                valueFormatter=pct_formatter,
                cellStyle={"textAlign": "right"}
            )

            grid_options = gb.build()

            grid_options.update({
                "groupDisplayType": "singleColumn",
                "groupDefaultExpanded": 1,
                "suppressAggFuncInHeader": False
            })

            AgGrid(
                df_grid,
                gridOptions=grid_options,
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True,
                fit_columns_on_grid_load=True,
                height=650,
                theme="streamlit",
                key=f"detalle_360_{empresa_sel}"
            )

            df_excel_cuentas = df_pl.copy()

            df_excel_cuentas["CLASIFICACION_A"] = (
                df_excel_cuentas["CLASIFICACION_A"].astype(str).str.upper().str.strip()
            )
            df_excel_cuentas["CATEGORIA_A"] = (
                df_excel_cuentas["CATEGORIA_A"].astype(str).str.upper().str.strip()
            )

            df_excel_cuentas = df_excel_cuentas[
                ["Cuenta", "Descripcion", "CLASIFICACION_A", "CATEGORIA_A", "2026", "2025"]
            ].copy()

            df_excel_cuentas["% CAMBIO"] = np.where(
                df_excel_cuentas["2025"].abs() > 1e-9,
                (df_excel_cuentas["2026"] / df_excel_cuentas["2025"]) - 1.0,
                np.nan
            )

            df_excel_cuentas = df_excel_cuentas.sort_values(
                ["CLASIFICACION_A", "CATEGORIA_A", "Cuenta", "Descripcion"]
            )


            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_show.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_resumen")
                df_show2.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_agrupado")
                df_excel_cuentas.to_excel(writer, index=False, sheet_name=f"{empresa_sel[:25]}_cuentas")

            nombre_archivo = (
                "Estado_de_Resultados.xlsx"
                if empresa_sel == "ACUMULADO"
                else f"Estado_de_Resultados_{empresa_sel}.xlsx"
            )

            st.download_button(
                label=f"💾 Descargar Excel ({empresa_sel})",
                data=output.getvalue(),
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            return

        tabla_estado_resultados()

    elif selected in ['WACC Esgari', 'WACC', 'Costo de capital', 'Deuda']:

        st.markdown("<h2 style='text-align: center;'>Análisis de Tasa de Descuento (WACC)</h2>", unsafe_allow_html=True)
        st.markdown("---")

        if selected == "Costo de capital":
            sec = "Costo de Capital Propio"

        elif selected == "Deuda":
            sec = "Deuda"

        elif selected == "WACC":
            sec = "Cálculo del WACC"

        else:
            sec = option_menu(
                "Cálculos Financieros",
                ["Cálculo del WACC", "Costo de Capital Propio", "Deuda"],
                icons=["graph-up-arrow", "percent", "bank"],
                orientation="horizontal"
            )

        if sec == "Costo de Capital Propio":
            with st.container():
                st.subheader("Empresas Comparables")
                st.dataframe(com.style.format(precision=2))

                st.markdown("### Parámetros de Mercado")
                col1, col2 = st.columns(2)
                col1.metric("Beta desapalancada Promedio", f"{beta_pro:.2f}")
                col2.metric("Beta Apalancado Esgari", f"{beta_esg:.2f}")
                col1.metric("Equity Risk Premium (ERP) México", f"{erp_mex*100:.2f}%")
                col2.metric("Tasa Libre de Riesgo", f"{risk_free*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"Costo de Capital Propio: {eq*100:.2f}%", icon="📊")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                El **Costo de Capital Propio (Ke)** representa el rendimiento mínimo que los accionistas esperan por su inversión.

                Este valor es clave para decidir si una empresa debe seguir financiando sus operaciones con capital propio o buscar otras fuentes.

                Se basa en la sensibilidad de la empresa al mercado (Beta), ajustada por el apalancamiento financiero y el riesgo país.

                **Fórmula utilizada:**

                $$
                K_e = R_f + \\beta_{apal} \\times ERP
                $$

                Donde:

                - $R_f$ = Tasa libre de riesgo (CETES 28 dias)  
                - $\\beta_{apal}$ = Beta apalancada del proyecto  
                - $ERP$ = Prima de riesgo del mercado / Retorno esperado del mercado - $R_f$ (en este caso, para México)
                """)

        elif sec == "Cálculo del WACC":
            with st.container():
                st.subheader("Composición del WACC")
                col1, col2 = st.columns(2)
                col1.metric("Peso de la Deuda", f"{debt_weight*100:.2f}%")
                col2.metric("Costo de la Deuda (Neta)", f"{kd*100:.2f}%")
                col2.metric("Costo de Capital Propio", f"{eq*100:.2f}%")
                col1.metric("Peso del Capital", f"{(1-debt_weight)*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"WACC ESGARI: {wacc*100:.2f}%", icon="📊")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                El **WACC (Weighted Average Cost of Capital)** es una métrica fundamental en finanzas corporativas.

                Indica el costo promedio que tiene una empresa para financiarse, considerando el costo del capital propio y de la deuda.

                Se utiliza para descontar flujos de caja en evaluaciones de proyectos, valuaciones y análisis de retorno.

                Un proyecto es financieramente viable si su retorno es **mayor al WACC**, lo que implica generación de valor.

                **Fórmula utilizada:**

                $$
                WACC = \\left(\\frac{D}{D + E}\\right) \\cdot K_d + \\left(\\frac{E}{D + E}\\right) \\cdot K_e
                $$

                Donde:

                - $D$ = Deuda neta  
                - $E$ = Capital contable  
                - $K_d$ = Costo de la deuda después de impuestos  
                - $K_e$ = Costo de capital propio
                """)

        else:
            with st.container():
                st.subheader("Deuda Neta")
                col1, col2 = st.columns(2)
                col1.metric("Deuda Neta", f"${deuda_neta:,.0f}")
                col2.metric("Deuda Total", f"${deuda:,.0f}")
                col1.metric("Costo de la Deuda", f"{co_de*100:.2f}%")
                col2.metric("Costo de la deuda con escudo fiscal", f"{kd*100:.2f}%")

                st.markdown("### Resultado Final")
                st.success(f"Deuda Neta: ${deuda_neta:,.2f}", icon="💰")

                st.markdown("---")
                st.markdown("### Explicación y Fórmula")
                st.markdown("""
                La **deuda neta** representa la deuda total descontando el efectivo disponible, reflejando lo que realmente se debe financiar con recursos externos.

                El **costo de la deuda** se ajusta con el beneficio fiscal que representa el poder deducir intereses.

                Estas métricas permiten valorar si es más conveniente financiar con deuda o capital, dependiendo de la tasa efectiva que se obtiene.

                **Fórmulas utilizadas:**

                $$
                K_d = K_{deuda} \\cdot (1 - T)
                $$

                $$
                Deuda\\ Neta = Deuda\\ Total - Efectivo
                $$

                Donde:

                - $K_{deuda}$ = Tasa de interés nominal sobre la deuda  
                - $T$ = Tasa de impuesto corporativo  
                - $Efectivo$ = Saldo en bancos disponible
                """)

####PENDIENTE ------------------------------------
    elif selected in ['Balance', 'Balance General', 'Análisis ratios', 'D. de ratios']:

        def limpiar_valores(valor):
            if isinstance(valor, str):
                valor = valor.replace('$', '').replace(',', '').strip()
                if valor in ['-', '', '–', '—']:
                    return 0.0
                try:
                    return float(valor)
                except ValueError:
                    return 0.0
            return float(valor)

        st.markdown("<h2 style='text-align: center;'>Análisis balance</h2>", unsafe_allow_html=True)
        st.markdown("---")
        if selected == "Balance General":
            sec_ba = "Balance General"

        elif selected == "Análisis ratios":
            sec_ba = "Análisis ratios"

        elif selected == "D. de ratios":
            sec_ba = "D. de ratios"

        else:
            sec_ba = option_menu(
                "Cálculos Financieros",
                ["Balance General", "Análisis ratios", "D. de ratios"],
                icons=["graph-up-arrow", "percent", "calculator"],
                orientation="horizontal"
            )

        if sec_ba == "Balance General":

            st.markdown("## Balance General Comparativo ESGARI")
            st.markdown("En miles de MXN")

            df = df_balance.copy()

            df["NETO 2025"] = df["NETO 2025"].apply(limpiar_valores)
            df["NETO 2024"] = df["NETO 2024"].apply(limpiar_valores)

            df["% CAMBIO"] = np.where(
                df["NETO 2024"] == 0,
                0,
                ((df["NETO 2025"] - df["NETO 2024"]) / df["NETO 2024"]) * 100
            )

            def formato_miles(x):
                if pd.isna(x):
                    return "$ -"
                if x == 0:
                    return "$ -"
                return f"$ {x:,.0f}"

            def formato_pct(x):
                if pd.isna(x):
                    return "0.0%"
                return f"{x:.1f}%"

            def crear_tabla_bg(df_lado, titulo_lado):

                filas = []

                filas.append({
                    "CUENTA": titulo_lado,
                    "Actual": "",
                    "LY": "",
                    "% CAMBIO": "",
                    "tipo": "titulo"
                })

                for categoria in df_lado["Categoria"].dropna().unique():

                    filas.append({
                        "CUENTA": categoria.title(),
                        "Actual": "",
                        "LY": "",
                        "% CAMBIO": "",
                        "tipo": "categoria"
                    })

                    df_cat = df_lado[df_lado["Categoria"] == categoria]

                    for _, row in df_cat.iterrows():

                        cuenta = row["CUENTA"]

                        if str(cuenta).upper().startswith("TOTAL"):
                            tipo = "total"
                        else:
                            tipo = "normal"

                        filas.append({
                            "CUENTA": cuenta,
                            "Actual": row["NETO 2025"],
                            "LY": row["NETO 2024"],
                            "% CAMBIO": row["% CAMBIO"],
                            "tipo": tipo
                        })

                    filas.append({
                        "CUENTA": "",
                        "Actual": "",
                        "LY": "",
                        "% CAMBIO": "",
                        "tipo": "espacio"
                    })

                tabla = pd.DataFrame(filas)

                tabla_display = tabla.copy()

                tabla_display["Actual"] = tabla_display["Actual"].apply(
                    lambda x: formato_miles(x) if x != "" else ""
                )

                tabla_display["LY"] = tabla_display["LY"].apply(
                    lambda x: formato_miles(x) if x != "" else ""
                )

                tabla_display["% CAMBIO"] = tabla_display["% CAMBIO"].apply(
                    lambda x: formato_pct(x) if x != "" else ""
                )

                tabla_display = tabla_display[["CUENTA", "Actual", "LY", "% CAMBIO", "tipo"]]

                def estilo_filas(row):

                    if row["tipo"] in ["titulo", "categoria", "total"]:

                        return [
                            "background-color: #002060; color: white; font-weight: bold; border: 1px solid black;"
                        ] * 5

                    if row["tipo"] == "espacio":

                        return [
                            "background-color: white; color: black; height: 18px; border-left: 1px solid black; border-right: 1px solid black;"
                        ] * 5

                    return [
                        "background-color: white; color: black; border-left: 1px solid black; border-right: 1px solid black;"
                    ] * 5

                styled = (
                    tabla_display.drop(columns=["tipo"])
                    .style
                    .apply(lambda row: estilo_filas(tabla_display.loc[row.name]), axis=1)
                    .hide(axis="index")
                    .set_properties(**{
                        "font-size": "14px",
                        "padding": "3px"
                    })
                    .set_table_styles([
                        {
                            "selector": "th",
                            "props": [
                                ("background-color", "#002060"),
                                ("color", "white"),
                                ("font-weight", "bold"),
                                ("text-align", "center"),
                                ("border", "1px solid black")
                            ]
                        },
                        {
                            "selector": "td:nth-child(1)",
                            "props": [
                                ("text-align", "left"),
                                ("min-width", "280px")
                            ]
                        },
                        {
                            "selector": "td:nth-child(2)",
                            "props": [
                                ("text-align", "right"),
                                ("min-width", "100px")
                            ]
                        },
                        {
                            "selector": "td:nth-child(3)",
                            "props": [
                                ("text-align", "right"),
                                ("min-width", "100px")
                            ]
                        },
                        {
                            "selector": "td:nth-child(4)",
                            "props": [
                                ("text-align", "center"),
                                ("min-width", "90px")
                            ]
                        }
                    ])
                )

                return styled

            col1, col2 = st.columns(2)

            df_activo = df[df["Clasificacion"].str.upper() == "ACTIVO"].copy()
            df_pasivo_capital = df[df["Clasificacion"].str.upper() != "ACTIVO"].copy()

            with col1:
                st.table(crear_tabla_bg(df_activo, "Activo"))

            with col2:
                st.table(crear_tabla_bg(df_pasivo_capital, "Pasivo CP"))

            st.markdown("---")
            st.markdown("### Explicación")
            st.markdown("""
            Este balance general comparativo muestra los cambios entre los ejercicios.

            - **Columna "NETO ACTUAL"**: Datos proyectados o reales del ejercicio.
            - **Columna "NETO LY"**: Datos históricos del ejercicio anterior.
            - **Columna "% CAMBIO"**: Variación porcentual entre ambos periodos.

            El análisis permite identificar:
            - Incrementos o reducciones en activos y pasivos clave.
            - Tendencias en financiamiento y rentabilidad.
            - Cambios estructurales importantes en el capital contable.

            > Un cambio positivo en activos o capital puede indicar fortalecimiento, mientras que un aumento en pasivos puede requerir análisis adicional.
            """)

        elif sec_ba == "Análisis ratios":
            st.markdown("## 📊 Análisis de Ratios Financieros Comparativos")
            df = df_balance.copy()

            # Limpieza
            df['NETO 2025'] = df['NETO 2025'].apply(limpiar_valores)
            df['NETO 2024'] = df['NETO 2024'].apply(limpiar_valores)

            # Función para buscar valores por categoría
            def buscar_valor(categoria, year):
                try:
                    return df[df['Categoria'].str.upper() == categoria.upper()][f'NETO {year}'].sum()
                except:
                    return 0.0

            ratio_definiciones = {
                "Razón Circulante": lambda a, p: a / p if p else 0,
                "Endeudamiento": lambda p, a: p / a if a else 0,
                "Autonomía Financiera": lambda c, a: c / a if a else 0,
                "Pasivo / Capital": lambda p, c: p / c if c else 0,
                "Capital / Pasivo Total": lambda c, p: c / p if p else 0,
                "Activo / Capital": lambda a, c: a / c if c else 0,
            }

            # Valores base
            vals = {
                'ACTIVO': {
                    2025: buscar_valor('TOTAL ACTIVO', 2025),
                    2024: buscar_valor('TOTAL ACTIVO', 2024)
                },
                'PASIVO': {
                    2025: buscar_valor('TOTAL PASIVO', 2025),
                    2024: buscar_valor('TOTAL PASIVO', 2024)
                },
                'CAPITAL': {
                    2025: buscar_valor('TOTAL CAPITAL CONTABLE', 2025),
                    2024: buscar_valor('TOTAL CAPITAL CONTABLE', 2024)
                },
                'ACTIVO CIRCULANTE': {
                    2025: buscar_valor('TOTAL ACTIVO CIRCULANTE', 2025),
                    2024: buscar_valor('TOTAL ACTIVO CIRCULANTE', 2024)
                },
                'PASIVO CP': {
                    2025: buscar_valor('TOTAL PASIVO CORTO PLAZO', 2025),
                    2024: buscar_valor('TOTAL PASIVO CORTO PLAZO', 2024)
                }
            }

            # Cálculo de ratios para ambos años
            resultados = []
            for nombre, formula in ratio_definiciones.items():
                if "Circulante" in nombre:
                    v25 = formula(vals['ACTIVO CIRCULANTE'][2025], vals['PASIVO CP'][2025])
                    v24 = formula(vals['ACTIVO CIRCULANTE'][2024], vals['PASIVO CP'][2024])
                elif "Endeudamiento" in nombre:
                    v25 = formula(vals['PASIVO'][2025], vals['ACTIVO'][2025])
                    v24 = formula(vals['PASIVO'][2024], vals['ACTIVO'][2024])
                elif "Autonomía" in nombre:
                    v25 = formula(vals['CAPITAL'][2025], vals['ACTIVO'][2025])
                    v24 = formula(vals['CAPITAL'][2024], vals['ACTIVO'][2024])
                elif "Pasivo / Capital" in nombre:
                    v25 = formula(vals['PASIVO'][2025], vals['CAPITAL'][2025])
                    v24 = formula(vals['PASIVO'][2024], vals['CAPITAL'][2024])
                elif "Capital / Pasivo" in nombre:
                    v25 = formula(vals['CAPITAL'][2025], vals['PASIVO'][2025])
                    v24 = formula(vals['CAPITAL'][2024], vals['PASIVO'][2024])
                elif "Activo / Capital" in nombre:
                    v25 = formula(vals['ACTIVO'][2025], vals['CAPITAL'][2025])
                    v24 = formula(vals['ACTIVO'][2024], vals['CAPITAL'][2024])
                else:
                    v25 = v24 = 0
                delta = v25 - v24
                resultados.append({"Ratio": nombre, "2025": v25, "2024": v24, "Δ": delta})

            df_ratios = pd.DataFrame(resultados)

            # Mostrar métricas individuales
            st.markdown("### 📈 Comparativo de ratios financieros clave")
            for i, row in df_ratios.iterrows():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(row["Ratio"], f"{row['2025']:.2f}", delta=f"{row['Δ']:+.2f}")
                with col2:
                    st.metric(f"**2024:** ", f"{row['2024']:.2f}")
                with col3:
                    st.write(f"""
                        {row['Ratio']}:
                        {({
                            'Razón Circulante': "Capacidad para cubrir pasivos de corto plazo con activos líquidos.",
                            'Endeudamiento': "Porción de activos financiada por deuda.",
                            'Autonomía Financiera': "Grado de independencia financiera frente a terceros.",
                            'Pasivo / Capital': "Nivel de apalancamiento sobre capital propio.",
                            'Capital / Pasivo Total': "Capacidad de capital propio frente a obligaciones.",
                            'Activo / Capital': "Multiplicador del capital invertido en activos."
                        })[row['Ratio']]}
                    """)

            # Visualización interactiva con Plotly

            st.markdown("### 📊 Evolución gráfica comparativa")
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df_ratios["Ratio"], y=df_ratios["2024"], name='2024'))
            fig.add_trace(go.Bar(x=df_ratios["Ratio"], y=df_ratios["2025"], name='2025'))
            fig.update_layout(
                barmode='group',
                title="Ratios Financieros: Comparación 2025 vs 2024",
                yaxis_title="Valor del Ratio",
                xaxis_title="Ratio",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

        elif sec_ba == "D. de ratios":
            st.markdown(" Desglose de Ratios Financieros Comparativos")
            df = df_balance.copy()

            # Limpieza
            df['NETO 2025'] = df['NETO 2025'].apply(limpiar_valores)
            df['NETO 2024'] = df['NETO 2024'].apply(limpiar_valores)

            endeudamiento_25 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2025'].values[0]
            endeudamiento_24 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2024'].values[0]

            pasivo_LP_25 = (df[df['CUENTA'] == 'Contratos por derecho de uso']['NETO 2025'].values[0]
            + df[df['CUENTA'] == 'Creditos Bancarios']['NETO 2025'].values[0]
            + df[df['CUENTA'] == 'Impuestos Diferidos']['NETO 2025'].values[0])
            endeudamiento_LP_25 = pasivo_LP_25 / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2025'].values[0]

            pasivo_LP_24 = (df[df['CUENTA'] == 'Contratos por derecho de uso']['NETO 2024'].values[0]
            + df[df['CUENTA'] == 'Creditos Bancarios']['NETO 2024'].values[0]
            + df[df['CUENTA'] == 'Impuestos Diferidos']['NETO 2024'].values[0])
            endeudamiento_LP_24 = pasivo_LP_24 / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2024'].values[0]

            deuda_25 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2025'].values[0]
            deuda_24 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2024'].values[0]

            apalancamiento_25 = df[df['CUENTA'] == 'Total Activo']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2025'].values[0]
            apalancamiento_24 = df[df['CUENTA'] == 'Total Activo']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Capital Contable']['NETO 2024'].values[0]

            razon_circulante_25 = df[df['CUENTA'] == 'Total Activo Circulante']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2025'].values[0]
            razon_circulante_24 = df[df['CUENTA'] == 'Total Activo Circulante']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2024'].values[0]

            caja_25 = df[df['CUENTA'] == 'Bancos']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2025'].values[0]
            caja_24 = df[df['CUENTA'] == 'Bancos']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2024'].values[0]

            activo_circulante_25 = df[df['CUENTA'] == 'Total Activo Circulante']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2025'].values[0]
            activo_circulante_24 = df[df['CUENTA'] == 'Total Activo Circulante']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2024'].values[0]

            activo_fijo_25 = df[df['CUENTA'] == 'Total Activos Fijos, Neto']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2025'].values[0]
            activo_fijo_24 = df[df['CUENTA'] == 'Total Activos Fijos, Neto']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2024'].values[0]

            activo_diferido_25 = df[df['CUENTA'] == 'Total Activo Diferido']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2025'].values[0]
            activo_diferido_24 = df[df['CUENTA'] == 'Total Activo Diferido']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Activo']['NETO 2024'].values[0]

            pasivo_cp_25 = df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2025'].values[0]
            pasivo_cp_24 = df[df['CUENTA'] == 'Total Pasivos CP']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2024'].values[0]

            pasivo_lp_25 = (df[df['CUENTA'] == 'Contratos por derecho de uso']['NETO 2025'].values[0] 
            + df[df['CUENTA'] == 'Creditos Bancarios']['NETO 2025'].values[0]
            + df[df['CUENTA'] == 'Impuestos Diferidos']['NETO 2025'].values[0]
            + df[df['CUENTA'] == 'Reserva indemnizaciones']['NETO 2025'].values[0])

            pasivo_lp_total_25 = pasivo_lp_25 / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2025'].values[0]

            pasivo_lp_24 = (df[df['CUENTA'] == 'Contratos por derecho de uso']['NETO 2024'].values[0]
            + df[df['CUENTA'] == 'Creditos Bancarios']['NETO 2024'].values[0]
            + df[df['CUENTA'] == 'Impuestos Diferidos']['NETO 2024'].values[0]
            + df[df['CUENTA'] == 'Reserva indemnizaciones']['NETO 2024'].values[0])
            pasivo_lp_total_24 = pasivo_lp_24 / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2024'].values[0]

            pasivo_total_25 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2025'].values[0]
            pasivo_total_24 = df[df['CUENTA'] == 'Total Pasivo']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2024'].values[0]

            capital_contable_25 = df[df['CUENTA'] == 'Total Capital Contable']['NETO 2025'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2025'].values[0]
            capital_contable_24 = df[df['CUENTA'] == 'Total Capital Contable']['NETO 2024'].values[0] / df[df['CUENTA'] == 'Total Pasivo y Capital']['NETO 2024'].values[0]

            pasivo_capital_25 = pasivo_lp_total_25 + capital_contable_25 + pasivo_cp_25
            pasivo_capital_24 = pasivo_lp_total_24 + capital_contable_24 + pasivo_cp_24

            Activo_total_25 = activo_circulante_25 + activo_fijo_25 + activo_diferido_25
            Activo_total_24 = activo_circulante_24 + activo_fijo_24 + activo_diferido_24

            filas_azules = [
                "Ratio de solvencia",
                "Ratio de liquidez",
                "PROPORCIONES BG",
                "Activo Total",
                "Pasivo + Capital"
            ]

            # Flechas
            def flecha(actual, ly, invertido=False):

                if pd.isna(actual) or pd.isna(ly):
                    return ""

                if invertido:
                    if actual < ly:
                        return "🔼"
                    elif actual > ly:
                        return "🔽"
                    else:
                        return "➡️"

                else:
                    if actual > ly:
                        return "🔼"
                    elif actual < ly:
                        return "🔽"
                    else:
                        return "➡️"


            cambios = [
                "",  # Ratio de solvencia
                flecha(endeudamiento_25, endeudamiento_24, invertido=True),
                flecha(endeudamiento_LP_25, endeudamiento_LP_24, invertido=True),
                flecha(deuda_25, deuda_24, invertido=True),
                flecha(apalancamiento_25, apalancamiento_24, invertido=True),

                "",  # Ratio de liquidez
                flecha(razon_circulante_25, razon_circulante_24),
                flecha(caja_25, caja_24),

                "",  # PROPORCIONES BG
                flecha(activo_circulante_25, activo_circulante_24),
                flecha(activo_fijo_25, activo_fijo_24, invertido=True),
                flecha(activo_diferido_25, activo_diferido_24, invertido=True),
                "",  # Activo Total

                flecha(pasivo_cp_25, pasivo_cp_24, invertido=True),
                flecha(pasivo_lp_total_25, pasivo_lp_total_24, invertido=True),
                flecha(pasivo_total_25, pasivo_total_24, invertido=True),
                flecha(capital_contable_25, capital_contable_24),
                ""  # Pasivo + Capital
            ]

            df_ratios = pd.DataFrame({
                "Ratios": [
                    "Ratio de solvencia",
                    "De Endeudamiento",
                    "De Endeudamiento LP",
                    "De Deuda",
                    "De Apalancamiento",

                    "Ratio de liquidez",
                    "Razón Circulante",
                    "De Caja",

                    "PROPORCIONES BG",
                    "Activo Circulante",
                    "Activo Fijo",
                    "Activo Diferido",
                    "Activo Total",

                    "Pasivo CP",
                    "Pasivo LP",
                    "Pasivo Total",
                    "Capital Contable",
                    "Pasivo + Capital"
                ],

                "Actual": [
                    "",
                    endeudamiento_25,
                    endeudamiento_LP_25,
                    deuda_25,
                    apalancamiento_25,

                    "",
                    razon_circulante_25,
                    caja_25,

                    "",
                    activo_circulante_25,
                    activo_fijo_25,
                    activo_diferido_25,
                    Activo_total_25,

                    pasivo_cp_25,
                    pasivo_lp_total_25,
                    pasivo_total_25,
                    capital_contable_25,
                    pasivo_capital_25
                ],

                "LY": [
                    "",
                    endeudamiento_24,
                    endeudamiento_LP_24,
                    deuda_24,
                    apalancamiento_24,

                    "",
                    razon_circulante_24,
                    caja_24,

                    "",
                    activo_circulante_24,
                    activo_fijo_24,
                    activo_diferido_24,
                    Activo_total_24,

                    pasivo_cp_24,
                    pasivo_lp_total_24,
                    pasivo_total_24,
                    capital_contable_24,
                    pasivo_capital_24
                ],

                "Cambio": cambios
            })

            filas_porcentaje = [
                "Activo Circulante",
                "Activo Fijo",
                "Activo Diferido",
                "Activo Total",
                "Pasivo CP",
                "Pasivo LP",
                "Pasivo Total",
                "Capital Contable",
                "Pasivo + Capital"
            ]

            def formato_valor(row, col):

                valor = row[col]

                if valor == "":
                    return ""

                if row["Ratios"] in filas_porcentaje:
                    return f"{valor:.0%}"

                return f"{valor:,.2f}"

            df_display = df_ratios.copy()

            df_display["Actual"] = df_display.apply(
                lambda row: formato_valor(row, "Actual"),
                axis=1
            )

            df_display["LY"] = df_display.apply(
                lambda row: formato_valor(row, "LY"),
                axis=1
            )

            def estilo_filas(row):

                if row["Ratios"] in filas_azules:

                    return [
                        'background-color: #002060; color: white; font-weight: bold'
                    ] * len(row)

                return [''] * len(row)

            styled_df = (
                df_display.style
                .apply(estilo_filas, axis=1)
                .hide(axis="index")
                .set_properties(**{
                    'text-align': 'left',
                    'padding': '6px',
                    'font-size': '14px'
                })
                .set_table_styles([
                    {
                        'selector': 'th',
                        'props': [
                            ('background-color', '#002060'),
                            ('color', 'white'),
                            ('font-weight', 'bold'),
                            ('text-align', 'center')
                        ]
                    },
                    {
                        'selector': 'td:nth-child(2)',
                        'props': [('text-align', 'center')]
                    },
                    {
                        'selector': 'td:nth-child(3)',
                        'props': [('text-align', 'center')]
                    },
                    {
                        'selector': 'td:nth-child(4)',
                        'props': [('text-align', 'center')]
                    }
                ])
            )

            st.table(styled_df)

###Estado de resultados   ------------------------------------
    elif selected in ['E.Resultados', 'Flujo de Efectivo', 'Ratios', 'Dupont']:

        def limpiar_valores(valor):
            if isinstance(valor, str):
                valor = valor.replace('$', '').replace(',', '').strip()
                if valor in ['-', '', '–', '—']:
                    return 0.0
                try:
                    return float(valor)
                except ValueError:
                    return 0.0
            return float(valor)

        st.markdown("<h2 style='text-align: center;'>Información Financiera ESGARI</h2>", unsafe_allow_html=True)
        st.markdown("---")

        if selected == "E.Resultados":
            sec_ba = "E.Resultados"

        elif selected == "Flujo de Efectivo":
            sec_ba = "Flujo de Efectivo"

        elif selected == "Ratios":
            sec_ba = "Ratios"

        elif selected == "Dupont":
            sec_ba = "Dupont"

        else:
            sec_ba = option_menu(
                "Cálculos Financieros",
                ["E.Resultados", "Flujo de Efectivo", "Ratios", "Dupont"],
                icons=["clipboard-data", "briefcase", "percent", "diagram-3"],
                orientation="horizontal"
            )
        if sec_ba == "E.Resultados":

            st.markdown("## Estado de Resultados ESGARI")
            st.markdown("En miles de MXN")

            df = df_er.copy()
            df['Monto'] = df['Monto'].apply(limpiar_valores)

            # 🔹 Jerarquía (indentación)
            indent_map = {
                "Fletes": 1,
                "Combustible & Casetas": 1,
                "Activos por derecho de uso": 1,
                "Nomina Operadores": 1,
                "Otros": 1,
            }

            def aplicar_indentacion(cuenta):
                nivel = indent_map.get(cuenta, 0)
                return "&nbsp;" * 6 * nivel + cuenta

            df["Cuenta"] = df["Cuenta"].apply(aplicar_indentacion)

            # 🔹 Filas especiales
            filas_azules = [
                "Ingreso", "Utilidad Bruta", "Utilidad de Operación",
                "Utilidad Antes de Impuestos", "UTILIDAD NETA"
            ]

            filas_gris = ["Costo De Ventas"]

            # 🔹 Estilos
            def estilo_filas(row):
                if row["Cuenta"] in filas_azules:
                    return ['background-color: #0b2e6b; color: white; font-weight: bold'] * 2
                elif row["Cuenta"] in filas_gris:
                    return ['background-color: #8e6e6e6; font-weight: bold'] * 2
                else:
                    return [''] * 2

            styled_df = df[["Cuenta", "Monto"]].style \
                .apply(estilo_filas, axis=1) \
                .format({"Monto": "${:,.0f}"}) \
                .hide(axis="index") \
                .set_properties(**{
                    'text-align': 'left',
                    'padding': '6px'
                }) \
                .set_table_styles([
                    {
                        'selector': 'th',
                        'props': [
                            ('background-color', '#4f81bd'),
                            ('color', 'white'),
                            ('font-weight', 'bold'),
                            ('text-align', 'left')
                        ]
                    },
                    {
                        'selector': 'td:nth-child(2)',
                        'props': [('text-align', 'right')]
                    }
                ])

            st.table(styled_df)
        


        elif sec_ba == "Flujo de Efectivo":
            st.markdown("## Flujo de Efectivo ESGARI")
            st.markdown("En miles de MXN")
            df = df_balance.copy()
            df = df_er.copy()

            Utilidad_neta = df_er[df_er["Cuenta"] == "UTILIDAD NETA"]["Monto"].values[0]
            Dep_amortizacion = df_er[df_er["Cuenta"] == "AMORT Y DEP"]["Monto"].values[0]
            Utilidad_DA = Utilidad_neta + Dep_amortizacion

            ac_2025 = (
                df_balance[df_balance["CUENTA"] == "Cuentas por cobrar."]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Deudores diversos."]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Otros Activos"]["NETO 2025"].values[0]
            )

            ac_2024 = (
                df_balance[df_balance["CUENTA"] == "Cuentas por cobrar."]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Deudores diversos."]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Otros Activos"]["NETO 2024"].values[0]
            )

            Variacion_AC = ac_2024 - ac_2025

            pc_2025 = (
                df_balance[df_balance["CUENTA"] == "Proveedores"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "IVA trasladado"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Pasivos Acumulados"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Provision ISR y PTU"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Reserva indemnizaciones"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Impuestos Diferidos"]["NETO 2025"].values[0]
            )

            pc_2024 = (
                df_balance[df_balance["CUENTA"] == "Proveedores"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "IVA trasladado"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Pasivos Acumulados"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Provision ISR y PTU"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Reserva indemnizaciones"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Impuestos Diferidos"]["NETO 2024"].values[0]
            )

            Variacion_PC = pc_2025 - pc_2024

            Cambio_AD = (
                df_balance[df_balance["CUENTA"] == "Total Activo Diferido"]["NETO 2024"].values[0]
                - df_balance[df_balance["CUENTA"] == "Total Activo Diferido"]["NETO 2025"].values[0]
            )

            Flujo_operativo = Utilidad_DA + Variacion_AC + Variacion_PC + Cambio_AD

            inversion = (
                df_balance[df_balance["CUENTA"] == "Total Activos Fijos, Neto"]["NETO 2024"].values[0]
                - df_balance[df_balance["CUENTA"] == "Total Activos Fijos, Neto"]["NETO 2025"].values[0]
            )

            inversion_total = inversion - Dep_amortizacion

            arrenda_25 = (
                df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2025"].values[0]
            )

            arrenda_24 = (
                df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2024"].values[0]
            )

            arrenda_total = arrenda_25 - arrenda_24

            ## cambiar variable, no se considera todo el capital
            capital1 = (
                df_balance[df_balance["CUENTA"] == "Capital social"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Utilidades Acumuladas"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Adquisicion de Negocio"]["NETO 2025"].values[0]
            )

            capital2 = (
                df_balance[df_balance["CUENTA"] == "Capital social"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Utilidades Acumuladas"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Adquisicion de Negocio"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Utilidad del Ejercicio"]["NETO 2024"].values[0]
            )

            adquisicion = capital1 - capital2

            deuda_25 = (
                df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Acreedores diversos"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2025"].values[0]
            )

            deuda_24 = (
                df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Acreedores diversos"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2024"].values[0]
            )

            pago_deuda = deuda_25 - deuda_24

            flujo_financiamiento = adquisicion + pago_deuda + arrenda_total

            efectivo_periodo = Flujo_operativo + inversion_total + flujo_financiamiento

            flujo_inicial = df_balance[df_balance["CUENTA"] == "Bancos"]["NETO 2024"].values[0]
            flujo_final = efectivo_periodo + flujo_inicial
            Saldo_bancos = df_balance[df_balance["CUENTA"] == "Bancos"]["NETO 2025"].values[0]

            st.session_state["Flujo operativo"] = Flujo_operativo
            st.session_state["Utilidad neta"] = Utilidad_neta
            st.session_state["Efectivo del periodo"] = efectivo_periodo
            st.session_state["Flujo financiamiento"] = flujo_financiamiento
            st.session_state["Inversion total"] = inversion_total
            st.session_state["Flujo final"] = flujo_final

            # Tabla detallada estilo reporte 
            df_flujo = pd.DataFrame({
                "Concepto": [
                    "Estado de flujo de efectivo",
                    "",
                    "Utilidad neta",
                    "Depreciaciones y amortizaciones",
                    "Utilidad después de depreciaciones y amortizaciones",
                    "",
                    "Cambios en capital de trabajo",
                    "Cambio Activo Circulante",
                    "Cambio Pasivo Circulante",
                    "Cambio diferido",
                    "",
                    "Flujo de efectivo de actividades de operación",
                    "",
                    "Inversiones (+ desinversiones)",
                    "Flujo de efectivo de actividades de inversión",
                    "",
                    "Arrendamientos",
                    "Adquisicion de Negocio// Dividendos",
                    "Adquisicion de deuda",
                    "Flujo de efectivo de actividades de financiamiento",
                    "",
                    "Efectivo del periodo",
                    "Flujo inicial del periodo",
                    "Flujo final de periodo",
                    "SALDO EN BANCOS"
                ],
                "Monto": [
                    "",
                    "",
                    Utilidad_neta,
                    Dep_amortizacion,
                    Utilidad_DA,
                    "",
                    "",
                    Variacion_AC,
                    Variacion_PC,
                    Cambio_AD,
                    "",
                    Flujo_operativo,
                    "",
                    inversion_total,
                    inversion_total,
                    "",
                    arrenda_total,
                    adquisicion,
                    pago_deuda,
                    flujo_financiamiento,
                    "",
                    efectivo_periodo,
                    flujo_inicial,
                    flujo_final,
                    Saldo_bancos
                ]
            })

            filas_azules = [
                "Estado de flujo de efectivo",
                "Utilidad neta",
                "Depreciaciones y amortizaciones",
                "Utilidad después de depreciaciones y amortizaciones",
                "Cambios en capital de trabajo",
                "Flujo de efectivo de actividades de operación",
                "Flujo de efectivo de actividades de inversión",
                "Flujo de efectivo de actividades de financiamiento",
                "Efectivo del periodo",
                "SALDO EN BANCOS"
            ]

            filas_claras = [
                "Flujo de efectivo de actividades de operación",
                "Flujo de efectivo de actividades de inversión",
                "Flujo de efectivo de actividades de financiamiento",
                "Flujo final de periodo"
            ]

            def estilo_filas(row):
                if row["Concepto"] in filas_azules:
                    return ['background-color: #0b2e6b; color: white; font-weight: bold'] * 2
                elif row["Concepto"] in filas_claras:
                    return ['background-color: #b8c6df; font-weight: bold'] * 2
                elif row["Concepto"] == "":
                    return ['background-color: #f2f2f2'] * 2
                else:
                    return ['background-color: #0b2e6b; color: white'] * 2 if "Cambio" in row["Concepto"] or "Arrendamientos" in row["Concepto"] else [''] * 2

            styled = df_flujo.style \
                .apply(estilo_filas, axis=1) \
                .format({"Monto": lambda x: "" if x == "" else f"${x:,.0f}"}) \
                .hide(axis="index") \
                .set_properties(**{
                    'padding': '6px',
                    'text-align': 'left'
                }) \
                .set_table_styles([
                    {
                        'selector': 'td:nth-child(2)',
                        'props': [('text-align', 'right')]
                    },
                    {
                        'selector': 'th',
                        'props': [
                            ('background-color', '#d9d9d9'),
                            ('font-weight', 'bold')
                        ]
                    }
                ])

            st.table(styled)

        elif sec_ba == "Ratios":
            st.markdown("## Análisis de Ratios Financieros")
            df = df_balance.copy()
            df = df_er.copy()
            
            Flujo_operativo = st.session_state.get("Flujo operativo", 0)
            Utilidad_neta = st.session_state.get("Utilidad neta", 0)
            flujo_financiamiento = st.session_state.get("Flujo financiamiento", 0)
            inversion_total = st.session_state.get("Inversion total", 0)
            efectivo_periodo = st.session_state.get("Efectivo del periodo", 0)
            flujo_final = st.session_state.get("Flujo final", 0)

            cintereses = (
                Flujo_operativo
                / df_er[df_er["Cuenta"] == "Resultado Financiero Integral"]["Monto"].values[0]
                if df_er[df_er["Cuenta"] == "Resultado Financiero Integral"]["Monto"].values[0] != 0
                else 0
            )

            deuda2 = (
                df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2025"].values[0]
            )

            cdeuda = Flujo_operativo / deuda2 if deuda2 != 0 else 0

            deuda3 = (
                df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2025"].values[0]
            )

            cdeuda2 = Flujo_operativo / deuda3 if deuda3 != 0 else 0

            cpasivocirculante = (
                Flujo_operativo
                / df_balance[df_balance["CUENTA"] == "Total Pasivos CP"]["NETO 2025"].values[0]
                if df_balance[df_balance["CUENTA"] == "Total Pasivos CP"]["NETO 2025"].values[0] != 0
                else 0
            )

            Efectividad_fo = (
                Flujo_operativo / Utilidad_neta
                if Utilidad_neta != 0
                else 0
            )

            Efectividad_fv = (
                Flujo_operativo
                / df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0]
                if df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] != 0
                else 0
            )

            col1, col2, col3 = st.columns(3)

            col1.metric("Cobertura de Intereses", f"{cintereses:.2f}")
            col2.metric("Cobertura de Deuda Total", f"{cdeuda:.2f}")
            col3.metric("Cobertura de Deuda Bancaria", f"{cdeuda2:.2f}")

            st.markdown("### Ratios de Liquidez y Efectividad")

            col1, col2 = st.columns(2)

            col1.metric("Cobertura de Pasivo Circulante", f"{cpasivocirculante:.2f}")
            col2.metric("Efectividad del Flujo Operativo", f"{Efectividad_fo:.2f}")

            col1.metric("Efectividad del Flujo Operativo Ventas", f"{Efectividad_fv:.2f}")

            st.markdown("---")
            st.markdown("### ROIC")
            nopat = df_er[df_er["Cuenta"] == "Utilidad de Operación"]["Monto"].values[0] * (1 - 0.40)
            aver_inicial = (df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Contrato de derecho de uso (CP)"]["NETO 2024"].values[0]
            + df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Contratos por derecho de uso"]["NETO 2024"].values[0]
            + df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Creditos Bancarios"]["NETO 2024"].values[0]
            + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Creditos Bancarios CP"]["NETO 2024"].values[0]
            + df_balance[df_balance["CUENTA"] == "Total Capital Contable"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Total Capital Contable"]["NETO 2024"].values[0]
            )
            aver = (aver_inicial / 2) - df_balance[df_balance["CUENTA"] == "Bancos"]["NETO 2025"].values[0]


            roic = nopat / aver if aver != 0 else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("NOPAT", f"${nopat:,.0f}")
            col2.metric("Capital Invertido Promedio", f"${aver:,.0f}")
            col3.metric("ROIC", f"{roic:.2%}")


            st.markdown("---")
            st.markdown("### Estructura del Capital")

            saldo_inicial_c = df_balance[df_balance["CUENTA"] == "Capital social"]["NETO 2024"].values[0]
            saldo_inicial_u = (
                df_balance[df_balance["CUENTA"] == "Utilidades Acumuladas"]["NETO 2024"].values[0]
                + df_balance[df_balance["CUENTA"] == "Adquisicion de Negocio"]["NETO 2024"].values[0]
            )
            saldo_inicial_r = df_balance[df_balance["CUENTA"] == "Utilidad del Ejercicio"]["NETO 2024"].values[0]

            saldo_inicial_total = saldo_inicial_c + saldo_inicial_u + saldo_inicial_r

            # Traspaso de utilidad
            traspaso_u = saldo_inicial_r
            traspaso_r = -saldo_inicial_r

            # Resultado actual
            resultado_ejercicio = Utilidad_neta

            # Adquisición / goodwill
            adquisicion = (
                df_balance[df_balance["CUENTA"] == "Adquisicion de Negocio"]["NETO 2025"].values[0]
                - df_balance[df_balance["CUENTA"] == "Adquisicion de Negocio"]["NETO 2024"].values[0]
            )

            # Saldos finales
            saldo_final_c = saldo_inicial_c
            saldo_final_u = saldo_inicial_u + traspaso_u + adquisicion
            saldo_final_r = resultado_ejercicio
            saldo_final_total = saldo_final_c + saldo_final_u + saldo_final_r

            df_capital = pd.DataFrame({
                "EN MILES (000 MXN)": [
                    "Saldo inicial al 1° de enero 2026",
                    "Traspaso de resultados del ejercicio anterior",
                    "Resultado del ejercicio",
                    "Adquisicion del Negocio",
                    "Saldo final"
                ],

                "Capital Social": [
                    saldo_inicial_c,
                    0,
                    0,
                    0,
                    saldo_final_c
                ],

                "Utilidad Ejercicios Anteriores": [
                    saldo_inicial_u,
                    traspaso_u,
                    0,
                    adquisicion,
                    saldo_final_u
                ],

                "Resultado del Ejercicio": [
                    saldo_inicial_r,
                    traspaso_r,
                    resultado_ejercicio,
                    0,
                    saldo_final_r
                ],

                "Total Capital Contable": [
                    saldo_inicial_total,
                    0,
                    resultado_ejercicio,
                    adquisicion,
                    saldo_final_total
                ]
            })

            columnas_numericas = [
                "Capital Social",
                "Utilidad Ejercicios Anteriores",
                "Resultado del Ejercicio",
                "Total Capital Contable"
            ]

            def formato_miles(x):
                if pd.isna(x):
                    return ""
                if x == 0:
                    return "$ -"
                return f"$ {x:,.0f}"

            df_capital_format = df_capital.copy()

            for col in columnas_numericas:
                df_capital_format[col] = df_capital_format[col].apply(formato_miles)

            filas_azules = [
                "Saldo inicial al 1° de enero 2026",
                "Saldo final"
            ]

            def estilo_filas(row):
                if row["EN MILES (000 MXN)"] in filas_azules:
                    return [
                        "background-color: #9dc3e6; color: black; font-weight: bold;"
                    ] * len(row)

                return [
                    "background-color: white; color: black; font-weight: bold;"
                ] * len(row)

            styled_df = (
                df_capital_format.style
                .apply(estilo_filas, axis=1)
                .hide(axis="index")
                .set_properties(**{
                    "border": "1px solid black",
                    "padding": "4px",
                    "font-size": "14px"
                })
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#002060"),
                            ("color", "white"),
                            ("font-weight", "bold"),
                            ("text-align", "center"),
                            ("border", "1px solid black")
                        ]
                    },
                    {
                        "selector": "td:nth-child(1)",
                        "props": [
                            ("text-align", "left"),
                            ("min-width", "320px")
                        ]
                    },
                    {
                        "selector": "td:nth-child(n+2)",
                        "props": [
                            ("text-align", "right"),
                            ("min-width", "120px")
                        ]
                    }
                ])
            )

            st.table(styled_df)

            st.markdown("---")
            st.markdown("### Resumen Flujo de Efectivo")

            df_flujo_resumen = pd.DataFrame({
                "Comparativa": [
                    "Flujo de efectivo de actividades de operación",
                    "Flujo de efectivo de actividades de inversión",
                    "Flujo de efectivo de actividades de financiamiento",
                    "Efectivo del periodo",
                    "Flujo final de periodo"
                ],

                "Actual": [
                    Flujo_operativo,
                    inversion_total,
                    flujo_financiamiento,
                    efectivo_periodo,
                    flujo_final
                ]
            })


            def formato_miles(x):

                if pd.isna(x):
                    return ""

                if x == 0:
                    return "$ -"

                return f"$ {x:,.0f}"

            df_flujo_resumen_format = df_flujo_resumen.copy()

            df_flujo_resumen_format["Actual"] = (
                df_flujo_resumen_format["Actual"]
                .apply(formato_miles)
            )


            filas_azules = [
                "Efectivo del periodo",
                "Flujo final de periodo"
            ]

            def estilo_filas(row):

                if row["Comparativa"] in filas_azules:

                    return [
                        "background-color: #9dc3e6; color: black; font-weight: bold;"
                    ] * len(row)

                return [
                    "background-color: white; color: black;"
                ] * len(row)

            styled_df = (
                df_flujo_resumen_format.style
                .apply(estilo_filas, axis=1)
                .hide(axis="index")
                .set_properties(**{
                    "border": "1px solid black",
                    "padding": "4px",
                    "font-size": "14px"
                })
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#002060"),
                            ("color", "white"),
                            ("font-weight", "bold"),
                            ("text-align", "center"),
                            ("border", "1px solid black")
                        ]
                    },
                    {
                        "selector": "td:nth-child(1)",
                        "props": [
                            ("text-align", "left"),
                            ("min-width", "500px")
                        ]
                    },
                    {
                        "selector": "td:nth-child(2)",
                        "props": [
                            ("text-align", "right"),
                            ("min-width", "150px")
                        ]
                    }
                ])
            )

            st.table(styled_df)

        elif sec_ba == "Dupont":
            st.markdown("## Análisis Dupont")
            df = df_balance.copy()
            df = df_er.copy()

            Utilidad_neta = st.session_state.get("Utilidad neta", 0)

            Average_equity = (df_balance[df_balance["CUENTA"] == "Total Capital Contable"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Total Capital Contable"]["NETO 2024"].values[0]) / 2
            Average_assets = (df_balance[df_balance["CUENTA"] == "Total Pasivo y Capital"]["NETO 2025"].values[0] + df_balance[df_balance["CUENTA"] == "Total Pasivo y Capital"]["NETO 2024"].values[0]) / 2

            ROE = Utilidad_neta / Average_equity if Average_equity != 0 else 0
            ROA = Utilidad_neta / Average_assets if Average_assets != 0 else 0
            Leverage = Average_assets / Average_equity if Average_equity != 0 else 0
            Net_profit_margin = Utilidad_neta / df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] if df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] != 0 else 0
            Total_asset_turnover = df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] / Average_assets if Average_assets != 0 else 0
            Tax_burden =  Utilidad_neta / df_er[df_er["Cuenta"] == "Utilidad Antes de Impuestos"]["Monto"].values[0]
            interest_burden = df_er[df_er["Cuenta"] == "Utilidad Antes de Impuestos"]["Monto"].values[0] / df_er[df_er["Cuenta"] == "Utilidad de Operación"]["Monto"].values[0] if df_er[df_er["Cuenta"] == "Utilidad de Operación"]["Monto"].values[0] != 0 else 0
            ebit_margin = df_er[df_er["Cuenta"] == "Utilidad de Operación"]["Monto"].values[0] / df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] if df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] != 0 else 0


            st.markdown("### Desglose del ROE por componentes")
            col1, col2, col3 = st.columns(3)    
            col1.metric("ROE", f"{ROE:.2%}")
            col2.metric("ROA", f"{ROA:.2%}")
            col3.metric("Leverage", f"{Leverage:.2f}")

            st.markdown("### Margen, Rotación y Carga Fiscal")
            col1, col2, col3 = st.columns(3)
            col1.metric("Margen Neto", f"{Net_profit_margin:.2%}")
            col2.metric("Rotación de Activos", f"{Total_asset_turnover:.2%}")
            col3.metric("Carga Fiscal", f"{Tax_burden:.2%}")

            st.markdown("### Carga por Intereses y Margen Operativo")
            col1, col2 = st.columns(2)
            col1.metric("Carga por Intereses", f"{interest_burden:.2%}")
            col2.metric("Margen EBIT", f"{ebit_margin:.2%}")
            
            st.markdown("---")
            st.markdown("### Ciclo Financieros")

            trimestre_sel = st.selectbox(
                "Selecciona el trimestre para calcular el ciclo financiero",
                ["1T", "2T", "3T", "4T"]
            )

            # 🔹 Días por trimestre
            mapa_trimestre = {
                "1T": 90,
                "2T": 180,
                "3T": 270,
                "4T": 360
            }

            dias_trimestre = mapa_trimestre[trimestre_sel]

            promedio_cxp = (
                df_balance[df_balance["CUENTA"] == "Proveedores"]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Proveedores"]["NETO 2024"].values[0]
            ) / 2

            promedio_cxc = (
                df_balance[df_balance["CUENTA"] == "Cuentas por cobrar."]["NETO 2025"].values[0]
                + df_balance[df_balance["CUENTA"] == "Cuentas por cobrar."]["NETO 2024"].values[0]
            ) / 2

            dias_cxc = (
                (promedio_cxc * dias_trimestre)
                / df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0]
                if df_er[df_er["Cuenta"] == "Ingreso"]["Monto"].values[0] != 0
                else 0
            )

            dias_cxp = (
                (promedio_cxp * dias_trimestre)
                / df_er[df_er["Cuenta"] == "Costo de Ventas"]["Monto"].values[0]
                if df_er[df_er["Cuenta"] == "Costo de Ventas"]["Monto"].values[0] != 0
                else 0
            )

            ciclo_operativo = dias_cxc
            ciclo_financiero = dias_cxc - dias_cxp

            # 🔹 HTML estilo dashboard
            html = f"""
            <div style="width: 350px; font-family: Arial;">

                <div style="text-align:center; font-weight:bold; border:1px solid black; padding:5px;">
                    {trimestre_sel} 2026
                </div>

                <div style="display:flex;">
                    <div style="background:#0b2e6b; color:white; padding:8px; width:70%; font-weight:bold;">
                        CICLO OPERATIVO
                    </div>
                    <div style="border:1px solid black; width:30%; text-align:center; padding:8px;">
                        {ciclo_operativo:,.0f}
                    </div>
                </div>

                <div style="background:#0b2e6b; color:white; padding:8px; margin-top:10px; width:70%; font-weight:bold;">
                    DIAS CXC
                </div>

                <div style="border:1px solid black; width:70%; text-align:center; padding:8px;">
                    {dias_cxc:,.0f}
                </div>

                <div style="display:flex; margin-top:15px;">
                    <div style="background:#0b2e6b; color:white; padding:8px; width:70%; font-weight:bold;">
                        CICLO FINANCIERO
                    </div>
                    <div style="border:1px solid black; width:30%; text-align:center; padding:8px;">
                        {ciclo_financiero:,.0f}
                    </div>
                </div>

                <div style="display:flex; margin-top:10px;">
                    <div style="background:#0b2e6b; color:white; padding:8px; width:50%; font-weight:bold;">
                        DÍAS CXC
                    </div>
                    <div style="background:#0b2e6b; color:white; padding:8px; width:50%; font-weight:bold;">
                        DÍAS CXP
                    </div>
                </div>

                <div style="display:flex;">
                    <div style="border:1px solid black; width:50%; text-align:center; padding:8px;">
                        {dias_cxc:,.0f}
                    </div>
                    <div style="border:1px solid black; width:50%; text-align:center; padding:8px;">
                        {dias_cxp:,.0f}
                    </div>
                </div>

            </div>
            """

            components.html(html, height=450)



















































































































































































































































































































