"""
Signature discovery for multi-tissue disease analysis.

This module identifies disease signatures that are consistent across
multiple tissues and tissue-specific signatures.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json


class SignatureDiscovery:
    """Discovers cross-tissue and tissue-specific disease signatures."""
    
    def __init__(self):
        """Initialize signature discovery."""
        pass
    
    def identify_cross_tissue_signatures(
        self,
        tissue_results: Dict[str, pd.DataFrame],
        min_tissues: int = 2,
        direction_consistent: bool = True
    ) -> pd.DataFrame:
        """
        Identify genes significant across multiple tissues.
        
        Parameters
        ----------
        tissue_results : dict
            Dictionary mapping tissue names to DE results DataFrames
        min_tissues : int
            Minimum number of tissues gene must be significant in
        direction_consistent : bool
            If True, require same direction across tissues
            
        Returns
        -------
        cross_tissue_sigs : pd.DataFrame
            Cross-tissue signatures with aggregated statistics
        """
        print(f"\nIdentifying cross-tissue signatures...")
        print(f"  Tissues: {list(tissue_results.keys())}")
        print(f"  Min tissues required: {min_tissues}")
        
        # Collect all genes
        all_genes = set()
        for tissue_df in tissue_results.values():
            all_genes.update(tissue_df['gene'].unique())
        
        print(f"  Total unique genes: {len(all_genes)}")
        
        # For each gene, check presence across tissues
        cross_tissue_data = []
        
        for gene in all_genes:
            gene_info = {
                'gene': gene,
                'n_tissues': 0,
                'tissues': [],
                'avg_log2fc': [],
                'directions': [],
                'min_pval_adj': 1.0
            }
            
            for tissue, tissue_df in tissue_results.items():
                gene_rows = tissue_df[tissue_df['gene'] == gene]
                
                if len(gene_rows) > 0:
                    row = gene_rows.iloc[0]
                    gene_info['n_tissues'] += 1
                    gene_info['tissues'].append(tissue)
                    gene_info['avg_log2fc'].append(row['logfoldchanges'])
                    gene_info['directions'].append(row['direction'])
                    gene_info['min_pval_adj'] = min(
                        gene_info['min_pval_adj'],
                        row['pvals_adj']
                    )
            
            # Check if meets criteria
            if gene_info['n_tissues'] >= min_tissues:
                if direction_consistent:
                    # Check all directions are the same
                    if len(set(gene_info['directions'])) == 1:
                        gene_info['avg_log2fc'] = np.mean(gene_info['avg_log2fc'])
                        gene_info['direction'] = gene_info['directions'][0]
                        gene_info['tissues'] = ','.join(gene_info['tissues'])
                        cross_tissue_data.append(gene_info)
                else:
                    gene_info['avg_log2fc'] = np.mean(gene_info['avg_log2fc'])
                    gene_info['direction'] = gene_info['directions'][0]
                    gene_info['tissues'] = ','.join(gene_info['tissues'])
                    cross_tissue_data.append(gene_info)
        
        # Create DataFrame
        cross_tissue_df = pd.DataFrame(cross_tissue_data)
        
        if len(cross_tissue_df) > 0:
            # Remove temporary columns
            cross_tissue_df = cross_tissue_df.drop(columns=['directions'])
            
            # Sort by number of tissues and significance
            cross_tissue_df = cross_tissue_df.sort_values(
                ['n_tissues', 'min_pval_adj'],
                ascending=[False, True]
            )
        
        print(f"\n✓ Found {len(cross_tissue_df)} cross-tissue signatures")
        if len(cross_tissue_df) > 0:
            print(f"  Present in {cross_tissue_df['n_tissues'].min()}-{cross_tissue_df['n_tissues'].max()} tissues")
        
        return cross_tissue_df
    
    def identify_tissue_specific_signatures(
        self,
        tissue_results: Dict[str, pd.DataFrame],
        cross_tissue_genes: List[str]
    ) -> Dict[str, pd.DataFrame]:
        """
        Identify tissue-specific signatures.
        
        Parameters
        ----------
        tissue_results : dict
            DE results per tissue
        cross_tissue_genes : list
            Genes already identified as cross-tissue
            
        Returns
        -------
        tissue_specific : dict
            Dictionary of tissue-specific signatures
        """
        print(f"\nIdentifying tissue-specific signatures...")
        
        tissue_specific = {}
        
        for tissue, tissue_df in tissue_results.items():
            # Filter out cross-tissue genes
            specific = tissue_df[~tissue_df['gene'].isin(cross_tissue_genes)].copy()
            
            tissue_specific[tissue] = specific
            
            print(f"  {tissue}: {len(specific)} tissue-specific genes")
        
        return tissue_specific
    
    def create_signature_summary(
        self,
        cross_tissue_sigs: pd.DataFrame,
        tissue_specific_sigs: Dict[str, pd.DataFrame]
    ) -> Dict:
        """
        Create summary of discovered signatures.
        
        Returns
        -------
        summary : dict
            Summary statistics
        """
        summary = {
            'cross_tissue': {
                'total_genes': len(cross_tissue_sigs),
                'upregulated': (cross_tissue_sigs['direction'] == 'up').sum() if len(cross_tissue_sigs) > 0 else 0,
                'downregulated': (cross_tissue_sigs['direction'] == 'down').sum() if len(cross_tissue_sigs) > 0 else 0,
                'top_genes': cross_tissue_sigs.head(20)['gene'].tolist() if len(cross_tissue_sigs) > 0 else []
            },
            'tissue_specific': {}
        }
        
        for tissue, sig_df in tissue_specific_sigs.items():
            summary['tissue_specific'][tissue] = {
                'total_genes': len(sig_df),
                'upregulated': (sig_df['direction'] == 'up').sum(),
                'downregulated': (sig_df['direction'] == 'down').sum(),
                'top_genes': sig_df.head(20)['gene'].tolist()
            }
        
        return summary
    
    def save_signatures(
        self,
        cross_tissue_sigs: pd.DataFrame,
        tissue_specific_sigs: Dict[str, pd.DataFrame],
        output_dir: str = "results/signatures"
    ):
        """Save discovered signatures."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save cross-tissue signatures
        if len(cross_tissue_sigs) > 0:
            cross_path = output_path / "cross_tissue_signatures.csv"
            cross_tissue_sigs.to_csv(cross_path, index=False)
            print(f"\n✓ Saved cross-tissue signatures: {cross_path}")
        
        # Save tissue-specific signatures
        for tissue, sig_df in tissue_specific_sigs.items():
            tissue_path = output_path / f"{tissue}_specific_signatures.csv"
            sig_df.to_csv(tissue_path, index=False)
            print(f"✓ Saved {tissue} signatures: {tissue_path}")
        
        # Save summary
        summary = self.create_signature_summary(cross_tissue_sigs, tissue_specific_sigs)
        summary_path = output_path / "signature_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✓ Saved summary: {summary_path}")


if __name__ == "__main__":
    print("Signature discovery module loaded successfully")
