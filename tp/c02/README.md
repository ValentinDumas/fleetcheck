# TP C2 — v0.1 : le parc en liste de dicts

Lun 12/10, 10:15–11:05. Correction commentée à 11:05, TP fini ou non.

## Objectif

Un seul fichier `fleetcheck.py` qui décrit le parc de serveurs en liste de dicts, le filtre par environnement et par rôle, compte les serveurs par clé et affiche un résumé.

## Point de départ

Un fichier `fleetcheck.py` vide dans votre dépôt personnel.

Contraintes :

- Les fonctions **renvoient** leur résultat (`return`). Seul le bloc principal affiche (`print`).
- Le bloc principal reste au niveau du module, sans `if __name__ == "__main__":` (vu en C5).
- Un dict garde l'ordre d'insertion : les comptes s'affichent dans l'ordre de première apparition des valeurs.

## Étapes

### 1. Le parc — fin 10:20

Copiez cette liste en tête de `fleetcheck.py`. Ne la retapez pas. Ce sont les serveurs de `tp/servers.csv`.

```python
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
```

Vérification :

```text
$ python3 -i fleetcheck.py
>>> len(SERVERS)
9
```

### 2. Filtres — fin 10:35

`by_env(servers, env)` renvoie la liste des serveurs de l'environnement `env`. `by_role(servers, role)` renvoie la liste des serveurs du rôle `role`. Ni l'une ni l'autre ne modifie la liste reçue.

Vérification, dans `python3 -i fleetcheck.py` :

```text
>>> len(by_env(SERVERS, 'prod')), len(by_role(SERVERS, 'api'))
(7, 3)
```

### 3. Comptage — fin 10:50

`count_by(servers, key)` renvoie un dict `{valeur: nombre de serveurs}` pour la clé `key` (`'env'`, `'role'`…).

Vérification, dans `python3 -i fleetcheck.py` :

```text
>>> count_by(SERVERS, 'env')
{'prod': 7, 'staging': 2}
```

### 4. Résumé — fin 11:05

Le bloc principal affiche le nombre de serveurs, les comptes par env et par rôle, puis les noms des serveurs à la fois `prod` et `web`.

Vérification : `python3 fleetcheck.py` affiche exactement :

```text
9 serveurs
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
```

C'est le critère de fin du TP.

## Pour aller plus loin

Non corrigé en salle.

- `count_by` écrit avec `collections.Counter`. Le résultat compare égal à l'ancien : `count_by(SERVERS, 'env') == {'prod': 7, 'staging': 2}` affiche `True`.
- Les serveurs triés par port : le premier est `db-1` (5432), le deuxième `web-1` (8001).
- `find(servers, name)` renvoie le serveur de ce nom, ou `None` s'il n'existe pas : `find(SERVERS, 'db-1')['ip']` affiche `'192.0.2.1'`, `find(SERVERS, 'nope') is None` affiche `True`.

## En retard

La version de référence v0.1 est publiée dans `reference/` à la fin du créneau. Copiez-la dans votre dépôt pour démarrer le TP C3.
