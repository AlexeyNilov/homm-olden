---
title: HOMM Olden Era Reference
layout: default
permalink: /
---

# HOMM Olden Era — Reference

<p class="lede">Hero classes, subclasses, and starting loadouts for
<em>Heroes of Might and Magic: Olden Era</em>. Datamined from the game's
JSON files; updated to match the current build.</p>

## Pages

- **[Subclasses & Required Skills](subclasses/)** — A 24-row matrix of every
  subclass (two per class, twelve classes), showing the five skills each
  needs at level&nbsp;3 plus the unique passive effect. Built around the
  fact that every subclass takes exactly 1 Combat + 1 Magic + 1 School + 2
  Utility skills, the design surfaces that pattern at a glance.

- **[Heroes — Starting Skills, Stats & Armies](heroes/)** — All 108 stock
  heroes by faction, with their starting Attack/Defense/Power/Knowledge,
  starting skills (each hero gets the faction skill plus one other),
  starting army composition (three unit stacks with min/max counts), and
  signature specialization name.

## Notes

- Six playable factions: Temple (human), Necropolis (undead), Grove
  (nature), Hive (demon), Schism (unfrozen), Dungeon. Each has 18 heroes
  split into two classes (Might / Magic).
- Two skills are class-locked and never appear in subclass conditions:
  *Combat* (Might-only) and *Thaumaturgy* (Magic-only). *Siegecraft* and
  *Recruitment* are also never required for any subclass.
- Effect text is preserved verbatim; placeholders like `{0}` are filled at
  runtime from each subclass's bonuses block.

<p class="note"><strong>Reproduce</strong>: <code>python3
catalog/scripts/build_docs.py</code> regenerates these pages from
<code>HeroesOldenEra_Data/StreamingAssets/Core.zip</code> after extraction
into <code>catalog/raw/</code>.</p>
