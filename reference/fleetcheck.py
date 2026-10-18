import csv
import ipaddress
import json
import sys
from datetime import datetime

INVENTORY = "servers.csv"
HEADER = ["name", "env", "ip", "port", "role"]


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


def load(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError as e:
        print(f"inventaire illisible : {e}")
        sys.exit(1)
    if not rows or rows[0] != HEADER:
        print(f"en-tête attendu dans {path} : {','.join(HEADER)}")
        sys.exit(1)

    servers, invalid = [], []
    for line, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        try:
            if len(row) != len(HEADER):
                raise InvalidServer(f"{len(row)} champs au lieu de {len(HEADER)}")
            servers.append(validate(dict(zip(HEADER, row))))
        except InvalidServer as e:
            invalid.append({"line": line, "raw": ",".join(row), "error": str(e)})
    if not servers:
        print(f"aucune ligne valide dans {path}")
        sys.exit(1)
    return servers, invalid


def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"config illisible ({path}) : {e}")
        sys.exit(1)


def build_report(servers, invalid):
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary": {"total": len(servers), "invalid": len(invalid)},
        "services": servers,
        "invalid_lines": invalid,
    }


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


config = load_config("config.json")
servers, invalid = load(INVENTORY)
print(f"{len(servers)} serveurs valides, {len(invalid)} invalides")
print(f"par env : {format_counts(count_by(servers, 'env'))}")
print(f"par rôle : {format_counts(count_by(servers, 'role'))}")
prod_web = by_role(by_env(servers, "prod"), "web")
print(f"prod/web : {', '.join(s['name'] for s in prod_web)}")
for line in invalid:
    print(f"invalide ligne {line['line']} : {line['error']}")

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(build_report(servers, invalid), f, indent=2, ensure_ascii=False)
