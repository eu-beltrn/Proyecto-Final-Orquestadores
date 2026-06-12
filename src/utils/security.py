import hashlib
import pandas as pd

def enmascarar_dato(texto):
    """Convierte un texto plano en un hash SHA-256 irreversible para proteger la identidad."""
    if pd.isna(texto) or texto is None:
        return None
    return hashlib.sha256(str(texto).encode('utf-8')).hexdigest()

def aplicar_gobernanza_datos(df, columnas_sensibles):
    """
    Simula la aplicación de políticas de privacidad.
    Recibe un DataFrame y enmascara las columnas que contienen datos sensibles.
    """
    df_seguro = df.copy()
    for col in columnas_sensibles:
        if col in df_seguro.columns:
            df_seguro[col] = df_seguro[col].apply(enmascarar_dato)
            
    return df_seguro