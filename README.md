# Heroes of Might and Magic: Olden Era — Datamine

Hero classes, subclasses, and starting loadouts for *HOMM: Olden Era*,
extracted from the game's JSON files and rendered as a small reference site.

**Site**: <https://alcaras.github.io/homm-olden/>

## What's here

```
docs/                # GitHub Pages site (the published reference)
  index.md
  subclasses.md      # 24-row sparse-matrix subclass map
  heroes.md          # 108 stock heroes by faction
  _layouts/, assets/ # Jekyll layout + Tufte-inspired CSS

catalog/
  scripts/           # Build scripts (re-run to regenerate)
    load_json.py            # tolerant JSON loader (BOMs, comments, trailing commas)
    build_catalog.py        # SQLite catalog of every entity
    build_classes_json.py   # 12 classes with stat rolls + skill weights
    build_heroes_starting_skills.py
    build_specializations_json.py
    build_docs.py           # generates docs/*.md
    analysis_tier_list.py   # squadValue / costGold tier list
    analysis_hero_score.py
    analysis_magic_coverage.py
  out/                # Derived analyses (CSV / JSON / MD)
    classes.json              # all 12 classes, every starting stat + skill weight
    specializations.json      # all 126 hero specializations
    heroes_starting_skills.{md,csv}
    tier_list.{md,csv}
    hero_score.{md,csv}
    magic_coverage.{md,csv}
    catalog.sqlite            # full SQLite catalog of every entity
```

The raw game files (`HeroesOldenEra_Data/`, `catalog/raw/`) are **deliberately
excluded** from this repo — they're copyrighted game data. To regenerate the
JSONs and the site from a fresh checkout, you need a copy of the game.

## Reproducing locally

1. Install the game and locate `HeroesOldenEra_Data/` (Steam: `~/Library/Application Support/Steam/steamapps/common/Heroes of Might and Magic Olden Era/`).
2. Symlink or copy that folder into the repo root.
3. Extract the game data:
   ```bash
   python scripts/extract_data.py 
   ```
4. Build the catalog and docs:
   ```bash
   python3 catalog/scripts/build_catalog.py
   python3 catalog/scripts/build_classes_json.py
   python3 catalog/scripts/build_specializations_json.py
   python3 catalog/scripts/build_docs.py
   # optional analyses
   python3 catalog/scripts/analysis_tier_list.py
   python3 catalog/scripts/analysis_hero_score.py
   python3 catalog/scripts/analysis_magic_coverage.py
   ```

## Notes

- All hero / unit / skill / subclass display names are pulled from the
  English locale (`raw/Lang/english/texts/*.json`).
- The build is intentionally simple: one tolerant JSON loader + a few
  Python scripts using only the standard library (no extra deps).
- Effects render with `{0}` placeholders preserved — the values are
  computed at runtime from each entity's `bonuses` block. The
  `descriptionArgs` field in `specializations.json` tells you what each
  placeholder maps to.

## Disclaimer

Fan-made reference. Not affiliated with Unfrozen, Hooded Horse, or
Ubisoft. All names and effect text remain property of the game's
publishers; reproduced here for community reference only.
