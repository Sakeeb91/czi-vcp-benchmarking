#!/usr/bin/env python3
"""
Explore CZI CELLxGENE Census datasets
"""

import cellxgene_census
import pandas as pd

def main():
    print("=" * 80)
    print("CZI CELLxGENE Census - Dataset Explorer")
    print("=" * 80)
    print()

    # Open the census
    print("Opening the CELLxGENE Census...")
    census = cellxgene_census.open_soma()

    print("✓ Census opened successfully!")
    print()

    # Get census version info
    print("=" * 80)
    print("CENSUS VERSION INFORMATION")
    print("=" * 80)
    census_info = cellxgene_census.get_census_version_description("latest")
    print(f"Census Build Date: {census_info.get('census_build_date', 'N/A')}")
    print(f"Census Version: {census_info.get('census_version', 'N/A')}")
    print(f"Number of Cells: {census_info.get('total_cell_count', 'N/A'):,}")
    print()

    # Get dataset information
    print("=" * 80)
    print("AVAILABLE DATASETS")
    print("=" * 80)

    # Get the dataset table
    datasets = census["census_info"]["datasets"].read().concat().to_pandas()

    print(f"\nTotal number of datasets: {len(datasets)}")
    print()

    # Show summary statistics
    print("Datasets by collection:")
    collection_counts = datasets.groupby('collection_name').size().sort_values(ascending=False)
    for collection, count in collection_counts.head(10).items():
        print(f"  • {collection}: {count} datasets")

    print()
    print("Datasets by organism:")
    organism_counts = datasets.groupby('dataset_h5ad_path').count()
    if 'organism' in datasets.columns:
        organism_counts = datasets.groupby('organism').size().sort_values(ascending=False)
        for organism, count in organism_counts.head(10).items():
            print(f"  • {organism}: {count} datasets")

    print()
    print("=" * 80)
    print("SAMPLE DATASETS (First 10)")
    print("=" * 80)

    # Display first 10 datasets with key information
    display_cols = ['dataset_id', 'collection_name', 'dataset_title', 'cell_count']
    available_cols = [col for col in display_cols if col in datasets.columns]

    if available_cols:
        sample_datasets = datasets[available_cols].head(10)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 50)
        print(sample_datasets.to_string(index=False))

    print()
    print("=" * 80)
    print("CENSUS DATA STRUCTURE")
    print("=" * 80)
    print("\nAvailable organisms in the census:")
    for organism in census['census_data'].keys():
        print(f"  • {organism}")

        # Get some metadata about this organism
        organism_data = census['census_data'][organism]
        print(f"    - Has expression data: {'obs' in organism_data}")
        print(f"    - Has variable data: {'var' in organism_data}")
        print(f"    - Has X matrix: {'X' in organism_data}")

    print()
    print("=" * 80)
    print("COLUMN INFORMATION")
    print("=" * 80)
    print("\nDataset table columns:")
    for col in datasets.columns:
        print(f"  • {col}")

    # Save datasets to CSV for easier exploration
    output_file = "/Users/sakeeb/Code repositories/vcp dataset exploration/available_datasets.csv"
    datasets.to_csv(output_file, index=False)
    print()
    print(f"✓ Full dataset list saved to: {output_file}")

    # Close the census
    census.close()
    print()
    print("=" * 80)
    print("Exploration complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
