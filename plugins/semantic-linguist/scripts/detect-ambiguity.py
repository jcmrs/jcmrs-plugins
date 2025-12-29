#!/usr/bin/env python3
"""
Semantic Ambiguity Detection Script

Analyzes text for ambiguous terminology using knowledge base and returns
confidence scores and detected ambiguities.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_knowledge_base(plugin_root: Path) -> Dict:
    """Load all knowledge base JSON files."""
    knowledge_dir = plugin_root / "skills" / "semantic-validation" / "knowledge"

    with open(knowledge_dir / "ambiguous-terms.json") as f:
        ambiguous_terms = json.load(f)

    with open(knowledge_dir / "technical-mappings.json") as f:
        technical_mappings = json.load(f)

    with open(knowledge_dir / "ontology-graph.json") as f:
        ontology_graph = json.load(f)

    return {
        "ambiguous_terms": ambiguous_terms,
        "technical_mappings": technical_mappings,
        "ontology_graph": ontology_graph
    }


def detect_meta_questions(text: str) -> List[str]:
    """Detect meta-questions in text."""
    meta_patterns = [
        r"am i making sense",
        r"does this make sense",
        r"is this right",
        r"am i doing this right",
        r"making sense\?"
    ]

    detected = []
    text_lower = text.lower()

    for pattern in meta_patterns:
        if re.search(pattern, text_lower):
            detected.append(pattern)

    return detected


def detect_user_self_identification(text: str) -> List[str]:
    """Detect when user identifies as non-technical."""
    patterns = [
        r"non-technical user",
        r"i'm not technical",
        r"i am not technical",
        r"beginner",
        r"not a programmer"
    ]

    detected = []
    text_lower = text.lower()

    for pattern in patterns:
        if re.search(pattern, text_lower):
            detected.append(pattern)

    return detected


def detect_known_ambiguous_terms(text: str, knowledge: Dict) -> List[Tuple[str, Dict]]:
    """Detect known ambiguous terms from knowledge base."""
    detected = []
    text_lower = text.lower()

    for term, data in knowledge["ambiguous_terms"].items():
        # Check direct term match
        if term in text_lower:
            detected.append((term, data))
            continue

        # Check user_triggers if present
        if "user_triggers" in data:
            for trigger in data["user_triggers"]:
                if trigger.lower() in text_lower:
                    detected.append((term, data))
                    break

    return detected


def detect_vague_verbs(text: str) -> List[str]:
    """Detect vague action verbs."""
    patterns = [
        r"make it \w+",
        r"do the thing",
        r"fix it",
        r"get it working",
        r"create \w+ without specifics"
    ]

    detected = []
    text_lower = text.lower()

    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        detected.extend(matches)

    return detected


def detect_generic_terms(text: str) -> List[str]:
    """Detect generic technical terms without context."""
    generic_terms = [
        "agent", "task", "tool", "component", "service",
        "module", "container", "wrapper", "handler"
    ]

    # Simple heuristic: word appears without specific framework context
    detected = []
    text_lower = text.lower()

    # Check if text has framework-specific context
    has_autogen_context = any(keyword in text_lower for keyword in [
        "autogen", "conversableagent", "groupchat", "assistantagent"
    ])
    has_langroid_context = any(keyword in text_lower for keyword in [
        "langroid", "chatagent", "toolmessage", "task.run"
    ])

    # If no clear framework context, generic terms are ambiguous
    if not has_autogen_context and not has_langroid_context:
        for term in generic_terms:
            # Word boundary match
            if re.search(rf"\b{term}\b", text_lower):
                detected.append(term)

    return detected


def detect_unclear_references(text: str) -> List[str]:
    """Detect unclear references."""
    patterns = [
        r"\bthat\b(?! \w+)",  # "that" without following noun
        r"\bit\b(?! \w+)",    # "it" without following noun
        r"the thing",
        r"like before(?! \w+)"
    ]

    detected = []

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        detected.extend(matches)

    return detected


def calculate_confidence_score(detections: Dict[str, List]) -> int:
    """Calculate overall confidence score based on detected patterns."""
    score = 0

    # Meta-questions: +100 (auto-trigger)
    if detections["meta_questions"]:
        score += 100

    # User self-identification: +100
    if detections["user_self_id"]:
        score += 100

    # Known ambiguous terms: +40 each
    for term, data in detections["known_terms"]:
        score += int(data.get("ambiguity_score", 0.8) * 100)

    # Vague action verbs: +30 each
    score += len(detections["vague_verbs"]) * 30

    # Generic terms without context: +25 each
    score += len(detections["generic_terms"]) * 25

    # Unclear references: +20 each
    score += len(detections["unclear_refs"]) * 20

    return min(score, 100)  # Cap at 100


def analyze_text(text: str, plugin_root: Path) -> Dict:
    """
    Analyze text for semantic ambiguities.

    Returns:
        Dictionary with detections and confidence score.
    """
    knowledge = load_knowledge_base(plugin_root)

    detections = {
        "meta_questions": detect_meta_questions(text),
        "user_self_id": detect_user_self_identification(text),
        "known_terms": detect_known_ambiguous_terms(text, knowledge),
        "vague_verbs": detect_vague_verbs(text),
        "generic_terms": detect_generic_terms(text),
        "unclear_refs": detect_unclear_references(text)
    }

    confidence_score = calculate_confidence_score(detections)

    return {
        "confidence_score": confidence_score,
        "detections": detections,
        "should_validate": confidence_score >= 80,
        "severity": (
            "high" if confidence_score >= 80 else
            "moderate" if confidence_score >= 60 else
            "low"
        )
    }


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: detect-ambiguity.py <text> [plugin_root]")
        sys.exit(1)

    text = sys.argv[1]
    plugin_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent.parent

    result = analyze_text(text, plugin_root)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
