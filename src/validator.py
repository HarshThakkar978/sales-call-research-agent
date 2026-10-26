import re

HEADINGS = [
    "What the company does",
    "What changed in the last 90 days",
    "Three talking points",
]
GAP_LINE = "Not found in sources"
CLOSING_RE = re.compile(r"^Tool calls used: (\d+)$")
TOOL_CALL_BUDGET = 8

_HEADING_RE = re.compile(r"^\s*(?:#+\s*)?(?:\d+[.)]\s*)?(.+?)\s*:?\s*$")
_BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?!\()")
_URL_END_RE = re.compile(r"\((https?://[^)\s]+)\)\.?$")


def _lines(briefing_markdown):
    return [line.strip() for line in briefing_markdown.strip().splitlines() if line.strip()]


def _heading_index(line):
    match = _HEADING_RE.match(line)
    if match and match.group(1).lower() in (h.lower() for h in HEADINGS):
        return [h.lower() for h in HEADINGS].index(match.group(1).lower())
    return None


def _is_closing(line):
    return bool(CLOSING_RE.match(line))


def _sections(lines):
    """Map heading index to the body lines under it, skipping the closing line."""
    sections, current = {}, None
    for line in lines:
        idx = _heading_index(line)
        if idx is not None:
            current = idx
            sections.setdefault(idx, [])
        elif current is not None and not _is_closing(line):
            sections[current].append(line)
    return sections


def _factual_sentences(lines):
    sentences = []
    for line in lines:
        if _heading_index(line) is not None or line == GAP_LINE or _is_closing(line):
            continue
        text = _BULLET_RE.sub("", line)
        sentences.extend(s for s in _SENTENCE_SPLIT_RE.split(text) if s.strip())
    return sentences


def _check_headings(lines):
    found = [i for i in map(_heading_index, lines) if i is not None]
    reasons = []
    for i, heading in enumerate(HEADINGS):
        if i not in found:
            reasons.append(f"missing heading: {heading}")
    if not reasons and found != sorted(found):
        reasons.append("headings are not in the required order")
    return reasons


def _check_sections_present(lines):
    # A section holding only the exact gap line has content, so it is present.
    reasons = []
    sections = _sections(lines)
    for i, heading in enumerate(HEADINGS):
        if i in sections and not sections[i]:
            reasons.append(f"section is empty: {heading}")
    return reasons


def _check_sources(lines, fetched_urls):
    reasons = []
    fetched = set(fetched_urls)
    for sentence in _factual_sentences(lines):
        match = _URL_END_RE.search(sentence)
        if not match:
            reasons.append(f"no source URL at end of sentence: {sentence}")
        elif match.group(1) not in fetched:
            reasons.append(f"source URL was never fetched: {match.group(1)}")
    return reasons


def _check_closing(lines):
    if not lines:
        return ["missing closing tool call line"]
    match = CLOSING_RE.match(lines[-1])
    if not match:
        return ["last line is not the closing tool call line"]
    used = int(match.group(1))
    if used > TOOL_CALL_BUDGET:
        return [f"tool calls used {used} exceeds budget of {TOOL_CALL_BUDGET}"]
    return []


def validate(briefing_markdown, fetched_urls):
    lines = _lines(briefing_markdown)
    reasons = (
        _check_headings(lines)
        + _check_sections_present(lines)
        + _check_sources(lines, fetched_urls)
        + _check_closing(lines)
    )
    return (not reasons, reasons)
