from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase

@patch('scraper.management.commands.runscraper.CrawlTaskHandler.run_spider')
@patch(
    'scraper.management.commands.runscraper.CrawlTaskHandler.__init__',
    return_value=None
)
class RunScraperCommandTest(SimpleTestCase):

    def setUp(self):
        self.out = StringIO()

    def test_runscraper_without_args(self, mock_init, mock_run):
        call_command('runscraper', stdout=self.out)
        self.assertTrue(mock_init.called)
        self.assertTrue(mock_run.called)
        self.assertIn('current year', self.out.getvalue())
        with self.assertRaises(AssertionError):
            mock_init.assert_called_with(year=2019)

    def test_runscraper_with_args(self, mock_init, mock_run):
        year = 2018
        call_command('runscraper', year=year, stdout=self.out)
        self.assertTrue(mock_init.called)
        self.assertTrue(mock_run.called)
        self.assertNotIn('current year', self.out.getvalue())
        self.assertIn(str(year), self.out.getvalue())
        self.assertTrue(mock_init.called)
        _, kwargs = mock_init.call_args
        self.assertEqual(kwargs.get('input'), 'inputargument')
        self.assertEqual(kwargs.get('year'), year)
