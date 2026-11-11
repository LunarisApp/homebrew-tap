import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("updater", Path(__file__).with_name("update-release.py"))
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class ReleaseUpdateTests(unittest.TestCase):
    def test_signing_transitions_and_idempotency(self):
        for path in updater.PACKAGES:
            current = (updater.ROOT / path).read_text()
            formula = path.startswith("Formula/")
            signed = updater.render(current, "1.0.0", "a" * 64, False, formula)
            self.assertNotIn("-adhoc", signed)
            self.assertNotIn("caveats", signed)
            adhoc = updater.render(signed, "1.0.1", "b" * 64, True, formula)
            self.assertIn("-adhoc", adhoc)
            self.assertIn("caveats", adhoc)
            self.assertEqual(adhoc, updater.render(adhoc, "1.0.1", "b" * 64, True, formula))
            with self.assertRaisesRegex(ValueError, "downgrade"):
                updater.render(adhoc, "1.0.0", "b" * 64, True, formula)

    def test_verify_both_artifacts_before_writing(self):
        for corrupt in (False, True):
            with self.subTest(corrupt=corrupt), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                originals = {}
                for path in updater.PACKAGES:
                    (root / path).parent.mkdir(exist_ok=True)
                    originals[path] = (updater.ROOT / path).read_text()
                    (root / path).write_text(originals[path])
                names = [pattern.format(version="1.0.0", suffix="") for pattern in updater.PACKAGES.values()]
                release = {"tagName": "v1.0.0", "isDraft": False, "isPrerelease": False,
                           "assets": [{"name": name} for name in names]}

                def gh(*args):
                    if args[1] == "view":
                        return json.dumps(release)
                    destination = Path(args[args.index("--dir") + 1])
                    digest = hashlib.sha256(b"artifact").hexdigest()
                    for index, name in enumerate(names):
                        (destination / name).write_bytes(b"bad" if corrupt and index == 1 else b"artifact")
                    (destination / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name in names))
                    return ""

                with patch.object(updater, "gh", gh):
                    if corrupt:
                        with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                            updater.update(root=root)
                    else:
                        updater.update(root=root)
                for path, original in originals.items():
                    content = (root / path).read_text()
                    if corrupt:
                        self.assertEqual(original, content)
                    else:
                        if path.startswith("Formula/"):
                            self.assertIn("releases/download/v1.0.0/", content)
                            self.assertIn("lunaris-cli-1.0.0-", content)
                        else:
                            self.assertIn('version "1.0.0"', content)
                        self.assertNotIn("-adhoc", content)

    def test_reject_draft_prerelease_and_invalid_tag(self):
        for change in ({"isDraft": True}, {"isPrerelease": True}, {"tagName": "v1.0.0-rc.1"}):
            release = {"tagName": "v1.0.0", "isDraft": False, "isPrerelease": False, "assets": [], **change}
            with patch.object(updater, "gh", return_value=json.dumps(release)), self.assertRaises(ValueError):
                updater.update()


if __name__ == "__main__":
    unittest.main()
