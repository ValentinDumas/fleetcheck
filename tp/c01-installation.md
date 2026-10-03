# C1 — Installation et premier script

À faire avant le lun 12/10 avec le guide ci-dessous. En salle, les 40 min du TP servent à vérifier et à réparer.

Commandes données pour macOS et Linux. Sous Windows : `py` à la place de `python3`, `dir` à la place de `ls`.

## Guide d'installation

| Étape | macOS / Linux | Windows | Vérification |
|---|---|---|---|
| Python ≥ 3.10 | `python3 --version` ; sinon python.org ou gestionnaire de paquets | python.org, cocher « Add to PATH » | `python3 --version` (Windows : `py --version`) affiche 3.10 ou plus |
| Éditeur | VS Code + extension Python, ou PyCharm | idem | Un fichier `.py` est coloré, l'interpréteur est détecté |
| git | `git --version` | Git for Windows | Version affichée |
| Dépôt personnel | `fleetcheck-<nom>` sur GitHub ou GitLab | idem | Premier commit poussé |
| Dépôt public du cours | `git clone https://github.com/ValentinDumas/fleetcheck.git` | idem | `simserver.py` présent |

Sous macOS, le `python3` fourni avec les outils en ligne de commande d'Apple peut être en 3.9 : installer alors Python depuis python.org.

## TP en salle

| Fin | Étape | Vérification |
|---|---|---|
| 09:00 | 1. Python, éditeur et git vérifiés. Main levée si une commande échoue. | `python3 --version` affiche 3.10 ou plus ; `git --version` affiche une version |
| 09:15 | 2. Dépôt personnel `fleetcheck-<nom>` créé sur GitHub ou GitLab et cloné ; dépôt public `fleetcheck` cloné à côté, dans le même dossier parent | `ls fleetcheck/simserver.py` trouve le fichier |
| 09:25 | 3. `hello.py` dans le dépôt personnel : il affiche `platform.system()` puis `sys.version`. Commit et push | `python3 hello.py` affiche deux lignes ; `git log --oneline -1` montre le commit |
| 09:30 | 4. Bilan collectif | Votre `hello.py` est poussé, ou vous avez un binôme nommé pour C2 |

À 09:15, si Python ne se lance pas encore sur votre poste : vous travaillez en binôme avec un voisin équipé pendant C2, et votre installation se règle pendant le TP de C2.

### `hello.py`

```python
import platform
import sys

print(platform.system())
print(sys.version)
```

Sortie attendue : le système (`Darwin`, `Linux` ou `Windows`), puis une version qui commence par `3.10` ou plus. Exemple sous macOS :

```text
Darwin
3.14.4 (main, Apr  7 2026, 13:13:20) [Clang 21.0.0 (clang-2100.0.123.102)]
```

Ne travaillez jamais dans le clone du dépôt public : un `git pull` y écraserait votre code.

## Pour aller plus loin

Lancer `python3 simserver.py` dans le clone du dépôt public, puis ouvrir `http://127.0.0.1:8001/health` dans le navigateur : premier contact avec le serveur du chapitre 5.
