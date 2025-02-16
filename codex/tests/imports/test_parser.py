from django.test import TestCase

from codex.imports.csv import parse_classes


class CSVImportParserTest(TestCase):
    """Tests for the import parser functions"""

    def test_parse_classes(self):
        test_class_1 = {"class": "Wizard", "subclass": "Abjuration", "level": 10}

        self.assertEqual(parse_classes("Wizard (Abjuration) 10"), test_class_1)
