import argparse
import csv
import ipaddress
import json
import logging
import sys
from datetime import datetime

HEADER = ["name", "env", "ip", "port", "role"]

log = logging.getLogger("fleetcheck")


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
    except (OSError, UnicodeDecodeError) as e:
        log.error("inventaire illisible : %s", e)
        sys.exit(2)
    if not rows or rows[0] != HEADER:
        log.error("en-tête attendu dans %s : %s", path, ",".join(HEADER))
        sys.exit(2)

    servers, invalid = [], []
    for line, row in enumerate(rows[1:], start=2):
        if not row:
            continue
        try:
            if len(row) != len(HEADER):
                raise InvalidServer(f"{len(row)} champs au lieu de {len(HEADER)}")
            servers.append(validate(dict(zip(HEADER, row))))
            log.debug("ligne %d valide : %s", line, row[0])
        except InvalidServer as e:
            log.warning("ligne %d ignorée : %s", line, e)
            invalid.append({"line": line, "raw": ",".join(row), "error": str(e)})
    if not servers:
        log.error("aucune ligne valide dans %s", path)
        sys.exit(2)
    log.info("%d serveur(s) valide(s), %d ligne(s) invalide(s) dans %s", len(servers), len(invalid), path)
    return servers, invalid


def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        log.error("config illisible (%s) : %s", path, e)
        sys.exit(2)


def exit_code(statuses, invalid_count):
    if invalid_count:
        return 2
    if "down" in statuses:
        return 1
    return 0


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


def print_summary(servers, invalid):
    print(f"{len(servers)} serveurs valides, {len(invalid)} invalides")
    print(f"par env : {format_counts(count_by(servers, 'env'))}")
    print(f"par rôle : {format_counts(count_by(servers, 'role'))}")
    prod_web = by_role(by_env(servers, "prod"), "web")
    print(f"prod/web : {', '.join(s['name'] for s in prod_web)}")


def main():
    parser = argparse.ArgumentParser(description="Inventaire d'un parc de serveurs.")
    parser.add_argument("--inventory", default="servers.csv", help="fichier CSV d'inventaire (défaut : servers.csv)")
    parser.add_argument("--env", help="ne garder que cet environnement")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="format de la sortie standard")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="-v : INFO, -vv : DEBUG")
    args = parser.parse_args()

    if args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s %(message)s", stream=sys.stderr)

    config = load_config("config.json")
    servers, invalid = load(args.inventory)
    if args.env:
        servers = by_env(servers, args.env)
        if not servers:
            log.error("aucun serveur pour --env %s", args.env)
            sys.exit(2)

    report = build_report(servers, invalid)
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    log.info("rapport écrit : report.json")

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_summary(servers, invalid)

    sys.exit(exit_code([], len(invalid)))


if __name__ == "__main__":
    main()
