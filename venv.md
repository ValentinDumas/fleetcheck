# Environnement virtuel (venv) : aide-mémoire

Un environnement virtuel est un dossier, `.venv`, qui contient son propre Python et ses propres paquets : ce qu'on y installe ne touche ni le Python du système ni les autres projets. Dans ce cours, il n'y en a qu'un, `esgi-python/.venv`, créé au TP 0.1 et partagé par `fleetcheck` et votre dépôt.

Prérequis : Python 3.14 installé (`python3.14 --version` sous macOS et Linux, `py -3.14 --version` sous Windows). Toutes les commandes se tapent dans un terminal (PowerShell sous Windows, ou le terminal de JupyterLab), **depuis le dossier `esgi-python`**.

## Commandes

| Étape | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Aller dans le dossier | `cd esgi-python` | `cd esgi-python` |
| Créer le venv (une fois) | `python3.14 -m venv .venv` | `py -3.14 -m venv .venv` |
| Installer un paquet | `.venv/bin/python -m pip install requests==2.34.2` | `.venv\Scripts\python -m pip install requests==2.34.2` |
| Installer les dépendances d'un projet | `.venv/bin/python -m pip install -r requirements.txt` | `.venv\Scripts\python -m pip install -r requirements.txt` |
| Lancer un script | `.venv/bin/python script.py` | `.venv\Scripts\python script.py` |
| Lancer JupyterLab | `.venv/bin/python -m jupyter lab` | `.venv\Scripts\python -m jupyter lab` |
| Lister les paquets installés | `.venv/bin/python -m pip freeze` | `.venv\Scripts\python -m pip freeze` |

Pas besoin d'activer le venv : appeler directement son `python` suffit. Dans un notebook lancé par ce JupyterLab, `%pip install <paquet>` installe dans le venv.

## Activer le venv (facultatif)

Activer permet de taper `python` et `pip` au lieu du chemin complet, jusqu'à la fermeture du terminal.

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Activer | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| Désactiver | `deactivate` | `deactivate` |

Le prompt affiche alors `(.venv)`.

## Vérifier quel Python tourne

Dans un notebook ou dans `python` :

```python
import sys
print(sys.executable)                 # chemin sous esgi-python/.venv
print(sys.prefix != sys.base_prefix)  # True : on est dans le venv
```

## Pannes courantes

| Symptôme | Cause | Réparation |
|---|---|---|
| `ModuleNotFoundError` alors que le paquet est installé | Installé dans un autre Python que celui qui exécute | Réinstaller avec `.venv/bin/python -m pip install …` (Windows : `.venv\Scripts\python …`), ou `%pip install …` dans le notebook |
| `python3 --version` affiche 3.9 (macOS) | `python3` désigne le Python d'Apple | Utiliser `python3.14` |
| `ensurepip is not available` (Linux) | Module venv absent | `sudo apt install python3.14-venv`, puis recréer le venv |
| `Activate.ps1 … cannot be loaded because running scripts is disabled` (Windows) | Politique d'exécution de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou ne pas activer et appeler `.venv\Scripts\python` |
| `No such file or directory: .venv/bin/python` | Terminal ouvert ailleurs que dans `esgi-python` | `cd esgi-python`, puis relancer |
| Venv cassé (Python réinstallé, dossier déplacé) | `.venv` pointe vers un Python qui n'existe plus | Supprimer `.venv`, le recréer, réinstaller JupyterLab (`… -m pip install jupyterlab`) et les dépendances (`… -m pip install -r requirements.txt`) |

`.venv/` ne se commite jamais : il se recrée à partir de `requirements.txt`. Dans un dépôt qui le contient, ajoutez la ligne `.venv/` au `.gitignore`.
