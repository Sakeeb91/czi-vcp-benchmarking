"""
Scanpy preprocessing pipeline for single-cell RNA-seq data.

This module implements quality control, normalization, and feature selection
using Scanpy best practices.
"""

import scanpy as sc
import anndata as ad
import numpy as np
import yaml
from pathlib import Path
from typing import Optional, Tuple


class ScancpyPreprocessor:
    """Scanpy-based preprocessing pipeline."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__).parents[2] / "config.yaml"
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['scanpy']
    
    def preprocess(
        self,
        adata: ad.AnnData,
        copy: bool = False,
        verbose: bool = True
    ) -> ad.AnnData:
        """
        Run full preprocessing pipeline.
        
        Steps:
        1. Calculate QC metrics
        2. Filter cells and genes
        3. Normalize
        4. Log transform
        5. Identify highly variable genes
        6. Scale
        7. PCA
        8. Neighbors graph
        9. UMAPParameters
        ----------
        adata : anndata.AnnData
            Input data
        copy : bool
            If True, return a copy
        verbose : bool
            Print progress
            
        Returns
        -------
        adata_processed : anndata.AnnData
            Preprocessed data
        """
        if copy:
            adata = adata.copy()
        
        if verbose:
            print(f"\nStarting Scanpy preprocessing")
            print(f"Input: {adata.n_obs} cells x {adata.n_vars} genes")
        
        # Step 1: Calculate QC metrics
        if verbose:
            print("\n1. Calculating QC metrics...")
        
        adata.var['mt'] = adata.var_names.str.startswith('MT-')
        sc.pp.calculate_qc_metrics(
            adata,
            qc_vars=['mt'],
            percent_top=None,
            log1p=False,
            inplace=True
        )
        
        # Step 2: Filter
        if verbose:
            print("2. Filtering cells and genes...")
        
        sc.pp.filter_cells(adata, min_genes=self.config['min_genes'])
        sc.pp.filter_genes(adata, min_cells=self.config['min_cells'])
        
        # Filter by MT content
        adata = adata[adata.obs.pct_counts_mt < self.config['mt_percent_max'], :]
        
        if verbose:
            print(f"   After filtering: {adata.n_obs} cells x {adata.n_vars} genes")
        
        # Step 3: Normalize
        if verbose:
            print("3. Normalizing...")
        
        sc.pp.normalize_total(adata, target_sum=self.config['target_sum'])
        
        # Step 4: Log transform
        if verbose:
            print("4. Log transforming...")
        
        sc.pp.log1p(adata)
        
        # Step 5: Highly variable genes
        if verbose:
            print("5. Identifying highly variable genes...")
        
        sc.pp.highly_variable_genes(
            adata,
            n_top_genes=self.config['n_top_genes'],
            subset=False
        )
        
        n_hvgs = adata.var.highly_variable.sum()
        if verbose:
            print(f"   Found {n_hvgs} highly variable genes")
        
        # Step 6: Scale
        if verbose:
            print("6. Scaling...")
        
        sc.pp.scale(adata, max_value=10)
        
        # Step 7: PCA
        if verbose:
            print("7. Computing PCA...")
        
        sc.tl.pca(adata, n_comps=self.config['n_pcs'], svd_solver='arpack')
        
        # Step 8: Neighbors
        if verbose:
            print("8. Computing neighborhood graph...")
        
        sc.pp.neighbors(adata, n_neighbors=self.config['n_neighbors'])
        
        # Step 9: UMAP
        if verbose:
            print("9. Computing UMAP...")
        
        sc.tl.umap(adata)
        
        if verbose:
            print(f"\n✓ Preprocessing complete!")
            print(f"Final: {adata.n_obs} cells x {adata.n_vars} genes")
        
        return adata
    
    def quick_qc_plots(self, adata: ad.AnnData, save_path: Optional[str] = None):
        """Generate QC plots."""
        import matplotlib.pyplot as plt
        
        sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
                     jitter=0.4, multi_panel=True, save=save_path)


if __name__ == "__main__":
    print("Scanpy preprocessing module loaded successfully")
