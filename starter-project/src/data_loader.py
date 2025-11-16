"""
Functions for loading data from the CZI CELLxGENE Census
"""

import cellxgene_census
import pandas as pd
from typing import List, Optional
from tqdm import tqdm


def load_cell_metadata(
    organism: str = "homo_sapiens",
    tissues: Optional[List[str]] = None,
    max_cells_per_tissue: int = 10000,
    census_version: str = "stable"
) -> pd.DataFrame:
    """
    Load cell metadata from the Census.

    Parameters:
    -----------
    organism : str
        Either "homo_sapiens" or "mus_musculus"
    tissues : List[str], optional
        List of specific tissues to query. If None, queries all tissues.
    max_cells_per_tissue : int
        Maximum number of cells to retrieve per tissue
    census_version : str
        Census version to use (default: "stable")

    Returns:
    --------
    pd.DataFrame
        Cell metadata including cell_type, tissue, disease, etc.
    """
    print(f"Loading cell metadata for {organism}...")

    with cellxgene_census.open_soma(census_version=census_version) as census:
        organism_data = census["census_data"][organism]

        # Query cell metadata
        columns = ["cell_type", "tissue", "disease", "sex", "assay", "suspension_type"]

        if tissues:
            # Build filter for specific tissues
            tissue_filter = " or ".join([f'tissue == "{t}"' for t in tissues])
            print(f"Querying tissues: {', '.join(tissues)}")

            cell_data = organism_data["obs"].read(
                column_names=columns,
                value_filter=tissue_filter
            ).concat().to_pandas()
        else:
            print("Querying all tissues...")
            cell_data = organism_data["obs"].read(
                column_names=columns
            ).concat().to_pandas()

        # Limit cells per tissue if specified
        if max_cells_per_tissue:
            cell_data = cell_data.groupby('tissue').head(max_cells_per_tissue)

        print(f"✓ Loaded {len(cell_data):,} cells")
        print(f"  Tissues: {cell_data['tissue'].nunique()}")
        print(f"  Cell Types: {cell_data['cell_type'].nunique()}")

        return cell_data


def get_available_tissues(
    organism: str = "homo_sapiens",
    census_version: str = "stable"
) -> pd.Series:
    """
    Get list of available tissues and their cell counts.

    Parameters:
    -----------
    organism : str
        Either "homo_sapiens" or "mus_musculus"
    census_version : str
        Census version to use

    Returns:
    --------
    pd.Series
        Tissue names and their cell counts
    """
    print(f"Getting available tissues for {organism}...")

    with cellxgene_census.open_soma(census_version=census_version) as census:
        organism_data = census["census_data"][organism]

        # Query just tissue information
        tissue_data = organism_data["obs"].read(
            column_names=["tissue"]
        ).concat().to_pandas()

        tissue_counts = tissue_data['tissue'].value_counts()
        print(f"✓ Found {len(tissue_counts)} unique tissues")

        return tissue_counts


def get_cell_type_summary(cell_data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for cell types across tissues.

    Parameters:
    -----------
    cell_data : pd.DataFrame
        Cell metadata from load_cell_metadata()

    Returns:
    --------
    pd.DataFrame
        Summary table with cell type counts per tissue
    """
    summary = cell_data.groupby(['tissue', 'cell_type']).size().reset_index(name='count')
    summary = summary.pivot(index='cell_type', columns='tissue', values='count').fillna(0)

    return summary
