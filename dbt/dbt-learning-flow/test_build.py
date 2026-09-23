import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import dbt_learning as flow


class BuildTests(unittest.TestCase):
    def test_packets_preserve_content_but_exclude_listings_and_exact_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = 'A detailed explanation of state comparison.\n' * 1000
            manifest = {}
            for name, route, body in [('state', '/reference/state', text),
                                     ('duplicate', '/reference/copy', text),
                                     ('author', '/blog/authors/example', 'Author biography. ' * 100),
                                     ('tag', '/tags/example', 'Tag listing. ' * 100)]:
                file = root / 'data' / 'pages' / (name + '.md')
                flow.save(file, body)
                url = flow.BASE + route + '.md'
                manifest[url] = {'url': url, 'title': name, 'status': 'ok',
                                 'in_current_inventory': True, 'fetched_at': '2026-09-22',
                                 'file': file.relative_to(root).as_posix()}
            flow.save_json(root / 'data' / 'manifest.json', manifest)
            with patch.multiple(flow, ROOT=root, DATA=root / 'data', GUIDE=root / 'guide', IMPORTS=root / 'imports'):
                flow.build(None)
            excluded = flow.read_json(root / 'guide' / 'excluded-from-study.json', [])
            self.assertEqual(len(excluded), 3)
            packets = flow.read_json(root / 'guide' / 'packets.json', [])
            self.assertGreater(len(packets), 1)
            self.assertTrue(all(p['topic'] == '08-state' for p in packets))
            sources = flow.read_json(root / 'guide' / 'sources.json', [])
            self.assertEqual(len(sources), 1)

    def test_short_markdown_uses_html_instead_of_silently_discarding_page(self):
        class Fetch:
            def get(self, url):
                if url.endswith('.md'):
                    return '# FAQs'
                return '<main><h1>FAQs</h1><p>' + 'Useful content. ' * 20 + '</p></main>'
        body, url, fmt = flow.fetch_document(Fetch(), flow.BASE + '/docs/faqs.md')
        self.assertIn('Useful content.', body)
        self.assertEqual(fmt, 'html-extracted')
        self.assertEqual(url, flow.BASE + '/docs/faqs')


if __name__ == '__main__':
    unittest.main()
