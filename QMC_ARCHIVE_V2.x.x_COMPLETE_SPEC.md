# QMC Archive JSON v3.1 - SPÉCIFICATION COMPLÈTE

> **Produit par** : QMC Quantum Framework **v2.7.1** (classe `ExecutionArchive`).
> Le **format d'archive reste v3.1.0** (rétro-compatible) ; v2.7.1 ajoute la compression par défaut,
> des écritures atomiques, la redaction des secrets et quelques nouveaux champs (voir « Mise à jour v2.7.1 »).

## Informations Générales

| Attribut | Valeur |
|----------|--------|
| **Schema version** | `3.1.0` |
| **Format** | `QMC_EXECUTION_ARCHIVE_V3` |
| **Min Parser** | `3.0.0` |
| **Framework** | `2.7.1` (champ `_schema.framework_version`) |
| **Sections** | 41 |
| **Compression** | **gzip par défaut** → fichier `archive_*.json.gz` (`compress=True`, ~80 % plus petit) |
| **Taille typique** | 100-800 KB (non compressé) · ~20-160 KB (gzip) |

---

## 🆕 Mise à jour v2.7.1 (ce qui change vs v2.6.x)

Le **schéma d'archive est inchangé (v3.1.0, 41 sections)** : tout parser v3.x reste compatible. Les évolutions
v2.7.1 portent sur la **production** de l'archive et l'**enrichissement** de certaines sections.

### Production de l'archive
| Évolution | Détail |
|-----------|--------|
| **Compression par défaut** | `ExecutionArchive(compress=True)` → fichier **`.json.gz`** (gzip). Pour du JSON brut : `compress=False`. |
| **Écritures atomiques** | Tous les JSON (archive, session, rapports) sont écrits via `temp + fsync + os.replace` → pas de fichier corrompu en cas de crash. |
| **Permissions restrictives** | Fichiers sensibles en `0o600`, répertoires de run en `0o700` (POSIX). |
| **Redaction des secrets** | Tokens IBM/QMC masqués dans `session_logs`, `environment_vars` et tout message — voir `_redact_secrets`. |
| **`framework_version`** | `_schema.framework_version` et `metadata.framework_version` = **`2.7.1`**. |
| **`integrity.circuits_hash`** | Couvre désormais **TOUS** les circuits (auparavant les 20 premiers). |

### Sections enrichies (nouveaux champs)
| Section | Nouveaux champs v2.7.1 |
|---------|------------------------|
| **§22 `results[]`** | `result_type` (`"sampler"`/`"estimator"`) ; pour multi-registres : `register_counts` + `primary_register` (plus de fusion par sommation) ; pour Estimator multi-observables : `expectation_value` (scalaire **ou liste**) + `expectation_values`, `std_errors`, `n_observables`. *(Tous les champs additionnels du résultat sont préservés.)* |
| **Calibration interne (`NoiseAnalyzer`)** | Le résumé de calibration peuple désormais réellement `gate_2q` `{mean, min, max, count}` (erreur 2-qubits) — auparavant absent, ce qui rendait l'estimation EPLG constante. *(La §9 `gates_calibration` exposait déjà `avg/min/max_2q_error`.)* |
| **§32 `analysis_results.randomness`** | Les espaces séparateurs de registres ne sont plus comptés comme bits ; ajout de `n_qubits` ; ratios `ones/zeros/balance` corrigés. |
| **Analyzers (FidelityAnalyzer / XEBAnalyzer)** | Barres d'erreur : `std_error` + `ci_95` (fidélité) ; `xeb_stderr`, `xeb_ci95`, `xeb_normalized_stderr` (XEB). `quantum_signature` ne passe à `true` que si la borne inférieure de l'IC reste > 0. |

> ⚠️ **Note crypto** : le champ `quantum_entropy_bits` (protocoles QMC) reflète désormais une **min-entropie**
> réelle (NIST SP 800-90B) ; les primitives crypto sont réelles (AES-256-GCM/HKDF, ZKP, RSW) en v2.7.1.

---

## Structure Complète (41 Sections)

```
archive.json
├── _schema                    # Section 0: Versioning
├── metadata                   # Section 1: Identification
├── system_info                # Section 2: Environnement système
├── python_env                 # Section 3: Python
├── dependencies               # Section 4: Librairies
├── environment_vars           # Section 5: Variables env
├── ibm_account                # Section 6: Compte IBM
├── backend                    # Section 7: Backend info
├── qpu_state                  # Section 8: État QPU complet
├── gates_calibration          # Section 9: Calibration gates
├── topology                   # Section 10: Topologie
├── calibration_health         # Section 11: Santé calibration
├── framework_config           # Section 12: Config framework
├── quality_thresholds         # Section 13: Seuils qualité
├── circuits_original          # Section 14: Circuits originaux
├── circuits_transpiled        # Section 15: Circuits transpilés
├── transpilation_config       # Section 16: Config transpilation
├── layout_mapping             # Section 17: Mapping layout
├── mitigation_config          # Section 18: Config mitigation
├── sampler_options            # Section 19: Options sampler
├── execution                  # Section 20: Info exécution
├── job_metadata               # Section 21: Metadata job
├── results                    # Section 22: Résultats
├── raw_memory                 # Section 23: Shots bruts
├── statistics                 # Section 24: Statistiques
├── session_logs               # Section 25: Logs
├── warnings                   # Section 26: Warnings
├── pre_execution_estimates    # Section 27: Estimations
├── error                      # Section 28: Erreur si échec
├── backend_extended           # Section 29: Backend étendu
├── usage_and_costs            # Section 30: Usage/coûts
├── transpilation_detailed     # Section 31: Transpilation détaillée
├── analysis_results           # Section 32: Analyses
├── timing_detailed            # Section 33: Timing détaillé
├── reproducibility            # Section 34: Reproductibilité
├── qubits_analysis            # Section 35: Analyse qubits
├── connections_detailed       # Section 36: Connexions 2Q
├── network_info               # Section 37: Réseau
├── process_info               # Section 38: Process
├── qdna_fingerprint           # Section 39: QDNA
└── integrity                  # Section 40: Checksums
```

---

## SECTION 0: `_schema`

**Description:** Version et format de l'archive. TOUJOURS EN PREMIER.

```json
{
  "_schema": {
    "version": "3.1.0",
    "format": "QMC_EXECUTION_ARCHIVE_V3",
    "min_parser_version": "3.0.0",
    "created_by": "QMC Framework",
    "framework_version": "2.7.1",
    "spec_url": "https://docs.qmc-lab.com/archive-schema/v3"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `version` | string | Version SemVer du schéma (3.1.0) |
| `format` | string | Identifiant format (QMC_EXECUTION_ARCHIVE_V3) |
| `min_parser_version` | string | Version min du parser requis |
| `created_by` | string | Créateur de l'archive |
| `framework_version` | string | Version du framework QMC |
| `spec_url` | string | URL de la spécification |

---

## SECTION 1: `metadata`

**Description:** Identification unique de l'exécution.

```json
{
  "metadata": {
    "execution_id": "550e8400-e29b-41d4-a716-446655440000",
    "project": "QMC_FULL_VALIDATION",
    "run_name": "qpu_20260123_174035_QMC_FULL_VALIDATION",
    "status": "COMPLETED",
    "created_at": "2026-01-23T17:40:35.123456",
    "completed_at": "2026-01-23T17:41:33.456789",
    "duration_seconds": 58.33,
    "framework_version": "2.7.1",
    "user": "chistelle",
    "hostname": "WORKSTATION-01",
    "tags": ["validation", "full_test", "v2.7.1"]
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `execution_id` | string (UUID) | Identifiant unique de l'exécution |
| `project` | string | Nom du projet |
| `run_name` | string | Nom du run (répertoire) |
| `status` | string | COMPLETED, ERROR, CANCELLED |
| `created_at` | string (ISO) | Timestamp début |
| `completed_at` | string (ISO) | Timestamp fin |
| `duration_seconds` | float | Durée totale en secondes |
| `framework_version` | string | Version framework |
| `user` | string | Utilisateur/compte |
| `hostname` | string | Nom de la machine |
| `tags` | array[string] | Tags optionnels |

---

## SECTION 2: `system_info`

**Description:** Informations complètes sur le système d'exécution.

```json
{
  "system_info": {
    "os": {
      "system": "Windows",
      "release": "10",
      "version": "10.0.19045",
      "machine": "AMD64",
      "processor": "Intel64 Family 6 Model 165 Stepping 5"
    },
    "cpu": {
      "physical_cores": 6,
      "logical_cores": 12,
      "max_frequency_mhz": 3700.0,
      "current_frequency_mhz": 3696.0,
      "cpu_percent": 15.3,
      "model": "Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz"
    },
    "memory": {
      "total_gb": 31.89,
      "available_gb": 18.45,
      "used_gb": 13.44,
      "percent_used": 42.1
    },
    "gpu": {
      "available": true,
      "name": "NVIDIA GeForce RTX 2070",
      "memory_total_gb": 8.0,
      "driver_version": "536.99"
    },
    "python_path": "C:\\Users\\user\\miniconda3\\envs\\qiskit\\python.exe"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `os.system` | string | Nom OS (Windows, Linux, Darwin) |
| `os.release` | string | Version OS |
| `os.version` | string | Version détaillée |
| `os.machine` | string | Architecture (AMD64, x86_64) |
| `os.processor` | string | Info processeur |
| `cpu.physical_cores` | int | Cœurs physiques |
| `cpu.logical_cores` | int | Cœurs logiques |
| `cpu.max_frequency_mhz` | float | Fréquence max |
| `cpu.current_frequency_mhz` | float | Fréquence actuelle |
| `cpu.cpu_percent` | float | Usage CPU % |
| `cpu.model` | string | Modèle CPU complet |
| `memory.total_gb` | float | RAM totale |
| `memory.available_gb` | float | RAM disponible |
| `memory.used_gb` | float | RAM utilisée |
| `memory.percent_used` | float | % RAM utilisé |
| `gpu.available` | bool | GPU disponible |
| `gpu.name` | string | Nom GPU |
| `gpu.memory_total_gb` | float | VRAM |
| `gpu.driver_version` | string | Version driver |
| `python_path` | string | Chemin Python |

---

## SECTION 3: `python_env`

**Description:** Environnement Python.

```json
{
  "python_env": {
    "version": "3.11.7",
    "version_info": [3, 11, 7, "final", 0],
    "implementation": "CPython",
    "compiler": "MSC v.1937 64 bit (AMD64)",
    "executable": "C:\\Users\\user\\miniconda3\\envs\\qiskit\\python.exe",
    "prefix": "C:\\Users\\user\\miniconda3\\envs\\qiskit",
    "virtualenv": "qiskit",
    "encoding": "utf-8",
    "platform": "win32"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `version` | string | Version Python (3.11.7) |
| `version_info` | array | [major, minor, micro, level, serial] |
| `implementation` | string | CPython, PyPy, etc. |
| `compiler` | string | Compilateur utilisé |
| `executable` | string | Chemin exécutable |
| `prefix` | string | Préfixe installation |
| `virtualenv` | string | Nom environnement virtuel |
| `encoding` | string | Encodage par défaut |
| `platform` | string | Plateforme (win32, linux) |

---

## SECTION 4: `dependencies`

**Description:** TOUTES les librairies installées avec versions.

```json
{
  "dependencies": {
    "qiskit_core": {
      "qiskit": "2.4.1",
      "qiskit-ibm-runtime": "0.47.0",
      "qiskit-aer": "0.17.2",
      "qiskit-ibm-provider": null
    },
    "ibm_addons": {
      "mthree": "2.8.0",
      "qiskit-aqc-tensor": "0.0.4",
      "qiskit-addon-mpf": "0.2.0",
      "qiskit-addon-obp": "0.1.0",
      "qiskit-addon-sqd": "0.8.0",
      "circuit-knitting-toolbox": "1.2.0"
    },
    "scientific": {
      "numpy": "1.26.4",
      "scipy": "1.14.1",
      "pandas": "2.2.0",
      "matplotlib": "3.8.2"
    },
    "utilities": {
      "python-dotenv": "1.0.0",
      "tqdm": "4.66.1",
      "requests": "2.31.0"
    },
    "all_installed": {
      "qiskit": "2.4.1",
      "numpy": "1.26.4"
    }
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `qiskit_core` | object | Packages Qiskit principaux |
| `ibm_addons` | object | IBM Quantum Addons |
| `scientific` | object | Librairies scientifiques |
| `utilities` | object | Utilitaires |
| `all_installed` | object | TOUS les packages pip |

---

## SECTION 5: `environment_vars`

**Description:** Variables d'environnement QMC/IBM (tokens masqués).

```json
{
  "environment_vars": {
    "QMC_PROJECT": "QMC_FULL_VALIDATION",
    "QMC_SHOTS": "100",
    "QMC_BACKEND": "ibm_torino",
    "QMC_LOG_LEVEL": "INFO",
    "QMC_GENERATE_REPORT": "true",
    "QMC_GENERATE_ARCHIVE": "true",
    "IBM_TOKEN_CHISTELLE": "4LxoO...***MASKED***",
    "IBM_INSTANCE_CHISTELLE": null,
    "IBM_CHANNEL": "ibm_quantum"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `QMC_*` | string | Variables QMC Framework |
| `IBM_TOKEN_*` | string | Token IBM (MASQUÉ) |
| `IBM_INSTANCE_*` | string | CRN instance |
| `IBM_CHANNEL` | string | Canal (ibm_quantum, ibm_cloud) |

---

## SECTION 6: `ibm_account`

**Description:** Informations compte IBM Quantum.

```json
{
  "ibm_account": {
    "available": true,
    "account_name": "CHISTELLE",
    "channel": "ibm_quantum",
    "hub": "ibm-q",
    "group": "open",
    "project": "main",
    "instance": "ibm-q/open/main",
    "crn": null,
    "plan": "open"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `available` | bool | Compte disponible |
| `account_name` | string | Nom du compte |
| `channel` | string | ibm_quantum ou ibm_cloud |
| `hub` | string | Hub IBM |
| `group` | string | Groupe |
| `project` | string | Projet |
| `instance` | string | Instance complète |
| `crn` | string | Cloud Resource Name |
| `plan` | string | Type de plan |

---

## SECTION 7: `backend`

**Description:** Informations du backend IBM Quantum.

```json
{
  "backend": {
    "available": true,
    "name": "ibm_torino",
    "num_qubits": 133,
    "processor_type": "Heron",
    "processor_revision": "r1",
    "basis_gates": ["id", "rz", "sx", "x", "cz", "measure", "delay", "reset"],
    "native_2q_gate": "cz",
    "max_circuits": 300,
    "max_shots": 100000,
    "coupling_map_size": 300,
    "online": true,
    "version": "2.3.45"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `available` | bool | Backend accessible |
| `name` | string | Nom (ibm_torino) |
| `num_qubits` | int | Nombre de qubits |
| `processor_type` | string | Type processeur (Heron, Eagle) |
| `processor_revision` | string | Révision (r1, r2, r3) |
| `basis_gates` | array[string] | Gates natives |
| `native_2q_gate` | string | Gate 2Q native (cz, ecr) |
| `max_circuits` | int | Max circuits par job |
| `max_shots` | int | Max shots |
| `coupling_map_size` | int | Nombre connexions |
| `online` | bool | Backend en ligne |
| `version` | string | Version backend |

---

## SECTION 8: `qpu_state` ⭐ CRITIQUE

**Description:** État COMPLET de CHAQUE qubit au moment de l'exécution.

```json
{
  "qpu_state": {
    "available": true,
    "timestamp": "2026-01-23T17:22:54+00:00",
    "calibration_id": "ibm_torino_20260123_172254",
    "num_qubits": 133,
    "qubits": [
      {
        "index": 0,
        "t1_us": 185.32,
        "t2_us": 145.67,
        "frequency_ghz": 4.723456,
        "anharmonicity_ghz": -0.321,
        "readout_error": 0.0234,
        "readout_length_us": 1.3,
        "prob_meas0_prep1": 0.0156,
        "prob_meas1_prep0": 0.0312,
        "sx_error": 0.000234,
        "sx_duration_ns": 35.5,
        "x_error": 0.000234,
        "x_duration_ns": 35.5,
        "status": "ok"
      },
      {
        "index": 41,
        "t1_us": 5.2,
        "t2_us": 3.1,
        "frequency_ghz": 4.812345,
        "anharmonicity_ghz": -0.298,
        "readout_error": 0.18,
        "readout_length_us": 1.3,
        "prob_meas0_prep1": 0.12,
        "prob_meas1_prep0": 0.24,
        "sx_error": 0.0045,
        "sx_duration_ns": 35.5,
        "x_error": 0.0045,
        "x_duration_ns": 35.5,
        "status": "faulty"
      }
    ],
    "summary": {
      "total_qubits": 133,
      "qubits_ok": 94,
      "qubits_suspect": 35,
      "qubits_faulty": 4,
      "faulty_indices": [41, 53, 86, 127],
      "suspect_indices": [0, 8, 21, 42, 70, 78, 85, 88, 97, 103, 106, 115, 124],
      "t1": {
        "mean_us": 174.5,
        "median_us": 175.2,
        "std_us": 45.3,
        "min_us": 3.2,
        "max_us": 335.2
      },
      "t2": {
        "mean_us": 134.8,
        "median_us": 130.5,
        "std_us": 38.7,
        "min_us": 7.3,
        "max_us": 295.8
      },
      "readout_error": {
        "mean": 0.0447,
        "median": 0.0325,
        "std": 0.0312,
        "min": 0.0089,
        "max": 0.1523
      },
      "sx_error": {
        "mean": 0.000312,
        "median": 0.000245,
        "min": 0.000089,
        "max": 0.0045
      }
    }
  }
}
```

### Champs par qubit

| Champ | Type | Unité | Description |
|-------|------|-------|-------------|
| `index` | int | - | Index du qubit (0 à N-1) |
| `t1_us` | float | µs | Temps de relaxation T1 |
| `t2_us` | float | µs | Temps de déphasage T2 |
| `frequency_ghz` | float | GHz | Fréquence du qubit |
| `anharmonicity_ghz` | float | GHz | Anharmonicité |
| `readout_error` | float | - | Erreur de lecture (0-1) |
| `readout_length_us` | float | µs | Durée de lecture |
| `prob_meas0_prep1` | float | - | P(mesure 0 | préparé 1) |
| `prob_meas1_prep0` | float | - | P(mesure 1 | préparé 0) |
| `sx_error` | float | - | Erreur gate √X |
| `sx_duration_ns` | float | ns | Durée gate √X |
| `x_error` | float | - | Erreur gate X |
| `x_duration_ns` | float | ns | Durée gate X |
| `status` | string | - | "ok", "suspect", "faulty" |

### Critères de classification

| Status | Critères |
|--------|----------|
| `ok` | T1 > 50µs ET readout_error < 5% |
| `suspect` | T1 < 50µs OU readout_error > 5% |
| `faulty` | T1 < 10µs OU readout_error > 15% |

---

## SECTION 9: `gates_calibration`

**Description:** Calibration de TOUTES les gates.

```json
{
  "gates_calibration": {
    "available": true,
    "timestamp": "2026-01-23T17:22:54+00:00",
    "gates_1q": [
      {
        "gate": "sx",
        "qubit": 0,
        "error": 0.000234,
        "duration_ns": 35.5,
        "calibrated": true
      },
      {
        "gate": "x",
        "qubit": 0,
        "error": 0.000234,
        "duration_ns": 35.5,
        "calibrated": true
      }
    ],
    "gates_2q": [
      {
        "gate": "cz",
        "qubits": [0, 1],
        "error": 0.00567,
        "duration_ns": 300.0,
        "calibrated": true
      },
      {
        "gate": "cz",
        "qubits": [1, 0],
        "error": 0.00567,
        "duration_ns": 300.0,
        "calibrated": true
      }
    ],
    "summary": {
      "gates_1q_count": 532,
      "gates_2q_count": 300,
      "avg_1q_error": 0.000312,
      "avg_2q_error": 0.0275,
      "min_2q_error": 0.00135,
      "max_2q_error": 1.0,
      "median_2q_error": 0.00258,
      "std_2q_error": 0.1409
    }
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `gates_1q[].gate` | string | Nom de la gate (sx, x, rz) |
| `gates_1q[].qubit` | int | Index du qubit |
| `gates_1q[].error` | float | Taux d'erreur |
| `gates_1q[].duration_ns` | float | Durée en nanosecondes |
| `gates_2q[].gate` | string | Nom de la gate (cz, ecr) |
| `gates_2q[].qubits` | array[int] | Paire de qubits [q0, q1] |
| `gates_2q[].error` | float | Taux d'erreur |
| `gates_2q[].duration_ns` | float | Durée en nanosecondes |

---

## SECTION 10: `topology`

**Description:** Topologie du backend (coupling map).

```json
{
  "topology": {
    "available": true,
    "type": "heavy-hex",
    "num_qubits": 133,
    "num_edges": 300,
    "coupling_map": [
      [0, 1], [1, 0], [1, 2], [2, 1], [0, 14], [14, 0]
    ],
    "adjacency_list": {
      "0": [1, 14],
      "1": [0, 2],
      "2": [1, 3],
      "3": [2, 4, 15]
    },
    "max_degree": 3,
    "avg_degree": 2.26,
    "diameter": 23
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `type` | string | Type topologie (heavy-hex) |
| `num_qubits` | int | Nombre de qubits |
| `num_edges` | int | Nombre de connexions |
| `coupling_map` | array[array[int]] | Liste des connexions [q1, q2] |
| `adjacency_list` | object | Liste d'adjacence {qubit: [voisins]} |
| `max_degree` | int | Degré max (connexions par qubit) |
| `avg_degree` | float | Degré moyen |
| `diameter` | int | Diamètre du graphe |

---

## SECTION 11: `calibration_health`

**Description:** Score de santé et analyse de la calibration.

```json
{
  "calibration_health": {
    "available": true,
    "health_score": 57.9,
    "health_grade": "F",
    "status": "DEGRADED",
    "components": {
      "qubit_availability": {"score": 97.0, "weight": 25},
      "qubit_health": {"score": 73.7, "weight": 15},
      "connection_health": {"score": 96.0, "weight": 15},
      "readout_quality": {"score": 11.8, "weight": 20},
      "gate_quality": {"score": 0.0, "weight": 15},
      "coherence_time": {"score": 58.2, "weight": 10}
    },
    "faulty_qubits": [41, 53, 86, 127],
    "suspect_qubits": [0, 8, 21, 42, 70, 78, 85, 88, 97, 103, 106, 115, 124],
    "broken_connections": [[20, 21], [38, 53], [53, 57]],
    "recommendations": [
      "AVOID 4 faulty qubits: [41, 53, 86, 127]",
      "Enable READOUT ERROR MITIGATION (M3/TREX)",
      "Enable PAULI TWIRLING for 2-qubit gates",
      "QPU is DEGRADED. Consider waiting for next calibration cycle."
    ],
    "optimal_region": {
      "start_qubit": 64,
      "size": 87,
      "qubits": [64, 65, 66, 67, 68, 69, 70, 71, 75, 90]
    }
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `health_score` | float | Score global 0-100 |
| `health_grade` | string | A, B, C, D, F |
| `status` | string | EXCELLENT, GOOD, DEGRADED, POOR |
| `components` | object | Scores par composant |
| `faulty_qubits` | array[int] | Indices qubits défaillants |
| `suspect_qubits` | array[int] | Indices qubits suspects |
| `broken_connections` | array[array] | Connexions cassées |
| `recommendations` | array[string] | Recommandations |
| `optimal_region` | object | Meilleure région contiguë |

---

## SECTION 12: `framework_config`

**Description:** Configuration du framework QMC.

```json
{
  "framework_config": {
    "project": "QMC_FULL_VALIDATION",
    "mode": "qpu",
    "backend_name": "ibm_torino",
    "shots": 100,
    "optimization_level": 3,
    "resilience_level": 1,
    "security": {
      "confirmation_required": true,
      "dry_run": false,
      "max_cost_minutes": 10
    },
    "features": {
      "fractional_gates": false,
      "gen3_turbo": false,
      "dynamic_circuits": true
    },
    "budget": {
      "monthly_limit_minutes": 100,
      "used_minutes": 0.28,
      "remaining_minutes": 99.72
    }
  }
}
```

---

## SECTION 13: `quality_thresholds`

**Description:** Seuils de qualité configurés.

```json
{
  "quality_thresholds": {
    "min_fidelity": 0.1,
    "min_entropy": 0.5,
    "max_readout_error": 0.15,
    "max_2q_error": 0.1,
    "min_t1_us": 10,
    "min_t2_us": 5,
    "min_health_score": 40
  }
}
```

---

## SECTION 14: `circuits_original` ⭐ CRITIQUE

**Description:** Circuits ORIGINAUX (avant transpilation) - RECONSTRUCTIBLES.

```json
{
  "circuits_original": [
    {
      "index": 0,
      "name": "GHZ_5Q",
      "num_qubits": 5,
      "num_clbits": 5,
      "depth": 6,
      "size": 10,
      "num_parameters": 0,
      "global_phase": "0",
      "gate_counts": {
        "h": 1,
        "cx": 4,
        "measure": 5
      },
      "num_1q_gates": 1,
      "num_2q_gates": 4,
      "num_measurements": 5,
      "qasm": "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[5];\ncreg c[5];\nh q[0];\ncx q[0],q[1];\ncx q[1],q[2];\ncx q[2],q[3];\ncx q[3],q[4];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];\nmeasure q[2] -> c[2];\nmeasure q[3] -> c[3];\nmeasure q[4] -> c[4];",
      "qasm_truncated": false,
      "instructions": [
        {"name": "h", "qubits": [0], "clbits": [], "params": []},
        {"name": "cx", "qubits": [0, 1], "clbits": [], "params": []},
        {"name": "cx", "qubits": [1, 2], "clbits": [], "params": []},
        {"name": "cx", "qubits": [2, 3], "clbits": [], "params": []},
        {"name": "cx", "qubits": [3, 4], "clbits": [], "params": []},
        {"name": "measure", "qubits": [0], "clbits": [0], "params": []},
        {"name": "measure", "qubits": [1], "clbits": [1], "params": []},
        {"name": "measure", "qubits": [2], "clbits": [2], "params": []},
        {"name": "measure", "qubits": [3], "clbits": [3], "params": []},
        {"name": "measure", "qubits": [4], "clbits": [4], "params": []}
      ],
      "parameters": null,
      "layout": null
    }
  ]
}
```

### Champs par circuit

| Champ | Type | Description |
|-------|------|-------------|
| `index` | int | Index du circuit (0 à N-1) |
| `name` | string | Nom du circuit |
| `num_qubits` | int | Nombre de qubits |
| `num_clbits` | int | Nombre de bits classiques |
| `depth` | int | Profondeur du circuit |
| `size` | int | Nombre total d'opérations |
| `num_parameters` | int | Paramètres non liés |
| `global_phase` | string | Phase globale |
| `gate_counts` | object | Comptage par type de gate |
| `num_1q_gates` | int | Nombre gates 1 qubit |
| `num_2q_gates` | int | Nombre gates 2 qubits |
| `num_measurements` | int | Nombre de mesures |
| `qasm` | string | Code QASM 2.0 complet |
| `qasm_truncated` | bool | QASM tronqué si trop long |
| `instructions` | array | Liste des instructions |
| `parameters` | object | Paramètres si circuit paramétré |
| `layout` | object | Layout (null avant transpilation) |

### Format instruction

```json
{
  "name": "cx",
  "qubits": [0, 1],
  "clbits": [],
  "params": []
}
```

---

## SECTION 15: `circuits_transpiled`

**Description:** Circuits après transpilation - même format que `circuits_original` avec layout.

```json
{
  "circuits_transpiled": [
    {
      "index": 0,
      "name": "GHZ_5Q",
      "num_qubits": 26,
      "num_clbits": 5,
      "depth": 16,
      "size": 32,
      "gate_counts": {
        "rz": 5,
        "sx": 18,
        "cz": 4,
        "measure": 5
      },
      "num_1q_gates": 23,
      "num_2q_gates": 4,
      "qasm": "OPENQASM 2.0;...",
      "instructions": [],
      "layout": {
        "initial_layout": "Layout({...})",
        "final_layout": [64, 65, 66, 67, 68],
        "virtual_to_physical": {
          "0": 64,
          "1": 65,
          "2": 66,
          "3": 67,
          "4": 68
        }
      }
    }
  ]
}
```

### Layout

| Champ | Type | Description |
|-------|------|-------------|
| `initial_layout` | string | Layout initial (repr) |
| `final_layout` | array[int] | Mapping final qubit virtuel → physique |
| `virtual_to_physical` | object | Dictionnaire v→p |

---

## SECTION 16: `transpilation_config`

**Description:** Configuration de transpilation utilisée.

```json
{
  "transpilation_config": {
    "optimization_level": 3,
    "layout_method": "sabre",
    "routing_method": "sabre",
    "translation_method": null,
    "approximation_degree": 1.0,
    "seed_transpiler": 12345,
    "coupling_map_used": true,
    "basis_gates": ["id", "rz", "sx", "x", "cz"],
    "initial_layout": "VF2PostLayout",
    "vf2_trials": 100000
  }
}
```

---

## SECTION 17: `layout_mapping`

**Description:** Mapping qubits virtuels → physiques.

```json
{
  "layout_mapping": {
    "available": true,
    "circuits": [
      {
        "index": 0,
        "name": "GHZ_5Q",
        "virtual_to_physical": {
          "0": 64,
          "1": 65,
          "2": 66,
          "3": 67,
          "4": 68
        },
        "physical_qubits_used": [64, 65, 66, 67, 68],
        "ancilla_qubits": []
      }
    ]
  }
}
```

---

## SECTION 18: `mitigation_config`

**Description:** Configuration de mitigation d'erreurs.

```json
{
  "mitigation_config": {
    "enabled": true,
    "twirling": {
      "enabled": true,
      "num_randomizations": 32,
      "gates": ["cx", "cz"]
    },
    "dynamical_decoupling": {
      "enabled": true,
      "sequence": "XY4",
      "pulse_alignment": 16,
      "extra_slack_distribution": "middle"
    },
    "zne": {
      "enabled": false,
      "noise_factors": [1, 2, 3],
      "extrapolator": "exponential"
    },
    "m3": {
      "enabled": false,
      "calibrated": false,
      "num_shots_calibration": 8192
    },
    "resilience_level": 1
  }
}
```

---

## SECTION 19: `sampler_options`

**Description:** Options du Sampler IBM Runtime.

```json
{
  "sampler_options": {
    "default_shots": 100,
    "dynamical_decoupling": {
      "enable": true,
      "sequence_type": "XY4"
    },
    "twirling": {
      "enable_gates": true,
      "num_randomizations": 32
    },
    "resilience": {
      "measure_mitigation": false,
      "zne_mitigation": false
    },
    "execution": {
      "rep_delay": null
    }
  }
}
```

---

## SECTION 20: `execution`

**Description:** Informations d'exécution du job.

```json
{
  "execution": {
    "job_id": "d5pq99pdgvjs73dc3scg",
    "backend": "ibm_torino",
    "status": "COMPLETED",
    "shots": 100,
    "circuits_count": 19,
    "total_shots": 1900,
    "timing": {
      "total_seconds": 58.36,
      "queue_seconds": 0.9,
      "execution_seconds": 45.4,
      "qpu_seconds": 3.0
    },
    "submitted_at": "2026-01-23T17:41:10.431Z",
    "started_at": "2026-01-23T17:41:21.741Z",
    "completed_at": "2026-01-23T17:41:31.888Z"
  }
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `job_id` | string | ID du job IBM |
| `backend` | string | Backend utilisé |
| `status` | string | COMPLETED, ERROR, CANCELLED |
| `shots` | int | Shots par circuit |
| `circuits_count` | int | Nombre de circuits |
| `total_shots` | int | shots × circuits |
| `timing.total_seconds` | float | Temps total |
| `timing.queue_seconds` | float | Temps en queue |
| `timing.execution_seconds` | float | Temps exécution |
| `timing.qpu_seconds` | float | Temps QPU réel |
| `submitted_at` | string | Timestamp soumission |
| `started_at` | string | Timestamp démarrage |
| `completed_at` | string | Timestamp fin |

---

## SECTION 21: `job_metadata`

**Description:** Métadonnées du job IBM.

```json
{
  "job_metadata": {
    "job_id": "d5pq99pdgvjs73dc3scg",
    "session_id": null,
    "tags": ["QMC_FULL_VALIDATION", "v2.7.1"],
    "primitive": "sampler",
    "primitive_version": 2,
    "program_id": "sampler",
    "log_level": "WARNING",
    "job_tags": []
  }
}
```

---

## SECTION 22: `results` ⭐ CRITIQUE

**Description:** Résultats complets de chaque circuit.

```json
{
  "results": [
    {
      "index": 0,
      "name": "GHZ_5Q",
      "shots": 100,
      "status": "COMPLETED",
      "num_outcomes": 12,
      "counts": {
        "00000": 42,
        "11111": 42,
        "00001": 3,
        "00010": 2,
        "00100": 2,
        "01000": 2,
        "10000": 2,
        "11110": 2,
        "11101": 1,
        "11011": 1,
        "10111": 1
      },
      "probabilities": {
        "00000": 0.42,
        "11111": 0.42,
        "00001": 0.03,
        "00010": 0.02,
        "00100": 0.02,
        "01000": 0.02,
        "10000": 0.02,
        "11110": 0.02,
        "11101": 0.01,
        "11011": 0.01,
        "10111": 0.01
      },
      "top_10": [
        {"bitstring": "00000", "count": 42, "probability": 0.42},
        {"bitstring": "11111", "count": 42, "probability": 0.42},
        {"bitstring": "00001", "count": 3, "probability": 0.03}
      ],
      "fidelity": 0.84,
      "metadata": {
        "meas_level": 2,
        "meas_return": "avg"
      }
    }
  ]
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `index` | int | Index du circuit |
| `name` | string | Nom du circuit |
| `shots` | int | Shots exécutés |
| `status` | string | Statut résultat |
| `num_outcomes` | int | Nombre d'états distincts |
| `counts` | object | {bitstring: count} |
| `probabilities` | object | {bitstring: prob} |
| `top_10` | array | 10 résultats les plus fréquents |
| `fidelity` | float | Fidélité calculée (si applicable) |
| `metadata` | object | Métadonnées IBM |

### Champs additionnels v2.7.1

| Champ | Type | Description |
|-------|------|-------------|
| `result_type` | string | `"sampler"` (counts) ou `"estimator"` (valeurs propres) |
| `register_counts` | object | *(multi-registres)* `{nom_registre: {bitstring: count}}` — registres exposés **séparément** (plus de fusion par sommation) |
| `primary_register` | string | *(multi-registres)* nom du registre primaire retenu pour `counts` |
| `expectation_value` | float \| array | *(estimator)* valeur propre — **scalaire** (1 observable) ou **liste** (multi-observables) |
| `expectation_values` | array[float] | *(estimator multi-obs)* une valeur par observable |
| `std_errors` | array[float] | *(estimator multi-obs)* erreur-type par observable |
| `n_observables` | int | *(estimator multi-obs)* nombre d'observables |

**Exemple — résultat Estimator multi-observables :**
```json
{
  "index": 0,
  "result_type": "estimator",
  "expectation_value": [0.812, -0.044, 0.501],
  "expectation_values": [0.812, -0.044, 0.501],
  "std_error": [0.006, 0.005, 0.007],
  "std_errors": [0.006, 0.005, 0.007],
  "n_observables": 3,
  "shots": 4096,
  "counts": {}, "num_outcomes": 0, "probabilities": {}, "top_10": []
}
```

**Exemple — résultat multi-registres (Sampler) :**
```json
{
  "index": 0,
  "result_type": "sampler",
  "primary_register": "meas",
  "counts": {"00": 510, "11": 490},
  "register_counts": {
    "meas": {"00": 510, "11": 490},
    "anc":  {"0": 1000}
  }
}
```

---

## SECTION 23: `raw_memory`

**Description:** Shots individuels (optionnel, peut être volumineux).

```json
{
  "raw_memory": {
    "available": true,
    "circuits": [
      {
        "index": 0,
        "name": "GHZ_5Q",
        "shots": ["00000", "11111", "00000", "11111", "00001"]
      }
    ]
  }
}
```

---

## SECTION 24: `statistics`

**Description:** Statistiques calculées sur les résultats.

```json
{
  "statistics": {
    "global": {
      "total_circuits": 19,
      "total_shots": 1900,
      "avg_fidelity": 0.35,
      "avg_entropy": 2.45,
      "avg_num_outcomes": 45
    },
    "per_circuit": [
      {
        "index": 0,
        "name": "GHZ_5Q",
        "entropy": 1.23,
        "uniformity": 0.15,
        "concentration": 0.84,
        "sparsity": 0.003
      }
    ]
  }
}
```

---

## SECTION 25: `session_logs`

**Description:** Derniers logs de la session (100 dernières lignes).

```json
{
  "session_logs": [
    "[17:40:36.053] [=] Mode: qpu",
    "[17:40:39.925] [=] ✅ Connecté: ibm_torino (133Q)",
    "[17:41:11.030] [=] Job ID: d5pq99pdgvjs73dc3scg",
    "[17:41:32.474] [=] [OK] Job terminé!"
  ]
}
```

---

## SECTION 26: `warnings`

**Description:** Warnings générés pendant l'exécution.

```json
{
  "warnings": [
    {
      "timestamp": "2026-01-23T17:40:36.070",
      "message": "Pas d'instance CRN configurée pour ce compte!",
      "category": "config"
    },
    {
      "timestamp": "2026-01-23T17:41:32.692",
      "message": "Circuit 13: 2 registres classiques détectés",
      "category": "circuit"
    }
  ]
}
```

---

## SECTION 27: `pre_execution_estimates`

**Description:** Estimations avant exécution.

```json
{
  "pre_execution_estimates": {
    "estimated_qpu_time_seconds": 1.35,
    "estimated_queue_time_seconds": 60,
    "estimated_cost_minutes": 0.02,
    "transpilation_score": 94,
    "transpilation_grade": "GO",
    "overhead_2q_percent": 0.0,
    "estimated_swaps": 0
  }
}
```

---

## SECTION 28: `error`

**Description:** Erreur complète si échec (null si succès).

```json
{
  "error": null
}
```

Si erreur:
```json
{
  "error": {
    "type": "IBMJobError",
    "message": "Job failed: backend timeout",
    "traceback": "Traceback (most recent call last):\n  File...",
    "timestamp": "2026-01-23T17:45:00.000Z",
    "job_id": "d5pq99pdgvjs73dc3scg",
    "recoverable": false
  }
}
```

---

## SECTION 29: `backend_extended` 🆕

**Description:** Informations étendues du backend.

```json
{
  "backend_extended": {
    "available": true,
    "status": {
      "operational": true,
      "pending_jobs": 5,
      "status_msg": null
    },
    "supported_features": {
      "dynamic_circuits": true,
      "mid_circuit_measurement": true,
      "classical_feedback": true,
      "reset": true,
      "delay": true,
      "fractional_gates": true
    },
    "limits": {
      "max_shots": 100000,
      "max_circuits": 300,
      "max_qubits": 133,
      "rep_delay_range_us": [0, 500],
      "default_rep_delay_us": 250
    },
    "processor": {
      "family": "Heron",
      "revision": "r1",
      "segment": "A",
      "clops": 290000
    },
    "dates": {
      "online_date": "2024-06-15T00:00:00"
    }
  }
}
```

---

## SECTION 30: `usage_and_costs` 🆕

**Description:** Usage et coûts de l'exécution.

```json
{
  "usage_and_costs": {
    "this_execution": {
      "qpu_time_seconds": 3.0,
      "shots_executed": 1900,
      "circuits_executed": 19
    },
    "monthly_usage": {
      "used_minutes": 0.28,
      "budget_minutes": 100,
      "remaining_minutes": 99.72
    },
    "ibm_quotas": null
  }
}
```

---

## SECTION 31: `transpilation_detailed` 🆕

**Description:** Métriques détaillées de transpilation par circuit.

```json
{
  "transpilation_detailed": {
    "available": true,
    "seed_transpiler": 12345,
    "metrics_per_circuit": [
      {
        "index": 0,
        "before": {"depth": 6, "gates_2q": 4},
        "after": {"depth": 16, "gates_2q": 4},
        "overhead": {"depth_pct": 166.7, "gates_2q_pct": 0.0},
        "swap_gates_added": 0
      }
    ],
    "totals": {
      "total_depth_before": 150,
      "total_depth_after": 690,
      "depth_overhead_pct": 360.0,
      "total_2q_before": 45,
      "total_2q_after": 216,
      "gates_2q_overhead_pct": 380.0,
      "total_swaps_added": 171
    }
  }
}
```

---

## SECTION 32: `analysis_results` 🆕

**Description:** Résultats d'analyse (XEB, fidelity, randomness).

```json
{
  "analysis_results": {
    "xeb": {
      "available": false,
      "per_circuit": []
    },
    "fidelity": {
      "available": true,
      "avg_fidelity": 0.35,
      "per_circuit": [
        {"index": 0, "fidelity": 0.84},
        {"index": 1, "fidelity": 0.37}
      ]
    },
    "randomness": {
      "available": true,
      "total_bits": 9500,
      "ones_ratio": 0.4987,
      "zeros_ratio": 0.5013,
      "balance": 0.9974
    },
    "correlations": {}
  }
}
```

---

## SECTION 33: `timing_detailed` 🆕

**Description:** Timeline complète de l'exécution.

```json
{
  "timing_detailed": {
    "timeline": {
      "script_start": "2026-01-23T17:40:35.800",
      "framework_init": "2026-01-23T17:40:36.053",
      "backend_connect": "2026-01-23T17:40:39.925",
      "calibration_analyzed": "2026-01-23T17:40:42.448",
      "circuits_built": "2026-01-23T17:40:43.193",
      "transpilation_start": "2026-01-23T17:40:46.449",
      "transpilation_end": "2026-01-23T17:40:48.178",
      "job_submitted": "2026-01-23T17:41:11.030",
      "job_queued": "2026-01-23T17:41:11.589",
      "job_running": "2026-01-23T17:41:21.741",
      "job_completed": "2026-01-23T17:41:31.888",
      "results_received": "2026-01-23T17:41:32.474",
      "archive_generated": "2026-01-23T17:41:33.991"
    },
    "durations": {
      "total_s": 58.19,
      "init_s": 0.25,
      "connect_s": 3.87,
      "calibration_s": 2.52,
      "circuits_s": 0.75,
      "transpilation_s": 1.73,
      "submission_s": 22.85,
      "queue_wait_s": 10.15,
      "qpu_execution_s": 3.0,
      "results_s": 0.59
    }
  }
}
```

---

## SECTION 34: `reproducibility` 🆕

**Description:** Informations pour reproduire l'exécution.

```json
{
  "reproducibility": {
    "seeds": {
      "numpy_seed": 42,
      "qiskit_seed": 12345,
      "transpiler_seed": 67890
    },
    "exact_versions": {
      "qiskit": "2.4.1",
      "qiskit-ibm-runtime": "0.47.0",
      "numpy": "1.26.4",
      "scipy": "1.14.1"
    },
    "git": {
      "branch": "main",
      "commit": "abc123def456",
      "dirty": false
    }
  }
}
```

---

## SECTION 35: `qubits_analysis` 🆕

**Description:** Analyse des qubits effectivement utilisés.

```json
{
  "qubits_analysis": {
    "available": true,
    "qubits_used": [64, 65, 66, 67, 68, 69, 70, 71, 75, 90],
    "num_qubits_used": 10,
    "used_qubits_quality": {
      "avg_t1_us": 185.3,
      "min_t1_us": 145.2,
      "avg_t2_us": 142.8,
      "avg_readout_error": 0.023,
      "worst_qubit": {"index": 70, "score": 0.65},
      "best_qubit": {"index": 65, "score": 0.92}
    },
    "connections_used": [[64, 65], [65, 66], [66, 67], [67, 68]],
    "connections_quality": {
      "avg_error": 0.0045,
      "worst_connection": {"qubits": [70, 71], "error": 0.012}
    }
  }
}
```

---

## SECTION 36: `connections_detailed` 🆕

**Description:** TOUTES les connexions 2Q du backend.

```json
{
  "connections_detailed": {
    "available": true,
    "total_connections": 300,
    "connections": [
      {
        "qubits": [0, 1],
        "gate": "cz",
        "error": 0.00567,
        "duration_ns": 300.0,
        "quality": "excellent"
      },
      {
        "qubits": [20, 21],
        "gate": "cz",
        "error": 1.0,
        "duration_ns": 300.0,
        "quality": "broken"
      }
    ],
    "stats": {
      "excellent_count": 45,
      "good_count": 180,
      "degraded_count": 60,
      "poor_count": 15,
      "avg_error": 0.0275,
      "min_error": 0.00135,
      "max_error": 1.0
    }
  }
}
```

### Classification qualité connexions

| Quality | Error Range |
|---------|-------------|
| `excellent` | error < 1% |
| `good` | 1% ≤ error < 3% |
| `degraded` | 3% ≤ error < 6% |
| `poor` | 6% ≤ error < 15% |
| `broken` | error ≥ 15% ou error = 1.0 |

---

## SECTION 37: `network_info` 🆕

**Description:** Informations réseau.

```json
{
  "network_info": {
    "hostname": "WORKSTATION-01",
    "local_ip": "192.168.1.100",
    "proxy": {
      "http": null,
      "https": null
    }
  }
}
```

---

## SECTION 38: `process_info` 🆕

**Description:** Informations du processus Python.

```json
{
  "process_info": {
    "pid": 12345,
    "memory_usage_mb": 1250.5,
    "memory_percent": 4.2,
    "cpu_percent": 15.3,
    "threads": 8
  }
}
```

---

## SECTION 39: `qdna_fingerprint` (déprécié — module externe)

**Statut :** depuis la séparation des modules propriétaires, **le framework public ne produit
plus ce champ**. La fonctionnalité correspondante est désormais fournie comme **module externe**
(chargé à la demande via `fw.load_module(...)`, voir `qmc_modules/`). Les archives générées par
le framework seul **ne contiennent donc pas** cette section ; si un module externe choisit de
l'ajouter, sa structure est définie par ce module et non par le présent format d'archive.

Les parsers doivent traiter `qdna_fingerprint` comme **optionnel et absent par défaut**.

---

## SECTION 40: `integrity`

**Description:** Checksums SHA-256 pour validation.

```json
{
  "integrity": {
    "results_hash": "sha256:a1b2c3d4e5f6789...",
    "circuits_hash": "sha256:fedcba9876543...",
    "qpu_state_hash": "sha256:123456789abcdef...",
    "archive_hash": null
  }
}
```

---

## Exemple de Code Parser Python

```python
import json
from pathlib import Path

def parse_qmc_archive(filepath: str) -> dict:
    """Parse une archive QMC v3.x (supporte .json ET .json.gz — gzip par défaut en v2.7.1)."""
    import gzip

    # [v2.7.1] Les archives sont compressées (.json.gz) par défaut : ouvrir en conséquence.
    opener = gzip.open if str(filepath).endswith('.gz') else open
    with opener(filepath, 'rt', encoding='utf-8') as f:
        archive = json.load(f)
    
    # Vérifier la version
    schema = archive.get('_schema', {})
    version = schema.get('version', '0.0.0')
    
    if not version.startswith('3.'):
        raise ValueError(f"Version non supportée: {version}")
    
    print(f"Archive v{version} - {schema.get('format')}")
    
    return archive


def get_qpu_state(archive: dict) -> list:
    """Récupère l'état de tous les qubits."""
    qpu = archive.get('qpu_state', {})
    return qpu.get('qubits', [])


def get_faulty_qubits(archive: dict) -> list:
    """Liste les qubits défaillants."""
    qubits = get_qpu_state(archive)
    return [q['index'] for q in qubits if q.get('status') == 'faulty']


def reconstruct_circuit(archive: dict, index: int = 0):
    """Reconstruit un circuit depuis l'archive."""
    from qiskit import QuantumCircuit
    
    circuits = archive.get('circuits_original', [])
    if index >= len(circuits):
        raise IndexError(f"Circuit {index} non trouvé")
    
    c = circuits[index]
    
    # Méthode 1: Via QASM
    if c.get('qasm') and not c.get('qasm_truncated'):
        return QuantumCircuit.from_qasm_str(c['qasm'])
    
    # Méthode 2: Via instructions
    qc = QuantumCircuit(c['num_qubits'], c['num_clbits'])
    for inst in c.get('instructions', []):
        gate = getattr(qc, inst['name'], None)
        if gate:
            if inst['clbits']:
                gate(*inst['qubits'], *inst['clbits'])
            else:
                gate(*inst['qubits'])
    return qc


def get_results(archive: dict) -> list:
    """Récupère les résultats."""
    return archive.get('results', [])


def get_counts(archive: dict, circuit_index: int = 0) -> dict:
    """Récupère les counts d'un circuit."""
    results = get_results(archive)
    if circuit_index < len(results):
        return results[circuit_index].get('counts', {})
    return {}


def analyze_execution(archive: dict) -> dict:
    """Analyse complète de l'exécution."""
    return {
        'job_id': archive.get('execution', {}).get('job_id'),
        'backend': archive.get('backend', {}).get('name'),
        'status': archive.get('metadata', {}).get('status'),
        'circuits': len(archive.get('results', [])),
        'total_shots': archive.get('execution', {}).get('total_shots'),
        'qpu_time_s': archive.get('execution', {}).get('timing', {}).get('qpu_seconds'),
        'faulty_qubits': get_faulty_qubits(archive),
        'health_score': archive.get('calibration_health', {}).get('health_score'),
    }


# Usage
if __name__ == '__main__':
    archive = parse_qmc_archive('archive_xxx.json')
    
    # Analyse rapide
    info = analyze_execution(archive)
    print(f"Job: {info['job_id']}")
    print(f"Backend: {info['backend']}")
    print(f"Status: {info['status']}")
    print(f"QPU Time: {info['qpu_time_s']}s")
    print(f"Health Score: {info['health_score']}")
    print(f"Faulty Qubits: {info['faulty_qubits']}")
    
    # Résultats
    for r in get_results(archive):
        print(f"{r['name']}: fidelity={r.get('fidelity', 'N/A')}")
    
    # Reconstruire circuit
    qc = reconstruct_circuit(archive, 0)
    print(qc)
```

---

## Validation JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "QMC Archive v3.1",
  "type": "object",
  "required": ["_schema", "metadata", "results"],
  "properties": {
    "_schema": {
      "type": "object",
      "required": ["version", "format"],
      "properties": {
        "version": {"type": "string", "pattern": "^3\\."},
        "format": {"const": "QMC_EXECUTION_ARCHIVE_V3"}
      }
    },
    "metadata": {
      "type": "object",
      "required": ["execution_id", "status"]
    },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["index", "counts"]
      }
    }
  }
}
```

---

## Changelog

### Framework v2.7.1 (2026-05) — schéma inchangé (v3.1.0)
- **Compression gzip par défaut** (`compress=True`) → fichiers `archive_*.json.gz` (~80 % plus petit).
- **Écritures atomiques** (temp + fsync + `os.replace`) et **permissions** `0o600`/`0o700`.
- **Redaction des secrets** (tokens masqués) dans `session_logs` / `environment_vars` / messages.
- `_schema.framework_version` / `metadata.framework_version` = **`2.7.1`**.
- `integrity.circuits_hash` couvre **tous** les circuits (auparavant 20).
- `results[]` enrichis : `result_type`, `register_counts`/`primary_register` (multi-registres, plus de fusion),
  `expectation_value` scalaire/liste + `expectation_values`/`std_errors`/`n_observables` (Estimator multi-obs).
- `analysis_results.randomness` : séparateurs de registres ignorés, `n_qubits` ajouté, ratios corrigés.
- Calibration interne : `gate_2q` réellement peuplé (consommé par EPLG) ; analyzers avec barres d'erreur
  (`ci_95`, `xeb_stderr`/`xeb_ci95`).
- Cryptographie réelle (AES-256-GCM/HKDF, ZKP, RSW) et min-entropie NIST pour les protocoles QMC.

### v3.1.0 (2026-01-23)
- Ajout de 11 nouvelles sections (29-39)
- `backend_extended`: Features, limites, CLOPS
- `usage_and_costs`: Temps QPU, budget
- `transpilation_detailed`: Overhead par circuit
- `analysis_results`: XEB, fidelity, randomness
- `timing_detailed`: Timeline complète
- `reproducibility`: Seeds, Git
- `qubits_analysis`: Qualité des qubits utilisés
- `connections_detailed`: Toutes les connexions 2Q
- `network_info`: IP, proxy
- `process_info`: PID, mémoire
- `qdna_fingerprint`: (déprécié — non produit par le framework public ; voir module externe)

### v3.0.0 (2026-01-22)
- Version initiale avec 30 sections
- Support circuits reconstructibles (QASM + instructions)
- État QPU complet

---

© QMC Research Lab 2026
