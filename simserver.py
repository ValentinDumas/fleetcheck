"""Serveur simulé du fil rouge fleetcheck : un port par service, plus un port plateforme.

python simserver.py [--seed N] [--inventory | --scenario] [--base-port 8000] [--host 127.0.0.1]
"""

import argparse
import csv
import json
import random
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICES = [
    ("web-1", "prod", "web"),
    ("web-2", "prod", "web"),
    ("api-1", "prod", "api"),
    ("api-2", "prod", "api"),
    ("worker-1", "prod", "worker"),
    ("web-stg-1", "staging", "web"),
    ("api-stg-1", "staging", "api"),
]
REFERENCE = {
    "web-1": ("healthy", "2.3.1"),
    "web-2": ("slow", "2.3.1"),
    "api-1": ("healthy", "2.3.1"),
    "api-2": ("error", "2.3.1"),
    "worker-1": ("flaky", "2.3.0"),
    "web-stg-1": ("healthy", "2.4.0-rc1"),
    "api-stg-1": ("timeout", "2.4.0-rc1"),
}
TIMEOUT_DELAY_S = 10
FLAKY_CYCLE = [503, 503, 200]


def release(version, released_at):
    return {"tag_name": f"v{version}", "name": version, "released_at": released_at}


def reference_scenario(base_port):
    services = []
    for i, (name, env, role) in enumerate(SERVICES, start=1):
        behavior, version = REFERENCE[name]
        services.append({"name": name, "env": env, "role": role, "port": base_port + i,
                         "behavior": behavior, "version": version, "delay_s": 1.5, "error_code": 503})
    releases = [release("2.3.1", "2026-09-28T10:00:00Z"), release("2.3.0", "2026-09-14T10:00:00Z")]
    return {"seed": None, "releases": releases, "services": services}


def seeded_scenario(seed, base_port):
    rng = random.Random(seed)
    major, minor, patch = rng.randint(1, 4), rng.randint(1, 9), rng.randint(0, 9)
    latest = f"{major}.{minor}.{patch}"
    previous = f"{major}.{minor - 1}.{rng.randint(0, 9)}"
    prerelease = f"{major}.{minor + 1}.0-rc1"

    behaviors = ["slow", "error", "timeout", "flaky"] + ["healthy"] * (len(SERVICES) - 4)
    rng.shuffle(behaviors)
    prod_names = [name for name, env, _ in SERVICES if env == "prod"]
    lagging = rng.sample(prod_names, rng.choice([1, 2]))
    delay_s = round(rng.uniform(1.2, 2.5), 1)
    error_code = rng.choice([500, 502, 503])

    services = []
    for i, ((name, env, role), behavior) in enumerate(zip(SERVICES, behaviors), start=1):
        if env == "staging":
            version = prerelease
        else:
            version = previous if name in lagging else latest
        services.append({"name": name, "env": env, "role": role, "port": base_port + i,
                         "behavior": behavior, "version": version, "delay_s": delay_s,
                         "error_code": error_code})
    releases = [release(latest, "2026-09-28T10:00:00Z"), release(previous, "2026-09-14T10:00:00Z")]
    return {"seed": seed, "releases": releases, "services": services}


def write_inventory(scenario, base_port):
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["name", "env", "ip", "port", "role"])
    for s in scenario["services"]:
        writer.writerow([s["name"], s["env"], "127.0.0.1", s["port"], s["role"]])
    writer.writerow(["cache-1", "prod", "127.0.0.1", base_port + 9, "cache"])
    writer.writerow(["db-1", "prod", "192.0.2.1", 5432, "db"])


class Handler(BaseHTTPRequestHandler):
    flaky_lock = threading.Lock()
    flaky_calls = {}

    def log_message(self, format, *args):
        pass

    def send_json(self, code, body=None):
        elapsed = time.monotonic() - self.started
        name = self.server.service["name"] if self.server.service else "platform"
        print(f"{time.strftime('%H:%M:%S')} {name:<10} {self.command:<4} {self.path} {code} {elapsed:.2f}s",
              flush=True)
        try:
            self.send_response(code)
            if body is None:
                self.end_headers()
                return
            data = json.dumps(body).encode()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass  # client parti avant la réponse (timeout côté client)

    def do_GET(self):
        self.started = time.monotonic()
        service = self.server.service
        if service is None:
            if self.path == "/api/v4/projects/fleetcheck/releases":
                self.send_json(200, self.server.releases)
            else:
                self.send_json(404, {"error": "not found"})
            return
        if self.path not in ("/health", "/version"):
            self.send_json(404, {"error": "not found"})
            return

        name, behavior = service["name"], service["behavior"]
        if behavior == "slow":
            time.sleep(service["delay_s"])
        elif behavior == "timeout":
            time.sleep(TIMEOUT_DELAY_S)

        if self.path == "/version":
            self.send_json(200, {"service": name, "version": service["version"]})
            return
        code = 200
        if behavior == "error":
            code = service["error_code"]
        elif behavior == "flaky":
            with self.flaky_lock:
                calls = self.flaky_calls.get(name, 0)
                self.flaky_calls[name] = calls + 1
            code = FLAKY_CYCLE[calls % len(FLAKY_CYCLE)]
        if code == 200:
            self.send_json(200, {"service": name, "status": "ok"})
        else:
            self.send_json(code, {"service": name, "status": "error", "reason": "database unreachable"})

    def do_POST(self):
        self.started = time.monotonic()
        if self.server.service is not None or self.path != "/webhook":
            self.send_json(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length))
        except ValueError:
            payload = None
        if not isinstance(payload, dict) or "content" not in payload:
            self.send_json(400, {"error": "JSON body with a 'content' key expected"})
            return
        print(f"--- webhook reçu ---\n{payload['content']}\n--------------------", flush=True)
        self.send_json(204)


def start_servers(scenario, host, base_port):
    servers = []
    targets = [(base_port, None)] + [(s["port"], s) for s in scenario["services"]]
    for port, service in targets:
        try:
            server = ThreadingHTTPServer((host, port), Handler)
        except OSError as e:
            for s in servers:
                s.server_close()
            print(f"Port {port} indisponible ({e.strerror}). Essayez --base-port 9000.", file=sys.stderr)
            sys.exit(1)
        server.service = service
        server.releases = scenario["releases"]
        servers.append(server)
    for server in servers:
        threading.Thread(target=server.serve_forever, daemon=True).start()
    return servers


def print_banner(scenario, host, base_port):
    hidden = scenario["seed"] is not None
    print(f"Plateforme  http://{host}:{base_port}  (releases, webhook)")
    for s in scenario["services"]:
        detail = "" if hidden else f"  {s['behavior']:<8} {s['version']}"
        print(f"{s['name']:<10}  http://{host}:{s['port']}{detail}")
    print(f"Port {base_port + 9} non servi (connexion refusée). Ctrl+C pour arrêter.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Serveur simulé pour fleetcheck.")
    parser.add_argument("--seed", type=int, help="scénario tiré de cette graine")
    parser.add_argument("--inventory", action="store_true", help="écrit servers.csv sur stdout et quitte")
    parser.add_argument("--scenario", action="store_true", help="écrit le scénario en JSON et quitte")
    parser.add_argument("--base-port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    if args.seed is None:
        scenario = reference_scenario(args.base_port)
    else:
        scenario = seeded_scenario(args.seed, args.base_port)
    if args.inventory:
        write_inventory(scenario, args.base_port)
        return
    if args.scenario:
        print(json.dumps(scenario, indent=2))
        return

    servers = start_servers(scenario, args.host, args.base_port)
    print_banner(scenario, args.host, args.base_port)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for server in servers:
            server.shutdown()
            server.server_close()
        print("Arrêt.")


if __name__ == "__main__":
    main()
