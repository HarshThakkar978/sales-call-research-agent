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
- `passed`: `True` if every rule holds, otherwise `False`.
- `reasons`: a list of strings, one per broken rule. It is empty when `passed` is `True`.

Limit: the source check only proves a cited URL was fetched. `validate` never sees page text, so it cannot tell whether that page supports the sentence.

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
collecting ... collected 7 items

tests/test_validator.py::test_validate_matches_expected[SB-01] PASSED    [ 14%]
tests/test_validator.py::test_validate_matches_expected[SB-02] PASSED    [ 28%]
tests/test_validator.py::test_validate_matches_expected[SB-03] PASSED    [ 42%]
tests/test_validator.py::test_validate_matches_expected[SB-04] PASSED    [ 57%]
tests/test_validator.py::test_validate_matches_expected[SB-05] PASSED    [ 71%]
tests/test_validator.py::test_validate_matches_expected[SB-06] PASSED    [ 85%]
tests/test_validator.py::test_source_check_only_confirms_url_was_fetched PASSED [100%]

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
============================== 7 passed in 0.01s ===============================
```
