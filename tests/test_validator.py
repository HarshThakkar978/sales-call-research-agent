import json
from pathlib import Path

import pytest

from src.validator import validate

ROWS = json.loads((Path(__file__).parent / "briefings.json").read_text())


@pytest.mark.parametrize("row", ROWS, ids=[r["sample_id"] for r in ROWS])
def test_validate_matches_expected(row):
    passed, reasons = validate(row["briefing_markdown"], list(row["fetched_urls"]))
    print(f"{row['sample_id']} passed={passed} reasons={reasons}")
    assert passed == row["expected_valid"], (
        f"{row['sample_id']} expected {row['expected_valid']}, reasons: {reasons}\n"
        f"{row['briefing_markdown']}"
    )


def test_source_check_only_confirms_url_was_fetched():
    # Known limit: validate sees URLs, not page text. A fetched URL passes even
    # if that page never said what the sentence claims.
    briefing = (
        "## What the company does\n"
        "Acme makes anvils (https://acme.com/about).\n"
        "## What changed in the last 90 days\n"
        "Acme acquired a rocket company last month (https://acme.com/about).\n"
        "## Three talking points\n"
        "1. Ask about anvil demand (https://acme.com/about).\n"
        "Tool calls used: 3"
    )
    passed, _ = validate(briefing, ["https://acme.com/about"])
    assert passed
    passed, reasons = validate(briefing, [])
    assert not passed and any("never fetched" in r for r in reasons)
