"""Offline checks: python -m unittest -v test_flow.py (not run in this session)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import dbt_learning as flow


class WorkflowTests(unittest.TestCase):
    def test_url_boundaries(self):
        self.assertIsNone(flow.canonical('https://example.org/docs/a'))
        self.assertIsNone(flow.canonical('http://docs.getdbt.com/docs/a'))
        self.assertIsNone(flow.canonical('https://docs.getdbt.com/img/logo.png'))
        self.assertEqual(flow.canonical('https://docs.getdbt.com/docs/a/?x=y#h'),
                         'https://docs.getdbt.com/docs/a.md')

    def test_no_source_text_lost(self):
        text = ('alpha\n```sql\nselect 1;\n```\n' * 2000) + 'last line'
        parts = list(flow.split_text(text))
        self.assertEqual(''.join(parts), text)
        self.assertTrue(all(len(part) <= 16000 for part in parts))

    def test_discovery_deduplicates(self):
        class FakeFetcher:
            def get(self, url):
                if url.endswith('llms.txt'):
                    return '[Models](https://docs.getdbt.com/docs/build/models.md)'
                return ('<urlset><url><loc>https://docs.getdbt.com/docs/build/models</loc></url>'
                        '<url><loc>https://docs.getdbt.com/docs/build/tests</loc></url>'
                        '<url><loc>https://example.org/unrelated</loc></url></urlset>')
        with tempfile.TemporaryDirectory() as directory, patch.object(flow, 'DATA', Path(directory)):
            inventory, issues = flow.discover(FakeFetcher())
        self.assertEqual(len(inventory), 2)
        self.assertEqual(issues, [])

    def test_failed_pages_remain_visible(self):
        rows = {'a': {'url': 'a', 'status': 'ok', 'in_current_inventory': True},
                'b': {'url': 'b', 'status': 'error', 'in_current_inventory': True},
                'c': {'url': 'c', 'status': 'ok', 'in_current_inventory': False}}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.multiple(flow, DATA=root / 'data', IMPORTS=root / 'imports'):
                report = flow.coverage(rows)
        self.assertEqual(report['statuses'], {'ok': 1, 'error': 1})
        self.assertEqual([r['url'] for r in report['uncollected']], ['b'])
        self.assertEqual(report['removed_from_inventory'], ['c'])


if __name__ == '__main__':
    unittest.main()
