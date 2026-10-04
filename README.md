# fleetcheck

Fil rouge du cours Développement Python, 3 ESGI ALT DevOps.

`fleetcheck` lit un inventaire de serveurs (`servers.csv`), contrôle chaque service (ping, `GET /health`, version déployée), produit un rapport JSON, alerte par webhook et renvoie un code de sortie exploitable en CI.

| Chemin | Contenu |
|---|---|
| `tp/` | Guide d'installation (`c01-installation.md`) et énoncés des TP, un notebook JupyterLab par créneau (`c01.ipynb` …) : copiez-le dans votre dépôt, à côté de `fleetcheck.py` |
| `simserver.py` | Serveur simulé : `python3 simserver.py`, puis `python3 simserver.py --inventory` pour générer `servers.csv` |
| `reference/` | Version de référence, mise à jour à la fin de chaque créneau (v0.1 à v1.0). Chaque version publiée porte un tag |

Travaillez dans votre propre dépôt : un `git pull` de celui-ci écraserait votre code. En cas de retard, copiez les fichiers de `reference/` dont vous avez besoin.

Consulter une version précise, dans un clone à part :

```sh
git clone https://github.com/ValentinDumas/fleetcheck.git fleetcheck-ref
cd fleetcheck-ref
git tag                    # versions publiées
git switch --detach v0.4   # reference/ contient la correction de fin de C5
git switch main            # dernière version publiée
```

Le tag d'un créneau est aussi le point de départ du TP suivant.
