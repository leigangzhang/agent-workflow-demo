"""The evidence runner: it must never mistake a sentence or a placeholder for a command."""

from __future__ import annotations


from tests.harness import ROOT, WORKFLOW, load_checker, load_run_evidence, sections
from pathlib import Path
import subprocess
import tempfile
import unittest


class RunEvidence(unittest.TestCase):
    """The runner must never mistake a sentence or a placeholder for a command."""

    @classmethod
    def setUpClass(cls):
        cls.module = load_run_evidence()

    def test_recognises_runnable_commands(self):
        for entry in ("python3 tools/check-invariants.py", "./scripts/check.sh", "make check"):
            with self.subTest(entry=entry):
                self.assertEqual(self.module.classify(entry)[0], "runnable")

    def test_treats_prose_as_manual_evidence(self):
        for entry in ("read the Alternatives considered section yourself", "run the owning test for each changed file"):
            with self.subTest(entry=entry):
                self.assertNotEqual(self.module.classify(entry)[0], "runnable")

    def test_a_command_shaped_entry_must_use_a_runner_token(self):
        for entry in ("definitely-not-on-path --check", "./scripts/missing.sh"):
            with self.subTest(entry=entry):
                self.assertTrue(self.module.looks_like_command(entry))

    def test_plain_prose_is_not_mistaken_for_a_command(self):
        for entry in ("read the Migration steps yourself", "confirm the outside install ran in a clean directory"):
            with self.subTest(entry=entry):
                self.assertFalse(self.module.looks_like_command(entry))

    def test_placeholders_are_never_runnable(self):
        self.assertEqual(self.module.classify("<your unit command>")[0], "placeholder")

    def test_a_placeholder_anywhere_disqualifies_the_entry(self):
        self.assertEqual(self.module.classify("python3 tools/x.py --base <ref>")[0], "placeholder")

    def test_a_command_that_cannot_run_is_unknown_not_failed(self):
        """A tooling problem is not a verdict about the change, and it is never a pass."""
        self.assertEqual(self.module.verdict_for(None, "could not spawn it")[0], "UNKNOWN")
        for code in (126, 127):
            with self.subTest(exit=code):
                self.assertEqual(self.module.verdict_for(subprocess.CompletedProcess(args="x", returncode=code), None)[0], "UNKNOWN")

    def test_a_command_that_ran_gets_a_pass_or_fail_verdict(self):
        for code, expected in ((0, "PASS"), (1, "FAIL"), (2, "FAIL")):
            with self.subTest(exit=code):
                self.assertEqual(self.module.verdict_for(subprocess.CompletedProcess(args="x", returncode=code), None)[0], expected)

    def test_resolution_is_checked_against_the_repository_root(self):
        self.assertTrue(self.module.resolves(ROOT, "python3 tools/check-invariants.py"))
        self.assertFalse(self.module.resolves(ROOT, "./tools/does-not-exist.py"))

    def test_every_declared_command_resolves(self):
        violations = self.module.validate_commands(self.module.plan_for_all(WORKFLOW))
        self.assertEqual(violations, [], "a declared command that cannot run is not evidence")

    def test_a_later_record_gets_a_successor_instead_of_overwriting(self):
        """An evidence record is a claim about a moment; a re-run must not rewrite it."""
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "evidence" / "2026-01-01-main.md"
            base.parent.mkdir(parents=True)
            self.assertEqual(self.module.unique_record_path(base), base)
            base.write_text("first run\n", encoding="utf-8")
            successor = self.module.unique_record_path(base)
            self.assertEqual(successor.name, "2026-01-01-main-2.md")
            successor.write_text("second run\n", encoding="utf-8")
            self.assertEqual(self.module.unique_record_path(base).name, "2026-01-01-main-3.md")
            self.assertEqual(base.read_text(encoding="utf-8"), "first run\n")
