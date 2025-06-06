from django.test import TestCase

from codex.imports.csv import parse_classes


class CSVImportParserTest(TestCase):
    """Tests for the import parser functions"""

    def test_parse_classes_single(self):
        test_class_1 = {"name": "Wizard", "subclass": "Abjuration", "value": 10}
        test_class_2 = {"name": "Fighter", "subclass": "", "value": 3}
        test_class_3 = {"name": "Sorcerer", "subclass": "Draconic Red", "value": 15}

        self.assertEqual(parse_classes("Wizard (Abjuration) 10"), [test_class_1])
        self.assertEqual(parse_classes("Fighter - 3"), [test_class_2])
        self.assertEqual(parse_classes("3 Fighter"), [test_class_2])
        self.assertEqual(parse_classes("sorcerer (draconic - red) 15"), [test_class_3])

    def test_parse_classes_multiple(self):
        test_class_1 = {"name": "Sorcerer", "subclass": "Wild Magic", "value": 5}
        test_class_2 = {"name": "Paladin", "subclass": "", "value": 1}

        classes = parse_classes("Paladin / 5 Sorcerer (Wild magic)")
        self.assertEqual(classes[1], test_class_1)
        self.assertEqual(classes[0], test_class_2)
