"""Kommandozeilen-Schnittstelle für das Vorhersagesystem.

Aufrufe:

    python -m matchday_predictor              # Beispiel-Spieltag
    python -m matchday_predictor --details    # inkl. Beitrags-Aufschlüsselung
    python -m matchday_predictor --json f.json # eigene Begegnungen aus Datei
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import CoachingStaff, Team, TeamChemistry
from .predictor import MatchdayPredictor, ModelWeights, Prediction
from .sample_data import sample_matchday
from .worldcup2026 import matchday_one as worldcup_matchday_one


def _team_from_dict(data: dict) -> Team:
    coach = data["staff"]
    chem = data["chemistry"]
    return Team(
        name=data["name"],
        staff=CoachingStaff(
            name=coach.get("name", f"Stab {data['name']}"),
            head_coach=coach["head_coach"],
            assistants=coach["assistants"],
            tactical_experience=coach["tactical_experience"],
            continuity=coach["continuity"],
        ),
        chemistry=TeamChemistry(
            squad_continuity=chem["squad_continuity"],
            minutes_together=chem["minutes_together"],
            new_signings_integration=chem["new_signings_integration"],
            preseason_quality=chem["preseason_quality"],
        ),
        squad_quality=data.get("squad_quality", 70.0),
    )


def _fixtures_from_json(path: Path) -> list[tuple[Team, Team]]:
    """Lädt Begegnungen aus einer JSON-Datei.

    Erwartetes Format::

        {"fixtures": [{"home": {<team>}, "away": {<team>}}, ...]}
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    fixtures = []
    for match in payload["fixtures"]:
        fixtures.append(
            (_team_from_dict(match["home"]), _team_from_dict(match["away"]))
        )
    return fixtures


def _print_details(prediction: Prediction) -> None:
    for team, parts in prediction.contributions.items():
        breakdown = " | ".join(f"{name}: {value:4.1f}" for name, value in parts.items())
        print(f"      {team:<26} {breakdown}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Vorhersagesystem für den ersten Spieltag "
        "(Schwerpunkt: Trainerstab & Eingespieltheit).",
    )
    parser.add_argument(
        "--worldcup",
        action="store_true",
        help="1. Spieltag der WM 2026 (echte Teams, neutraler Boden).",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="JSON-Datei mit Begegnungen (Standard: Beispiel-Spieltag).",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Beiträge von Trainerstab, Eingespieltheit und Kader zeigen.",
    )
    parser.add_argument("--coaching-weight", type=float, default=0.40)
    parser.add_argument("--cohesion-weight", type=float, default=0.40)
    parser.add_argument("--squad-weight", type=float, default=0.20)
    parser.add_argument(
        "--home-advantage",
        type=float,
        default=None,
        help="Heimbonus in Stärkepunkten "
        "(Standard: 5, bei --worldcup 0 wegen neutralem Boden).",
    )
    args = parser.parse_args(argv)

    weights = ModelWeights(
        coaching=args.coaching_weight,
        cohesion=args.cohesion_weight,
        squad=args.squad_weight,
    )
    if args.home_advantage is not None:
        home_advantage = args.home_advantage
    else:
        home_advantage = 0.0 if args.worldcup else 5.0
    predictor = MatchdayPredictor(weights, home_advantage=home_advantage)

    if args.worldcup:
        fixtures = worldcup_matchday_one()
    elif args.json:
        fixtures = _fixtures_from_json(args.json)
    else:
        fixtures = sample_matchday()

    norm = predictor.weights
    title = "Vorhersage 1. Spieltag – WM 2026" if args.worldcup else "Vorhersage 1. Spieltag"
    print(title)
    print(
        f"Gewichtung: Trainerstab {norm.coaching:.0%} | "
        f"Eingespieltheit {norm.cohesion:.0%} | Kader {norm.squad:.0%}"
    )
    print("=" * 60)
    for prediction in predictor.predict_matchday(fixtures):
        print(prediction.summary())
        if args.details:
            _print_details(prediction)
        print("-" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
