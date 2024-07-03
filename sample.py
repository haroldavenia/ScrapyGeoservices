import deepdiff as deepdiff
import pandas as pd
import json
import numpy as np

def compare_features(df_old, df_new, attr_id):
    if not set(df_old.columns).issubset(df_new.columns):
        print("Las columnas no coinciden entre df_old y df_new")
        return None, None, None, pd.DataFrame({'Columns in df_old': list(set(df_old.columns) - set(df_new.columns)),
                                               'Columns in df_new': list(
                                                   set(df_new.columns) - set(df_old.columns))})

    df_old.set_index(attr_id, inplace=True)
    df_new.set_index(attr_id, inplace=True)

    # Fill NaN or None values with a specific value for comparison
    df_old.fillna(value=np.nan, inplace=True)
    df_new.fillna(value=np.nan, inplace=True)

    # Convert NaN values to a string or specific value
    df_old.replace(np.nan, 'MISSING', inplace=True)
    df_new.replace(np.nan, 'MISSING', inplace=True)

    added_features = df_new[~df_new.index.isin(df_old.index)].copy()
    removed_features = df_old[~df_old.index.isin(df_new.index)].copy()
    common_columns = df_old.columns.intersection(df_new.columns)

    # Perform the comparison with the replaced values
    modified_indices = df_new[df_new[common_columns].ne(df_old[common_columns]).any(axis=1)].index
    modified_features = df_new[df_new.index.isin(modified_indices) & df_new.index.isin(df_old.index)].copy()
    modified_features = modified_features[~modified_features.index.isin(added_features.index)]

    return added_features, removed_features, modified_features, None

# Ejemplo de uso:
# Suponiendo que tienes JSON data y lo has convertido a DataFrames df_old y df_new
json_data_old = '''
{
    "type": "FeatureCollection", "features": [{
      "type": "Feature",
      "id": "mc_inst_com_der_emision.194",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -5.89108155,
          43.43300
        ]
      },
      "geometry_name": "shape",
      "properties": {
        "renade": "ES033306000209",
        "id_instalacion": "195",
        "nombre_instalacion": "Calera de San Cucao, SA",
        "direccion": "Argüera s/n - SAN CUCAO DE LLANERA",
        "codigo_postal": "33425",
        "localidad": "Llanera",
        "provincia": "Asturias",
        "comunidad": "Principado de Asturias",
        "pais": "España",
        "longitud": "-5.89108154579905",
        "latitud": "43.4330100002853",
        "f2005": 83506,
        "f2006": "66726",
        "f2007": "78685",
        "f2008": "74739",
        "f2009": "55099",
        "f2010": "75924",
        "f2011": "70611",
        "f2012": "44372",
        "f2013": "45309",
        "f2014": "46098",
        "f2015": "43300",
        "f2016": "38664",
        "f2017": "62432",
        "f2018": "37314",
        "f2019": "55023",
        "f2020": "53718",
        "f2021": " ",
        "f2022": " ",
        "f2023": " ",
        "f2024": " ",
        "f2025": " ",
        "f2026": " ",
        "f2027": " ",
        "f2028": " ",
        "f2029": " ",
        "f2030": " ",
        "excl_fase_iii_2013_2020": "NO",
        "excl_fase_iv_2021_2025": "NO",
        "excl_fase_iv_2021_2025_a": "NO",
        "excl_fase_iv_2026_2030": " ",
        "excl_fase_iv_2026_2030_a": " ",
        "gdb_geomattr_data": null
      },
      "bbox": [
        -5.89108155,
        43.43301,
        -5.89108155,
        43.43301
      ]
    }]
}
'''

json_data_new = '''
{
    "type": "FeatureCollection", "features": [{
      "type": "Feature",
      "id": "mc_inst_com_der_emision.194",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -5.89108155,
          43.43301
        ]
      },
      "geometry_name": "shape",
      "properties": {
        "renade": "ES033306000209",
        "id_instalacion": "195",
        "nombre_instalacion": "Calera de San Cucao, SA",
        "direccion": "Argüera s/n - SAN CUCAO DE LLANERA",
        "codigo_postal": "33425",
        "localidad": "Llanera",
        "provincia": "Asturias",
        "comunidad": "Principado de Asturias",
        "pais": "España",
        "longitud": "-5.89108154579905",
        "latitud": "43.4330100002853",
        "f2005": 83506,
        "f2006": "66726",
        "f2007": "78685",
        "f2008": "74739",
        "f2009": "55099",
        "f2010": "75924",
        "f2011": "70611",
        "f2012": "44372",
        "f2013": "45309",
        "f2014": "46098",
        "f2015": "43300",
        "f2016": "38664",
        "f2017": "62432",
        "f2018": "37314",
        "f2019": "55023",
        "f2020": "53718",
        "f2021": " ",
        "f2022": " ",
        "f2023": " ",
        "f2024": " ",
        "f2025": " ",
        "f2026": " ",
        "f2027": " ",
        "f2028": " ",
        "f2029": " ",
        "f2030": " ",
        "excl_fase_iii_2013_2020": "NO",
        "excl_fase_iv_2021_2025": "NO",
        "excl_fase_iv_2021_2025_a": "NO",
        "excl_fase_iv_2026_2030": " ",
        "excl_fase_iv_2026_2030_a": " ",
        "gdb_geomattr_data": null
      },
      "bbox": [
        -5.89108155,
        43.43301,
        -5.89108155,
        43.43301
      ]
    }]
}
'''

# Convertir JSON a DataFrames
data_old = json.loads(json_data_old)
data_new = json.loads(json_data_new)
df_old = pd.json_normalize(data_old['features'])
df_new = pd.json_normalize(data_new['features'])

# Llamar a la función compare_features
attr_id = 'id'
added, removed, modified, error = compare_features(df_old, df_new, attr_id)

# Imprimir resultados
print("Características añadidas:")
print(added)

print("Características eliminadas:")
print(removed)

print("Características modificadas:")
print(modified)


diff = deepdiff.DeepDiff(data_old['features'], data_new['features'])
print("Diferencias:", diff)

if error is not None:
    print("Error:")
    print(error)