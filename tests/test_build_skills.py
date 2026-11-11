"""Regression checks for descriptions emitted by the skill catalog builder."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalog.scripts import build_skills


class SkillDescriptionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "skills-data.js"
            with patch.object(build_skills, "OUT_JS", output):
                build_skills.build()
            payload = json.loads(output.read_text().split(" = ", 1)[1].removesuffix(";\n"))
        cls.skills = {skill["id"]: skill for skill in payload["SKILLS"]}

    def test_battlecraft_values(self):
        """Each Battlecraft rank displays its actual Attack and Defense bonus."""
        skill = self.skills["skill_formation"]
        for level, percent in zip(skill["levels"], (10, 15, 20)):
            self.assertIn(f"+{percent}% Attack", level["desc"])
            self.assertIn(f"+{percent}% Defense", level["desc"])
        self.assertEqual(skill["baseDesc"], skill["levels"][0]["desc"])

    def test_direct_and_constant_values(self):
        """Descriptions use argument mappings for percentages and fixed numbers."""
        assault = self.skills["skill_assault"]
        self.assertIn("+10%", assault["levels"][0]["desc"])
        luck = self.skills["skill_luck"]
        subskill = next(s for level in luck["levels"] for s in level["subskills"]
                        if s["id"] == "sub_skill_luck_5")
        self.assertIn("200%", subskill["desc"])
        self.assertIn("5%", subskill["desc"])

    def test_hero_dependent_formula(self):
        """Sight-dependent ranges retain the game's formula without inventing a hero."""
        skill = self.skills["skill_enlightenment"]
        subskill = next(s for level in skill["levels"] for s in level["subskills"]
                        if s["id"] == "sub_skill_enlightenment_3")
        self.assertIn("300% × hero sight radius", subskill["desc"])

    def test_reductions_have_one_sign(self):
        """Negative modifiers display the reduction sign already supplied by the text."""
        for level, percent in zip(self.skills["skill_protection"]["levels"], (10, 15, 20)):
            self.assertEqual(level["desc"], f"Friendly creatures take –{percent}% Damage from basic attacks.")
        luck = self.skills["skill_luck"]
        subskill = next(s for level in luck["levels"] for s in level["subskills"]
                        if s["id"] == "sub_skill_luck_3")
        self.assertEqual(subskill["desc"], "Enemy Luck is reduced by 1 in battle.")

    def test_fractional_percentages(self):
        """Communion preserves fractional percentage points instead of a raw fraction."""
        for level in self.skills["skill_faction_unfrozen"]["levels"]:
            self.assertIn("by 2.5%", level["desc"])

    def test_ability_levels(self):
        """Egg strength uses the ability level selected by each skill rank."""
        for level, percent in zip(self.skills["skill_faction_demons"]["levels"], (8, 12, 16)):
            self.assertIn(f"{percent}% of the total HP", level["desc"])

    def test_rank_arithmetic(self):
        """Avatar damage includes the per-rank multiplier and the fixed base bonus."""
        skill = self.skills["skill_summoner"]
        for level, damage in zip(skill["levels"], (6, 8, 10)):
            self.assertIn(f"+{damage}\u00a0Damage", level["desc"])

    def test_no_unexpanded_placeholders(self):
        """Catalog readers see values or formulas throughout every description."""
        for skill in self.skills.values():
            descriptions = [skill["baseDesc"]]
            for level in skill["levels"]:
                descriptions.append(level["desc"])
                descriptions.extend(s["desc"] for s in level["subskills"])
            for description in descriptions:
                with self.subTest(skill=skill["id"], description=description):
                    self.assertNotRegex(description, r"\{\d+\}|\?")


if __name__ == "__main__":
    unittest.main()
