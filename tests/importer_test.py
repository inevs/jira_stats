import unittest

from jira_stats.jira_importer import Importer


class MyTestCase(unittest.TestCase):
    def test_convert_transition(self):
        created = "2023-12-05T08:44:39.082+0100"
        status_change = {
            "field": "status",
            "fieldtype": "jira",
            "from": "1",
            "fromString": "Open",
            "to": "10204",
            "toString": "In Analysis Development"
        }
        config = {"open":["In Analysis Development"]}
        importer = Importer(config=config)
        transition = importer.convert_transition(created, status_change)
        self.assertEqual(transition.timestamp, created)
        self.assertEqual(transition.from_state, "Open")
        self.assertEqual(transition.to_state, "In Analysis Development")
        self.assertEqual(transition.transition_type, "open")


if __name__ == '__main__':
    unittest.main()
