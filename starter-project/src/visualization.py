"""
Visualization functions for cell type analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path


def plot_cell_type_heatmap(
    summary_df: pd.DataFrame,
    output_path: str = "results/figures/cell_type_heatmap.png",
    figsize: tuple = (12, 10)
):
    """
    Create a heatmap showing cell type distribution across tissues.

    Parameters:
    -----------
    summary_df : pd.DataFrame
        Pivot table with cell types as rows and tissues as columns
    output_path : str
        Path to save the figure
    figsize : tuple
        Figure size (width, height)
    """
    plt.figure(figsize=figsize)

    # Log transform for better visualization
    plot_data = summary_df.apply(lambda x: x + 1).apply(lambda x: x.astype(float))

    sns.heatmap(
        plot_data,
        cmap="YlOrRd",
        cbar_kws={'label': 'Cell Count (log scale)'},
        linewidths=0.5,
        linecolor='lightgray'
    )

    plt.title("Cell Type Distribution Across Tissues", fontsize=16, pad=20)
    plt.xlabel("Tissue", fontsize=12)
    plt.ylabel("Cell Type", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved heatmap to {output_path}")
    plt.close()


def plot_top_cell_types(
    cell_data: pd.DataFrame,
    top_n: int = 20,
    output_path: str = "results/figures/top_cell_types.png",
    figsize: tuple = (10, 8)
):
    """
    Create a bar chart of the most abundant cell types.

    Parameters:
    -----------
    cell_data : pd.DataFrame
        Cell metadata
    top_n : int
        Number of top cell types to show
    output_path : str
        Path to save the figure
    figsize : tuple
        Figure size
    """
    plt.figure(figsize=figsize)

    cell_type_counts = cell_data['cell_type'].value_counts().head(top_n)

    sns.barplot(
        x=cell_type_counts.values,
        y=cell_type_counts.index,
        palette="viridis"
    )

    plt.title(f"Top {top_n} Most Abundant Cell Types", fontsize=16, pad=20)
    plt.xlabel("Number of Cells", fontsize=12)
    plt.ylabel("Cell Type", fontsize=12)
    plt.tight_layout()

    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved bar chart to {output_path}")
    plt.close()


def plot_tissue_composition(
    cell_data: pd.DataFrame,
    tissue: str,
    output_path: str = None,
    figsize: tuple = (10, 8)
):
    """
    Create a pie chart showing cell type composition for a specific tissue.

    Parameters:
    -----------
    cell_data : pd.DataFrame
        Cell metadata
    tissue : str
        Tissue name to plot
    output_path : str
        Path to save the figure
    figsize : tuple
        Figure size
    """
    tissue_data = cell_data[cell_data['tissue'] == tissue]

    if len(tissue_data) == 0:
        print(f"Warning: No data found for tissue '{tissue}'")
        return

    plt.figure(figsize=figsize)

    cell_type_counts = tissue_data['cell_type'].value_counts().head(10)

    plt.pie(
        cell_type_counts.values,
        labels=cell_type_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )

    plt.title(f"Cell Type Composition in {tissue.title()}", fontsize=16, pad=20)
    plt.axis('equal')

    if output_path is None:
        output_path = f"results/figures/{tissue.replace(' ', '_')}_composition.png"

    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved pie chart to {output_path}")
    plt.close()


def plot_tissue_comparison(
    cell_data: pd.DataFrame,
    tissues: list,
    output_path: str = "results/figures/tissue_comparison.png",
    figsize: tuple = (14, 6)
):
    """
    Create a grouped bar chart comparing cell types across tissues.

    Parameters:
    -----------
    cell_data : pd.DataFrame
        Cell metadata
    tissues : list
        List of tissues to compare
    output_path : str
        Path to save the figure
    figsize : tuple
        Figure size
    """
    # Filter for selected tissues
    filtered_data = cell_data[cell_data['tissue'].isin(tissues)]

    # Get top cell types across these tissues
    top_cell_types = filtered_data['cell_type'].value_counts().head(15).index

    # Filter for top cell types
    plot_data = filtered_data[filtered_data['cell_type'].isin(top_cell_types)]

    # Create cross-tabulation
    ct = pd.crosstab(plot_data['cell_type'], plot_data['tissue'])

    fig, ax = plt.subplots(figsize=figsize)
    ct.plot(kind='bar', ax=ax, width=0.8)

    plt.title("Cell Type Distribution Across Selected Tissues", fontsize=16, pad=20)
    plt.xlabel("Cell Type", fontsize=12)
    plt.ylabel("Number of Cells", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Tissue", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Create output directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved comparison chart to {output_path}")
    plt.close()
