"""Tests for the three tools. Standard library only.

    python3 -m unittest discover tests

They cover what the manual verification covered while the tools were built: the
leak list parser, the two leak tiers, every voice check on planted text, the
dictionary and jargon handling the slip planner relies on, the typo classifier,
the redactor, and the two guards that stop the scraper writing where it should not.
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))

import voicecheck as vc                 # noqa: E402
import slipplan as sp                   # noqa: E402
import extract_voice_corpus as ex       # noqa: E402


def found_ids(lines):
    return set(vc.scan(lines))


class LeakList(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        self.tmp.write(
            "# overlay\n\nnotes with `not-a-term` above the heading\n\n"
            "## Leak list\n\n- `/Users/bob`\n- `XQZ`\n- `cumulus`\n- `203.0.x.x`\n"
            "- `<placeholder>`\n\n## Notes\n\n- `also-not-a-term`\n")
        self.tmp.close()
        self.saved = vc.PRIVATE
        vc.PRIVATE = self.tmp.name

    def tearDown(self):
        vc.PRIVATE = self.saved
        os.unlink(self.tmp.name)

    def terms(self):
        return {raw: rx for raw, rx in vc.leak_terms()}

    def test_only_backticks_under_the_heading_count(self):
        self.assertEqual(set(self.terms()), {"/Users/bob", "XQZ", "cumulus", "203.0.x.x"})

    def test_acronym_is_word_bounded_and_case_sensitive(self):
        xqz = self.terms()["XQZ"]
        self.assertIsNone(xqz.search("an exquisite pxqzy mix"))
        self.assertIsNotNone(xqz.search("the XQZ program"))
        self.assertIsNone(xqz.search("a xqz of passage"))

    def test_lowercase_term_is_case_insensitive(self):
        self.assertIsNotNone(self.terms()["cumulus"].search("deploy to Cumulus-4"))

    def test_path_term_has_no_leading_boundary(self):
        self.assertIsNotNone(self.terms()["/Users/bob"].search("in /Users/bob/src"))

    def test_x_octets_are_ranges(self):
        rx = self.terms()["203.0.x.x"]
        self.assertIsNotNone(rx.search("at 203.0.113.9 tonight"))
        self.assertIsNone(rx.search("at 23.0.113.9 tonight"))

    def test_scan_leaks_exempts_noreply(self):
        hits = vc.scan_leaks(["author bob <bob@users.noreply.github.com>", "ssh cumulus"],
                             vc.leak_terms())
        self.assertEqual(hits, {"cumulus": [2]})


class GenericTier(unittest.TestCase):
    def test_shapes_are_found(self):
        lines = ["mail bob@corp.com", "cd /Users/bob/x", "host 203.0.113.5",
                 "key ghp_abcdefghijklmnopqrstuvwxyz0123", "Bearer abcdefghijklmnopqrstu",
                 "-----BEGIN RSA PRIVATE KEY-----", "password: hunter2"]
        hits = vc.scan_generic(lines)
        self.assertEqual(set(hits), {"email", "home path", "ipv4", "token", "bearer",
                                     "private key", "credential"})

    def test_placeholders_and_noreply_are_not_leaks(self):
        lines = ["bob@users.noreply.github.com", "me@example.com", "user@<hostname>.local",
                 "/Users/<username>", "range 100.x.x.x"]
        self.assertEqual(vc.scan_generic(lines), {})


class VoiceChecks(unittest.TestCase):
    def test_each_planted_tell_fires(self):
        cases = {
            "emdash": "a robust — plan",
            "emoji": "done ⚠️ here",
            "british": "the colour is fine",
            "hype": "a seamless flow",
            "apostrophe": "it's fine and you're here",
            "uncontracted": "it is not for you",
            "boldnum": "the slab is **67 x 91 mm** wide",
            "titlecase": "## Printing The Body Now",
            "formal": "clone the repository in order to start",
            "arrow": "66 → 67",
            "bang": "great!",
        }
        for cid, text in cases.items():
            with self.subTest(cid):
                self.assertIn(cid, found_ids([text]))

    def test_inline_code_is_a_literal(self):
        self.assertEqual(found_ids(["the `OpenSCAD — repository` file"]), set())

    def test_namecaps_uses_jargon_file_and_skips_headings(self):
        self.assertIn("namecaps", found_ids(["export the STL from OpenSCAD"]))
        self.assertNotIn("namecaps", found_ids(["## OpenSCAD notes"]))
        self.assertNotIn("namecaps", found_ids(["export the stl from openscad"]))

    def test_long_sentence_is_counted_across_lines(self):
        words = " ".join(["word"] * 35) + "."
        two_lines = [words[:80], words[80:]]
        self.assertIn("longsentence", found_ids(two_lines))
        self.assertNotIn("longsentence", found_ids(["short one.", "and another."]))

    def test_table_and_quote_lines_are_exempt(self):
        self.assertEqual(found_ids(["| PLA — robust |", "> colour"]), set())


class Dictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real = sp.load_dict()
        cls.jargon = sp.jargon_words()

    def test_inflections_the_word_list_lacks(self):
        for w in ("flipped", "outputting", "categories", "scallops"):
            self.assertTrue(sp.is_real(w, self.real), w)

    def test_typos_are_not_real(self):
        for w in ("wokr", "htis", "disstinctive", "orientaiton"):
            self.assertFalse(sp.is_real(w, self.real), w)

    def test_jargon_and_its_plural(self):
        self.assertTrue(sp.is_real("repos", self.real))
        self.assertTrue(sp.is_jargon("readmes", self.jargon))
        self.assertFalse(sp.is_jargon("reading", self.jargon))

    def test_classifier(self):
        self.assertEqual(ex.classify_typo("wokr", self.real)[0], "swap")
        self.assertEqual(ex.classify_typo("agressive", self.real)[0], "drop")
        self.assertEqual(ex.classify_typo("coupoin", self.real)[0], "double")
        self.assertIsNone(ex.classify_typo("zzzqqq", self.real))

    def test_inventory_skips_contractions_and_repeats(self):
        typed = ["youre going to want htis", "htis is repeated", "and htis again",
                 "one wokr here"]
        _, found = ex.typo_inventory(typed, self.real)
        self.assertIn("wokr", found)
        self.assertNotIn("htis", found)      # three times: a habit, not a slip
        self.assertNotIn("youre", found)


class Redaction(unittest.TestCase):
    def test_every_shape(self):
        out = ex.redact("bob@corp.com /Users/bob ghp_abcdefghijklmnopqrstuvwxyz0123 "
                        "Bearer abcdefghijklmnopqrstu password: hunter2 "
                        "-----BEGIN RSA PRIVATE KEY----- on cumulus",
                        [("cumulus", vc.re.compile(r"\bcumulus\b", vc.re.I))])
        for gone in ("bob@corp.com", "/Users/bob", "ghp_", "abcdefghijklmnopqrstu",
                     "hunter2", "BEGIN RSA", "cumulus"):
            self.assertNotIn(gone, out)
        self.assertIn("password: [secret]", out)


class ScraperGuards(unittest.TestCase):
    def test_refuses_unignored_path_inside_a_repo(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            self.assertIsNotNone(ex.unsafe_target(os.path.join(d, "dump.txt")))
            with open(os.path.join(d, ".gitignore"), "w") as fh:
                fh.write("dump.txt\n")
            self.assertIsNone(ex.unsafe_target(os.path.join(d, "dump.txt")))

    def test_outside_a_repo_is_fine(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(ex.unsafe_target(os.path.join(d, "dump.txt")))

    def test_too_few_messages_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "corpus.txt")
            saved = ex.collect
            ex.collect = lambda: [("2026-01-01T00:00:00", "hi")]
            try:
                self.assertEqual(ex.main([out]), 1)
            finally:
                ex.collect = saved
            self.assertFalse(os.path.exists(out))

    def test_private_overlay_is_not_tracked(self):
        self.assertFalse(vc.private_is_tracked())


if __name__ == "__main__":
    unittest.main()
