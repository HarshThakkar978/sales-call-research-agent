# Sales Call Research Agent

## Briefing Contract

Three sections, in this order:

```
1. What the company does
2. What changed in the last 90 days
3. Three talking points
```

Four rules:

```
1. Every factual sentence ends with a source URL in parentheses.
2. A gap gets one exact line: Not found in sources
3. The briefing ends with a closing line: Tool calls used: N
4. The budget is 8 tool calls
```

A section that contains only the gap line counts as present, and the gap line needs no source URL.

The two exact lines are `Not found in sources` (no period) and `Tool calls used: N`, where N is a whole number of 8 or less. The validator in `src/validator.py` matches them word for word, so use them exactly.

## Validator inputs and output

```
validate(briefing_markdown, fetched_urls) -> (passed, reasons)
```

- `briefing_markdown`: the briefing text, as one string.
- `fetched_urls`: a list of the URLs the agent actually fetched. A source URL in the briefing that is not in this list is rejected.
- `page_text` (optional): a dict of URL to the text of that page. When a cited URL has text here, at least half of the claim's key terms must appear in it, otherwise the sentence is rejected. The advice after ", so " in a talking point is not part of the claim.
- `passed`: `True` if every rule holds, otherwise `False`.
- `reasons`: a list of strings, one per broken rule. It is empty when `passed` is `True`.

Limit: without `page_text`, the source check only proves a cited URL was fetched. With it, the check is a key-term overlap, so it catches a citation on the wrong page but not a subtle misreading of the right page.

## Developer usage

```python
from src.validator import validate

passed, reasons = validate(briefing_markdown, fetched_urls)
if not passed:
    print(reasons)
```

Run the tests:

```
pip install -r requirements.txt
pytest -v -rP
```

## Rep usage

## Run record

Command: `pytest -v -rP`. The `-rP` flag prints the validator's reasons for every row, including rows that pass.

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Users/harsh/sales-call-research-agent/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/harsh/sales-call-research-agent
configfile: pytest.ini
collecting ... collected 9 items

tests/test_validator.py::test_validate_matches_expected[SB-01] PASSED    [ 11%]
tests/test_validator.py::test_validate_matches_expected[SB-02] PASSED    [ 22%]
tests/test_validator.py::test_validate_matches_expected[SB-03] PASSED    [ 33%]
tests/test_validator.py::test_validate_matches_expected[SB-04] PASSED    [ 44%]
tests/test_validator.py::test_validate_matches_expected[SB-05] PASSED    [ 55%]
tests/test_validator.py::test_validate_matches_expected[SB-06] PASSED    [ 66%]
tests/test_validator.py::test_source_check_only_confirms_url_was_fetched PASSED [ 77%]
tests/test_validator.py::test_fetched_url_with_unrelated_page_text_is_rejected PASSED [ 88%]
tests/test_validator.py::test_fetched_url_with_supporting_page_text_passes PASSED [100%]

==================================== PASSES ====================================
____________________ test_validate_matches_expected[SB-01] _____________________
----------------------------- Captured stdout call -----------------------------
SB-01 passed=True reasons=[]
____________________ test_validate_matches_expected[SB-02] _____________________
----------------------------- Captured stdout call -----------------------------
SB-02 passed=True reasons=[]
____________________ test_validate_matches_expected[SB-03] _____________________
----------------------------- Captured stdout call -----------------------------
SB-03 passed=True reasons=[]
____________________ test_validate_matches_expected[SB-04] _____________________
----------------------------- Captured stdout call -----------------------------
SB-04 passed=False reasons=['missing heading: What changed in the last 90 days']
____________________ test_validate_matches_expected[SB-05] _____________________
----------------------------- Captured stdout call -----------------------------
SB-05 passed=False reasons=['no source URL at end of sentence: Mailchimp has been part of Intuit since its acquisition in 2021.']
____________________ test_validate_matches_expected[SB-06] _____________________
----------------------------- Captured stdout call -----------------------------
SB-06 passed=False reasons=['source URL was never fetched: https://www.canva.com/enterprise/']
____________ test_fetched_url_with_unrelated_page_text_is_rejected _____________
----------------------------- Captured stdout call -----------------------------
unrelated page text: passed=False reasons=['cited page does not support sentence: Acme makes anvils for roadrunner trapping (https://acme.com/about).', 'cited page does not support sentence: Acme makes anvils, so ask about anvil demand (https://acme.com/about).']
============================== 9 passed in 0.01s ===============================
```
