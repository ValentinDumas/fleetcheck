# fleetcheck

Fil rouge du cours Développement Python, 3 ESGI ALT DevOps.

`fleetcheck` lit un inventaire de serveurs (`servers.csv`), contrôle chaque service (ping, `GET /health`, version déployée), produit un rapport JSON, alerte par webhook et renvoie un code de sortie exploitable en CI.

| Chemin | Contenu |
|---|---|
| `tp/` | Guide d'installation (`tp0.1-installation.md`) et énoncés des TP, un notebook JupyterLab par TP, numéroté par chapitre (`tp0.1.ipynb`, `tp1.1.ipynb` …) : copiez-le dans votre dépôt, à côté de `fleetcheck.py` |
| `simserver.py` | Serveur simulé : `python3.14 simserver.py` (Windows : `py -3.14 simserver.py`), puis la même commande suivie de `--inventory > servers.csv` pour générer l'inventaire (PowerShell : `| Set-Content -Encoding ascii servers.csv`, voir le TP 5.1) |
| `reference/` | Version de référence, mise à jour à la fin de chaque TP (TP 1.1 au TP 6.3). Chaque version publiée porte le tag de son TP (`tp1.1` …) |

Clonez ce dépôt en premier, dans `esgi-python`, puis créez votre dépôt personnel `fleetcheck-<nom>` et clonez-le à côté (`tp/tp0.1-installation.md`, section 4). Gardez ce clone en lecture seule : on y lit, on n'y écrit jamais. Vous codez dans votre dépôt personnel, qui ne dépend plus de celui-ci, et vous y commitez étape par étape.

- **Récupérer une nouvelle version** : `git pull` dans ce clone.
- **Notebooks** : copiez-les à la main dans votre dépôt avant de les exécuter. Un notebook exécuté ou enregistré dans `tp/` modifie le clone et le `git pull` refuse de s'exécuter : `git restore .` annule ces modifications, puis relancez le `git pull`.
- **En retard** : copiez dans votre dépôt les fichiers de `reference/` dont vous avez besoin.

Consulter une version précise, dans un clone à part :

```sh
git clone https://github.com/ValentinDumas/fleetcheck.git fleetcheck-ref
cd fleetcheck-ref
git tag                    # versions publiées
git switch --detach tp2.2   # reference/ contient la correction du TP 2.2
git switch main            # dernière version publiée
```

Le tag d'un TP est aussi le point de départ du TP suivant.
