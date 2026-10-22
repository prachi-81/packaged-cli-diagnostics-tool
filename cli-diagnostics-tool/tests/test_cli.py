
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from envdoctor.cli import collect_diagnostics, main


class DiagnosticsTests(unittest.TestCase):

    def test_collect_diagnostics(self):
        data = collect_diagnostics()

        self.assertIn("python_version", data)
        self.assertIn("disk_space", data)
        self.assertIn("developer_tools", data)
        self.assertIn("environment_variables", data)

    @patch("envdoctor.cli.shutil.which", return_value=None)
    def test_missing_developer_tools(self, mock_which):
        data = collect_diagnostics()

        self.assertTrue(
            all(value is False
                for value in data["developer_tools"].values())
        )

    def test_json_output(self):
        with patch("envdoctor.cli.collect_diagnostics") as mock_data:
            mock_data.return_value = {
                "python_version": "3.14.0",
                "operating_system": "Windows",
                "disk_space": {
                    "total_bytes": 1000,
                    "free_bytes": 500,
                },
                "environment_variables": {},
                "developer_tools": {},
            }

            with patch("sys.argv", ["envdoctor", "--json"]):
                with patch("builtins.print") as mock_print:
                    result = main()

        self.assertEqual(result, 0)
        printed = mock_print.call_args_list[0].args[0]
        parsed = json.loads(printed)
        self.assertEqual(parsed["python_version"], "3.14.0")

    def test_output_to_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "report.txt"

            with patch("sys.argv", [
                "envdoctor", "--output", str(output_file)
            ]):
                with patch("builtins.print"):
                    result = main()

            self.assertEqual(result, 0)
            self.assertTrue(output_file.exists())
            self.assertIn(
                "DEVELOPER ENVIRONMENT HEALTH REPORT",
                output_file.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
