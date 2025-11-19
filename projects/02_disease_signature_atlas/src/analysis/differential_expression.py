"""
Differential expression analysis for disease signature discovery.

This module implements differential expression analysis using Scanpy,
comparing disease vs control conditions across tissues.
"""

import scanpy as sc
import pandas as pd
import numpy as np
import anndata as ad
from typing import Optional, List, Dict, Tuple
import yaml
from pathlib import Path


class DifferentialExpressionAnalyzer:
    """Performs differential expression analysis between conditions."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__).parents[2] / "config.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.de_config = config['differential_expression']
    
    def prepare_for_de(
        self,
        disease_data: ad.AnnData,
        control_data: ad.AnnData,
        tissue_label: Optional[str] = None
    ) -> ad.AnnData:
        """
        Combine disease and control data for DE analysis.
        
        Parameters
        ----------
        disease_data : anndata.AnnData
            Preprocessed disease data
        control_data : anndata.AnnData
            Preprocessed control data
        tissue_label : str, optional
            Tissue label to add to metadata
            
        Returns
        -------
        combined : anndata.AnnData
            Combined data with condition labels
        """
        # Add condition labels
        disease_data.obs['condition'] = 'disease'
        control_data.obs['condition'] = 'control'
        
        if tissue_label:
            disease_data.obs['tissue'] = tissue_label
            control_data.obs['tissue'] = tissue_label
        
        # Concatenate
        combined = ad.concat([disease_data, control_data], label='source')
        
        print(f"Combined data: {combined.n_obs} cells")
        print(f"  Disease: {(combined.obs['condition'] == 'disease').sum()}")
        print(f"  Control: {(combined.obs['condition'] == 'control').sum()}")
        
        return combined
    
    def run_de_analysis(
        self,
        adata: ad.AnnData,
        groupby: str = 'condition',
        reference: str = 'control',
        method: Optional[str] = None,
        key_added: str = 'rank_genes_groups'
    ) -> pd.DataFrame:
        """
        Run differential expression analysis.
        
        Parameters
        ----------
        adata : anndata.AnnData
            Combined data with condition labels
        groupby : str
            Column in obs to group by
        reference : str
            Reference group for comparison
        method : str, optional
            Statistical test method
        key_added : str
            Key to store results in adata.uns
            
        Returns
        -------
        results_df : pd.DataFrame
            Differential expression results
        """
        if method is None:
            method = self.de_config['method']
        
        print(f"\nRunning differential expression analysis...")
        print(f"  Method: {method}")
        print(f"  Grouping: {groupby}")
        print(f"  Reference: {reference}")
        
        # Run DE analysis
        sc.tl.rank_genes_groups(
            adata,
            groupby=groupby,
            reference=reference,
            method=method,
            key_added=key_added
        )
        
        # Extract results
        result = adata.uns[key_added]
        groups = result['names'].dtype.names
        
        # Convert to DataFrame
        results_list = []
        for group in groups:
            if group == reference:
                continue
            
            group_df = pd.DataFrame({
                'gene': result['names'][group],
                'logfoldchanges': result['logfoldchanges'][group],
                'pvals': result['pvals'][group],
                'pvals_adj': result['pvals_adj'][group],
                'scores': result['scores'][group],
                'group': group
            })
            results_list.append(group_df)
        
        results_df = pd.concat(results_list, ignore_index=True)
        
        print(f"✓ Found {len(results_df)} gene-group combinations")
        
        return results_df
    
    def filter_significant_genes(
        self,
        results_df: pd.DataFrame,
        min_log2fc: Optional[float] = None,
        max_pval_adj: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Filter for significant genes.
        
        Parameters
        ----------
        results_df : pd.DataFrame
            DE analysis results
        min_log2fc : float, optional
            Minimum absolute log2 fold change
        max_pval_adj : float, optional
            Maximum adjusted p-value
            
        Returns
        -------
        filtered_df : pd.DataFrame
            Filtered results
        """
        if min_log2fc is None:
            min_log2fc = self.de_config['min_log2fc']
        if max_pval_adj is None:
            max_pval_adj = self.de_config['adj_pval_threshold']
        
        filtered = results_df[
            (results_df['pvals_adj'] < max_pval_adj) &
            (abs(results_df['logfoldchanges']) > min_log2fc)
        ].copy()
        
        # Add direction
        filtered['direction'] = filtered['logfoldchanges'].apply(
            lambda x: 'up' if x > 0 else 'down'
        )
        
        # Sort by significance
        filtered = filtered.sort_values('pvals_adj')
        
        print(f"\nSignificant genes (adj p < {max_pval_adj}, |log2FC| > {min_log2fc}):")
        print(f"  Total: {len(filtered)}")
        print(f"  Upregulated: {(filtered['direction'] == 'up').sum()}")
        print(f"  Downregulated: {(filtered['direction'] == 'down').sum()}")
        
        return filtered
    
    def get_top_genes(
        self,
        results_df: pd.DataFrame,
        n_genes: int = 50,
        by: str = 'pvals_adj',
        direction: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get top genes from results.
        
        Parameters
        ----------
        results_df : pd.DataFrame
            DE results
        n_genes : int
            Number of top genes
        by : str
            Column to sort by
        direction : str, optional
            Filter by direction ('up' or 'down')
            
        Returns
        -------
        top_genes : pd.DataFrame
            Top genes
        """
        df = results_df.copy()
        
        if direction:
            df = df[df['direction'] == direction]
        
        if by == 'pvals_adj':
            top = df.nsmallest(n_genes, by)
        elif by == 'logfoldchanges':
            top = df.nlargest(n_genes, by)
        else:
            top = df.head(n_genes)
        
        return top
    
    def save_results(
        self,
        results_df: pd.DataFrame,
        output_path: str,
        tissue: Optional[str] = None
    ):
        """Save DE results to CSV."""
        if tissue:
            output_path = output_path.replace('.csv', f'_{tissue}.csv')
        
        results_df.to_csv(output_path, index=False)
        print(f"\n✓ Saved results to: {output_path}")


def run_single_tissue_de(
    disease_data: ad.AnnData,
    control_data: ad.AnnData,
    tissue: str = "blood",
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Run DE analysis for a single tissue.
    
    Parameters
    ----------
    disease_data : anndata.AnnData
        Disease data
    control_data : anndata.AnnData
        Control data
    tissue : str
        Tissue name
    output_dir : str, optional
        Directory to save results
        
    Returns
    -------
    sig_genes : pd.DataFrame
        Significant genes
    """
    print(f"\n{'='*70}")
    print(f"Differential Expression Analysis: {tissue}")
    print(f"{'='*70}")
    
    analyzer = DifferentialExpressionAnalyzer()
    
    # Prepare data
    combined = analyzer.prepare_for_de(disease_data, control_data, tissue)
    
    # Run DE
    results = analyzer.run_de_analysis(combined)
    
    # Filter significant genes
    sig_genes = analyzer.filter_significant_genes(results)
    
    # Save if output directory provided
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = str(Path(output_dir) / f"de_results_{tissue}.csv")
        analyzer.save_results(sig_genes, output_path)
    
    return sig_genes


if __name__ == "__main__":
    print("Differential expression module loaded successfully")
