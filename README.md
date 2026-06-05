# QMC Quantum Framework v2.7.1

<div align="center">

![Version](https://img.shields.io/badge/version-2.7.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Qiskit](https://img.shields.io/badge/qiskit-2.3%2B-6929C4.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![IBM Quantum](https://img.shields.io/badge/IBM%20Quantum-Heron%20r1--r3-054ADA.svg)
![Audited](https://img.shields.io/badge/audited-237%20fixes-success.svg)

**Framework de test quantique complet — un seul fichier, fait tout, simple et rapide**

*QMC Research Lab — France*

[⚡ Quick Use](#-quick-use) • [📖 Wiki](https://qmc-lab.com/framework/wiki) • [Installation](#-installation) • [Features](#-features) • [API](#-api-reference)

</div>

---

## ⚡ Quick Use

> **Philosophie** : copiez **un seul fichier** `qmc_quantum_framework_v2_7_1.py`, importez, et tout fonctionne.
> L'`import` est **pur** (aucun effet de bord, aucune installation au chargement).

```bash
# 1) Dépendances — au choix :
python qmc_quantum_framework_v2_7_1.py --check-deps          # vérifie (sans rien installer)
python qmc_quantum_framework_v2_7_1.py --install             # installe les manquantes
#   ou manuellement :
pip install qiskit qiskit-ibm-runtime numpy scipy cryptography python-dotenv matplotlib
```

```python
# 2) Trois lignes pour exécuter un circuit sur IBM Quantum
from qmc_quantum_framework_v2_7_1 import QMCFramework

fw = QMCFramework(backend_name="ibm_torino", project="MonExperience", shots=4096)
fw.connect()                                   # lit les credentials depuis .env

circuit  = fw.build_circuit("ghz", n_qubits=5) # 21 builders : ghz, bell, iqp, grover, qft, qpe, teleportation…
results  = fw.run_on_qpu([circuit])            # transpile + exécute + rapport HTML + archive JSON

print("Job ID :", fw.last_job_id)
print("Counts :", results[0]["counts"])
print("Sorties dans qmc_runs/ (rapport .html + archive .json.gz)")
```

```bash
# 3) Essayer SANS credentials IBM (simulateur local Aer)
python test_qmc_v2_7_1_FULL_VALIDATION.py --skip-qpu       # 15 tests (API, multi-job, transpilation)
python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-sim   # exécution réelle sur AerSimulator
```

📖 **Plus d'exemples → [Wiki / Quick Start](https://qmc-lab.com/framework/wiki/quick-start)**

---

## 📖 Wiki & Documentation

La documentation complète est sur le **wiki** : **<https://qmc-lab.com/framework/wiki>**

| Section | Lien |
|---------|------|
| 🏁 Démarrage rapide | <https://qmc-lab.com/framework/wiki/quick-start> |
| 📦 Installation & configuration | <https://qmc-lab.com/framework/wiki/installation> |
| 🔬 Circuit Builders (21) | <https://qmc-lab.com/framework/wiki/circuit-builders> |
| 📊 Analyzers (12) | <https://qmc-lab.com/framework/wiki/analyzers> |
| 🔐 Cryptographie quantique | <https://qmc-lab.com/framework/wiki/crypto> |
| ☁️ Audit multi-comptes | <https://qmc-lab.com/framework/wiki/multi-account-audit> |
| 📈 Rapports & archives | <https://qmc-lab.com/framework/wiki/reports> |
| 🧩 Référence API | <https://qmc-lab.com/framework/wiki/api-reference> |
| 🗒️ Changelog | <https://qmc-lab.com/framework/wiki/changelog> |

---

## 🎯 Overview

Le **QMC Quantum Framework** est un framework Python **mono-fichier** pour l'exécution et l'analyse
d'expériences quantiques sur les processeurs IBM Quantum. Conçu pour être **simple, rapide et complet** :

- 🔬 **21 Circuit Builders** : GHZ, Bell, IQP, Grover, QFT, QPE, Téléportation, et plus
- 📊 **12 Analyzers** : Fidelity, Entropy, Correlation, XEB, Bell/CHSH — **avec barres d'erreur**
- 🔐 **Cryptographie RÉELLE** : AES-256-GCM + HKDF, HMAC, ZKP Schnorr, time-lock RSW, QRNG (NIST)
- 🚀 **Exécution QPU** : IBM Quantum (Heron r1/r2/r3), multi-job avec reprise, transpilation parallèle + cache
- 📈 **Rapports automatiques** : HTML interactifs + archives JSON (gzip par défaut)
- ☁️ **Cloud & Audit** : QMC Archive Manager + audit complet multi-comptes IBM

---

## ✨ What's New in v2.7.1

Version **auditée et durcie** (audit multi-agents → **237 correctifs** `[v2.7.1 FIX]`, tous vérifiés) :

- 🔴 **Correction quantique** : QPE (phases exactes), téléportation (corrections conditionnelles), SwapTest,
  Deutsch-Jozsa, encodage d'amplitude, Bell σ, tests NIST, QuantumVolume (critère 2σ / ≥100 essais).
- 🔐 **Cryptographie réelle** (remplace les démos) : `QMCQuantumCrypto` (AES-256-GCM + HKDF-SHA256, HMAC,
  min-entropie NIST SP 800-90B), `QMCSigmaZK` (ZKP Schnorr + range-proof vérifiables), `QMCTimeLock` (puzzle RSW).
- 🛡️ **Sécurité** : anti-exfiltration de jeton (allowlist https), anti-SSRF (webhooks épinglés), anti-XSS des
  rapports, redaction des secrets dans les logs, nettoyage des credentials temporaires.
- 🧱 **Robustesse & perf** : écritures JSON atomiques, intégrité des résultats (registres/shots), reprise QPU
  fiabilisée, **cache de transpilation** câblé, addons IBM réparés (M3/EPLG/CLOPS/Trotter).
- 🧹 **Propreté** : `import` PUR (auto-install opt-in via `--install`), **hiérarchie de classe linéarisée**
  (`QMCFramework` = classe complète, plus de monkey-patch), API publique stable + `__all__`.

📖 **Détail complet → [Wiki / Changelog](https://qmc-lab.com/framework/wiki/changelog)** • `qmc_audit/CHANGELOG_v2_7_1.md`

---

## 📦 Installation

### Prérequis
- Python **3.10+**
- Un compte **IBM Quantum** avec token API
- ~500 MB d'espace disque

### Installation
```bash
git clone https://github.com/QmcLabOfficial/QMC_FRAMEWORK.git
cd QMC_FRAMEWORK

# Dépendances (recommandé : un environnement virtuel)
python -m venv .venv && . .venv/bin/activate          # Windows: .venv\Scripts\activate
python qmc_quantum_framework_v2_7_1.py --install        # ou pip install … (voir Quick Use)

# Configuration
cp .env.example .env       # puis éditer .env avec vos credentials
```

### Configuration (`.env`)

Voir **`.env.example`** (template complet). Le framework détecte automatiquement tous les comptes définis
via le motif `IBM_API_KEY_<LABEL>` (+ `IBM_INSTANCE_<LABEL>` optionnel), et le compte **actif** via
`IBM_API_KEY_ACTIVE_<LABEL>`.

```env
# === Comptes IBM Quantum (multi-comptes : un LABEL libre par compte) ===
IBM_API_KEY_ALICE=your_ibm_api_key_here
IBM_API_KEY_LAB=your_ibm_api_key_here
IBM_INSTANCE_LAB=crn:v1:bluemix:public:quantum-computing:us-east:a/xxxx::   # optionnel (plan payant)

# === Compte ACTIF par défaut ===
IBM_API_KEY_ACTIVE_QMCLAB=your_active_ibm_api_key_here
IBM_INSTANCE_QMCLAB=crn:v1:bluemix:public:quantum-computing:us-east:a/xxxx::

# === QMC Archive Manager (optionnel) ===
QMC_ARCHIVE_URL=https://votre-projet.supabase.co/functions/v1/upload   # https requis (allowlist d'hôtes)
QMC_ARCHIVE_TOKEN=qmc_your_archive_token_here
QMC_ARCHIVE_UPLOAD=true

# === Options ===
QMC_GENERATE_REPORT=true
QMC_GENERATE_ARCHIVE=true
QMC_AUTO_CONFIRM=false
```

> ⚠️ **Sécurité** : ne **commitez jamais** votre `.env` (il contient des secrets). Vérifiez qu'il figure dans
> `.gitignore` et conservez-le hors d'un dossier synchronisé/public. Les tokens sont automatiquement masqués
> dans les logs et rapports (redaction v2.7.1). 📖 [Wiki / Sécurité](https://qmc-lab.com/framework/wiki/installation).

📖 **Guide détaillé → [Wiki / Installation](https://qmc-lab.com/framework/wiki/installation)**

---

## 🚀 Exemples

### Analyse de calibration
```python
calibration = fw.noise.analyze_calibration()
print("Erreur readout moyenne :", calibration["summary"]["readout_error"]["mean"])
print("Erreur 2-qubit moyenne :", calibration["summary"]["gate_2q"]["mean"])
```

### Analyzers avec barres d'erreur
```python
from qmc_quantum_framework_v2_7_1 import FidelityAnalyzer, XEBAnalyzer

counts = results[0]["counts"]
fid = FidelityAnalyzer().analyze(counts)
print(f"Fidélité = {fid['fidelity']:.3f} ± {fid['std_error']:.3f}  (IC95 {fid['ci_95']})")
```

### Cryptographie réelle
```python
from qmc_quantum_framework_v2_7_1 import QMCQuantumCrypto, QMCSigmaZK

key = QMCQuantumCrypto.hkdf_sha256(b"quantum-entropy-seed", length=32)
enc = QMCQuantumCrypto.aead_encrypt(key, b"message secret")      # AES-256-GCM
clr = QMCQuantumCrypto.aead_decrypt(key, enc["nonce"], enc["ciphertext"])

proof = QMCSigmaZK.range_prove(value=42, lower=0, upper=100)      # preuve ZK (sans révéler 42)
assert QMCSigmaZK.range_verify(proof)
```

### Multi-job avec reprise automatique
```python
jobs = [{"circuits": [c1], "shots": 4096, "label": "job_1"},
        {"circuits": [c2], "shots": 4096, "label": "job_2"}]
session = fw.run_multi_job_session(jobs=jobs)     # reprend automatiquement en cas de crash
```

### Audit multi-comptes
```python
result = fw.audit_accounts(window_days=30, budget_minutes=10.0)
print("Comptes :", result["global_stats"]["total_accounts"])
print("Rapport :", result["generated_files"]["html"])
```

📖 **Tous les exemples → [Wiki / Quick Start](https://qmc-lab.com/framework/wiki/quick-start)**

---

## 📚 Features

### Circuit Builders (21) — 📖 [Wiki](https://qmc-lab.com/framework/wiki/circuit-builders)

| Builder | Description | Builder | Description |
|---------|-------------|---------|-------------|
| `GHZBuilder` | États GHZ | `QPEBuilder` | Estimation de phase |
| `BellBuilder` | Paires de Bell | `DeutschJozsaBuilder` | Deutsch-Jozsa |
| `IQPBuilder` | Instantaneous QP | `BernsteinVaziraniBuilder` | Bernstein-Vazirani |
| `ClusterBuilder` | États cluster | `SimonBuilder` | Algorithme de Simon |
| `RandomCircuitBuilder` | Circuits aléatoires | `SwapTestBuilder` | Test SWAP (fidélité) |
| `QFTBuilder` | Transformée de Fourier | `QRNGBuilder` | Générateur aléatoire |
| `GroverBuilder` | Algorithme de Grover | `TeleportationBuilder` | Téléportation |
| `ParameterizedCircuitBuilder` | Circuits VQE | `AmplitudeEncodingBuilder` | Encodage d'amplitude |
| `QuantumSignatureBuilder` | Signatures quantiques | `ZKPBuilder` | Zero-Knowledge Proofs |
| `TimeLockBuilder` | Time-lock (RSW) | `ObliviousTransferBuilder` | Transfert inconscient |
| `HardwareEfficientBuilder` | Ansatz hardware-efficient | | |

### Analyzers (12) — 📖 [Wiki](https://qmc-lab.com/framework/wiki/analyzers)

| Analyzer | Métriques | Analyzer | Métriques |
|----------|-----------|----------|-----------|
| `FidelityAnalyzer` | Fidélité + IC95 | `CompressionAnalyzer` | Couverture d'états |
| `EntropyAnalyzer` | Shannon / Von Neumann | `XEBCrossValidationAnalyzer` | XEB validation croisée |
| `CorrelationAnalyzer` | Corrélations + σ | `HoneypotAnalyzer` | Détection d'attaques |
| `XEBAnalyzer` | XEB + barres d'erreur | `QuantumAdvantageAnalyzer` | Avantage quantique (gaté) |
| `BellAnalyzer` | CHSH (S, σ binomial) | `RandomnessAnalyzer` | Tests style NIST |

### Fonctionnalités avancées
- **Fractional Gates** (RX/RZZ natives) · **Gen3 Turbo** · **Dynamic Circuits**
- **Error Mitigation** : M3, ZNE, Twirling, DD, PEA
- **Transpilation parallèle multi-CPU + cache** (lots identiques réutilisés)
- **Multi-job avec reprise** · **Cryptographie réelle** (AES-GCM / HKDF / ZK) · **Modules externes** chargés à la demande

---

## 🧩 API Reference

📖 **Référence complète → [Wiki / API](https://qmc-lab.com/framework/wiki/api-reference)**

```python
from qmc_quantum_framework_v2_7_1 import QMCFramework   # classe principale (concrète, complète)

fw = QMCFramework(backend_name="ibm_fez", project="QMC_Test", shots=4096,
                  use_fractional_gates=False, gen3_turbo=False)

fw.connect()                                  # -> bool
fw.build_circuit("ghz", n_qubits=5)           # -> QuantumCircuit
fw.transpile_circuits([circuit])              # transpilation (parallèle + cache)
fw.run_on_qpu([circuit], shots=4096)          # -> List[Dict] (counts, shots, …)
fw.run_multi_job_session(jobs=[...])          # multi-job + reprise
fw.audit_accounts(window_days=30)             # audit multi-comptes
fw.estimate_eplg(); fw.estimate_clops()       # addons IBM (M3/EPLG/CLOPS/Trotter)
fw.last_job_id                                # ID du dernier job soumis

module = fw.load_module("nom")                # charge un module externe (brevets fournis séparément)
module.run(...)                               # QMCModuleNotAvailableError si non disponible
```

> **Hiérarchie (v2.7.1, linéarisée)** : `QMCFrameworkBase → QMCFrameworkExtended → QMCFramework`,
> où `QMCFramework` est la **classe concrète publique** (la relique `QMCFrameworkV2_4` a été supprimée).
> `import` pur, pas d'alias ni de monkey-patch.

---

## 🧪 Tests

```bash
# Validation complète sur QPU réel
python test_qmc_v2_7_1_FULL_VALIDATION.py --backend ibm_torino --shots 100

# Tests locaux (sans QPU / sans credentials)
python test_qmc_v2_7_1_FULL_VALIDATION.py --skip-qpu          # API + multi-job + transpilation
python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-sim      # exécution AerSimulator
```

> 💡 Sous Windows, lancez avec `PYTHONUTF8=1` pour l'affichage des emojis/box-drawing.

---

## 📜 Changelog (résumé)

- **v2.7.1 (2026-05)** — Audit complet : **237 correctifs**, cryptographie réelle, sécurité durcie, import pur,
  hiérarchie linéarisée, cache de transpilation, barres d'erreur. 📖 [Changelog complet](https://qmc-lab.com/framework/wiki/changelog)
- **v2.7.0 (2026-01)** — Multi-Job Session + Auto-Resume + Transpilation parallèle.
- **v2.6.3 (2026-01)** — QMC Accounts Audit Module.
- **v2.6.2 / v2.6.1 / v2.6.0** — Archive Manager, auto-fetch QPU, Fractional Gates / Gen3 Turbo.

---

## 🔒 Modules propriétaires (brevets)

Les implémentations brevetées **ne sont pas incluses** dans ce framework public : leur
fonctionnement n'est **jamais exposé** dans le code. Elles sont distribuées comme **modules
externes**, chargés **à la demande** via `fw.load_module("<nom>")` (dossier `qmc_modules/`,
emplacement surchargé par `QMC_MODULES_PATH`) et fournis séparément aux clients autorisés.
En l'absence du module, le framework lève `QMCModuleNotAvailableError`.

| Référence | Module (fourni séparément) |
|-----------|----------------------------|
| FR2514352 | QMC Core |
| FR2514504 | QMC Biometric |
| FR2514363 | QMC Shield |
| FR2514509 | QAEE |
| FR2514682 | QGP |
| FR2515002 | QDNA-ID |
| FR2515103 | QRPM |
| FR2515682 | QMC SIP |

> Contrat d'un module et template d'interface : voir [`qmc_modules/README.md`](qmc_modules/README.md).

---

## 🤝 Contributing & Contact

Projet en développement privé pour QMC Research Lab.
- 🌐 Site : [qmc-lab.com](https://qmc-lab.com) · 📖 Wiki : [qmc-lab.com/framework/wiki](https://qmc-lab.com/framework/wiki)
- 📦 GitHub : [@QmcLabOfficial](https://github.com/QmcLabOfficial)

---

## 📄 License

**Proprietary** — © 2024-2026 QMC Research Lab, Menton, France.
Toute reproduction, distribution ou utilisation non autorisée est strictement interdite.

---

<div align="center">

**Built with ❤️ by QMC Research Lab**

*Quantum Mandatory Cryptography — Where Security REQUIRES Quantum*

</div>
