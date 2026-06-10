"""Datenmodelle für Mannschaften, Trainerstab und Eingespieltheit.

Alle Einzelwerte liegen auf einer Skala von 0 bis 100. Daraus werden zwei
zusammengesetzte Kennzahlen abgeleitet:

* ``CoachingStaff.quality``  – Qualität des Trainerstabs
* ``TeamChemistry.cohesion`` – wie gut sich das Team bereits kennt
"""

from __future__ import annotations

from dataclasses import dataclass


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    """Begrenzt ``value`` auf das Intervall ``[low, high]``."""
    return max(low, min(high, value))


def _weighted(values: dict[str, float], weights: dict[str, float]) -> float:
    """Gewichteter Durchschnitt; Gewichte müssen sich nicht zu 1 summieren."""
    total_weight = sum(weights.values())
    if total_weight == 0:
        raise ValueError("Die Summe der Gewichte darf nicht 0 sein.")
    score = sum(values[key] * weights[key] for key in weights)
    return clamp(score / total_weight)


@dataclass
class CoachingStaff:
    """Qualität des Trainerstabs – Kernkriterium für den ersten Spieltag.

    Ohne Saisonform ist das Kalibre und die Stabilität der Bank eines der
    aussagekräftigsten Signale: Ein erfahrener, eingespielter Stab bringt
    eine Mannschaft deutlich besser vorbereitet in die erste Partie.
    """

    name: str
    head_coach: float           # Qualität des Cheftrainers
    assistants: float           # Qualität/Tiefe des Assistenz- und Funktionsteams
    tactical_experience: float  # Erfolgsbilanz, Erfahrung in Drucksituationen
    continuity: float           # Stabilität – gleicher Stab wie in der Vorsaison?

    # Gewichtung der Teilkriterien innerhalb des Stab-Scores.
    SUB_WEIGHTS = {
        "head_coach": 0.45,
        "assistants": 0.20,
        "tactical_experience": 0.20,
        "continuity": 0.15,
    }

    @property
    def quality(self) -> float:
        """Gesamtqualität des Trainerstabs (0–100)."""
        return _weighted(
            {
                "head_coach": self.head_coach,
                "assistants": self.assistants,
                "tactical_experience": self.tactical_experience,
                "continuity": self.continuity,
            },
            self.SUB_WEIGHTS,
        )


@dataclass
class TeamChemistry:
    """Wie gut sich die Mannschaft bereits als Team kennt (Eingespieltheit).

    Ein Kader, der lange zusammenspielt, startet schärfer in die Saison als
    eine frisch zusammengestellte Mannschaft – unabhängig vom Einzeltalent.
    Viele Neuzugänge senken die Eingespieltheit, eine gute Vorbereitung und
    ein stabiler Stamm heben sie.
    """

    squad_continuity: float           # Anteil des gehaltenen Vorsaison-Kaders
    minutes_together: float           # gemeinsame Spielminuten der Stamm-Elf
    new_signings_integration: float   # wie gut Neuzugänge integriert sind
    preseason_quality: float          # Qualität/Ergebnisse der Vorbereitung

    SUB_WEIGHTS = {
        "squad_continuity": 0.35,
        "minutes_together": 0.30,
        "new_signings_integration": 0.20,
        "preseason_quality": 0.15,
    }

    @property
    def cohesion(self) -> float:
        """Gesamteingespieltheit des Teams (0–100)."""
        return _weighted(
            {
                "squad_continuity": self.squad_continuity,
                "minutes_together": self.minutes_together,
                "new_signings_integration": self.new_signings_integration,
                "preseason_quality": self.preseason_quality,
            },
            self.SUB_WEIGHTS,
        )


@dataclass
class Team:
    """Eine Mannschaft mit den für den ersten Spieltag relevanten Faktoren."""

    name: str
    staff: CoachingStaff
    chemistry: TeamChemistry
    squad_quality: float = 70.0  # Roh-Talent als Grundlinie (zweitrangig an MD1)

    @property
    def coaching_quality(self) -> float:
        return self.staff.quality

    @property
    def cohesion(self) -> float:
        return self.chemistry.cohesion
