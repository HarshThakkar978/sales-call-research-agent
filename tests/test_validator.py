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


ACME = (
    "## What the company does\n"
    "Acme makes anvils for roadrunner trapping (https://acme.com/about).\n"
    "## What changed in the last 90 days\n"
    "Not found in sources\n"
    "## Three talking points\n"
    "1. Acme makes anvils, so ask about anvil demand (https://acme.com/about).\n"
    "Tool calls used: 3"
)


def test_fetched_url_with_unrelated_page_text_is_rejected():
    page_text = {"https://acme.com/about": "We bake sourdough bread and cakes daily."}
    passed, reasons = validate(ACME, ["https://acme.com/about"], page_text)
    print(f"unrelated page text: passed={passed} reasons={reasons}")
    assert not passed
    assert any("cited page does not support sentence" in r for r in reasons)


def test_fetched_url_with_supporting_page_text_passes():
    page_text = {"https://acme.com/about": "Acme makes anvils used for roadrunner trapping."}
    passed, reasons = validate(ACME, ["https://acme.com/about"], page_text)
    assert passed, reasons
