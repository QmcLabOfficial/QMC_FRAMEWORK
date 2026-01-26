# QMC Quantum Framework v2.6.3 - Documentation Complète

> **Documentation destinée aux IA et développeurs pour créer des scripts d'exécution quantique**

---

## Table des matières

1. [Installation et Configuration](#1-installation-et-configuration)
2. [Connexion au Backend IBM](#2-connexion-au-backend-ibm)
3. [Création de Circuits](#3-création-de-circuits)
4. [Exécution sur QPU](#4-exécution-sur-qpu)
5. [Récupération des Résultats](#5-récupération-des-résultats)
6. [Analyse des Résultats](#6-analyse-des-résultats)
7. [Circuit Builders Disponibles](#7-circuit-builders-disponibles)
8. [Analyzers Disponibles](#8-analyzers-disponibles)
9. [Fonctionnalités Avancées](#9-fonctionnalités-avancées)
10. [Exemples Complets](#10-exemples-complets)
11. [Gestion des Erreurs](#11-gestion-des-erreurs)
12. [Référence API Rapide](#12-référence-api-rapide)
13. [QMC Archive Manager (v2.6.2)](#13-qmc-archive-manager-v262)
14. [★ NEW v2.6.3: QMC Accounts Audit](#14-qmc-accounts-audit-v263)
15. [Notes Importantes](#15-notes-importantes)
16. [Changelog](#16-changelog)

---

## 1. Installation et Configuration

### Import du Framework

```python
from qmc_quantum_framework_v2_6_3 import (
    QMCFramework,
    GHZBuilder, IQPBuilder, BellBuilder, ClusterBuilder,
    RandomCircuitBuilder, QFTBuilder, ParameterizedCircuitBuilder,
    GroverBuilder, QPEBuilder, DeutschJozsaBuilder, BernsteinVaziraniBuilder,
    SimonBuilder, SwapTestBuilder, QRNGBuilder, TeleportationBuilder,
    FidelityAnalyzer, EntropyAnalyzer, CorrelationAnalyzer,
    XEBAnalyzer, BellAnalyzer, RandomnessAnalyzer,
    # v2.6.2: QMC Archive Manager
    QMCArchiveUploader, get_archive_uploader,
    # ★ NEW v2.6.3: QMC Accounts Audit
    QMCJobDataCollector, QMCAuditHTMLReportGenerator,
    get_all_ibm_accounts_from_env, run_accounts_audit
)
```

### Configuration Environnement (.env)

Créer un fichier `.env` dans le répertoire de travail :

```env
# ═══════════════════════════════════════════════════════════════════════════════
# QMC FRAMEWORK v2.6.3 - CONFIGURATION COMPLÈTE
# ═══════════════════════════════════════════════════════════════════════════════

# === CREDENTIALS IBM QUANTUM (Compte principal) ===
IBM_QUANTUM_TOKEN=your_ibm_quantum_token_here

# === ★ NEW v2.6.3: MULTI-COMPTES IBM QUANTUM ===
# Format: IBM_API_KEY_<LABEL>=<token>
# ou:     IBM_API_KEY_ACTIVE_<LABEL>=<token>
IBM_API_KEY_MAIN=your_main_account_token
IBM_API_KEY_BACKUP=your_backup_account_token
IBM_API_KEY_ACTIVE_RESEARCH=your_research_account_token

# Optionnel: Instance/CRN par compte
IBM_CRN_MAIN=crn:v1:bluemix:public:quantum-computing:...
IBM_CRN_BACKUP=crn:v1:bluemix:public:quantum-computing:...

# === RAPPORTS ET ARCHIVES ===
QMC_GENERATE_REPORT=true          # Génère rapport HTML après exécution
QMC_GENERATE_ARCHIVE=true         # Génère archive JSON après exécution
QMC_OUTPUT_DIR=qmc_runs           # Répertoire de sortie

# === v2.6.2: QMC ARCHIVE MANAGER (Cloud Upload) ===
QMC_ARCHIVE_URL=http://localhost:4000      # URL de l'API QMC Archive Manager
QMC_ARCHIVE_TOKEN=your_archive_api_token   # Token d'authentification
QMC_ARCHIVE_UPLOAD=true                    # Activer/désactiver l'upload automatique
QMC_ARCHIVE_DEFAULT_PROJECTS=uuid1,uuid2   # UUIDs des projets par défaut

# === SÉCURITÉ ===
QMC_HIDE_TOKEN=true               # Masquer le token IBM dans les logs
```

---

## 2. Connexion au Backend IBM

### Connexion Simple

```python
# Initialiser le framework avec un backend
fw = QMCFramework(
    backend_name="ibm_torino",      # Backend IBM (Heron r1, 133 qubits)
    project="MonProjet",            # Nom du projet (pour les logs)
    default_shots=4096              # Shots par défaut
)

# Se connecter
success = fw.connect()
if success:
    print(f"✅ Connecté à {fw.backend_name}")
    print(f"   Qubits disponibles: {fw.backend.num_qubits}")
```

### Backends Disponibles (Janvier 2026)

| Backend | Qubits | Type | Gate 2Q | CLOPS | Erreur 2Q (médiane) |
|---------|--------|------|---------|-------|---------------------|
| `ibm_boston` | 156 | Heron r3 | CZ | 340k | 1.14e-3 ⭐ |
| `ibm_pittsburgh` | 156 | Heron r3 | CZ | 330k | 1.74e-3 |
| `ibm_kingston` | 156 | Heron r2 | CZ | 340k | 1.82e-3 |
| `ibm_fez` | 156 | Heron r2 | CZ | 320k | 2.80e-3 |
| `ibm_marrakesh` | 156 | Heron r2 | CZ | 300k | 2.39e-3 |
| `ibm_torino` | 133 | Heron r1 | CZ | 290k | 2.55e-3 |
| `ibm_miami` | 120 | Nighthawk r1 | CZ | 24k | 3.00e-3 |

> **Recommandation:** `ibm_boston` pour la meilleure qualité, `ibm_torino` pour un bon compromis.

### Connexion avec Analyse de Calibration

```python
fw = QMCFramework(backend_name="ibm_torino", project="Test")
fw.connect()

# Analyser la calibration du QPU
topology = fw.analyze_calibration()

# Afficher le rapport de calibration premium
topology.print_full_report()

# Informations disponibles
print(f"Qubits défaillants: {topology.faulty_qubits}")
print(f"Qubits suspects: {topology.suspect_qubits}")
print(f"Connexions cassées: {topology.broken_connections}")
```

---

## 3. Création de Circuits

### Méthode 1 : Utiliser les Builders Intégrés

```python
# GHZ State (intrication maximale)
ghz_builder = GHZBuilder(topology=fw.topology)
ghz_circuit = ghz_builder.build(n_qubits=50)

# IQP Circuit (cryptographie)
iqp_builder = IQPBuilder()
iqp_circuit = iqp_builder.build(n_qubits=30, depth=10)

# Bell States (paires intriquées)
bell_builder = BellBuilder()
bell_circuit = bell_builder.build(n_pairs=5)  # 10 qubits

# Random Circuit (benchmarking)
random_builder = RandomCircuitBuilder()
random_circuit = random_builder.build(n_qubits=20, depth=15, seed=42)

# QFT (Quantum Fourier Transform)
qft_builder = QFTBuilder()
qft_circuit = qft_builder.build(n_qubits=8)
```

### Méthode 2 : Créer des Circuits Manuellement (Qiskit)

```python
from qiskit import QuantumCircuit

# Circuit personnalisé
qc = QuantumCircuit(5, 5)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)
qc.measure_all()
```

### Créer un Batch de Circuits

```python
# Batch avec différentes tailles
builder = GHZBuilder(topology=fw.topology)
circuits = builder.build_batch(scales=[10, 20, 30, 50, 75, 100])

# Ou manuellement
circuits = [
    ghz_builder.build(n_qubits=50),
    iqp_builder.build(n_qubits=30, depth=5),
    bell_builder.build(n_pairs=10),
]
```

---

## 4. Exécution sur QPU

### Exécution Simple

```python
# Exécuter un circuit
results = fw.run_on_qpu(circuit, shots=4096)

# Exécuter plusieurs circuits
results = fw.run_on_qpu(circuits, shots=4096)
```

### Exécution avec Confirmation (Recommandé pour Tests)

```python
# Demande confirmation avant exécution (affiche coût estimé)
results = fw.run_on_qpu_with_confirm(
    circuits,
    shots=4096,
    description="Test GHZ 50-100 qubits"
)
```

### Paramètres d'Exécution

```python
results = fw.run_on_qpu(
    circuits,
    shots=4096,                    # Nombre de mesures par circuit
    auto_transpile=True,           # Transpiler automatiquement (recommandé)
    optimize_layout=False,         # Layout personnalisé QMC
    layout_strategy='none',        # 'none' (Sabre), 'topology_aware', 'best_qubits'
    show_calibration=True,         # Afficher résumé calibration
    timeout=3600,                  # Timeout en secondes (1h)
    generate_report=True,          # Générer rapport HTML
    generate_archive=True,         # Générer archive JSON
    
    # ★ NEW v2.6.2: QMC Archive Manager
    upload_to_archive=True,                    # Upload auto vers QMC Archive (défaut: True)
    archive_projects=['uuid1', 'uuid2'],       # Projets cibles (ou None pour defaults)
    archive_notes="Mon expérience HAWKING"     # Notes personnalisées (ou None pour auto)
)
```

### ★ NEW v2.6.2: Paramètres QMC Archive

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `upload_to_archive` | `bool` | `True` | Active/désactive l'upload vers QMC Archive Manager |
| `archive_projects` | `List[str]` | `None` | Liste des UUIDs de projets. Si `None`, utilise `QMC_ARCHIVE_DEFAULT_PROJECTS` |
| `archive_notes` | `str` | `None` | Notes personnalisées. Si `None`, génère automatiquement: "Job: {id} \| Date: {date} \| Backend: {name}" |

### Options de Layout Strategy

| Strategy | Description | Utilisation |
|----------|-------------|-------------|
| `'none'` | Layout Sabre IBM par défaut | Standard |
| `'topology_aware'` | Utilise la calibration pour éviter les mauvais qubits | Haute fidélité |
| `'best_qubits'` | Sélectionne les meilleurs qubits contigus | Circuits critiques |

---

## 5. Récupération des Résultats

### Structure des Résultats

```python
results = fw.run_on_qpu(circuits, shots=4096)

# results est une liste de dictionnaires
for i, result in enumerate(results):
    print(f"Circuit {i}:")
    print(f"  Counts: {result['counts']}")        # Dict[str, int]
    print(f"  Shots: {result['shots']}")          # int
    print(f"  Circuit name: {result.get('circuit_name', 'N/A')}")
```

### Format des Counts

```python
# Les counts sont des dictionnaires bitstring → nombre d'occurrences
counts = results[0]['counts']
# Exemple: {'00000': 2048, '11111': 2048}

# Bitstrings les plus fréquents
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
top_5 = sorted_counts[:5]
print(f"Top 5 bitstrings: {top_5}")
```

### Accès aux Métadonnées

```python
result = results[0]

# Informations disponibles
circuit_name = result.get('circuit_name')
n_qubits = result.get('n_qubits')
shots = result.get('shots')
counts = result.get('counts')

# Métadonnées du job
job_id = result.get('job_id')
backend_name = result.get('backend')
```

### Extraire les Informations de Timing

```python
# Si vous avez accès au contexte d'exécution
# (disponible dans les archives JSON)
timing = {
    'total_time_s': 450.0,       # Temps total
    'queue_time_s': 440.0,       # Temps en file d'attente
    'qpu_time_s': 3.0,           # Temps QPU réel
    'transpile_time_s': 0.5      # Temps de transpilation
}
```

---

## 6. Analyse des Résultats

### Analyzer Intégrés

```python
# Fidelity Analysis (GHZ)
fidelity_analyzer = FidelityAnalyzer()
fidelity_result = fidelity_analyzer.analyze(
    counts=results[0]['counts'],
    n_qubits=50,
    expected_state='ghz'  # 'ghz', 'bell', ou custom
)
print(f"Fidelity: {fidelity_result['fidelity']:.4f}")

# Entropy Analysis
entropy_analyzer = EntropyAnalyzer()
entropy_result = entropy_analyzer.analyze(counts=results[0]['counts'])
print(f"Shannon Entropy: {entropy_result['shannon_entropy']:.4f} bits")

# Correlation Analysis
corr_analyzer = CorrelationAnalyzer()
corr_result = corr_analyzer.analyze(counts=results[0]['counts'])
print(f"Pairwise correlations: {corr_result['correlations']}")
```

### XEB Analysis (Cross-Entropy Benchmarking)

```python
xeb_analyzer = XEBAnalyzer()

# Analyser les résultats de circuits random
xeb_result = xeb_analyzer.compute_from_circuits(
    circuits=circuits,           # Circuits originaux (non transpilés)
    qpu_results=results          # Résultats du QPU
)
print(f"XEB Fidelity: {xeb_result['xeb_fidelity']:.4f}")
```

### Bell Test Analysis

```python
bell_analyzer = BellAnalyzer()

# Pour circuits Bell/CHSH
bell_result = bell_analyzer.analyze(counts=results[0]['counts'])
print(f"CHSH value: {bell_result.get('chsh_value', 'N/A')}")
print(f"Violation: {bell_result.get('bell_violation', False)}")
```

---

## 7. Circuit Builders Disponibles

### Builders de Base

| Builder | Description | Paramètres |
|---------|-------------|------------|
| `GHZBuilder` | État GHZ (intrication maximale) | `n_qubits`, `add_barriers` |
| `IQPBuilder` | Circuits IQP (#P-hard) | `n_qubits`, `depth` |
| `BellBuilder` | Paires de Bell | `n_pairs` ou `n_qubits` |
| `ClusterBuilder` | États cluster (MBQC) | `n_qubits` |
| `RandomCircuitBuilder` | Circuits aléatoires | `n_qubits`, `depth`, `seed` |
| `QFTBuilder` | Quantum Fourier Transform | `n_qubits`, `inverse` |
| `ParameterizedCircuitBuilder` | Circuits variationnels | `n_qubits`, `n_layers` |

### Builders Algorithmiques

| Builder | Description | Méthode Statique d'Extraction |
|---------|-------------|------------------------------|
| `GroverBuilder` | Algorithme de Grover | - |
| `QPEBuilder` | Phase Estimation | `extract_phase(counts, n_precision)` |
| `DeutschJozsaBuilder` | Deutsch-Jozsa | `interpret_result(counts)` |
| `BernsteinVaziraniBuilder` | Bernstein-Vazirani | `extract_secret(counts)` |
| `SimonBuilder` | Algorithme de Simon | `solve_secret(measurements, n)` |
| `SwapTestBuilder` | SWAP Test (fidélité) | `compute_fidelity(counts)` |
| `QRNGBuilder` | Générateur aléatoire | `extract_random_bytes(counts, n)` |
| `AmplitudeEncodingBuilder` | Encodage d'amplitude | `decode_amplitudes(counts, n)` |
| `TeleportationBuilder` | Téléportation quantique | `verify_teleportation(counts, state)` |

### Exemples d'Utilisation des Builders Algorithmiques

```python
# Deutsch-Jozsa
dj_builder = DeutschJozsaBuilder()
dj_circuit = dj_builder.build(n_qubits=5, oracle_type='balanced')
results = fw.run_on_qpu(dj_circuit, shots=1024)
result_type = DeutschJozsaBuilder.interpret_result(results[0]['counts'])
print(f"Function is: {result_type}")  # 'constant' ou 'balanced'

# Bernstein-Vazirani
bv_builder = BernsteinVaziraniBuilder()
bv_circuit = bv_builder.build(n_qubits=6, secret='10110')
results = fw.run_on_qpu(bv_circuit, shots=1024)
secret = BernsteinVaziraniBuilder.extract_secret(results[0]['counts'])
print(f"Secret found: {secret}")  # '10110'

# QPE (Phase Estimation)
qpe_builder = QPEBuilder()
qpe_circuit = qpe_builder.build(n_precision=4, unitary='T')  # Phase = π/4
results = fw.run_on_qpu(qpe_circuit, shots=4096)
phase = QPEBuilder.extract_phase(results[0]['counts'], n_precision=4)
print(f"Estimated phase: {phase:.4f}")  # ~0.125 (1/8)

# QRNG (Générateur de Nombres Aléatoires)
qrng_builder = QRNGBuilder()
qrng_circuit = qrng_builder.build(n_qubits=8)
results = fw.run_on_qpu(qrng_circuit, shots=1000)
random_bytes = QRNGBuilder.extract_random_bytes(results[0]['counts'], n_bytes=16)
print(f"Random bytes: {random_bytes.hex()}")

# Swap Test (Fidélité entre états)
swap_builder = SwapTestBuilder()
swap_circuit = swap_builder.build(state1=[0], state2=[0])  # Compare |0⟩ et |0⟩
results = fw.run_on_qpu(swap_circuit, shots=4096)
fidelity = SwapTestBuilder.compute_fidelity(results[0]['counts'])
print(f"Fidelity: {fidelity:.4f}")  # ~1.0

# Téléportation
teleport_builder = TeleportationBuilder()
teleport_circuit = teleport_builder.build(state_to_teleport='|+⟩')
results = fw.run_on_qpu(teleport_circuit, shots=4096)
verification = TeleportationBuilder.verify_teleportation(
    results[0]['counts'], 
    expected_state='|+⟩'
)
print(f"Teleportation success: {verification['success']}")
```

---

## 8. Analyzers Disponibles

| Analyzer | Description | Métriques Clés |
|----------|-------------|----------------|
| `FidelityAnalyzer` | Fidélité vs état attendu | `fidelity`, `hellinger_fidelity` |
| `EntropyAnalyzer` | Entropie de Shannon | `shannon_entropy`, `min_entropy` |
| `CorrelationAnalyzer` | Corrélations inter-qubits | `correlations`, `mutual_info` |
| `XEBAnalyzer` | Cross-Entropy Benchmarking | `xeb_fidelity`, `linear_xeb` |
| `BellAnalyzer` | Tests de Bell/CHSH | `chsh_value`, `bell_violation` |
| `RandomnessAnalyzer` | Qualité aléatoire | `nist_tests`, `entropy_rate` |
| `CompressionAnalyzer` | Compressibilité | `compression_ratio` |

### Exemple d'Analyse Complète

```python
from qmc_quantum_framework_v2_6_2 import (
    FidelityAnalyzer, EntropyAnalyzer, CorrelationAnalyzer
)

results = fw.run_on_qpu(circuits, shots=4096)

for i, result in enumerate(results):
    counts = result['counts']
    n_qubits = result.get('n_qubits', 50)
    
    # Fidelity
    fid_analyzer = FidelityAnalyzer()
    fid = fid_analyzer.analyze(counts, n_qubits=n_qubits, expected_state='ghz')
    
    # Entropy
    ent_analyzer = EntropyAnalyzer()
    ent = ent_analyzer.analyze(counts)
    
    # Correlation
    corr_analyzer = CorrelationAnalyzer()
    corr = corr_analyzer.analyze(counts)
    
    print(f"Circuit {i}:")
    print(f"  Fidelity: {fid['fidelity']:.4f}")
    print(f"  Entropy: {ent['shannon_entropy']:.2f} bits")
    print(f"  Avg Correlation: {corr.get('avg_correlation', 'N/A')}")
```

---

## 9. Fonctionnalités Avancées

### Transpilation Personnalisée

```python
# Transpiler avec options avancées
transpiled = fw.transpile_circuits(
    circuits,
    optimization_level=3,          # 0-3 (3 = max optimisation)
    layout_strategy='topology_aware'
)

# Analyser la transpilation
from qmc_quantum_framework_v2_6_2 import QiskitTranspilerWrapper

analysis = QiskitTranspilerWrapper.analyze_transpilation(
    original_circuit=circuits[0],
    transpiled_circuit=transpiled[0]
)
print(f"Depth reduction: {analysis['depth_reduction']}%")
print(f"2Q gates: {analysis['original_2q_gates']} → {analysis['transpiled_2q_gates']}")
```

### Mitigation d'Erreurs

```python
from qmc_quantum_framework_v2_6_2 import MitigationConfig

# Configuration de mitigation
mitigation = MitigationConfig(
    resilience_level=2,            # 0-2 (2 = max mitigation)
    zne_enabled=True,              # Zero Noise Extrapolation
    pec_enabled=False,             # Probabilistic Error Cancellation
    dynamical_decoupling=True      # DD sequences
)

# Appliquer lors de l'exécution (via Qiskit Runtime options)
```

### Sauvegarde et Chargement des Résultats

```python
# Les archives JSON sont automatiquement générées
# Chemin: qmc_runs/{run_dir}/archive_{timestamp}_{job_id}_{status}.json

# Charger une archive
import json
with open('archive_20260123_010232_d5pbhngh0i0s_OK.json', 'r') as f:
    archive = json.load(f)

# Contenu de l'archive
results = archive['results']           # Liste des résultats
config = archive['config']             # Configuration utilisée
calibration = archive['calibration']   # Données de calibration
timing = archive['timing']             # Informations de timing
```

### Chemin Optimal de Qubits

```python
# Obtenir le meilleur chemin de qubits contigus
topology = fw.analyze_calibration()
best_path = topology.get_best_path(n_qubits=50)
print(f"Meilleur chemin de 50 qubits: {best_path}")
print(f"Start: Q{best_path[0]}, End: Q{best_path[-1]}")
```

---

## 10. Exemples Complets

### Exemple 1 : Test GHZ Multi-Échelle

```python
from qmc_quantum_framework_v2_6_2 import QMCFramework, GHZBuilder, FidelityAnalyzer

# Initialiser
fw = QMCFramework(backend_name="ibm_torino", project="GHZ_Test")
fw.connect()

# Analyser la calibration
topology = fw.analyze_calibration()

# Créer circuits GHZ à différentes échelles
builder = GHZBuilder(topology=topology)
circuits = builder.build_batch(scales=[10, 25, 50, 75, 100])

# Exécuter avec confirmation
results = fw.run_on_qpu_with_confirm(
    circuits, 
    shots=4096,
    description="Test GHZ scaling 10-100 qubits"
)

# Analyser les résultats
analyzer = FidelityAnalyzer()
for i, result in enumerate(results):
    n_qubits = [10, 25, 50, 75, 100][i]
    fid_result = analyzer.analyze(
        result['counts'], 
        n_qubits=n_qubits,
        expected_state='ghz'
    )
    print(f"GHZ-{n_qubits}: Fidelity = {fid_result['fidelity']:.4f}")
```

### Exemple 2 : Algorithme de Grover

```python
from qmc_quantum_framework_v2_6_2 import QMCFramework, GroverBuilder

fw = QMCFramework(backend_name="ibm_torino", project="Grover")
fw.connect()

# Créer circuit Grover (recherche de |11⟩ dans 4 éléments)
builder = GroverBuilder()
circuit = builder.build(
    n_qubits=2,
    marked_states=['11'],  # État(s) à trouver
    n_iterations=1         # √N iterations optimal
)

# Exécuter
results = fw.run_on_qpu(circuit, shots=4096)

# Analyser
counts = results[0]['counts']
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
print(f"Most frequent state: {sorted_counts[0][0]} ({sorted_counts[0][1]} counts)")
# Devrait être '11' avec haute probabilité
```

### Exemple 3 : Générateur de Nombres Aléatoires Quantiques

```python
from qmc_quantum_framework_v2_6_2 import QMCFramework, QRNGBuilder

fw = QMCFramework(backend_name="ibm_torino", project="QRNG")
fw.connect()

# Créer circuit QRNG (8 bits par shot)
builder = QRNGBuilder()
circuit = builder.build(n_qubits=8)

# Exécuter plusieurs fois pour générer des données
results = fw.run_on_qpu(circuit, shots=10000)

# Extraire les bytes aléatoires
random_bytes = QRNGBuilder.extract_random_bytes(
    results[0]['counts'], 
    n_bytes=1000
)

# Sauvegarder
with open('quantum_random.bin', 'wb') as f:
    f.write(random_bytes)

print(f"Generated {len(random_bytes)} random bytes")
print(f"Preview: {random_bytes[:16].hex()}")
```

### Exemple 4 : Benchmarking XEB

```python
from qmc_quantum_framework_v2_6_2 import (
    QMCFramework, RandomCircuitBuilder, XEBAnalyzer
)

fw = QMCFramework(backend_name="ibm_torino", project="XEB_Benchmark")
fw.connect()

# Créer circuits random pour XEB
builder = RandomCircuitBuilder()
circuits = []
for depth in [5, 10, 15, 20]:
    circuit = builder.build(n_qubits=20, depth=depth, seed=42+depth)
    circuits.append(circuit)

# Exécuter
results = fw.run_on_qpu(circuits, shots=4096)

# Analyser avec XEB
xeb = XEBAnalyzer()
xeb_results = xeb.compute_from_circuits(circuits, results)

print(f"XEB Fidelity: {xeb_results['xeb_fidelity']:.4f}")
print(f"Linear XEB: {xeb_results['linear_xeb']:.4f}")
```

### ★ Exemple 5 (NEW v2.6.2) : Exécution avec Upload QMC Archive

```python
from qmc_quantum_framework_v2_6_2 import QMCFramework, GHZBuilder

# Configuration via .env:
# QMC_ARCHIVE_URL=https://archive.qmc-lab.com
# QMC_ARCHIVE_TOKEN=your_api_token
# QMC_ARCHIVE_DEFAULT_PROJECTS=project-uuid-1,project-uuid-2

fw = QMCFramework(backend_name="ibm_torino", project="HAWKING_Palier3")
fw.connect()

builder = GHZBuilder(topology=fw.topology)
circuit = builder.build(n_qubits=50)

# Exécuter avec upload automatique vers QMC Archive
results = fw.run_on_qpu(
    circuit,
    shots=4096,
    generate_archive=True,          # Génère le JSON local
    upload_to_archive=True,         # Upload vers le cloud
    archive_projects=['abc123'],    # Projet spécifique (optionnel)
    archive_notes="Expérience HAWKING Palier 3 - GHZ 50 qubits"  # Notes personnalisées
)

# Le framework affiche automatiquement:
# [QMC Archive] ✅ Uploaded: archive_20260126_143022_xxxxx_OK.json → Task abc12345... (1 projects)
```

### ★ Exemple 6 (NEW v2.6.2) : Upload Manuel vers QMC Archive

```python
from qmc_quantum_framework_v2_6_2 import QMCArchiveUploader

# Uploader une archive existante manuellement
uploader = QMCArchiveUploader(
    api_url="https://archive.qmc-lab.com",
    api_token="your_api_token",
    default_projects=["project-uuid-1"]
)

# Vérifier si l'upload est possible
if uploader.is_enabled():
    result = uploader.upload(
        file_path="archive_20260126_143022_xxxxx_OK.json",
        project_ids=["project-uuid-1", "project-uuid-2"],
        notes="Upload manuel - Données HAWKING",
        max_retries=3,
        timeout=30
    )
    
    # Afficher le résultat
    uploader.print_upload_report(result)
    
    if result['success']:
        print(f"✅ Upload réussi! Task ID: {result['task_id']}")
    else:
        print(f"❌ Échec: {result['error']}")
else:
    print("Upload désactivé (pas de token configuré)")
```

---

## 11. Gestion des Erreurs

### Exceptions Disponibles

```python
from qmc_quantum_framework_v2_6_2 import (
    QMCException,           # Base exception
    QMCConnectionError,     # Erreur de connexion
    QMCCredentialsError,    # Token invalide
    QMCBackendError,        # Backend non disponible
    QMCTranspilationError,  # Erreur transpilation
    QMCExecutionError,      # Erreur exécution job
    QMCTimeoutError,        # Timeout dépassé
    QMCJobCancelledError,   # Job annulé
    QMCCircuitError,        # Circuit invalide
    QMCCalibrationError,    # Erreur calibration
)
```

### Gestion des Erreurs

```python
from qmc_quantum_framework_v2_6_2 import (
    QMCFramework, QMCConnectionError, QMCExecutionError, QMCTimeoutError
)

try:
    fw = QMCFramework(backend_name="ibm_torino", project="Test")
    fw.connect()
    
    results = fw.run_on_qpu(circuits, shots=4096, timeout=3600)
    
except QMCConnectionError as e:
    print(f"❌ Connexion échouée: {e}")
    print(f"   Backend: {e.backend}")
    
except QMCTimeoutError as e:
    print(f"⏰ Timeout: {e}")
    print(f"   Job ID: {e.job_id}")
    print(f"   Timeout: {e.timeout_s}s")
    
except QMCExecutionError as e:
    print(f"💥 Erreur exécution: {e}")
    print(f"   Job ID: {e.job_id}")
```

---

## 12. Référence API Rapide

### QMCFramework - Méthodes Principales

| Méthode | Description | Retour |
|---------|-------------|--------|
| `connect()` | Se connecter au backend | `bool` |
| `analyze_calibration()` | Analyser la calibration QPU | `DynamicTopology` |
| `run_on_qpu(circuits, shots)` | Exécuter sur QPU | `List[Dict]` |
| `run_on_qpu_with_confirm(...)` | Exécuter avec confirmation | `List[Dict]` |
| `transpile_circuits(circuits)` | Transpiler les circuits | `List[QuantumCircuit]` |
| `run_local(circuits, shots)` | Simuler localement | `List[Dict]` |

### Format des Résultats

```python
result = {
    'counts': Dict[str, int],      # {'00000': 2048, '11111': 2048}
    'shots': int,                   # 4096
    'circuit_name': str,            # 'ghz_50'
    'n_qubits': int,                # 50
    'job_id': str,                  # 'd5pbhngh0i0s73ep1j10'
    'backend': str,                 # 'ibm_torino'
}
```

### Builders - Paramètres Communs

```python
builder.build(
    n_qubits: int,          # Nombre de qubits
    add_barriers: bool,     # Ajouter des barrières visuelles
    add_measurements: bool, # Ajouter mesures (défaut: True)
    **kwargs                # Paramètres spécifiques au builder
)

builder.build_batch(
    scales: List[int],      # Liste de tailles [10, 25, 50, 100]
    **kwargs                # Paramètres passés à build()
)
```

### Analyzers - Interface Commune

```python
analyzer.analyze(
    counts: Dict[str, int], # Counts du résultat
    **kwargs                # Paramètres spécifiques
) -> Dict                   # Résultats d'analyse
```

---

## 13. ★ QMC Archive Manager (v2.6.2)

### Vue d'Ensemble

La version 2.6.2 introduit **QMC Archive Manager**, un système d'upload automatique des archives JSON vers un serveur cloud pour centraliser et organiser les résultats expérimentaux.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW QMC ARCHIVE MANAGER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   run_on_qpu()                                                              │
│       │                                                                     │
│       ▼                                                                     │
│   [1] Exécution sur QPU IBM                                                 │
│       │                                                                     │
│       ▼                                                                     │
│   [2] Génération archive JSON locale (v3.1, 41 sections)                    │
│       │                                                                     │
│       ▼                                                                     │
│   [3] Upload automatique vers QMC Archive Manager (si configuré)            │
│       │   • Retry 3x avec backoff exponentiel (2s, 4s, 8s)                  │
│       │   • Non-bloquant: échec n'interrompt pas le script                 │
│       │                                                                     │
│       ▼                                                                     │
│   [4] Génération rapport HTML                                               │
│       │                                                                     │
│       ▼                                                                     │
│   [5] Retour des résultats                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Variables d'Environnement

| Variable | Type | Défaut | Description |
|----------|------|--------|-------------|
| `QMC_ARCHIVE_URL` | `str` | `http://localhost:4000` | URL de l'API QMC Archive Manager |
| `QMC_ARCHIVE_TOKEN` | `str` | `""` | Token d'authentification (requis pour activer l'upload) |
| `QMC_ARCHIVE_UPLOAD` | `bool` | `true` | Active/désactive l'upload automatique |
| `QMC_ARCHIVE_DEFAULT_PROJECTS` | `str` | `""` | Liste d'UUIDs séparés par virgule |

### Classe QMCArchiveUploader

```python
from qmc_quantum_framework_v2_6_2 import QMCArchiveUploader, get_archive_uploader

# Méthode 1: Utiliser l'instance globale (recommandé)
uploader = get_archive_uploader()

# Méthode 2: Créer une instance personnalisée
uploader = QMCArchiveUploader(
    api_url="https://archive.qmc-lab.com",     # URL de l'API
    api_token="your_api_token",                 # Token d'auth
    default_projects=["uuid1", "uuid2"],        # Projets par défaut
    enabled=True,                               # Force activation
    logger=my_logger                            # Logger personnalisé
)
```

### Méthodes Disponibles

| Méthode | Description | Retour |
|---------|-------------|--------|
| `is_enabled()` | Vérifie si l'upload est possible | `bool` |
| `upload(file_path, ...)` | Upload un fichier vers l'API | `Dict` |
| `print_upload_report(result)` | Affiche le rapport d'upload | `None` |
| `get_status_summary()` | Résumé de la dernière opération | `Dict` |

### Méthode upload() - Signature Complète

```python
def upload(
    file_path: str,                    # Chemin vers le fichier JSON
    project_ids: List[str] = None,     # UUIDs des projets (ou None pour defaults)
    notes: str = None,                 # Notes personnalisées (ou None pour auto)
    job_id: str = None,                # Job ID pour notes auto
    extra_info: Dict = None,           # Infos supplémentaires pour notes
    max_retries: int = 3,              # Nombre de tentatives
    timeout: int = 30                  # Timeout par requête (secondes)
) -> Dict:
    """
    Returns:
        {
            'success': bool,           # True si upload réussi
            'task_id': str | None,     # ID de la tâche créée
            'filename': str,           # Nom du fichier
            'projects_assigned': int,  # Nombre de projets assignés
            'attempts': int,           # Nombre de tentatives effectuées
            'error': str | None        # Message d'erreur si échec
        }
    """
```

### Génération Automatique des Notes

Si `notes` n'est pas fourni, le framework génère automatiquement :

```
Job: d5pbhngh0i0s73ep1j10 | Date: 2026-01-26 14:30:22 | Backend: ibm_torino | Circuits: 5
```

### Gestion des Erreurs (Non-Bloquant)

L'upload QMC Archive est **non-bloquant**. En cas d'échec :

1. Le framework log un warning
2. Les données locales (archive JSON) sont préservées
3. Le script continue normalement
4. Les résultats QPU sont retournés

```python
# Même si l'upload échoue, le script continue:
results = fw.run_on_qpu(circuits, shots=4096, upload_to_archive=True)
# [QMC Archive] ⚠️ Upload error (non-blocking): Connection refused
# → results contient quand même les données QPU
```

### Cas d'Erreurs Gérés

| Situation | Comportement | Retry |
|-----------|--------------|-------|
| Pas de token configuré | Désactivé silencieusement | Non |
| `QMC_ARCHIVE_UPLOAD=false` | Désactivé explicitement | Non |
| Fichier inexistant | Retourne erreur | Non |
| Token invalide (401) | Retourne erreur | Non |
| Fichier trop grand (413) | Retourne erreur | Non |
| Timeout | Retry avec backoff | Oui (3x) |
| Erreur connexion | Retry avec backoff | Oui (3x) |
| Erreur serveur (500) | Retry avec backoff | Oui (3x) |

### Exemple Complet avec Gestion d'Erreurs

```python
from qmc_quantum_framework_v2_6_2 import QMCFramework, QMCArchiveUploader

# Vérifier la configuration avant exécution
uploader = QMCArchiveUploader()

if uploader.is_enabled():
    print("✅ QMC Archive Manager configuré")
    print(f"   URL: {uploader.api_url}")
    print(f"   Projets par défaut: {uploader.default_projects}")
else:
    print("⚠️ QMC Archive Manager non configuré (pas de token)")
    print("   → Les archives seront sauvegardées localement uniquement")

# Exécuter normalement
fw = QMCFramework(backend_name="ibm_torino", project="Test")
fw.connect()

results = fw.run_on_qpu(
    circuits,
    shots=4096,
    upload_to_archive=True,  # Tentera l'upload si configuré
    archive_notes="Test avec vérification préalable"
)

# Vérifier le résultat de l'upload (si disponible dans run_context)
# L'upload n'affecte PAS le retour de run_on_qpu()
```

---

## 14. ★ QMC Accounts Audit (v2.6.3)

### Vue d'Ensemble

La version 2.6.3 introduit un **module d'audit complet** pour analyser l'utilisation QPU de plusieurs comptes IBM Quantum, avec génération de rapports HTML professionnels style IBM Carbon Design System.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WORKFLOW QMC ACCOUNTS AUDIT                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [1] Récupération des comptes depuis .env                                  │
│       • IBM_API_KEY_<LABEL>=<token>                                         │
│       • IBM_API_KEY_ACTIVE_<LABEL>=<token>                                  │
│                                                                             │
│   [2] Connexion à chaque compte IBM Quantum                                 │
│                                                                             │
│   [3] Collecte des jobs (30 jours par défaut)                               │
│       • Status, backend, usage, dates                                       │
│       • Statistiques agrégées par compte                                    │
│                                                                             │
│   [4] Génération des rapports                                               │
│       • JSON: données brutes complètes                                      │
│       • HTML: rapport visuel avec graphiques Chart.js                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Usage via QMCFramework (Recommandé)

```python
from qmc_quantum_framework_v2_6_3 import QMCFramework

fw = QMCFramework(backend_name="ibm_torino", project="Audit")

# Audit automatique de tous les comptes dans .env
result = fw.audit_accounts(
    window_days=30,           # Période d'analyse (jours)
    budget_minutes=10.0,      # Budget QPU par compte
    generate_html=True,       # Générer rapport HTML
    generate_json=True,       # Générer fichier JSON
    output_dir="qmc_audit"    # Répertoire de sortie
)

# Accès aux résultats
print(f"Total jobs: {result['global_stats']['total_jobs']}")
print(f"Usage total: {result['global_stats']['total_usage_minutes']:.2f} min")
print(f"Rapport HTML: {result['generated_files']['html']}")
```

### Usage via Fonction Standalone

```python
from qmc_quantum_framework_v2_6_3 import (
    run_accounts_audit,
    get_all_ibm_accounts_from_env
)

# Lister les comptes disponibles
accounts = get_all_ibm_accounts_from_env()
print(f"Comptes trouvés: {list(accounts.keys())}")

# Lancer l'audit
result = run_accounts_audit(
    accounts=accounts,        # Ou None pour auto-détection
    window_days=30,
    limit=500,                # Max jobs par compte
    backend_name=None,        # Filtrer par backend (optionnel)
    budget_minutes=10.0,
    output_dir="qmc_audit",
    generate_html=True,
    generate_json=True,
    verbose=True
)
```

### Usage avec Comptes Personnalisés

```python
# Définir les comptes manuellement
accounts = {
    'main': {
        'token': 'your_main_token',
        'channel': 'ibm_quantum_platform'
    },
    'research': {
        'token': 'your_research_token',
        'channel': 'ibm_quantum_platform',
        'instance': 'crn:v1:bluemix:public:quantum-computing:...'
    }
}

result = fw.audit_accounts(accounts=accounts, budget_minutes=15.0)
```

### Configuration Multi-Comptes (.env)

```env
# Format 1: IBM_API_KEY_<LABEL>
IBM_API_KEY_MAIN=abc123...
IBM_API_KEY_BACKUP=def456...

# Format 2: IBM_API_KEY_ACTIVE_<LABEL> (prioritaire)
IBM_API_KEY_ACTIVE_RESEARCH=ghi789...

# Optionnel: Instance/CRN par compte
IBM_CRN_MAIN=crn:v1:bluemix:public:quantum-computing:...
IBM_INSTANCE_RESEARCH=crn:v1:bluemix:public:quantum-computing:...

# Optionnel: Channel par compte (défaut: ibm_quantum_platform)
IBM_CHANNEL_MAIN=ibm_quantum_platform
```

### Classes Disponibles

| Classe | Description |
|--------|-------------|
| `QMCJobDataCollector` | Collecte les données de jobs de tous les comptes |
| `QMCAuditHTMLReportGenerator` | Génère des rapports HTML style IBM Carbon |

### Fonctions Disponibles

| Fonction | Description |
|----------|-------------|
| `get_all_ibm_accounts_from_env()` | Récupère tous les comptes depuis .env |
| `run_accounts_audit(...)` | Point d'entrée principal pour l'audit |

### Méthodes QMCFramework

| Méthode | Description |
|---------|-------------|
| `fw.audit_accounts(...)` | Lance un audit via l'instance framework |
| `fw.list_ibm_accounts()` | Liste les comptes configurés dans .env |

### Format des Résultats

```python
result = {
    'report_title': 'QMC Quantum Accounts - Full Audit Report',
    'collection_date': '2026-01-26T14:30:22',
    'window_days': 30,
    'accounts': {
        'main': {
            'label': 'main',
            'collection_status': 'success',
            'jobs': [
                {
                    'job_id': 'd5pbhngh0i0s73ep1j10',
                    'status': 'DONE',
                    'backend': 'ibm_torino',
                    'usage_seconds': 12.5,
                    'creation_date': '2026-01-25T10:30:00',
                    ...
                },
                ...
            ],
            'stats': {
                'jobs_count': 42,
                'usage_seconds': 318.5,
                'usage_minutes': 5.31,
                'avg_usage_per_job': 7.58,
                'by_status': {'DONE': 40, 'ERROR': 2},
                'by_backend': {'ibm_torino': 30, 'ibm_fez': 12},
                'jobs_per_day': {'2026-01-25': 15, '2026-01-24': 12, ...},
                'usage_per_day': {'2026-01-25': 120.5, ...}
            },
            'errors': []
        },
        'backup': {...}
    },
    'global_stats': {
        'total_accounts': 2,
        'total_jobs': 150,
        'total_usage_seconds': 750.0,
        'total_usage_minutes': 12.5,
        'by_status': {'DONE': 140, 'ERROR': 10},
        'by_backend': {'ibm_torino': 100, 'ibm_fez': 50},
        'jobs_per_day': {...},
        'usage_per_day': {...}
    },
    'generated_files': {
        'html': 'qmc_audit/qmc_accounts_audit_20260126_143022.html',
        'json': 'qmc_audit/audit_20260126_143022.json'
    }
}
```

### Rapport HTML

Le rapport HTML généré inclut:

- **Métriques globales**: nombre de comptes, jobs totaux, usage QPU, budget restant
- **Graphique Usage par Compte**: barres comparant usage vs budget
- **Graphique Timeline**: évolution de l'usage sur 14 jours
- **Graphique Statuts**: répartition des jobs par statut (DONE, ERROR, etc.)
- **Graphique Backends**: distribution des jobs par backend
- **Table des Comptes**: avec indicateurs visuels (🟢 Healthy, 🟡 Warning, 🔴 Critical)
- **Table des Jobs Récents**: 30 derniers jobs avec statut coloré

Le style utilise **IBM Carbon Design System** (White Theme) pour un rendu professionnel.

### Exemple Complet

```python
from qmc_quantum_framework_v2_6_3 import QMCFramework

# Initialiser le framework
fw = QMCFramework(backend_name="ibm_torino", project="MonitoringQPU")

# Lister les comptes détectés
accounts = fw.list_ibm_accounts()
print(f"Comptes détectés: {list(accounts.keys())}")

# Lancer l'audit complet
result = fw.audit_accounts(
    window_days=30,
    budget_minutes=10.0,
    generate_html=True,
    output_dir="monthly_audit"
)

# Afficher le résumé
gs = result['global_stats']
print(f"\n📊 RÉSUMÉ GLOBAL")
print(f"   Comptes: {gs['total_accounts']}")
print(f"   Jobs: {gs['total_jobs']}")
print(f"   Usage: {gs['total_usage_minutes']:.2f} minutes")

# Détails par compte
for label, acc in result['accounts'].items():
    stats = acc['stats']
    print(f"\n   {label.upper()}:")
    print(f"      Jobs: {stats['jobs_count']}")
    print(f"      Usage: {stats['usage_minutes']:.2f} min")
    
# Ouvrir le rapport HTML
import webbrowser
webbrowser.open(result['generated_files']['html'])
```

---

## 15. Notes Importantes

1. **Token IBM Quantum** : Obtenez votre token sur [quantum.ibm.com](https://quantum.ibm.com)

2. **Coûts QPU** : Les exécutions QPU consomment des crédits IBM. Utilisez `run_on_qpu_with_confirm()` pour voir l'estimation avant exécution.

3. **Rapports Automatiques** : Un rapport HTML et une archive JSON sont générés automatiquement après chaque exécution QPU.

4. **Optimisation** : Utilisez `analyze_calibration()` pour identifier les meilleurs qubits avant de construire vos circuits.

5. **Transpilation** : Laissez `auto_transpile=True` pour une transpilation optimale par Qiskit.

6. **QMC Archive (v2.6.2)** : L'upload cloud est non-bloquant et ne nécessite pas de configuration pour fonctionner en mode local uniquement.

7. **★ QMC Accounts Audit (v2.6.3)** : Audit multi-comptes intégré avec rapports HTML style IBM Carbon.

---

## 16. Changelog

### v2.6.3 (Janvier 2026)

- ★ **QMC Accounts Audit Module**
  - Nouvelle classe `QMCJobDataCollector` pour collecter les données multi-comptes
  - Nouvelle classe `QMCAuditHTMLReportGenerator` pour rapports HTML IBM Carbon
  - Nouvelle fonction `get_all_ibm_accounts_from_env()` pour auto-détection des comptes
  - Nouvelle fonction `run_accounts_audit()` comme point d'entrée principal
  - Nouvelle méthode `QMCFramework.audit_accounts()` pour usage simplifié
  - Nouvelle méthode `QMCFramework.list_ibm_accounts()` pour lister les comptes
  - Support multi-patterns: `IBM_API_KEY_<LABEL>` et `IBM_API_KEY_ACTIVE_<LABEL>`
  - Rapports HTML avec graphiques Chart.js (usage, timeline, statuts, backends)
  - Export JSON complet des données d'audit
  - Statistiques agrégées: par compte, par backend, par jour, par statut

### v2.6.2 (Janvier 2026)

- ★ **QMC Archive Manager Integration**
  - Nouvelle classe `QMCArchiveUploader` pour upload cloud
  - Variables d'environnement: `QMC_ARCHIVE_URL`, `QMC_ARCHIVE_TOKEN`, `QMC_ARCHIVE_UPLOAD`, `QMC_ARCHIVE_DEFAULT_PROJECTS`
  - Nouveaux paramètres `run_on_qpu()`: `upload_to_archive`, `archive_projects`, `archive_notes`
  - Upload automatique non-bloquant avec retry (3x, backoff exponentiel)
  - Génération automatique des notes (Job ID + Date + Backend)
  - Fonction globale `get_archive_uploader()`

### v2.6.1 (Janvier 2026)

- ✅ Auto-fetch QPU state avant `run_on_qpu()`
- ✅ Variable `QMC_SKIP_QPU_STATE_FETCH` pour désactiver
- ✅ Correction initialisation `fw.topology`

### v2.6.0 (Janvier 2026)

- ✅ Correction récupération données 2Q Gate depuis `backend.target`
- ✅ Correction date de calibration (Last calibration)
- ✅ Nouvelle visualisation "Maximum Contiguous Good Qubits"
- ✅ Support Qiskit Runtime v2 / Qiskit 1.0+
- ✅ Estimation temps QPU avec formule IBM officielle
- ✅ **Mise à jour backends IBM (Janvier 2026)**
  - Nouveaux: `ibm_boston`, `ibm_pittsburgh`, `ibm_kingston`, `ibm_miami`
  - `ibm_torino` est Heron r1 (pas Eagle)
  - `ibm_miami` est Nighthawk r1 (nouvelle architecture)
  - Tous les backends utilisent CZ (plus de ECR)

---

## Types de Processeurs IBM

| Type | Génération | Gate 2Q | CLOPS | Notes |
|------|------------|---------|-------|-------|
| **Heron r3** | 2025 | CZ | 330-340k | Dernière génération, meilleure qualité |
| **Heron r2** | 2024 | CZ | 300-340k | Très performant |
| **Heron r1** | 2024 | CZ | 290k | Première génération Heron |
| **Nighthawk r1** | 2025 | CZ | 24k | Nouvelle architecture expérimentale |

> **Note:** Les processeurs Eagle (ECR gate) ne sont plus disponibles sur le plan open-instance.

---

## Référence Rapide des Nouvelles Fonctionnalités

### v2.6.3 - QMC Accounts Audit

```python
# Via QMCFramework
fw = QMCFramework(backend_name="ibm_torino")
result = fw.audit_accounts(window_days=30, budget_minutes=10.0)
accounts = fw.list_ibm_accounts()

# Via fonctions standalone
from qmc_quantum_framework_v2_6_3 import run_accounts_audit, get_all_ibm_accounts_from_env
accounts = get_all_ibm_accounts_from_env()
result = run_accounts_audit(accounts=accounts)
```

### v2.6.2 - QMC Archive Manager

```python
# Upload automatique lors de run_on_qpu
results = fw.run_on_qpu(circuits, upload_to_archive=True, archive_notes="Mon expérience")

# Upload manuel
from qmc_quantum_framework_v2_6_3 import QMCArchiveUploader
uploader = QMCArchiveUploader()
result = uploader.upload("archive.json", project_ids=["uuid1"])
```

---

*Documentation générée pour QMC Quantum Framework v2.6.3*
*Compatible avec Qiskit 1.0+ et IBM Quantum Runtime*
*QMC Archive Manager + QMC Accounts Audit intégrés*
