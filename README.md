# JARVIS F1 Desktop

Version desktop native multi-mode. La télémétrie F1 25 est écoutée sur UDP `20777`.

## Installation

### Windows
Double-cliquez sur `installer_windows.bat`.

### macOS/Linux
```bash
chmod +x installer_unix.sh
./installer_unix.sh
```

Si vous utilisez Ubuntu/Debian et que Qt WebEngine ne démarre pas, installez également:
```bash
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine
```

## Utilisation

Choisissez un mode dans la liste supérieure. Chaque mode charge un HUD indépendant. `F1 Engineer` affiche l'état du listener UDP et les métadonnées des paquets reçus.

Dans F1 25, activez la télémétrie UDP et configurez l'adresse IP de cette machine avec le port `20777`. Le format de télémétrie doit être `2025`.

Le header F1 25 est décodé (format, version, ID paquet, session, frame et index voiture). Les payloads complets restent version-dépendants; l'application ne fabrique pas de valeurs lorsqu'un champ réel n'est pas disponible.

## Dépannage

- `ModuleNotFoundError: PyQt5`: relancez l'installateur depuis le dossier du projet.
- `UDP ERROR: Address already in use`: fermez une autre application utilisant 20777.
- `UDP waiting`: vérifiez que le jeu envoie vers la bonne IP et que le pare-feu autorise UDP entrant.
- Sous Windows, autorisez Python dans le pare-feu lors de la première exécution.

Les clés API sont stockées localement dans `~/.jarvis-f1/config.json`. Ne transmettez jamais ce fichier.
