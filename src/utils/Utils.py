import re
import json
import os
import pandas as pd
import pathlib
import numpy as np
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox

FORMAT_TIME = "%Y%m%d_%H%M%S"


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def validate_bbox(x_min, y_min, x_max, y_max):
    if x_min == '' and y_min == '' and x_max == '' and y_max == '':
        return True, None, None
    elif x_min == '' or y_min == '' or x_max == '' or y_max == '':
        return False, None, "All bbox values must be empty."
    else:
        try:
            xmin = float(x_min)
            ymin = float(y_min)
            xmax = float(x_max)
            ymax = float(y_max)
            return True, (xmin, ymin, xmax, ymax), None
        except ValueError:
            return False, None, "All bbox values must be valid float numbers."


def valid_int(value):
    try:
        value_int = int(value)
        return True, value_int, None
    except ValueError:
        return False, None, "All bbox values must be valid float numbers."


def read_features_from_json(path_file):
    try:
        with open(path_file) as json_file:
            data = json.load(json_file)
            features = data.get('features', None)
            if features is None:
                raise ValueError("Invalid JSON: 'features' key not found")
            return pd.json_normalize(data.get('features', None))
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Error reading JSON file: {e}")


def read_previous_json(name_file):
    documents_folder = pathlib.Path.home().joinpath("Documents").joinpath("Geoservices")
    if not documents_folder.exists():
        return None

    previous_files = sorted([f for f in os.listdir(documents_folder) if
                             f.startswith("{}_".format(name_file)) and f.endswith(".json")])
    if previous_files:
        previous_file_path = os.path.join(documents_folder, previous_files[-1])
        return previous_file_path

    return None


def save_previous_json_backup(name_file):
    documents_folder = pathlib.Path.home().joinpath("Documents").joinpath("Geoservices")
    previous_files = sorted([f for f in os.listdir(documents_folder) if
                             f.startswith("{}_".format(name_file)) and f.endswith(".json")])
    if previous_files:
        previous_file_path = os.path.join(documents_folder, previous_files[-1])
        try:
            os.rename(previous_file_path, previous_file_path + ".bak")
        except FileExistsError:
            print(f"Backup file already exists: {previous_file_path}.bak")


def generate_report(added, removed, modified, columns_diff, name_file):
    timestamp = datetime.now().strftime(FORMAT_TIME)
    documents_folder = pathlib.Path.home().joinpath("Documents").joinpath("Geoservices")
    report_path = os.path.join(documents_folder, f"{name_file}_updates_{timestamp}.xlsx")
    with pd.ExcelWriter(report_path) as writer:
        if added is not None and not added.empty:
            added.to_excel(writer, sheet_name='Added Features')
        if removed is not None and not removed.empty:
            removed.to_excel(writer, sheet_name='Removed Features')
        if modified is not None and not modified.empty:
            modified.to_excel(writer, sheet_name='Modified Features')
        if columns_diff is not None and not columns_diff.empty:
            columns_diff.to_excel(writer, sheet_name='Columns Differences')
    return f"Report generated: {report_path}"


def write_JSON_file(json_data, name_file):
    timestamp = datetime.now().strftime(get_format_time())
    documents_folder = pathlib.Path.home().joinpath("Documents").joinpath("Geoservices")
    if not documents_folder.exists():
        documents_folder.mkdir(parents=True)
    json_file_path = os.path.join(documents_folder, f"{name_file}_{timestamp}.json")
    with open(json_file_path, "w") as json_file:
        # json_data = json.loads(self.__query_result.to_json)
        # json.dump(json_data, json_file, indent=4)
        json_file.write(json_data)
    return json_file_path


def compare_features(df_old, df_new, attr_id):
    if not set(df_old.columns).issubset(df_new.columns):
        print("Las columnas no coinciden entre df_old y df_new")
        return None, None, None, pd.DataFrame({
            'Columns in df_old': list(set(df_old.columns) - set(df_new.columns)),
            'Columns in df_new': list(set(df_new.columns) - set(df_old.columns))
        })

    # Eliminar duplicados y resetear el índice
    df_old = df_old.drop_duplicates(subset=[attr_id]).set_index(attr_id)
    df_new = df_new.drop_duplicates(subset=[attr_id]).set_index(attr_id)

    # Fill NaN or None values with a specific value for comparison
    df_old_filled = df_old.fillna(value=np.nan).copy()
    df_new_filled = df_new.fillna(value=np.nan).copy()

    # Convert NaN values to a string or specific value
    df_old_filled.replace(np.nan, 'MISSING', inplace=True)
    df_new_filled.replace(np.nan, 'MISSING', inplace=True)

    added_features = df_new_filled[~df_new_filled.index.isin(df_old_filled.index)].copy()
    removed_features = df_old_filled[~df_old_filled.index.isin(df_new_filled.index)].copy()
    common_columns = df_old_filled.columns.intersection(df_new_filled.columns)

    # Ensure that both DataFrames are aligned on the index before comparison
    df_old_aligned = df_old_filled.reindex(df_new_filled.index)
    df_new_aligned = df_new_filled.reindex(df_old_filled.index)

    # Perform the comparison with the aligned DataFrames
    modified_indices = df_new_aligned[df_new_aligned[common_columns].ne(df_old_aligned[common_columns]).any(axis=1)].index
    modified_features = df_new_filled.loc[modified_indices.intersection(df_old_filled.index)].copy()
    modified_features = modified_features[~modified_features.index.isin(added_features.index)]

    return added_features, removed_features, modified_features, None


def get_format_time():
    return FORMAT_TIME


def show_message_box(title, message, icon, buttons_ok_cancel=False, add_message=None):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(message)
    if add_message:
        msg.setInformativeText(add_message)
    if buttons_ok_cancel:
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    msg.exec_()
