#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QMC ACCOUNTS AUDIT - Script Simple                        ║
║                        QMC Research Lab - v2.6.3                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Audit rapide de tous vos comptes IBM Quantum avec rapport HTML              ║
║  - Auto-détection des comptes depuis .env                                    ║
║  - Génération de rapports HTML style IBM Carbon                              ║
║  - Gestion des comptes inaccessibles (clés expirées, etc.)                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python qmc_audit_accounts.py                     # Audit standard 30 jours
    python qmc_audit_accounts.py --days 7           # Derniers 7 jours
    python qmc_audit_accounts.py --budget 15        # Budget 15 min/compte
    python qmc_audit_accounts.py --list             # Lister les comptes
    python qmc_audit_accounts.py --output reports   # Sortie dans ./reports

Configuration .env:
    IBM_API_KEY_<LABEL>=<token>
    IBM_API_KEY_ACTIVE_<LABEL>=<token>
    IBM_CRN_<LABEL>=<crn>  (optionnel)
"""

import argparse
import sys
import os
import webbrowser
from pathlib import Path
from datetime import datetime

# Désactiver les vérifications de dépendances pour import rapide
os.environ['QMC_SKIP_DEP_CHECK'] = 'true'
os.environ['QMC_SILENT_DEP_CHECK'] = 'true'


def print_banner():
    """Affiche la bannière du script."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QMC ACCOUNTS AUDIT - v2.6.3                               ║
║                    QMC Research Lab - Menton                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


def list_accounts():
    """Liste tous les comptes IBM Quantum détectés."""
    try:
        from qmc_quantum_framework_v2_6_3 import get_all_ibm_accounts_from_env
    except ImportError:
        print("❌ Framework v2.6.3 non trouvé!")
        print("   Assurez-vous que qmc_quantum_framework_v2_6_3.py est dans le répertoire courant")
        return
    
    accounts = get_all_ibm_accounts_from_env()
    
    if not accounts:
        print("❌ Aucun compte IBM Quantum détecté dans .env")
        print()
        print("   Configuration attendue dans .env:")
        print("   IBM_API_KEY_<LABEL>=<votre_token>")
        print("   IBM_API_KEY_ACTIVE_<LABEL>=<votre_token>")
        return
    
    print(f"📋 Comptes IBM Quantum détectés: {len(accounts)}")
    print("─" * 50)
    
    for label, config in sorted(accounts.items()):
        has_instance = "instance" in config
        token_preview = config.get('token', '')[:8] + '...'
        channel = config.get('channel', 'ibm_quantum_platform')
        
        print(f"  • {label.upper()}")
        print(f"      Token: {token_preview}")
        print(f"      Channel: {channel}")
        if has_instance:
            print(f"      Instance: ✅ Configurée")
        print()


def run_audit(args):
    """Lance l'audit des comptes."""
    try:
        from qmc_quantum_framework_v2_6_3 import (
            run_accounts_audit, 
            get_all_ibm_accounts_from_env
        )
    except ImportError:
        print("❌ Framework v2.6.3 non trouvé!")
        print("   Assurez-vous que qmc_quantum_framework_v2_6_3.py est dans le répertoire courant")
        sys.exit(1)
    
    # Vérifier les comptes
    accounts = get_all_ibm_accounts_from_env()
    
    if not accounts:
        print("❌ Aucun compte IBM Quantum détecté dans .env")
        print()
        print("   Configuration attendue dans .env:")
        print("   IBM_API_KEY_<LABEL>=<votre_token>")
        print("   IBM_API_KEY_ACTIVE_<LABEL>=<votre_token>")
        sys.exit(1)
    
    print(f"📊 Démarrage de l'audit...")
    print(f"   Comptes: {len(accounts)}")
    print(f"   Période: {args.days} jours")
    print(f"   Budget: {args.budget} min/compte")
    print()
    
    # Lancer l'audit
    try:
        result = run_accounts_audit(
            accounts=accounts,
            window_days=args.days,
            limit=args.limit,
            budget_minutes=args.budget,
            output_dir=args.output,
            generate_html=True,
            generate_json=args.json,
            verbose=not args.quiet
        )
        
        # Afficher le résumé des comptes inaccessibles
        inaccessible = []
        for label, acc in result.get('accounts', {}).items():
            if not acc.get('accessible', True) or acc.get('collection_status') == 'error':
                error_msg = acc.get('error_message', 'Erreur inconnue')
                inaccessible.append((label, error_msg))
        
        if inaccessible:
            print()
            print("⚠️  COMPTES INACCESSIBLES:")
            print("─" * 50)
            for label, error in inaccessible:
                print(f"   🔴 {label.upper()}: {error}")
            print()
        
        # Ouvrir le rapport HTML si demandé
        if args.open and 'html' in result.get('generated_files', {}):
            html_path = result['generated_files']['html']
            print(f"\n🌐 Ouverture du rapport dans le navigateur...")
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
        
        print()
        print("✅ Audit terminé!")
        
        if 'html' in result.get('generated_files', {}):
            print(f"   📊 Rapport HTML: {result['generated_files']['html']}")
        if 'json' in result.get('generated_files', {}):
            print(f"   📄 Données JSON: {result['generated_files']['json']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de l'audit: {e}")
        import traceback
        if args.debug:
            traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="QMC Accounts Audit - Audit rapide des comptes IBM Quantum",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python qmc_audit_accounts.py                    # Audit standard
  python qmc_audit_accounts.py --days 7           # Derniers 7 jours
  python qmc_audit_accounts.py --budget 15        # Budget 15 min/compte
  python qmc_audit_accounts.py --list             # Lister les comptes
  python qmc_audit_accounts.py --open             # Ouvrir le rapport HTML

Configuration .env requise:
  IBM_API_KEY_<LABEL>=<token>
  IBM_API_KEY_ACTIVE_<LABEL>=<token>
  IBM_CRN_<LABEL>=<crn>  (optionnel)
        """
    )
    
    # Actions
    parser.add_argument('--list', '-l', action='store_true',
                        help="Lister les comptes IBM détectés")
    
    # Paramètres d'audit
    parser.add_argument('--days', '-d', type=int, default=30,
                        help="Nombre de jours à analyser (défaut: 30)")
    parser.add_argument('--budget', '-b', type=float, default=10.0,
                        help="Budget QPU par compte en minutes (défaut: 10)")
    parser.add_argument('--limit', type=int, default=500,
                        help="Nombre max de jobs par compte (défaut: 500)")
    parser.add_argument('--output', '-o', type=str, default='qmc_audit',
                        help="Répertoire de sortie (défaut: qmc_audit)")
    
    # Options
    parser.add_argument('--json', '-j', action='store_true',
                        help="Générer aussi le fichier JSON")
    parser.add_argument('--open', action='store_true',
                        help="Ouvrir le rapport HTML dans le navigateur")
    parser.add_argument('--quiet', '-q', action='store_true',
                        help="Mode silencieux (moins de logs)")
    parser.add_argument('--debug', action='store_true',
                        help="Afficher les erreurs détaillées")
    
    args = parser.parse_args()
    
    # Afficher la bannière
    if not args.quiet:
        print_banner()
    
    # Actions
    if args.list:
        list_accounts()
    else:
        run_audit(args)


if __name__ == '__main__':
    main()
