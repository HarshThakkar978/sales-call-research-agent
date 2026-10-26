import json
from pathlib import Path

import pytest

from src.validator import validate

ROWS = json.loads((Path(__file__).parent / "briefings.json").read_text())


@pytest.mark.parametrize("row", ROWS, ids=[r["sample_id"] for r in ROWS])
def test_validate_matches_expected(row):
    passed, reasons = validate(row["briefing_markdown"], list(row["fetched_urls"]))
    assert passed == row["expected_valid"], (
        f"{row['sample_id']} expected {row['expected_valid']}, reasons: {reasons}\n"
        f"{row['briefing_markdown']}"
    )
