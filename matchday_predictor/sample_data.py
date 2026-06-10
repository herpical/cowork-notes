"""Beispielhafter erster Spieltag.

Die Werte sind illustrativ (frei gewählt, 0–100) und sollen zeigen, wie sich
ein starker Trainerstab und ein eingespieltes Team in der Vorhersage
niederschlagen. Für den echten Einsatz ersetzt man sie durch eigene
Einschätzungen oder lädt sie aus einer JSON-Datei (siehe ``cli.py``).
"""

from __future__ import annotations

from .models import CoachingStaff, Team, TeamChemistry


def _team(
    name: str,
    *,
    coach: tuple[float, float, float, float],
    chem: tuple[float, float, float, float],
    squad: float,
) -> Team:
    return Team(
        name=name,
        staff=CoachingStaff(
            name=f"Stab {name}",
            head_coach=coach[0],
            assistants=coach[1],
            tactical_experience=coach[2],
            continuity=coach[3],
        ),
        chemistry=TeamChemistry(
            squad_continuity=chem[0],
            minutes_together=chem[1],
            new_signings_integration=chem[2],
            preseason_quality=chem[3],
        ),
        squad_quality=squad,
    )


# Frei erfundene Teams, bewusst mit unterschiedlichen Profilen:
# - "Eintracht Beispielstadt": Top-Stab, sehr eingespielt
# - "FC Neuaufbau":            teurer Kader, aber neuer Stab & viele Neuzugänge
TEAMS: dict[str, Team] = {
    "Eintracht Beispielstadt": _team(
        "Eintracht Beispielstadt",
        coach=(88, 82, 85, 90),
        chem=(85, 88, 78, 82),
        squad=80,
    ),
    "FC Neuaufbau": _team(
        "FC Neuaufbau",
        coach=(72, 65, 60, 40),
        chem=(45, 40, 55, 60),
        squad=86,
    ),
    "SV Konstanz": _team(
        "SV Konstanz",
        coach=(78, 75, 80, 85),
        chem=(80, 82, 70, 75),
        squad=72,
    ),
    "TSV Umbruch": _team(
        "TSV Umbruch",
        coach=(70, 68, 62, 55),
        chem=(58, 55, 60, 65),
        squad=70,
    ),
    "1. FC Routine": _team(
        "1. FC Routine",
        coach=(82, 78, 84, 88),
        chem=(88, 90, 72, 80),
        squad=74,
    ),
    "Sportclub Talent": _team(
        "Sportclub Talent",
        coach=(74, 70, 58, 50),
        chem=(52, 48, 58, 70),
        squad=78,
    ),
}


def sample_matchday() -> list[tuple[Team, Team]]:
    """Liefert die Begegnungen des Beispiel-Spieltags (Heim, Auswärts)."""
    t = TEAMS
    return [
        (t["Eintracht Beispielstadt"], t["FC Neuaufbau"]),
        (t["SV Konstanz"], t["TSV Umbruch"]),
        (t["1. FC Routine"], t["Sportclub Talent"]),
    ]
