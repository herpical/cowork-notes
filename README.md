# cowork-notes

## Vorhersagesystem für den ersten Spieltag

Ein Vorhersagemodell, das speziell auf den **ersten Spieltag** zugeschnitten
ist. Zu diesem Zeitpunkt gibt es noch keine Form-, xG- oder Tabellendaten der
laufenden Saison. Deshalb stützt sich das Modell auf die beiden
aussagekräftigsten früh verfügbaren Signale:

1. **Qualität des Trainerstabs** – Cheftrainer, Assistenz-/Funktionsteam,
   taktische Erfahrung und Stabilität (gleicher Stab wie in der Vorsaison?).
2. **Eingespieltheit der Mannschaft** – wie gut sich das Team bereits als
   Einheit kennt: gehaltener Kader, gemeinsame Spielminuten der Stamm-Elf,
   Integration der Neuzugänge und Qualität der Vorbereitung.

Eine **Kaderqualität** (Roh-Talent) fließt als Grundlinie mit geringerem
Gewicht ein, da sie am ersten Spieltag weniger aussagekräftig ist.

### Funktionsweise

```
Trainerstab (40 %) ┐
Eingespieltheit (40 %) ┼─► Team-Stärke (0–100)
Kaderqualität (20 %) ┘

Δ Stärke + Heimvorteil ─► erwartete Tordifferenz ─► Poisson
                                    │
                                    └─► Heimsieg / Remis / Auswärtssieg + Ergebnis
```

Die Stärkedifferenz (inkl. Heimvorteil) wird in eine erwartete Tordifferenz
übersetzt und über zwei Poisson-Verteilungen in Wahrscheinlichkeiten und das
wahrscheinlichste Ergebnis umgerechnet. Alle Gewichte und Parameter sind
konfigurierbar.

### Nutzung

Beispiel-Spieltag berechnen:

```bash
python -m matchday_predictor
```

Mit Aufschlüsselung der Einzelbeiträge:

```bash
python -m matchday_predictor --details
```

Eigene Begegnungen aus einer JSON-Datei (Format siehe
`examples/matchday.json`):

```bash
python -m matchday_predictor --json examples/matchday.json
```

Gewichtung anpassen (z. B. Trainerstab stärker gewichten):

```bash
python -m matchday_predictor --coaching-weight 0.5 --cohesion-weight 0.35 --squad-weight 0.15
```

### Programmatische Nutzung

```python
from matchday_predictor import (
    CoachingStaff, TeamChemistry, Team, MatchdayPredictor,
)

home = Team(
    name="Eintracht Beispielstadt",
    staff=CoachingStaff("Stab", head_coach=88, assistants=82,
                        tactical_experience=85, continuity=90),
    chemistry=TeamChemistry(squad_continuity=85, minutes_together=88,
                            new_signings_integration=78, preseason_quality=82),
    squad_quality=80,
)
away = Team(
    name="FC Neuaufbau",
    staff=CoachingStaff("Stab", head_coach=72, assistants=65,
                        tactical_experience=60, continuity=40),
    chemistry=TeamChemistry(squad_continuity=45, minutes_together=40,
                            new_signings_integration=55, preseason_quality=60),
    squad_quality=86,
)

prediction = MatchdayPredictor().predict(home, away)
print(prediction.summary())
```

### Projektstruktur

```
matchday_predictor/
  models.py      # Team, CoachingStaff, TeamChemistry + Score-Berechnung
  predictor.py   # Stärke-, Poisson- und Wahrscheinlichkeitslogik
  sample_data.py # Beispiel-Spieltag mit illustrativen Werten
  cli.py         # Kommandozeilen-Schnittstelle
examples/        # Beispiel-JSON für eigene Begegnungen
tests/           # pytest-Tests
```

### Tests

```bash
python -m pytest
```

> Hinweis: Die Werte in `sample_data.py` und `examples/` sind frei gewählt und
> dienen nur der Veranschaulichung. Für reale Vorhersagen ersetzt man sie durch
> eigene Einschätzungen der Teams.
