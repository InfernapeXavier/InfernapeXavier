"""Test the profile generator through its generated README."""

import json
import runpy
import unittest
from contextlib import chdir
from pathlib import Path
from tempfile import TemporaryDirectory


class GenerateReadmeTest(unittest.TestCase):
    def test_profile_keeps_compact_interests_collapsed(self):
        script = Path(__file__).with_name("generate_readme.py").resolve()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / ".github" / "scripts"
            scripts.mkdir(parents=True)
            (root / "data").mkdir()
            data = {
                "currentlyWatching": [
                    {"title": title} for title in ["Frieren", "氷菓", "A & B", "Omitted anime"]
                ],
                "currentlyReading": [
                    {"title": title}
                    for title in ["Yotsuba&!", "SPY x FAMILY", "Blue Period", "Omitted manga"]
                ],
            }
            (root / "data" / "anilist.json").write_text(json.dumps(data))
            with chdir(scripts):
                runpy.run_path(str(script), run_name="__main__")
            readme = (root / "README.md").read_text()

        self.assertIn("Infrastructure Engineer", readme)
        self.assertIn("[Academia.edu](https://www.academia.edu)", readme)
        self.assertIn("(http://rohitc.tech)", readme)
        self.assertIn("AI tooling infrastructure", readme)
        self.assertNotIn("<details open", readme)
        interests = readme.split("<details>")[1].split("</details>")[0]
        self.assertIn("Outside of work", interests)
        for title in ["Frieren", "氷菓", "A & B", "Yotsuba&!", "SPY x FAMILY", "Blue Period"]:
            self.assertIn(f"- {title}\n", interests)
        self.assertNotIn("Omitted", readme)
        for removed in ["spotify", "intro.png", "```bash"]:
            self.assertNotIn(removed, readme)

    def test_missing_cache_keeps_intro_and_empty_interests(self):
        script = Path(__file__).with_name("generate_readme.py").resolve()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / ".github" / "scripts"
            scripts.mkdir(parents=True)
            with chdir(scripts):
                runpy.run_path(str(script), run_name="__main__")
            readme = (root / "README.md").read_text()

        self.assertIn("# Hi, I'm Rohit", readme)
        self.assertIn("### Watching\n\nNothing currently.", readme)
        self.assertIn("### Reading\n\nNothing currently.", readme)


if __name__ == "__main__":
    unittest.main()
