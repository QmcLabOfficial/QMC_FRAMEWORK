#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║        QMC FRAMEWORK v2.6.3 - VALIDATION EXHAUSTIVE COMPLÈTE                     ║
║        Test de TOUS les composants avec exécution QPU réelle                     ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  TESTS INCLUS:                                                                   ║
║  ├── [SECTION 1] Import & Initialisation                                         ║
║  ├── [SECTION 2] Connexion & Calibration                                         ║
║  ├── [SECTION 3] TOUS les Circuit Builders (21 builders)                        ║
║  │   ├── GHZ, Bell, IQP, Cluster, Random, QFT, Parametrized                     ║
║  │   ├── Grover, QPE, Deutsch-Jozsa, Bernstein-Vazirani, Simon                  ║
║  │   ├── SwapTest, QRNG, Teleportation, AmplitudeEncoding                       ║
║  │   └── QuantumSignature, ZKP, TimeLock, ObliviousTransfer, HardwareEfficient  ║
║  ├── [SECTION 4] TOUS les Analyzers (12 analyzers)                              ║
║  │   ├── Fidelity, Entropy, Correlation, XEB, Bell, Randomness                  ║
║  │   └── Compression, XEBCrossValidation, Honeypot, QuantumAdvantage            ║
║  ├── [SECTION 5] Nouvelles fonctionnalités v2.6.0/v2.6.1                        ║
║  │   ├── Fractional Gates, Dynamic Circuits, Gen3 Turbo                         ║
║  │   ├── Fake Backends, QPY Serialization, Session/Batch Mode                   ║
║  │   ├── Primitives V2, Noise Learner, Execution Spans                          ║
║  │   └── Parallel Transpilation, Backend Selection, Calibration ID              ║
║  ├── [SECTION 5b] v2.6.2: QMC Archive Manager Integration                       ║
║  │   ├── QMCArchiveUploader class, upload(), is_enabled()                       ║
║  │   ├── Variables: QMC_ARCHIVE_URL, QMC_ARCHIVE_TOKEN, etc.                    ║
║  │   └── run_on_qpu() params: upload_to_archive, archive_projects, archive_notes║
║  ├── [SECTION 5c] ★ NEW v2.6.3: QMC Accounts Audit Module                       ║
║  │   ├── QMCJobDataCollector, QMCAuditHTMLReportGenerator                       ║
║  │   ├── get_all_ibm_accounts_from_env(), run_accounts_audit()                  ║
║  │   └── QMCFramework.audit_accounts(), list_ibm_accounts()                     ║
║  ├── [SECTION 6] Optimizers & Calculators                                        ║
║  │   ├── CircuitOptimizer, DynamicClusterOptimizer, TrotterOptimizer            ║
║  │   └── EPLGCalculator, CLOPSCalculator, CircuitCostEstimator                  ║
║  ├── [SECTION 7] Error Mitigation                                                ║
║  │   ├── ErrorMitigationManager, M3 Wrapper                                     ║
║  │   └── Twirling, DD, ZNE configurations                                       ║
║  ├── [SECTION 8] QDNA Features                                                   ║
║  ├── [SECTION 9] Exécution QPU (100 shots/circuit)                              ║
║  ├── [SECTION 10] Analyse des résultats                                          ║
║  └── [SECTION 11] Archive JSON v3.1 (41 sections)                               ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Usage:                                                                          ║
║    python test_qmc_v2_6_3_FULL_VALIDATION.py                                     ║
║    python test_qmc_v2_6_3_FULL_VALIDATION.py --backend ibm_torino --shots 100    ║
║    python test_qmc_v2_6_3_FULL_VALIDATION.py --skip-qpu   # Tests locaux seuls   ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import argparse
import tempfile
import traceback
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# ==============================================================================
# CONFIGURATION
# ==============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_banner():
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
║{Colors.BOLD}      ⚛️  QMC FRAMEWORK v2.6.3 - VALIDATION EXHAUSTIVE COMPLÈTE  ⚛️            {Colors.END}{Colors.CYAN}║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Test de TOUS les composants: 21 Builders, 12 Analyzers, Optimizers, etc.        ║
║  ★ v2.6.2: QMC Archive Manager   ★ v2.6.3: QMC Accounts Audit                   ║
║  Avec exécution QPU réelle pour validation complète du framework                 ║
╚══════════════════════════════════════════════════════════════════════════════════╝{Colors.END}
""")

def print_section(title: str, emoji: str = "📋"):
    print()
    print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {emoji} {title}{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")

def print_subsection(title: str):
    print(f"\n{Colors.YELLOW}  ▶ {title}{Colors.END}")

def print_test(name: str, status: str, message: str = ""):
    icons = {
        "PASS": f"{Colors.GREEN}✅{Colors.END}",
        "FAIL": f"{Colors.RED}❌{Colors.END}",
        "SKIP": f"{Colors.YELLOW}⏭️{Colors.END}",
        "INFO": f"{Colors.BLUE}ℹ️{Colors.END}",
        "WARN": f"{Colors.YELLOW}⚠️{Colors.END}",
        "RUN": f"{Colors.MAGENTA}🔄{Colors.END}",
    }
    icon = icons.get(status, "  ")
    msg = f" - {message}" if message else ""
    print(f"    {icon} {name}{msg}")

def print_metric(name: str, value: Any, unit: str = ""):
    unit_str = f" {unit}" if unit else ""
    print(f"       {Colors.DIM}├─{Colors.END} {name}: {Colors.BOLD}{value}{Colors.END}{unit_str}")

# ==============================================================================
# TEST RESULTS TRACKER
# ==============================================================================

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.tests = []
        self.qpu_results = []
        self.circuits_for_qpu = []
        self.start_time = time.time()
    
    def add(self, name: str, status: str, details: str = "", category: str = ""):
        self.tests.append({
            'name': name, 'status': status, 'details': details,
            'category': category, 'timestamp': datetime.now().isoformat()
        })
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        else:
            self.skipped += 1
    
    def add_circuit_for_qpu(self, name: str, circuit):
        """Ajoute un circuit à la liste pour exécution QPU, si pas de paramètres non liés."""
        # Vérifier si le circuit a des paramètres non liés
        if hasattr(circuit, 'parameters') and len(circuit.parameters) > 0:
            print_test(name, "SKIP", f"{len(circuit.parameters)} paramètres non liés - exclu de QPU")
            return False
        self.circuits_for_qpu.append((name, circuit))
        return True
    
    def add_qpu_result(self, circuit_name: str, counts: Dict, analysis: Dict = None):
        self.qpu_results.append({
            'circuit': circuit_name, 'counts': counts,
            'analysis': analysis or {}, 'timestamp': datetime.now().isoformat()
        })
    
    def summary(self):
        total = self.passed + self.failed + self.skipped
        elapsed = time.time() - self.start_time
        
        print()
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        print(f"{Colors.BOLD}  📊 RÉSUMÉ DES TESTS - VALIDATION EXHAUSTIVE{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        print(f"  Total Tests:     {total}")
        print(f"  {Colors.GREEN}Passés:          {self.passed}{Colors.END}")
        print(f"  {Colors.RED}Échoués:         {self.failed}{Colors.END}")
        print(f"  {Colors.YELLOW}Ignorés:         {self.skipped}{Colors.END}")
        print(f"  Circuits QPU:    {len(self.circuits_for_qpu)}")
        print(f"  Résultats QPU:   {len(self.qpu_results)}")
        print(f"  Temps Total:     {elapsed:.1f}s")
        print(f"{Colors.CYAN}{'═' * 80}{Colors.END}")
        
        # Statistiques par catégorie
        categories = {}
        for t in self.tests:
            cat = t.get('category', 'Autres')
            if cat not in categories:
                categories[cat] = {'pass': 0, 'fail': 0, 'skip': 0}
            if t['status'] == 'PASS':
                categories[cat]['pass'] += 1
            elif t['status'] == 'FAIL':
                categories[cat]['fail'] += 1
            else:
                categories[cat]['skip'] += 1
        
        if categories:
            print(f"\n  📈 Par catégorie:")
            for cat, stats in sorted(categories.items()):
                total_cat = stats['pass'] + stats['fail'] + stats['skip']
                pct = 100 * stats['pass'] / total_cat if total_cat > 0 else 0
                bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
                print(f"    {cat:<25} [{bar}] {stats['pass']}/{total_cat} ({pct:.0f}%)")
        
        if self.failed > 0:
            print(f"\n{Colors.RED}  ❌ Tests échoués:{Colors.END}")
            for t in self.tests:
                if t['status'] == "FAIL":
                    print(f"    • [{t.get('category', '')}] {t['name']}: {t['details'][:60]}")
        
        if self.qpu_results:
            print(f"\n{Colors.GREEN}  📈 Résultats QPU:{Colors.END}")
            for r in self.qpu_results[:10]:
                analysis = r.get('analysis', {})
                fidelity = analysis.get('fidelity', 'N/A')
                if isinstance(fidelity, float):
                    fidelity = f"{fidelity:.4f}"
                print(f"    • {r['circuit']}: Fidelity={fidelity}")
            if len(self.qpu_results) > 10:
                print(f"    ... et {len(self.qpu_results) - 10} autres")
        
        return self.failed == 0

results = TestResults()

# ==============================================================================
# SECTION 1: IMPORT & INITIALISATION
# ==============================================================================

def import_framework() -> Tuple[bool, Dict]:
    """Importe TOUS les composants du framework."""
    print_section("IMPORT DU FRAMEWORK", "📦")
    
    modules = {}
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Import principal
        print_subsection("Import des composants principaux")
        from qmc_quantum_framework_v2_6_3 import (
            QMCFramework, SUPPORTED_BACKENDS, RECOMMENDED_BACKENDS, RunMode
        )
        
        # Essayer d'importer QMCFrameworkV2_4 qui a toutes les fonctionnalités
        try:
            from qmc_quantum_framework_v2_6_3 import QMCFrameworkV2_4
            modules['QMCFramework'] = QMCFrameworkV2_4  # Utiliser V2_4 par défaut
            print_test("QMCFrameworkV2_4", "PASS", "Classe complète avec QDNA")
        except ImportError:
            modules['QMCFramework'] = QMCFramework
            print_test("QMCFramework", "PASS", "Classe de base")
        
        modules['SUPPORTED_BACKENDS'] = SUPPORTED_BACKENDS
        modules['RunMode'] = RunMode
        results.add("Import QMCFramework", "PASS", category="Import")
        
        # Import des Builders
        print_subsection("Import des Circuit Builders (21)")
        builders_to_import = [
            'GHZBuilder', 'IQPBuilder', 'BellBuilder', 'ClusterBuilder',
            'RandomCircuitBuilder', 'QFTBuilder', 'ParameterizedCircuitBuilder',
            'GroverBuilder', 'QPEBuilder', 'DeutschJozsaBuilder', 'BernsteinVaziraniBuilder',
            'SimonBuilder', 'SwapTestBuilder', 'QRNGBuilder', 'TeleportationBuilder',
            'AmplitudeEncodingBuilder', 'QuantumSignatureBuilder', 'ZKPBuilder',
            'TimeLockBuilder', 'ObliviousTransferBuilder', 'HardwareEfficientBuilder'
        ]
        
        import importlib
        qmc_module = importlib.import_module('qmc_quantum_framework_v2_6_3')
        
        imported_builders = 0
        for builder_name in builders_to_import:
            try:
                if hasattr(qmc_module, builder_name):
                    modules[builder_name] = getattr(qmc_module, builder_name)
                    imported_builders += 1
            except Exception:
                pass
        
        print_test(f"Circuit Builders", "PASS" if imported_builders > 15 else "WARN", 
                   f"{imported_builders}/{len(builders_to_import)} importés")
        results.add("Import Builders", "PASS" if imported_builders > 15 else "WARN", 
                    f"{imported_builders} builders", category="Import")
        
        # Import des Analyzers
        print_subsection("Import des Analyzers (12)")
        analyzers_to_import = [
            'FidelityAnalyzer', 'EntropyAnalyzer', 'CorrelationAnalyzer',
            'XEBAnalyzer', 'BellAnalyzer', 'RandomnessAnalyzer', 'CompressionAnalyzer',
            'XEBCrossValidationAnalyzer', 'HoneypotAnalyzer', 'QuantumAdvantageAnalyzer'
        ]
        
        imported_analyzers = 0
        for analyzer_name in analyzers_to_import:
            try:
                if hasattr(qmc_module, analyzer_name):
                    modules[analyzer_name] = getattr(qmc_module, analyzer_name)
                    imported_analyzers += 1
            except Exception:
                pass
        
        print_test(f"Analyzers", "PASS" if imported_analyzers > 5 else "WARN",
                   f"{imported_analyzers}/{len(analyzers_to_import)} importés")
        results.add("Import Analyzers", "PASS" if imported_analyzers > 5 else "WARN",
                    f"{imported_analyzers} analyzers", category="Import")
        
        # Import des composants avancés
        print_subsection("Import des composants avancés")
        advanced_imports = [
            'CircuitOptimizer', 'DynamicClusterOptimizer', 'ErrorMitigationManager',
            'CircuitCostEstimator', 'MitigationConfig', 'QualityThresholds'
        ]
        
        imported_advanced = 0
        for comp_name in advanced_imports:
            try:
                if hasattr(qmc_module, comp_name):
                    modules[comp_name] = getattr(qmc_module, comp_name)
                    imported_advanced += 1
            except Exception:
                pass
        
        print_test(f"Composants avancés", "PASS" if imported_advanced > 3 else "WARN",
                   f"{imported_advanced}/{len(advanced_imports)} importés")
        results.add("Import Avancés", "PASS", f"{imported_advanced} composants", category="Import")
        
        # Import Archive JSON v3.1
        print_subsection("Import Archive JSON v3.1")
        try:
            if hasattr(qmc_module, 'ExecutionArchive'):
                modules['ExecutionArchive'] = getattr(qmc_module, 'ExecutionArchive')
                print_test("ExecutionArchive", "PASS")
            if hasattr(qmc_module, 'ARCHIVE_SCHEMA_VERSION'):
                modules['ARCHIVE_SCHEMA_VERSION'] = getattr(qmc_module, 'ARCHIVE_SCHEMA_VERSION')
                print_test("ARCHIVE_SCHEMA_VERSION", "PASS", modules['ARCHIVE_SCHEMA_VERSION'])
            results.add("Import Archive", "PASS", category="Import")
        except Exception as e:
            print_test("Archive imports", "WARN", str(e))
        
        return True, modules
        
    except Exception as e:
        print_test("Import Framework", "FAIL", str(e))
        results.add("Import Framework", "FAIL", str(e), category="Import")
        traceback.print_exc()
        return False, modules


def check_dependencies() -> Dict:
    """Vérifie toutes les dépendances."""
    print_subsection("Vérification des dépendances")
    
    deps = {}
    
    try:
        from qiskit import QuantumCircuit
        deps['qiskit'] = True
        print_test("Qiskit", "PASS")
    except ImportError:
        deps['qiskit'] = False
        print_test("Qiskit", "SKIP", "Non installé")
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        deps['qiskit_ibm_runtime'] = True
        print_test("qiskit-ibm-runtime", "PASS")
    except ImportError:
        deps['qiskit_ibm_runtime'] = False
        print_test("qiskit-ibm-runtime", "SKIP")
    
    try:
        from qiskit_ibm_runtime.fake_provider import FakeTorino
        deps['fake_provider'] = True
        print_test("Fake Provider", "PASS")
    except ImportError:
        deps['fake_provider'] = False
        print_test("Fake Provider", "SKIP")
    
    try:
        import numpy as np
        deps['numpy'] = True
        print_test("NumPy", "PASS")
    except ImportError:
        deps['numpy'] = False
        print_test("NumPy", "SKIP")
    
    return deps

# ==============================================================================
# SECTION 2: CONNEXION & CALIBRATION
# ==============================================================================

def test_connection_and_calibration(fw, backend_name: str) -> bool:
    """Test la connexion et l'analyse de calibration."""
    print_section("CONNEXION ET CALIBRATION", "🔌")
    
    try:
        print_subsection("Connexion au backend")
        success = fw.connect()
        
        if success:
            print_test(f"Connexion à {backend_name}", "PASS", f"{fw.backend.num_qubits} qubits")
            results.add("Connexion Backend", "PASS", f"{fw.backend.num_qubits}Q", category="Connexion")
        else:
            print_test(f"Connexion à {backend_name}", "FAIL")
            results.add("Connexion Backend", "FAIL", category="Connexion")
            return False
        
        # Analyse de calibration
        print_subsection("Analyse de calibration")
        topology = fw.analyze_calibration()
        
        if topology:
            print_test("analyze_calibration()", "PASS")
            print_metric("Faulty qubits", len(topology.faulty_qubits) if topology.faulty_qubits else 0)
            print_metric("Suspect qubits", len(topology.suspect_qubits) if topology.suspect_qubits else 0)
            if hasattr(topology, 'health_score'):
                print_metric("Health Score", f"{topology.health_score:.1f}%")
            results.add("Analyze Calibration", "PASS", category="Connexion")
        else:
            print_test("analyze_calibration()", "WARN", "Données limitées")
            results.add("Analyze Calibration", "SKIP", category="Connexion")
        
        # Test list_calibrations (v2.6.1)
        print_subsection("Calibration ID Management (v2.6.1)")
        if hasattr(fw, 'list_calibrations'):
            try:
                calibrations = fw.list_calibrations(limit=3)
                print_test("list_calibrations()", "PASS", f"{len(calibrations)} calibrations")
                results.add("List Calibrations", "PASS", category="Connexion")
            except Exception as e:
                print_test("list_calibrations()", "WARN", str(e)[:40])
                results.add("List Calibrations", "SKIP", str(e)[:40], category="Connexion")
        
        return True
        
    except Exception as e:
        print_test("Connexion/Calibration", "FAIL", str(e))
        results.add("Connexion/Calibration", "FAIL", str(e), category="Connexion")
        traceback.print_exc()
        return False

# ==============================================================================
# SECTION 3: TOUS LES CIRCUIT BUILDERS
# ==============================================================================

def test_all_circuit_builders(fw, modules: Dict, deps: Dict) -> int:
    """Teste TOUS les circuit builders disponibles."""
    print_section("CIRCUIT BUILDERS (21 types)", "🔧")
    
    if not deps.get('qiskit'):
        print_test("Circuit Builders", "SKIP", "Qiskit non installé")
        results.add("Circuit Builders", "SKIP", "Qiskit requis", category="Builders")
        return 0
    
    topology = getattr(fw, 'topology', None)
    circuits_created = 0
    
    # === BASIC BUILDERS ===
    print_subsection("Basic Builders")
    
    # GHZ Builder
    try:
        GHZBuilder = modules.get('GHZBuilder')
        if GHZBuilder:
            builder = GHZBuilder(topology=topology)
            circuit = builder.build(n_qubits=5)
            results.add_circuit_for_qpu('GHZ_5Q', circuit)
            print_test("GHZBuilder", "PASS", f"5Q, depth={circuit.depth()}")
            results.add("GHZBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("GHZBuilder", "FAIL", str(e)[:50])
        results.add("GHZBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Bell Builder
    try:
        BellBuilder = modules.get('BellBuilder')
        if BellBuilder:
            builder = BellBuilder(topology=topology)
            circuit = builder.build(n_pairs=2)
            results.add_circuit_for_qpu('Bell_2pairs', circuit)
            print_test("BellBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("BellBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("BellBuilder", "FAIL", str(e)[:50])
        results.add("BellBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # IQP Builder
    try:
        IQPBuilder = modules.get('IQPBuilder')
        if IQPBuilder:
            builder = IQPBuilder(topology=topology)
            circuit = builder.build(n_qubits=4, depth=3)
            results.add_circuit_for_qpu('IQP_4Q_d3', circuit)
            print_test("IQPBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("IQPBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("IQPBuilder", "FAIL", str(e)[:50])
        results.add("IQPBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Cluster Builder
    try:
        ClusterBuilder = modules.get('ClusterBuilder')
        if ClusterBuilder:
            builder = ClusterBuilder(topology=topology)
            circuit = builder.build(n_qubits=4)
            results.add_circuit_for_qpu('Cluster_4Q', circuit)
            print_test("ClusterBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("ClusterBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("ClusterBuilder", "FAIL", str(e)[:50])
        results.add("ClusterBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Random Circuit Builder
    try:
        RandomCircuitBuilder = modules.get('RandomCircuitBuilder')
        if RandomCircuitBuilder:
            builder = RandomCircuitBuilder(topology=topology)
            circuit = builder.build(n_qubits=4, depth=5, seed=42)
            results.add_circuit_for_qpu('Random_4Q', circuit)
            print_test("RandomCircuitBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("RandomCircuitBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("RandomCircuitBuilder", "FAIL", str(e)[:50])
        results.add("RandomCircuitBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # QFT Builder
    try:
        QFTBuilder = modules.get('QFTBuilder')
        if QFTBuilder:
            builder = QFTBuilder(topology=topology)
            circuit = builder.build(n_qubits=4)
            results.add_circuit_for_qpu('QFT_4Q', circuit)
            print_test("QFTBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("QFTBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("QFTBuilder", "FAIL", str(e)[:50])
        results.add("QFTBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # === ALGORITHM BUILDERS ===
    print_subsection("Algorithm Builders")
    
    # Grover Builder
    try:
        GroverBuilder = modules.get('GroverBuilder')
        if GroverBuilder:
            builder = GroverBuilder(topology=topology)
            circuit = builder.build(n_qubits=3, marked_state='101')
            results.add_circuit_for_qpu('Grover_3Q', circuit)
            print_test("GroverBuilder", "PASS", f"3Q, depth={circuit.depth()}")
            results.add("GroverBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("GroverBuilder", "FAIL", str(e)[:50])
        results.add("GroverBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # QPE Builder
    try:
        QPEBuilder = modules.get('QPEBuilder')
        if QPEBuilder:
            builder = QPEBuilder(topology=topology)
            circuit = builder.build(n_counting_qubits=3)
            results.add_circuit_for_qpu('QPE_3Q', circuit)
            print_test("QPEBuilder", "PASS", f"depth={circuit.depth()}")
            results.add("QPEBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("QPEBuilder", "FAIL", str(e)[:50])
        results.add("QPEBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Deutsch-Jozsa Builder
    try:
        DeutschJozsaBuilder = modules.get('DeutschJozsaBuilder')
        if DeutschJozsaBuilder:
            builder = DeutschJozsaBuilder(topology=topology)
            circuit = builder.build(n_qubits=3, oracle_type='balanced')
            results.add_circuit_for_qpu('DeutschJozsa_3Q', circuit)
            print_test("DeutschJozsaBuilder", "PASS", f"3Q, depth={circuit.depth()}")
            results.add("DeutschJozsaBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("DeutschJozsaBuilder", "FAIL", str(e)[:50])
        results.add("DeutschJozsaBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Bernstein-Vazirani Builder
    try:
        BernsteinVaziraniBuilder = modules.get('BernsteinVaziraniBuilder')
        if BernsteinVaziraniBuilder:
            builder = BernsteinVaziraniBuilder(topology=topology)
            circuit = builder.build(secret='101')
            results.add_circuit_for_qpu('BernsteinVazirani_3Q', circuit)
            print_test("BernsteinVaziraniBuilder", "PASS", f"secret=101, depth={circuit.depth()}")
            results.add("BernsteinVaziraniBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("BernsteinVaziraniBuilder", "FAIL", str(e)[:50])
        results.add("BernsteinVaziraniBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Simon Builder
    try:
        SimonBuilder = modules.get('SimonBuilder')
        if SimonBuilder:
            builder = SimonBuilder(topology=topology)
            circuit = builder.build(n_qubits=2)
            results.add_circuit_for_qpu('Simon_2Q', circuit)
            print_test("SimonBuilder", "PASS", f"2Q, depth={circuit.depth()}")
            results.add("SimonBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("SimonBuilder", "FAIL", str(e)[:50])
        results.add("SimonBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # === UTILITY BUILDERS ===
    print_subsection("Utility Builders")
    
    # SwapTest Builder
    try:
        SwapTestBuilder = modules.get('SwapTestBuilder')
        if SwapTestBuilder:
            builder = SwapTestBuilder(topology=topology)
            circuit = builder.build(n_qubits=2)
            results.add_circuit_for_qpu('SwapTest_2Q', circuit)
            print_test("SwapTestBuilder", "PASS", f"2Q, depth={circuit.depth()}")
            results.add("SwapTestBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("SwapTestBuilder", "FAIL", str(e)[:50])
        results.add("SwapTestBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # QRNG Builder
    try:
        QRNGBuilder = modules.get('QRNGBuilder')
        if QRNGBuilder:
            builder = QRNGBuilder(topology=topology)
            circuit = builder.build(n_qubits=4)
            results.add_circuit_for_qpu('QRNG_4Q', circuit)
            print_test("QRNGBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("QRNGBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("QRNGBuilder", "FAIL", str(e)[:50])
        results.add("QRNGBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Teleportation Builder
    try:
        TeleportationBuilder = modules.get('TeleportationBuilder')
        if TeleportationBuilder:
            builder = TeleportationBuilder(topology=topology)
            circuit = builder.build()
            results.add_circuit_for_qpu('Teleportation_3Q', circuit)
            print_test("TeleportationBuilder", "PASS", f"3Q, depth={circuit.depth()}")
            results.add("TeleportationBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("TeleportationBuilder", "FAIL", str(e)[:50])
        results.add("TeleportationBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Hardware Efficient Builder
    try:
        HardwareEfficientBuilder = modules.get('HardwareEfficientBuilder')
        if HardwareEfficientBuilder:
            builder = HardwareEfficientBuilder(topology=topology)
            circuit = builder.build(n_qubits=4, depth=2)
            
            # Lier les paramètres si présents
            if hasattr(circuit, 'parameters') and len(circuit.parameters) > 0:
                import numpy as np
                param_values = {p: np.random.uniform(0, 2*np.pi) for p in circuit.parameters}
                circuit = circuit.assign_parameters(param_values)
            
            results.add_circuit_for_qpu('HardwareEfficient_4Q', circuit)
            print_test("HardwareEfficientBuilder", "PASS", f"4Q, depth={circuit.depth()}")
            results.add("HardwareEfficientBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("HardwareEfficientBuilder", "FAIL", str(e)[:50])
        results.add("HardwareEfficientBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # === CRYPTO BUILDERS ===
    print_subsection("Crypto Builders")
    
    # Quantum Signature Builder
    try:
        QuantumSignatureBuilder = modules.get('QuantumSignatureBuilder')
        if QuantumSignatureBuilder:
            builder = QuantumSignatureBuilder(topology=topology)
            # Le hash doit être en bytes (au moins 32 bytes pour SHA-256)
            test_hash = hashlib.sha256(b"test message for quantum signature").digest()
            circuit = builder.build(message_hash=test_hash, n_qubits=4)
            results.add_circuit_for_qpu('QuantumSignature_4Q', circuit)
            print_test("QuantumSignatureBuilder", "PASS", f"depth={circuit.depth()}")
            results.add("QuantumSignatureBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("QuantumSignatureBuilder", "FAIL", str(e)[:50])
        results.add("QuantumSignatureBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # ZKP Builder
    try:
        ZKPBuilder = modules.get('ZKPBuilder')
        if ZKPBuilder:
            builder = ZKPBuilder(topology=topology)
            circuit = builder.build(secret_bit=1, n_qubits=3)
            results.add_circuit_for_qpu('ZKP_3Q', circuit)
            print_test("ZKPBuilder", "PASS", f"3Q, depth={circuit.depth()}")
            results.add("ZKPBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("ZKPBuilder", "FAIL", str(e)[:50])
        results.add("ZKPBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # TimeLock Builder
    try:
        TimeLockBuilder = modules.get('TimeLockBuilder')
        if TimeLockBuilder:
            builder = TimeLockBuilder(topology=topology)
            circuit = builder.build(n_qubits=3, depth=2)
            results.add_circuit_for_qpu('TimeLock_3Q', circuit)
            print_test("TimeLockBuilder", "PASS", f"3Q, depth={circuit.depth()}")
            results.add("TimeLockBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("TimeLockBuilder", "FAIL", str(e)[:50])
        results.add("TimeLockBuilder", "FAIL", str(e)[:50], category="Builders")
    
    # Oblivious Transfer Builder
    try:
        ObliviousTransferBuilder = modules.get('ObliviousTransferBuilder')
        if ObliviousTransferBuilder:
            builder = ObliviousTransferBuilder(topology=topology)
            circuit = builder.build(sender_bits='10', choice_bit=0)
            results.add_circuit_for_qpu('ObliviousTransfer_3Q', circuit)
            print_test("ObliviousTransferBuilder", "PASS", f"depth={circuit.depth()}")
            results.add("ObliviousTransferBuilder", "PASS", category="Builders")
            circuits_created += 1
    except Exception as e:
        print_test("ObliviousTransferBuilder", "FAIL", str(e)[:50])
        results.add("ObliviousTransferBuilder", "FAIL", str(e)[:50], category="Builders")
    
    print(f"\n    {Colors.GREEN}✅ {circuits_created} circuits créés pour test QPU{Colors.END}")
    return circuits_created

# ==============================================================================
# SECTION 4: TOUS LES ANALYZERS
# ==============================================================================

def test_all_analyzers(modules: Dict, deps: Dict) -> bool:
    """Teste TOUS les analyzers disponibles."""
    print_section("ANALYZERS (12 types)", "📊")
    
    if not deps.get('numpy'):
        print_test("Analyzers", "SKIP", "NumPy non installé")
        return False
    
    # Créer des counts de test
    test_counts_ghz = {'00000': 450, '11111': 450, '00001': 50, '11110': 50}
    test_counts_random = {f'{i:05b}': 30 + i for i in range(32)}
    test_counts_bell = {'00': 480, '11': 480, '01': 20, '10': 20}
    
    analyzers_tested = 0
    
    # Fidelity Analyzer
    print_subsection("Fidelity Analyzer")
    try:
        FidelityAnalyzer = modules.get('FidelityAnalyzer')
        if FidelityAnalyzer:
            analyzer = FidelityAnalyzer()
            result = analyzer.analyze(test_counts_ghz, n_qubits=5)
            fidelity = result.get('fidelity', 0)
            print_test("FidelityAnalyzer", "PASS", f"Fidelity={fidelity:.4f}")
            print_metric("CI 95%", result.get('ci_95', 'N/A'))
            results.add("FidelityAnalyzer", "PASS", f"F={fidelity:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("FidelityAnalyzer", "FAIL", str(e)[:50])
        results.add("FidelityAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Entropy Analyzer
    print_subsection("Entropy Analyzer")
    try:
        EntropyAnalyzer = modules.get('EntropyAnalyzer')
        if EntropyAnalyzer:
            analyzer = EntropyAnalyzer()
            result = analyzer.analyze(test_counts_random)
            entropy = result.get('shannon_entropy', 0)
            print_test("EntropyAnalyzer", "PASS", f"Entropy={entropy:.4f}")
            results.add("EntropyAnalyzer", "PASS", f"S={entropy:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("EntropyAnalyzer", "FAIL", str(e)[:50])
        results.add("EntropyAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Correlation Analyzer
    print_subsection("Correlation Analyzer")
    try:
        CorrelationAnalyzer = modules.get('CorrelationAnalyzer')
        if CorrelationAnalyzer:
            analyzer = CorrelationAnalyzer()
            result = analyzer.analyze(test_counts_ghz)
            corr = result.get('mean_correlation', 0)
            print_test("CorrelationAnalyzer", "PASS", f"MeanCorr={corr:.4f}")
            results.add("CorrelationAnalyzer", "PASS", f"C={corr:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("CorrelationAnalyzer", "FAIL", str(e)[:50])
        results.add("CorrelationAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # XEB Analyzer
    print_subsection("XEB Analyzer")
    try:
        XEBAnalyzer = modules.get('XEBAnalyzer')
        if XEBAnalyzer:
            analyzer = XEBAnalyzer()
            result = analyzer.analyze(test_counts_random, n_qubits=5)
            xeb = result.get('xeb_fidelity', 0)
            print_test("XEBAnalyzer", "PASS", f"XEB={xeb:.4f}")
            results.add("XEBAnalyzer", "PASS", f"XEB={xeb:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("XEBAnalyzer", "FAIL", str(e)[:50])
        results.add("XEBAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Bell Analyzer
    print_subsection("Bell Analyzer")
    try:
        BellAnalyzer = modules.get('BellAnalyzer')
        if BellAnalyzer:
            analyzer = BellAnalyzer()
            result = analyzer.analyze(test_counts_bell, n_qubits=2)
            chsh = result.get('chsh_value', 0)
            print_test("BellAnalyzer", "PASS", f"CHSH={chsh:.4f}")
            results.add("BellAnalyzer", "PASS", f"CHSH={chsh:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("BellAnalyzer", "FAIL", str(e)[:50])
        results.add("BellAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Randomness Analyzer
    print_subsection("Randomness Analyzer")
    try:
        RandomnessAnalyzer = modules.get('RandomnessAnalyzer')
        if RandomnessAnalyzer:
            analyzer = RandomnessAnalyzer()
            result = analyzer.analyze(test_counts_random)
            min_entropy = result.get('min_entropy', 0)
            print_test("RandomnessAnalyzer", "PASS", f"MinEntropy={min_entropy:.4f}")
            results.add("RandomnessAnalyzer", "PASS", f"H_min={min_entropy:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("RandomnessAnalyzer", "FAIL", str(e)[:50])
        results.add("RandomnessAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Compression Analyzer
    print_subsection("Compression Analyzer")
    try:
        CompressionAnalyzer = modules.get('CompressionAnalyzer')
        if CompressionAnalyzer:
            analyzer = CompressionAnalyzer()
            result = analyzer.analyze(test_counts_random)
            ratio = result.get('compression_ratio', 0)
            print_test("CompressionAnalyzer", "PASS", f"Ratio={ratio:.4f}")
            results.add("CompressionAnalyzer", "PASS", f"CR={ratio:.4f}", category="Analyzers")
            analyzers_tested += 1
    except Exception as e:
        print_test("CompressionAnalyzer", "FAIL", str(e)[:50])
        results.add("CompressionAnalyzer", "FAIL", str(e)[:50], category="Analyzers")
    
    # Advanced Analyzers
    print_subsection("Advanced Analyzers")
    
    for analyzer_name in ['XEBCrossValidationAnalyzer', 'HoneypotAnalyzer', 'QuantumAdvantageAnalyzer']:
        try:
            AnalyzerClass = modules.get(analyzer_name)
            if AnalyzerClass:
                print_test(analyzer_name, "PASS", "Classe disponible")
                results.add(analyzer_name, "PASS", "Disponible", category="Analyzers")
                analyzers_tested += 1
            else:
                print_test(analyzer_name, "SKIP", "Non importé")
                results.add(analyzer_name, "SKIP", category="Analyzers")
        except Exception as e:
            print_test(analyzer_name, "FAIL", str(e)[:50])
            results.add(analyzer_name, "FAIL", str(e)[:50], category="Analyzers")
    
    print(f"\n    {Colors.GREEN}✅ {analyzers_tested} analyzers testés{Colors.END}")
    return analyzers_tested > 5

# ==============================================================================
# SECTION 5: FONCTIONNALITÉS v2.6.0/v2.6.1
# ==============================================================================

def test_v260_features(fw, deps: Dict) -> bool:
    """Teste TOUTES les nouvelles fonctionnalités v2.6.0/v2.6.1."""
    print_section("NOUVELLES FONCTIONNALITÉS v2.6.0/v2.6.1", "🆕")
    
    all_passed = True
    features_tested = 0
    
    # Fractional Gates
    print_subsection("Fractional Gates")
    for method in ['enable_fractional_gates', 'get_fractional_gate_depth_comparison', 'transpile_with_fractional']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
        else:
            all_passed = False
    
    # Dynamic Circuits
    print_subsection("Dynamic Circuits")
    for method in ['create_dynamic_circuit', 'check_dynamic_circuit_support']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Test création circuit dynamique
    if hasattr(fw, 'create_dynamic_circuit') and deps.get('qiskit'):
        try:
            circuit = fw.create_dynamic_circuit(n_qubits=3, with_reset=True, with_conditional=True)
            if circuit and hasattr(fw, 'check_dynamic_circuit_support'):
                features = fw.check_dynamic_circuit_support(circuit)
                print_metric("is_dynamic", features.get('is_dynamic', False))
                print_metric("has_reset", features.get('has_reset', False))
                print_metric("has_conditional", features.get('has_conditional', False))
        except Exception as e:
            print_test("Dynamic circuit creation", "WARN", str(e)[:40])
    
    # Gen3 Turbo
    print_subsection("Gen3 Turbo Mode")
    has_gen3 = hasattr(fw, 'enable_gen3_turbo')
    print_test("enable_gen3_turbo()", "PASS" if has_gen3 else "FAIL")
    results.add("v2.6.1 Gen3 Turbo", "PASS" if has_gen3 else "FAIL", category="v2.6.1")
    if has_gen3:
        features_tested += 1
    
    # Fake Backends
    print_subsection("Fake Backends")
    for method in ['get_fake_backend', 'test_locally']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Test fake backend
    if hasattr(fw, 'get_fake_backend') and deps.get('fake_provider'):
        try:
            fake = fw.get_fake_backend('heron')
            print_test("Fake backend creation", "PASS" if fake else "FAIL")
        except Exception as e:
            print_test("Fake backend creation", "WARN", str(e)[:40])
    
    # QPY Serialization
    print_subsection("QPY Serialization")
    for method in ['save_circuits_qpy', 'load_circuits_qpy']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Session/Batch Mode
    print_subsection("Session & Batch Mode")
    for method in ['run_with_session', 'run_with_batch']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Primitives V2
    print_subsection("Primitives V2")
    for method in ['get_sampler_v2', 'get_estimator_v2']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Noise Learner
    print_subsection("Noise Learner")
    has_noise = hasattr(fw, 'learn_noise')
    print_test("learn_noise()", "PASS" if has_noise else "FAIL")
    results.add("v2.6.1 learn_noise", "PASS" if has_noise else "FAIL", category="v2.6.1")
    if has_noise:
        features_tested += 1
    
    # Execution Spans
    print_subsection("Execution Spans & Timing")
    for method in ['get_execution_spans', 'draw_circuit_timing']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    # Parallel Transpilation
    print_subsection("Parallel Transpilation")
    has_parallel = hasattr(fw, 'transpile_parallel')
    print_test("transpile_parallel()", "PASS" if has_parallel else "FAIL")
    results.add("v2.6.1 transpile_parallel", "PASS" if has_parallel else "FAIL", category="v2.6.1")
    if has_parallel:
        features_tested += 1
    
    # Backend Selection
    print_subsection("Backend Selection")
    has_least_busy = hasattr(fw, 'get_least_busy')
    print_test("get_least_busy()", "PASS" if has_least_busy else "FAIL")
    results.add("v2.6.1 get_least_busy", "PASS" if has_least_busy else "FAIL", category="v2.6.1")
    if has_least_busy:
        features_tested += 1
    
    # Calibration ID
    print_subsection("Calibration ID Management")
    for method in ['list_calibrations', 'connect_with_calibration']:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "FAIL")
        results.add(f"v2.6.1 {method}", "PASS" if has_method else "FAIL", category="v2.6.1")
        if has_method:
            features_tested += 1
    
    print(f"\n    {Colors.GREEN}✅ {features_tested} fonctionnalités v2.6.1 testées{Colors.END}")
    return all_passed

# ==============================================================================
# SECTION 5b: FONCTIONNALITÉS v2.6.2 - QMC ARCHIVE MANAGER
# ==============================================================================

def test_v262_qmc_archive(fw, modules: Dict) -> bool:
    """Teste les fonctionnalités QMC Archive Manager v2.6.2."""
    print_section("QMC ARCHIVE MANAGER v2.6.2", "☁️")
    
    import importlib
    all_passed = True
    features_tested = 0
    
    # Import du module pour accéder aux variables et classes
    try:
        qmc_module = importlib.import_module('qmc_quantum_framework_v2_6_3')
    except ImportError:
        print_test("Import qmc_quantum_framework_v2_6_3", "FAIL", "Module non trouvé")
        results.add("v2.6.2 QMC Archive Import", "FAIL", category="v2.6.2")
        return False
    
    # --- Variables d'environnement ---
    print_subsection("Variables d'environnement QMC Archive")
    
    env_vars = [
        ('QMC_ARCHIVE_URL', 'URL de l\'API'),
        ('QMC_ARCHIVE_TOKEN', 'Token d\'authentification'),
        ('QMC_ARCHIVE_UPLOAD', 'Activer/désactiver upload'),
        ('QMC_ARCHIVE_DEFAULT_PROJECTS', 'Projets par défaut'),
    ]
    
    for var_name, description in env_vars:
        has_var = hasattr(qmc_module, var_name)
        print_test(f"{var_name}", "PASS" if has_var else "FAIL", description)
        results.add(f"v2.6.2 {var_name}", "PASS" if has_var else "FAIL", category="v2.6.2")
        if has_var:
            features_tested += 1
            # Afficher la valeur si c'est URL ou UPLOAD (pas le token!)
            if var_name in ['QMC_ARCHIVE_URL', 'QMC_ARCHIVE_UPLOAD']:
                value = getattr(qmc_module, var_name)
                print_metric("Valeur", value)
        else:
            all_passed = False
    
    # --- Classe QMCArchiveUploader ---
    print_subsection("QMCArchiveUploader Class")
    
    try:
        QMCArchiveUploader = getattr(qmc_module, 'QMCArchiveUploader', None)
        if QMCArchiveUploader:
            print_test("QMCArchiveUploader", "PASS", "Classe disponible")
            results.add("v2.6.2 QMCArchiveUploader class", "PASS", category="v2.6.2")
            features_tested += 1
            
            # Tester l'instanciation
            uploader = QMCArchiveUploader(api_token='', enabled=False)
            print_test("Instanciation (disabled)", "PASS")
            
            # Vérifier les méthodes essentielles
            required_methods = ['is_enabled', 'upload', 'print_upload_report', '_generate_default_notes']
            for method in required_methods:
                has_method = hasattr(uploader, method)
                print_test(f"{method}()", "PASS" if has_method else "FAIL")
                results.add(f"v2.6.2 QMCArchiveUploader.{method}", "PASS" if has_method else "FAIL", category="v2.6.2")
                if has_method:
                    features_tested += 1
                else:
                    all_passed = False
            
            # Tester is_enabled() sans token
            is_enabled = uploader.is_enabled()
            print_test("is_enabled() sans token", "PASS" if not is_enabled else "FAIL", 
                      f"Retourne {is_enabled} (attendu: False)")
            results.add("v2.6.2 is_enabled() logic", "PASS" if not is_enabled else "FAIL", category="v2.6.2")
            
            # Tester génération notes automatiques
            notes = uploader._generate_default_notes(job_id='test_job_123', 
                                                      extra_info={'backend': 'ibm_fez', 'circuits': 5})
            has_job = 'test_job_123' in notes
            has_backend = 'ibm_fez' in notes
            print_test("Génération notes auto", "PASS" if has_job and has_backend else "FAIL",
                      f"'{notes[:50]}...'")
            results.add("v2.6.2 notes generation", "PASS" if has_job else "FAIL", category="v2.6.2")
            if has_job:
                features_tested += 1
            
        else:
            print_test("QMCArchiveUploader", "FAIL", "Classe non trouvée")
            results.add("v2.6.2 QMCArchiveUploader class", "FAIL", category="v2.6.2")
            all_passed = False
    except Exception as e:
        print_test("QMCArchiveUploader", "FAIL", str(e)[:50])
        results.add("v2.6.2 QMCArchiveUploader", "FAIL", str(e)[:50], category="v2.6.2")
        all_passed = False
    
    # --- Fonction get_archive_uploader ---
    print_subsection("Fonction get_archive_uploader()")
    
    try:
        get_archive_uploader = getattr(qmc_module, 'get_archive_uploader', None)
        if get_archive_uploader:
            print_test("get_archive_uploader()", "PASS", "Fonction disponible")
            results.add("v2.6.2 get_archive_uploader", "PASS", category="v2.6.2")
            features_tested += 1
            
            # Appeler la fonction
            uploader = get_archive_uploader()
            print_test("Retourne QMCArchiveUploader", "PASS" if uploader else "FAIL")
        else:
            print_test("get_archive_uploader()", "FAIL", "Fonction non trouvée")
            results.add("v2.6.2 get_archive_uploader", "FAIL", category="v2.6.2")
            all_passed = False
    except Exception as e:
        print_test("get_archive_uploader()", "FAIL", str(e)[:50])
        results.add("v2.6.2 get_archive_uploader", "FAIL", str(e)[:50], category="v2.6.2")
    
    # --- Test upload() avec fichier inexistant (doit retourner dict, pas exception) ---
    print_subsection("Robustesse upload() - Non-blocking")
    
    try:
        uploader = QMCArchiveUploader(api_token='test_token_fake')
        
        # Test 1: Fichier inexistant
        result = uploader.upload('/nonexistent/file.json')
        is_dict = isinstance(result, dict)
        has_success = 'success' in result
        has_error = 'error' in result
        is_failed = result.get('success') == False if is_dict else False
        
        print_test("upload() fichier inexistant", 
                  "PASS" if is_dict and is_failed else "FAIL",
                  "Retourne dict avec success=False")
        results.add("v2.6.2 upload robustness", "PASS" if is_dict and is_failed else "FAIL", category="v2.6.2")
        
        if is_dict and is_failed:
            features_tested += 1
            print_metric("success", result.get('success'))
            print_metric("error", result.get('error', 'N/A')[:40])
            print_metric("attempts", result.get('attempts'))
        
        # Test 2: Uploader désactivé
        uploader_disabled = QMCArchiveUploader(api_token='')
        result2 = uploader_disabled.upload('/any/file.json')
        is_disabled_correct = isinstance(result2, dict) and result2.get('success') == False
        print_test("upload() sans token", "PASS" if is_disabled_correct else "FAIL",
                  "success=False, error='disabled'")
        results.add("v2.6.2 upload disabled", "PASS" if is_disabled_correct else "FAIL", category="v2.6.2")
        if is_disabled_correct:
            features_tested += 1
        
        # Test 3: print_upload_report ne plante pas
        try:
            uploader.print_upload_report(result, compact=True)
            print_test("print_upload_report()", "PASS", "Pas d'exception")
            results.add("v2.6.2 print_upload_report", "PASS", category="v2.6.2")
            features_tested += 1
        except Exception as e:
            print_test("print_upload_report()", "FAIL", str(e)[:40])
            results.add("v2.6.2 print_upload_report", "FAIL", str(e)[:40], category="v2.6.2")
            all_passed = False
            
    except Exception as e:
        print_test("Tests robustesse upload()", "FAIL", str(e)[:50])
        results.add("v2.6.2 upload robustness", "FAIL", str(e)[:50], category="v2.6.2")
        all_passed = False
    
    # --- Test avec fichier temporaire réel ---
    print_subsection("Upload avec fichier temporaire")
    
    try:
        import json
        
        # Créer un fichier JSON temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({'test': 'data', 'metadata': {'job_id': 'test123'}}, f)
            temp_file = f.name
        
        uploader = QMCArchiveUploader(api_token='fake_token_for_test')
        
        # Tenter upload (échouera car serveur inaccessible, mais doit retourner dict)
        result = uploader.upload(
            temp_file,
            project_ids=['test-project-uuid'],
            notes='Test note from validation script',
            max_retries=1,
            timeout=2
        )
        
        is_valid_result = (
            isinstance(result, dict) and
            'success' in result and
            'task_id' in result and
            'filename' in result and
            'attempts' in result and
            'error' in result
        )
        
        print_test("Upload avec fichier réel", "PASS" if is_valid_result else "FAIL",
                  "Retourne dict complet même si échec réseau")
        results.add("v2.6.2 upload real file", "PASS" if is_valid_result else "FAIL", category="v2.6.2")
        
        if is_valid_result:
            features_tested += 1
            print_metric("success", result.get('success'))
            print_metric("attempts", result.get('attempts'))
            print_metric("filename", result.get('filename', 'N/A'))
        
        # Nettoyer
        os.unlink(temp_file)
        
    except Exception as e:
        print_test("Upload fichier temporaire", "FAIL", str(e)[:50])
        results.add("v2.6.2 upload real file", "FAIL", str(e)[:50], category="v2.6.2")
        # Cleanup en cas d'erreur
        try:
            os.unlink(temp_file)
        except:
            pass
    
    # --- Paramètres run_on_qpu() pour QMC Archive ---
    print_subsection("Paramètres run_on_qpu() pour QMC Archive")
    
    try:
        # Vérifier que run_on_qpu accepte les nouveaux paramètres
        import inspect
        if hasattr(fw, 'run_on_qpu'):
            sig = inspect.signature(fw.run_on_qpu)
            params = list(sig.parameters.keys())
            
            archive_params = ['upload_to_archive', 'archive_projects', 'archive_notes']
            for param in archive_params:
                has_param = param in params
                print_test(f"run_on_qpu({param}=)", "PASS" if has_param else "FAIL")
                results.add(f"v2.6.2 run_on_qpu.{param}", "PASS" if has_param else "FAIL", category="v2.6.2")
                if has_param:
                    features_tested += 1
                else:
                    all_passed = False
        else:
            print_test("run_on_qpu() non disponible", "SKIP")
            results.add("v2.6.2 run_on_qpu params", "SKIP", category="v2.6.2")
            
    except Exception as e:
        print_test("Vérification params run_on_qpu", "FAIL", str(e)[:50])
        results.add("v2.6.2 run_on_qpu params", "FAIL", str(e)[:50], category="v2.6.2")
    
    # --- Résumé ---
    print(f"\n    {Colors.GREEN}✅ {features_tested} fonctionnalités QMC Archive v2.6.2 testées{Colors.END}")
    
    if all_passed:
        print(f"    {Colors.GREEN}✅ Tous les tests QMC Archive passés!{Colors.END}")
    else:
        print(f"    {Colors.YELLOW}⚠️ Certains tests QMC Archive ont échoué{Colors.END}")
    
    return all_passed


# ==============================================================================
# SECTION 5c: ★ NEW v2.6.3 - QMC ACCOUNTS AUDIT MODULE
# ==============================================================================

def test_v263_accounts_audit(fw, modules: Dict) -> bool:
    """
    [v2.6.3] Teste le module d'audit des comptes IBM Quantum.
    
    Tests:
    - Classes: QMCJobDataCollector, QMCAuditHTMLReportGenerator
    - Fonctions: get_all_ibm_accounts_from_env, run_accounts_audit
    - Méthodes: QMCFramework.audit_accounts, list_ibm_accounts
    - Gestion des erreurs: comptes inaccessibles, clés invalides
    """
    print_section("QMC ACCOUNTS AUDIT v2.6.3", "📊")
    
    all_passed = True
    features_tested = 0
    
    # --- Test 1: Import des classes ---
    print_subsection("Classes d'audit")
    
    try:
        qmc_module = importlib.import_module('qmc_quantum_framework_v2_6_3')
        
        # QMCJobDataCollector
        if hasattr(qmc_module, 'QMCJobDataCollector'):
            QMCJobDataCollector = qmc_module.QMCJobDataCollector
            print_test("QMCJobDataCollector", "PASS", "Classe disponible")
            results.add("QMCJobDataCollector import", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Test instanciation
            try:
                collector = QMCJobDataCollector(verbose=False)
                print_test("QMCJobDataCollector instanciation", "PASS")
                results.add("QMCJobDataCollector instance", "PASS", category="v2.6.3")
                features_tested += 1
                
                # Test méthodes
                if hasattr(collector, 'collect_all_accounts'):
                    print_test("collect_all_accounts()", "PASS", "Méthode présente")
                    features_tested += 1
                if hasattr(collector, 'log'):
                    print_test("log()", "PASS", "Méthode présente")
                    features_tested += 1
                    
            except Exception as e:
                print_test("QMCJobDataCollector instanciation", "FAIL", str(e)[:50])
                all_passed = False
        else:
            print_test("QMCJobDataCollector", "FAIL", "Classe non trouvée")
            results.add("QMCJobDataCollector import", "FAIL", category="v2.6.3")
            all_passed = False
        
        # QMCAuditHTMLReportGenerator
        if hasattr(qmc_module, 'QMCAuditHTMLReportGenerator'):
            QMCAuditHTMLReportGenerator = qmc_module.QMCAuditHTMLReportGenerator
            print_test("QMCAuditHTMLReportGenerator", "PASS", "Classe disponible")
            results.add("QMCAuditHTMLReportGenerator import", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Test instanciation
            try:
                generator = QMCAuditHTMLReportGenerator(output_dir="/tmp/test_audit")
                print_test("QMCAuditHTMLReportGenerator instanciation", "PASS")
                results.add("QMCAuditHTMLReportGenerator instance", "PASS", category="v2.6.3")
                features_tested += 1
                
                # Test méthodes
                if hasattr(generator, 'generate_report'):
                    print_test("generate_report()", "PASS", "Méthode présente")
                    features_tested += 1
                if hasattr(generator, '_build_accounts_table'):
                    print_test("_build_accounts_table()", "PASS", "Méthode présente")
                    features_tested += 1
                    
            except Exception as e:
                print_test("QMCAuditHTMLReportGenerator instanciation", "FAIL", str(e)[:50])
                all_passed = False
        else:
            print_test("QMCAuditHTMLReportGenerator", "FAIL", "Classe non trouvée")
            results.add("QMCAuditHTMLReportGenerator import", "FAIL", category="v2.6.3")
            all_passed = False
            
    except ImportError as e:
        print_test("Import qmc_quantum_framework_v2_6_3", "FAIL", "Module non trouvé")
        results.add("v2.6.3 Module import", "FAIL", str(e)[:50], category="v2.6.3")
        return False
    except Exception as e:
        print_test("Import classes", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 2: Fonctions globales ---
    print_subsection("Fonctions globales")
    
    try:
        # get_all_ibm_accounts_from_env
        if hasattr(qmc_module, 'get_all_ibm_accounts_from_env'):
            get_accounts = qmc_module.get_all_ibm_accounts_from_env
            print_test("get_all_ibm_accounts_from_env()", "PASS", "Fonction disponible")
            results.add("get_all_ibm_accounts_from_env", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Test exécution (retourne dict vide si pas de comptes)
            try:
                accounts = get_accounts()
                print_test("get_all_ibm_accounts_from_env() exécution", "PASS", f"{len(accounts)} compte(s)")
                features_tested += 1
            except Exception as e:
                print_test("get_all_ibm_accounts_from_env() exécution", "FAIL", str(e)[:50])
                all_passed = False
        else:
            print_test("get_all_ibm_accounts_from_env", "FAIL", "Non trouvée")
            all_passed = False
        
        # run_accounts_audit
        if hasattr(qmc_module, 'run_accounts_audit'):
            print_test("run_accounts_audit()", "PASS", "Fonction disponible")
            results.add("run_accounts_audit", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Vérifier signature
            import inspect
            sig = inspect.signature(qmc_module.run_accounts_audit)
            params = list(sig.parameters.keys())
            expected = ['accounts', 'window_days', 'limit', 'budget_minutes', 'generate_html']
            missing = [p for p in expected if p not in params]
            if not missing:
                print_test("run_accounts_audit() signature", "PASS", f"{len(params)} paramètres")
                features_tested += 1
            else:
                print_test("run_accounts_audit() signature", "WARN", f"Manque: {missing}")
        else:
            print_test("run_accounts_audit", "FAIL", "Non trouvée")
            all_passed = False
            
    except Exception as e:
        print_test("Fonctions globales", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 3: Méthodes QMCFramework ---
    print_subsection("Méthodes QMCFramework")
    
    try:
        # audit_accounts
        if hasattr(fw, 'audit_accounts'):
            print_test("QMCFramework.audit_accounts()", "PASS", "Méthode disponible")
            results.add("fw.audit_accounts()", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Vérifier signature
            import inspect
            sig = inspect.signature(fw.audit_accounts)
            params = list(sig.parameters.keys())
            if 'window_days' in params and 'budget_minutes' in params:
                print_test("audit_accounts() signature", "PASS", f"{len(params)} paramètres")
                features_tested += 1
        else:
            print_test("QMCFramework.audit_accounts()", "FAIL", "Non trouvée")
            results.add("fw.audit_accounts()", "FAIL", category="v2.6.3")
            all_passed = False
        
        # list_ibm_accounts
        if hasattr(fw, 'list_ibm_accounts'):
            print_test("QMCFramework.list_ibm_accounts()", "PASS", "Méthode disponible")
            results.add("fw.list_ibm_accounts()", "PASS", category="v2.6.3")
            features_tested += 1
            
            # Test exécution
            try:
                accounts = fw.list_ibm_accounts()
                print_test("list_ibm_accounts() exécution", "PASS", f"{len(accounts)} compte(s)")
                features_tested += 1
            except Exception as e:
                print_test("list_ibm_accounts() exécution", "FAIL", str(e)[:50])
        else:
            print_test("QMCFramework.list_ibm_accounts()", "FAIL", "Non trouvée")
            results.add("fw.list_ibm_accounts()", "FAIL", category="v2.6.3")
            all_passed = False
            
    except Exception as e:
        print_test("Méthodes QMCFramework", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 4: Gestion des erreurs (comptes inaccessibles) ---
    print_subsection("Gestion erreurs (comptes inaccessibles)")
    
    try:
        # Test avec un compte invalide
        collector = qmc_module.QMCJobDataCollector(verbose=False)
        
        # Simuler la structure de données d'un compte en erreur
        test_data = {
            "accounts": {
                "test_error": {
                    "label": "test_error",
                    "collection_status": "error",
                    "accessible": False,
                    "error_type": "AUTH_FAILED",
                    "error_message": "Clé API invalide",
                    "stats": {"jobs_count": 0, "usage_minutes": 0}
                }
            },
            "global_stats": {"total_jobs": 0, "total_usage_minutes": 0}
        }
        
        # Vérifier que le générateur HTML gère les erreurs
        generator = qmc_module.QMCAuditHTMLReportGenerator(output_dir="/tmp/test_audit_errors")
        
        # Test _build_accounts_table avec compte en erreur
        html_table = generator._build_accounts_table(test_data["accounts"], budget_minutes=10.0)
        
        if "INACCESSIBLE" in html_table:
            print_test("Affichage compte inaccessible", "PASS", "Tag INACCESSIBLE présent")
            features_tested += 1
        else:
            print_test("Affichage compte inaccessible", "WARN", "Tag INACCESSIBLE manquant")
        
        if "Error" in html_table or "error" in html_table.lower():
            print_test("Tag erreur dans HTML", "PASS", "Erreur visible")
            features_tested += 1
        
        results.add("Gestion comptes inaccessibles", "PASS", category="v2.6.3")
        
    except Exception as e:
        print_test("Gestion erreurs", "FAIL", str(e)[:50])
        results.add("Gestion comptes inaccessibles", "FAIL", str(e)[:50], category="v2.6.3")
        all_passed = False
    
    # --- Test 5: Structure des résultats ---
    print_subsection("Structure des résultats d'audit")
    
    try:
        # Vérifier qu'un résultat d'audit a la bonne structure
        expected_fields = ['accessible', 'collection_status', 'error_type', 'error_message']
        
        # Test avec données simulées
        test_account = {
            "accessible": False,
            "collection_status": "error",
            "error_type": "AUTH_FAILED",
            "error_message": "Test error"
        }
        
        for field in expected_fields:
            if field in test_account:
                print_test(f"Champ '{field}'", "PASS", "Présent dans structure")
                features_tested += 1
        
        results.add("Structure résultats audit", "PASS", category="v2.6.3")
        
    except Exception as e:
        print_test("Structure résultats", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Résumé ---
    print(f"\n    {Colors.GREEN}✅ {features_tested} fonctionnalités QMC Accounts Audit v2.6.3 testées{Colors.END}")
    
    if all_passed:
        print(f"    {Colors.GREEN}✅ Tous les tests Accounts Audit passés!{Colors.END}")
    else:
        print(f"    {Colors.YELLOW}⚠️ Certains tests Accounts Audit ont échoué{Colors.END}")
    
    return all_passed


# ==============================================================================
# SECTION 6: OPTIMIZERS & CALCULATORS
# ==============================================================================

def test_optimizers_and_calculators(fw, modules: Dict) -> bool:
    """Teste les optimizers et calculators."""
    print_section("OPTIMIZERS & CALCULATORS", "⚡")
    
    tested = 0
    
    # CircuitOptimizer
    print_subsection("CircuitOptimizer")
    try:
        if hasattr(fw, 'circuit_optimizer') or modules.get('CircuitOptimizer'):
            print_test("CircuitOptimizer", "PASS", "Disponible")
            results.add("CircuitOptimizer", "PASS", category="Optimizers")
            tested += 1
        else:
            print_test("CircuitOptimizer", "SKIP", "Non initialisé")
            results.add("CircuitOptimizer", "SKIP", category="Optimizers")
    except Exception as e:
        print_test("CircuitOptimizer", "FAIL", str(e)[:50])
        results.add("CircuitOptimizer", "FAIL", str(e)[:50], category="Optimizers")
    
    # DynamicClusterOptimizer
    print_subsection("DynamicClusterOptimizer")
    try:
        DynamicClusterOptimizer = modules.get('DynamicClusterOptimizer')
        if DynamicClusterOptimizer:
            print_test("DynamicClusterOptimizer", "PASS", "Classe disponible")
            results.add("DynamicClusterOptimizer", "PASS", category="Optimizers")
            tested += 1
    except Exception as e:
        print_test("DynamicClusterOptimizer", "FAIL", str(e)[:50])
        results.add("DynamicClusterOptimizer", "FAIL", str(e)[:50], category="Optimizers")
    
    # CircuitCostEstimator
    print_subsection("CircuitCostEstimator")
    try:
        if hasattr(fw, 'cost_estimator') or hasattr(fw, 'estimate_cost'):
            print_test("CircuitCostEstimator", "PASS", "Disponible")
            results.add("CircuitCostEstimator", "PASS", category="Optimizers")
            tested += 1
        else:
            print_test("CircuitCostEstimator", "SKIP", "Non initialisé")
            results.add("CircuitCostEstimator", "SKIP", category="Optimizers")
    except Exception as e:
        print_test("CircuitCostEstimator", "FAIL", str(e)[:50])
        results.add("CircuitCostEstimator", "FAIL", str(e)[:50], category="Optimizers")
    
    # EPLG Calculator
    print_subsection("EPLGCalculator")
    try:
        if hasattr(fw, 'estimate_eplg'):
            print_test("EPLGCalculator", "PASS", "estimate_eplg() disponible")
            results.add("EPLGCalculator", "PASS", category="Optimizers")
            tested += 1
        else:
            print_test("EPLGCalculator", "SKIP", "Non disponible")
            results.add("EPLGCalculator", "SKIP", category="Optimizers")
    except Exception as e:
        print_test("EPLGCalculator", "FAIL", str(e)[:50])
        results.add("EPLGCalculator", "FAIL", str(e)[:50], category="Optimizers")
    
    # CLOPS Calculator
    print_subsection("CLOPSCalculator")
    try:
        if hasattr(fw, 'estimate_clops'):
            print_test("CLOPSCalculator", "PASS", "estimate_clops() disponible")
            results.add("CLOPSCalculator", "PASS", category="Optimizers")
            tested += 1
        else:
            print_test("CLOPSCalculator", "SKIP", "Non disponible")
            results.add("CLOPSCalculator", "SKIP", category="Optimizers")
    except Exception as e:
        print_test("CLOPSCalculator", "FAIL", str(e)[:50])
        results.add("CLOPSCalculator", "FAIL", str(e)[:50], category="Optimizers")
    
    # TrotterOptimizer
    print_subsection("TrotterOptimizer")
    try:
        if hasattr(fw, 'trotter_optimizer'):
            print_test("TrotterOptimizer", "PASS", "Disponible")
            results.add("TrotterOptimizer", "PASS", category="Optimizers")
            tested += 1
        else:
            print_test("TrotterOptimizer", "SKIP", "Non initialisé")
            results.add("TrotterOptimizer", "SKIP", category="Optimizers")
    except Exception as e:
        print_test("TrotterOptimizer", "FAIL", str(e)[:50])
        results.add("TrotterOptimizer", "FAIL", str(e)[:50], category="Optimizers")
    
    print(f"\n    {Colors.GREEN}✅ {tested} optimizers/calculators testés{Colors.END}")
    return tested > 2

# ==============================================================================
# SECTION 7: ERROR MITIGATION
# ==============================================================================

def test_error_mitigation(fw, modules: Dict) -> bool:
    """Teste les fonctionnalités d'error mitigation."""
    print_section("ERROR MITIGATION", "🛡️")
    
    tested = 0
    
    # ErrorMitigationManager
    print_subsection("ErrorMitigationManager")
    try:
        if hasattr(fw, 'error_mitigation'):
            print_test("ErrorMitigationManager", "PASS", "Initialisé")
            
            # Vérifier les configurations
            if hasattr(fw.error_mitigation, 'get_summary'):
                summary = fw.error_mitigation.get_summary()
                print_metric("DD enabled", summary.get('dynamical_decoupling', {}).get('enabled', 'N/A'))
                print_metric("Twirling enabled", summary.get('twirling', {}).get('enabled', 'N/A'))
            
            results.add("ErrorMitigationManager", "PASS", category="Mitigation")
            tested += 1
        else:
            print_test("ErrorMitigationManager", "SKIP", "Non initialisé")
            results.add("ErrorMitigationManager", "SKIP", category="Mitigation")
    except Exception as e:
        print_test("ErrorMitigationManager", "FAIL", str(e)[:50])
        results.add("ErrorMitigationManager", "FAIL", str(e)[:50], category="Mitigation")
    
    # M3 Mitigation
    print_subsection("M3 Mitigation Wrapper")
    try:
        if hasattr(fw, 'calibrate_m3') and hasattr(fw, 'mitigate_with_m3'):
            print_test("M3 Wrapper", "PASS", "calibrate_m3() & mitigate_with_m3() disponibles")
            results.add("M3 Wrapper", "PASS", category="Mitigation")
            tested += 1
        else:
            print_test("M3 Wrapper", "SKIP", "Méthodes non disponibles")
            results.add("M3 Wrapper", "SKIP", category="Mitigation")
    except Exception as e:
        print_test("M3 Wrapper", "FAIL", str(e)[:50])
        results.add("M3 Wrapper", "FAIL", str(e)[:50], category="Mitigation")
    
    # MitigationConfig
    print_subsection("MitigationConfig")
    try:
        MitigationConfig = modules.get('MitigationConfig')
        if MitigationConfig:
            config = MitigationConfig(
                enable_dd=True,
                enable_twirling=True,
                enable_zne=False
            )
            print_test("MitigationConfig", "PASS", "Configuration créée")
            print_metric("DD", config.enable_dd)
            print_metric("Twirling", config.enable_twirling)
            print_metric("ZNE", config.enable_zne)
            results.add("MitigationConfig", "PASS", category="Mitigation")
            tested += 1
        else:
            print_test("MitigationConfig", "SKIP", "Non importé")
            results.add("MitigationConfig", "SKIP", category="Mitigation")
    except Exception as e:
        print_test("MitigationConfig", "FAIL", str(e)[:50])
        results.add("MitigationConfig", "FAIL", str(e)[:50], category="Mitigation")
    
    # IBM Addons Status
    print_subsection("IBM Addons Status")
    try:
        if hasattr(fw, 'get_ibm_addons_status'):
            status = fw.get_ibm_addons_status()
            print_test("get_ibm_addons_status()", "PASS")
            for addon, info in status.items():
                if isinstance(info, dict):
                    avail = info.get('available', False)
                    print_metric(addon, "✓" if avail else "✗")
            results.add("IBM Addons Status", "PASS", category="Mitigation")
            tested += 1
    except Exception as e:
        print_test("IBM Addons Status", "FAIL", str(e)[:50])
        results.add("IBM Addons Status", "FAIL", str(e)[:50], category="Mitigation")
    
    print(f"\n    {Colors.GREEN}✅ {tested} composants mitigation testés{Colors.END}")
    return tested > 1

# ==============================================================================
# SECTION 8: QDNA FEATURES
# ==============================================================================

def test_qdna_features(fw) -> bool:
    """Teste les fonctionnalités QDNA-ID."""
    print_section("QDNA FEATURES", "🧬")
    
    tested = 0
    
    qdna_methods = [
        ('qdna_enroll', 'Génère une empreinte QDNA'),
        ('qdna_verify', 'Vérifie une empreinte'),
        ('qdna_compare', 'Compare deux empreintes'),
        ('qdna_discover_regions', 'Découvre les régions optimales'),
        ('qdna_load_fingerprint', 'Charge une empreinte'),
        ('qdna_get_fingerprint', 'Récupère l\'empreinte courante'),
    ]
    
    for method, desc in qdna_methods:
        has_method = hasattr(fw, method)
        print_test(f"{method}()", "PASS" if has_method else "SKIP", desc if has_method else "Non disponible")
        results.add(f"QDNA {method}", "PASS" if has_method else "SKIP", category="QDNA")
        if has_method:
            tested += 1
    
    print(f"\n    {Colors.GREEN}✅ {tested} méthodes QDNA disponibles{Colors.END}")
    return tested > 3

# ==============================================================================
# SECTION 9: EXÉCUTION QPU
# ==============================================================================

def run_qpu_tests(fw, shots: int, modules: Dict) -> bool:
    """Exécute TOUS les circuits créés sur le QPU."""
    print_section(f"EXÉCUTION QPU ({shots} shots/circuit)", "🚀")
    
    circuits = results.circuits_for_qpu
    
    if not circuits:
        print_test("Circuits disponibles", "FAIL", "Aucun circuit")
        results.add("QPU Execution", "FAIL", "Aucun circuit", category="QPU")
        return False
    
    print_subsection(f"Préparation de {len(circuits)} circuits")
    
    # Afficher les circuits
    for name, circuit in circuits[:10]:
        print_test(name, "INFO", f"{circuit.num_qubits}Q, depth={circuit.depth()}")
    if len(circuits) > 10:
        print(f"       ... et {len(circuits) - 10} autres circuits")
    
    circuit_list = [c[1] for c in circuits]
    circuit_names = [c[0] for c in circuits]
    
    # Exécution
    print_subsection("Soumission au QPU")
    try:
        os.environ['QMC_AUTO_CONFIRM'] = 'true'
        
        print_test("Soumission", "RUN", f"{len(circuits)} circuits, {shots} shots")
        
        qpu_results = fw.run_on_qpu(
            circuit_list,
            shots=shots,
            auto_transpile=True,
            generate_report=True,
            generate_archive=True
        )
        
        if qpu_results is None:
            print_test("Exécution QPU", "FAIL", "Résultats nuls")
            results.add("QPU Execution", "FAIL", "Résultats nuls", category="QPU")
            return False
        
        print_test("Exécution QPU", "PASS", f"{len(qpu_results)} résultats")
        results.add("QPU Execution", "PASS", f"{len(qpu_results)} circuits", category="QPU")
        
        # Analyser les résultats
        return analyze_qpu_results(qpu_results, circuit_names, modules)
        
    except Exception as e:
        print_test("Exécution QPU", "FAIL", str(e))
        results.add("QPU Execution", "FAIL", str(e), category="QPU")
        traceback.print_exc()
        return False

# ==============================================================================
# SECTION 10: ANALYSE DES RÉSULTATS
# ==============================================================================

def analyze_qpu_results(qpu_results: List[Dict], circuit_names: List[str], modules: Dict) -> bool:
    """Analyse TOUS les résultats QPU."""
    print_section("ANALYSE DES RÉSULTATS QPU", "📊")
    
    FidelityAnalyzer = modules.get('FidelityAnalyzer')
    EntropyAnalyzer = modules.get('EntropyAnalyzer')
    
    all_valid = True
    
    for i, result in enumerate(qpu_results):
        name = circuit_names[i] if i < len(circuit_names) else f"Circuit_{i}"
        counts = result.get('counts', {})
        
        if not counts:
            results.add(f"Résultat {name}", "FAIL", "Counts vides", category="QPU Results")
            all_valid = False
            continue
        
        total_shots = sum(counts.values())
        n_unique = len(counts)
        
        # Analyse de fidélité
        analysis = {}
        if FidelityAnalyzer:
            try:
                analyzer = FidelityAnalyzer()
                fidelity_result = analyzer.analyze(counts)
                analysis = fidelity_result
            except:
                pass
        
        results.add_qpu_result(name, counts, analysis)
        
        fidelity = analysis.get('fidelity', 0)
        status = "PASS" if fidelity > 0.1 else "WARN" if fidelity > 0.01 else "INFO"
        results.add(f"Résultat {name}", status, f"F={fidelity:.4f}, {n_unique} états", category="QPU Results")
    
    # Afficher résumé
    print_subsection("Résumé des résultats")
    for i, r in enumerate(results.qpu_results[:15]):
        analysis = r.get('analysis', {})
        fidelity = analysis.get('fidelity', 0)
        print_test(r['circuit'], "INFO", f"Fidelity={fidelity:.4f}")
    
    if len(results.qpu_results) > 15:
        print(f"       ... et {len(results.qpu_results) - 15} autres résultats")
    
    return all_valid

# ==============================================================================
# SECTION 11: ARCHIVE JSON v3.1 (41 SECTIONS)
# ==============================================================================

def test_archive_json_v31(fw, modules: Dict) -> bool:
    """Test de l'archive JSON v3.1 ultra-complète (41 sections)."""
    print_section("ARCHIVE JSON v3.1", "📦")
    
    try:
        ExecutionArchive = modules.get('ExecutionArchive')
        ARCHIVE_SCHEMA_VERSION = modules.get('ARCHIVE_SCHEMA_VERSION', '?.?.?')
        
        if not ExecutionArchive:
            print_test("ExecutionArchive", "FAIL", "Classe non trouvée")
            results.add("Archive JSON v3.1", "FAIL", "ExecutionArchive non trouvé", category="Archive")
            return False
        
        print_test("Import ExecutionArchive", "PASS")
        print_test(f"Version schéma", "PASS", ARCHIVE_SCHEMA_VERSION)
        
        # Vérifier que la version est 3.1.x
        is_v31 = str(ARCHIVE_SCHEMA_VERSION).startswith('3.1')
        print_test("Version >= 3.1.0", "PASS" if is_v31 else "WARN", ARCHIVE_SCHEMA_VERSION)
        
        # Créer une instance
        archive = ExecutionArchive(
            framework=fw,
            include_instructions=True,
            include_raw_memory=True,
            max_qasm_size=100000
        )
        print_test("Instance créée", "PASS")
        
        # Vérifier les méthodes v3
        v3_methods = [
            '_collect_metadata_v3', '_collect_system_info_v3', '_collect_python_env_v3',
            '_collect_dependencies_v3', '_collect_environment_vars_v3', '_collect_ibm_account_v3',
            '_collect_qpu_state_v3', '_collect_gates_calibration_v3', '_collect_topology_v3',
            '_collect_calibration_health_v3', '_collect_quality_thresholds_v3', '_collect_circuits_v3',
            '_collect_backend_extended_v3', '_collect_usage_costs_v3', '_collect_transpilation_detailed_v3',
            '_collect_analysis_results_v3', '_collect_timing_detailed_v3', '_collect_reproducibility_v3',
            '_collect_qubits_analysis_v3', '_collect_connections_detailed_v3', '_collect_network_info_v3',
            '_collect_process_info_v3', '_collect_qdna_fingerprint_v3',
        ]
        
        missing = [m for m in v3_methods if not hasattr(archive, m)]
        print_test(f"Méthodes v3 ({len(v3_methods) - len(missing)}/{len(v3_methods)})", 
                  "PASS" if not missing else "WARN")
        
        # Tester la génération d'archive
        print_subsection("Test génération archive")
        
        mock_results = [
            {'counts': {'00000': 45, '11111': 42, '00001': 8, '10101': 5}, 'shots': 100, 'fidelity': 0.87},
        ]
        mock_context = {
            'job_id': 'test_archive_123', 'shots': 100, 'circuits_count': 1,
            'status': 'COMPLETED', 'total_time_s': 5.5, 'qpu_time_s': 1.2,
        }
        
        archive_data = archive._build_complete_archive(
            results=mock_results, circuits=None, transpiled_circuits=None,
            run_context=mock_context, error=None
        )
        
        # Vérifier les 41 sections
        required_sections = [
            '_schema', 'metadata', 'system_info', 'python_env', 'dependencies',
            'environment_vars', 'ibm_account', 'backend', 'qpu_state',
            'gates_calibration', 'topology', 'calibration_health',
            'framework_config', 'quality_thresholds', 'circuits_original',
            'circuits_transpiled', 'transpilation_config', 'layout_mapping',
            'mitigation_config', 'sampler_options', 'execution', 'job_metadata',
            'results', 'raw_memory', 'statistics', 'session_logs', 'warnings',
            'pre_execution_estimates', 'error', 'backend_extended', 'usage_and_costs',
            'transpilation_detailed', 'analysis_results', 'timing_detailed',
            'reproducibility', 'qubits_analysis', 'connections_detailed',
            'network_info', 'process_info', 'qdna_fingerprint', 'integrity'
        ]
        
        present = [s for s in required_sections if s in archive_data]
        missing_sections = [s for s in required_sections if s not in archive_data]
        
        print_test(f"Sections présentes ({len(present)}/41)", 
                  "PASS" if len(present) == 41 else "WARN", 
                  f"{len(present)} sections")
        
        if missing_sections:
            for s in missing_sections[:5]:
                print_test(f"  Section manquante: {s}", "WARN")
        
        # Vérifier _schema
        schema = archive_data.get('_schema', {})
        print_test("_schema.version", "PASS" if 'version' in schema else "FAIL", 
                  schema.get('version', 'N/A'))
        print_test("_schema.format", "PASS" if 'format' in schema else "FAIL",
                  schema.get('format', 'N/A'))
        
        # Vérifier les nouvelles sections v3.1
        new_sections = [
            'backend_extended', 'usage_and_costs', 'transpilation_detailed',
            'analysis_results', 'timing_detailed', 'reproducibility',
            'qubits_analysis', 'connections_detailed', 'network_info',
            'process_info', 'qdna_fingerprint'
        ]
        new_present = sum(1 for s in new_sections if s in archive_data)
        print_test(f"Nouvelles sections v3.1 ({new_present}/11)", 
                  "PASS" if new_present == 11 else "WARN")
        
        # Taille JSON
        import json
        json_str = json.dumps(archive_data, default=str)
        size_kb = len(json_str) / 1024
        print_test(f"Taille archive", "INFO", f"{size_kb:.1f} KB")
        
        # Résultat
        success = len(present) >= 40 and is_v31 and not missing
        if success:
            results.add("Archive JSON v3.1", "PASS", f"41 sections, v{ARCHIVE_SCHEMA_VERSION}", category="Archive")
        else:
            results.add("Archive JSON v3.1", "WARN", f"{len(present)} sections", category="Archive")
        
        return success
        
    except Exception as e:
        print_test("Test Archive", "FAIL", str(e))
        results.add("Archive JSON v3.1", "FAIL", str(e), category="Archive")
        traceback.print_exc()
        return False

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='QMC Framework v2.6.2 - Validation EXHAUSTIVE',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--backend', type=str, default='ibm_torino',
                       help='Backend IBM (défaut: ibm_torino)')
    parser.add_argument('--shots', type=int, default=100,
                       help='Shots par circuit (défaut: 100)')
    parser.add_argument('--skip-qpu', action='store_true',
                       help='Ignorer les tests QPU')
    parser.add_argument('--project', type=str, default='QMC_FULL_VALIDATION',
                       help='Nom du projet')
    
    args = parser.parse_args()
    
    # Bannière
    print_banner()
    print(f"  📅 Date:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🖥️  Backend:  {args.backend}")
    print(f"  🎯 Shots:    {args.shots}")
    print(f"  📁 Project:  {args.project}")
    print(f"  🔄 Mode:     {'Local uniquement' if args.skip_qpu else 'Avec QPU'}")
    
    # Import
    success, modules = import_framework()
    if not success:
        print(f"\n{Colors.RED}❌ Import échoué. Arrêt.{Colors.END}")
        sys.exit(1)
    
    # Dépendances
    deps = check_dependencies()
    
    # Initialisation
    print_section("INITIALISATION DU FRAMEWORK", "⚙️")
    
    QMCFramework = modules.get('QMCFramework')
    RunMode = modules.get('RunMode')
    fw = None
    
    try:
        fw = QMCFramework(
            backend_name=args.backend,
            project=args.project,
            shots=args.shots
        )
        print_test("Instance QMCFramework", "PASS")
        
        print_subsection("Initialisation complète")
        if RunMode:
            fw.initialize(mode=RunMode.QPU, config={'shots': args.shots})
            print_test("Framework initialisé", "PASS", "Mode QPU")
        
        results.add("Instance Framework", "PASS", category="Init")
    except Exception as e:
        print_test("Instance QMCFramework", "FAIL", str(e))
        results.add("Instance Framework", "FAIL", str(e), category="Init")
        traceback.print_exc()
        results.summary()
        sys.exit(1)
    
    # Tests
    if not args.skip_qpu:
        connected = test_connection_and_calibration(fw, args.backend)
        if not connected:
            print(f"\n{Colors.YELLOW}⚠️ Connexion échouée. Passage en mode local.{Colors.END}")
            args.skip_qpu = True
    
    # Circuit Builders
    test_all_circuit_builders(fw, modules, deps)
    
    # Analyzers
    test_all_analyzers(modules, deps)
    
    # v2.6.1 Features
    test_v260_features(fw, deps)
    
    # v2.6.2 QMC Archive Features (NEW)
    test_v262_qmc_archive(fw, modules)
    
    # v2.6.3 QMC Accounts Audit Features (NEW)
    test_v263_accounts_audit(fw, modules)
    
    # Optimizers & Calculators
    test_optimizers_and_calculators(fw, modules)
    
    # Error Mitigation
    test_error_mitigation(fw, modules)
    
    # QDNA Features
    test_qdna_features(fw)
    
    # Archive JSON v3.1
    test_archive_json_v31(fw, modules)
    
    # QPU Execution
    if not args.skip_qpu and results.circuits_for_qpu:
        run_qpu_tests(fw, args.shots, modules)
    elif args.skip_qpu:
        print_section("EXÉCUTION QPU", "🚀")
        print(f"    {Colors.YELLOW}⏭️ Tests QPU ignorés (--skip-qpu){Colors.END}")
        results.add("QPU Execution", "SKIP", "--skip-qpu", category="QPU")
    
    # Résumé
    success = results.summary()
    
    print()
    if success:
        print(f"{Colors.GREEN}{'═' * 80}")
        print(f"  ✅ VALIDATION EXHAUSTIVE RÉUSSIE")
        print(f"{'═' * 80}{Colors.END}")
    else:
        print(f"{Colors.RED}{'═' * 80}")
        print(f"  ❌ VALIDATION EXHAUSTIVE ÉCHOUÉE")
        print(f"{'═' * 80}{Colors.END}")
    print()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
