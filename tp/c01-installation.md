# Installation

À faire avant le lun 12/10, chez vous : l'installation télécharge environ 226 Mo. En salle, les 40 min du TP servent à vérifier et à réparer, avec le notebook `tp/c01.ipynb`.

Tout le monde installe la même version, Python 3.14, depuis python.org : les messages d'erreur montrés en cours sont ceux de 3.14, et JupyterLab s'installe de la même façon sur chaque système.

## 1. Python 3.14

| Système | Installation | Vérification |
|---|---|---|
| Windows | Installeur de https://www.python.org/downloads/ ; cocher « Add python.exe to PATH » | `py -3.14 --version` |
| macOS | Installeur `.pkg` de https://www.python.org/downloads/ | `python3.14 --version` |
| Linux | python.org ne fournit pas d'installeur : paquet `python3.14` de la distribution (Ubuntu : PPA deadsnakes, avec `python3.14-venv`) | `python3.14 --version` |

La vérification affiche `Python 3.14.x`. Sous macOS, `python3` peut encore désigner le Python 3.9 d'Apple : utilisez `python3.14`.

## 2. git

`git --version` affiche une version. Sinon : Git for Windows sous Windows, `xcode-select --install` sous macOS, paquet `git` sous Linux.

## 3. Dossier de travail et JupyterLab

Un dossier `esgi-python` contient l'environnement virtuel (`.venv`) et, plus tard, vos dépôts. Dans un terminal (PowerShell sous Windows) :

| Étape | macOS / Linux | Windows |
|---|---|---|
| Dossier | `mkdir esgi-python` puis `cd esgi-python` | idem |
| Environnement virtuel | `python3.14 -m venv .venv` | `py -3.14 -m venv .venv` |
| JupyterLab | `.venv/bin/python -m pip install jupyterlab` | `.venv\Scripts\python -m pip install jupyterlab` |
| Lancement | `.venv/bin/python -m jupyter lab` | `.venv\Scripts\python -m jupyter lab` |

Pas besoin d'activer l'environnement : on appelle directement son `python`. Le lancement ouvre JupyterLab dans le navigateur, sur `http://localhost:8888`. Il s'arrête par Ctrl+C dans le terminal. Le venv sera expliqué en séance v0.6 (mar 10/11).

Vérification : dans JupyterLab, *File > New > Notebook*, noyau *Python 3*, puis une cellule :

```python
import sys
print(sys.version)
print(sys.prefix)
```

La première ligne commence par `3.14`, la seconde finit par `.venv`.

## 4. Dépôts

Dans le terminal de JupyterLab (*File > New > Terminal*), depuis `esgi-python` :

| Étape | Commande | Vérification |
|---|---|---|
| Dépôt personnel | Créer `fleetcheck-<nom>` sur GitHub ou GitLab, puis `git clone <url>` | Le dossier apparaît dans JupyterLab |
| Dépôt public du cours | `git clone https://github.com/ValentinDumas/fleetcheck.git` | `fleetcheck/simserver.py` présent |

Le dépôt public est en lecture seule : ne codez jamais dedans, et copiez les notebooks dans votre dépôt avant de les exécuter. Pour récupérer les nouvelles versions, lancez `git pull` dans `fleetcheck/` ; s'il refuse à cause de modifications locales, `git restore .` puis relancez-le.

Arborescence attendue :

```text
esgi-python/
├── .venv/
├── fleetcheck/           dépôt public : énoncés (tp/), simserver.py, reference/
└── fleetcheck-<nom>/     votre dépôt : fleetcheck.py et vos notebooks rendus
```

## Éditeur

JupyterLab suffit : il ouvre les notebooks, édite `fleetcheck.py` dans un onglet et fournit le terminal. VS Code ou PyCharm restent possibles si vous les connaissez déjà, à condition d'utiliser le Python de `.venv`.
