# C6 — Logging et codes de sortie (v0.5)

Mar 13/10, TP de 12:00 à 12:25. Correction à 12:25, TP fini ou non. À 12:30, écrans fermés : QCM papier de révision. La référence v0.5 est publiée à 13:00.

Commandes données pour macOS et Linux. Sous Windows (PowerShell) : `py` pour `python3`, `$LASTEXITCODE` pour `$?`, `$null` pour `/dev/null`.

## Objectif

`fleetcheck` devient utilisable en CI :

- le journal (lignes ignorées, erreurs) passe par `logging` sur stderr, et stdout ne contient plus que le résultat ;
- `-v` et `-vv` règlent la quantité de journal ;
- le code de sortie dit si le contrôle est fiable : `0` succès, `1` panne détectée, `2` erreur fatale ou ligne d'inventaire invalide.

## Point de départ

Votre `fleetcheck.py` de v0.4, avec `config.json`, `servers.csv` et `servers-broken.csv` dans le même dossier.

En retard ou en panne : copiez dans votre dépôt les fichiers de `reference/` au tag `v0.4` du dépôt public (`git switch --detach v0.4` dans votre clone de consultation, voir le `README.md` à la racine).

Vérifiez avant de commencer :

```sh
python3 fleetcheck.py --env staging
```

```
2 serveurs valides, 0 invalides
par env : staging 2
par rôle : web 1, api 1
prod/web : 
```

## Étapes

| Fin | Étape | Vérification |
|---|---|---|
| 12:08 | 1. Remplacer les `print` d'erreur par `logging` sur stderr : `WARNING` pour une ligne invalide, `ERROR` pour une erreur fatale. `-v` passe en `INFO`, `-vv` en `DEBUG` | `python3 fleetcheck.py --inventory servers-broken.csv 2>/dev/null` n'affiche plus aucune ligne `invalide` ; sans `2>/dev/null`, les 3 lignes `WARNING` attendues apparaissent |
| 12:15 | 2. Fonction `exit_code(statuses, invalid_count)` | `python3 -c "from fleetcheck import exit_code; print(exit_code(['ok', 'down'], 0), exit_code(['ok'], 1), exit_code([], 0))"` affiche `1 2 0` |
| 12:25 | 3. Erreurs fatales en `ERROR` et code `2` ; code de sortie final calculé par `exit_code` | Les 4 commandes du critère final |

À 12:15, si plus d'un tiers de la salle n'a pas `exit_code`, l'enseignant l'écrit au tableau et `-vv` passe en « pour aller plus loin ».

### Étape 1 — logging sur stderr

- Un logger nommé `fleetcheck`, configuré une seule fois au début de `main()` : format `%(levelname)s %(message)s`, sortie stderr.
- Une ligne invalide donne un `WARNING` de la forme `ligne N ignorée : <erreur>`. Les lignes `invalide ligne N : ...` du résumé disparaissent : le résumé ne garde que ses 4 lignes.
- Les messages d'erreur fatale de v0.4 (`print` suivi de `sys.exit`) deviennent des `ERROR`. Le code de sortie change à l'étape 3.
- Option `-v` / `--verbose`, répétable : niveau `WARNING` sans option, `INFO` avec `-v`, `DEBUG` avec `-vv`.
- Les arguments du message sont passés séparément (`log.warning("ligne %d ignorée : %s", line, e)`), pas en f-string.

Log attendu sur stderr :

```sh
python3 fleetcheck.py --inventory servers-broken.csv > /dev/null
```

```
WARNING ligne 4 ignorée : port non entier : 'abc'
WARNING ligne 8 ignorée : IP invalide : '300.0.0.1'
WARNING ligne 12 ignorée : 3 champs au lieu de 5
```

Sortie standard seule :

```sh
python3 fleetcheck.py --inventory servers-broken.csv 2>/dev/null
```

```
9 serveurs valides, 3 invalides
par env : prod 7, staging 2
par rôle : web 3, api 3, worker 1, cache 1, db 1
prod/web : web-1, web-2
```

Sans option, un run sur `servers.csv` n'écrit rien sur stderr. Avec `-v`, la référence écrit :

```
INFO 9 serveur(s) valide(s), 0 ligne(s) invalide(s) dans servers.csv
INFO rapport écrit : report.json
```

Le texte exact des messages `INFO` et `DEBUG` est libre ; seul leur niveau compte.

### Étape 2 — `exit_code`

`exit_code(statuses, invalid_count)` reçoit une liste de statuts de services (`"ok"`, `"degraded"`, `"down"`) et le nombre de lignes invalides. Elle renvoie :

| Condition, évaluée dans l'ordre | Code |
|---|---|
| `invalid_count` non nul | `2` |
| au moins un statut `down` | `1` |
| sinon | `0` |

La fonction est pure : ni `print`, ni `sys.exit`, ni lecture de fichier. Aucun service n'est encore contrôlé (le contrôle réseau arrive en C9) : `main()` l'appelle avec une liste vide.

### Étape 3 — codes de sortie

Erreurs fatales : log `ERROR`, puis `sys.exit(2)`, sans écrire `report.json`.

| Cas | Message de la référence |
|---|---|
| Inventaire absent | `ERROR inventaire illisible : [Errno 2] No such file or directory: 'nope.csv'` |
| Config absente ou JSON invalide | `ERROR config illisible (config.json) : ...` |
| Aucune ligne valide dans l'inventaire | `ERROR aucune ligne valide dans <fichier>` |
| `--env` ne garde aucun serveur | `ERROR aucun serveur pour --env <valeur>` |

Fin de `main()` : `sys.exit(exit_code([], len(invalid)))`. Une ligne invalide donne donc `2`, mais le rapport est écrit et le résumé affiché : les serveurs valides restent traités.

## Critère final

```sh
python3 fleetcheck.py > /dev/null; echo $?
python3 fleetcheck.py --inventory servers-broken.csv > /dev/null; echo $?
python3 fleetcheck.py --env prd; echo $?
python3 fleetcheck.py --format json 2>/dev/null | python3 -m json.tool > /dev/null && echo OK
```

Sortie attendue, commande par commande :

```
0
```

```
WARNING ligne 4 ignorée : port non entier : 'abc'
WARNING ligne 8 ignorée : IP invalide : '300.0.0.1'
WARNING ligne 12 ignorée : 3 champs au lieu de 5
2
```

```
ERROR aucun serveur pour --env prd
2
```

```
OK
```

En v0.4, `--env prd` affichait `0 serveurs valides, 0 invalides` et sortait en `0` : une faute de frappe dans un job de CI laissait le pipeline vert sans rien contrôler.

## Pour aller plus loin

- `-vv` (niveau `DEBUG`), si le point de contrôle de 12:15 l'a retiré du socle. Exemple de la référence, une ligne par ligne d'inventaire lue :

```sh
python3 fleetcheck.py -vv > /dev/null
```

```
DEBUG ligne 2 valide : web-1
DEBUG ligne 3 valide : web-2
...
DEBUG ligne 10 valide : db-1
INFO 9 serveur(s) valide(s), 0 ligne(s) invalide(s) dans servers.csv
INFO rapport écrit : report.json
```

- Étape 3 non finie à 12:25 : terminez-la chez vous à partir de la référence v0.5, publiée à 13:00.
