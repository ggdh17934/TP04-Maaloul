import importlib.util
import math
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("analysis", Path(__file__).parents[1] / "app" / "analyze.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class AnalysisTests(unittest.TestCase):
    def test_chunks_preserve_first_last_and_missing_values(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "tiny.csv"
            rows = []
            for value in range(1, 6):
                row = [str(value)] * 29
                if value == 3:
                    row[1] = ""
                rows.append(",".join(row))
            source.write_text("\n".join(rows) + "\n", encoding="utf-8")
            result = app.analyze(source, chunksize=2)
            self.assertEqual(result["rows"], 5)
            self.assertEqual(result["metrics"]["label"]["sum"], 15)
            self.assertEqual(result["metrics"]["lepton_pt"]["valid_count"], 4)
            self.assertEqual(result["metrics"]["lepton_pt"]["missing_count"], 1)
            self.assertTrue(math.isclose(result["metrics"]["lepton_pt"]["mean"], 3))
    def test_invalid_column_count_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bad.csv"
            source.write_text("1,2,3\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "29 fields"):
                app.analyze(source)
    def test_zero_chunksize_rejected(self):
        with self.assertRaises(ValueError):
            app.analyze("unused.csv", 0)

if __name__ == "__main__":
    unittest.main()
