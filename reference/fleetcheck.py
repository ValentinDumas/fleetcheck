SERVERS = [
    {"name": "web-1", "env": "prod", "ip": "127.0.0.1", "port": 8001, "role": "web"},
    {"name": "web-2", "env": "prod", "ip": "127.0.0.1", "port": 8002, "role": "web"},
    {"name": "api-1", "env": "prod", "ip": "127.0.0.1", "port": 8003, "role": "api"},
    {"name": "api-2", "env": "prod", "ip": "127.0.0.1", "port": 8004, "role": "api"},
    {"name": "worker-1", "env": "prod", "ip": "127.0.0.1", "port": 8005, "role": "worker"},
    {"name": "web-stg-1", "env": "staging", "ip": "127.0.0.1", "port": 8006, "role": "web"},
    {"name": "api-stg-1", "env": "staging", "ip": "127.0.0.1", "port": 8007, "role": "api"},
    {"name": "cache-1", "env": "prod", "ip": "127.0.0.1", "port": 8009, "role": "cache"},
    {"name": "db-1", "env": "prod", "ip": "192.0.2.1", "port": 5432, "role": "db"},
]


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


print(f"{len(SERVERS)} serveurs")
print(f"par env : {format_counts(count_by(SERVERS, 'env'))}")
print(f"par rôle : {format_counts(count_by(SERVERS, 'role'))}")
prod_web = by_role(by_env(SERVERS, "prod"), "web")
print(f"prod/web : {', '.join(s['name'] for s in prod_web)}")
