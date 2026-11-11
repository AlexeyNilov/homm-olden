# CLAUDE.md — HOMM Olden Era datamine + reference site

Project notes for future agent sessions in this repo.

## What this is

A datamine of *Heroes of Might and Magic: Olden Era*
## Layout

```
HeroesOldenEra_Data/         # Game install (gitignored — copyrighted)
  StreamingAssets/Core.zip   # ~7800 hand-authored JSON5-ish data files
  resources.assets / .resS   # ~4 GB Unity bundle holding all art assets
  sharedassets*.assets       # 70+ secondary bundles (some UI/building textures)
  il2cpp_data/Metadata/      # global-metadata.dat (IL2CPP string-mineable)
  boot.config                # game build-guid lives here

dll/                         # User-dropped GameAssembly.dll (gitignored)
                             # 95 MB; only needed to re-confirm extracted asset
                             # names match a new game build.

catalog/
  raw/                       # Extracted Core.zip + Unity ScriptableObjects
                             # (gitignored — copyrighted)
    DB/                      # Most data files we touch
    Lang/english/texts/      # Localized display names (menu.json holds the
                             # hotkey labels alongside the rest)
    Assets/                  # Extracted ScriptableObjects (e.g. QwertyProfile.json)

  scripts/                   # All Python build scripts
    load_json.py             # Tolerant loader (BOMs, // comments, trailing commas)
    build_catalog.py         # Generic SQLite catalog of every entity
    build_classes_json.py    # 12 classes × stats × skill weights × subclasses
    build_classes_data_js.py # Emits docs/classes-data.js for the Hero Sim
    build_specializations_json.py
    build_heroes_starting_skills.py
    build_data_js.py         # Generates docs/data.js (the SPA's data)
    build_skills.py          # Emits docs/skills-data.js (incl. sub-skills)
    build_spells.py          # Emits docs/spells-data.js (placeholder-resolved)
    build_mechanics.py       # Faction signature-mechanic copy (shared)
    build_tier_list.py       # Hero tiers + faction-page metadata + subclass
                             # verdicts (lexiav-grounded)
    build_calc.py            # Buildings + Laws calculator data
    build_draft_guide.py     # Per-faction draft guidance
    build_faction_guides.py  # Faction overview cards
    build_artifacts.py / build_map_objects.py / build_map_templates.py /
    build_resources.py / build_hotkeys.py / build_docs.py
    extract_images.py        # Pulls 1400+ PNGs from resources.assets +
                             # sharedassets*.assets via UnityPy
    analysis_*.py            # tier list, hero score, magic coverage

  out/                       # Generated artifacts (committed)
    catalog.sqlite, classes.json, specializations.json, *.csv, *.md

docs/                        # GitHub Pages root (committed)
  index.html                 # Loads React + ReactDOM from CDN
  app.jsx                    # Path-routed SPA shell + nav tabs
  *-view.jsx                 # Component per page (e.g. heroes-view, calc-view,
                             # combat-view, hotkeys-view, hero-builder-view)
  *-data.js                  # Generated data files (data.js, tier-data,
                             # spells-data, skills-data, classes-data,
                             # calc-data, artifacts-data, hotkeys-data, etc.)
  dist/*.js                  # Pre-compiled JSX (esbuild output, committed)
  style.css                  # Tufte-inspired (cream paper, charter serif).
                             # Dark-mode override via @media prefers-color-scheme
                             # at the bottom — use token vars, not literals.
  img/{factions,heroes,units,specs,skills,subskills,
        spells,buildings,laws,map_objects,resources,artifacts}/  # 1400+ PNGs
  404.html                   # GitHub Pages SPA fallback (path routing support)
  .nojekyll

scripts/
  build_jsx.sh               # Pre-compile docs/*.jsx → docs/dist/*.js via npx esbuild
  dev_server.py              # Local SPA-aware dev server (path-route fallback)
```

## SPA pages / routes

`/` Index · `/mechanics` · `/factions`, `/faction/<id>` · `/buildings/<id>` · `/laws/<id>` · `/subclasses` · `/skills` · `/spells`, `/spell/<id>` · `/map-objects` · `/map-templates` · `/resources` · `/artifacts` · `/heroes`, `/hero/<id>` · `/units`, `/units/<faction>`, `/unit/<id>` · `/tier` · `/guides` · `/draft` · `/combat` (damage sim) · `/hotkeys` · `/builder` and `/builder/<hero_id>?lvl=N` (Hero Level-Up Simulator).

Each route corresponds to a `<window.XxxView>` mounted from `app.jsx`. Subviews access `window.OE_DATA`, `window.OE_<page>_DATA`, and `window.OE_routeToUrl(...)` / `window.OE_go(...)` for navigation.

## Reproducing from a clean game install

1. Game install at `~/Library/.../Heroes of Might and Magic Olden Era/HeroesOldenEra_Data` symlinked or copied into the repo root.
2. `python3 -c "<the unzip snippet from README.md>"` extracts `Core.zip` → `catalog/raw/`.
3. `python3 catalog/scripts/build_data_js.py` regenerates `docs/data.js`.
4. Then in dependency order: `build_mechanics.py`, `build_tier_list.py` (imports from mechanics), then `build_calc.py`, `build_skills.py`, `build_spells.py`, `build_artifacts.py`, `build_map_objects.py`, `build_map_templates.py`, `build_resources.py`, `build_faction_guides.py`, `build_draft_guide.py`, `build_classes_data_js.py`.
5. **Hotkeys**: `python3 catalog/scripts/build_hotkeys.py --extract` pulls the `QwertyProfile` TextAsset out of `HeroesOldenEra_Data/resources.assets` via UnityPy → `catalog/raw/Assets/QwertyProfile.json`, then rebuilds `docs/hotkeys-data.js`. After the first extract, plain `python3 catalog/scripts/build_hotkeys.py` is enough.
6. **After ANY `.jsx` change**: `scripts/build_jsx.sh` to regenerate `docs/dist/*.js`. Uses `npx esbuild` (auto-installs on first run; cache at `~/.npm/_npx`). Without this step the site loads the old compiled JS.
7. `python3 -m venv .venv && .venv/bin/pip install UnityPy` then `.venv/bin/python catalog/scripts/extract_images.py` regenerates `docs/img/`. The image index now scans all `sharedassets*.assets` bundles plus `resources.assets` (some building/UI textures live in the secondary bundles).

Local preview: `python3 scripts/dev_server.py [port]` — SPA-aware fallback (any unknown path serves `index.html`, required for path routing). Plain `python3 -m http.server` won't work for deep links.

## Conventions and gotchas

- **JSONs are not strict JSON.** Always go through `load_json.load_array()`. They have BOMs, `//` line comments, occasional trailing commas, and the wrapper `{"array": [...]}`.
- **Localization wrapper differs.** `Lang/english/texts/*.json` are wrapped as `{"tokens": [...]}` and `Lang/args/*.json` as `{"tokensArgs": [...]}`. Each entry is `{sid, text}`.
- **Faction id duality.** In-game `fraction` field uses keys `human / undead / nature / demon / unfrozen / dungeon`. Display ids in the site use `temple / necropolis / grove / hive / schism / dungeon`. `data.js` FACTIONS records map both via `id` (display) and `unitKey` (in-game). Heroes/units in `data.js` use the display id.
- **Routing.** Path-based SPA: `/units/temple`, `/buildings/temple?b=Main:2`, etc. App detects `/homm-olden/` base path on GitHub Pages. `404.html` runs the spa-github-pages fallback so deep links work. `app.jsx` migrates legacy `#path` URLs once on first load. `<base href>` is injected at the top of `<head>` before any other tags so relative script srcs resolve correctly after the `replaceState` shim.
- **JSX → JS pipeline.** `docs/*.jsx` files are pre-compiled to `docs/dist/*.js` via `scripts/build_jsx.sh` (esbuild). The site loads the compiled JS, NOT the JSX. Forgetting to rebuild = stale UI. React + ReactDOM still load via CDN (kept global, not bundled).
- **`window.OE_go`** is exposed in `app.jsx` so view files compiled separately can navigate without a prop thread.
- **Dark mode.** Token system in `:root` has `--bg / --paper / --bg-warm / --ink / --ink-2 / --muted / --rule / --rule-bold / --hover / --accent / --accent-2 / --gold` etc., with overrides in a `@media (prefers-color-scheme: dark)` block near the bottom of `style.css`. **Always use the tokens, never hardcoded `white` / `#fff` etc.** — pages built with literals (combat sim, hotkeys) were unreadable in dark mode.
- **Attack-type mapping (verified against unit data, not the field names):**
  - `attackType_ = "melee"` → "Melee"
  - `attackType_ = "shoot"` → "Ranged" (archers, mages — `shoot_attack` damage tag, `range_type` AI). E.g. crossbowman, succubus, **Faun = `elf_tracker`**, lich.
  - `attackType_ = "range"` → "Long" (long-reach melee — `range_attack` tag, `reach_type` AI). E.g. unfrozen_cultist, trick_demon.
  - Source counts: 104 / 35 / 13. Don't guess from the keyword names; they are misleading.
- **Image asset names.** Heroes: `hero_<faction>_<n>_<name>` exactly as JSON `icon` field. Specs: `<spec_id>` exactly. Factions: `fraction_<key>` (preferred) or `<key>_icon` (fallback). Units: title-cased `Icon_<UnitId>` with one alias (`trogl` → `Troglodyte`) and a few units that use bare-id names (`halfling`, `unfrozen_cultist`, `dragon_hunter`); see `extract_images.py` for the fallback chain.
- **Map-object icon overrides.** `extract_images.py` has a `MAP_OBJECT_OVERRIDES` dict for ids where the default candidates don't resolve (typos in shipped asset names like `barracks_neutral_giand_frog`, placeholder-name remaps like `mana_well → autumn_well_01_diffuse`, `_icon`-suffixed sprites). Six map objects have no shipped texture and render via the `onError` fallback.
- **Summoned units.** `build_data_js.py` flags base-variant units that have no `upgradeSid` and no `expBonus` as `summoned: true` (only `lava_larva` and `undead_peasant` qualify). The combat-sim and faction-units view filter these out so the real tier-N base (e.g. Scorpion, not Fire Larva) isn't masked.
- **Class-locked skills** never appear in subclass conditions: `skill_battle_artistry` (Combat, might-only) and `skill_wisdom` (Thaumaturgy, magic-only). Subclass universe is exactly 20 skills; `skill_siege` (Siegecraft) and `skill_trainer` (Recruitment) are also never required.
- **Subclass recipe is uniformly 1-1-1-2** across Combat / Magic-craft / School / Utility for all 24 subclasses. The matrix surfaces this; see footer note on `subclasses-view.jsx`.
- **Stat-roll breakpoint is level 24**, not 12 (some legacy HOMM doc uses 12). All heroes within a faction-class share starting stats, statsRolls, and skill table.
- **Subclass requirement = level 3** in each of 5 specific main skills. A skill has 3 levels, so 15 advances total. Heroes start with 1–2 skills at L1, or 1 skill at L2.
- **Olden-Era level-up mechanic (used by the Hero Sim):**
  - Stat point: +1 to one of A/D/P/K via the class's `rollPre24` (below L24) or `rollPost24` (at/after) probabilities.
  - 3-skill offer composition: 1 guaranteed UPGRADE (existing skill, cur 1–2), 1 guaranteed NEW (cur = 0), 1 "joker" slot ≈50/50 either. Each individual pick within its bucket is weighted by the class chance table. Falls back when one bucket is empty.
  - After picking a main skill that advances to L2 or L3, the game offers 3 sub-skills (from `skills.json → parametersPerLevel[lvl].subSkills`). Pick 1.
  - All confirmed against the IL2CPP class names `BhLevelUpStatsAndSkillsView` / `BhLevelUpSkillView` / `BhLevelUpSubSkillView` and the wiki / community guides.
- **Specialization descriptions** still contain `{0}/{1}/{2}` placeholders; resolution requires walking the spec's `bonuses` block via the runtime arg resolver. Not implemented. `specializations.json` includes `descriptionArgs` mapping each placeholder to a named runtime variable.
- **Game version**: there is no semver. `boot.config` has a `build-guid`; `Core.zip` mtime is the data freshness. Footer surfaces both.
- **`gh` CLI is authenticated** as account `alcaras` (active). `drabiej` also logged in but inactive.
- **Don't push raw game data**. `.gitignore` excludes `HeroesOldenEra_Data/`, `catalog/raw/`, and `dll/`. The 100+ MB of extracted icons in `docs/img/` is committed under fan-content disclaimer in README.
- **Dropbox sync EPERM lock.** Mid-sync edits sometimes fail with `EPERM: operation not permitted`. Re-read the file (it may have been overwritten by Dropbox) and re-apply. The shell heredoc append pattern (`cat >> file << EOF`) usually wins races.

## Common tasks

- **After a game patch**: re-extract `Core.zip` → `catalog/raw/`; rerun `build_data_js.py` + the other `build_*.py` scripts; if art changed, rerun `extract_images.py`; if hotkeys changed, rerun `build_hotkeys.py --extract`. Commit + push triggers Pages rebuild (~30–60s).
- **Adding a new view**: data lives in `docs/<name>-data.js` (generate via a `build_<name>.py` script), component in `docs/<name>-view.jsx`, route + nav tab in `docs/app.jsx` (`SIMPLE_VIEWS`, `parsePath`, `go`, `titleFor`, the `<nav>` block, and the dispatch `{route.view === '<name>' && ...}`), `<script>` tag in `docs/index.html` for both the data file and the compiled dist file, then `bash scripts/build_jsx.sh`.
- **CSS changes**: `docs/style.css`. Color tokens in `:root` + dark-mode block at the bottom. Multi-select segmented controls use `.seg.multi`; single-select uses `.seg`.
- **Tooltips**: see the `.u-tooltip` pattern in `style.css` + the corresponding markup in `units-view.jsx` for the hover-revealed pattern with auto-flip near the bottom.

## Don't

- Don't add Jekyll back. The `.nojekyll` is intentional — keeps deploys instant and lets `.jsx` / nested folders work.
- Don't rename the in-game `fraction` keys; only the display layer renames them. Anything that joins on raw JSONs needs the in-game key.
- Don't trust the `attackType_` keyword name. Verify mapping against `damageDealer.tags[0]` (`shoot_attack` vs `range_attack`) and the unit's `ai` field.
- Don't manually edit `docs/data.js`, `docs/<name>-data.js`, or `docs/img/*` — all generated. Edit the source script and rerun.
- Don't force-push to `main` without an explicit user-confirmed reason; `--force-with-lease` is preferred when force-push is needed.
