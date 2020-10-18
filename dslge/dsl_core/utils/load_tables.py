import numpy as np
import pandas as pd
import io
from dsl_core.utils.constants import DOC_DIR

def _file_serialize(filename, fieldnames=None, file_type='csv', sep=',', encoding='utf-8'):
    df = pd.DataFrame()
    if file_type == 'csv':
        df = pd.read_csv(filename + '.csv', sep=sep,
                         usecols=fieldnames, encoding=encoding)
    else:
        df = pd.read_excel(filename + '.' + file_type, usecols=fieldnames)
    df.to_pickle(filename + '.pkl')
    return df


def _load_file(filename):
    df = pd.DataFrame()
    try:
        df = pd.read_pickle(filename + '.pkl')
        return df
    except:
        return df


def load_serialized_file(path, fieldnames=None, file_type='csv', sep=',', encoding='utf-8'):
    df = _load_file(path)
    if df.empty:
        return _file_serialize(path, fieldnames=fieldnames, file_type=file_type, sep=sep, encoding=encoding)
    return df


def load_df_from_table_with_col(filename, fieldname, nitems=0, fieldnames=None, file_type='csv', encoding='utf-8', sep=';'):
    df = load_serialized_file(
        DOC_DIR + filename, file_type=file_type, sep=sep, encoding=encoding, fieldnames=fieldnames)
    df = df if nitems == 0 else df[0:nitems]
    df.dropna(
        axis=0, subset=[fieldname], inplace=True)
    df.reset_index(inplace=True)
    return df


def load_df_from_table(filename, nitems=0, file_type='csv', encoding='utf-8', sep=';'):
    df = load_serialized_file(
        DOC_DIR + filename, file_type=file_type, sep=sep, encoding=encoding)
    df = df if nitems == 0 else df[0:nitems]
    return df


