#!/usr/bin/env python3
"""
Simple example of querying the CZI CELLxGENE Census
This script demonstrates basic queries without downloading large amounts of data
"""

import cellxgene_census
import pandas as pd

def main():
    print("=" * 80)
    print("CZI CELLxGENE Census - Simple Query Example")
    print("=" * 80)
    print()

    print("Opening the census (stable version to ensure consistency)...")
    # Open the stable census version
    with cellxgene_census.open_soma(census_version="stable") as census:
        print("✓ Census opened successfully!")
        print()

        # Example 1: Get a small sample of human cell metadata
        print("=" * 80)
        print("EXAMPLE 1: Sample Human Cell Metadata")
        print("=" * 80)
        print("\nQuerying first 1000 human cells...")

        human = census["census_data"]["homo_sapiens"]

        # Read a small sample of cell metadata
        cell_metadata = human["obs"].read(
            column_names=["cell_type", "tissue", "disease", "sex", "organism"],
            value_filter="tissue == 'blood'"  # Filter for blood tissue
        ).concat().to_pandas()

        # Limit to first 1000 rows
        sample = cell_metadata.head(1000)

        print(f"\nRetrieved {len(sample)} cells from blood tissue")
        print("\nCell Type Distribution:")
        print(sample['cell_type'].value_counts().head(10))

        print("\nDisease Distribution:")
        print(sample['disease'].value_counts().head(5))

        print()

        # Example 2: Get gene information
        print("=" * 80)
        print("EXAMPLE 2: Gene Information")
        print("=" * 80)
        print("\nQuerying gene metadata...")

        var = human["var"].read().concat().to_pandas()
        print(f"\nTotal genes in dataset: {len(var)}")
        print("\nFirst 10 genes:")
        print(var.head(10)[['feature_name', 'feature_id']])

        print()

        # Example 3: Summary statistics
        print("=" * 80)
        print("EXAMPLE 3: Available Tissues in Human Data")
        print("=" * 80)

        # Get unique tissues (using a limited query)
        tissue_query = human["obs"].read(
            column_names=["tissue"]
        ).concat().to_pandas()

        print("\nUnique tissues available:")
        tissues = tissue_query['tissue'].value_counts().head(20)
        for tissue, count in tissues.items():
            print(f"  • {tissue}: {count:,} cells")

        print()

    print("=" * 80)
    print("Query complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
