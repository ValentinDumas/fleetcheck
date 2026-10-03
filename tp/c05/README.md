# TP C5 — v0.4 : inventaire CSV et ligne de commande

Mar 13/10, en deux parties :

| Horaire | Contenu |
|---|---|
| 10:00–10:25 | Partie 1 : inventaire CSV |
| 10:25–10:30 | Correction de la partie 1 |
| 10:45–11:10 | Partie 2 : ligne de commande |
| 11:10–11:15 | Correction de la partie 2, puis publication de la référence v0.4 |

Chaque correction commence à l'heure, partie finie ou non.

## Objectif

`servers.csv` remplace la liste `SERVERS` écrite dans le code. Chaque ligne fausse est notée avec son numéro de ligne, sans arrêter le script. Puis `fleetcheck` devient une commande : `--inventory`, `--env`, `--format`.

## Point de départ

Votre `fleetcheck.py` de fin de C4 (v0.3), avec `config.json`. En retard : copiez `reference/fleetcheck.py` et `reference/config.json` du dépôt public, à la version `v0.3`.

Sous Windows : `py` pour `python3`, `$LASTEXITCODE` pour `$?`, `$null` pour `/dev/null`.

## Partie 1 — inventaire CSV

Pendant cette partie, le fichier lu est fixé par une constante en tête de script :

```python
INVENTORY = "servers.csv"
```

La partie 2 la remplace par l'option `--inventory`.

### 1. Les deux inventaires — fin 10:05

```sh
python3 simserver.py --inventory > servers.csv
```

Copiez aussi `tp/servers-broken.csv` à côté de `fleetcheck.py`. Ouvrez les deux fichiers et lisez l'en-tête.

Sous Windows PowerShell 5, `>` écrit de l'UTF-16 : copiez `tp/servers.csv` (même contenu) au lieu de lancer la commande.

Vérification : l'en-tête de `servers.csv` est `name,env,ip,port,role`, suivi de 9 lignes de données. `servers-broken.csv` contient les mêmes 9 serveurs plus 3 lignes fausses : port `abc` en ligne 4, IP `300.0.0.1` en ligne 8, ligne à 3 champs en ligne 12.

### 2. `load(path)` — fin 10:20

`load(path)` remplace la liste `SERVERS` et la `load` de C3. Elle renvoie toujours `servers, invalid`.

- Lire le fichier avec `csv.reader`.
- Vérifier l'en-tête : `name,env,ip,port,role`.
- Pour chaque ligne de données, numérotée comme dans l'éditeur (l'en-tête est la ligne 1) :
  - vérifier le nombre de champs ;
  - construire le dict avec `dict(zip(HEADER, row))`, où `HEADER` est la liste des 5 colonnes ;
  - le passer à `validate` de C3, **sans la modifier**.
- Chaque ligne invalide devient un dict au format suivant :

```python
{"line": 4, "raw": "api-3,prod,127.0.0.1,abc,api", "error": "port non entier : 'abc'"}
```

`raw` est la ligne telle qu'elle est dans le fichier. Une ligne à 3 champs a pour erreur `3 champs au lieu de 5`.

Le résumé texte cite désormais la ligne et non plus le nom (une ligne à 3 champs n'a pas de nom fiable) : `invalide ligne <n> : <erreur>`. `report.json` suit : `invalid_lines` passe au format ci-dessus.

Vérification avec `INVENTORY = "servers.csv"` :

```sh
python3 fleetcheck.py
```

```
9 serveurs valides, 0 invalides
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
```

Avec `INVENTORY = "servers-broken.csv"` :

```
9 serveurs valides, 3 invalides
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
invalide ligne 4 : port non entier : 'abc'
invalide ligne 8 : IP invalide : '300.0.0.1'
invalide ligne 12 : 3 champs au lieu de 5
```

« invalides » reste au pluriel à 0 : c'est le comportement de la référence.

### 3. Cas fatals — fin 10:25

Trois cas arrêtent le script avec un message d'une ligne et `sys.exit(1)`, comme `load_config` :

| Cas | Message |
|---|---|
| Fichier absent | `inventaire illisible : <détail de l'erreur>` |
| En-tête absent ou faux | `en-tête attendu dans <fichier> : name,env,ip,port,role` |
| Aucune ligne valide | `aucune ligne valide dans <fichier>` |

Vérification avec `INVENTORY = "absent.csv"` :

```sh
python3 fleetcheck.py; echo $?
```

```
inventaire illisible : [Errno 2] No such file or directory: 'absent.csv'
1
```

Pas de trace Python. Remettez `INVENTORY = "servers.csv"`.

Si votre `load` ne renvoie pas les 9 valides de `servers.csv` à 10:15, terminez l'étape 2 jusqu'à 10:25 ; l'étape 3 se fait alors à la maison, à partir de la référence.

### Avant 10:45

La `load` corrigée est publiée à 10:25 dans `tp/c05/load.py`. Si la vôtre ne donne pas les sorties ci-dessus, collez ce fichier dans `fleetcheck.py` à la place de votre `load` avant 10:45 : la partie 2 en dépend.

### À éviter

- Ouvrir le CSV sans `newline=""` : lignes vides intercalées sous Windows à l'écriture.
- Compter les lignes à partir de 0, ou sans l'en-tête : le numéro ne correspond plus à l'éditeur.
- Recopier `validate` au lieu de la réutiliser.

## Partie 2 — ligne de commande

### 1. `main()` et le parser — fin 10:55

Écrivez `main()` avec un parser `argparse` à 3 options :

| Option | Valeur |
|---|---|
| `--inventory` | fichier CSV, défaut `servers.csv` |
| `--env` | facultatif, un environnement |
| `--format` | `text` (défaut) ou `json`, rien d'autre |

Chaque option a un `help`. La constante `INVENTORY` disparaît. Le script appelle `main()` sous `if __name__ == "__main__":`.

Vérification :

```sh
python3 fleetcheck.py --help
```

L'aide liste `--inventory`, `--env` et `--format`.

### 2. `--env` — fin 11:02

`--env` filtre les serveurs valides avant le résumé et le rapport. Sans `--env`, rien ne change.

Vérification :

```sh
python3 fleetcheck.py --env staging
```

```
2 serveurs valides, 0 invalides
par env : staging 2
par rôle : web 1, api 1
prod/web : 
```

La dernière ligne s'arrête après `prod/web : ` : aucun serveur `prod` ne reste après le filtre.

### 3. `--format json` — fin 11:10

`--format json` affiche le contenu du rapport sur stdout, avec `json.dumps(report, indent=2, ensure_ascii=False)`. `--format text` garde le résumé. `report.json` est écrit dans les deux cas.

Vérification :

```sh
python3 fleetcheck.py --format json | python3 -m json.tool > /dev/null && echo OK
python3 fleetcheck.py --format xml; echo $?
```

La première commande affiche `OK`. La seconde affiche l'usage puis une erreur argparse, et le code `2` :

```
fleetcheck.py: error: argument --format: invalid choice: 'xml' (choose from text, json)
2
```

Selon la version de Python, les choix s'affichent avec ou sans guillemets (`'text', 'json'`).

Enfin, `python3 fleetcheck.py --inventory servers-broken.csv` redonne la sortie attendue de la partie 1.

### À observer

`python3 fleetcheck.py --env prd` (faute de frappe) affiche `0 serveurs valides, 0 invalides` et sort en `0` : une CI serait verte sans avoir rien contrôlé. v0.5 corrige ce défaut en C6.
