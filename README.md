# JARVIS F1 Desktop

Version fiable de l'application native multi-mode. Elle n'ouvre pas un navigateur : PyQt5 affiche le HUD dans une fenêtre desktop.

## Installation

### Windows
Double-cliquer sur `installer_windows.bat`.

### macOS / Linux
```bash
chmod +x installer_unix.sh
./installer_unix.sh
```

Python 3.9+ est requis. Le script crée un environnement `.venv` et installe les dépendances sans modifier l'installation globale de Python.

## Modes

- Normal / Dev
- F1 Engineer
- Discrete
- Background
- Architect
- Crisis Diagnostic
- Executive

Le sélecteur en haut de la fenêtre recharge un HUD différent pour chaque mode. Le mode F1 écoute les paquets UDP sur `0.0.0.0:20777` et indique le nombre de paquets reçus. Le décodage détaillé dépend du format/version du jeu et sera ajouté dans un adaptateur dédié.

## Configuration IA

Le bouton `AI CONFIG` permet de définir le fournisseur, une clé principale, des clés de secours et le routage. La configuration est enregistrée dans `~/.jarvis-f1/config.json`; les clés ne sont jamais injectées dans le HTML du dashboard. Ne partage jamais ce fichier.

## Dépannage

- Si Qt ne démarre pas sous Linux, installe les bibliothèques système Qt/WebEngine de ta distribution.
- Si le port 20777 est occupé, ferme l'autre écouteur ou modifie le port dans `app.py`.
- Le jeu doit être configuré pour envoyer la télémétrie UDP vers l'adresse de la machine et le port `20777`.
