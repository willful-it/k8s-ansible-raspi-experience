from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='inventory.db', create_db=True)
# set_sql_debug(True)


class Host(db.Entity):
    ip = Required(str, unique=True)
    mac = Required(str, unique=True)
    hostname = Required(str, unique=True)


db.generate_mapping(create_tables=True)


@db_session
def get_host_by_mac(mac: str) -> Host:
    return Host.get(mac=mac)


@db_session
def save_host(mac: str, ip: str, hostname: str) -> Host:
    host = Host(ip=ip, mac=mac, hostname=hostname)
    commit()

    return host
