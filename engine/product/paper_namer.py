import re
from engine.product.models import Group

_SUBJECT_HINTS = [
    "subject",
    "course",
    "course code",
    "paper",
    "examination",
    "title",
    "name of the paper",
    "paper name",
    "subject name",
    "branch",
]

_KNOWN_SUBJECTS = [
    "pharmacology",
    "engineering mathematics",
    "computer networks",
    "operating systems",
    "data structures",
    "database management systems",
    "machine learning",
    "artificial intelligence",
    "digital electronics",
    "software engineering",
    "computer graphics",
    "physics",
    "chemistry",
    "mathematics",
    "pathology",
    "microbiology",
    "forensic medicine",
    "community medicine",
    "anatomy",
    "physiology",
    "biochemistry",
    "general medicine",
    "general surgery",
    "pediatrics",
    "obstetrics and gynecology",
    "ophthalmology",
    "ent",
    "orthopedics",
    "dermatology",
    "psychiatry",
    "radiology",
    "anesthesiology",
    "immunology",
    "genetics",
    "cell biology",
    "molecular biology",
    "bioinformatics",
    "statistics",
    "probability",
    "linear algebra",
    "calculus",
    "discrete mathematics",
    "numerical analysis",
    "design and analysis of algorithms",
    "theory of computation",
    "compiler design",
    "computer architecture",
    "microprocessors",
    "embedded systems",
    "vlsi design",
    "power systems",
    "control systems",
    "signal processing",
    "communication engineering",
    "digital signal processing",
    "python programming",
    "java programming",
    "c programming",
    "object oriented programming",
    "database management",
    "data mining",
    "web technologies",
    "cloud computing",
    "cyber security",
    "network security",
    "cryptography",
    "blockchain technology",
    "internet of things",
    "computer graphics and visualization",
    "human computer interaction",
    "management information systems",
    "financial management",
    "accounting",
    "economics",
    "business statistics",
    "organizational behavior",
    "marketing management",
    "human resource management",
    "operations research",
    "supply chain management",
    "engineering mechanics",
    "fluid mechanics",
    "thermodynamics",
    "heat transfer",
    "machine design",
    "manufacturing processes",
    "material science",
    "structural analysis",
    "reinforced concrete design",
    "steel structures",
    "geotechnical engineering",
    "transportation engineering",
    "environmental engineering",
    "water resources engineering",
    "surveying",
    "construction management",
]

_REMOVE_PREFIXES = re.compile(
    r"^(subject|course|paper|code|title|name)\s*[:\-.]?\s*",
    re.IGNORECASE,
)

_TRAILING_JUNK = re.compile(r"[:\-.\s]+$")

_WHITESPACE = re.compile(r"\s+")

_UNIVERSITY_KEYWORDS = [
    "university",
    "institute of technology",
    "institute of",
    "college of",
    "academy of",
]

_NUMBER_ONLY = re.compile(r"^\d+$")

_ISO_DATE = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}$")

_SLASH_DATE = re.compile(r"^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$")

_DATE_PATTERN = re.compile(
    r"^(january|february|march|april|may|june|july|august|september|october|november|december)"
    r"\s+\d{4}$",
    re.IGNORECASE,
)


def _clean_candidate(text: str) -> str | None:
    text = _WHITESPACE.sub(" ", text).strip()

    # Remove common prefixes iteratively (handles "paper name:" -> "Advanced Topics").
    while True:
        m = _REMOVE_PREFIXES.match(text)
        if not m:
            break
        text = text[m.end() :].strip()

    # Remove trailing junk.
    text = _TRAILING_JUNK.sub("", text).strip()

    if not text:
        return None

    if len(text) < 3:
        return None

    if _NUMBER_ONLY.match(text):
        return None

    if _DATE_PATTERN.match(text):
        return None

    if _ISO_DATE.match(text):
        return None

    if _SLASH_DATE.match(text):
        return None

    # Reject university names.
    lower = text.lower()
    for kw in _UNIVERSITY_KEYWORDS:
        if kw in lower:
            return None

    return text


def _score_subject_match(text: str) -> tuple[str, int] | None:
    lower = text.lower()
    for known in _KNOWN_SUBJECTS:
        if known in lower:
            # Prefer exact(-ish) match — the known subject is a substantial
            # portion of the candidate.
            score = len(known) * 2
            return (known, score)

    return None


def _find_best_line(lines: list[str]) -> str | None:
    best_candidate: str | None = None
    best_score = 0

    for line in lines:
        trimmed = line.strip()
        if not trimmed:
            continue

        lower = trimmed.lower()

        # Check for subject hint keywords BEFORE prefix removal
        # so 'paper name: ...' still matches.
        has_hint = any(
            hint in lower
            for hint in _SUBJECT_HINTS
        )

        # Check known subject match before cleaning too.
        subject_score = 0
        matched: str | None = None
        for known in _KNOWN_SUBJECTS:
            if known in lower:
                subject_score = len(known) * 2
                matched = known
                break

        score = (
            (50 if has_hint else 0)
            + subject_score
        )

        if score <= best_score:
            continue

        cleaned = _clean_candidate(line)
        if cleaned is None:
            continue

        best_score = score
        if matched:
            best_candidate = matched
        elif has_hint:
            best_candidate = cleaned

    return best_candidate


def name_group(group: Group, fallback_index: int) -> str:
    """Assign a human-readable name to a group using OCR heuristics.

    Returns the assigned name (sets ``group.paper_name`` as a side effect).
    """
    # Collect OCR lines from the first page of the group.
    if not group.pages:
        fallback_name = f"Unknown Paper {fallback_index}"
        group.paper_name = fallback_name
        return fallback_name

    first_page = group.pages[0]
    lines = first_page.ocr_text.split("\n")

    # Limit to first 30 lines.
    lines = [l.strip() for l in lines[:30] if l.strip()]

    best = _find_best_line(lines)

    if best:
        name = best.title()
        group.paper_name = name
        return name

    fallback_name = f"Unknown Paper {fallback_index}"
    group.paper_name = fallback_name
    return fallback_name


def name_groups(groups: list[Group]) -> list[Group]:
    """Assign names to all groups in-place."""
    # First pass: track used names for duplicate handling.
    used: dict[str, int] = {}
    fallback_counter = 1

    for group in groups:
        fallback_index = fallback_counter

        name_group(group, fallback_index)

        name = group.paper_name
        if name.startswith("Unknown Paper"):
            fallback_counter += 1
            continue

        if name.lower() in used:
            used[name.lower()] += 1
            group.paper_name = f"{name} ({used[name.lower()]})"
        else:
            used[name.lower()] = 1

    return groups
