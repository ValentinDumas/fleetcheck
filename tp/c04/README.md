# TP C4 — v0.3 : `config.json` et `report.json`

Mar 13/10, 08:30–09:20. Correction à 09:20, TP fini ou non. Référence v0.3 publiée à 09:30.

## Objectif

`fleetcheck` charge sa configuration depuis `config.json` et écrit son résultat dans `report.json`, lisible par `jq` ou un autre script. Une config absente ou mal formée arrête le script avec un message d'une ligne et le code `1`, sans trace Python.

## Point de départ

Votre `fleetcheck.py` de fin de C3 (v0.2). En retard : copiez `reference/fleetcheck.py` du dépôt public, à la version `v0.2`.

Le résumé texte de v0.2 ne change pas : `print` reste sur l'écran, le rapport s'ajoute.

Sous Windows : `py` pour `python3`, `$LASTEXITCODE` pour `$?`.

## Étapes

### 1. Créer `config.json` — fin 08:35

À côté de `fleetcheck.py`, créez `config.json` avec ce contenu :

```json
{
  "timeout_s": 2,
  "attempts": 3,
  "backoff_s": 0.5,
  "degraded_s": 1.0,
  "ping_timeout_s": 1,
  "drift_envs": ["prod"],
  "releases_url": "http://127.0.0.1:8000/api/v4/projects/fleetcheck/releases",
  "reports_dir": "reports",
  "archive_after_days": 7
}
```

Les clés serviront de C8 à C11. En v0.3, on vérifie seulement que le fichier se charge.

Vérification :

```sh
python3 -m json.tool config.json
```

Le JSON est réaffiché, sans erreur.

### 2. `load_config(path)` — fin 08:50

Écrivez `load_config(path)` :

- elle renvoie le dict lu dans le fichier ;
- si le fichier manque ou si le JSON est faux, elle affiche avec `print` une ligne `config illisible (<path>) : <détail de l'erreur>`, puis arrête le script avec `sys.exit(1)`.

Appelez-la au début du script avec `"config.json"`.

Vérification : renommez `config.json` en `config.bak`, puis :

```sh
python3 fleetcheck.py; echo $?
```

Sortie attendue, sans trace Python :

```
config illisible (config.json) : [Errno 2] No such file or directory: 'config.json'
1
```

Remettez le nom `config.json`.

Si `load_config` ne marche toujours pas à 08:50 : chargez la config avec `json.load` sans gestion d'erreur et passez à l'étape 3. Le rapport compte plus que le message d'erreur.

### 3. Écrire `report.json` — fin 09:10

À chaque exécution, le script écrit `report.json` à la racine, au format suivant (extrait : 1 service et 1 invalide montrés) :

```json
{
  "generated_at": "2026-10-13T08:52:10+02:00",
  "summary": {"total": 9, "invalid": 2},
  "services": [{"name": "web-1", "env": "prod", "ip": "127.0.0.1", "port": 8001, "role": "web"}],
  "invalid_lines": [{"name": "api-3", "error": "port non entier : 'abc'"}]
}
```

- `services` : les serveurs valides, tels que `load` les renvoie (port en entier).
- `invalid_lines` : les invalides collectés par `load`.
- `summary` : `total` est le nombre de serveurs valides, `invalid` le nombre d'invalides.
- `generated_at` s'obtient avec cette ligne, après `from datetime import datetime` :

```python
datetime.now().astimezone().isoformat(timespec="seconds")
```

Le fichier doit rester lisible : indentation de 2 espaces, accents écrits tels quels.

Vérification :

```sh
python3 -m json.tool report.json
```

Le fichier est relu sans erreur. Début de la sortie (la date est celle de votre exécution) :

```
{
    "generated_at": "2026-10-13T08:52:10+02:00",
    "summary": {
        "total": 9,
        "invalid": 2
    },
```

### 4. Config cassée — fin 09:20

Ajoutez une virgule après la dernière valeur de `config.json` (`"archive_after_days": 7,`), puis :

```sh
python3 fleetcheck.py; echo $?
```

Une seule ligne qui commence par `config illisible (config.json) :`, pas de trace, puis `1`. Le détail dépend de la version de Python :

```
config illisible (config.json) : Illegal trailing comma before end of object: line 10 column 26 (char 259)
1
```

Avant Python 3.13, le détail est `Expecting property name enclosed in double quotes: ...`.

Réparez `config.json`. `python3 fleetcheck.py` redonne la sortie de v0.2 :

```
9 serveurs valides, 2 invalides
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
invalide api-3 : port non entier : 'abc'
invalide web-3 : IP invalide : '300.0.0.1'
```

## À éviter

- `json.dump` hors d'un `with` : fichier vide si le script plante avant la fermeture.
- Lancer le script depuis un autre dossier : `config.json` est cherché dans le dossier courant, pas à côté du script. Notez-le, la réponse vient en C13.
- `except Exception` autour du chargement : il cache aussi une faute de frappe dans votre code.

## Pour aller plus loin

- Refuser une config à laquelle manque une clé attendue.
- Écrire le rapport dans `Path(config["reports_dir"]) / "report.json"`, en créant le dossier s'il n'existe pas.
