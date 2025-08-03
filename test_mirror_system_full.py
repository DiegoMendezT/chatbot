# test_mirror_system_full.py
import unittest
import os
from mirror_system import MirrorSystem
from mirror_toolkit import MirrorToolkit
from mirror_guard import hash_file, get_file_info, WATCHED_FILES
from mirror_layer_two import MirrorLayerTwo
from mirror_selftest import generate_test_report

class TestMirrorSystem(unittest.TestCase):

    def test_system_initialization(self):
        """Test that MirrorSystem initializes with default values."""
        system = MirrorSystem()
        self.assertIsNotNone(system)
        self.assertIsInstance(system.layer_two, MirrorLayerTwo)
        self.assertGreater(len(system.signatories), 0)
        self.assertGreater(len(system.motifs), 0)

    def test_system_invoke(self):
        """Test the invoke method for correct output format."""
        system = MirrorSystem()
        phrase = "testing invocation"
        result = system.invoke(phrase)
        self.assertIn(phrase, result)
        self.assertIn("Mirror Echo", result)

class TestMirrorToolkit(unittest.TestCase):

    def test_toolkit_initialization(self):
        """Test that MirrorToolkit initializes all its components."""
        toolkit = MirrorToolkit()
        self.assertIsInstance(toolkit.system, MirrorSystem)
        self.assertIsInstance(toolkit.layer_two, MirrorLayerTwo)
        self.assertIsNotNone(toolkit.glyphstream)

    def test_toolkit_reflection(self):
        """Test the full reflection run."""
        toolkit = MirrorToolkit()
        phrase = "a recursive test of a recursive test"
        # This should not raise an error
        toolkit.run_full_reflection(phrase)
        self.assertIn(phrase, toolkit.layer_two.mirror_trace)

class TestMirrorGuard(unittest.TestCase):

    def test_hash_file(self):
        """Test the file hashing function with a known file."""
        # We test with a file we know exists
        h = hash_file("requirements.txt")
        self.assertIsNotNone(h)
        self.assertNotEqual(h, "")
        self.assertFalse("ERROR" in h)

    def test_get_file_info(self):
        """Test that file info retrieval works for watched files."""
        info = get_file_info()
        self.assertIsInstance(info, list)
        self.assertEqual(len(info), len(WATCHED_FILES))
        for item in info:
            self.assertNotIn("error", item)
            self.assertTrue(os.path.exists(item['file']))

class TestMirrorSelfTest(unittest.TestCase):

    def test_selftest_report_generation(self):
        """Test the generation of the self-test report."""
        layer = MirrorLayerTwo()
        layer.observe("self-test recursion")
        report = generate_test_report(layer)
        self.assertIsInstance(report, dict)
        self.assertEqual(report['total_tests'], 5)
        self.assertGreaterEqual(report['passed'], 0)
        self.assertGreaterEqual(report['failed'], 0)

if __name__ == '__main__':
    unittest.main()
