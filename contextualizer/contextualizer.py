import cobra

def integrate_context(model, upregulated_genes):
    """
    Modifies a model by upregulating reactions associated with a given list of genes.

    Args:
        model (cobra.Model): The model to modify.
        upregulated_genes (list): A list of gene IDs to upregulate.

    Returns:
        cobra.Model: The modified model.
    """
    context_model = model.copy()
    upregulated_count = 0
    for gene_id in upregulated_genes:
        try:
            # Find the gene in the model
            gene = context_model.genes.get_by_id(gene_id)
            # Increase the upper bound of all associated reactions
            for rxn in gene.reactions:
                if rxn.upper_bound < 1000.0:
                    rxn.upper_bound = 1000.0
            upregulated_count += len(gene.reactions)
        except KeyError:
            # Gene from the list might not be in the model, which is fine
            pass
            
    print(f"   - Upregulated {upregulated_count} reactions based on the gene list.")
    return context_model