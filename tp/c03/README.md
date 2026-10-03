# TP C3 — v0.2 : valider et collecter les erreurs

Lun 12/10, 12:00–12:50. Correction commentée à 12:50, TP fini ou non.

## Objectif

Valider chaque serveur du parc, lever une exception métier `InvalidServer` avec un message qui dit quoi corriger, et ranger les serveurs en valides et invalides au lieu de s'arrêter au premier serveur faux. Le résumé de v0.1 ne porte plus que sur les valides.

## Point de départ

Votre `fleetcheck.py` de v0.1. Sinon, `reference/fleetcheck.py` du tag `v0.1` du dépôt public.

## Étapes

### 1. Le nouveau parc et l'exception — fin 12:05

Remplacez `SERVERS` par la liste ci-dessous. Les ports sont maintenant des chaînes, comme ils sortiront du CSV en C5, et deux lignes fausses sont ajoutées à la fin.

```python
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
```

Écrivez la classe `InvalidServer`, sous-classe d'`Exception`.

Vérification :

```text
$ python3 -i fleetcheck.py
>>> len(SERVERS)
11
```

### 2. `validate(server)` — fin 12:25

`validate(server)` renvoie un **nouveau** dict, identique au serveur reçu sauf `port` converti en `int`. Si le serveur est faux, elle lève `InvalidServer`. Règles, contrôlées dans cet ordre :

| Règle | Message de l'exception |
|---|---|
| Port non entier | `port non entier : 'abc'` |
| Port hors de 1–65535 | `port hors de 1-65535 : 70000` |
| IP invalide (`ipaddress.ip_address`) | `IP invalide : '300.0.0.1'` |
| Champ `name`, `env` ou `role` vide | `champ 'env' vide` |

La règle « champ vide » peut passer en « pour aller plus loin » à 12:25, sur annonce de l'enseignant. La sortie attendue de l'étape 4 n'en dépend pas.

Vérification, dans `python3 -i fleetcheck.py` :

```text
>>> validate(SERVERS[0])['port'] + 1
8002
>>> validate(SERVERS[9])
Traceback (most recent call last):
  ...
InvalidServer: port non entier : 'abc'
```

### 3. `load(raw_servers)` — fin 12:40

`load(raw_servers)` valide chaque serveur et renvoie le tuple `(valides, invalides)`. `valides` est la liste des dicts renvoyés par `validate`. Chaque invalide est un dict `{"name": ..., "error": ...}`, où `error` est le message de l'exception. Un serveur faux n'arrête pas les suivants.

Vérification, dans `python3 -i fleetcheck.py` :

```text
>>> [len(x) for x in load(SERVERS)]
[9, 2]
```

### 4. Résumé — fin 12:50

Le résumé de v0.1 porte sur les serveurs valides seulement, puis une ligne par invalide.

Vérification : `python3 fleetcheck.py` affiche exactement :

```text
9 serveurs valides, 2 invalides
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
invalide api-3 : port non entier : 'abc'
invalide web-3 : IP invalide : '300.0.0.1'
```

C'est le critère de fin du TP.

## Pour aller plus loin

Non corrigé en salle. Aucune ligne fournie n'est concernée : la sortie attendue ne change pas. Testez en ajoutant vos propres lignes fausses.

- Refuser un `env` hors de `{"prod", "staging", "dev"}`.
- Refuser deux serveurs de même nom.

## En retard

La version de référence v0.2 est publiée dans `reference/` à la fin du créneau. Elle sert de point de départ en C4.
