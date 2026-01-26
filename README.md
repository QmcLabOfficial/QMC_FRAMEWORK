# QMC Quantum Framework v2.6.3

<div align="center">

![Version](https://img.shields.io/badge/version-2.6.3-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Qiskit](https://img.shields.io/badge/qiskit-1.0%2B-6929C4.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![IBM Quantum](https://img.shields.io/badge/IBM%20Quantum-Heron%20r1--r3-054ADA.svg)

**Framework de test quantique complet pour les brevets QMC**

*QMC Research Lab - Menton, France*

[Documentation](#-documentation) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [API Reference](#-api-reference)

</div>

---

## 🎯 Overview

Le **QMC Quantum Framework** est un framework Python complet pour l'exécution et l'analyse d'expériences quantiques sur les processeurs IBM Quantum. Développé par QMC Research Lab, il fournit une abstraction de haut niveau pour :

- 🔬 **21 Circuit Builders** : GHZ, Bell, IQP, Grover, QFT, et plus
- 📊 **12 Analyzers** : Fidelity, Entropy, Correlation, XEB, Bell violations
- 🚀 **Exécution QPU** : Support complet IBM Quantum (Heron r1/r2/r3)
- 📈 **Rapports automatiques** : HTML interactifs + archives JSON complètes
- ☁️ **Cloud Integration** : QMC Archive Manager pour stockage centralisé
- 🔍 **Multi-Account Audit** : Audit complet de tous vos comptes IBM Quantum

---

## ✨ What's New in v2.6.3

### 🔍 QMC Accounts Audit Module

Audit complet de vos comptes IBM Quantum avec rapports HTML style IBM Carbon :

```python
from qmc_quantum_framework_v2_6_3 import QMCFramework

fw = QMCFramework(backend_name="ibm_torino")

# Audit tous les comptes configurés dans .env
result = fw.audit_accounts(window_days=30, budget_minutes=10.0)

# Ou via le script dédié
# python qmc_audit_accounts.py --days 30 --budget 10 --open
```

**Features:**
- ✅ Auto-détection des comptes depuis `.env`
- ✅ Rapports HTML avec graphiques Chart.js
- ✅ Gestion intelligente des comptes inaccessibles
- ✅ Statistiques par compte, backend, jour

<details>
<summary>📸 Voir exemple de rapport</summary>

Le rapport HTML inclut :
- 6 métriques globales (comptes, jobs, usage, budget)
- Graphique usage par compte vs budget
- Timeline 14 jours
- Distribution des statuts (DONE, ERROR, etc.)
- Distribution par backend
- Table détaillée des comptes avec indicateurs visuels

</details>

---

## 📦 Installation

### Prérequis

- Python 3.10+
- Compte IBM Quantum avec token API
- ~500 MB d'espace disque

### Installation

```bash
# Cloner le repository
git clone https://github.com/QmcLabOfficial/qmc-quantum-framework.git
cd qmc-quantum-framework

# Installer les dépendances
pip install qiskit qiskit-ibm-runtime python-dotenv numpy scipy

# Copier le fichier d'environnement
cp .env.example .env
# Éditer .env avec vos credentials
```

### Configuration (.env)

```env
# === IBM QUANTUM (Compte principal) ===
IBM_QUANTUM_TOKEN=your_token_here

# === Multi-comptes (optionnel) ===
IBM_API_KEY_MAIN=token_compte_principal
IBM_API_KEY_BACKUP=token_compte_backup
IBM_API_KEY_ACTIVE_RESEARCH=token_compte_research

# === QMC Archive Manager (optionnel) ===
QMC_ARCHIVE_URL=http://your-archive-server:4000
QMC_ARCHIVE_TOKEN=your_archive_token
QMC_ARCHIVE_UPLOAD=true

# === Options ===
QMC_GENERATE_REPORT=true
QMC_GENERATE_ARCHIVE=true
QMC_OUTPUT_DIR=qmc_runs
```

---

## 🚀 Quick Start

### Exemple Minimal

```python
from qmc_quantum_framework_v2_6_3 import QMCFramework, GHZBuilder

# Initialiser le framework
fw = QMCFramework(
    backend_name="ibm_torino",
    project="MonExperience",
    shots=4096
)

# Connecter au backend
fw.connect()

# Créer un circuit GHZ 5 qubits
builder = GHZBuilder(num_qubits=5)
circuit = builder.build()

# Exécuter sur QPU (avec confirmation)
results = fw.run_on_qpu_with_confirm([circuit])

# Résultats disponibles
print(f"Job ID: {results['job_id']}")
print(f"Counts: {results['counts'][0]}")
print(f"Rapport: {results['report_path']}")
```

### Analyse de Calibration

```python
# Analyser l'état du QPU avant expérience
calibration = fw.analyze_calibration()

print(f"Qubits totaux: {calibration['total_qubits']}")
print(f"Qubits sains: {calibration['healthy_qubits']}")
print(f"Meilleurs qubits: {calibration['best_qubits'][:10]}")
```

### Audit Multi-Comptes

```python
# Audit de tous les comptes IBM Quantum
result = fw.audit_accounts(
    window_days=30,
    budget_minutes=10.0,
    generate_html=True
)

print(f"Comptes: {result['global_stats']['total_accounts']}")
print(f"Jobs totaux: {result['global_stats']['total_jobs']}")
print(f"Rapport: {result['generated_files']['html']}")
```

---

## 📚 Features

### Circuit Builders (21)

| Builder | Description | Qubits |
|---------|-------------|--------|
| `GHZBuilder` | États GHZ (intrication maximale) | N |
| `BellBuilder` | Paires de Bell | 2 |
| `IQPBuilder` | Instantaneous Quantum Polynomial | N |
| `ClusterBuilder` | États cluster (graph states) | N |
| `RandomCircuitBuilder` | Circuits aléatoires | N |
| `QFTBuilder` | Transformée de Fourier Quantique | N |
| `GroverBuilder` | Algorithme de Grover | N |
| `QPEBuilder` | Estimation de Phase Quantique | N |
| `DeutschJozsaBuilder` | Algorithme Deutsch-Jozsa | N |
| `BernsteinVaziraniBuilder` | Algorithme Bernstein-Vazirani | N |
| `SimonBuilder` | Algorithme de Simon | N |
| `SwapTestBuilder` | Test SWAP (fidelity) | 2N+1 |
| `QRNGBuilder` | Générateur aléatoire quantique | N |
| `TeleportationBuilder` | Téléportation quantique | 3 |
| `ParameterizedCircuitBuilder` | Circuits paramétrés (VQE) | N |
| `AmplitudeEncodingBuilder` | Encodage d'amplitude | N |
| `QuantumSignatureBuilder` | Signatures quantiques | N |
| `ZKPBuilder` | Zero-Knowledge Proofs | N |
| `TimeLockBuilder` | Time-lock puzzles quantiques | N |
| `ObliviousTransferBuilder` | Transfert inconscient | N |
| `HardwareEfficientBuilder` | Circuits optimisés hardware | N |

### Analyzers (12)

| Analyzer | Métriques |
|----------|-----------|
| `FidelityAnalyzer` | Fidelity vs état cible |
| `EntropyAnalyzer` | Entropie de Shannon, Von Neumann |
| `CorrelationAnalyzer` | Corrélations inter-qubits |
| `XEBAnalyzer` | Cross-Entropy Benchmarking |
| `BellAnalyzer` | Violations CHSH, S-value |
| `RandomnessAnalyzer` | Tests NIST (χ², runs, etc.) |
| `CompressionAnalyzer` | Ratio de compression |
| `XEBCrossValidationAnalyzer` | XEB avec validation croisée |
| `HoneypotAnalyzer` | Détection d'attaques |
| `QuantumAdvantageAnalyzer` | Avantage quantique |

### Fonctionnalités Avancées

- **Fractional Gates** : Portes RX/RZZ natives (-600% depth)
- **Gen3 Turbo Mode** : Nouveau moteur IBM (75x speedup)
- **Dynamic Circuits** : Mesures mid-circuit + reset
- **Error Mitigation** : ZNE, Twirling, DD, PEA
- **Parallel Transpilation** : Multi-threading pour gros batches
- **QPY Serialization** : Sauvegarde/chargement circuits optimisés

---

## 📊 Rapports Générés

### Rapport HTML

Chaque exécution QPU génère un rapport HTML interactif :

- 📈 Histogrammes des résultats
- 🗺️ Heatmap des qubits (qualité)
- 📊 Métriques de calibration
- ⏱️ Timeline d'exécution
- 🔧 Paramètres de transpilation

### Archive JSON (v3.1)

Archive complète avec 41 sections :

```json
{
  "archive_version": "3.1",
  "execution": { "job_id", "backend", "shots", "duration" },
  "circuits": { "names", "depths", "gate_counts" },
  "results": { "counts", "memory", "quasi_dists" },
  "calibration": { "qubits", "gates", "readout_errors" },
  "analysis": { "fidelity", "entropy", "correlations" },
  ...
}
```

---

## 🔧 API Reference

### QMCFramework

```python
class QMCFramework:
    def __init__(
        self,
        backend_name: str = "ibm_fez",
        project: str = "QMC_Test",
        shots: int = 4096,
        use_fractional_gates: bool = False,
        gen3_turbo: bool = False
    )
    
    def connect(self) -> bool
    def analyze_calibration(self) -> Dict
    def run_on_qpu(self, circuits, shots=None, **kwargs) -> Dict
    def run_on_qpu_with_confirm(self, circuits, **kwargs) -> Dict
    
    # v2.6.3: Audit
    def audit_accounts(self, window_days=30, budget_minutes=10.0, **kwargs) -> Dict
    def list_ibm_accounts(self) -> Dict
```

### Fonctions Globales

```python
# v2.6.2: Archive Manager
from qmc_quantum_framework_v2_6_3 import get_archive_uploader
uploader = get_archive_uploader()
uploader.upload("archive.json", project_ids=["uuid1"])

# v2.6.3: Accounts Audit
from qmc_quantum_framework_v2_6_3 import run_accounts_audit, get_all_ibm_accounts_from_env
accounts = get_all_ibm_accounts_from_env()
result = run_accounts_audit(accounts, window_days=30)
```

---

## 🧪 Tests

### Validation Complète

```bash
# Tests complets avec QPU
python test_qmc_v2_6_3_FULL_VALIDATION.py --backend ibm_torino --shots 100

# Tests locaux uniquement (sans QPU)
python test_qmc_v2_6_3_FULL_VALIDATION.py --skip-qpu

# Audit des comptes
python qmc_audit_accounts.py --list
python qmc_audit_accounts.py --days 7 --open
```

### Structure des Tests

```
test_qmc_v2_6_3_FULL_VALIDATION.py
├── Section 1: Import & Initialisation
├── Section 2: Connexion & Calibration
├── Section 3: Circuit Builders (21)
├── Section 4: Analyzers (12)
├── Section 5: Features v2.6.0/v2.6.1
├── Section 5b: QMC Archive v2.6.2
├── Section 5c: Accounts Audit v2.6.3
├── Section 6: Optimizers & Calculators
├── Section 7: Error Mitigation
├── Section 8: QDNA Features
├── Section 9: QPU Execution
├── Section 10: Results Analysis
└── Section 11: Archive JSON v3.1
```

---

## 📁 Project Structure

```
qmc-quantum-framework/
├── qmc_quantum_framework_v2_6_3.py    # Framework principal (43k+ lignes)
├── test_qmc_v2_6_3_FULL_VALIDATION.py # Tests exhaustifs
├── qmc_audit_accounts.py              # Script d'audit simple
├── QMC_FRAMEWORK_DOCUMENTATION_2_6_3.md # Documentation AI-readable
├── README.md                          # Ce fichier
├── .env.example                       # Template configuration
└── qmc_runs/                          # Rapports générés
    ├── *.html                         # Rapports HTML
    └── *.json                         # Archives JSON
```

---

## 📜 Changelog

### v2.6.3 (2026-01-26)
- ✨ **QMC Accounts Audit Module**
  - `QMCJobDataCollector` : collecte multi-comptes
  - `QMCAuditHTMLReportGenerator` : rapports IBM Carbon
  - `fw.audit_accounts()`, `fw.list_ibm_accounts()`
  - Gestion intelligente des comptes inaccessibles

### v2.6.2 (2026-01-26)
- ✨ **QMC Archive Manager Integration**
  - Upload automatique non-bloquant
  - `QMCArchiveUploader` class
  - Paramètres `run_on_qpu()` : `upload_to_archive`, `archive_projects`

### v2.6.1 (2026-01-24)
- ✨ Auto-fetch état QPU avant `run_on_qpu()`
- 🔧 `QMC_SKIP_QPU_STATE_FETCH` pour override

### v2.6.0 (2026-01-23)
- ✨ Fractional Gates support
- ✨ Gen3 Turbo Mode (75x speedup)
- ✨ PEA Mitigation
- 🔧 Support Qiskit 1.0+ / Runtime 0.45+

<details>
<summary>Versions antérieures</summary>

### v2.5.23 (2025-01-05)
- 18 nouvelles fonctionnalités
- Support complet IBM Heron r1/r2/r3

### v2.5.22 (2025-01-01)
- Compatibilité émulateur ↔ QPU
- Système d'audit intégré

</details>

---

## 🔒 Brevets Associés

Ce framework supporte le développement et la validation des brevets QMC :

| Référence | Nom | Description |
|-----------|-----|-------------|
| FR2514352 | QMC Core | Chiffrement quantique IQP #P-hard |
| FR2514504 | QMC Biometric | Dérivation biométrique quantique |
| FR2514363 | QMC Shield | Migration matérielle clés quantiques |
| FR2514509 | QAEE | Estimation d'Amplitude Adaptative |
| FR2514682 | QGP | Quantum Genesis Protocol |
| FR2515002 | QDNA-ID | Authentification QPU par signature bruit |
| FR2515103 | QRPM | Quantum Random Permutation Module |
| FR2515682 | QMC SIP | Quantum Secure Identity Protocol |

---

## 🤝 Contributing

Ce projet est actuellement en développement privé pour QMC Research Lab.

Pour toute question ou collaboration :
- 📧 Contact : [QMC Research Lab](https://qmc-lab.com)
- 🔗 LinkedIn : QMC Research Lab
- 📦 GitHub : [@QmcLabOfficial](https://github.com/QmcLabOfficial)

---

## 📄 License

**Proprietary** - © 2024-2026 QMC Research Lab, Menton, France

Ce code est la propriété exclusive de QMC Research Lab. Toute reproduction, distribution ou utilisation non autorisée est strictement interdite.

---

<div align="center">

**Built with ❤️ by QMC Research Lab**

*Quantum Mandatory Cryptography - Where Security REQUIRES Quantum*

</div>
