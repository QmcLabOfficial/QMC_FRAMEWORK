# QMC Quantum Framework v2.7.2

<div align="center">

![Version](https://img.shields.io/badge/version-2.7.2-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Qiskit](https://img.shields.io/badge/qiskit-2.3%2B-6929C4.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![IBM Quantum](https://img.shields.io/badge/IBM%20Quantum-Heron%20r1--r3-054ADA.svg)
![Audited](https://img.shields.io/badge/audited-237%20fixes-success.svg)

**Complete quantum testing framework — one single file, does everything, simple and fast**

*QMC Research Lab — France*

[⚡ Quick Use](#-quick-use) • [📖 Wiki](https://qmc-lab.com/framework/wiki) • [Installation](#-installation) • [Features](#-features) • [API](#-api-reference)

</div>

---

## ⚡ Quick Use

> **Philosophy**: copy **one single file** `qmc_quantum_framework_v2_7_2.py`, import it, and everything works.
> The `import` is **pure** (no side effects, no installation at load time).

```bash
# 1) Dependencies — your choice:
python qmc_quantum_framework_v2_7_2.py --check-deps          # check (installs nothing)
python qmc_quantum_framework_v2_7_2.py --install             # install the missing ones
#   or manually:
pip install qiskit qiskit-ibm-runtime numpy scipy cryptography python-dotenv matplotlib
```

```python
# 2) Three lines to run a circuit on IBM Quantum
from qmc_quantum_framework_v2_7_2 import QMCFramework

fw = QMCFramework(backend_name="ibm_torino", project="MyExperiment", shots=4096)
fw.connect()                                   # reads credentials from .env

circuit  = fw.build_circuit("ghz", n_qubits=5) # 21 builders: ghz, bell, iqp, grover, qft, qpe, teleportation…
results  = fw.run_on_qpu([circuit])            # transpile + execute + HTML report + JSON archive

print("Job ID :", fw.last_job_id)
print("Counts :", results[0]["counts"])
print("Outputs in qmc_runs/ (.html report + .json.gz archive)")
```

```bash
# 3) Try it WITHOUT IBM credentials (local Aer simulator)
python qmc_quantum_framework_v2_7_2.py --selftest          # embedded test suite (no dependency, no QPU)
python test_qmc_v2_7_2_FULL_VALIDATION.py --skip-qpu       # 15 tests (API, multi-job, transpilation)
python test_qmc_v2_7_2_FULL_VALIDATION.py --multijob-sim   # real execution on AerSimulator
```

📖 **More examples → [Wiki / Quick Start](https://qmc-lab.com/framework/wiki/quick-start)**

---

## 📖 Wiki & Documentation

Full documentation lives on the **wiki**: **<https://qmc-lab.com/framework/wiki>**

| Section | Link |
|---------|------|
| 🏁 Quick start | <https://qmc-lab.com/framework/wiki/quick-start> |
| 📦 Installation & configuration | <https://qmc-lab.com/framework/wiki/installation> |
| 🔬 Circuit Builders (21) | <https://qmc-lab.com/framework/wiki/circuit-builders> |
| 📊 Analyzers (12) | <https://qmc-lab.com/framework/wiki/analyzers> |
| 🔐 Quantum cryptography | <https://qmc-lab.com/framework/wiki/crypto> |
| ☁️ Multi-account audit | <https://qmc-lab.com/framework/wiki/multi-account-audit> |
| 📈 Reports & archives | <https://qmc-lab.com/framework/wiki/reports> |
| 🧩 API Reference | <https://qmc-lab.com/framework/wiki/api-reference> |
| 🗒️ Changelog | <https://qmc-lab.com/framework/wiki/changelog> |

---

## 🎯 Overview

The **QMC Quantum Framework** is a **single-file** Python framework for running and analyzing
quantum experiments on IBM Quantum processors. Designed to be **simple, fast and complete**:

- 🔬 **21 Circuit Builders**: GHZ, Bell, IQP, Grover, QFT, QPE, Teleportation, and more
- 📊 **12 Analyzers**: Fidelity, Entropy, Correlation, XEB, Bell/CHSH — **with error bars**
- 🔐 **REAL cryptography**: AES-256-GCM + HKDF, HMAC, Schnorr ZKP, RSW time-lock, QRNG (NIST)
- 🚀 **QPU execution**: IBM Quantum (Heron r1/r2/r3), multi-job with resume, parallel transpilation + cache
- 📈 **Automatic reports**: interactive HTML + JSON archives (gzip by default)
- ☁️ **Cloud & Audit**: QMC Archive Manager + full multi-account IBM audit

---

## ✨ What's New in v2.7.2

- 🧩 **Patented modules externalized**: the inner workings of the inventions are no longer exposed in the
  public file. They are loaded **on demand** via `fw.load_module("<name>")` from `qmc_modules/` (see
  `QMC_MODULES_PATH`), otherwise `QMCModuleNotAvailableError`.
- 🧪 **EMBEDDED non-regression test suite** (single-file): `python qmc_quantum_framework_v2_7_2.py --selftest`
  (no dependency) **and** `pytest qmc_quantum_framework_v2_7_2.py`. Covers QPE, teleportation (Z **and X**
  basis), adversarial crypto (Schnorr/range/AES-GCM/time-lock), result parsing, anti-SSRF and the module loader.
- 🔬 **Scientific rigor**: field `quantum_advantage_proven` → **`advantage_indicators_passed`** (no longer
  overclaims a proof of advantage); teleportation of |+⟩/|−⟩ now verifiable in the **X basis** (deterministic);
  guard on the Pedersen generator; **real thread-local log stack**; `debug` tracing of data paths.

> **Based on v2.7.1** (multi-agent audit → **237 fixes** `[v2.7.1 FIX]`, all verified):

- 🔴 **Quantum correctness**: QPE (exact phases), teleportation (conditional corrections), SwapTest,
  Deutsch-Jozsa, amplitude encoding, Bell σ, NIST-style tests, QuantumVolume (2σ / ≥100 trials criterion).
- 🔐 **Real cryptography** (replaces the demos): `QMCQuantumCrypto` (AES-256-GCM + HKDF-SHA256, HMAC,
  NIST SP 800-90B min-entropy), `QMCSigmaZK` (verifiable Schnorr ZKP + range proof), `QMCTimeLock` (RSW puzzle).
- 🛡️ **Security**: token anti-exfiltration (https allowlist), anti-SSRF (pinned webhooks), report anti-XSS,
  secret redaction in logs, cleanup of temporary credentials.
- 🧱 **Robustness & perf**: atomic JSON writes, result integrity (registers/shots), hardened QPU resume,
  wired-in **transpilation cache**, repaired IBM add-ons (M3/EPLG/CLOPS/Trotter).
- 🧹 **Cleanliness**: **pure** `import` (opt-in auto-install via `--install`), **linearized class hierarchy**
  (`QMCFramework` = complete class, no more monkey-patching), stable public API + `__all__`.

📖 **Full details → [Wiki / Changelog](https://qmc-lab.com/framework/changelog)** • `qmc_audit/CHANGELOG_v2_7_1.md`

---

## 📦 Installation

### Requirements
- Python **3.10+**
- An **IBM Quantum** account with an API token
- ~500 MB of disk space

### Install
```bash
git clone https://github.com/QmcLabOfficial/QMC_FRAMEWORK.git
cd QMC_FRAMEWORK

# Dependencies (recommended: a virtual environment)
python -m venv .venv && . .venv/bin/activate          # Windows: .venv\Scripts\activate
python qmc_quantum_framework_v2_7_2.py --install        # or pip install … (see Quick Use)

# Configuration
cp .env.example .env       # then edit .env with your credentials
```

### Optional: install as a package (still one file)
The framework stays a **single module**; `pyproject.toml` only adds metadata and a console entry point.
```bash
pip install .                 # declares deps + installs the `qmc` console command
qmc --selftest                # run the embedded test suite via the console script
```
```python
# Stable import shim (survives version bumps v2_7_2 -> v2_7_3 without touching your scripts):
from qmc import QMCFramework   # instead of `from qmc_quantum_framework_v2_7_2 import QMCFramework`
```

### Configuration (`.env`)

See **`.env.example`** (complete template). The framework automatically detects all accounts defined
via the `IBM_API_KEY_<LABEL>` pattern (+ optional `IBM_INSTANCE_<LABEL>`), and the **active** account via
`IBM_API_KEY_ACTIVE_<LABEL>`.

```env
# === IBM Quantum accounts (multi-account: one free-form LABEL per account) ===
IBM_API_KEY_ALICE=your_ibm_api_key_here
IBM_API_KEY_LAB=your_ibm_api_key_here
IBM_INSTANCE_LAB=crn:v1:bluemix:public:quantum-computing:us-east:a/xxxx::   # optional (paid plan)

# === Default ACTIVE account ===
IBM_API_KEY_ACTIVE_QMCLAB=your_active_ibm_api_key_here
IBM_INSTANCE_QMCLAB=crn:v1:bluemix:public:quantum-computing:us-east:a/xxxx::

# === QMC Archive Manager (optional) ===
QMC_ARCHIVE_URL=https://your-project.supabase.co/functions/v1/upload   # https required (host allowlist)
QMC_ARCHIVE_TOKEN=qmc_your_archive_token_here
QMC_ARCHIVE_UPLOAD=true

# === Options ===
QMC_GENERATE_REPORT=true
QMC_GENERATE_ARCHIVE=true
QMC_AUTO_CONFIRM=false
```

> ⚠️ **Security**: **never commit** your `.env` (it contains secrets). Make sure it is listed in
> `.gitignore` and keep it out of any synced/public folder. Tokens are automatically redacted in logs and
> reports (redaction since v2.7.1). 📖 [Wiki / Security](https://qmc-lab.com/framework/wiki/installation).

📖 **Detailed guide → [Wiki / Installation](https://qmc-lab.com/framework/wiki/installation)**

---

## 🚀 Examples

### Calibration analysis
```python
calibration = fw.noise.analyze_calibration()
print("Mean readout error :", calibration["summary"]["readout_error"]["mean"])
print("Mean 2-qubit error :", calibration["summary"]["gate_2q"]["mean"])
```

### Analyzers with error bars
```python
from qmc_quantum_framework_v2_7_2 import FidelityAnalyzer, XEBAnalyzer

counts = results[0]["counts"]
fid = FidelityAnalyzer().analyze(counts)
print(f"Fidelity = {fid['fidelity']:.3f} ± {fid['std_error']:.3f}  (95% CI {fid['ci_95']})")
```

### Real cryptography
```python
from qmc_quantum_framework_v2_7_2 import QMCQuantumCrypto, QMCSigmaZK

key = QMCQuantumCrypto.hkdf_sha256(b"quantum-entropy-seed", length=32)
enc = QMCQuantumCrypto.aead_encrypt(key, b"secret message")        # AES-256-GCM
clr = QMCQuantumCrypto.aead_decrypt(key, enc["nonce"], enc["ciphertext"])

proof = QMCSigmaZK.range_prove(value=42, lower=0, upper=100)        # ZK proof (without revealing 42)
assert QMCSigmaZK.range_verify(proof)
```

### Multi-job with automatic resume
```python
jobs = [{"circuits": [c1], "shots": 4096, "label": "job_1"},
        {"circuits": [c2], "shots": 4096, "label": "job_2"}]
session = fw.run_multi_job_session(jobs=jobs)     # automatically resumes on a crash
```

### Multi-account audit
```python
result = fw.audit_accounts(window_days=30, budget_minutes=10.0)
print("Accounts :", result["global_stats"]["total_accounts"])
print("Report   :", result["generated_files"]["html"])
```

📖 **All examples → [Wiki / Quick Start](https://qmc-lab.com/framework/wiki/quick-start)**

---

## 📚 Features

### Circuit Builders (21) — 📖 [Wiki](https://qmc-lab.com/framework/wiki/circuit-builders)

| Builder | Description | Builder | Description |
|---------|-------------|---------|-------------|
| `GHZBuilder` | GHZ states | `QPEBuilder` | Phase estimation |
| `BellBuilder` | Bell pairs | `DeutschJozsaBuilder` | Deutsch-Jozsa |
| `IQPBuilder` | Instantaneous QP | `BernsteinVaziraniBuilder` | Bernstein-Vazirani |
| `ClusterBuilder` | Cluster states | `SimonBuilder` | Simon's algorithm |
| `RandomCircuitBuilder` | Random circuits | `SwapTestBuilder` | SWAP test (fidelity) |
| `QFTBuilder` | Fourier transform | `QRNGBuilder` | Random number generator |
| `GroverBuilder` | Grover's algorithm | `TeleportationBuilder` | Teleportation |
| `ParameterizedCircuitBuilder` | VQE circuits | `AmplitudeEncodingBuilder` | Amplitude encoding |
| `QuantumSignatureBuilder` | Quantum signatures | `ZKPBuilder` | Zero-Knowledge Proofs |
| `TimeLockBuilder` | Time-lock (RSW) | `ObliviousTransferBuilder` | Oblivious transfer |
| `HardwareEfficientBuilder` | Hardware-efficient ansatz | | |

### Analyzers (12) — 📖 [Wiki](https://qmc-lab.com/framework/wiki/analyzers)

| Analyzer | Metrics | Analyzer | Metrics |
|----------|---------|----------|---------|
| `FidelityAnalyzer` | Fidelity + 95% CI | `CompressionAnalyzer` | State coverage |
| `EntropyAnalyzer` | Shannon / Von Neumann | `XEBCrossValidationAnalyzer` | XEB cross-validation |
| `CorrelationAnalyzer` | Correlations + σ | `HoneypotAnalyzer` | Attack detection |
| `XEBAnalyzer` | XEB + error bars | `QuantumAdvantageAnalyzer` | Quantum-behavior indicators (gated) |
| `BellAnalyzer` | CHSH (S, binomial σ) | `RandomnessAnalyzer` | NIST-style tests |

### Advanced features
- **Fractional Gates** (native RX/RZZ) · **Gen3 Turbo** · **Dynamic Circuits**
- **Error Mitigation**: M3, ZNE, Twirling, DD, PEA
- **Parallel multi-CPU transpilation + cache** (identical batches reused)
- **Multi-job with resume** · **Real cryptography** (AES-GCM / HKDF / ZK) · **External modules** loaded on demand

---

## 🧩 API Reference

📖 **Full reference → [Wiki / API](https://qmc-lab.com/framework/wiki/api-reference)**

```python
from qmc_quantum_framework_v2_7_2 import QMCFramework   # main class (concrete, complete)

fw = QMCFramework(backend_name="ibm_fez", project="QMC_Test", shots=4096,
                  use_fractional_gates=False, gen3_turbo=False)

fw.connect()                                  # -> bool
fw.build_circuit("ghz", n_qubits=5)           # -> QuantumCircuit
fw.transpile_circuits([circuit])              # transpilation (parallel + cache)
fw.run_on_qpu([circuit], shots=4096)          # -> List[Dict] (counts, shots, …)
fw.run_multi_job_session(jobs=[...])          # multi-job + resume
fw.audit_accounts(window_days=30)             # multi-account audit
fw.estimate_eplg(); fw.estimate_clops()       # IBM add-ons (M3/EPLG/CLOPS/Trotter)
fw.last_job_id                                # ID of the last submitted job

module = fw.load_module("name")               # load an external module (patented modules provided separately)
module.run(...)                               # QMCModuleNotAvailableError if not available
```

> **Hierarchy (linearized in v2.7.1)**: `QMCFrameworkBase → QMCFrameworkExtended → QMCFramework`,
> where `QMCFramework` is the **concrete public class** (the legacy `QMCFrameworkV2_4` alias was removed).
> Pure `import`, no alias, no monkey-patching.

---

## 🧪 Tests

```bash
# EMBEDDED non-regression suite (single-file, NO dependency or QPU required)
python qmc_quantum_framework_v2_7_2.py --selftest             # QPE, teleport (Z+X), adversarial crypto, loader…
pytest qmc_quantum_framework_v2_7_2.py -q                     # same tests, via pytest

# Full integration validation on a real QPU
python test_qmc_v2_7_2_FULL_VALIDATION.py --backend ibm_torino --shots 100

# Local tests (no QPU / no credentials)
python test_qmc_v2_7_2_FULL_VALIDATION.py --skip-qpu          # API + multi-job + transpilation + loader
python test_qmc_v2_7_2_FULL_VALIDATION.py --multijob-sim      # AerSimulator execution
```

> 💡 On Windows, run with `PYTHONUTF8=1` for correct emoji/box-drawing display.

---

## 📜 Changelog (summary)

- **v2.7.2 (2026-06)** — Patented modules **externalized** (loaded on demand), **embedded test suite**
  (`--selftest` / pytest), scientific rigor (`advantage_indicators_passed`, X-basis teleport), thread-local log,
  `LICENSE` + `.gitattributes`.
- **v2.7.1 (2026-05)** — Full audit: **237 fixes**, real cryptography, hardened security, pure import,
  linearized hierarchy, transpilation cache, error bars. 📖 [Full changelog](https://qmc-lab.com/framework/wiki/changelog)
- **v2.7.0 (2026-01)** — Multi-Job Session + Auto-Resume + parallel transpilation.
- **v2.6.3 (2026-01)** — QMC Accounts Audit Module.
- **v2.6.2 / v2.6.1 / v2.6.0** — Archive Manager, QPU auto-fetch, Fractional Gates / Gen3 Turbo.

---

## 🔒 Proprietary modules (patents)

The patented implementations are **not included** in this public framework: their inner workings are
**never exposed** in the code. They are distributed as **external modules**, loaded **on demand** via
`fw.load_module("<name>")` (`qmc_modules/` folder, location overridable via `QMC_MODULES_PATH`) and
provided separately to authorized clients. If the module is absent, the framework raises
`QMCModuleNotAvailableError`.

| Reference | Module (provided separately) |
|-----------|------------------------------|
| FR2514352 | QMC Core |
| FR2514504 | QMC Biometric |
| FR2514363 | QMC Shield |
| FR2514509 | QAEE |
| FR2514682 | QGP |
| FR2515002 | QDNA-ID |
| FR2515103 | QRPM |
| FR2515682 | QMC SIP |

> Module contract and interface template: see [`qmc_modules/README.md`](qmc_modules/README.md).

---

## 🤝 Contributing & Contact

Privately developed project for QMC Research Lab.
- 🌐 Website: [qmc-lab.com](https://qmc-lab.com) · 📖 Wiki: [qmc-lab.com/framework/wiki](https://qmc-lab.com/framework/wiki)
- 📦 GitHub: [@QmcLabOfficial](https://github.com/QmcLabOfficial)

---

## 📄 License

**Proprietary** — © 2024-2026 QMC Research Lab, Menton, France.
Any unauthorized reproduction, distribution or use is strictly prohibited.

---

<div align="center">

**Built with ❤️ by QMC Research Lab**

*Quantum Mandatory Cryptography — Where Security REQUIRES Quantum*

</div>
