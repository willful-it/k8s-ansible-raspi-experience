from pony.orm import Database, Required, commit, db_session

db = Database()


class Host(db.Entity):
    ip = Required(str, unique=True)
    mac = Required(str, unique=True)
    hostname = Required(str, unique=True)


class PersistenceService:
    def __init__(self):
        db.bind(provider='sqlite', filename='inventory.db', create_db=True)
        db.generate_mapping(create_tables=True)

    @db_session
    def get_host_by_mac(self, mac: str) -> Host:
        """Returns a host by its mac address

        Args:
            mac (str): The mac address to search for

        Returns:
            Host: The host if found, None otherwise
        """

        return Host.get(mac=mac)

    @db_session
    def create_host(self, mac: str, ip: str,
                    hostname: str, role: str = None) -> Host:
        """Creates an host

        Args:
            mac (str): The host mac address
            ip (str): The host ipv4 address
            hostname (str): The host name
            role (str, optional): The role of the host. Defaults to None.

        Returns:
            Host: The created host
        """

        host = Host(ip=ip, mac=mac, hostname=hostname)
        commit()

        return host
