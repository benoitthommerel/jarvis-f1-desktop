# JARVIS F1 Race Engineer - Desktop Application

**Une application de bureau native pour Windows, macOS et Linux avec interface F1 télémétrie, support multi-clés API et routage automatique.**

## Features

✅ **Application de Bureau Native** (pas de navigateur)  
✅ **Dashboard F1 Telemetry** avec réacteur arc animé  
✅ **Menu AI Config** intégré pour gestion des clés API  
✅ **Support Multi-Clés** avec routage automatique  
✅ **Modes d'exploitation** : Normal Dev, F1 Engineer, Discret, Background Worker  
✅ **Sélection de provider** : OpenAI, Claude, Gemini, Groq, Ollama  
✅ **Compatibilité universelle** : Windows, macOS, Linux  

## Installation Rapide

### Windows

```bash
double-clic sur lancer.bat
```

### macOS / Linux

```bash
chmod +x lancer.sh
./lancer.sh
```

## Structure du Projet

```
jarvis-f1-desktop/
├── app.py           # Application principale (PyQt5 + WebEngine)
├── lancer.bat       # Script de lancement Windows
├── lancer.sh        # Script de lancement macOS/Linux
└── README.md        # Ce fichier
```

## Utilisation

1. **Lancer l'application** via le script approprié à votre système
2. **Configurer les clés API** via le bouton ⚙ **AI Config**
3. **Sélectionner votre mode** (Normal Dev, F1 Engineer, etc.)
4. **Utiliser JARVIS** avec le dashboard F1 complet

## Sélection du Mode

| Mode | Fonction |
|------|----------|
| **Normal Dev** | Développement standard avec JARVIS |
| **F1 Engineer** | Mode ingénieur de course avec télémétrie complète |
| **Discrete** | Interface minimale, pas de perturbations |
| **Background Worker** | Exécution silencieuse des tâches en arrière-plan |

## Configuration des Clés API

Dans le menu **AI Config**, vous pouvez :
- Sélectionner votre provider IA préféré
- Ajouter votre clé API principale
- Ajouter des clés de secours (séparées par des virgules)
- Choisir le mode de routage :
  - **Auto Failover** : Bascule automatique en cas d'erreur
  - **Manual Select** : Choix manuel à chaque fois
  - **Round Robin** : Distribution équilibrée

## Prérequis

- **Python 3.8+**
- **PyQt5**
- **PyQtWebEngine**

Les scripts d'installation s'en chargent automatiquement.

## Problèmes Courants

### Python non trouvé (Windows)
→ Le script `lancer.bat` télécharge et installe Python automatiquement

### Permission refusée (macOS/Linux)
```bash
chmod +x lancer.sh
```

### Erreur PyQt5
```bash
pip install PyQt5 PyQtWebEngine --upgrade
```

## Architecture

```
JARVIS F1 Desktop
├── PyQt5 (Interface de bureau native)
├── QWebEngineView (Moteur de rendu HTML/CSS/JS)
├── HTML/CSS/SVG (Dashboard F1 moderne)
└── Python (Backend + gestion des configs)
```

## Améliorations Futures

- [ ] Intégration WebSocket pour télémétrie en temps réel
- [ ] Lecture/écriture de fichiers de configuration JSON
- [ ] Export des données de course
- [ ] Support des plug-ins personnalisés
- [ ] Synchronisation cloud des configurations

## License

MIT - Libre d'utilisation et de modification

## Contact & Support

📧 **Email** : soldat.80100@hotmail.fr  
🐙 **GitHub** : [benoitthommerel/jarvis-f1-desktop](https://github.com/benoitthommerel/jarvis-f1-desktop)

---

**Made with ❤️ by Benoit Thommerel**