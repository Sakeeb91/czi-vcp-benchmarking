import cellxgene_census
import tiledbsoma as soma
import pandas as pd

def load_census_data(
    tissue="blood",
    organism="homo_sapiens",
    census_version="stable",
    max_cells=1000,
    var_names=None
):
    """
    Loads a subset of data from the CZI CELLxGENE Census.
    
    Args:
        tissue (str): Tissue to filter by (e.g., 'blood').
        organism (str): Organism to query (default: 'homo_sapiens').
        census_version (str): Census version to use.
        max_cells (int): Maximum number of cells to retrieve.
        var_names (list): List of gene names to retrieve (optional).
        
    Returns:
        tuple: (anndata.AnnData, int) - The data matrix and the total number of matching cells found.
    """
    print(f"Opening Census ({census_version})...")
    with cellxgene_census.open_soma(census_version=census_version) as census:
        # 1. Get the obs (cell metadata) to identify cells of interest
        print(f"Querying {organism} cells for tissue='{tissue}'...")
        obs = census["census_data"][organism].obs
        
        # Create a query for the specific tissue
        query = obs.read(
            value_filter=f"tissue == '{tissue}' and is_primary_data == True",
            column_names=["soma_joinid"]
        )
        
        # Get all matching IDs
        # Note: For very large datasets, we might want to use an iterator, 
        # but for 'blood' it might still be large, so we concat and sample.
        print("Fetching cell IDs...")
        obs_df = query.concat().to_pandas()
        print(f"Found {len(obs_df)} matching cells.")
        total_cells = len(obs_df)
        
        if len(obs_df) > max_cells:
            print(f"Sampling {max_cells} cells...")
            obs_df = obs_df.sample(n=max_cells, random_state=42)
            
        obs_soma_joinids = obs_df["soma_joinid"].tolist()
        
        # 2. Fetch AnnData for the selected cells
        print("Fetching expression data (this may take a moment)...")
        adata = cellxgene_census.get_anndata(
            census,
            organism=organism,
            obs_coords=obs_soma_joinids,
            var_value_filter=f"feature_name in {var_names}" if var_names else None
        )
        
        print(f"Successfully loaded data: {adata.shape}")
        return adata, total_cells

if __name__ == "__main__":
    # Test the loader
    adata, total = load_census_data(max_cells=100)
    print(f"Total available: {total}")
    print(adata)
