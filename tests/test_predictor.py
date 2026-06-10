"""Tests für das Vorhersagesystem des ersten Spieltags."""

import math

import pytest

from matchday_predictor import (
    CoachingStaff,
    MatchdayPredictor,
    ModelWeights,
    Team,
    TeamChemistry,
)


def make_team(name, *, coach=70, chem=70, squad=70):
    """Erzeugt ein Team mit gleichmäßigen Werten für alle Teilkriterien."""
    return Team(
        name=name,
        staff=CoachingStaff(
            name=f"Stab {name}",
            head_coach=coach,
            assistants=coach,
            tactical_experience=coach,
            continuity=coach,
        ),
        chemistry=TeamChemistry(
            squad_continuity=chem,
            minutes_together=chem,
            new_signings_integration=chem,
            preseason_quality=chem,
        ),
        squad_quality=squad,
    )


def test_composites_average_to_inputs():
    team = make_team("X", coach=80, chem=60, squad=50)
    assert team.coaching_quality == pytest.approx(80)
    assert team.cohesion == pytest.approx(60)


def test_probabilities_sum_to_one():
    predictor = MatchdayPredictor()
    pred = predictor.predict(make_team("A"), make_team("B"))
    total = pred.prob_home_win + pred.prob_draw + pred.prob_away_win
    assert total == pytest.approx(1.0, abs=1e-9)


def test_better_coaching_increases_win_probability():
    predictor = MatchdayPredictor()
    strong = make_team("Stark", coach=95)
    weak = make_team("Schwach", coach=45)
    pred = predictor.predict(strong, weak)
    assert pred.prob_home_win > pred.prob_away_win
    assert pred.home_strength > pred.away_strength


def test_better_cohesion_increases_win_probability():
    predictor = MatchdayPredictor()
    gelled = make_team("Eingespielt", chem=95)
    new = make_team("Neu", chem=40)
    pred = predictor.predict(gelled, new)
    assert pred.prob_home_win > pred.prob_away_win


def test_home_advantage_breaks_symmetry():
    predictor = MatchdayPredictor(home_advantage=5.0)
    pred = predictor.predict(make_team("Heim"), make_team("Auswärts"))
    # Identische Teams -> Heimvorteil muss Heimsieg wahrscheinlicher machen.
    assert pred.prob_home_win > pred.prob_away_win


def test_no_home_advantage_is_symmetric():
    predictor = MatchdayPredictor(home_advantage=0.0)
    pred = predictor.predict(make_team("A"), make_team("B"))
    assert pred.prob_home_win == pytest.approx(pred.prob_away_win, abs=1e-9)
    assert pred.expected_goals_home == pytest.approx(pred.expected_goals_away)


def test_weights_are_normalised():
    predictor = MatchdayPredictor(ModelWeights(coaching=2, cohesion=2, squad=1))
    w = predictor.weights
    assert w.coaching + w.cohesion + w.squad == pytest.approx(1.0)
    assert w.coaching == pytest.approx(0.4)


def test_coaching_dominates_squad_with_default_weights():
    """Mit Standardgewichten schlägt ein Top-Stab einen reinen Talent-Vorteil."""
    predictor = MatchdayPredictor()
    # Heim: Top-Stab & top eingespielt, schwächerer Kader.
    home = make_team("Struktur", coach=92, chem=90, squad=62)
    # Auswärts: Star-Kader, aber schwacher Stab & unausgereift.
    away = make_team("Stars", coach=55, chem=45, squad=92)
    pred = predictor.predict(home, away)
    assert pred.home_strength > pred.away_strength


def test_invalid_weights_raise():
    with pytest.raises(ValueError):
        MatchdayPredictor(ModelWeights(coaching=0, cohesion=0, squad=0))


def test_most_likely_score_is_nonnegative():
    predictor = MatchdayPredictor()
    pred = predictor.predict(make_team("A", coach=90), make_team("B", coach=50))
    home_goals, away_goals = pred.most_likely_score
    assert home_goals >= 0 and away_goals >= 0
    # Stärkeres Heimteam sollte im Top-Ergebnis nicht weniger Tore erzielen.
    assert home_goals >= away_goals
