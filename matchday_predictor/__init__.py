"""Vorhersagesystem für den ersten Spieltag.

Am ersten Spieltag fehlen Form-, xG- und Tabellendaten der laufenden Saison.
Die beiden stärksten verfügbaren Signale sind daher:

1. die Qualität des Trainerstabs und
2. wie gut sich die Mannschaft bereits als Team kennt (Eingespieltheit).

Dieses Paket modelliert beide Kriterien explizit, kombiniert sie mit einer
Kader-Grundlinie und einem Heimvorteil und übersetzt das Ergebnis über ein
Poisson-Modell in Wahrscheinlichkeiten und ein erwartetes Ergebnis.
"""

from .models import CoachingStaff, TeamChemistry, Team
from .predictor import MatchdayPredictor, ModelWeights, Prediction

__all__ = [
    "CoachingStaff",
    "TeamChemistry",
    "Team",
    "MatchdayPredictor",
    "ModelWeights",
    "Prediction",
]
