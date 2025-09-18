import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from streamlit_option_menu import option_menu
import io
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import plotly.express as px
from plotly import graph_objects as go
import numpy as np
from st_aggrid.shared import JsCode

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

categorias_felx_com = ['COSTO DE PERSONAL', 'GASTO DE PERSONAL', 'NOMINA ADMINISTRATIVOS']
da = ['AMORT ARRENDAMIENTO', 'AMORTIZACION', 'DEPRECIACION']
meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

@st.cache_data
def cargar_datos(url):
    response = requests.get(url)
    response.raise_for_status()
    archivo_excel = BytesIO(response.content)
    return pd.read_excel(archivo_excel, engine="openpyxl")

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
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

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

    ingreso_fin = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']

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

    # Caso especial: si solo tiene acceso a "ESGARI"
    if st.session_state["cecos"] == ["ESGARI"]:
        opciones = ["ESGARI"] + cecos["nombre"].tolist()
        ceco_nombre = col.selectbox("Selecciona un ceco", opciones)

        if ceco_nombre == "ESGARI":
            ceco_codigo = cecos["ceco"].tolist()  # Accede a todos

        else:
            # Buscar código del nombre elegido
            ceco_codigo = cecos[cecos["nombre"] == ceco_nombre]["ceco"].values.tolist()
    else:
        # Normal: mostrar solo nombres permitidos
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
            user, rol, proyectos, cecos = validar_credenciales(df_usuarios, username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user
                st.session_state["rol"] = rol
                st.session_state["proyectos"] = proyectos
                st.session_state["cecos"] = cecos
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
    # Ya ha iniciado sesión
    st.sidebar.success(f"👤 Usuario: {st.session_state['username']}")

    if st.sidebar.button("Cerrar sesión"):
        for key in ["logged_in", "username", "rol", "proyectos"]:
            st.session_state[key] = "" if key != "logged_in" else False
        st.rerun()
    if st.session_state['rol'] == "admin":
        if st.sidebar.button("🔄 Recargar datos"):
            st.cache_data.clear()
            st.rerun()
    if st.session_state["username"] == "gonza" or st.session_state["username"] == "Octavio" or st.session_state["username"] == "Karla" or st.session_state["username"] == "Roman":
        link_360 = "https://drive.google.com/file/d/1ZQkWXHE9sakW9NL7eUfz8gOh8dg1L5w2/view?usp=sharing"
        def get_direct_link(shareable_link):
            # Extraer el ID del enlace compartido
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
        # Mostrar botones de descarga para cada archivo
        def create_download_buttons():
            # Diccionario de enlaces con nombres de archivos
            files = {
                "Excel P&L 360.xlsm": excel_360,
            }

            for file_name, file_url in files.items():
                # Descargar el archivo desde el enlace de Google Drive
            
                file_data = download_file_from_drive(file_url)
                
                # Mostrar el botón de descarga
                if file_data:
                    st.sidebar.download_button(
                        label=f"Descargar {file_name}",
                        data=file_data,
                        file_name=file_name,
                        mime="application/vnd.ms-excel.sheet.macroEnabled.12",  # MIME type para .xlsm
                    )


        # Crear los botones de descarga
        create_download_buttons()

    ct("ESGARI 360")
    fecha_act = fecha_actualizacion['fecha'].iloc[0]
    meses = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    fecha_texto = f"{fecha_act.day} de {meses[fecha_act.month]} de {fecha_act.year}"
    texto_centrado(f"Fecha de actualización: {fecha_texto}")
    
    if st.session_state["rol"] in ["director", "admin"] and "ESGARI" in st.session_state["proyectos"]:
        selected = option_menu(
        menu_title=None,
        options=["Resumen", "Estado de Resultado", "Comparativa", "Análisis", "Proyeccion", "LY", "PPT", "Meses", "Mes Corregido",
                 "CeCo", "Ratios", "Dashboard", "Benchmark", "Simulador", "Gastos por Empresa", "Comercial"],
        icons = [
                "house",                # Resumen
                "clipboard-data",       # Estado de Resultado
                "file-earmark-bar-graph",# Comparativa
                "bar-chart",            # Análisis
                "building",             # Proyeccion
                "clock-history",        # LY
                "easel",                # PPT
                "calendar",             # Meses
                "graph-up",             # Mes Corregido
                "person-gear",          # CeCo -> "Centro de Costos"
                "percent",              # Ratios
                "speedometer" ,         # Dashboard
                "trophy",
                "sliders",
                "dollar",
            ],
        default_index=0,
        orientation="horizontal",)
    elif st.session_state["rol"] == "director" or st.session_state["rol"] == "admin":
        selected = option_menu(
        menu_title=None,
        options=["Estado de Resultado", "Comparativa", "Análisis", "Proyeccion", "LY", "PPT", "Meses", "Mes Corregido", "CeCo", "Ratios", "Comercial"],
        icons=["clipboard-data", "file-earmark-bar-graph", "bar-chart", "building", "clock-history", "easel", "calendar", "graph-up", "person-gear", "percent"],
        default_index=0,
        orientation="horizontal",)
    elif st.session_state["rol"] == "gerente":
        selected = option_menu(
        menu_title=None,
        options=["Estado de Resultado", "Comparativa", "Análisis", "Proyeccion", "LY", "PPT", "Meses", "Mes Corregido", "CeCo", "Comercial"],
        icons=["clipboard-data", "file-earmark-bar-graph", "bar-chart", "building", "clock-history", "easel", "graph-up", "person-gear"],
        default_index=0,
        orientation="horizontal",)
    elif st.session_state["rol"] == "ceco":
        selected = option_menu(
        menu_title=None,
        options=[ "CeCo"],
        icons=["person-gear"],
        default_index=0,
        orientation="horizontal",)
    elif st.session_state["rol"] == "comercial":
        selected = option_menu(
        menu_title=None,
        options=[ "Comercial"],
        icons=["bar-chart"],
        default_index=0,
        orientation="horizontal",)   



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
        meses_disponibles = [mes for mes in meses_ordenados if mes in df_2025["Mes_A"].unique()]
        mes_ant = meses_disponibles[-2] if meses_disponibles else None
        mes_act = meses_disponibles[-1] if meses_disponibles else None
        df_mes = df_2025[df_2025["Mes_A"] == mes_act]
        mes = filtro_meses(col1, df_mes)
        codigo_pro, pro = filtro_pro(col2)
        fecha_act = fecha_actualizacion['fecha'].iloc[0].day
        fecha_completa = fecha_actualizacion['fecha'].iloc[0]
        ultimo_dia_mes = (fecha_completa + pd.offsets.MonthEnd(0)).day
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
            ingreso_sem = "https://docs.google.com/spreadsheets/d/14l6QLudSBpqxmfuwRqVxCXzhSFzRL0AqWJqVuIOaFFQ/export?format=xlsx"
            df = cargar_datos(ingreso_sem)
            df["mes"] = pd.to_datetime(df["fecha"]).dt.day
            indice_mas_cercano = (df['mes'] - fecha_act).abs().idxmin()
            valor_mas_cercano = df.loc[indice_mas_cercano, 'mes']

            df_va = df[df['mes'] == valor_mas_cercano]
            df_va["ingreso"] = df_va["ingreso"] / valor_mas_cercano * fecha_act
            df_va = df_va.drop(columns=["mes", "semana", "fecha"])
            df_fin = df[df["semana"] == 4]
            df_fin = df_fin.drop(columns=["mes", "semana", "fecha"])

            # Hacer merge por la columna 'proyecto'
            df_merged = pd.merge(df_va, df_fin, on="proyecto", suffixes=("_va", "_fin"))

            # Crear columna con la división de ingresos
            df_merged["ingreso_dividido"] = df_merged["ingreso_va"] / df_merged["ingreso_fin"]

            df_proyeccion = df_2025[df_2025["Mes_A"] == mes_act]
            df_proyeccion = df_proyeccion.groupby([
                    "Proyecto_A", "Categoria_A"
                ], as_index=False)["Neto_A"].sum()
            df_proyeccion = df_proyeccion[df_proyeccion["Categoria_A"] == "INGRESO"]
            df_proyeccion = df_proyeccion.drop(columns=["Categoria_A"])
            df_proyeccion["Proyecto_A"] = df_proyeccion["Proyecto_A"].astype(float)
            df_proyeccion = pd.merge(df_proyeccion, df_merged, left_on="Proyecto_A", right_on="proyecto", how="left")
            df_proyeccion["Neto_A"] = df_proyeccion["Neto_A"] / df_proyeccion["ingreso_dividido"]
            df_proyeccion = df_proyeccion.drop(columns=["proyecto", "ingreso_va", "ingreso_fin", "ingreso_dividido"])
            df_proyeccion["Proyecto_A"] = df_proyeccion["Proyecto_A"].astype(float).astype(int).astype(str)
            ingreso_pro_fut = df_proyeccion[df_proyeccion["Proyecto_A"].isin(codigo_pro)]["Neto_A"].sum()

        if promedio_fijo == "LM":
            
            df_ext = df_2025[df_2025["Mes_A"] == mes_ant]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            if pro != "ESGARI":
                df_ext = df_ext[df_ext["Proyecto_A"].isin(codigo_pro)]
            df_ext = df_ext[~df_ext["Proyecto_A"].isin(["8002", "8003", "8004"])]
            df_ext["Mes_A"] = mes_act
            df_ext["Neto_A"] = df_ext["Neto_A"]
            df_sum = df_ext
            patio_pro = patio(df_2025, [mes_ant], codigo_pro, pro)
            oh_pro = oh(df_2025, [mes_ant], codigo_pro, pro)
         
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
                meses_sel = [mes_ant] if mes_ant else []
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

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
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
            df_ext_var = df_2025[df_2025["Mes_A"] == mes_ant]
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

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
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

            ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
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

                ingreso_fin_cue = ['INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
                intereses = df_junto[df_junto["Clasificacion_A"] == "GASTOS FINANCIEROS"]["Neto_A"].sum() - df_junto[df_junto["Categoria_A"].isin(ingreso_fin_cue)]["Neto_A"].sum()

                if modo_oh_master == "Calcular como % de ingresos":
                    oh_pct_elegido = oh_pct_elegido  # ya estaba definido arriba
                else:
                    oh_pct_elegido = None

                proyecciones(ingreso_pro_fut, df_ext_var, df_sum, oh_pro, intereses, patio_pro, coss_pro, gadmn_pro, oh_pct_elegido)


            else:
                st.warning("No hay suficientes meses anteriores para calcular el promedio de 3 meses.")  

    
    
    
    elif selected == "LY":
        st.write("Bienvenido a la sección de LY. Aquí puedes ver los datos del año anterior.")
        estdo_re(df_ly, ceco = "2")


    elif selected == "PPT":
        st.write("Bienvenido a la sección de PPT. Aquí puedes ver el presupuesto!")
        estdo_re(df_ppt, ceco = "3")
    
    
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

            import plotly.express as px

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
                "📉 Composición de Gastos",
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


            # --- TAB 2: Composición de Gastos ---
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

                from plotly.subplots import make_subplots
                import plotly.graph_objects as go
                
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


    elif selected == "Mes Corregido":
        texto_centrado("Aqui puedes ver como se veria el mes si tuviera los gastos fijos cargados adecuadamente")

        costos_variables = ["FLETES", "CASETAS", "COMBUSTIBLE", "OTROS COSS", "INGRESO"]
        promedio_fijo = st.selectbox("Seleciona que promedio usar para los gastos fijos", ["LM", "YTD", "TRES MESES"])
        fecha_act = fecha_actualizacion['fecha'].iloc[0].day
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        meses_disponibles = [mes for mes in meses_ordenados if mes in df_2025["Mes_A"].unique()]
        mes_ant = meses_disponibles[-2] if meses_disponibles else None
        mes_act = meses_disponibles[-1] if meses_disponibles else None


        if promedio_fijo == "LM":
            
            df_ext = df_2025[df_2025["Mes_A"] == mes_ant]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            df_ext["Mes_A"] = mes_act
            df_ext["Neto_A"] = df_ext["Neto_A"] / 30.4 * fecha_act
            df_varia = df_2025[df_2025["Mes_A"] == mes_act]
            
            df_varia = df_varia[df_varia["Categoria_A"].isin(costos_variables)]
            df_corregido = pd.concat([df_ext, df_varia], ignore_index=True)
            
            estdo_re(df_corregido, ceco = "4")
            
        elif promedio_fijo == "YTD":

            df_ext = df_2025[df_2025["Mes_A"] != mes_act]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]
            numero_meses = df_ext['Mes_A'].nunique()

            columns = ['Empresa_A', 'CeCo_A', 'Proyecto_A', 'Cuenta_A', 
                    'Clasificacion_A', 'Cuenta_Nombre_A', 'Categoria_A']

            # Paso 1: Agrupamos incluyendo 'Mes_A' y sumamos 'Neto_A'
            df_sum = df_ext.groupby(columns, as_index=False)['Neto_A'].sum()

            df_sum['Neto_A'] = df_sum['Neto_A']/numero_meses
            df_sum["Mes_A"] = mes_act
            df_sum["Neto_A"] = df_sum["Neto_A"] / 30.4 * fecha_act
            df_varia = df_2025[df_2025["Mes_A"] == mes_act]
            
            df_varia = df_varia[df_varia["Categoria_A"].isin(costos_variables)]
            df_corregido = pd.concat([df_sum, df_varia], ignore_index=True)
            
            estdo_re(df_corregido, ceco = "5")
    
        elif promedio_fijo == "TRES MESES":

            # Identificamos los 3 meses anteriores al mes actual
            idx_mes_act = meses_ordenados.index(mes_act)
            meses_previos = meses_ordenados[max(0, idx_mes_act - 3):idx_mes_act]

            # Filtramos gastos fijos (no variables) de los 3 meses anteriores
            df_ext = df_2025[df_2025["Mes_A"].isin(meses_previos)]
            df_ext = df_ext[~(df_ext["Categoria_A"].isin(costos_variables))]

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
                df_sum["Neto_A"] = df_sum["Neto_A"] / 30.4 * fecha_act

                # Obtenemos los gastos variables reales del mes actual
                df_varia = df_2025[df_2025["Mes_A"] == mes_act]
                df_varia = df_varia[df_varia["Categoria_A"].isin(costos_variables)]

                # Combinamos fijos simulados y variables reales
                df_corregido = pd.concat([df_sum, df_varia], ignore_index=True)
                estdo_re(df_corregido, ceco = "6")
            else:
                st.warning("No hay suficientes meses anteriores para calcular el promedio de 3 meses.")

    elif selected == "CeCo":
        import altair as alt
        texto_centrado("GASTOS POR CECO")

        col1, col2 = st.columns(2)
        ceco_codigo, ceco_nombre = filtro_ceco(col1)

        df_cecos = df_2025.copy()
        df_cecos["CeCo_A"] = df_cecos["CeCo_A"].astype(str)
        df_cecos = df_cecos[df_cecos["CeCo_A"].isin(ceco_codigo)]
        df_cecos_ly = df_ly.copy()
        df_cecos_ly["CeCo_A"] = df_cecos_ly["CeCo_A"].astype(str)
        df_cecos_ly = df_cecos_ly[df_cecos_ly["CeCo_A"].isin(ceco_codigo)]
        df_cecos_ppt = df_ppt.copy()
        df_cecos_ppt["CeCo_A"] = df_cecos_ppt["CeCo_A"].astype(str)
        df_cecos_ppt = df_cecos_ppt[df_cecos_ppt["CeCo_A"].isin(ceco_codigo)]

        def tabla_expandible_comp(df, df_ly, df_ppt, cat, mes, ceco, key_prefix):
            columnas = ['Cuenta_Nombre_A', 'Categoria_A']
            ingreso_fin = [
                'INGRESO POR REVALUACION CAMBIARIA', 'INGRESO POR INTERESES', 
                'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE'
            ]
            # Filtrar según categoría
            if cat == 'INGRESO':
                df_tab = df[df['Categoria_A'] == cat]
                df_tab_ly = df_ly[df_ly['Categoria_A'] == cat]
                df_tab_ppt = df_ppt[df_ppt['Categoria_A'] == cat]
            elif cat == 'INGRESO FINANCIERO':
                df_tab = df[df['Categoria_A'].isin(ingreso_fin)]
                df_tab_ly = df_ly[df_ly['Categoria_A'].isin(ingreso_fin)]
                df_tab_ppt = df_ppt[df_ppt['Categoria_A'].isin(ingreso_fin)]
            else:
                df_tab = df[df['Clasificacion_A'] == cat]
                df_tab_ly = df_ly[df_ly['Clasificacion_A'] == cat]
                df_tab_ppt = df_ppt[df_ppt['Clasificacion_A'] == cat]

            df_tab = df_tab[df_tab['Mes_A'].isin(mes)].groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            df_tab_ly = df_tab_ly[df_tab_ly['Mes_A'].isin(mes)].groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            df_tab_ppt = df_tab_ppt[df_tab_ppt['Mes_A'].isin(mes)].groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

            df_comb = pd.merge(df_tab, df_tab_ly, on=columnas, how='outer', suffixes=('','_ly'))
            df_comb = pd.merge(df_comb, df_tab_ppt, on=columnas, how='outer', suffixes=('','_ppt'))

            df_comb['YTD'] = df_comb['Neto_A'].fillna(0)
            df_comb['LY'] = df_comb['Neto_A_ly'].fillna(0)
            df_comb['PPT'] = df_comb['Neto_A_ppt'].fillna(0)

            df_comb["Alcance_LY"] = df_comb.apply(lambda r: (r["YTD"]/r["LY"]*100-100) if r["LY"] else 0, axis=1)
            df_comb["Alcance_PPT"] = df_comb.apply(lambda r: (r["YTD"]/r["PPT"]*100-100) if r["PPT"] else 0, axis=1)

            df_comb_or = df_comb.fillna("").reset_index(drop=True)

            # AgGrid con formato USD
            js_fmt = JsCode("""
            function(params) {
                if (isNaN(params.value)) return '';
                return params.value.toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2
                });
            }
            """)
            df_comb_or = df_comb_or.drop(columns=["Neto_A", "Neto_A_ly", "Neto_A_ppt"], errors='ignore')
            gb = GridOptionsBuilder.from_dataframe(df_comb_or)
            gb.configure_default_column(groupable=True)
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)
            for c in ["YTD", "LY", "PPT"]:
                gb.configure_column(c, type=["numericColumn"], aggFunc="last", valueFormatter=js_fmt)
            gb.configure_column("Alcance_LY", aggFunc="last", valueFormatter="`${value.toFixed(2)}%`")
            gb.configure_column("Alcance_PPT", aggFunc="last", valueFormatter="`${value.toFixed(2)}%`")
            # Calcular fila total por categoria (sin Cuenta_Nombre_A)
            total_cat = df_comb.groupby("Categoria_A", as_index=False).agg({
                "YTD": "sum",
                "LY": "sum",
                "PPT": "sum"
            })
            total_cat["Cuenta_Nombre_A"] = ""  # vacío para que suba al final
            total_cat["Alcance_LY"] = total_cat.apply(
                lambda r: (r["YTD"] / r["LY"] * 100 - 100) if r["LY"] else 0, axis=1
            )
            total_cat["Alcance_PPT"] = total_cat.apply(
                lambda r: (r["YTD"] / r["PPT"] * 100 - 100) if r["PPT"] else 0, axis=1
            )

            # Unir al dataframe original
            df_comb_or = pd.concat([df_comb_or, total_cat], ignore_index=True, sort=False)
            AgGrid(df_comb_or, gridOptions=gb.build(), enable_enterprise_modules=True,
                allow_unsafe_jscode=True, theme="streamlit", height=400,
                key=f"{key_prefix}_{cat}_{ceco}_{mes}")

            df_sin_total = df_comb_or[df_comb_or["Cuenta_Nombre_A"] != ""]

            resumen = {
                "cat": cat,
                "YTD": df_sin_total["YTD"].sum(),
                "LY": df_sin_total["LY"].sum(),
                "PPT": df_sin_total["PPT"].sum()
            }
            
            df_chart = pd.DataFrame([{"Tipo": t, "Valor": resumen[t]} for t in ["YTD","LY","PPT"]])
            st.altair_chart(
                alt.Chart(df_chart).mark_bar().encode(x="Tipo", y="Valor", color="Tipo")
                                .properties(title=f"{cat}: Totales"),
                use_container_width=True
            )
            return resumen

        # --- Selección de meses ---
        meses = filtro_meses(col2, df_cecos)

        # --- Pestañas ---
        resumenes = {}
        ventanas = ['INGRESO','COSS','G.ADMN','GASTOS FINANCIEROS','INGRESO FINANCIERO']
        tabs = st.tabs(ventanas)
        for i, cat in enumerate(ventanas):
            with tabs[i]:
                resumenes[cat] = tabla_expandible_comp(df_cecos, df_cecos_ly, df_cecos_ppt, cat, meses, ceco_codigo, cat)

        # --- Resumen global ---
        ing = resumenes["INGRESO"]
        diff_ing = ing["YTD"] - ing["LY"]
        otros = ['COSS','G.ADMN','GASTOS FINANCIEROS','INGRESO FINANCIERO']
        ytd_otros = sum(resumenes[c]["YTD"] for c in otros)
        ly_otros = sum(resumenes[c]["LY"] for c in otros)
        diff_otros = ytd_otros - ly_otros
        diff_ing_ppt = ing["YTD"] - ing["PPT"]
        ppt_otros = ytd_otros - sum(resumenes[c]["PPT"] for c in otros)


        st.subheader("📌 Totales Globales")
        c1, c2 = st.columns(2)
        c1.metric("💰 INGRESO (YTD−LY)", f"${diff_ing:,.2f}",
                delta=f"{(diff_ing/ing['LY']*100) if ing['LY'] else 0:.2f}%")
        c2.metric("📉 OTROS GASTOS (YTD−LY)", f"${diff_otros:,.2f}",
                delta=f"{(diff_otros/ly_otros*100) if ly_otros else 0:.2f}%")
        c1.metric("💰 INGRESO (YTD−PPT)", f"${diff_ing_ppt:,.2f}",
                delta=f"{(diff_ing_ppt/ing['PPT']*100) if ing['PPT'] else 0:.2f}%")
        c2.metric("📉 OTROS GASTOS (YTD−PPT)", f"${ppt_otros:,.2f}",
                delta=f"{(ppt_otros/resumenes['COSS']['PPT']*100) if resumenes['COSS']['PPT'] else 0:.2f}%")

        df_global = pd.DataFrame([
            {"Categoria":"INGRESO","Tipo":"YTD","Valor":ing["YTD"]},
            {"Categoria":"INGRESO","Tipo":"LY","Valor":ing["LY"]},
            {"Categoria":"OTROS","Tipo":"YTD","Valor":ytd_otros},
            {"Categoria":"OTROS","Tipo":"LY","Valor":ly_otros},
            {"Categoria":"INGRESO","Tipo":"PPT","Valor":ing["PPT"]},
            {"Categoria":"OTROS","Tipo":"PPT","Valor":ytd_otros - sum(resumenes[c]["PPT"] for c in otros)}
        ])
        st.altair_chart(
            alt.Chart(df_global).mark_bar().encode(x="Categoria:N", y="Valor:Q", color="Tipo:N")
                            .properties(title="Comparativo Global YTD vs LY"),
            use_container_width=True
    )

    elif selected == "Ratios":
        st.title("📊 Análisis de Ratios Personalizados")

        def filtro_pro_ratios(col):
            df_visibles = proyectos[proyectos["proyectos"].astype(str).isin(st.session_state["proyectos"])]
            nombre_a_codigo = dict(zip(df_visibles["nombre"], df_visibles["proyectos"].astype(str)))
            proyectos_dict = {}

            if st.session_state["proyectos"] == ["ESGARI"]:
                opciones = ["ESGARI"] + proyectos["nombre"].tolist()
                seleccionados = col.multiselect("Selecciona proyecto(s)", opciones, default=["ESGARI"])
                if "ESGARI" in seleccionados:
                    codigos_todos = proyectos["proyectos"].astype(str).tolist()
                    proyectos_dict["ESGARI"] = codigos_todos
                seleccion_otros = [s for s in seleccionados if s != "ESGARI"]
                for nombre in seleccion_otros:
                    codigo = proyectos[proyectos["nombre"] == nombre]["proyectos"].astype(str).iloc[0]
                    proyectos_dict[nombre] = codigo
            else:
                seleccionados = col.multiselect("Selecciona proyecto(s)", list(nombre_a_codigo.keys()))
                for nombre in seleccionados:
                    proyectos_dict[nombre] = nombre_a_codigo[nombre]
            return proyectos_dict

        dic_proyectos = filtro_pro_ratios(st)

        lista_proyectos_local = []
        for _nombre, _cod in dic_proyectos.items():
            if isinstance(_cod, list):
                lista_proyectos_local.extend(_cod)
            else:
                lista_proyectos_local.append(_cod)

        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.",
                        "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
        meses_disponibles = [m for m in meses_ordenados if m in df_2025["Mes_A"].unique()]
        meses_sel = st.multiselect("Selecciona meses a analizar", meses_disponibles, default=meses_disponibles)

        num_ratios = st.number_input("¿Cuántos ratios deseas analizar?", min_value=1, max_value=5, value=1, step=1)

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

        ratio_config = []
        for i in range(num_ratios):
            with st.expander(f"⚙️ Configuración del Ratio {i+1}", expanded=(i == 0)):
                nombre = st.text_input(f"Nombre del Ratio {i+1}", value=f"Ratio {i+1}", key=f"ratio_name_{i}")
                col1, col2 = st.columns(2)

                # Numerador
                tipo_num = col1.selectbox("Campo Numerador", list(campo_map.keys()), key=f"tipo_num_{i}")
                if campo_map[tipo_num] == "ER":
                    valor_num = col1.selectbox("Valor Numerador", er_labels, key=f"val_num_{i}")
                    num_extra = None
                else:
                    valor_num = col1.selectbox(
                        "Valor Numerador",
                        sorted(df_2025[campo_map[tipo_num]].dropna().unique()),
                        key=f"val_num_{i}"
                    )
                    add_extra_num = col1.checkbox("➕ Agregar otro valor al numerador", key=f"extra_num_check_{i}")
                    if add_extra_num:
                        tipo_num_2 = col1.selectbox("Campo adicional Numerador", list(campo_map.keys()), key=f"tipo_num_2_{i}")
                        valor_num_2 = col1.selectbox(
                            "Valor adicional Numerador",
                            sorted(df_2025[campo_map[tipo_num_2]].dropna().unique()),
                            key=f"val_num_2_{i}"
                        )
                        num_extra = {
                            "campo": campo_map[tipo_num_2],
                            "valor": valor_num_2
                        }
                    else:
                        num_extra = None

                # Denominador
                tipo_den = col2.selectbox("Campo Denominador", list(campo_map.keys()), key=f"tipo_den_{i}")
                if campo_map[tipo_den] == "ER":
                    valor_den = col2.selectbox("Valor Denominador", er_labels, key=f"val_den_{i}")
                    den_extra = None
                else:
                    valor_den = col2.selectbox(
                        "Valor Denominador",
                        sorted(df_2025[campo_map[tipo_den]].dropna().unique()),
                        key=f"val_den_{i}"
                    )
                    add_extra_den = col2.checkbox("➕ Agregar otro valor al denominador", key=f"extra_den_check_{i}")
                    if add_extra_den:
                        tipo_den_2 = col2.selectbox("Campo adicional Denominador", list(campo_map.keys()), key=f"tipo_den_2_{i}")
                        valor_den_2 = col2.selectbox(
                            "Valor adicional Denominador",
                            sorted(df_2025[campo_map[tipo_den_2]].dropna().unique()),
                            key=f"val_den_2_{i}"
                        )
                        den_extra = {
                            "campo": campo_map[tipo_den_2],
                            "valor": valor_den_2
                        }
                    else:
                        den_extra = None

                ratio_config.append({
                    "nombre": nombre,
                    "campo_num": campo_map[tipo_num],
                    "valor_num": valor_num,
                    "extra_num": num_extra,
                    "campo_den": campo_map[tipo_den],
                    "valor_den": valor_den,
                    "extra_den": den_extra
                })

        resultados = []
        for proyecto, codigos in dic_proyectos.items():
            if not isinstance(codigos, list):
                codigos = [codigos]
            for mes in meses_sel:
                df_mes = df_2025[(df_2025["Mes_A"] == mes) & (df_2025["Proyecto_A"].isin(codigos))]

                necesita_er = any(cfg["campo_num"] == "ER" or cfg["campo_den"] == "ER" for cfg in ratio_config)
                er_vals = {}
                if necesita_er:
                    er_vals = estado_resultado(df_2025, [mes], proyecto, codigos, lista_proyectos_local)

                for config in ratio_config:
                    if config["campo_num"] == "ER":
                        num = float(er_vals.get(er_label_to_key[config["valor_num"]], 0))
                    else:
                        num = float(df_mes[df_mes[config["campo_num"]] == config["valor_num"]]["Neto_A"].sum())
                        if config["extra_num"]:
                            num += float(df_mes[df_mes[config["extra_num"]["campo"]] == config["extra_num"]["valor"]]["Neto_A"].sum())

                    if config["campo_den"] == "ER":
                        den = float(er_vals.get(er_label_to_key[config["valor_den"]], 0))
                    else:
                        den = float(df_mes[df_mes[config["campo_den"]] == config["valor_den"]]["Neto_A"].sum())
                        if config["extra_den"]:
                            den += float(df_mes[df_mes[config["extra_den"]["campo"]] == config["extra_den"]["valor"]]["Neto_A"].sum())

                    ratio = num / den if den != 0 else 0
                    resultados.append({
                        "Mes": mes,
                        "Proyecto": proyecto,
                        "Ratio": ratio,
                        "Nombre": config["nombre"]
                    })

        df_result = pd.DataFrame(resultados)
        df_result["Mes"] = pd.Categorical(df_result["Mes"], categories=meses_ordenados, ordered=True)
        df_result = df_result.sort_values(["Nombre", "Proyecto", "Mes"])

        if not df_result.empty:
            st.subheader("📈 Evolución de Ratios")
            fig = px.line(
                df_result,
                x="Mes",
                y="Ratio",
                color="Nombre",
                line_dash="Proyecto",
                markers=True,
                title="Ratios por mes y proyecto"
            )
            fig.update_layout(
                height=500,
                legend_title_text="Ratio",
                xaxis_title="Mes",
                yaxis_title="Valor del ratio"
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Tabla de resultados")
            st.dataframe(df_result, use_container_width=True)
        else:
            st.info("Selecciona al menos un proyecto y mes para calcular ratios.")

    elif selected == "Dashboard":
        st.title("📊 Dashboard Ejecutivo")

        col1, col2 = st.columns(2)
        meses_sel = filtro_meses(col1, df_2025)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)

        if not meses_sel:
            st.warning("Selecciona al menos un mes para continuar.")
        else:
            er = estado_resultado(df_2025, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)
            er_ppt = estado_resultado(df_ppt, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)

            col1, col2, col3 = st.columns(3)
            col1.metric("Ingreso", f"${er['ingreso_proyecto']:,.0f}", f"vs PPT: {((er['ingreso_proyecto']/er_ppt['ingreso_proyecto'])-1)*100:.1f}%")
            col2.metric("Utilidad Operativa", f"${er['utilidad_operativa']:,.0f}", f"{er['por_utilidad_operativa']*100:.1f}%")
            col3.metric("EBT", f"${er['ebt']:,.0f}", f"{er['por_ebt']*100:.1f}%")

            st.subheader("🚨 Alertas Rápidas")
            alertas = []

            if er["por_utilidad_operativa"] < 0.24:
                alertas.append(f"🔴 Margen U. Operativa bajo: {er['por_utilidad_operativa']*100:.1f}% (meta: 24%)")

            if er["por_ebt"] < 0.115:
                alertas.append(f"🟠 Margen EBT bajo: {er['por_ebt']*100:.1f}% (meta: 11.5%)")

            if er["ingreso_proyecto"] < er_ppt["ingreso_proyecto"]:
                delta_ing = ((er["ingreso_proyecto"]/er_ppt["ingreso_proyecto"]) - 1) * 100
                alertas.append(f"🟠 Ingreso por debajo del presupuesto: {delta_ing:.1f}%")

            if not alertas:
                st.success("✅ Sin alertas críticas este periodo")
            else:
                for a in alertas:
                    st.warning(a)

            st.subheader("Composición de los gastos")

            fig = go.Figure(data=[
                go.Pie(
                    labels=["COSS", "G.ADMN", "Gastos Financieros"],
                    values=[
                        er['coss_total'],
                        er['gadmn_pro'],
                        er['gasto_fin_pro']
                    ],
                    hole=0.4,
                    textinfo="label+percent"
                )
            ])
            
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📉 Tendencias vs LY y Presupuesto")

        # Comparativos adicionales
        er_ly = estado_resultado(df_ly, meses_sel, proyecto_nombre, proyecto_codigo, list_pro)

        def trend_card(label, actual, ly, ppt):
            col1, col2, col3 = st.columns(3)
            col1.metric(label, f"${actual:,.0f}")
            col2.metric("vs LY", f"${actual - ly:,.0f}", f"{((actual / ly) - 1) * 100:.1f}%" if ly != 0 else "N/A")
            col3.metric("vs PPT", f"${actual - ppt:,.0f}", f"{((actual / ppt) - 1) * 100:.1f}%" if ppt != 0 else "N/A")

        trend_card("Ingreso", er["ingreso_proyecto"], er_ly["ingreso_proyecto"], er_ppt["ingreso_proyecto"])
        trend_card("COSS", er["coss_total"], er_ly["coss_total"], er_ppt["coss_total"])
        trend_card("G.ADMN", er["gadmn_pro"], er_ly["gadmn_pro"], er_ppt["gadmn_pro"])
        trend_card("Gasto Financiero", er["gasto_fin_pro"], er_ly["gasto_fin_pro"], er_ppt["gasto_fin_pro"])

    elif selected == "Benchmark":
        st.title("🏆 Benchmark entre Proyectos")

        col1, col2 = st.columns(2)
        meses_sel = filtro_meses(col1, df_2025)

        if not meses_sel:
            st.warning("Selecciona al menos un mes.")
        else:
            # === Diccionario de nombres legibles de proyectos
            nombre_dict = dict(zip(proyectos["proyectos"].astype(str), proyectos["nombre"]))

            # === Excluir proyectos auxiliares
            excluidos = ["8002", "8003", "8004"]
            proyectos_validos = [
                p for p in df_2025["Proyecto_A"].unique()
                if p not in excluidos and p in nombre_dict
            ]

            resultados = []

            for proyecto in proyectos_validos:
                nombre = nombre_dict[proyecto]
                codigo = [proyecto]

                # === KPI base
                ingreso_val = ingreso(df_2025, meses_sel, codigo, nombre)
                patio_val = patio(df_2025, meses_sel, codigo, nombre)
                oh_val = oh(df_2025, meses_sel, codigo, nombre)

                gasto_fin_val, _, _ = gasto_fin(df_2025, meses_sel, codigo, nombre, list_pro)
                ingreso_fin_val, _, _ = ingreso_fin(df_2025, meses_sel, codigo, nombre, list_pro)
                intereses = gasto_fin_val - ingreso_fin_val

                df_proj = df_2025[
                    (df_2025["Mes_A"].isin(meses_sel)) &
                    (df_2025["Proyecto_A"] == proyecto)
                ]

                coss_val = df_proj[df_proj["Clasificacion_A"] == "COSS"]["Neto_A"].sum()
                gadmn_val = df_proj[df_proj["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

                uo_val = ingreso_val - coss_val - gadmn_val - patio_val
                ebit_val = uo_val - oh_val
                ebt_val = ebit_val - intereses

                resultados.append({
                    "Proyecto": nombre,
                    "Ingreso": ingreso_val,
                    "EBT": ebt_val,
                    "Utilidad Operativa": uo_val,
                    "Margen EBT (%)": ebt_val / ingreso_val if ingreso_val else 0,
                    "Margen UO (%)": uo_val / ingreso_val if ingreso_val else 0,
                    "% G.ADMN": gadmn_val / ingreso_val if ingreso_val else 0,
                    "% COSS": coss_val / ingreso_val if ingreso_val else 0,
                    "OH": oh_val,
                    "Intereses": intereses,
                    "PATIO": patio_val
                })

            df_benchmark = pd.DataFrame(resultados)

            # === Orden por KPI
            kpi_orden = col2.selectbox("📌 Ordenar por KPI", [
                "EBT", "Margen EBT (%)", "Margen UO (%)", "% G.ADMN", "% COSS", "Utilidad Operativa"
            ])

            df_benchmark = df_benchmark.sort_values(
                by=kpi_orden,
                ascending=(kpi_orden in ["% G.ADMN", "% COSS"])
            )

            # === Formato visual
            df_viz = df_benchmark.copy()
            df_viz["EBT"] = df_viz["EBT"].map("${:,.0f}".format)
            df_viz["Ingreso"] = df_viz["Ingreso"].map("${:,.0f}".format)
            df_viz["Utilidad Operativa"] = df_viz["Utilidad Operativa"].map("${:,.0f}".format)
            df_viz["OH"] = df_viz["OH"].map("${:,.0f}".format)
            df_viz["Intereses"] = df_viz["Intereses"].map("${:,.0f}".format)
            df_viz["PATIO"] = df_viz["PATIO"].map("${:,.0f}".format)

            for col in ["Margen EBT (%)", "Margen UO (%)", "% G.ADMN", "% COSS"]:
                df_viz[col] = df_viz[col].map("{:.2%}".format)

            st.subheader("📊 Tabla de Benchmark")
            st.dataframe(df_viz, use_container_width=True)

            st.subheader(f"📈 Gráfico de {kpi_orden}")

            df_plot = df_benchmark[["Proyecto", kpi_orden]].copy()
            is_percent = "%" in kpi_orden

            fig = px.bar(
                df_plot,
                x="Proyecto",
                y=kpi_orden,
                text=df_plot[kpi_orden].map(lambda x: f"{x:.2%}" if is_percent else f"${x:,.0f}")
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_tickformat=".0%" if is_percent else None,
                yaxis_title=kpi_orden,
                xaxis_title="Proyecto",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)


    elif selected == "Simulador":
        st.title("🧪 Simulador de Decisiones")

        col1, col2 = st.columns(2)
        meses_seleccionado = filtro_meses(col1, df_2025)
        proyecto_codigo, proyecto_nombre = filtro_pro(col2)

        if not meses_seleccionado:
            st.warning("Selecciona uno o más meses.")
        else:
            # 1. Calcular PATIO, OH, INTERESES del df completo
            patio_pro = patio(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre)
            oh_pro = oh(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre)
            gasto_fin_pro, _, _ = gasto_fin(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, list_pro)
            ingreso_fin_pro, _, _ = ingreso_fin(df_2025, meses_seleccionado, proyecto_codigo, proyecto_nombre, list_pro)
            intereses_base = gasto_fin_pro - ingreso_fin_pro

            # 2. Filtrar gastos excluyendo proyectos auxiliares
            excluidos = ["8002", "8003", "8004"]
            if proyecto_nombre == "ESGARI":
                df_filtrado = df_2025[
                    (df_2025["Mes_A"].isin(meses_seleccionado)) &
                    (~df_2025["Proyecto_A"].isin(excluidos))
                ]
            else:
                df_filtrado = df_2025[
                    (df_2025["Mes_A"].isin(meses_seleccionado)) &
                    (df_2025["Proyecto_A"].isin(proyecto_codigo)) &
                    (~df_2025["Proyecto_A"].isin(excluidos))
                ]

            ingreso_base = df_filtrado[df_filtrado["Categoria_A"] == "INGRESO"]["Neto_A"].sum()

            # 3. Variables normalizadas por categoría
            categorias_variables = ["FLETES", "CASETAS", "COMBUSTIBLE", "OTROS COSS"]
            df_ext_var = df_filtrado[df_filtrado["Categoria_A"].isin(categorias_variables)].copy()
            df_ext_var["Neto_normalizado"] = df_ext_var["Neto_A"] / ingreso_base if ingreso_base else 0

            # 4. Gastos fijos
            categorias_excluir = categorias_variables + ["INGRESO"]
            df_sum = df_filtrado[~df_filtrado["Categoria_A"].isin(categorias_excluir)].copy()

            # === Sliders distribuidos horizontalmente
            st.subheader("🎛 Ajustes por categoría")

            col_ing, col_int = st.columns([3, 1])
            ingreso_factor = col_ing.slider("📈 Ingreso", 0.80, 1.20, 1.00, 0.01)
            intereses_factor = col_int.slider("💵 Intereses", 0.50, 1.50, 1.00, 0.05)

            col1, col2, col3, col4 = st.columns(4)
            fletes_factor = col1.slider("🚛 Fletes", 0.5, 1.5, 1.0, 0.05)
            casetas_factor = col2.slider("🛣️ Casetas", 0.5, 1.5, 1.0, 0.05)
            combustible_factor = col3.slider("⛽ Combustible", 0.5, 1.5, 1.0, 0.05)
            otros_factor = col4.slider("📦 Otros COSS", 0.5, 1.5, 1.0, 0.05)

            col5, col6, col7 = st.columns(3)
            gadmn_factor = col5.slider("🏢 G.ADMN", 0.5, 1.5, 1.0, 0.05)
            patio_factor = col6.slider("🏗️ PATIO", 0.5, 1.5, 1.0, 0.05)
            oh_factor = col7.slider("⚙️ OH", 0.5, 1.5, 1.0, 0.05)

            ingreso_esc = ingreso_base * ingreso_factor
            intereses_esc = intereses_base * intereses_factor
            patio_esc = patio_pro * patio_factor
            oh_esc = oh_pro * oh_factor

            # Variables ajustadas individualmente
            ajustes = {
                "FLETES": fletes_factor,
                "CASETAS": casetas_factor,
                "COMBUSTIBLE": combustible_factor,
                "OTROS COSS": otros_factor
            }

            df_ext_var_adj = df_ext_var.copy()
            df_ext_var_adj["Neto_A"] = df_ext_var_adj.apply(
                lambda row: row["Neto_normalizado"] * ingreso_esc * ajustes.get(row["Categoria_A"], 1.0),
                axis=1
            )
            df_ext_var_adj = df_ext_var_adj.drop(columns=["Neto_normalizado"])
            df_sum.loc[df_sum["Clasificacion_A"] == "G.ADMN", "Neto_A"] *= gadmn_factor


            df_junto = pd.concat([df_ext_var_adj, df_sum], ignore_index=True)

            coss_pro = df_junto[df_junto["Clasificacion_A"] == "COSS"]["Neto_A"].sum()
            gadmn_pro = df_junto[df_junto["Clasificacion_A"] == "G.ADMN"]["Neto_A"].sum()

            utilidad_op = ingreso_esc - coss_pro - gadmn_pro - patio_esc
            ebit = utilidad_op - oh_esc
            ebt = ebit - intereses_esc

            df_resultado = pd.DataFrame({
                "Concepto": [
                    "Ingresos Proyectados", "COSS Variables", "PATIO", "Gastos Administrativos",
                    "Utilidad Operativa", "% Utilidad Operativa", "OH", "EBIT",
                    "Intereses", "EBT", "% EBT"
                ],
                "Valor": [
                    f"${ingreso_esc:,.2f}",
                    f"${coss_pro:,.2f}",
                    f"${patio_esc:,.2f}",
                    f"${gadmn_pro:,.2f}",
                    f"${utilidad_op:,.2f}",
                    f"{(utilidad_op / ingreso_esc):.2%}" if ingreso_esc else "N/A",
                    f"${oh_esc:,.2f}",
                    f"${ebit:,.2f}",
                    f"${intereses_esc:,.2f}",
                    f"${ebt:,.2f}",
                    f"{(ebt / ingreso_esc):.2%}" if ingreso_esc else "N/A"
                ]
            })

            mostrar_tabla_estilizada(df_resultado, id=93)

    
    elif selected == "Gastos por Empresa":
        ct("GASTO POR EMPRESA")
        empresas = [0, 10, 20, 30, 40, 50]
        nombre_empresas = [
            'ESGARI',
            'ESGARI HOLDING MEXICO, S.A. DE C.V.',
            'RESA MULTIMODAL, S.A. DE C.V', 
            'UBIKARGA S.A DE C.V', 
            'ESGARI FORWARDING SA DE CV', 
            'ESGARI WAREHOUSING & MANUFACTURING, S DE R.L DE C.V'
        ]
        empresas_dict = dict(zip(nombre_empresas, empresas))
        col1, col2 = st.columns(2)

        def filtro_emp(col):
            emp = col.selectbox('Selecciona la empresa', empresas_dict)
            if emp == 'ESGARI':
                codigo_emp = empresas
            else:
                codigo_emp = [empresas_dict[emp]]
            return emp, codigo_emp

        emp, codigo_emp = filtro_emp(col1)
        meses = filtro_meses(col2, df_2025)

        df_emp = df_2025[
            (df_2025["Mes_A"].isin(meses)) &
            (df_2025["Empresa_A"].isin(codigo_emp)) &
            (~df_2025["Clasificacion_A"].isin(["INGRESO", "IMPUESTOS", "OTROS INGRESOS"]))
        ]

        df_emp = df_emp.groupby(
            ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A", "Mes_A"],
            as_index=False
        )["Neto_A"].sum()

        df_pivot = df_emp.pivot_table(
            index=["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"],
            columns="Mes_A",
            values="Neto_A",
            aggfunc="sum",
            fill_value=0
        ).reset_index()

        # Ordenar columnas de meses cronológicamente
        meses_ordenados = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", 
                        "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]

        # Filtrar solo los meses seleccionados que existen en los datos
        columnas_meses = [m for m in meses_ordenados if m in df_pivot.columns]

        # Reordenar columnas
        df_pivot = df_pivot[["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"] + columnas_meses]

        # Añadir Total y Promedio al final
        df_pivot["Total"] = df_pivot[columnas_meses].sum(axis=1)
        df_pivot["Promedio"] = df_pivot[columnas_meses].mean(axis=1)


        df_pivot["Total"] = df_pivot[meses].sum(axis=1)
        df_pivot["Promedio"] = df_pivot[meses].mean(axis=1)

        gb = GridOptionsBuilder.from_dataframe(df_pivot)
        gb.configure_column("Clasificacion_A", rowGroup=True, hide=True)
        gb.configure_column("Categoria_A", rowGroup=True, hide=True)
        gb.configure_column("Cuenta_Nombre_A", pinned="left")

        formatter = JsCode("""
            function(params) {
                if (params.value === 0 || params.value === null) {
                    return "$0.00";
                }
                return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(params.value);
            }
        """)

        for col in df_pivot.columns:
            if col not in ["Clasificacion_A", "Categoria_A", "Cuenta_Nombre_A"]:
                gb.configure_column(
                    col,
                    type=["numericColumn"],
                    aggFunc="sum",
                    valueFormatter=formatter,
                    cellStyle={'textAlign': 'right'}
                )

        gridOptions = gb.build()
        st.write("### Tabla por Mes con Total y Promedio")
        AgGrid(
            df_pivot,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            domLayout='normal',
            height=600
        )

        # Exportar a Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_pivot.to_excel(writer, index=False, sheet_name="Gastos_por_empresa")
            output.seek(0)

        st.download_button(
            label=f"Descargar tabla",
            data=output,
            file_name=f"gastos_{emp}_{'_'.join(meses)}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"_download_gastos_emp"
        )

    elif selected == "Comercial":
        ct("Ingresos")
        codi_pro, nom_pro = filtro_pro(st)

        # ---------- Función reutilizable de proyección ----------

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
                df_hist = cargar_datos(ingreso_sem_url)
                df_hist["mes"] = pd.to_datetime(df_hist["fecha"]).dt.day
                idx = (df_hist['mes'] - fecha_act).abs().idxmin()
                dia_ref = int(df_hist.loc[idx, 'mes'])

                df_va = df_hist[df_hist['mes'] == dia_ref].copy()
                df_va["ingreso"] = df_va["ingreso"] / max(dia_ref, 1) * fecha_act
                df_va = df_va.drop(columns=["mes", "semana", "fecha"])

                df_fin = df_hist[df_hist["semana"] == 4].copy()
                df_fin = df_fin.drop(columns=["mes", "semana", "fecha"])

                df_merged = pd.merge(df_va, df_fin, on="proyecto", suffixes=("_va", "_fin"))
                df_merged["ingreso_dividido"] = df_merged["ingreso_va"] / df_merged["ingreso_fin"].replace({0: pd.NA})
                df_merged = df_merged.replace([pd.NA, pd.NaT, float("inf"), -float("inf")], 0)

                df_proy = (df_2025[df_2025["Mes_A"] == mes_act]
                        .groupby(["Proyecto_A", "Categoria_A"], as_index=False)["Neto_A"].sum())
                df_proy = df_proy[df_proy["Categoria_A"] == "INGRESO"].drop(columns=["Categoria_A"])

                df_proy["Proyecto_A"] = df_proy["Proyecto_A"].astype(float)
                df_proy = pd.merge(df_proy, df_merged, left_on="Proyecto_A", right_on="proyecto", how="left")
                df_proy["Neto_A"] = df_proy["Neto_A"] / df_proy["ingreso_dividido"].replace({0: pd.NA}).fillna(0)

                df_proy = df_proy.drop(columns=["proyecto", "ingreso_va", "ingreso_fin", "ingreso_dividido"])
                df_proy["Proyecto_A"] = df_proy["Proyecto_A"].astype(float).astype(int).astype(str)

                if pro == "ESGARI":
                    return float(df_proy["Neto_A"].sum())
                cods = codigo_pro if isinstance(codigo_pro, list) else [codigo_pro]
                return float(df_proy[df_proy["Proyecto_A"].isin(cods)]["Neto_A"].sum())

            raise ValueError("modo debe ser 'lineal' o 'historico'")

        # ---------- Helper para ingresos por mes ----------
        def ingre_co(df):
            if nom_pro != "ESGARI":
                df = df[df["Proyecto_A"].isin(codi_pro)]
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
                pro=nom_pro,
                codigo_pro=codi_pro,
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























