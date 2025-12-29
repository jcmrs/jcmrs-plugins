#!/usr/bin/env python3
"""
Domain Mapping Script

Maps terminology between Autogen, Langroid, and general AI concepts using
the ontology graph and technical mappings knowledge base.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def load_mappings(plugin_root: Path) -> Dict:
    """Load technical mappings and ontology graph."""
    knowledge_dir = plugin_root / "skills" / "semantic-validation" / "knowledge"

    with open(knowledge_dir / "technical-mappings.json") as f:
        technical_mappings = json.load(f)

    with open(knowledge_dir / "ontology-graph.json") as f:
        ontology_graph = json.load(f)

    return {
        "technical": technical_mappings,
        "ontology": ontology_graph
    }


def find_cross_domain_equivalent(term: str, mappings: Dict) -> Optional[Dict]:
    """Find cross-domain equivalents for a term."""
    # Check in cross_domain_equivalents
    cross_domain = mappings["technical"].get("cross_domain_equivalents", {})

    for concept, equivalents in cross_domain.items():
        # Check if term matches any value in equivalents
        for domain, domain_term in equivalents.items():
            if term.lower() in domain_term.lower() or domain_term.lower() in term.lower():
                return {
                    "concept": concept,
                    "equivalents": equivalents,
                    "matched_domain": domain
                }

    return None


def get_autogen_mapping(term: str, mappings: Dict) -> Optional[Dict]:
    """Get Autogen-specific mapping for a term."""
    autogen = mappings["technical"].get("autogen", {})

    # Search in all categories
    for category, items in autogen.items():
        if isinstance(items, dict):
            for key, value in items.items():
                if term.lower() in key.lower():
                    return {
                        "category": category,
                        "term": key,
                        "details": value
                    }

    return None


def get_langroid_mapping(term: str, mappings: Dict) -> Optional[Dict]:
    """Get Langroid-specific mapping for a term."""
    langroid = mappings["technical"].get("langroid", {})

    # Search in all categories
    for category, items in langroid.items():
        if isinstance(items, dict):
            for key, value in items.items():
                if term.lower() in key.lower():
                    return {
                        "category": category,
                        "term": key,
                        "details": value
                    }

    return None


def get_ontology_entry(term: str, mappings: Dict) -> Optional[Dict]:
    """Get ontology graph entry for a term."""
    ontology = mappings["ontology"]

    # Search in autogen ontology
    autogen_ontology = ontology.get("autogen", {})
    for key, value in autogen_ontology.items():
        if term.lower() in key.lower():
            return {
                "domain": "autogen",
                "term": key,
                "ontology": value
            }

    # Search in langroid ontology
    langroid_ontology = ontology.get("langroid", {})
    for key, value in langroid_ontology.items():
        if term.lower() in key.lower():
            return {
                "domain": "langroid",
                "term": key,
                "ontology": value
            }

    # Search in conceptual relationships
    conceptual = ontology.get("conceptual_relationships", {})
    for concept, data in conceptual.items():
        if term.lower() in concept.lower():
            return {
                "domain": "conceptual",
                "concept": concept,
                "relationships": data
            }

    return None


def map_term(term: str, source_domain: Optional[str], target_domain: Optional[str],
             plugin_root: Path) -> Dict:
    """
    Map a term between domains.

    Args:
        term: The term to map
        source_domain: Source domain (autogen, langroid, general, or None for auto-detect)
        target_domain: Target domain (autogen, langroid, general, or None for all)
        plugin_root: Plugin root directory path

    Returns:
        Dictionary with mapping results
    """
    mappings = load_mappings(plugin_root)

    result = {
        "term": term,
        "source_domain": source_domain,
        "target_domain": target_domain,
        "mappings": {}
    }

    # Find cross-domain equivalents
    cross_domain = find_cross_domain_equivalent(term, mappings)
    if cross_domain:
        result["mappings"]["cross_domain"] = cross_domain

    # Get domain-specific mappings
    if not target_domain or target_domain == "autogen":
        autogen_mapping = get_autogen_mapping(term, mappings)
        if autogen_mapping:
            result["mappings"]["autogen"] = autogen_mapping

    if not target_domain or target_domain == "langroid":
        langroid_mapping = get_langroid_mapping(term, mappings)
        if langroid_mapping:
            result["mappings"]["langroid"] = langroid_mapping

    # Get ontology entry
    ontology_entry = get_ontology_entry(term, mappings)
    if ontology_entry:
        result["mappings"]["ontology"] = ontology_entry

    # Determine if mapping was found
    result["found"] = len(result["mappings"]) > 0

    return result


def get_all_cross_domain_mappings(plugin_root: Path) -> Dict:
    """Get all cross-domain equivalent mappings."""
    mappings = load_mappings(plugin_root)
    return mappings["technical"].get("cross_domain_equivalents", {})


def get_domain_hierarchy(domain: str, plugin_root: Path) -> Optional[Dict]:
    """Get complete hierarchy for a domain (autogen or langroid)."""
    mappings = load_mappings(plugin_root)

    if domain == "autogen":
        return mappings["ontology"].get("autogen", {})
    elif domain == "langroid":
        return mappings["ontology"].get("langroid", {})
    else:
        return None


def format_mapping_output(result: Dict, verbose: bool = False) -> str:
    """Format mapping result for display."""
    output = []
    output.append(f"# Mapping: {result['term']}")
    output.append("")

    if not result["found"]:
        output.append("No mappings found for this term.")
        return "\n".join(output)

    # Cross-domain equivalents
    if "cross_domain" in result["mappings"]:
        cd = result["mappings"]["cross_domain"]
        output.append(f"## Cross-Domain Concept: {cd['concept']}")
        output.append("")
        for domain, equiv in cd["equivalents"].items():
            marker = " (matched)" if domain == cd["matched_domain"] else ""
            output.append(f"- **{domain.capitalize()}**: {equiv}{marker}")
        output.append("")

    # Autogen mapping
    if "autogen" in result["mappings"]:
        am = result["mappings"]["autogen"]
        output.append(f"## Autogen: {am['term']}")
        output.append(f"**Category**: {am['category']}")
        output.append("")
        details = am["details"]
        if isinstance(details, dict):
            for key, value in details.items():
                output.append(f"- **{key}**: {value}")
        output.append("")

    # Langroid mapping
    if "langroid" in result["mappings"]:
        lm = result["mappings"]["langroid"]
        output.append(f"## Langroid: {lm['term']}")
        output.append(f"**Category**: {lm['category']}")
        output.append("")
        details = lm["details"]
        if isinstance(details, dict):
            for key, value in details.items():
                output.append(f"- **{key}**: {value}")
        output.append("")

    # Ontology entry
    if verbose and "ontology" in result["mappings"]:
        oe = result["mappings"]["ontology"]
        output.append(f"## Ontology ({oe.get('domain', 'N/A')})")
        output.append("")
        if "ontology" in oe:
            output.append("```json")
            output.append(json.dumps(oe["ontology"], indent=2))
            output.append("```")

    return "\n".join(output)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: domain-mapper.py <term> [source_domain] [target_domain] [plugin_root]")
        print("\nExamples:")
        print("  domain-mapper.py ConversableAgent")
        print("  domain-mapper.py agent autogen langroid")
        print("  domain-mapper.py task langroid autogen")
        sys.exit(1)

    term = sys.argv[1]
    source_domain = sys.argv[2] if len(sys.argv) > 2 else None
    target_domain = sys.argv[3] if len(sys.argv) > 3 else None
    plugin_root = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(__file__).parent.parent

    result = map_term(term, source_domain, target_domain, plugin_root)

    # Output as JSON for programmatic use
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        # Output as formatted markdown for human reading
        print(format_mapping_output(result, verbose="--verbose" in sys.argv))


if __name__ == "__main__":
    main()
