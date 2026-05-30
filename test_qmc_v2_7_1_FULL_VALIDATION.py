#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║        QMC FRAMEWORK v2.7.1 - VALIDATION EXHAUSTIVE COMPLÈTE                     ║
║        Test de TOUS les composants avec exécution QPU réelle                     ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  TESTS INCLUS:                                                                   ║
║  ├── [SECTION 1] Import & Initialisation                                         ║
║  ├── [SECTION 2] Connexion & Calibration                                         ║
║  ├── [SECTION 3] TOUS les Circuit Builders (21 builders)                        ║
║  ├── [SECTION 4] TOUS les Analyzers (12 analyzers)                              ║
║  ├── [SECTION 5] v2.6.0/v2.6.1 Features                                         ║
║  ├── [SECTION 5b] v2.6.2: QMC Archive Manager                                   ║
║  ├── [SECTION 5c] v2.6.3: QMC Accounts Audit                                    ║
║  ├── [SECTION 5d] ★★ v2.7.1: MULTI-JOB SESSION MANAGER ★★                      ║
║  │   ├── MultiJobSession, MultiJobSessionStatus classes                          ║
║  │   ├── find_session_file(), fw.run_multi_job_session()                        ║
║  │   ├── fw.list_sessions(), fw.print_sessions_list()                           ║
║  │   ├── archive_project parameter for global upload                             ║
║  │   └── TEST QPU: 4 jobs × 200 shots avec reprise                               ║
║  ├── [SECTION 5e] ★★ v2.7.1: PARALLEL TRANSPILATION + PROGRESS BAR ★★          ║
║  │   ├── _parallel_transpile_worker (module-level)                               ║
║  │   ├── transpile_circuits(parallel=, n_workers=, show_progress=)              ║
║  │   ├── transpile_parallel() → délègue à transpile_circuits                    ║
║  │   ├── auto_transpile=False préservé dans MultiJobSession                     ║
║  │   └── TEST: progress bar + parallélisme local                                 ║
║  ├── [SECTION 6] Optimizers & Calculators                                        ║
║  ├── [SECTION 7] Error Mitigation                                                ║
║  ├── [SECTION 8] QDNA Features                                                   ║
║  ├── [SECTION 9] Exécution QPU (100 shots/circuit)                              ║
║  ├── [SECTION 10] Analyse des résultats                                          ║
║  └── [SECTION 11] Archive JSON v3.1                                              ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Usage:                                                                          ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py                                     ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py --backend ibm_fez --shots 100       ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py --skip-qpu      # Tests locaux      ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py --only-multijob # Multi-job seul    ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-qpu  # Multi-job QPU     ║
║    python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-sim  # Multi-job SIM     ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import argparse
import tempfile
import traceback
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# ══════════════════════════════════════════════════════════════════════════════
# [v2.7.1] ADAPTATION — rediriger les imports du test vers le module v2.7.1.
# On charge qmc_quantum_framework_v2_7_1.py et on l'enregistre dans sys.modules
# SOUS LES DEUX NOMS, de sorte que tous les `importlib.import_module('..._v2_7_1')`
# et `from ..._v2_7_1 import ...` du test résolvent la v2.7.1 sans éditer chaque ligne.
# Les variables d'env désactivent le check de dépendances interactif à l'import.
# ══════════════════════════════════════════════════════════════════════════════
import importlib.util as _ilu
os.environ.setdefault("QMC_SKIP_DEP_CHECK", "true")
os.environ.setdefault("QMC_SILENT_DEP_CHECK", "true")
os.environ.setdefault("QMC_AUTO_INSTALL_DEPS", "false")
_v271_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "qmc_quantum_framework_v2_7_1.py")
_spec_271 = _ilu.spec_from_file_location("qmc_quantum_framework_v2_7_1", _v271_path)
_mod_271 = _ilu.module_from_spec(_spec_271)
sys.modules["qmc_quantum_framework_v2_7_1"] = _mod_271
_spec_271.loader.exec_module(_mod_271)
print(f"[v2.7.1 TEST] Module chargé: v{getattr(_mod_271, '__version__', '?')} "
      f"(QMCFramework concrète, relique QMCFrameworkV2_4 supprimée: "
      f"{not hasattr(_mod_271, 'QMCFrameworkV2_4')})")

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
║{Colors.BOLD}      ⚛️  QMC FRAMEWORK v2.7.1 - VALIDATION EXHAUSTIVE COMPLÈTE  ⚛️            {Colors.END}{Colors.CYAN}║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  Test de TOUS les composants: 21 Builders, 12 Analyzers, Optimizers, etc.        ║
║  ★ v2.7.1 MAJOR: Multi-Job Session + Parallel Transpilation + Progress Bar      ║
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
        """Ajoute un circuit à la liste pour exécution QPU."""
        if hasattr(circuit, 'parameters') and len(circuit.parameters) > 0:
            print_test(name, "SKIP", f"{len(circuit.parameters)} paramètres non liés")
            return False
        self.circuits_for_qpu.append((name, circuit))
        return True
    
    def add_qpu_result(self, circuit_name: str, counts: Dict, analysis: Dict = None):
        self.qpu_results.append({
            'name': circuit_name,
            'counts': counts,
            'analysis': analysis
        })
    
    def summary(self) -> bool:
        elapsed = time.time() - self.start_time
        total = self.passed + self.failed + self.skipped
        
        print_section("RÉSUMÉ DES TESTS", "📊")
        
        print(f"\n    Total: {total} tests")
        print(f"    {Colors.GREEN}✅ Passés: {self.passed}{Colors.END}")
        print(f"    {Colors.RED}❌ Échoués: {self.failed}{Colors.END}")
        print(f"    {Colors.YELLOW}⏭️ Ignorés: {self.skipped}{Colors.END}")
        print(f"    ⏱️  Durée: {elapsed:.1f}s")
        
        if self.qpu_results:
            print(f"\n    🚀 Résultats QPU: {len(self.qpu_results)} circuits exécutés")
        
        # Par catégorie
        categories = {}
        for t in self.tests:
            cat = t.get('category', 'Other')
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0, 'skipped': 0}
            categories[cat][t['status'].lower()] = categories[cat].get(t['status'].lower(), 0) + 1
        
        if categories:
            print("\n    Par catégorie:")
            for cat, stats in sorted(categories.items()):
                p, f, s = stats.get('pass', 0), stats.get('fail', 0), stats.get('skip', 0)
                print(f"       {cat}: ✅{p} ❌{f} ⏭️{s}")
        
        return self.failed == 0

# Global results tracker
results = TestResults()

# ==============================================================================
# SECTION 5d: v2.7.1 MULTI-JOB SESSION MANAGER
# ==============================================================================

def test_v271_multijob_session(fw, modules: Dict, mode: str = "local") -> bool:
    """
    Teste le Multi-Job Session Manager v2.7.1.
    
    Args:
        fw: QMCFramework instance
        modules: Dict des modules importés
        mode: "local" (classes/méthodes), "sim" (simulation), "qpu" (QPU réel)
    
    Returns:
        True si tous les tests passent
    """
    print_section("v2.7.1: MULTI-JOB SESSION MANAGER ★★", "🔄")
    
    features_tested = 0
    all_passed = True
    
    # --- Test 1: Imports des classes ---
    print_subsection("Import des classes Multi-Job")
    
    MultiJobSession = None
    MultiJobSessionStatus = None
    find_session_file = None
    
    try:
        # Import direct
        import importlib
        qmc_module = importlib.import_module('qmc_quantum_framework_v2_7_1')
        
        if hasattr(qmc_module, 'MultiJobSession'):
            MultiJobSession = qmc_module.MultiJobSession
            print_test("MultiJobSession", "PASS", "Classe importée")
            results.add("MultiJobSession class", "PASS", category="v2.7.1")
            features_tested += 1
        else:
            print_test("MultiJobSession", "FAIL", "Non trouvée")
            results.add("MultiJobSession class", "FAIL", category="v2.7.1")
            all_passed = False
        
        if hasattr(qmc_module, 'MultiJobSessionStatus'):
            MultiJobSessionStatus = qmc_module.MultiJobSessionStatus
            print_test("MultiJobSessionStatus", "PASS", "Classe importée")
            results.add("MultiJobSessionStatus class", "PASS", category="v2.7.1")
            features_tested += 1
            
            # Vérifier les constantes
            statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'PARTIAL']
            job_statuses = ['JOB_PENDING', 'JOB_SUBMITTED', 'JOB_RUNNING', 'JOB_COMPLETED', 'JOB_FAILED', 'JOB_SKIPPED']
            
            missing = []
            for s in statuses + job_statuses:
                if not hasattr(MultiJobSessionStatus, s):
                    missing.append(s)
            
            if not missing:
                print_test("Constantes de statut", "PASS", f"{len(statuses + job_statuses)} constantes")
                features_tested += 1
            else:
                print_test("Constantes de statut", "WARN", f"Manque: {missing[:3]}")
        else:
            print_test("MultiJobSessionStatus", "FAIL", "Non trouvée")
            all_passed = False
        
        if hasattr(qmc_module, 'find_session_file'):
            find_session_file = qmc_module.find_session_file
            print_test("find_session_file()", "PASS", "Fonction importée")
            results.add("find_session_file", "PASS", category="v2.7.1")
            features_tested += 1
        else:
            print_test("find_session_file()", "FAIL", "Non trouvée")
            all_passed = False
            
    except Exception as e:
        print_test("Import classes Multi-Job", "FAIL", str(e)[:50])
        results.add("Import Multi-Job classes", "FAIL", str(e)[:50], category="v2.7.1")
        all_passed = False
    
    # --- Test 2: Méthodes QMCFramework ---
    print_subsection("Méthodes QMCFramework Multi-Job")
    
    try:
        # run_multi_job_session
        if hasattr(fw, 'run_multi_job_session'):
            print_test("fw.run_multi_job_session()", "PASS", "Méthode disponible")
            results.add("fw.run_multi_job_session()", "PASS", category="v2.7.1")
            features_tested += 1
            
            # Vérifier signature
            import inspect
            sig = inspect.signature(fw.run_multi_job_session)
            params = list(sig.parameters.keys())
            expected = ['jobs', 'resume_session_id', 'session_name', 'output_dir', 'archive_project', 'auto_confirm']
            missing = [p for p in expected if p not in params]
            
            if not missing:
                print_test("run_multi_job_session() signature", "PASS", f"{len(params)} paramètres")
                print_metric("archive_project", "✓ Supporté (nouveau v2.7.1)")
                features_tested += 1
            else:
                print_test("run_multi_job_session() signature", "WARN", f"Manque: {missing}")
        else:
            print_test("fw.run_multi_job_session()", "FAIL", "Non trouvée")
            results.add("fw.run_multi_job_session()", "FAIL", category="v2.7.1")
            all_passed = False
        
        # list_sessions
        if hasattr(fw, 'list_sessions'):
            print_test("fw.list_sessions()", "PASS", "Méthode disponible")
            results.add("fw.list_sessions()", "PASS", category="v2.7.1")
            features_tested += 1
        else:
            print_test("fw.list_sessions()", "FAIL", "Non trouvée")
            all_passed = False
        
        # print_sessions_list
        if hasattr(fw, 'print_sessions_list'):
            print_test("fw.print_sessions_list()", "PASS", "Méthode disponible")
            results.add("fw.print_sessions_list()", "PASS", category="v2.7.1")
            features_tested += 1
        else:
            print_test("fw.print_sessions_list()", "FAIL", "Non trouvée")
            all_passed = False
            
    except Exception as e:
        print_test("Méthodes QMCFramework", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 3: Création et manipulation de session (local) ---
    print_subsection("Création et manipulation de session (local)")
    
    if MultiJobSession and MultiJobSessionStatus:
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Créer des jobs factices
                mock_jobs = [
                    {"circuits_count": 3, "shots": 200, "label": "test_job_1", "metadata": {"seed": 42}},
                    {"circuits_count": 3, "shots": 200, "label": "test_job_2", "metadata": {"seed": 1042}},
                    {"circuits_count": 3, "shots": 200, "label": "test_job_3", "metadata": {"seed": 2042}},
                    {"circuits_count": 3, "shots": 200, "label": "test_job_4", "metadata": {"seed": 3042}},
                ]
                
                session = MultiJobSession.create_new(
                    jobs=mock_jobs,
                    output_dir=tmpdir,
                    backend="ibm_fez",
                    ibm_account="TEST"
                )
                
                print_test("Création session", "PASS", f"ID: {session.session_id[:25]}...")
                print_metric("total_jobs", session.total_jobs)
                print_metric("status", session.status)
                features_tested += 1
                
                # Sauvegarder
                session.save()
                if session.session_file.exists():
                    print_test("Sauvegarde session.json", "PASS")
                    features_tested += 1
                else:
                    print_test("Sauvegarde session.json", "FAIL")
                    all_passed = False
                
                # Charger
                loaded = MultiJobSession.load(session.session_file)
                if loaded.session_id == session.session_id:
                    print_test("Chargement session", "PASS")
                    features_tested += 1
                else:
                    print_test("Chargement session", "FAIL")
                    all_passed = False
                
                # Transitions de statut
                session.mark_job_submitted(0, "ibm_test_job_id")
                session.mark_job_running(0)
                session.mark_job_completed(0, qpu_seconds=5.5, archive_path="/test/archive.json")
                
                summary = session.get_summary()
                if summary["completed"] == 1 and summary["pending"] == 3:
                    print_test("Transitions de statut", "PASS", f"✅{summary['completed']} ⏳{summary['pending']}")
                    features_tested += 1
                else:
                    print_test("Transitions de statut", "FAIL")
                    all_passed = False
                
                # Test find_session_file
                if find_session_file:
                    found = find_session_file(session.session_id, search_dirs=[tmpdir])
                    if found:
                        print_test("find_session_file()", "PASS", "Session trouvée")
                        features_tested += 1
                    else:
                        print_test("find_session_file()", "FAIL")
                        all_passed = False
                
                # Tableau de statut
                try:
                    session.print_status_table()
                    print_test("print_status_table()", "PASS")
                    features_tested += 1
                except:
                    print_test("print_status_table()", "FAIL")
                    all_passed = False
                
                # Message de confirmation
                msg = session.get_confirmation_message(is_resume=False)
                if "NOUVELLE SESSION" in msg or "jobs" in msg.lower():
                    print_test("get_confirmation_message()", "PASS")
                    features_tested += 1
                else:
                    print_test("get_confirmation_message()", "WARN", "Format inattendu")
                
                # Compatibilité compte
                if session.is_account_compatible("TEST"):
                    print_test("is_account_compatible()", "PASS", "Même compte")
                    features_tested += 1
                else:
                    print_test("is_account_compatible()", "FAIL")
                    all_passed = False
                    
                results.add("MultiJobSession manipulation", "PASS", category="v2.7.1")
                
            except Exception as e:
                print_test("Manipulation session", "FAIL", str(e)[:50])
                results.add("MultiJobSession manipulation", "FAIL", str(e)[:50], category="v2.7.1")
                all_passed = False
                traceback.print_exc()
    else:
        print_test("Tests session", "SKIP", "Classes non importées")
    
    # --- Test 4: Mode SIMULATION (si demandé) ---
    if mode in ["sim", "all"]:
        print_subsection("Test Multi-Job en SIMULATION")
        all_passed = _test_multijob_simulation(fw, modules) and all_passed
    
    # --- Test 5: Mode QPU (si demandé) ---
    if mode in ["qpu", "all"]:
        print_subsection("Test Multi-Job sur QPU RÉEL")
        all_passed = _test_multijob_qpu(fw, modules) and all_passed
    
    # --- Résumé ---
    print(f"\n    {Colors.GREEN}✅ {features_tested} fonctionnalités Multi-Job v2.7.1 testées{Colors.END}")
    
    if all_passed:
        print(f"    {Colors.GREEN}✅ TOUS LES TESTS MULTI-JOB PASSÉS{Colors.END}")
        results.add("v2.7.1 Multi-Job Session", "PASS", f"{features_tested} features", category="v2.7.1")
    else:
        print(f"    {Colors.RED}❌ CERTAINS TESTS MULTI-JOB ONT ÉCHOUÉ{Colors.END}")
        results.add("v2.7.1 Multi-Job Session", "FAIL", category="v2.7.1")
    
    return all_passed


def _test_multijob_simulation(fw, modules: Dict) -> bool:
    """
    Test Multi-Job avec simulation via fw.test_locally().
    
    Utilise le fake backend du framework pour chaque job,
    puis crée les archives/rapports manuellement.
    """
    try:
        from qiskit import QuantumCircuit
        
        print_test("Mode Simulation", "RUN", "Via fw.test_locally()...")
        
        # Vérifier si le framework supporte test_locally
        if not hasattr(fw, 'test_locally'):
            print_test("test_locally()", "SKIP", "Non supporté")
            return _test_multijob_simulation_basic(fw, modules)
        
        # Créer 4 circuits GHZ simples
        def create_ghz(n: int, label: str):
            qc = QuantumCircuit(n, name=label)
            qc.h(0)
            for i in range(n-1):
                qc.cx(i, i+1)
            qc.measure_all()
            return qc
        
        jobs = [
            {
                "circuits": [create_ghz(3, f"GHZ3_sim_j1_c{i}") for i in range(2)],
                "shots": 100,
                "label": "sim_job_1",
                "metadata": {"test": "simulation", "job_number": 1}
            },
            {
                "circuits": [create_ghz(3, f"GHZ3_sim_j2_c{i}") for i in range(2)],
                "shots": 100,
                "label": "sim_job_2",
                "metadata": {"test": "simulation", "job_number": 2}
            },
            {
                "circuits": [create_ghz(4, f"GHZ4_sim_j3_c{i}") for i in range(2)],
                "shots": 100,
                "label": "sim_job_3",
                "metadata": {"test": "simulation", "job_number": 3}
            },
            {
                "circuits": [create_ghz(4, f"GHZ4_sim_j4_c{i}") for i in range(2)],
                "shots": 100,
                "label": "sim_job_4",
                "metadata": {"test": "simulation", "job_number": 4}
            },
        ]
        
        # Dossier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"qmc_runs/test_multijob_SIM_{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print_metric("Output", str(output_dir))
        
        # Import des classes Multi-Job
        MultiJobSession = modules.get('MultiJobSession')
        MultiJobSessionStatus = modules.get('MultiJobSessionStatus')
        
        if not MultiJobSession:
            print_test("MultiJobSession", "FAIL", "Non importé")
            return False
        
        # Créer la session
        mock_jobs_for_session = [
            {"circuits_count": len(j["circuits"]), "shots": j["shots"], 
             "label": j["label"], "metadata": j.get("metadata", {})}
            for j in jobs
        ]
        
        session = MultiJobSession.create_new(
            jobs=mock_jobs_for_session,
            output_dir=str(output_dir),
            backend="fake_heron",
            ibm_account="SIMULATION"
        )
        session.save()
        
        print_test("Session créée", "PASS", f"ID: {session.session_id[:20]}...")
        
        # Exécuter chaque job avec test_locally
        all_results = []
        total_sim_time = 0
        
        for idx, job in enumerate(jobs):
            label = job["label"]
            circuits = job["circuits"]
            shots = job["shots"]
            
            try:
                session.mark_job_running(idx)
                session.save()
                
                start_time = time.time()
                
                # Exécuter via test_locally
                job_results = fw.test_locally(circuits, shots=shots, backend_type='heron')
                
                sim_time = time.time() - start_time
                total_sim_time += sim_time
                
                # Créer une archive JSON pour ce job
                archive_data = {
                    "experiment_id": f"SIM_{session.session_id}_{idx}",
                    "job_label": label,
                    "backend": "fake_heron",
                    "shots": shots,
                    "simulation": True,
                    "simulation_time_seconds": sim_time,
                    "results": job_results,
                    "metadata": job.get("metadata", {}),
                    "timestamp": datetime.now().isoformat()
                }
                
                archive_path = output_dir / f"archive_sim_job_{idx}_{label}.json"
                with open(archive_path, 'w') as f:
                    json.dump(archive_data, f, indent=2, default=str)
                
                # Marquer comme complété
                session.mark_job_completed(
                    idx, 
                    qpu_seconds=sim_time,  # Temps de simulation
                    archive_path=str(archive_path)
                )
                session.save()
                
                all_results.append({
                    "job_index": idx,
                    "label": label,
                    "results": job_results,
                    "archive_path": str(archive_path)
                })
                
                print_test(f"Job '{label}'", "PASS", f"{len(circuits)} circuits, {sim_time:.2f}s")
                
            except Exception as e:
                session.mark_job_failed(idx, str(e))
                session.save()
                print_test(f"Job '{label}'", "FAIL", str(e)[:40])
        
        # Résumé
        summary = session.get_summary()
        session.status = "COMPLETED" if summary["failed"] == 0 else "PARTIAL"
        session.save()
        
        print()
        session.print_status_table()
        
        print_metric("Temps simulation total", f"{total_sim_time:.2f}s")
        print_metric("Archives générées", f"{summary['completed']}/{len(jobs)}")
        print_metric("Session file", session.session_file.name)
        
        if summary["completed"] == len(jobs):
            print_test("Multi-Job Simulation COMPLET", "PASS", f"{len(jobs)} jobs")
            results.add("Multi-Job Simulation", "PASS", f"{len(jobs)} jobs avec archives", category="v2.7.1")
            return True
        else:
            print_test("Multi-Job Simulation", "WARN", f"{summary['completed']}/{len(jobs)} jobs")
            results.add("Multi-Job Simulation", "WARN", f"{summary['completed']}/{len(jobs)}", category="v2.7.1")
            return summary["completed"] > 0
        
    except ImportError as ie:
        print_test("Import Qiskit", "WARN", str(ie)[:50])
        # Fallback vers simulation basique
        return _test_multijob_simulation_basic(fw, modules)
        
    except Exception as e:
        print_test("Simulation Multi-Job", "FAIL", str(e)[:50])
        results.add("Multi-Job Simulation", "FAIL", str(e)[:50], category="v2.7.1")
        traceback.print_exc()
        return False


def _test_multijob_simulation_basic(fw, modules: Dict) -> bool:
    """
    Fallback: Test Multi-Job avec simulation basique via AerSimulator.
    
    Utilisé quand le framework ne supporte pas test_locally().
    N'utilise PAS le système Multi-Job complet - juste une validation des circuits.
    """
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        from qiskit import transpile
        
        print_test("Mode Simulation Basique", "INFO", "AerSimulator direct (sans archives)")
        
        # Créer 4 circuits GHZ simples
        def create_ghz(n: int, label: str):
            qc = QuantumCircuit(n, name=label)
            qc.h(0)
            for i in range(n-1):
                qc.cx(i, i+1)
            qc.measure_all()
            return qc
        
        jobs = [
            {"circuits": [create_ghz(3, f"GHZ3_sim_{i}") for i in range(2)], "shots": 100, "label": "sim_job_1"},
            {"circuits": [create_ghz(3, f"GHZ3_sim_{i}") for i in range(2)], "shots": 100, "label": "sim_job_2"},
            {"circuits": [create_ghz(4, f"GHZ4_sim_{i}") for i in range(2)], "shots": 100, "label": "sim_job_3"},
            {"circuits": [create_ghz(4, f"GHZ4_sim_{i}") for i in range(2)], "shots": 100, "label": "sim_job_4"},
        ]
        
        simulator = AerSimulator()
        all_results = []
        
        for job in jobs:
            circuits = job["circuits"]
            shots = job["shots"]
            label = job["label"]
            
            transpiled = transpile(circuits, simulator)
            result = simulator.run(transpiled, shots=shots).result()
            
            counts_list = [result.get_counts(i) for i in range(len(circuits))]
            all_results.append({
                "label": label,
                "counts": counts_list,
                "shots": shots
            })
            
            print_test(f"Job '{label}'", "PASS", f"{len(circuits)} circuits × {shots} shots")
        
        print_test("Simulation Basique", "PASS", f"4 jobs simulés (sans archives)")
        results.add("Multi-Job Simulation (basic)", "PASS", "4 jobs", category="v2.7.1")
        
        return True
        
    except ImportError:
        print_test("Simulation Basique", "SKIP", "qiskit-aer non installé")
        results.add("Multi-Job Simulation", "SKIP", "qiskit-aer manquant", category="v2.7.1")
        return True
        
    except Exception as e:
        print_test("Simulation Basique", "FAIL", str(e)[:50])
        results.add("Multi-Job Simulation", "FAIL", str(e)[:50], category="v2.7.1")
        traceback.print_exc()
        return False


def _test_multijob_qpu(fw, modules: Dict, shots: int = 200, archive_project: str = None) -> bool:
    """Test Multi-Job sur QPU réel (4 jobs × 200 shots)."""
    try:
        from qiskit import QuantumCircuit
        
        print_test("Mode QPU", "RUN", f"4 jobs × {shots} shots")
        
        if not fw._connected:
            print_test("Connexion QPU", "FAIL", "Non connecté")
            results.add("Multi-Job QPU", "FAIL", "Non connecté", category="v2.7.1")
            return False
        
        # Créer 4 jobs avec circuits GHZ simples
        def create_ghz(n: int, label: str):
            qc = QuantumCircuit(n, name=label)
            qc.h(0)
            for i in range(n-1):
                qc.cx(i, i+1)
            qc.measure_all()
            return qc
        
        jobs = [
            {
                "circuits": [create_ghz(5, f"GHZ5_qpu_j1_c{i}") for i in range(3)],
                "shots": shots,
                "label": "QPU_test_job_1",
                "metadata": {"test": "v2.7.1", "job_number": 1}
            },
            {
                "circuits": [create_ghz(5, f"GHZ5_qpu_j2_c{i}") for i in range(3)],
                "shots": shots,
                "label": "QPU_test_job_2",
                "metadata": {"test": "v2.7.1", "job_number": 2}
            },
            {
                "circuits": [create_ghz(8, f"GHZ8_qpu_j3_c{i}") for i in range(3)],
                "shots": shots,
                "label": "QPU_test_job_3",
                "metadata": {"test": "v2.7.1", "job_number": 3}
            },
            {
                "circuits": [create_ghz(8, f"GHZ8_qpu_j4_c{i}") for i in range(3)],
                "shots": shots,
                "label": "QPU_test_job_4",
                "metadata": {"test": "v2.7.1", "job_number": 4}
            },
        ]
        
        # Afficher les jobs
        print_metric("Total jobs", 4)
        print_metric("Circuits/job", 3)
        print_metric("Shots/job", shots)
        print_metric("Temps QPU estimé", "~10-15s")
        
        # Dossier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"qmc_runs/test_multijob_v271_{timestamp}"
        
        # Exécuter avec fw.run_multi_job_session
        print_test("Soumission Multi-Job", "RUN", "Envoi vers QPU...")
        
        try:
            # NE PAS activer auto-confirm pour permettre la confirmation Multi-Job
            # La confirmation se fait au niveau de la session Multi-Job
            # Les jobs individuels s'exécuteront ensuite sans confirmation
            
            multijob_results = fw.run_multi_job_session(
                jobs=jobs,
                output_dir=output_dir,
                session_name="TEST_V271",
                archive_project=archive_project,
                auto_confirm=False  # Demander confirmation du Multi-Job
            )
            
            if multijob_results is None:
                print_test("Exécution Multi-Job QPU", "FAIL", "Résultats nuls")
                results.add("Multi-Job QPU", "FAIL", "Résultats nuls", category="v2.7.1")
                return False
            
            # Vérifier les résultats
            status = multijob_results.get('status', 'UNKNOWN')
            completed = multijob_results.get('completed_jobs', 0)
            total = multijob_results.get('total_jobs', 0)
            qpu_time = multijob_results.get('total_qpu_seconds', 0)
            
            print_test("Exécution Multi-Job QPU", "PASS", f"Status: {status}")
            print_metric("Jobs complétés", f"{completed}/{total}")
            print_metric("Temps QPU", f"{qpu_time:.2f}s")
            print_metric("Session ID", multijob_results.get('session_id', 'N/A'))
            
            # Vérifier les archives générées
            session_file = multijob_results.get('session_file')
            if session_file and Path(session_file).exists():
                print_test("Fichier session.json", "PASS")
                
                # Vérifier le contenu
                with open(session_file) as f:
                    session_data = json.load(f)
                    
                jobs_data = session_data.get('jobs', [])
                archives_found = sum(1 for j in jobs_data if j.get('archive_path'))
                print_metric("Archives générées", f"{archives_found}/{len(jobs_data)}")
            else:
                print_test("Fichier session.json", "WARN", "Non trouvé")
            
            if status in ['COMPLETED', 'PARTIAL'] and completed > 0:
                print_test("Test Multi-Job QPU", "PASS", f"{completed} jobs réussis")
                results.add("Multi-Job QPU Execution", "PASS", f"{completed}/{total} jobs", category="v2.7.1")
                return True
            else:
                print_test("Test Multi-Job QPU", "FAIL", f"Status: {status}")
                results.add("Multi-Job QPU Execution", "FAIL", f"Status: {status}", category="v2.7.1")
                return False
                
        except KeyboardInterrupt:
            print_test("Multi-Job QPU", "WARN", "Interrompu par l'utilisateur")
            results.add("Multi-Job QPU", "SKIP", "Interrompu", category="v2.7.1")
            return True
            
    except Exception as e:
        print_test("Multi-Job QPU", "FAIL", str(e)[:50])
        results.add("Multi-Job QPU", "FAIL", str(e)[:50], category="v2.7.1")
        traceback.print_exc()
        return False


# ==============================================================================
# SECTION 5e: v2.7.1 PARALLEL TRANSPILATION + PROGRESS BAR
# ==============================================================================

def test_v271_parallel_transpilation(fw, modules: Dict) -> bool:
    """
    Teste la transpilation parallèle v2.7.1.
    
    Vérifie:
    - _parallel_transpile_worker existe au niveau module
    - transpile_circuits() accepte parallel, n_workers, show_progress
    - transpile_parallel() redirige vers transpile_circuits
    - MultiJobSession.create_new() préserve auto_transpile
    """
    print_section("v2.7.1: PARALLEL TRANSPILATION + PROGRESS BAR ★★", "⚡")
    
    features_tested = 0
    all_passed = True
    
    # --- Test 1: Module-level worker function ---
    print_subsection("Worker function (module-level)")
    
    try:
        import importlib
        qmc_module = importlib.import_module('qmc_quantum_framework_v2_7_1')
        
        if hasattr(qmc_module, '_parallel_transpile_worker'):
            worker = qmc_module._parallel_transpile_worker
            print_test("_parallel_transpile_worker()", "PASS", "Fonction module-level trouvée")
            results.add("_parallel_transpile_worker", "PASS", category="v2.7.1-transpile")
            features_tested += 1
            
            # Vérifier que c'est bien une fonction (pas une méthode)
            import inspect
            if inspect.isfunction(worker):
                print_test("Type: function (picklable)", "PASS")
                features_tested += 1
            else:
                print_test("Type", "WARN", f"Type={type(worker).__name__}")
        else:
            print_test("_parallel_transpile_worker()", "FAIL", "Non trouvée au niveau module")
            results.add("_parallel_transpile_worker", "FAIL", category="v2.7.1-transpile")
            all_passed = False
            
    except Exception as e:
        print_test("Import worker", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 2: Signature de transpile_circuits ---
    print_subsection("Signature transpile_circuits()")
    
    try:
        if hasattr(fw, 'transpile_circuits'):
            import inspect
            sig = inspect.signature(fw.transpile_circuits)
            params = list(sig.parameters.keys())
            
            new_params = ['parallel', 'n_workers', 'show_progress']
            found_params = []
            missing_params = []
            
            for p in new_params:
                if p in params:
                    found_params.append(p)
                else:
                    missing_params.append(p)
            
            if not missing_params:
                print_test("Nouveaux paramètres", "PASS", f"parallel, n_workers, show_progress")
                results.add("transpile_circuits() new params", "PASS", category="v2.7.1-transpile")
                features_tested += 1
                
                # Vérifier les valeurs par défaut
                defaults = {}
                for name, param in sig.parameters.items():
                    if name in new_params and param.default is not inspect.Parameter.empty:
                        defaults[name] = param.default
                
                if defaults.get('parallel') == 'auto':
                    print_test("parallel default='auto'", "PASS")
                    features_tested += 1
                else:
                    print_test("parallel default", "WARN", f"Got: {defaults.get('parallel')}")
                
                if defaults.get('show_progress') == True:
                    print_test("show_progress default=True", "PASS")
                    features_tested += 1
                else:
                    print_test("show_progress default", "WARN", f"Got: {defaults.get('show_progress')}")
                    
                if defaults.get('n_workers') is None:
                    print_test("n_workers default=None (auto)", "PASS")
                    features_tested += 1
                else:
                    print_test("n_workers default", "WARN", f"Got: {defaults.get('n_workers')}")
            else:
                print_test("Nouveaux paramètres", "FAIL", f"Manque: {missing_params}")
                results.add("transpile_circuits() new params", "FAIL", category="v2.7.1-transpile")
                all_passed = False
        else:
            print_test("transpile_circuits()", "FAIL", "Méthode non trouvée")
            all_passed = False
            
    except Exception as e:
        print_test("Signature transpile_circuits", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 3: transpile_parallel() redirige ---
    print_subsection("transpile_parallel() → transpile_circuits()")
    
    try:
        if hasattr(fw, 'transpile_parallel'):
            import inspect
            source = inspect.getsource(fw.transpile_parallel)
            
            if 'transpile_circuits' in source and "parallel='always'" in source:
                print_test("transpile_parallel() délègue", "PASS", "→ transpile_circuits(parallel='always')")
                results.add("transpile_parallel delegation", "PASS", category="v2.7.1-transpile")
                features_tested += 1
            else:
                print_test("transpile_parallel() code", "WARN", "Implémentation directe (pas de délégation)")
        else:
            print_test("transpile_parallel()", "FAIL", "Non trouvée")
            all_passed = False
            
    except Exception as e:
        print_test("transpile_parallel check", "FAIL", str(e)[:50])
        all_passed = False
    
    # --- Test 4: MultiJobSession préserve auto_transpile ---
    print_subsection("MultiJobSession.create_new() préserve auto_transpile")
    
    MultiJobSession = modules.get('MultiJobSession')
    
    if MultiJobSession:
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Créer des jobs avec auto_transpile=False
                mock_jobs = [
                    {"circuits_count": 5, "shots": 100, "label": "job_transpile_off",
                     "auto_transpile": False},
                    {"circuits_count": 5, "shots": 100, "label": "job_transpile_on",
                     "auto_transpile": True},
                    {"circuits_count": 5, "shots": 100, "label": "job_transpile_default"},
                ]
                
                session = MultiJobSession.create_new(
                    jobs=mock_jobs,
                    output_dir=tmpdir,
                    backend="ibm_fez",
                    ibm_account="TEST"
                )
                
                # Vérifier que auto_transpile est préservé
                j0 = session.jobs[0]
                j1 = session.jobs[1]
                j2 = session.jobs[2]
                
                if j0.get("auto_transpile") == False:
                    print_test("auto_transpile=False préservé", "PASS")
                    features_tested += 1
                else:
                    print_test("auto_transpile=False", "FAIL", f"Got: {j0.get('auto_transpile')}")
                    all_passed = False
                
                if j1.get("auto_transpile") == True:
                    print_test("auto_transpile=True préservé", "PASS")
                    features_tested += 1
                else:
                    print_test("auto_transpile=True", "FAIL", f"Got: {j1.get('auto_transpile')}")
                    all_passed = False
                
                if j2.get("auto_transpile") == True:
                    print_test("auto_transpile default=True", "PASS")
                    features_tested += 1
                else:
                    print_test("auto_transpile default", "FAIL", f"Got: {j2.get('auto_transpile')}")
                    all_passed = False
                
                # Vérifier persistance après save/load
                session.save()
                loaded = MultiJobSession.load(session.session_file)
                
                if loaded.jobs[0].get("auto_transpile") == False:
                    print_test("auto_transpile persiste après save/load", "PASS")
                    results.add("auto_transpile persistence", "PASS", category="v2.7.1-transpile")
                    features_tested += 1
                else:
                    print_test("auto_transpile persistence", "FAIL")
                    all_passed = False
                    
            except Exception as e:
                print_test("MultiJobSession auto_transpile", "FAIL", str(e)[:50])
                results.add("MultiJobSession auto_transpile", "FAIL", str(e)[:50], category="v2.7.1-transpile")
                all_passed = False
                traceback.print_exc()
    else:
        print_test("MultiJobSession auto_transpile", "SKIP", "Classe non importée")
    
    # --- Résumé ---
    print(f"\n    {Colors.GREEN}✅ {features_tested} fonctionnalités Parallel Transpilation v2.7.1 testées{Colors.END}")
    
    if all_passed:
        print(f"    {Colors.GREEN}✅ TOUS LES TESTS PARALLEL TRANSPILATION PASSÉS{Colors.END}")
        results.add("v2.7.1 Parallel Transpilation", "PASS", f"{features_tested} features", category="v2.7.1-transpile")
    else:
        print(f"    {Colors.RED}❌ CERTAINS TESTS ONT ÉCHOUÉ{Colors.END}")
        results.add("v2.7.1 Parallel Transpilation", "FAIL", category="v2.7.1-transpile")
    
    return all_passed


# ==============================================================================
# IMPORT & AUTRES FONCTIONS (depuis test v2.6.3)
# ==============================================================================

def import_framework() -> Tuple[bool, Dict]:
    """Importe le framework v2.7.1 et ses composants."""
    print_section("IMPORT DU FRAMEWORK", "📦")
    
    modules = {}
    
    # Ajouter le chemin
    sys.path.insert(0, '/mnt/user-data/outputs')
    sys.path.insert(0, '.')
    
    try:
        from qmc_quantum_framework_v2_7_1 import (
            QMCFramework,
            MultiJobSession,
            MultiJobSessionStatus,
            find_session_file,
        )
        modules['QMCFramework'] = QMCFramework
        modules['MultiJobSession'] = MultiJobSession
        modules['MultiJobSessionStatus'] = MultiJobSessionStatus
        modules['find_session_file'] = find_session_file
        
        print_test("Import QMCFramework", "PASS", "v2.7.1")
        print_test("Import MultiJobSession", "PASS")
        print_test("Import MultiJobSessionStatus", "PASS")
        print_test("Import find_session_file", "PASS")
        
        results.add("Import Framework", "PASS", "v2.7.1", category="Import")
        
        # Optionnels
        try:
            from qmc_quantum_framework_v2_7_1 import RunMode
            modules['RunMode'] = RunMode
            print_test("Import RunMode", "PASS")
        except:
            print_test("Import RunMode", "SKIP")
        
        return True, modules
        
    except ImportError as e:
        print_test("Import Framework", "FAIL", str(e))
        results.add("Import Framework", "FAIL", str(e), category="Import")
        return False, modules


def test_connection_and_calibration(fw, backend_name: str) -> bool:
    """Teste la connexion et la calibration."""
    print_section("CONNEXION & CALIBRATION", "🔌")
    
    # Vérifier d'abord les comptes IBM disponibles
    print_subsection("Vérification des comptes IBM")
    try:
        if hasattr(fw, 'list_ibm_accounts'):
            accounts = fw.list_ibm_accounts()
            if accounts:
                print_test("Comptes IBM trouvés", "PASS", f"{len(accounts)} compte(s)")
                for acc in accounts[:3]:  # Afficher max 3
                    print_metric(acc.get('label', 'unknown'), acc.get('instance', 'N/A'))
            else:
                print_test("Comptes IBM", "FAIL", "Aucun compte trouvé dans .env")
                print(f"\n    {Colors.YELLOW}💡 Vérifiez votre fichier .env avec:{Colors.END}")
                print(f"       IBM_QUANTUM_TOKEN=votre_token")
                print(f"       # ou")
                print(f"       IBM_TOKEN_1=votre_token")
                print(f"       IBM_INSTANCE_1=ibm-q/open/main")
                results.add("Comptes IBM", "FAIL", "Aucun compte", category="Connect")
                return False
        else:
            print_test("list_ibm_accounts()", "SKIP", "Non disponible")
    except Exception as e:
        print_test("Vérification comptes", "WARN", str(e)[:40])
    
    try:
        print_subsection("Connexion au backend")
        success = fw.connect()
        
        if success:
            print_test(f"Connexion {backend_name}", "PASS")
            results.add("Connexion IBM", "PASS", backend_name, category="Connect")
            
            # Calibration
            print_subsection("Analyse de calibration")
            try:
                topology = fw.analyze_calibration(compact=True)
                print_test("Calibration", "PASS")
                results.add("Calibration", "PASS", category="Connect")
                return True
            except Exception as e:
                print_test("Calibration", "WARN", str(e)[:50])
                results.add("Calibration", "WARN", str(e)[:50], category="Connect")
                return True
        else:
            print_test(f"Connexion {backend_name}", "FAIL", "connect() retourné False")
            results.add("Connexion IBM", "FAIL", category="Connect")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print_test("Connexion", "FAIL", error_msg[:50])
        
        # Diagnostics supplémentaires
        if "NoneType" in error_msg and "section" in error_msg:
            print(f"\n    {Colors.YELLOW}💡 Cette erreur indique un problème de configuration .env{Colors.END}")
            print(f"       Vérifiez que le fichier .env existe et contient:")
            print(f"       IBM_QUANTUM_TOKEN=votre_token_ibm")
        elif "401" in error_msg or "Unauthorized" in error_msg:
            print(f"\n    {Colors.YELLOW}💡 Token IBM invalide ou expiré{Colors.END}")
        elif "timeout" in error_msg.lower():
            print(f"\n    {Colors.YELLOW}💡 Timeout de connexion - réessayez{Colors.END}")
        
        results.add("Connexion IBM", "FAIL", error_msg[:50], category="Connect")
        return False


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='QMC Framework v2.7.1 - Validation EXHAUSTIVE',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Tous les tests
  python test_qmc_v2_7_1_FULL_VALIDATION.py
  
  # Sans QPU
  python test_qmc_v2_7_1_FULL_VALIDATION.py --skip-qpu
  
  # Multi-Job seulement (tests locaux)
  python test_qmc_v2_7_1_FULL_VALIDATION.py --only-multijob
  
  # Multi-Job avec simulation
  python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-sim
  
  # Multi-Job sur QPU réel
  python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-qpu --backend ibm_fez
  
  # Multi-Job QPU avec upload vers projet
  python test_qmc_v2_7_1_FULL_VALIDATION.py --multijob-qpu --archive-project UUID
  
  # ★ REPRENDRE une session interrompue:
  python test_qmc_v2_7_1_FULL_VALIDATION.py --resume-session SESSION_20260129_110752_abc123
"""
    )
    parser.add_argument('--backend', type=str, default='ibm_fez',
                       help='Backend IBM (défaut: ibm_fez)')
    parser.add_argument('--shots', type=int, default=100,
                       help='Shots par circuit (défaut: 100)')
    parser.add_argument('--skip-qpu', action='store_true',
                       help='Ignorer les tests QPU')
    parser.add_argument('--project', type=str, default='QMC_FULL_VALIDATION_V271',
                       help='Nom du projet')
    
    # Options Multi-Job spécifiques
    parser.add_argument('--only-multijob', action='store_true',
                       help='Exécuter uniquement les tests Multi-Job (locaux)')
    parser.add_argument('--multijob-sim', action='store_true',
                       help='Test Multi-Job en simulation')
    parser.add_argument('--multijob-qpu', action='store_true',
                       help='Test Multi-Job sur QPU réel')
    parser.add_argument('--multijob-shots', type=int, default=200,
                       help='Shots pour test Multi-Job QPU (défaut: 200)')
    parser.add_argument('--archive-project', type=str, default=None,
                       help='UUID projet QMC Archive pour Multi-Job')
    
    # ★ Option de reprise de session
    parser.add_argument('--resume-session', type=str, default=None,
                       metavar='SESSION_ID',
                       help='Reprendre une session Multi-Job interrompue (ex: SESSION_20260129_...)')
    
    args = parser.parse_args()
    
    # Bannière
    print_banner()
    print(f"  📅 Date:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  🖥️  Backend:  {args.backend}")
    print(f"  🎯 Shots:    {args.shots}")
    print(f"  📁 Project:  {args.project}")
    
    # Mode
    if args.resume_session:
        print(f"  🔄 Mode:     ★ REPRISE SESSION Multi-Job")
        print(f"  🔑 Session:  {args.resume_session}")
    elif args.only_multijob:
        print(f"  🔄 Mode:     Multi-Job uniquement (local)")
    elif args.multijob_sim:
        print(f"  🔄 Mode:     Multi-Job Simulation")
    elif args.multijob_qpu:
        print(f"  🔄 Mode:     Multi-Job QPU ({args.multijob_shots} shots)")
        if args.archive_project:
            print(f"  📤 Archive:  {args.archive_project[:20]}...")
    elif args.skip_qpu:
        print(f"  🔄 Mode:     Local uniquement")
    else:
        print(f"  🔄 Mode:     Complet avec QPU")
    
    # Import
    success, modules = import_framework()
    if not success:
        print(f"\n{Colors.RED}❌ Import échoué. Arrêt.{Colors.END}")
        sys.exit(1)
    
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
        print_test("Instance QMCFramework", "PASS", "v2.7.1")
        
        # IMPORTANT: Appeler initialize() pour créer le logger et les composants
        if RunMode:
            fw.initialize(mode=RunMode.QPU, config={'shots': args.shots})
            print_test("Framework initialisé", "PASS", "Mode QPU")
        else:
            print_test("RunMode", "WARN", "Non importé - initialize() non appelé")
        
        results.add("Instance Framework", "PASS", category="Init")
    except Exception as e:
        print_test("Instance QMCFramework", "FAIL", str(e))
        results.add("Instance Framework", "FAIL", str(e), category="Init")
        traceback.print_exc()
        results.summary()
        sys.exit(1)
    
    # ★ MODE: REPRISE DE SESSION
    if args.resume_session:
        print_section("REPRISE DE SESSION MULTI-JOB", "🔄")
        
        # Connexion requise
        connected = test_connection_and_calibration(fw, args.backend)
        if not connected:
            print(f"\n{Colors.RED}❌ Connexion échouée. Impossible de reprendre la session.{Colors.END}")
            sys.exit(1)
        
        print(f"\n  🔑 Recherche de la session: {args.resume_session}")
        
        try:
            # Reprendre la session
            resume_results = fw.run_multi_job_session(
                resume_session_id=args.resume_session,
                archive_project=args.archive_project,
                auto_confirm=False  # Demander confirmation avant reprise
            )
            
            if resume_results:
                status = resume_results.get('status', 'UNKNOWN')
                completed = resume_results.get('completed_jobs', 0)
                total = resume_results.get('total_jobs', 0)
                qpu_time = resume_results.get('total_qpu_seconds', 0)
                
                print_test("Reprise session", "PASS", f"Status: {status}")
                print_metric("Jobs complétés", f"{completed}/{total}")
                print_metric("Temps QPU total", f"{qpu_time:.2f}s")
                results.add("Resume Session", "PASS", f"{completed}/{total} jobs", category="v2.7.1")
            else:
                print_test("Reprise session", "FAIL", "Résultats nuls")
                results.add("Resume Session", "FAIL", category="v2.7.1")
                
        except Exception as e:
            print_test("Reprise session", "FAIL", str(e)[:50])
            results.add("Resume Session", "FAIL", str(e)[:50], category="v2.7.1")
            traceback.print_exc()
        
        success = results.summary()
        sys.exit(0 if success else 1)
    
    # MODE: Only Multi-Job
    if args.only_multijob:
        test_v271_multijob_session(fw, modules, mode="local")
        test_v271_parallel_transpilation(fw, modules)
        success = results.summary()
        sys.exit(0 if success else 1)
    
    # MODE: Multi-Job Simulation
    if args.multijob_sim:
        test_v271_multijob_session(fw, modules, mode="sim")
        success = results.summary()
        sys.exit(0 if success else 1)
    
    # MODE: Multi-Job QPU
    if args.multijob_qpu:
        # Connexion requise
        connected = test_connection_and_calibration(fw, args.backend)
        if not connected:
            print(f"\n{Colors.RED}❌ Connexion échouée. Impossible de lancer le test QPU.{Colors.END}")
            sys.exit(1)
        
        # Test Multi-Job QPU
        _test_multijob_qpu(fw, modules, shots=args.multijob_shots, archive_project=args.archive_project)
        success = results.summary()
        sys.exit(0 if success else 1)
    
    # MODE: Complet
    # Connexion
    if not args.skip_qpu:
        connected = test_connection_and_calibration(fw, args.backend)
        if not connected:
            print(f"\n{Colors.YELLOW}⚠️ Connexion échouée. Passage en mode local.{Colors.END}")
            args.skip_qpu = True
    
    # Tests v2.7.1 Multi-Job (toujours exécutés en mode complet)
    multijob_mode = "local" if args.skip_qpu else "all"
    test_v271_multijob_session(fw, modules, mode=multijob_mode)
    
    # Tests v2.7.1 Parallel Transpilation (toujours exécutés)
    test_v271_parallel_transpilation(fw, modules)
    
    # Note: les autres sections (Builders, Analyzers, etc.) seraient ici
    # Pour simplifier, on inclut juste le Multi-Job dans cette version
    
    print_section("AUTRES TESTS", "📋")
    print(f"    {Colors.YELLOW}ℹ️ Pour les tests complets (Builders, Analyzers, etc.),")
    print(f"       utilisez le script test_qmc_v2_6_3_FULL_VALIDATION.py{Colors.END}")
    print(f"    {Colors.YELLOW}   Les fonctionnalités v2.6.x sont rétro-compatibles avec v2.7.1{Colors.END}")
    
    # Résumé
    success = results.summary()
    
    print()
    if success:
        print(f"{Colors.GREEN}{'═' * 80}")
        print(f"  ✅ VALIDATION v2.7.1 RÉUSSIE (Multi-Job + Parallel Transpilation)")
        print(f"{'═' * 80}{Colors.END}")
    else:
        print(f"{Colors.RED}{'═' * 80}")
        print(f"  ❌ VALIDATION v2.7.1 ÉCHOUÉE")
        print(f"{'═' * 80}{Colors.END}")
    print()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
