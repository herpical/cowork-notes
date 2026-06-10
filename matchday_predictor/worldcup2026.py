"""Echter Datensatz: 1. Spieltag der FIFA WM 2026 (USA/Kanada/Mexiko).

Alle 48 Teams in den 12 Gruppen A–L und die Paarungen des 1. Spieltags
(Gruppenspiel 1, 11.–17. Juni 2026). Quellen für Gruppen & Paarungen:
FIFA, ESPN, Sky Sports, Yahoo Sports, Wikipedia (Stand Juni 2026).

Die Bewertungen (0–100) für Trainerstab, Eingespieltheit und Kaderqualität
sind **subjektive Experteneinschätzungen** – nachvollziehbar, aber nicht
objektiv messbar. Sie spiegeln den Stand vor Turnierbeginn wider:

* Trainerstab    – Kalibre/Erfahrung/Stabilität des Trainerteams
* Eingespieltheit – wie lange der Kern bereits zusammenspielt, Integration
                    der Neulinge, Qualität der Vorbereitung
* Kaderqualität  – Roh-Talent (Grundlinie)

Hinweis: WM-Spiele finden auf neutralem Boden statt; der Heimvorteil wird
für diesen Datensatz daher auf 0 gesetzt (siehe CLI ``--worldcup``). Die
Gastgeber-Vertrautheit von Mexiko/USA/Kanada ist über etwas höhere
Eingespieltheit/Vorbereitung berücksichtigt.
"""

from __future__ import annotations

from .models import CoachingStaff, Team, TeamChemistry


def _t(name, *, coach, chem, squad) -> Team:
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


# coach = (Cheftrainer, Assistenz, taktische Erfahrung, Kontinuität)
# chem  = (Kaderkontinuität, gem. Spielminuten, Integration Neulinge, Vorbereitung)
TEAMS: dict[str, Team] = {
    # --- Gruppe A ---
    "Mexiko": _t("Mexiko", coach=(72, 72, 80, 70), chem=(74, 76, 68, 74), squad=74),
    "Südafrika": _t("Südafrika", coach=(70, 66, 64, 80), chem=(80, 80, 70, 74), squad=64),
    "Südkorea": _t("Südkorea", coach=(68, 66, 62, 60), chem=(75, 76, 70, 72), squad=72),
    "Tschechien": _t("Tschechien", coach=(64, 62, 60, 62), chem=(70, 70, 66, 68), squad=68),
    # --- Gruppe B ---
    "Kanada": _t("Kanada", coach=(76, 74, 74, 68), chem=(72, 72, 72, 76), squad=74),
    "Bosnien-Herzegowina": _t("Bosnien-Herzegowina", coach=(60, 58, 58, 60), chem=(68, 68, 64, 64), squad=66),
    "Katar": _t("Katar", coach=(62, 62, 60, 66), chem=(86, 88, 66, 72), squad=58),
    "Schweiz": _t("Schweiz", coach=(70, 68, 68, 74), chem=(80, 82, 70, 74), squad=76),
    # --- Gruppe C ---
    "Brasilien": _t("Brasilien", coach=(92, 86, 90, 55), chem=(66, 68, 70, 74), squad=92),
    "Marokko": _t("Marokko", coach=(80, 78, 76, 82), chem=(86, 88, 76, 80), squad=80),
    "Haiti": _t("Haiti", coach=(52, 48, 46, 50), chem=(60, 58, 58, 56), squad=48),
    "Schottland": _t("Schottland", coach=(72, 70, 70, 88), chem=(86, 88, 72, 76), squad=66),
    # --- Gruppe D ---
    "USA": _t("USA", coach=(82, 80, 82, 66), chem=(70, 72, 72, 78), squad=76),
    "Paraguay": _t("Paraguay", coach=(72, 70, 72, 72), chem=(74, 74, 68, 72), squad=68),
    "Australien": _t("Australien", coach=(68, 66, 66, 72), chem=(80, 80, 70, 72), squad=64),
    "Türkei": _t("Türkei", coach=(74, 72, 72, 68), chem=(72, 72, 72, 74), squad=78),
    # --- Gruppe E ---
    "Deutschland": _t("Deutschland", coach=(82, 82, 80, 76), chem=(74, 76, 74, 78), squad=88),
    "Elfenbeinküste": _t("Elfenbeinküste", coach=(72, 70, 70, 78), chem=(82, 82, 72, 76), squad=74),
    "Ecuador": _t("Ecuador", coach=(72, 70, 68, 72), chem=(80, 80, 72, 74), squad=72),
    "Curaçao": _t("Curaçao", coach=(74, 64, 82, 50), chem=(64, 62, 62, 60), squad=50),
    # --- Gruppe F ---
    "Niederlande": _t("Niederlande", coach=(80, 78, 80, 72), chem=(78, 80, 74, 76), squad=86),
    "Japan": _t("Japan", coach=(76, 76, 72, 90), chem=(86, 88, 76, 82), squad=78),
    "Schweden": _t("Schweden", coach=(76, 74, 70, 55), chem=(70, 70, 72, 72), squad=78),
    "Tunesien": _t("Tunesien", coach=(64, 62, 62, 70), chem=(78, 78, 68, 70), squad=62),
    # --- Gruppe G ---
    "Belgien": _t("Belgien", coach=(72, 72, 74, 62), chem=(70, 72, 70, 72), squad=82),
    "Ägypten": _t("Ägypten", coach=(66, 64, 64, 66), chem=(78, 80, 70, 72), squad=70),
    "Iran": _t("Iran", coach=(66, 64, 64, 72), chem=(84, 84, 72, 74), squad=66),
    "Neuseeland": _t("Neuseeland", coach=(60, 58, 58, 68), chem=(78, 78, 66, 68), squad=52),
    # --- Gruppe H ---
    "Kap Verde": _t("Kap Verde", coach=(62, 58, 58, 66), chem=(74, 74, 66, 66), squad=56),
    "Saudi-Arabien": _t("Saudi-Arabien", coach=(74, 72, 76, 58), chem=(82, 84, 70, 72), squad=62),
    "Spanien": _t("Spanien", coach=(82, 82, 80, 80), chem=(82, 84, 78, 82), squad=92),
    "Uruguay": _t("Uruguay", coach=(86, 82, 86, 72), chem=(78, 80, 74, 76), squad=82),
    # --- Gruppe I ---
    "Frankreich": _t("Frankreich", coach=(86, 84, 88, 86), chem=(82, 84, 78, 80), squad=92),
    "Irak": _t("Irak", coach=(60, 58, 58, 62), chem=(76, 76, 66, 68), squad=58),
    "Norwegen": _t("Norwegen", coach=(72, 70, 68, 78), chem=(80, 82, 72, 76), squad=80),
    "Senegal": _t("Senegal", coach=(70, 70, 68, 64), chem=(80, 82, 74, 76), squad=82),
    # --- Gruppe J ---
    "Algerien": _t("Algerien", coach=(70, 68, 70, 64), chem=(76, 76, 70, 72), squad=74),
    "Argentinien": _t("Argentinien", coach=(90, 86, 88, 88), chem=(88, 90, 80, 84), squad=92),
    "Österreich": _t("Österreich", coach=(86, 84, 84, 80), chem=(84, 86, 76, 80), squad=78),
    "Jordanien": _t("Jordanien", coach=(62, 58, 58, 66), chem=(78, 78, 66, 66), squad=56),
    # --- Gruppe K ---
    "Kolumbien": _t("Kolumbien", coach=(76, 74, 74, 76), chem=(80, 82, 74, 76), squad=82),
    "DR Kongo": _t("DR Kongo", coach=(68, 66, 66, 70), chem=(74, 74, 68, 70), squad=68),
    "Portugal": _t("Portugal", coach=(80, 80, 80, 74), chem=(78, 80, 76, 78), squad=90),
    "Usbekistan": _t("Usbekistan", coach=(64, 62, 60, 68), chem=(80, 80, 66, 68), squad=58),
    # --- Gruppe L ---
    "Kroatien": _t("Kroatien", coach=(82, 80, 84, 86), chem=(84, 86, 76, 80), squad=82),
    "England": _t("England", coach=(82, 82, 82, 58), chem=(72, 74, 74, 78), squad=90),
    "Ghana": _t("Ghana", coach=(66, 64, 64, 66), chem=(72, 72, 70, 72), squad=70),
    "Panama": _t("Panama", coach=(66, 64, 64, 72), chem=(78, 78, 68, 70), squad=58),
}


# Paarungen des 1. Spieltags (Gruppenspiel 1). Erstgenanntes Team = laut
# Spielplan zuerst geführt. Die jeweils zweite Paarung pro Gruppe ergibt
# sich zwingend aus den verbleibenden zwei Teams.
_MATCHDAY_ONE = [
    # Gruppe A (11.06.)
    ("Mexiko", "Südafrika"),
    ("Südkorea", "Tschechien"),
    # Gruppe B (12./13.06.)
    ("Kanada", "Bosnien-Herzegowina"),
    ("Katar", "Schweiz"),
    # Gruppe C (13.06.)
    ("Brasilien", "Marokko"),
    ("Haiti", "Schottland"),
    # Gruppe D (12./13.06.)
    ("USA", "Paraguay"),
    ("Australien", "Türkei"),
    # Gruppe E
    ("Deutschland", "Elfenbeinküste"),
    ("Curaçao", "Ecuador"),
    # Gruppe F (14.06.)
    ("Niederlande", "Japan"),
    ("Schweden", "Tunesien"),
    # Gruppe G (15.06.)
    ("Belgien", "Ägypten"),
    ("Iran", "Neuseeland"),
    # Gruppe H (15.06.)
    ("Spanien", "Kap Verde"),
    ("Saudi-Arabien", "Uruguay"),
    # Gruppe I (16.06.)
    ("Frankreich", "Senegal"),
    ("Irak", "Norwegen"),
    # Gruppe J (16.06.)
    ("Argentinien", "Algerien"),
    ("Österreich", "Jordanien"),
    # Gruppe K (17.06.)
    ("Portugal", "DR Kongo"),
    ("Kolumbien", "Usbekistan"),
    # Gruppe L (17.06.)
    ("England", "Kroatien"),
    ("Ghana", "Panama"),
]


def matchday_one() -> list[tuple[Team, Team]]:
    """Liefert alle 24 Begegnungen des 1. Spieltags der WM 2026."""
    return [(TEAMS[home], TEAMS[away]) for home, away in _MATCHDAY_ONE]
