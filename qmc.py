"""
[v2.7.2] Shim d'import STABLE — `from qmc import QMCFramework`.

But : découpler le code utilisateur du nom de module versionné. Le framework reste
un SEUL fichier (`qmc_quantum_framework_v2_7_2.py`) ; ce shim n'est qu'une ré-export
de 3 lignes. À chaque montée de version, seule la ligne d'import ci-dessous change
(ex. `_v2_7_2` -> `_v2_7_3`), sans casser les scripts utilisateurs.

    from qmc import QMCFramework            # au lieu de qmc_quantum_framework_v2_7_2
    fw = QMCFramework(...)

NB : l'import du framework est PUR et rapide (~0.1 s ; qiskit_ibm_runtime est chargé
paresseusement au premier usage QPU).
"""
from qmc_quantum_framework_v2_7_2 import *          # noqa: F401,F403  (API publique via __all__)
from qmc_quantum_framework_v2_7_2 import __all__, __version__  # noqa: F401

# Réexporte explicitement l'API publique (utile pour les éditeurs/typage).
__all__ = list(__all__)
