import os
import configparser
import pyodbc

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
_config = configparser.ConfigParser()
_config.read(_CONFIG_PATH, encoding='utf-8')

def cfg_get(section: str, key: str, fallback=None):
    try:
        return _config.get(section, key, fallback=fallback)
    except Exception:
        return fallback

def cfg_getbool(section: str, key: str, fallback: bool=False) -> bool:
    try:
        return _config.getboolean(section, key, fallback=fallback)
    except Exception:
        return fallback

def load_sql_queries(path=os.path.join(os.path.dirname(__file__), 'zapytania.sql')):
    queries = {}
    name = None
    buf = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith('-- name:'):
                    if name and buf:
                        queries[name] = ''.join(buf).rstrip()
                    name = line_stripped.split(':', 1)[1].strip()
                    buf = []
                elif line_stripped == '-- end':
                    if name is not None:
                        queries[name] = ''.join(buf).rstrip()
                    name = None
                    buf = []
                elif name is not None:
                    buf.append(line)
        if name and buf:
            queries[name] = ''.join(buf).rstrip()
    except FileNotFoundError:
        pass
    return queries

# Globalny słownik SQL
SQL = load_sql_queries()

def create_connection():
    driver = cfg_get('database', 'driver', fallback='SQL Server')
    server = cfg_get('database', 'server')
    database = cfg_get('database', 'database')
    trusted = cfg_get('database', 'trusted_connection', fallback='yes')
    autocommit = cfg_getbool('database', 'autocommit', fallback=True)
    if driver and (not (driver.startswith('{') and driver.endswith('}'))):
        driver = '{' + driver + '}'
    conn_str = f'Driver={driver}; Server={server}; Database={database}; Trusted_Connection={trusted};'
    return pyodbc.connect(conn_str, autocommit=autocommit)