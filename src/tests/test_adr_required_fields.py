from contextlib import redirect_stdout
from io import StringIO
from unittest import TestCase

from lab8.check_submission import Report, _check_adr


class TestAdrRequiredFields(TestCase):
    def test_blank_run_id_is_reported_as_a_failure(self):
        adr = """- Shape chọn: workflow
- Commit hash: `f1595d5`
- Run id dẫn chứng:
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0
- Cost per success (mô phỏng, VND): 28.80
- Crash safety: 20/20
- Secret leak / approval bypass: 0 / 0
"""
        report = Report()
        output = StringIO()

        with redirect_stdout(output):
            _check_adr(report, adr)

        self.assertEqual(report.fails, 1)
        self.assertIn("'Run id dẫn chứng' còn trống", output.getvalue())
