#!/usr/bin/env python3
"""
List available CZI CELLxGENE Census datasets without opening the full census
"""

import cellxgene_census
import pandas as pd

def main():
    print("=" * 80)
    print("CZI CELLxGENE Census - Dataset Lister")
    print("=" * 80)
    print()

    # Get census version information
    print("Getting census version information...")
    try:
        census_versions = cellxgene_census.get_census_version_directory()
        print(f"✓ Found {len(census_versions)} census versions")
        print()

        print("Available Census Versions:")
        for idx, version in enumerate(census_versions[:5]):
            print(f"  {idx+1}. Version: {version.get('census_version', 'N/A')}")
            print(f"     Build Date: {version.get('census_build_date', 'N/A')}")
            print(f"     Release Build: {version.get('release_build', 'N/A')}")
            if 'soma' in version:
                print(f"     SOMA Encoding: {version.get('soma', {}).get('uri', 'N/A')}")
            print()

        # Get the latest stable version info
        print("=" * 80)
        print("LATEST STABLE VERSION INFO")
        print("=" * 80)
        latest = cellxgene_census.get_census_version_description("stable")
        print(f"Census Version: {latest.get('census_version', 'N/A')}")
        print(f"Build Date: {latest.get('census_build_date', 'N/A')}")
        print(f"Total Cell Count: {latest.get('total_cell_count', 'N/A'):,}")
        print(f"Unique Dataset Count: {latest.get('unique_dataset_count', 'N/A')}")
        print()

        # Try to get dataset summaries
        print("=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)
        print()
        print("The CELLxGENE Census contains single-cell RNA-seq data from:")
        print("  • Human (Homo sapiens)")
        print("  • Mouse (Mus musculus)")
        print()
        print("Key features:")
        print("  • All data harmonized to standard ontologies")
        print("  • Efficient querying through TileDB-SOMA")
        print("  • Regular updates with new datasets")
        print("  • Access to raw count matrices")
        print("  • Cell and gene metadata")
        print()

    except Exception as e:
        print(f"Error: {e}")
        print("\nTrying alternative approach...")

    print("=" * 80)
    print("ACCESSING DATASETS")
    print("=" * 80)
    print()
    print("To explore datasets in detail, you can:")
    print("  1. Use the CELLxGENE Discover web portal: https://cellxgene.cziscience.com/")
    print("  2. Use the Census Python API with specific queries")
    print("  3. Download specific datasets in H5AD format")
    print()

    print("Example code to query the census:")
    print()
    print("```python")
    print("import cellxgene_census")
    print()
    print("# Open the census (specify version to avoid warnings)")
    print('census = cellxgene_census.open_soma(census_version="stable")')
    print()
    print("# Get human data")
    print('human = census["census_data"]["homo_sapiens"]')
    print()
    print("# Query cell metadata")
    print('cell_metadata = human["obs"].read(column_names=["cell_type", "tissue", "disease"])')
    print()
    print("# Close when done")
    print("census.close()")
    print("```")
    print()

if __name__ == "__main__":
    main()
