"""
Module: parser_engine.parser
Parse COBRA model into internal reaction graph.
"""
import networkx as nx
import cobra


def parse_reaction_graph(model: cobra.Model) -> nx.DiGraph:
    """Build a directed graph: metabolites as nodes, reactions as edges."""
    G = nx.DiGraph()
    for met in model.metabolites:
        G.add_node(met.id)
    for rxn in model.reactions:
        for met in rxn.reactants:
            for prod in rxn.products:
                G.add_edge(met.id, prod.id, reaction=rxn.id)
    return G
