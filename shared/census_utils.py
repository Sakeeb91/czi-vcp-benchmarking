"""
Shared utilities for Census data loading across projects.

This module provides common functions for loading data from the 
CELLxGENE Census, refactored from individual project implementations.
"""

import cellxgene_census
import tiledbsoma as soma
import pandas as pd
import anndata as ad
from typing import Optional, List, Tuple, Union
import warnings


def load_census_data(
    tissue: str = "blood",
    organism: str = "homo_sapiens",
    census_version: str = "stable",
    max_cells: Optional[int] = None,
    var_names: Optional[List[str]] = None,
    value_filter: Optional[str] = None,
    obs_columns: Optional[List[str]] = None,
    verbose: bool = True
) -> Tuple[ad.AnnData, dict]:
    """
    Load data from the CZI CELLxGENE Census with flexible filtering.
    
    Parameters
    ----------
    tissue : str
        Tissue to filter by (e.g., 'blood', 'lung', 'heart')
    organism : str
        Organism: 'homo_sapiens' or 'mus_musculus'
    census_version : str
        Census version to use ('stable' or 'latest')
    max_cells : int, optional
        Maximum number of cells to retrieve. If None, loads all matching cells.
    var_names : list of str, optional
        Specific genes to retrieve. If None, loads all genes.
    value_filter : str, optional
        Additional SOMA value filter. If None, uses "tissue == {tissue} and is_primary_data == True"
    obs_columns : list of str, optional
        Specific metadata columns to retrieve. If None, loads common columns.
    verbose : bool
        Print progress messages
        
    Returns
    -------
    adata : anndata.AnnData
        The expression data and metadata
    metadata : dict
        Additional metadata about the query (total cells found, filtering info, etc.)
    
    Examples
    --------
    >>> # Load blood data with COVID-19 filter
    >>> adata, meta = load_census_data(
    ...     tissue="blood",
    ...     value_filter="tissue == 'blood' and disease == 'COVID-19'",
    ...     max_cells=5000
    ... )
    
    >>> # Load specific genes from lung tissue
    >>> genes = ["ACE2", "TMPRSS2", "IL6"]
    >>> adata, meta = load_census_data(
    ...     tissue="lung",
    ...     var_names=genes,
    ...     max_cells=1000
    ... )
    """
    if verbose:
        print(f"Opening CELLxGENE Census ({census_version})...")
    
    metadata = {
        "tissue": tissue,
        "organism": organism,
        "census_version": census_version,
        "total_cells_found": 0,
        "cells_loaded": 0,
        "filtering_applied": False
    }
    
    with cellxgene_census.open_soma(census_version=census_version) as census:
        # Build the filter
        if value_filter is None:
            value_filter = f"tissue == '{tissue}' and is_primary_data == True"
        
        if verbose:
            print(f"Querying {organism} cells with filter: {value_filter}")
        
        # Get cell metadata
        obs = census["census_data"][organism].obs
        
        # Query for matching cells
        query_result = obs.read(
            value_filter=value_filter,
            column_names=["soma_joinid"]
        )
        
        # Get all matching IDs
        if verbose:
            print("Fetching cell IDs...")
        
        obs_df = query_result.concat().to_pandas()
        total_cells = len(obs_df)
        metadata["total_cells_found"] = total_cells
        
        if verbose:
            print(f"Found {total_cells:,} matching cells")
        
        # Sample if needed
        if max_cells and len(obs_df) > max_cells:
            if verbose:
                print(f"Sampling {max_cells:,} cells...")
            obs_df = obs_df.sample(n=max_cells, random_state=42)
            metadata["filtering_applied"] = True
        
        metadata["cells_loaded"] = len(obs_df)
        obs_soma_joinids = obs_df["soma_joinid"].tolist()
        
        # Fetch AnnData
        if verbose:
            print("Fetching expression data (this may take a moment)...")
        
        adata = cellxgene_census.get_anndata(
            census,
            organism=organism,
            obs_coords=obs_soma_joinids,
            var_value_filter=f"feature_name in {var_names}" if var_names else None,
            column_names={"obs": obs_columns} if obs_columns else None
        )
        
        if verbose:
            print(f"✓ Successfully loaded data: {adata.shape}")
            print(f"  Cells: {adata.n_obs:,}")
            print(f"  Genes: {adata.n_vars:,}")
    
    return adata, metadata


def load_multi_tissue_data(
    tissues: List[str],
    organism: str = "homo_sapiens",
    census_version: str = "stable",
    max_cells_per_tissue: Optional[int] = None,
    value_filter_template: Optional[str] = None,
    verbose: bool = True
) -> Tuple[ad.AnnData, pd.DataFrame]:
    """
    Load data from multiple tissues and concatenate.
    
    Parameters
    ----------
    tissues : list of str
        List of tissues to load
    organism : str
        Organism to query
    census_version : str
        Census version
    max_cells_per_tissue : int, optional
        Maximum cells per tissue
    value_filter_template : str, optional
        Filter template with {tissue} placeholder
    verbose : bool
        Print progress
        
    Returns
    -------
    adata_combined : anndata.AnnData
        Combined data from all tissues
    metadata_df : pd.DataFrame
        Metadata about each tissue query
    """
    adatas = []
    metadata_list = []
    
    for tissue in tissues:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Loading tissue: {tissue}")
            print(f"{'='*60}")
        
        # Build filter for this tissue
        if value_filter_template:
            tissue_filter = value_filter_template.format(tissue=tissue)
        else:
            tissue_filter = f"tissue == '{tissue}' and is_primary_data == True"
        
        adata, meta = load_census_data(
            tissue=tissue,
            organism=organism,
            census_version=census_version,
            max_cells=max_cells_per_tissue,
            value_filter=tissue_filter,
            verbose=verbose
        )
        
        adatas.append(adata)
        metadata_list.append(meta)
    
    # Concatenate all tissues
    if verbose:
        print(f"\n{'='*60}")
        print("Concatenating tissues...")
        print(f"{'='*60}")
    
    adata_combined = ad.concat(adatas, label="tissue", keys=tissues)
    metadata_df = pd.DataFrame(metadata_list)
    
    if verbose:
        print(f"✓ Combined data: {adata_combined.shape}")
        print(f"  Total cells: {adata_combined.n_obs:,}")
        print(f"  Total genes: {adata_combined.n_vars:,}")
        print(f"  Tissues: {len(tissues)}")
    
    return adata_combined, metadata_df


def get_available_tissues(
    organism: str = "homo_sapiens",
    census_version: str = "stable",
    min_cells: int = 100,
    top_n: Optional[int] = None
) -> pd.Series:
    """
    Get available tissues and their cell counts from Census.
    
    Parameters
    ----------
    organism : str
        Organism to query
    census_version : str
        Census version
    min_cells : int
        Minimum cells required to include tissue
    top_n : int, optional
        Return only top N tissues by cell count
        
    Returns
    -------
    tissue_counts : pd.Series
        Tissue names and cell counts, sorted by count
    """
    print(f"Fetching available tissues from {organism}...")
    
    with cellxgene_census.open_soma(census_version=census_version) as census:
        obs = census["census_data"][organism].obs
        
        # Read tissue column
        tissue_data = obs.read(
            column_names=["tissue"],
            value_filter="is_primary_data == True"
        ).concat().to_pandas()
        
        # Count cells per tissue
        tissue_counts = tissue_data['tissue'].value_counts()
        
        # Filter by minimum cells
        tissue_counts = tissue_counts[tissue_counts >= min_cells]
        
        # Limit to top N if specified
        if top_n:
            tissue_counts = tissue_counts.head(top_n)
    
    print(f"✓ Found {len(tissue_counts)} tissues with >={min_cells} cells")
    
    return tissue_counts


def get_disease_info(
    organism: str = "homo_sapiens",
    tissue: Optional[str] = None,
    census_version: str = "stable"
) -> pd.DataFrame:
    """
    Get information about diseases available in the Census.
    
    Parameters
    ----------
    organism : str
        Organism to query
    tissue : str, optional
        Filter by specific tissue
    census_version : str
        Census version
        
    Returns
    -------
    disease_info : pd.DataFrame
        DataFrame with disease, tissue, and cell counts
    """
    print(f"Fetching disease information from {organism}...")
    
    with cellxgene_census.open_soma(census_version=census_version) as census:
        obs = census["census_data"][organism].obs
        
        # Build filter
        filter_str = "is_primary_data == True"
        if tissue:
            filter_str += f" and tissue == '{tissue}'"
        
        # Read disease and tissue data
        disease_data = obs.read(
            column_names=["disease", "tissue"],
            value_filter=filter_str
        ).concat().to_pandas()
        
        # Group by disease and tissue
        disease_summary = disease_data.groupby(['disease', 'tissue']).size().reset_index(name='cell_count')
        disease_summary = disease_summary.sort_values('cell_count', ascending=False)
    
    print(f"✓ Found {len(disease_summary)} disease-tissue combinations")
    
    return disease_summary
