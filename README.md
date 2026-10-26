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
2. A gap gets one exact line, for example: Not found in sources.
3. The briefing ends with a closing line stating total tool calls used
4. The budget is 8 tool calls
```

Code matches this wording word for word, so pick it once and never vary it.

## Usage

## Run record

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0 -- /Users/harsh/sales-call-research-agent/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/harsh/sales-call-research-agent
configfile: pytest.ini
collecting ... collected 6 items

tests/test_validator.py::test_validate_matches_expected[SB-01] PASSED    [ 16%]
tests/test_validator.py::test_validate_matches_expected[SB-02] PASSED    [ 33%]
tests/test_validator.py::test_validate_matches_expected[SB-03] PASSED    [ 50%]
tests/test_validator.py::test_validate_matches_expected[SB-04] PASSED    [ 66%]
tests/test_validator.py::test_validate_matches_expected[SB-05] PASSED    [ 83%]
tests/test_validator.py::test_validate_matches_expected[SB-06] PASSED    [100%]

============================== 6 passed in 0.01s ===============================
```
