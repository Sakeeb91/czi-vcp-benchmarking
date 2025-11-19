"""
Cross-tissue analysis for disease signature discovery.

This module implements methods for comparing disease effects across tissues,
including correlation analysis and signature overlap.
"""

import pandas as pd
import numpy as np
import scanpy as sc
import anndata as ad
from typing import Dict, List, Tuple, Optional
from scipy import stats

class CrossTissueAnalyzer:
    """Analyzes relationships between tissues in disease context."""
    
    def __init__(self):
        pass
        
    def compute_expression_correlation(
        self,
        tissue_data: Dict[str, ad.AnnData],
        genes: Optional[List[str]] = None,
        method: str = 'pearson'
    ) -> pd.DataFrame:
        """
        Compute correlation of gene expression changes across tissues.
        
        Parameters
        ----------
        tissue_data : dict
            Dictionary of AnnData objects per tissue (processed)
        genes : list, optional
            List of genes to include. If None, uses common HVGs.
        method : str
            Correlation method ('pearson' or 'spearman')
            
        Returns
        -------
        correlation_matrix : pd.DataFrame
            Correlation matrix between tissues
        """
        print(f"\nComputing cross-tissue expression correlation...")
        tissues = list(tissue_data.keys())
        
        # If genes not provided, find common variable genes
        if genes is None:
            common_genes = None
            for adata in tissue_data.values():
                curr_genes = set(adata.var_names)
                if common_genes is None:
                    common_genes = curr_genes
                else:
                    common_genes = common_genes.intersection(curr_genes)
            genes = list(common_genes)
            print(f"  Using {len(genes)} common genes")
            
        # Calculate mean expression per tissue
        tissue_means = {}
        for tissue, adata in tissue_data.items():
            # Use raw counts or normalized data if available
            if genes:
                valid_genes = [g for g in genes if g in adata.var_names]
                subset = adata[:, valid_genes]
                # Calculate mean expression
                means = np.mean(subset.X, axis=0)
                if hasattr(means, 'A1'): # If sparse matrix
                    means = means.A1
                tissue_means[tissue] = pd.Series(means, index=valid_genes)
                
        # Create DataFrame of means
        means_df = pd.DataFrame(tissue_means)
        
        # Compute correlation
        corr_matrix = means_df.corr(method=method)
        
        return corr_matrix

    def compute_signature_overlap(
        self,
        signatures: Dict[str, pd.DataFrame],
        metric: str = 'jaccard'
    ) -> pd.DataFrame:
        """
        Compute overlap between disease signatures across tissues.
        
        Parameters
        ----------
        signatures : dict
            Dictionary of DE results/signatures per tissue
        metric : str
            Overlap metric ('jaccard' or 'intersection')
            
        Returns
        -------
        overlap_matrix : pd.DataFrame
            Matrix of overlap scores
        """
        print(f"\nComputing signature overlap ({metric})...")
        tissues = list(signatures.keys())
        n_tissues = len(tissues)
        matrix = pd.DataFrame(index=tissues, columns=tissues, dtype=float)
        
        for i, t1 in enumerate(tissues):
            genes1 = set(signatures[t1]['gene'])
            for j, t2 in enumerate(tissues):
                genes2 = set(signatures[t2]['gene'])
                
                if metric == 'jaccard':
                    intersection = len(genes1.intersection(genes2))
                    union = len(genes1.union(genes2))
                    score = intersection / union if union > 0 else 0
                elif metric == 'intersection':
                    score = len(genes1.intersection(genes2))
                elif metric == 'overlap_coefficient':
                    intersection = len(genes1.intersection(genes2))
                    min_size = min(len(genes1), len(genes2))
                    score = intersection / min_size if min_size > 0 else 0
                
                matrix.iloc[i, j] = score
                
        return matrix

    def compare_fold_changes(
        self,
        de_results: Dict[str, pd.DataFrame],
        genes: List[str]
    ) -> pd.DataFrame:
        """
        Compare log fold changes for specific genes across tissues.
        
        Parameters
        ----------
        de_results : dict
            Dictionary of DE results
        genes : list
            Genes to compare
            
        Returns
        -------
        fc_matrix : pd.DataFrame
            Matrix of log2FC values (rows=genes, cols=tissues)
        """
        print(f"\nComparing fold changes for {len(genes)} genes...")
        
        data = {}
        for tissue, df in de_results.items():
            # Create mapping of gene to log2fc
            fc_map = dict(zip(df['gene'], df['logfoldchanges']))
            
            # Get values for requested genes (NaN if not present)
            data[tissue] = [fc_map.get(g, np.nan) for g in genes]
            
        return pd.DataFrame(data, index=genes)

if __name__ == "__main__":
    print("Cross-tissue analysis module loaded successfully")
