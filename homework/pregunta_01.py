"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import re
import pandas as pd

def pregunta_01():
    """
    Construye y retorna un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minúsculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    
    def formatear_columna(encabezado):
        """Convierte el encabezado a minúsculas y reemplaza espacios por guiones bajos."""
        return encabezado.lower().replace(" ", "_")

    
    with open("files/input/clusters_report.txt", "r") as archivo:
        lineas = archivo.readlines()

    
    titulo_1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    titulo_2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    titulo_1.pop()  # Eliminar el último elemento vacío
    titulo_2.pop(0)  # Eliminar el primer elemento vacío

  
    encabezados = [
        titulo_1[0],
        f"{titulo_1[1]} {titulo_2[0]}",
        f"{titulo_1[2]} {titulo_2[1]}",
        titulo_1[3]
    ]
    encabezados = [formatear_columna(h) for h in encabezados]

    datos = pd.read_fwf(
        "files/input/clusters_report.txt",
        widths=[9, 16, 16, 80], 
        header=None,
        names=encabezados,
        skip_blank_lines=False,
        converters={encabezados[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:]  #

    
    claves = datos[encabezados[3]]
    datos = datos[datos[encabezados[0]].notna()].drop(columns=[encabezados[3]])  
    datos = datos.astype({
        encabezados[0]: int,
        encabezados[1]: int,
        encabezados[2]: float,
    })

   
    palabras_clave = []
    texto_temporal = ""
    for linea in claves:        
        if isinstance(linea, str): 
            if linea.endswith("."): 
                linea = linea[:-1]  
            linea = re.sub(r'\s+', ' ', linea).strip()  
            texto_temporal += linea + " "
        elif texto_temporal:  # Cu
            palabras_clave.append(", ".join(re.split(r'\s*,\s*', texto_temporal.strip())))
            texto_temporal = ""  
    if texto_temporal: 
        palabras_clave.append(", ".join(re.split(r'\s*,\s*', texto_temporal.strip())))

   
    datos[encabezados[3]] = palabras_clave

    return datos

print(pregunta_01())