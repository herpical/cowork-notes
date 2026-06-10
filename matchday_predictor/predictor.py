"""Vorhersage-Engine für den ersten Spieltag.

Ablauf:

1. Aus jedem Team wird eine **Stärke** (0–100) berechnet, gewichtet aus
   Trainerstab, Eingespieltheit und Kader-Grundlinie.
2. Die Stärkedifferenz (plus Heimvorteil) wird in eine erwartete
   Tordifferenz ("Supremacy") übersetzt.
3. Über zwei Poisson-Verteilungen ergeben sich Sieg-/Remis-/Niederlage-
   Wahrscheinlichkeiten und das wahrscheinlichste Ergebnis.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .models import Team, clamp


@dataclass(frozen=True)
class ModelWeights:
    """Gewichtung der drei Stärkebausteine.

    Standardmäßig dominieren – wie gefordert – Trainerstab und
    Eingespieltheit mit je 40 %; die Kaderqualität bildet mit 20 % nur die
    Grundlinie, da sie am ersten Spieltag weniger aussagekräftig ist.
    """

    coaching: float = 0.40
    cohesion: float = 0.40
    squad: float = 0.20

    def normalised(self) -> "ModelWeights":
        total = self.coaching + self.cohesion + self.squad
        if total <= 0:
            raise ValueError("Die Summe der Gewichte muss positiv sein.")
        return ModelWeights(
            coaching=self.coaching / total,
            cohesion=self.cohesion / total,
            squad=self.squad / total,
        )


@dataclass
class Prediction:
    """Ergebnis einer Begegnung inkl. Begründung."""

    home: str
    away: str
    home_strength: float
    away_strength: float
    expected_goals_home: float
    expected_goals_away: float
    prob_home_win: float
    prob_draw: float
    prob_away_win: float
    most_likely_score: tuple[int, int]
    contributions: dict[str, dict[str, float]] = field(default_factory=dict)

    @property
    def outcome(self) -> str:
        """Wahrscheinlichstes Ergebnis als Klartext."""
        best = max(
            (self.prob_home_win, f"Heimsieg {self.home}"),
            (self.prob_draw, "Unentschieden"),
            (self.prob_away_win, f"Auswärtssieg {self.away}"),
            key=lambda item: item[0],
        )
        return best[1]

    def summary(self) -> str:
        """Mehrzeilige, menschenlesbare Zusammenfassung."""
        s_home, s_away = self.most_likely_score
        lines = [
            f"{self.home} vs. {self.away}",
            f"  Stärke:        {self.home_strength:5.1f}  :  {self.away_strength:5.1f}",
            f"  Erw. Tore:     {self.expected_goals_home:5.2f}  :  {self.expected_goals_away:5.2f}",
            f"  Wahrsch.:      Heim {self.prob_home_win:5.1%} | "
            f"Remis {self.prob_draw:5.1%} | Ausw. {self.prob_away_win:5.1%}",
            f"  Tipp:          {self.outcome}  ({s_home}:{s_away})",
        ]
        return "\n".join(lines)


class MatchdayPredictor:
    """Berechnet Vorhersagen für Begegnungen des ersten Spieltags."""

    def __init__(
        self,
        weights: ModelWeights | None = None,
        *,
        home_advantage: float = 5.0,
        league_avg_total_goals: float = 2.9,
        strength_points_per_goal: float = 15.0,
        max_goals: int = 8,
    ) -> None:
        """
        Args:
            weights: Gewichtung der Stärkebausteine.
            home_advantage: Heimbonus in Stärkepunkten.
            league_avg_total_goals: Erwartete Tore pro Spiel (beide Teams).
            strength_points_per_goal: Wie viele Stärkepunkte einem
                erwarteten Tor Vorsprung entsprechen.
            max_goals: Obergrenze der Tor-Verteilung für die Berechnung.
        """
        self.weights = (weights or ModelWeights()).normalised()
        self.home_advantage = home_advantage
        self.league_avg_total_goals = league_avg_total_goals
        self.strength_points_per_goal = strength_points_per_goal
        self.max_goals = max_goals

    # -- Stärke -----------------------------------------------------------

    def team_strength(self, team: Team) -> float:
        """Gewichtete Gesamtstärke eines Teams (0–100)."""
        w = self.weights
        return clamp(
            team.coaching_quality * w.coaching
            + team.cohesion * w.cohesion
            + team.squad_quality * w.squad
        )

    def _contributions(self, team: Team) -> dict[str, float]:
        """Beitrag jedes Bausteins zur Stärke – für die Begründung."""
        w = self.weights
        return {
            "Trainerstab": team.coaching_quality * w.coaching,
            "Eingespieltheit": team.cohesion * w.cohesion,
            "Kaderqualität": team.squad_quality * w.squad,
        }

    # -- Vorhersage -------------------------------------------------------

    def predict(self, home: Team, away: Team) -> Prediction:
        """Berechnet die Vorhersage für ``home`` (Heim) gegen ``away``."""
        s_home = self.team_strength(home)
        s_away = self.team_strength(away)

        diff = (s_home + self.home_advantage) - s_away
        supremacy = diff / self.strength_points_per_goal

        total = self.league_avg_total_goals
        lambda_home = max(0.15, (total + supremacy) / 2)
        lambda_away = max(0.15, (total - supremacy) / 2)

        p_home, p_draw, p_away, score = self._poisson_outcomes(
            lambda_home, lambda_away
        )

        return Prediction(
            home=home.name,
            away=away.name,
            home_strength=s_home,
            away_strength=s_away,
            expected_goals_home=lambda_home,
            expected_goals_away=lambda_away,
            prob_home_win=p_home,
            prob_draw=p_draw,
            prob_away_win=p_away,
            most_likely_score=score,
            contributions={
                home.name: self._contributions(home),
                away.name: self._contributions(away),
            },
        )

    def predict_matchday(
        self, fixtures: list[tuple[Team, Team]]
    ) -> list[Prediction]:
        """Vorhersagen für eine ganze Liste von Begegnungen."""
        return [self.predict(home, away) for home, away in fixtures]

    # -- Poisson-Hilfsfunktionen -----------------------------------------

    @staticmethod
    def _poisson_pmf(k: int, lam: float) -> float:
        return math.exp(-lam) * lam ** k / math.factorial(k)

    def _poisson_outcomes(
        self, lambda_home: float, lambda_away: float
    ) -> tuple[float, float, float, tuple[int, int]]:
        """Sieg-/Remis-/Niederlage-Wahrscheinlichkeiten und Top-Ergebnis."""
        home_pmf = [self._poisson_pmf(i, lambda_home) for i in range(self.max_goals + 1)]
        away_pmf = [self._poisson_pmf(j, lambda_away) for j in range(self.max_goals + 1)]

        p_home = p_draw = p_away = 0.0
        best_prob = -1.0
        best_score = (0, 0)

        for i, ph in enumerate(home_pmf):
            for j, pa in enumerate(away_pmf):
                joint = ph * pa
                if i > j:
                    p_home += joint
                elif i == j:
                    p_draw += joint
                else:
                    p_away += joint
                if joint > best_prob:
                    best_prob = joint
                    best_score = (i, j)

        # Restmasse jenseits von max_goals proportional verteilen,
        # damit sich die Wahrscheinlichkeiten zu 1 summieren.
        total = p_home + p_draw + p_away
        if total > 0:
            p_home, p_draw, p_away = p_home / total, p_draw / total, p_away / total

        return p_home, p_draw, p_away, best_score
