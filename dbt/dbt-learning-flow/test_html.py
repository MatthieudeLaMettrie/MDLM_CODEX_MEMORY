import unittest
from urllib.error import HTTPError
import dbt_learning as flow


class HtmlTests(unittest.TestCase):
    def test_content_and_code_survive_navigation_is_removed(self):
        html = ('<html><nav>UNWANTED_NAV</nav><main><article><h1>Example</h1>'
                '<p>' + 'Detailed explanation. ' * 10 + '</p>'
                '<pre><code>select 1;\nselect 2;</code></pre>'
                '<script>UNWANTED_SCRIPT</script></article></main></html>')
        text = flow.extract_html(html, 'https://docs.getdbt.com/blog/example')
        self.assertIn('# Example', text)
        self.assertIn('select 1;\nselect 2;', text)
        self.assertNotIn('UNWANTED', text)
        self.assertEqual(text.count('```'), 2)

    def test_404_falls_back_and_records_real_source(self):
        class FakeFetcher:
            def get(self, url):
                if url.endswith('.md'):
                    raise HTTPError(url, 404, 'missing', {}, None)
                return '<main><h1>Article</h1><p>' + 'Evidence. ' * 20 + '</p></main>'
        body, url, fmt = flow.fetch_document(FakeFetcher(), 'https://docs.getdbt.com/blog/example.md')
        self.assertEqual(url, 'https://docs.getdbt.com/blog/example')
        self.assertEqual(fmt, 'html-extracted')
        self.assertIn('Evidence.', body)

    def test_authentication_error_does_not_trigger_fallback(self):
        class FakeFetcher:
            def get(self, url):
                raise HTTPError(url, 403, 'forbidden', {}, None)
        with self.assertRaises(HTTPError):
            flow.fetch_document(FakeFetcher(), 'https://docs.getdbt.com/example.md')


if __name__ == '__main__':
    unittest.main()
