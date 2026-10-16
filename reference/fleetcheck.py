import ipaddress

SERVERS = [
    {"name": "web-1", "env": "prod", "ip": "127.0.0.1", "port": "8001", "role": "web"},
    {"name": "web-2", "env": "prod", "ip": "127.0.0.1", "port": "8002", "role": "web"},
    {"name": "api-1", "env": "prod", "ip": "127.0.0.1", "port": "8003", "role": "api"},
    {"name": "api-2", "env": "prod", "ip": "127.0.0.1", "port": "8004", "role": "api"},
    {"name": "worker-1", "env": "prod", "ip": "127.0.0.1", "port": "8005", "role": "worker"},
    {"name": "web-stg-1", "env": "staging", "ip": "127.0.0.1", "port": "8006", "role": "web"},
    {"name": "api-stg-1", "env": "staging", "ip": "127.0.0.1", "port": "8007", "role": "api"},
    {"name": "cache-1", "env": "prod", "ip": "127.0.0.1", "port": "8009", "role": "cache"},
    {"name": "db-1", "env": "prod", "ip": "192.0.2.1", "port": "5432", "role": "db"},
    {"name": "api-3", "env": "prod", "ip": "127.0.0.1", "port": "abc", "role": "api"},
    {"name": "web-3", "env": "prod", "ip": "300.0.0.1", "port": "8010", "role": "web"},
]


class InvalidServer(Exception):
    pass


def validate(server):
    try:
        port = int(server["port"])
    except ValueError:
        raise InvalidServer(f"port non entier : '{server['port']}'")
    if not 1 <= port <= 65535:
        raise InvalidServer(f"port hors de 1-65535 : {port}")
    try:
        ipaddress.ip_address(server["ip"])
    except ValueError:
        raise InvalidServer(f"IP invalide : '{server['ip']}'")
    for key in ("name", "env", "role"):
        if not server[key]:
            raise InvalidServer(f"champ '{key}' vide")
    valid = dict(server)
    valid["port"] = port
    return valid


def load(raw_servers):
    servers, invalid = [], []
    for raw in raw_servers:
        try:
            servers.append(validate(raw))
        except InvalidServer as e:
            invalid.append({"name": raw["name"], "error": str(e)})
    return servers, invalid


def by_env(servers, env):
    return [s for s in servers if s["env"] == env]


def by_role(servers, role):
    return [s for s in servers if s["role"] == role]


def count_by(servers, key):
    counts = {}
    for server in servers:
        counts[server[key]] = counts.get(server[key], 0) + 1
    return counts


def format_counts(counts):
    return ", ".join(f"{value} {count}" for value, count in counts.items())


servers, invalid = load(SERVERS)
print(f"{len(servers)} serveurs valides, {len(invalid)} invalides")
print(f"par env : {format_counts(count_by(servers, 'env'))}")
print(f"par rôle : {format_counts(count_by(servers, 'role'))}")
prod_web = by_role(by_env(servers, "prod"), "web")
print(f"prod/web : {', '.join(s['name'] for s in prod_web)}")
for line in invalid:
    print(f"invalide {line['name']} : {line['error']}")
