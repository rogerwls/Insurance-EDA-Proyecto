import streamlit as st
import pandas as pd
import numpy as np
# Importamos la clase que acabamos de estructurar
import libreria_clases_insurance as cli

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Insurance Renewal EDA",
    page_icon="📊",
    layout="wide"
)

# 2. INICIALIZACIÓN DE SESSION STATE
# Guardamos el DataFrame en memoria para que no se borre al cambiar de módulo
if 'df_insurance' not in st.session_state:
    st.session_state.df_insurance = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None

# 3. MENÚ LATERAL (Navegación Obligatoria)
st.sidebar.title("Navegación Principal")
opcion = st.sidebar.selectbox(
    "Seleccione un Módulo:",
    ["Home", "Carga de Datos", "EDA (Análisis Exploratorio)", "Conclusiones"]
)

# =========================================================
# MÓDULO 1: HOME
# =========================================================
if opcion == "Home":
    st.title("Insurance Renewal EDA – InsuranceCompany")
    st.subheader("Análisis Exploratorio de Renovación de Pólizas de Seguro")
    
    st.markdown("""
    ### 🎯 Objetivo del Proyecto
    Este sistema interactivo tiene como finalidad realizar un **Análisis Exploratorio de Datos (EDA)** profundo 
    sobre el comportamiento de renovación de los clientes de **InsuranceCompany**. A través de este análisis, 
    buscamos identificar patrones de morosidad, perfiles demográficos y canales de captación clave que influyen 
    directamente en el KPI de renovación (*Renewal*).
    """)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 👤 Datos del Autor")
        st.write("- **Estudiante:** Roger Wilfredo Lavado Soto")
        st.write("- **Curso:** Especialización en Python for Analytics")
        st.write("- **Institución:** DMC Institute")
        st.write("- **Año:** 2026")
        
    with col2:
        st.write("### 📊 Contexto del Dataset")
        st.write("""
        El conjunto de datos cuenta con **79,853 registros** y **13 variables** que capturan información financiera 
        crítica de los asegurados, incluyendo puntajes de suscripción (*underwriting score*), primas emitidas, 
        edad en días y, fundamentalmente, el conteo histórico de pagos atrasados segmentados por meses.
        """)
        
    st.divider()
    st.write("### 🛠️ Tecnologías e Interfaz Utilizadas")
    st.markdown("""
    - **Streamlit:** Construcción de módulos dinámicos (`st.sidebar`, `st.tabs`, `st.columns`).
    - **Python & POO:** Encapsulamiento del análisis a través de la clase `DataAnalyzer`.
    - **Pandas & NumPy:** Procesamiento matricial y manipulación de datos estructurados.
    - **Matplotlib & Seaborn:** Motor de visualización estadística bivariada y de distribuciones.
    """)

# =========================================================
# MÓDULO 2: CARGA DEL DATASET
# =========================================================
elif opcion == "Carga de Datos":
    st.title("📂 Módulo 2: Carga y Gestión de Datos")
    st.markdown("""
    En este módulo, el sistema carga el conjunto de datos de `InsuranceCompany`. 
    Se realiza una validación de integridad para asegurar que las variables y 
    dimensiones sean legibles para el análisis posterior.
    """)

    archivo_cargado = st.file_uploader("Seleccione el archivo CSV del caso de estudio:", type=["csv"])

    if archivo_cargado is not None:
        try:
            # Lectura del archivo
            df = pd.read_csv(archivo_cargado)
            
            # Guardamos el DataFrame en el estado de la sesión
            st.session_state.df_insurance = df
            
            # Inicializamos el objeto DataAnalyzer (POO)
            # Esto corrige el error de "atributo no encontrado" porque ahora 
            # el analyzer vive en la sesión correctamente
            from libreria_clases_insurance import DataAnalyzer
            st.session_state.analyzer = DataAnalyzer(df)
            
            st.success("✅ ¡Archivo cargado e inicializado correctamente!")

            # ÍTEM DE MUESTRA DE DATOS
            st.write("### Vista Previa de los Datos")
            st.dataframe(df.head(10), use_container_width=True)

            # ÍTEM DE DIMENSIONES (Aquí usamos el método que corregimos en la librería)
            filas, columnas = st.session_state.analyzer.obtener_dimensiones()
            
            c1, c2 = st.columns(2)
            c1.metric("Total de Registros (Filas)", filas)
            c2.metric("Total de Variables (Columnas)", columnas)

            st.info(f"El dataset está compuesto por {filas} observaciones y {columnas} variables, listo para el análisis EDA.")

        except Exception as e:
            st.error(f"❌ Ocurrió un error al procesar el archivo: {e}")
            st.warning("Verifique que el archivo CSV tenga el formato esperado.")
    else:
        st.warning("⚠️ Por favor, cargue un archivo CSV para continuar.")

# =========================================================
# MÓDULOS DE RESERVA (Para desarrollo posterior)
# =========================================================
elif opcion == "EDA (Análisis Exploratorio)":
    # Título Principal del Núcleo del Proyecto (Requisito Obligatorio)
    st.title("📊 Módulo 3: Análisis Exploratorio de Datos (EDA)")
    st.markdown("""
    Este módulo constituye el núcleo analítico de la aplicación. Su diseño interactivo permite 
    auditar la integridad estructural del dataset, clasificar sus dimensiones operativas y extraer 
    *insights* cuantitativos fundamentales sobre el comportamiento de los asegurados de **InsuranceCompany**.
    """)
    
    # CONTROL DE FLUJO: Validación estricta de carga previa del dataset
    if st.session_state.df_insurance is None:
        st.error("❌ **Acceso Restringido:** No se ha detectado ningún archivo en la memoria del sistema. Por favor, diríjase al módulo 'Carga de Datos' y cargue el archivo 'InsuranceCompany.csv' antes de proceder con el análisis.")
    else:
        # Extracción segura de datos y del objeto de la clase encapsuladora (POO)
        df = st.session_state.df_insurance
        an = st.session_state.analyzer
        
        # IMPORTACIÓN LOCAL DE MOTORES GRÁFICOS (Garantiza estabilidad en la renderización)
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Configuración estética global para los gráficos de Matplotlib/Seaborn
        sns.set_theme(style="whitegrid")
        plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12})
        
        # DEFINICIÓN DE INTERFAZ: Creación de las pestañas obligatorias de navegación interna
        tabs = st.tabs([
            "📋 1. Info General", 
            "🏷️ 2. Clasificación", 
            "📈 3. Estadísticas", 
            "🔍 4. Valores Faltantes", 
            "📊 5. Dist. Numéricas", 
            "🔤 6. Análisis Categórico", 
            "⚖️ 7. Bivariado (Num)", 
            "🗺️ 8. Bivariado (Cat)", 
            "🎛️ 9. Análisis Dinámico", 
            "🎯 10. Hallazgos Clave"
        ])
        
        # =========================================================================
        # ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET (.info())
        # =========================================================================
        with tabs[0]:
            st.write("## 📋 Ítem 1: Información General del Dataset")
            st.markdown("""
            **Explicación:** Esta sección emula de forma visual y tabular el comportamiento del método clásico `.info()` de Pandas. 
            Permite inspeccionar la infraestructura técnica del archivo cargado, detallando los tipos de datos asignados por el 
            intérprete y cuantificando de manera preliminar la presencia de celdas vacías.
            """)
            
            # Construcción dinámica de la matriz informativa de la estructura
            info_estructural = pd.DataFrame({
                "Columna / Variable": df.columns,
                "Tipo de Dato Técnico": [str(df[col].dtype) for col in df.columns],
                "Registros No Nulos": [int(df[col].count()) for col in df.columns],
                "Registros Nulos (Vacíos)": [int(df[col].isna().sum()) for col in df.columns],
                "Porcentaje de Vacíos (%)": [round((df[col].isna().sum() / len(df)) * 100, 3) for col in df.columns]
            })
            
            st.write("### 🔍 Matriz de Diagnóstico de Tipos de Datos e Integridad")
            st.dataframe(info_estructural, use_container_width=True, hide_index=True)
            
            st.info("""
            📌 **Interpretación Técnica:** El dataset presenta una composición mixta de variables continuas, discretas de conteo 
            y factores de texto. Se detecta con precisión que la variable crítica de evaluación de riesgo técnico 
            (`application_underwriting_score`) y las variables de morosidad concentran la totalidad de registros ausentes.
            """)

        # =========================================================================
        # ÍTEM 2: CLASIFICACIÓN DE VARIABLES (Uso de Función Personalizada de Clase)
        # =========================================================================
        with tabs[1]:
            st.write("## 🏷️ Ítem 2: Clasificación de Variables Numéricas y Categóricas")
            st.markdown("""
            **Explicación:** A través de la lógica de Programación Orientada a Objetos (POO), se ejecuta un método interno 
            que segrega sistemáticamente las columnas en dimensiones cuantitativas (numéricas) y cualitativas (categóricas). 
            Esta clasificación automatizada previene errores operacionales al momento de asignar los motores gráficos e interpretar los datos.
            """)
            
            # Recuperación de los atributos de listas calculados por la clase
            num_vars = an.num_cols
            cat_vars = an.cat_cols
            
            # Despliegue de métricas de conteo utilizando st.columns
            m_col1, m_col2 = st.columns(2)
            m_col1.metric(label="Total Variables Numéricas Detectadas", value=len(num_vars))
            m_col2.metric(label="Total Variables Categóricas Detectadas", value=len(cat_vars))
            
            st.divider()
            
            c_list1, c_list2 = st.columns(2)
            with c_list1:
                st.write("### 🔢 Variables Cuantitativas Identificadas")
                st.dataframe(pd.DataFrame({"Nombre Técnico de la Variable": num_vars}), use_container_width=True, hide_index=True)
            with c_list2:
                st.write("### 🔤 Variables Cualitativas / Factores Identificados")
                st.dataframe(pd.DataFrame({"Nombre Técnico de la Variable": cat_vars}), use_container_width=True, hide_index=True)

        # =========================================================================
        # ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS (.describe())
        # =========================================================================
        with tabs[2]:
            st.write("## 📈 Ítem 3: Resumen Estadístico Descriptivo")
            st.markdown("""
            **Explicación:** Aplicación del método `.describe()` para extraer métricas analíticas de tendencia central, 
            dispersión y posición. El análisis detallado de estos valores permite identificar anomalías distribucionales, 
            presencia de colas pesadas o sesgos severos en el comportamiento financiero de los clientes.
            """)
            
            # Widget interactivo opcional para filtrar variables específicas y cumplir uso de st.checkbox
            filtrar_moras = st.checkbox("Aislar únicamente métricas de variables de comportamiento de pago (Morosidad)")
            
            if filtrar_moras:
                columnas_interes = [c for c in num_vars if "Count" in c]
                if columnas_interes:
                    st.dataframe(df[columnas_interes].describe(), use_container_width=True)
                else:
                    st.warning("No se encontraron variables con el patrón de nombre 'Count'. Mostrando matriz completa.")
                    st.dataframe(df[num_vars].describe(), use_container_width=True)
            else:
                st.write("### 📊 Matriz Métrica de Variables Numéricas Continuas y Discretas")
                st.dataframe(df[num_vars].describe(), use_container_width=True)
            
            st.divider()
            st.write("### 💡 Interpretación Básica de Medias, Medianas y Dispersión")
            
            int_col1, int_col2 = st.columns(2)
            with int_col1:
                st.markdown("""
                * **Análisis de Asimetría en Ingresos (`Income`):** La media del ingreso mensual reportado es sustancialmente mayor que la mediana (Percentil 50%). Esta marcada discrepancia confirma una distribución con **sesgo positivo extremo (hacia la derecha)**, lo que evidencia que un grupo muy selecto y reducido de asegurados posee ingresos atípicos sumamente elevados, distorsionando el promedio global de la cartera.
                * **Evaluación de Edad (`age_in_days`):** La media aritmética y la mediana se encuentran fuertemente alineadas en torno a los 18,800 días (~51.5 años de edad), denotando una distribución simétrica y un segmento objetivo maduro y consolidado en términos demográficos.
                """)
            with int_col2:
                st.markdown("""
                * **Dispersión y Heterogeneidad del Costo de Pólizas (`premium`):** La desviación estándar de la prima es elevada respecto a su media aritmética. Esto indica una notable dispersión del riesgo y confirma que la compañía maneja una oferta comercial altamente heterogénea, comercializando desde microseguros accesibles hasta pólizas corporativas o patrimoniales de alto valor monetario.
                """)

        # =========================================================================
        # ÍTEM 4: ANÁLISIS PROFUNDO DE VALORES FALTANTES
        # =========================================================================
        with tabs[3]:
            st.write("## 🔍 Ítem 4: Auditoría y Diagnóstico de Valores Faltantes")
            st.markdown("""
            **Explicación:** Cuantificación y localización del vacío de datos. Los registros nulos representan una amenaza metodológica 
            para la toma de decisiones estratégicas, por lo que auditar su procedencia y volumen es mandatorio antes de proponer 
            cualquier plan de acción corporativo.
            """)
            
            df_nulos_resumen = info_estructural[info_estructural["Registros Nulos (Vacíos)"] > 0].sort_values(by="Registros Nulos (Vacíos)", ascending=False)
            
            if not df_nulos_resumen.empty:
                fn_col1, fn_col2 = st.columns([2, 3])
                with fn_col1:
                    st.write("### 📋 Conteo de Nulos Detectados")
                    st.dataframe(df_nulos_resumen[["Columna / Variable", "Registros Nulos (Vacíos)", "Porcentaje de Vacíos (%)"]], use_container_width=True, hide_index=True)
                
                with fn_col2:
                    st.write("### 📉 Representación Gráfica de la Ausencia de Datos")
                    fig_nulos, ax_nulos = plt.subplots(figsize=(7, 3.5))
                    sns.barplot(data=df_nulos_resumen, x="Registros Nulos (Vacíos)", y="Columna / Variable", palette="Oranges_r", ax=ax_nulos)
                    ax_nulos.set_title("Volumen de Datos Faltantes por Atributo", fontsize=11, fontweight="bold")
                    for index, value in enumerate(df_nulos_resumen["Registros Nulos (Vacíos)"]):
                        ax_nulos.text(value, index, f" {value:,}", va="center", fontweight="bold", fontsize=9)
                    st.pyplot(fig_nulos)
                
                st.divider()
                st.write("### 🧠 Discusión Breve sobre la Naturaleza de los Datos Ausentes")
                st.warning("""
                **Análisis Crítico de la Operación:** 1. **`application_underwriting_score` (~3.72% de nulos):** Este indicador mide la evaluación técnica de riesgo del solicitante al momento de postular a la póliza. La ausencia de este dato puede responder a dos realidades operativas: fallas de integración en sistemas tradicionales con plataformas web de venta rápida o clientes preferenciales exonerados de la evaluación convencional. Su omisión es un riesgo corporativo latente, por lo que se aconseja **imputar mediante la mediana histórica del grupo de riesgo** para no castigar artificialmente el análisis.
                2. **Bloque de Contadores de Morosidad (~0.12% de nulos):** Las variables asociadas al histórico de retrasos presentan un volumen marginal de nulos. Metodológicamente, un vacío en un campo de acumulación o conteo de incidencias negativas suele mapearse como la **ausencia total de la infracción**. Por lo tanto, la estrategia correcta para el negocio consiste en sustituir estos nulos por el valor entero `0`, asumiendo que son asegurados con un historial de pagos intachable.
                """)
            else:
                st.success("🎉 **Auditoría Exitosa:** No se han detectado celdas vacías ni valores nulos en ninguna de las variables del dataset.")

        # =========================================================================
        # ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS (Histogramas Interactivos)
        # =========================================================================
        with tabs[4]:
            st.write("## 📊 Ítem 5: Distribución de Variables Numéricas")
            st.markdown("""
            **Explicación:** Evaluación de la forma de las distribuciones. El análisis de histogramas permite identificar de manera visual 
            si los datos se comportan de acuerdo con estructuras simétricas, normales, multimodales o si sufren de severas distorsiones 
            causadas por valores atípicos (*outliers*).
            """)
            
            # CONTROL DINÁMICO: Inyección de widgets interactivos combinados (Requisito de la Guía)
            c_widgets1, c_widgets2, c_widgets3 = st.columns([2, 2, 2])
            with c_widgets1:
                var_dist_sel = st.selectbox("Seleccione la variable cuantitativa a graficar:", num_vars, index=0)
            with c_widgets2:
                bins_slider = st.slider("Ajuste el nivel de detalle del histograma (Número de Bins):", min_value=5, max_value=100, value=30)
            with c_widgets3:
                activar_kde = st.checkbox("Superponer Curva de Densidad Estimada (KDE)", value=True)
            
            # Generación interactiva del gráfico estadístico
            fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
            sns.histplot(data=df, x=var_dist_sel, bins=bins_slider, kde=activar_kde, color="#1f77b4", ax=ax_hist)
            ax_hist.set_title(f"Histograma Estadístico Interactivo para la Variable: {var_dist_sel}", fontsize=11, fontweight="bold")
            ax_hist.set_xlabel(var_dist_sel)
            ax_hist.set_ylabel("Frecuencia Absoluta de Registros")
            
            st.pyplot(fig_hist)
            
            st.write("### 📉 Interpretación Visual Orientada al Negocio")
            if "Income" in var_dist_sel:
                st.info("💡 **Interpretación:** La variable de ingresos muestra una concentración masiva de frecuencias en el extremo inferior izquierdo, confirmando un perfil de cliente de ingresos medios con una cola extremadamente larga hacia la derecha. Esto ratifica la necesidad de aplicar transformaciones matemáticas si se deseara modelar estadísticamente en el futuro.")
            elif "age" in var_dist_sel:
                st.info("💡 **Interpretación:** El histograma de edad en días describe una curva notablemente acampanada y equilibrada, lo que demuestra un reclutamiento homogéneo de clientes adultos en etapas económicamente estables de la vida.")
            else:
                st.info(f"💡 **Interpretación:** El perfil distribucional de '{var_dist_sel}' describe de forma clara el comportamiento real de los asegurados en cartera, permitiendo delimitar las fronteras operacionales normales frente a comportamientos atípicos.")

        # =========================================================================
        # ÍTEM 6: ANÁLISIS DE VARIABLES CATEGÓRICAS (Frecuencias y Proporciones)
        # =========================================================================
        with tabs[5]:
            st.write("## 🔤 Ítem 6: Análisis de Variables Categóricas")
            st.markdown("""
            **Explicación:** Este módulo desglosa la composición de las dimensiones cualitativas del dataset. 
            Muestra la frecuencia absoluta y la proporción porcentual de cada categoría, permitiendo reconocer la participación 
            de mercado interna de los diferentes segmentos y canales de la aseguradora.
            """)
            
            # Incorporación de la variable de renovación (Target) para enriquecer las opciones cualitativas
            opciones_cat = list(cat_vars)
            if 'renewal' in df.columns and 'renewal' not in opciones_cat:
                opciones_cat.append('renewal')
                
            var_cat_sel = st.selectbox("Seleccione la dimensión cualitativa a analizar:", opciones_cat, index=0)
            
            # Procesamiento matemático de frecuencias y proporciones
            conteo_abs = df[var_cat_sel].value_counts(dropna=False)
            proporciones = df[var_cat_sel].value_counts(normalize=True, dropna=False) * 100
            
            df_cat_resumen = pd.DataFrame({
                "Categoría / Etiqueta": conteo_abs.index,
                "Frecuencia Absoluta (Casos)": conteo_abs.values,
                "Proporción de Participación (%)": [f"{p:.2f}%" for p in proporciones.values]
            })
            
            cc_col1, cc_col2 = st.columns([2, 3])
            with cc_col1:
                st.write("### 📊 Tabla de Frecuencias Relativas")
                st.dataframe(df_cat_resumen, use_container_width=True, hide_index=True)
                
            with cc_col2:
                st.write("### 📉 Distribución de Participación (Gráfico de Barras)")
                fig_cat, ax_cat = plt.subplots(figsize=(7, 3.8))
                sns.barplot(x=conteo_abs.values, y=[str(idx) for idx in conteo_abs.index], palette="viridis", ax=ax_cat)
                ax_cat.set_title(f"Volumen y Distribución de Categorías para: {var_cat_sel}", fontsize=11, fontweight="bold")
                ax_cat.set_xlabel("Frecuencia de Ocurrencias")
                st.pyplot(fig_cat)

        # =========================================================================
        # ÍTEM 7: ANÁLISIS BIVARIADO - NUMÉRICO VS CATEGÓRICO (Target: Renewal)
        # =========================================================================
        with tabs[6]:
            st.write("## ⚖️ Ítem 7: Análisis Bivariado (Variables Numéricas vs Renovación)")
            st.markdown("""
            **Explicación:** Contraste estadístico de grupos. En esta sección se analiza cómo varían las métricas numéricas continuas 
            (como ingresos, primas o puntajes de riesgo) en función de la decisión final del cliente de renovar o abandonar la póliza (`renewal`). 
            Esto permite detectar si existen diferencias significativas en los perfiles financieros de ambos grupos.
            """)
            
            var_num_biv = st.selectbox("Seleccione el atributo numérico para evaluar contra la renovación:", num_vars, index=min(3, len(num_vars)-1))
            
            # Implementación de diagramas de caja (Boxplots) para comparar dispersión entre grupos
            fig_biv1, ax_biv1 = plt.subplots(figsize=(8, 4))
            sns.boxplot(data=df, x='renewal', y=var_num_biv, palette="Set2", ax=ax_biv1)
            ax_biv1.set_title(f"Diagrama de Cajas: {var_num_biv} desglosado por Estado de Renovación", fontsize=11, fontweight="bold")
            ax_biv1.set_xlabel("¿El Cliente Renovó la Póliza? (Target)")
            ax_biv1.set_ylabel(var_num_biv)
            
            # Control para mitigar distorsiones visuales por Outliers severos en Income
            if "Income" in var_num_biv:
                ax_biv1.set_ylim(0, df["Income"].quantile(0.95))
                st.caption("⚠️ *Nota Visual: El eje Y ha sido limitado al percentil 95 para ignorar outliers extremos y permitir la lectura del boxplot.*")
                
            st.pyplot(fig_biv1)
            
            st.write("### 💼 Valoración Estratégica del Comportamiento Cruzado")
            st.markdown(f"""
            Al cruzar la variable **{var_num_biv}** con la tasa de permanencia, la gerencia puede mapear si el precio o el perfil sociodemográfico 
            actúan como barreras de salida. Por ejemplo, variaciones marcadas en las medianas de los diagramas de cajas indicarían que el grupo 
            que decide no renovar está experimentando fricciones económicas o pertenece a un segmento con una sensibilidad al precio distinta.
            """)

        # =========================================================================
        # ÍTEM 8: ANÁLISIS BIVARIADO - CATEGÓRICO VS CATEGÓRICO
        # =========================================================================
        with tabs[7]:
            st.write("## 🗺️ Ítem 8: Análisis Bivariado (Variables Categóricas vs Renovación)")
            st.markdown("""
            **Explicación:** Análisis de tablas de contingencia cruzadas. Permite evaluar de manera directa la correlación e influencia 
            de factores cualitativos (tales como la zona de residencia o el canal de atracción) sobre la lealtad y retención del asegurado.
            """)
            
            var_cat_biv = st.selectbox("Seleccione el factor cualitativo a contrastar con el Target:", cat_vars, index=0)
            
            # Cálculo de la tabla de contingencia normalizada (Proporciones cruzadas)
            tabla_cruzada = pd.crosstab(df[var_cat_biv], df['renewal'], normalize='index') * 100
            
            bc_col1, bc_col2 = st.columns([2, 3])
            with bc_col1:
                st.write("### 📊 Tasa de Renovación Porcentual por Segmento")
                st.dataframe(tabla_cruzada.style.format("{:.2f}%"), use_container_width=True)
                
            with bc_col2:
                st.write("### 📉 Composición Porcentual Indexada")
                fig_biv2, ax_biv2 = plt.subplots(figsize=(7, 4))
                tabla_cruzada.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'], ax=ax_biv2)
                ax_biv2.set_title(f"Estructura de Renovación según {var_cat_biv}", fontsize=11, fontweight="bold")
                ax_biv2.set_ylabel("Porcentaje Representativo (%)")
                ax_biv2.set_xlabel(var_cat_biv)
                plt.xticks(rotation=0)
                plt.legend(title="¿Renovó?")
                st.pyplot(fig_biv2)

        # =========================================================================
        # ÍTEM 9: ANÁLISIS DINÁMICO BASADO EN PARAMETRIZACIÓN AVANZADA
        # =========================================================================
        with tabs[8]:
            st.write("## 🎛️ Ítem 9: Análisis Dinámico Basado en Parámetros Seleccionados")
            st.markdown("""
            **Explicación:** Interactividad analítica avanzada. Utilizando componentes de selección múltiple (`st.multiselect`), 
            esta pestaña faculta al usuario para aislar un subconjunto personalizado de variables macroeconómicas y de morosidad 
            para recalcular en tiempo real la matriz de correlación lineal de Pearson y su respectivo mapa de calor estadístico.
            """)
            
            # CONTROL DINÁMICO MULTISELECT: Configuración con variables por defecto para evitar pantallas en blanco
            variables_seleccionadas = st.multiselect(
                "Construya su matriz analítica seleccionando dos o más atributos numéricos:",
                options=num_vars,
                default=[num_vars[0], num_vars[1], num_vars[2]] if len(num_vars) >= 3 else num_vars
            )
            
            if len(variables_seleccionadas) >= 2:
                # Cómputo de la matriz de correlación en tiempo real
                matriz_corr = df[variables_seleccionadas].corr()
                
                dyn_col1, dyn_col2 = st.columns([2, 3])
                with dyn_col1:
                    st.write("### 🔢 Coeficientes de Correlación Numérica")
                    st.dataframe(matriz_corr.style.background_gradient(cmap='coolwarm', axis=None), use_container_width=True)
                
                with dyn_col2:
                    st.write("### 🗺️ Mapa de Calor de Interacciones Lineales (Heatmap)")
                    fig_heat, ax_heat = plt.subplots(figsize=(7, 4.5))
                    sns.heatmap(matriz_corr, annot=True, cmap="coolwarm", fmt=".3f", vmin=-1, vmax=1, center=0, cbar=True, ax=ax_heat)
                    ax_heat.set_title("Mapa de Interdependencias Lineales (Pearson)", fontsize=11, fontweight="bold")
                    st.pyplot(fig_heat)
            else:
                st.info("💡 **Guía de Uso:** Por favor, seleccione al menos **2 variables numéricas** en el componente superior para proyectar el mapa de interacciones y coeficientes lineales.")

        # =========================================================================
        # ÍTEM 10: HALLAZGOS CLAVE E INSIGHTS DEL EDA (Visualización Resumen)
        # =========================================================================
        with tabs[9]:
            st.write("## 🎯 Ítem 10: Hallazgos Clave e Insights del Análisis Exploratorio")
            st.markdown("""
            **Explicación:** Consolidación de hallazgos. Esta sección sintetiza las observaciones estadísticas de mayor impacto 
            descubiertas a lo largo del EDA, traduciendo los patrones numéricos abstractos en palancas estratégicas directas 
            para mitigar la fuga de clientes y optimizar la rentabilidad de **InsuranceCompany**.
            """)
            
            # Gráfico de síntesis ejecutiva: Relación entre morosidad acumulada y tasa de renovación
            st.write("### 📊 Gráfico Resumen Ejecutivo: Impacto del Historial de Atrasos en la Renovación")
            
            # Construimos una métrica combinada de morosidad para la visualización ejecutiva
            df_insight = df.copy()
            df_insight['Tiene_Historial_Mora'] = np.where(
                (df_insight['Count_3-6_months_late'] > 0) | 
                (df_insight['Count_6-12_months_late'] > 0) | 
                (df_insight['Count_more_than_12_months_late'] > 0), 
                'Con Retrasos', 'Sin Retrasos'
            )
            
            tabla_insight = pd.crosstab(df_insight['Tiene_Historial_Mora'], df_insight['renewal'], normalize='index') * 100
            
            fig_ins, ax_ins = plt.subplots(figsize=(8, 3.5))
            tabla_insight.plot(kind='barh', stacked=True, color=['#d9534f', '#5cb85c'], ax=ax_ins)
            ax_ins.set_title("Proporción de Renovación según Antecedentes de Pago", fontsize=11, fontweight="bold")
            ax_ins.set_xlabel("Porcentaje de la Cartera (%)")
            ax_ins.set_ylabel("Historial de Comportamiento")
            plt.legend(title="¿Renovó?")
            st.pyplot(fig_ins)
            
            st.divider()
            
elif opcion == "Conclusiones":
    st.title("💡 Conclusiones y Decisiones Estratégicas")
    st.markdown("""
    A continuación, se presentan las 5 conclusiones derivadas del análisis exploratorio, 
    enfocadas en la optimización de los procesos de retención de clientes y eficiencia operativa 
    de la aseguradora.
    """)

    # Definición de conclusiones técnicas y estratégicas
    conclusiones = [
        {
            "titulo": "1. Sensibilidad Crítica a la Morosidad",
            "texto": "Se ha identificado que cualquier registro de pago demorado (incluso a partir de los 3 meses) actúa como un factor de ruptura en la relación con el cliente. La decisión estratégica debe ser implementar programas de alerta temprana y refinanciamiento automático antes de que el asegurado alcance los 6 meses de impago."
        },
        {
            "titulo": "2. Validación de la Estructura de Ingresos",
            "texto": "La alta concentración de clientes en rangos de ingresos medios y la dispersión en los valores de primas indican que la compañía posee una oferta comercial robusta y diversificada. Se recomienda no enfocar las campañas de retención exclusivamente en el nivel de ingresos, sino en el valor percibido del servicio contratado."
        },
        {
            "titulo": "3. Homogeneidad del Perfil Demográfico",
            "texto": "El análisis de la edad de los asegurados confirma una distribución normal, sugiriendo que la base de clientes actual se encuentra en una etapa de madurez económica. La estrategia de comunicación debe alinearse con perfiles que buscan estabilidad y protección a largo plazo, evitando mensajes orientados a segmentos de mayor volatilidad."
        },
        {
            "titulo": "4. Canal de Captación y Calidad de Póliza",
            "texto": "La segmentación por canal de captación revela diferencias en las tasas de renovación. Es imperativo auditar los canales con menores tasas de retención para ajustar sus procesos de venta inicial, asegurando que las expectativas del cliente estén alineadas con el producto contratado desde el primer día."
        },
        {
            "titulo": "5. Oportunidad en la Gestión de Datos",
            "texto": "La existencia de nulos en variables clave de riesgo técnico durante el proceso de suscripción (`application_underwriting_score`) es una oportunidad de mejora operativa. Se recomienda estandarizar la captura de datos en todos los puntos de contacto para eliminar inconsistencias y fortalecer la calidad del historial de suscripción."
        }
    ]

    # Presentación interactiva de las conclusiones
    for con in conclusiones:
        with st.expander(con["titulo"]):
            st.write(con["texto"])

    st.divider()
    st.success("🎯 **Enfoque de Negocio:** Este análisis proporciona una base sólida para que la gerencia pueda priorizar recursos en la retención de clientes de alto riesgo y optimizar la captación en los canales más efectivos.")