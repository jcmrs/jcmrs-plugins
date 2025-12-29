#!/usr/bin/env python3
"""
Knowledge Base Query Script

Query the semantic-linguist knowledge base (ambiguous terms, technical mappings,
ontology graph) with various filters and search patterns.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_knowledge(plugin_root: Path) -> Dict:
    """Load all knowledge base files."""
    knowledge_dir = plugin_root / "skills" / "semantic-validation" / "knowledge"

    with open(knowledge_dir / "ambiguous-terms.json") as f:
        ambiguous = json.load(f)

    with open(knowledge_dir / "technical-mappings.json") as f:
        technical = json.load(f)

    with open(knowledge_dir / "ontology-graph.json") as f:
        ontology = json.load(f)

    return {
        "ambiguous_terms": ambiguous,
        "technical_mappings": technical,
        "ontology_graph": ontology
    }


def search_ambiguous_terms(query: str, knowledge: Dict,
                          min_score: Optional[float] = None,
                          category: Optional[str] = None) -> List[Dict]:
    """
    Search ambiguous terms by query string.

    Args:
        query: Search term (partial match)
        knowledge: Knowledge base dictionary
        min_score: Minimum ambiguity score filter
        category: Category filter (e.g., 'meta_question', 'vague_action_verb')

    Returns:
        List of matching terms with their data
    """
    results = []
    ambiguous = knowledge["ambiguous_terms"]

    for term, data in ambiguous.items():
        # Query match
        if query.lower() not in term.lower():
            continue

        # Score filter
        if min_score is not None:
            score = data.get("ambiguity_score", 0)
            if score < min_score:
                continue

        # Category filter
        if category is not None:
            term_category = data.get("category", "")
            if category.lower() not in term_category.lower():
                continue

        results.append({
            "term": term,
            "data": data
        })

    return results


def get_term_details(term: str, knowledge: Dict) -> Optional[Dict]:
    """Get complete details for a specific ambiguous term."""
    ambiguous = knowledge["ambiguous_terms"]
    return ambiguous.get(term)


def get_all_categories(knowledge: Dict) -> List[str]:
    """Get all unique categories from ambiguous terms."""
    categories = set()
    for data in knowledge["ambiguous_terms"].values():
        if "category" in data:
            categories.add(data["category"])
    return sorted(list(categories))


def get_high_ambiguity_terms(knowledge: Dict, threshold: float = 0.8) -> List[Dict]:
    """Get all terms with ambiguity score above threshold."""
    results = []
    for term, data in knowledge["ambiguous_terms"].items():
        score = data.get("ambiguity_score", 0)
        if score >= threshold:
            results.append({
                "term": term,
                "score": score,
                "data": data
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def search_domain_mappings(domain: str, query: str, knowledge: Dict) -> List[Dict]:
    """
    Search technical mappings for a specific domain.

    Args:
        domain: Domain to search (autogen, langroid, general)
        query: Search term
        knowledge: Knowledge base dictionary

    Returns:
        List of matching mappings
    """
    results = []
    technical = knowledge["technical_mappings"]

    if domain not in technical:
        return results

    domain_data = technical[domain]

    # Recursive search through nested structure
    def search_nested(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key

                # Match on key
                if query.lower() in key.lower():
                    results.append({
                        "path": current_path,
                        "key": key,
                        "value": value
                    })

                # Recurse
                search_nested(value, current_path)

        elif isinstance(obj, str):
            # Match on string values
            if query.lower() in obj.lower():
                results.append({
                    "path": path,
                    "value": obj
                })

    search_nested(domain_data)
    return results


def get_cross_domain_mapping(concept: str, knowledge: Dict) -> Optional[Dict]:
    """Get cross-domain equivalents for a concept."""
    cross_domain = knowledge["technical_mappings"].get("cross_domain_equivalents", {})
    return cross_domain.get(concept)


def search_ontology(query: str, knowledge: Dict) -> List[Dict]:
    """Search ontology graph for matching entries."""
    results = []
    ontology = knowledge["ontology_graph"]

    # Search in autogen
    if "autogen" in ontology:
        for key, value in ontology["autogen"].items():
            if query.lower() in key.lower():
                results.append({
                    "domain": "autogen",
                    "key": key,
                    "data": value
                })

    # Search in langroid
    if "langroid" in ontology:
        for key, value in ontology["langroid"].items():
            if query.lower() in key.lower():
                results.append({
                    "domain": "langroid",
                    "key": key,
                    "data": value
                })

    # Search in conceptual relationships
    if "conceptual_relationships" in ontology:
        for concept, data in ontology["conceptual_relationships"].items():
            if query.lower() in concept.lower():
                results.append({
                    "domain": "conceptual",
                    "concept": concept,
                    "data": data
                })

    return results


def get_statistics(knowledge: Dict) -> Dict:
    """Get statistics about the knowledge base."""
    ambiguous_count = len(knowledge["ambiguous_terms"])

    # Count by category
    category_counts = {}
    for data in knowledge["ambiguous_terms"].values():
        cat = data.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # High ambiguity count
    high_ambiguity = sum(
        1 for data in knowledge["ambiguous_terms"].values()
        if data.get("ambiguity_score", 0) >= 0.8
    )

    # Domain counts
    autogen_count = len(knowledge["technical_mappings"].get("autogen", {}))
    langroid_count = len(knowledge["technical_mappings"].get("langroid", {}))

    # Ontology counts
    ontology = knowledge["ontology_graph"]
    autogen_ontology = len(ontology.get("autogen", {}))
    langroid_ontology = len(ontology.get("langroid", {}))
    conceptual = len(ontology.get("conceptual_relationships", {}))

    return {
        "ambiguous_terms": {
            "total": ambiguous_count,
            "by_category": category_counts,
            "high_ambiguity": high_ambiguity
        },
        "technical_mappings": {
            "autogen": autogen_count,
            "langroid": langroid_count
        },
        "ontology": {
            "autogen": autogen_ontology,
            "langroid": langroid_ontology,
            "conceptual": conceptual
        }
    }


def format_search_results(results: List[Dict], query_type: str) -> str:
    """Format search results for display."""
    output = []

    if not results:
        output.append(f"No results found for query type: {query_type}")
        return "\n".join(output)

    output.append(f"# Search Results ({len(results)} found)")
    output.append("")

    for i, result in enumerate(results, 1):
        output.append(f"## Result {i}")

        if query_type == "ambiguous":
            output.append(f"**Term**: {result['term']}")
            data = result['data']
            output.append(f"**Score**: {data.get('ambiguity_score', 'N/A')}")
            output.append(f"**Category**: {data.get('category', 'N/A')}")

            if 'domains' in data:
                output.append("\n**Domains**:")
                for domain, meanings in data['domains'].items():
                    output.append(f"  - {domain}: {', '.join(meanings)}")

        elif query_type == "domain":
            output.append(f"**Path**: {result.get('path', 'N/A')}")
            output.append(f"**Key**: {result.get('key', 'N/A')}")
            if 'value' in result and isinstance(result['value'], (str, int, float)):
                output.append(f"**Value**: {result['value']}")

        elif query_type == "ontology":
            output.append(f"**Domain**: {result.get('domain', 'N/A')}")
            output.append(f"**Key**: {result.get('key', result.get('concept', 'N/A'))}")

        output.append("")

    return "\n".join(output)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: knowledge-query.py <query_type> <query> [options]")
        print("\nQuery types:")
        print("  ambiguous <term> [--min-score 0.8] [--category meta_question]")
        print("  domain <domain> <query>  (e.g., 'domain autogen agent')")
        print("  ontology <query>")
        print("  cross-domain <concept>")
        print("  stats")
        print("  categories")
        print("  high-ambiguity [threshold]")
        sys.exit(1)

    query_type = sys.argv[1]
    plugin_root = Path(__file__).parent.parent
    knowledge = load_knowledge(plugin_root)

    # Handle different query types
    if query_type == "ambiguous":
        query = sys.argv[2]
        min_score = float(sys.argv[4]) if "--min-score" in sys.argv else None
        category = sys.argv[sys.argv.index("--category") + 1] if "--category" in sys.argv else None

        results = search_ambiguous_terms(query, knowledge, min_score, category)
        print(format_search_results(results, "ambiguous"))

    elif query_type == "domain":
        domain = sys.argv[2]
        query = sys.argv[3]
        results = search_domain_mappings(domain, query, knowledge)
        print(format_search_results(results, "domain"))

    elif query_type == "ontology":
        query = sys.argv[2]
        results = search_ontology(query, knowledge)
        print(format_search_results(results, "ontology"))

    elif query_type == "cross-domain":
        concept = sys.argv[2]
        result = get_cross_domain_mapping(concept, knowledge)
        if result:
            print(json.dumps({concept: result}, indent=2))
        else:
            print(f"No cross-domain mapping found for: {concept}")

    elif query_type == "stats":
        stats = get_statistics(knowledge)
        print(json.dumps(stats, indent=2))

    elif query_type == "categories":
        categories = get_all_categories(knowledge)
        print("Available categories:")
        for cat in categories:
            print(f"  - {cat}")

    elif query_type == "high-ambiguity":
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
        results = get_high_ambiguity_terms(knowledge, threshold)
        print(f"# High Ambiguity Terms (score >= {threshold})")
        print("")
        for result in results:
            print(f"- **{result['term']}**: {result['score']}")

    else:
        print(f"Unknown query type: {query_type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
