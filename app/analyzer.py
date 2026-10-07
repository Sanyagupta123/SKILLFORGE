from __future__ import annotations

import re
from typing import Iterable

SKILL_LIBRARY: dict[str, dict[str, str | list[str]]] = {
    "Python": {"category": "Programming", "aliases": ["python"]},
    "JavaScript": {"category": "Programming", "aliases": ["javascript", "js", "java script"]},
    "Java": {"category": "Programming", "aliases": ["java"]},
    "TypeScript": {"category": "Programming", "aliases": ["typescript", "ts"]},
    "C#": {"category": "Programming", "aliases": ["c#", "c sharp", "csharp"]},
    "FastAPI": {"category": "Backend", "aliases": ["fastapi", "fast api"]},
    "Node.js": {"category": "Backend", "aliases": ["node.js", "nodejs", "node js"]},
    "REST APIs": {"category": "Backend", "aliases": ["rest api", "rest apis", "restful api"]},
    "React": {"category": "Frontend", "aliases": ["react", "reactjs", "react js"]},
    "PostgreSQL": {"category": "Database", "aliases": ["postgresql", "postgres", "postgre sql"]},
    "MySQL": {"category": "Database", "aliases": ["mysql"]},
    "MongoDB": {"category": "Database", "aliases": ["mongodb", "mongo"]},
    "Redis": {"category": "Database", "aliases": ["redis"]},
    "SQL": {"category": "Database", "aliases": ["sql"]},
    "Docker": {"category": "DevOps", "aliases": ["docker"]},
    "Kubernetes": {"category": "DevOps", "aliases": ["kubernetes", "k8s", "kube"]},
    "AWS": {"category": "Cloud", "aliases": ["aws", "amazon web services"]},
    "Azure": {"category": "Cloud", "aliases": ["azure"]},
    "GCP": {"category": "Cloud", "aliases": ["gcp", "google cloud"]},
    "Git": {"category": "Tools", "aliases": ["git", "github"]},
    "Machine Learning": {"category": "AI/ML", "aliases": ["machine learning", "ml"]},
    "Deep Learning": {"category": "AI/ML", "aliases": ["deep learning", "dl"]},
    "NLP": {"category": "AI/ML", "aliases": ["nlp", "natural language processing"]},
}

SKILL_CATEGORIES = {canonical: data["category"] for canonical, data in SKILL_LIBRARY.items()}


def normalize_alias(value: str) -> str:
    cleaned = str(value).lower()
    cleaned = cleaned.replace("#", " ")
    cleaned = re.sub(r"[^a-z0-9.]+", " ", cleaned)
    cleaned = cleaned.replace(".", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _build_alias_map() -> dict[str, str]:
    alias_map: dict[str, str] = {}
    for canonical, data in SKILL_LIBRARY.items():
        aliases = list(data["aliases"]) + [canonical]
        for alias in aliases:
            normalized = normalize_alias(alias)
            if normalized:
                alias_map[normalized] = canonical
    return alias_map


ALIASES = _build_alias_map()


def normalize_skill_name(value: str) -> str:
    if value is None:
        return ""
    normalized = normalize_alias(value)
    if not normalized:
        return ""
    return ALIASES.get(normalized, normalized.title())


def _tokenize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize_alias(value))


def extract_skills(text: str | None) -> list[str]:
    if text is None or not str(text).strip():
        return []

    normalized_text = normalize_alias(str(text))
    if not normalized_text:
        return []

    matches: list[tuple[int, str]] = []
    for alias, canonical in sorted(ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
        for match in re.finditer(pattern, normalized_text):
            matches.append((match.start(), canonical))

    ordered = sorted(matches, key=lambda item: item[0])
    seen: set[str] = set()
    found: list[str] = []
    for _, canonical in ordered:
        if canonical not in seen:
            found.append(canonical)
            seen.add(canonical)
    return found


def analyze_text(text: str | None) -> list[str]:
    return extract_skills(text)


def calculate_matching(required: Iterable[str], candidate: Iterable[str]) -> dict[str, object]:
    required_items = [normalize_skill_name(skill) for skill in required if normalize_skill_name(skill)]
    candidate_set = {normalize_skill_name(skill) for skill in candidate if normalize_skill_name(skill)}

    unique_required: list[str] = []
    seen_required: set[str] = set()
    for skill in required_items:
        if skill and skill not in seen_required:
            unique_required.append(skill)
            seen_required.add(skill)

    matched = [skill for skill in unique_required if skill in candidate_set]
    missing = [skill for skill in unique_required if skill not in candidate_set]
    score = round((len(matched) / len(unique_required) * 100), 2) if unique_required else 0.0

    return {"matched": matched, "missing": missing, "score": score}


def calculate_category_coverage(required_skills: Iterable[str], matched_skills: Iterable[str]) -> dict[str, float]:
    normalized_required = [normalize_skill_name(skill) for skill in required_skills if normalize_skill_name(skill)]
    normalized_matched = {normalize_skill_name(skill) for skill in matched_skills if normalize_skill_name(skill)}

    totals: dict[str, int] = {}
    matched_counts: dict[str, int] = {}
    for skill in normalized_required:
        category = SKILL_CATEGORIES.get(skill, "General")
        totals[category] = totals.get(category, 0) + 1
        if skill in normalized_matched:
            matched_counts[category] = matched_counts.get(category, 0) + 1

    coverage: dict[str, float] = {}
    for category, total in totals.items():
        coverage[category] = round((matched_counts.get(category, 0) / total) * 100, 2) if total else 0.0

    return coverage


def generate_recommendations(missing_skills: Iterable[str]) -> list[dict[str, object]]:
    recommendation_map = {
        "Docker": [
            "Learn container basics and how images are layered.",
            "Dockerize a small FastAPI application and test a local build.",
        ],
        "AWS": [
            "Study EC2, IAM, and S3 basics for cloud deployment.",
            "Deploy a small backend to AWS and practice environment configuration.",
        ],
        "Kubernetes": [
            "Learn pods, deployments, and services before scaling services.",
            "Deploy a simple containerized app on a local cluster.",
        ],
        "MongoDB": [
            "Practice CRUD operations and document modeling.",
            "Build a small app that reads and writes JSON data.",
        ],
        "Machine Learning": [
            "Review supervised learning basics and feature engineering.",
            "Train a small classification model on a real dataset.",
        ],
        "React": [
            "Practice reusable components and state-driven UI patterns.",
            "Build a mini dashboard with forms and dynamic cards.",
        ],
        "PostgreSQL": [
            "Learn SQL joins, indexes, and normalization basics.",
            "Model a small relational schema and query it efficiently.",
        ],
        "Git": [
            "Practice branching, commits, and pull requests.",
            "Use Git to track a portfolio project from start to finish.",
        ],
    }

    recommendations: list[dict[str, object]] = []
    for skill in missing_skills:
        canonical_skill = normalize_skill_name(skill)
        if not canonical_skill:
            continue
        actions = recommendation_map.get(
            canonical_skill,
            [
                f"Study the fundamentals of {canonical_skill}.",
                f"Apply {canonical_skill} in a practical project to build confidence.",
            ],
        )
        recommendations.append({"skill": canonical_skill, "recommendations": actions})
    return recommendations
