# `qmc_modules/` — Modules externes (propriétaires / brevets)

Ce dossier contient les **modules métier/propriétaires** du framework QMC.
Ils **ne sont pas** inclus dans `qmc_quantum_framework_v2_7_1.py` : le fonctionnement
des inventions brevetées n'est donc **jamais exposé** dans le fichier public.
Chaque module est un **script séparé**, chargé **à la demande** uniquement lorsqu'un
client y a accès.

## Comment ça marche

```python
from qmc_quantum_framework_v2_7_1 import QMCFramework

fw = QMCFramework(project="DEMO", backend_name="ibm_fez")
fw.connect()

module = fw.load_module("qmc_core")   # charge qmc_modules/qmc_core.py
result = module.run(...)
```

- `fw.load_module("nom")` charge le fichier **`qmc_modules/nom.py`**.
- Le fichier doit définir **une sous-classe de `QMCModule`** (voir le template).
- Si le fichier est **absent**, le framework lève **`QMCModuleNotAvailableError`**
  avec un message clair (le module est « fourni séparément sur demande »).

## Emplacement

Par défaut : ce dossier (`qmc_modules/`, à côté du framework).
Surchargeable par la variable d'environnement :

```bash
# Windows (PowerShell)
$env:QMC_MODULES_PATH = "C:\chemin\vers\mes_modules_proprietaires"
# Linux / macOS
export QMC_MODULES_PATH=/chemin/vers/mes_modules_proprietaires
```

## Contrat d'un module

Un module = un fichier `nom.py` définissant une classe qui hérite de `QMCModule` :

| Méthode | Obligatoire | Rôle |
|---|---|---|
| `get_name()` (classmethod) | ✅ | identifiant unique = `nom` du fichier |
| `run(**kwargs)` | ✅ | logique principale, retourne un `dict` |
| `get_version()` | ⛔ optionnel | version du module |
| `get_description()` | ⛔ optionnel | description courte |
| `get_patent_ref()` | ⛔ optionnel | référence interne (NON exposée publiquement) |
| `get_dependencies()` | ⛔ optionnel | autres modules requis |
| `initialize(config)` | ⛔ optionnel | initialisation (config) |

Le module reçoit l'instance `QMCFramework` via son constructeur
(`self.framework`) et peut donc utiliser toute l'API publique (build de circuits,
transpilation, `run_on_qpu`, crypto générique `QMCQuantumCrypto`, ZK `QMCSigmaZK`,
time-lock `QMCTimeLock`, analyzers, etc.).

Voir **`_module_template.py.template`** pour un squelette prêt à copier
(renommez-le en `mon_module.py` pour l'activer).

## ⚠️ Sécurité / IP

- Ne commitez **pas** les modules propriétaires dans le dépôt public.
- Le `.gitignore` du framework ignore `qmc_modules/*.py` (sauf le template et ce README).
