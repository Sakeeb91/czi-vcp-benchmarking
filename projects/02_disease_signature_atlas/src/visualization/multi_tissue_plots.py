"""
Visualization tools for multi-tissue analysis.

This module provides functions to create comparative plots across tissues,
including heatmaps, correlation plots, and signature overlaps.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from pathlib import Path

class MultiTissueVisualizer:
    """Creates visualizations for multi-tissue comparisons."""
    
    def __init__(self, style: str = 'seaborn-v0_8-whitegrid'):
        plt.style.use(style)
        self.colors = sns.color_palette("husl", 8)
        
    def plot_correlation_heatmap(
        self,
        corr_matrix: pd.DataFrame,
        title: str = "Cross-Tissue Correlation",
        save_path: Optional[str] = None
    ):
        """
        Plot heatmap of cross-tissue correlations.
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='RdBu_r',
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            fmt='.2f'
        )
        plt.title(title, fontsize=14)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved correlation plot to {save_path}")
        plt.close()

    def plot_signature_overlap(
        self,
        overlap_matrix: pd.DataFrame,
        title: str = "Signature Overlap (Jaccard Index)",
        save_path: Optional[str] = None
    ):
        """
        Plot heatmap of signature overlaps.
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            overlap_matrix,
            annot=True,
            cmap='YlOrRd',
            vmin=0,
            vmax=1,
            square=True,
            fmt='.2f'
        )
        plt.title(title, fontsize=14)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved overlap plot to {save_path}")
        plt.close()

    def plot_cross_tissue_heatmap(
        self,
        fc_matrix: pd.DataFrame,
        title: str = "Cross-Tissue Gene Signatures",
        save_path: Optional[str] = None,
        cluster_rows: bool = True,
        cluster_cols: bool = False
    ):
        """
        Plot heatmap of log fold changes for signature genes across tissues.
        """
        # Fill NaNs with 0 for visualization
        data = fc_matrix.fillna(0)
        
        # Determine figure size based on data
        n_genes, n_tissues = data.shape
        height = max(6, n_genes * 0.2)
        width = max(6, n_tissues * 1.5)
        
        g = sns.clustermap(
            data,
            cmap='RdBu_r',
            center=0,
            figsize=(width, height),
            row_cluster=cluster_rows,
            col_cluster=cluster_cols,
            annot=False,
            cbar_kws={'label': 'log2 Fold Change'}
        )
        
        g.fig.suptitle(title, y=1.02, fontsize=16)
        
        if save_path:
            g.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved signature heatmap to {save_path}")
        plt.close()

    def plot_upset_like_bar(
        self,
        signatures: Dict[str, pd.DataFrame],
        save_path: Optional[str] = None
    ):
        """
        Create a simple bar plot showing number of unique and shared genes.
        (Simplified alternative to UpSet plot)
        """
        tissues = list(signatures.keys())
        
        # Count genes per tissue
        counts = {t: len(df) for t, df in signatures.items()}
        
        # Count shared genes (pairwise)
        import itertools
        shared_counts = {}
        for t1, t2 in itertools.combinations(tissues, 2):
            genes1 = set(signatures[t1]['gene'])
            genes2 = set(signatures[t2]['gene'])
            shared = len(genes1.intersection(genes2))
            shared_counts[f"{t1} & {t2}"] = shared
            
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Total genes per tissue
        sns.barplot(x=list(counts.keys()), y=list(counts.values()), ax=ax1, palette="viridis")
        ax1.set_title("Total Signature Genes per Tissue")
        ax1.set_ylabel("Number of Genes")
        
        # Shared genes
        if shared_counts:
            sns.barplot(x=list(shared_counts.keys()), y=list(shared_counts.values()), ax=ax2, palette="magma")
            ax2.set_title("Shared Genes (Pairwise)")
            ax2.set_ylabel("Number of Shared Genes")
            ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved comparison bar plot to {save_path}")
        plt.close()

if __name__ == "__main__":
    print("Multi-tissue visualization module loaded successfully")
