import yaml
from os import path

yaml.warnings({'YAMLLoadWarning': False})


def get_configs():
    # configs = None
    with open(path.join('flask_kb/configs/', 'configs.yaml'), 'r') as stream:
        configs = yaml.load(stream)
    
    host, port = configs['host'], configs['port']
    user, pwd = configs['user'], configs['pwd']
    database, sql = configs['database'], configs['sql']
    
    return host, port, user, pwd, database, sql


load_configs = get_configs()
HOST, PORT = load_configs[:2]
USER, PWD = load_configs[2:4]
DB, SQL = load_configs[4:]

CONN_STRING = "{0}+mysqlconnector://{1}:{2}@{3}:{4}/{5}" \
    .format(SQL, USER, PWD, HOST, PORT, DB)
