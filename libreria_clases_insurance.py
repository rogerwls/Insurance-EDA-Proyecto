import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError("El DataFrame no puede ser nulo.")
        
        self.df = df.copy()
        self.target = 'renewal'
        self.num_cols = []
        self.cat_cols = []
        self.classify_variables()

    def classify_variables(self):
        """Identifica automáticamente columnas numéricas y categóricas."""
        self.num_cols = [c for c in self.df.select_dtypes(include=np.number).columns if c != self.target]
        self.cat_cols = [c for c in self.df.select_dtypes(exclude=np.number).columns if c != self.target]

    def obtener_dimensiones(self):
        """Retorna las filas y columnas del dataset."""
        return self.df.shape

    def obtener_info_general(self):
        """Retorna un resumen de tipos, nulos y porcentaje de vacíos."""
        info_dict = {
            "Columna / Variable": self.df.columns,
            "Tipo de Dato Técnico": [str(self.df[col].dtype) for col in self.df.columns],
            "Registros No Nulos": [int(self.df[col].count()) for col in self.df.columns],
            "Registros Nulos (Vacíos)": [int(self.df[col].isna().sum()) for col in self.df.columns],
            "Porcentaje de Vacíos (%)": [round((self.df[col].isna().sum() / len(self.df)) * 100, 3) for col in self.df.columns]
        }
        return pd.DataFrame(info_dict)

    def get_info(self):
        return self.obtener_info_general()

    def generar_descriptive_stats(self):
        """Ejecuta .describe() sobre variables numéricas."""
        return self.df[self.num_cols].describe()

    def get_describe(self):
        return self.df.describe()

    def plot_valores_faltantes(self):
        """Genera gráfico de barras de nulos."""
        nulos = self.df.isna().sum()
        nulos_filtrados = nulos[nulos > 0].sort_values(ascending=False)
        if nulos_filtrados.empty:
            return None
        fig, ax = plt.subplots(figsize=(7, 3.5))
        sns.barplot(x=nulos_filtrados.values, y=[str(idx) for idx in nulos_filtrados.index], palette="Oranges_r", ax=ax)
        return fig

    def plot_hist(self, col, bins=30, kde=True):
        """Gráfico de histograma."""
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(data=self.df, x=col, bins=bins, kde=kde, color="#1f77b4", ax=ax)
        return fig

    def plot_cat(self, col):
        """Gráfico de barras para categóricas."""
        conteo = self.df[col].value_counts(dropna=False)
        fig, ax = plt.subplots(figsize=(7, 3.8))
        sns.barplot(x=conteo.values, y=[str(idx) for idx in conteo.index], palette="viridis", ax=ax)
        return fig

    def plot_bivariado(self, col_y, col_x):
        """Análisis bivariado automático."""
        fig, ax = plt.subplots(figsize=(8, 4))
        if col_y in self.num_cols or pd.api.types.is_numeric_dtype(self.df[col_y]):
            sns.boxplot(data=self.df, x=col_x, y=col_y, palette="Set2", ax=ax)
        else:
            pd.crosstab(self.df[col_x], self.df[col_y], normalize='index').plot(kind='bar', stacked=True, ax=ax)
        return fig