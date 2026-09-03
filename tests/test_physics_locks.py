#!/usr/bin/env python3
"""Physics locks for HORIZON v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import horizon  # noqa: E402

FUTURE = "2028-08-31"
COPY_FILES = (
    "README.md",
    "INTERDIT.md",
    "JUGE.md",
    "horizon.py",
    "examples/hybride.horizon.json",
    "NOTICE",
    "COPYRIGHT.md",
)


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _cli(args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "horizon.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        **kwargs,
    )


def _carte_fichier(**overrides) -> dict:
    carte = {
        "format": "horizon.v0",
        "horizon_id": "HZ-test",
        "cible": "unforge",
        "cible_id": None,
        "suite": "UFHY1",
        "hypothese": "au moins une des deux signatures survit",
        "re_presser_avant": FUTURE,
        "juridiction": "QC",
        "langue": "fr-CA",
        "pose_at": "2026-08-31T20:00:00Z",
        "revocable": True,
        "sceau": None,
        "note": "test",
    }
    carte.update(overrides)
    return carte


class Ufhy1IsASuiteNotADate(unittest.TestCase):
    def test_ufhy1_as_calendar_date_is_refused(self):
        with self.assertRaises(SystemExit) as ctx:
            horizon.ecrire("ed25519", "UFHY1")
        self.assertIn("suite, pas une date", str(ctx.exception))
        self.assertIn("UFHY1", str(ctx.exception))

    def test_each_suite_name_as_date_is_refused(self):
        for nom in horizon.SUITES:
            with self.subTest(nom=nom):
                with self.assertRaises(SystemExit) as ctx:
                    horizon.ecrire("ed25519", nom)
                self.assertIn("suite, pas une date", str(ctx.exception))

    def test_cli_ufhy1_as_date_is_refused(self):
        proc = _cli(["ecrire", "--suite", "ed25519", "--re-presser-avant", "UFHY1"])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("suite, pas une date", proc.stderr)

    def test_lire_ufhy1_as_date_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mauvais.horizon.json"
            p.write_text(_dump(_carte_fichier(re_presser_avant="UFHY1")), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                horizon.lire(str(p))
            self.assertIn("suite, pas une date", str(ctx.exception))


class MissingDateIsRefused(unittest.TestCase):
    def test_ecrire_empty_date_is_refused(self):
        with self.assertRaises(SystemExit) as ctx:
            horizon.ecrire("UFHY1", "")
        self.assertIn("manquant", str(ctx.exception))

    def test_ecrire_none_date_is_refused(self):
        with self.assertRaises(SystemExit) as ctx:
            horizon.ecrire("UFHY1", None)  # type: ignore[arg-type]
        self.assertIn("manquant", str(ctx.exception))

    def test_cli_missing_date_is_refused(self):
        proc = _cli(["ecrire", "--suite", "UFHY1"])
        self.assertNotEqual(proc.returncode, 0)
        combined = proc.stderr + proc.stdout
        self.assertIn("re-presser-avant", combined)

    def test_lire_missing_date_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sans-date.horizon.json"
            carte = _carte_fichier()
            del carte["re_presser_avant"]
            p.write_text(_dump(carte), encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                horizon.lire(str(p))
            self.assertIn("pas de date", str(ctx.exception))


class PastDateAtWriteIsRefused(unittest.TestCase):
    def test_past_date_at_write_is_refused(self):
        with self.assertRaises(SystemExit) as ctx:
            horizon.ecrire("UFHY1", "2020-01-01")
        self.assertIn("déjà passée", str(ctx.exception))

    def test_today_is_not_still_ahead(self):
        today = datetime.now(timezone.utc).date().isoformat()
        with self.assertRaises(SystemExit) as ctx:
            horizon.ecrire("ed25519", today)
        self.assertIn("déjà passée", str(ctx.exception))

    def test_cli_past_date_is_refused(self):
        proc = _cli(["ecrire", "--suite", "UFHY1", "--re-presser-avant", "2020-01-01"])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("déjà passée", proc.stderr)


class FutureDateWrites(unittest.TestCase):
    def test_future_yyyy_mm_dd_writes(self):
        carte = horizon.ecrire("UFHY1", FUTURE)
        self.assertEqual(carte["format"], "horizon.v0")
        self.assertEqual(carte["suite"], "UFHY1")
        self.assertEqual(carte["re_presser_avant"], FUTURE)
        self.assertEqual(carte["hypothese"], horizon.HYPOTHESES["UFHY1"])
        self.assertIsNone(carte["sceau"])

    def test_three_suites_write_when_date_is_ahead(self):
        for nom in horizon.SUITES:
            with self.subTest(nom=nom):
                carte = horizon.ecrire(nom, FUTURE)
                self.assertEqual(carte["suite"], nom)
                self.assertEqual(carte["re_presser_avant"], FUTURE)

    def test_mldsa87_may_be_declared_and_is_not_signed(self):
        carte = horizon.ecrire("mldsa87", FUTURE)
        self.assertEqual(carte["suite"], "mldsa87")
        self.assertIsNone(carte["sceau"])
        self.assertNotIn("quantique", _dump(carte))

    def test_cli_future_date_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.horizon.json"
            proc = _cli(
                [
                    "ecrire",
                    "--suite",
                    "UFHY1",
                    "--re-presser-avant",
                    FUTURE,
                    "--vers",
                    str(dest),
                ]
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            carte = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(carte["suite"], "UFHY1")
            self.assertEqual(carte["re_presser_avant"], FUTURE)


class DenyMeansResellNotFake(unittest.TestCase):
    def test_deny_note_is_resell_not_fake(self):
        carte = _carte_fichier(re_presser_avant="2020-01-01")
        jugement = horizon.juger(carte, aujourd=date(2026, 9, 3))
        self.assertEqual(jugement["decision"], "deny")
        note = jugement["note"]
        self.assertIn("resseller", note.lower())
        self.assertNotIn("fichier est faux", note.lower())
        self.assertNotIn("file is fake", note.lower())
        self.assertNotIn("the file is fake", note.lower())
        self.assertIn("pas faux", note)

    def test_cli_juger_expired_card_says_resell(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "perime.horizon.json"
            p.write_text(_dump(_carte_fichier(re_presser_avant="2020-01-01")), encoding="utf-8")
            proc = _cli(["juger", str(p)])
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["decision"], "deny")
            self.assertIn("resseller", out["note"].lower())
            self.assertNotIn("file is fake", out["note"].lower())

    def test_juger_on_the_named_day_is_deny_and_resell(self):
        named = date(2028, 8, 31)
        carte = _carte_fichier(re_presser_avant=named.isoformat())
        jugement = horizon.juger(carte, aujourd=named)
        self.assertEqual(jugement["decision"], "deny")
        self.assertEqual(jugement["jours_restants"], 0)
        self.assertIn("resseller", jugement["note"].lower())
        self.assertNotIn("fichier est faux", jugement["note"].lower())
        self.assertNotIn("file is fake", jugement["note"].lower())

    def test_future_card_is_allow(self):
        carte = horizon.ecrire("UFHY1", FUTURE)
        jugement = horizon.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertGreater(jugement["jours_restants"], 0)

    def test_example_hybride_juger_is_allow(self):
        proc = _cli(["juger", str(ROOT / "examples" / "hybride.horizon.json")])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertEqual(out["suite"], "UFHY1")


class NoQuantumSealInJson(unittest.TestCase):
    def test_ecrire_json_is_not_a_quantum_seal(self):
        dumped = _dump(horizon.ecrire("UFHY1", FUTURE))
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("quantique", dumped)

    def test_juger_json_is_not_a_quantum_seal(self):
        dumped = _dump(horizon.juger(horizon.ecrire("ed25519", FUTURE)))
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Imagine", dumped)

    def test_deny_json_is_not_a_quantum_seal(self):
        dumped = _dump(horizon.juger(_carte_fichier(re_presser_avant="2020-01-01"), aujourd=date(2026, 9, 3)))
        self.assertEqual(json.loads(dumped)["decision"], "deny")
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("Imagine", dumped)

    def test_example_card_is_not_a_quantum_seal(self):
        text = (ROOT / "examples" / "hybride.horizon.json").read_text(encoding="utf-8")
        self.assertNotIn("QUANTUM", text)
        self.assertNotIn("Imagine", text)
        self.assertNotIn("quantique", text)

    def test_cli_ecrire_stdout_is_not_a_quantum_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.horizon.json"
            proc = _cli(
                [
                    "ecrire",
                    "--suite",
                    "mldsa87",
                    "--re-presser-avant",
                    FUTURE,
                    "--vers",
                    str(dest),
                ]
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertNotIn("QUANTUM", proc.stdout)
            self.assertNotIn("quantique", proc.stdout)


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)

    def test_readme_names_three_suites_and_calendar_lock(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`ed25519`", text)
        self.assertIn("`UFHY1`", text)
        self.assertIn("`mldsa87`", text)
        self.assertIn("YYYY-MM-DD", text)
        self.assertIn("python3 horizon.py ecrire|lire|juger", text)
        self.assertIn("suite name, never a calendar date", text)

    def test_readme_names_utc_calendar_day(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("The date is a UTC calendar day.", text)

    def test_readme_says_ufhy1_signs_and_today_hypothesis_or_later(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("UFHY1 signs AND today; the hypothesis is OR later.", text)

    def test_readme_says_named_day_denies_resell_before_utc(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("named day", text.lower())
        self.assertIn("You resell before that UTC date.", text)

    def test_readme_says_deny_means_resell(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("resell", text)
        self.assertIn("the file is fake", text)

    def test_interdit_stays(self):
        text = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("re_presser_avant", text)
        self.assertIn("UFHY1", text)
        self.assertIn("resseller", text)

    def test_rail_copy_has_no_imagine_word(self):
        for rel in COPY_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("Imagine", text, msg=rel)
            self.assertNotIn("imagine", text, msg=rel)

    def test_rail_copy_does_not_claim_formal_verification(self):
        for rel in COPY_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("formally verified", text, msg=rel)
            self.assertNotIn("formally-verified", text, msg=rel)

    def test_cli_surface_stays_ecrire_lire_juger(self):
        proc = _cli(["-h"])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("ecrire", proc.stdout)
        self.assertIn("lire", proc.stdout)
        self.assertIn("juger", proc.stdout)


if __name__ == "__main__":
    unittest.main()
