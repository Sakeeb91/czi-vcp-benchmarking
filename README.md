# CZI CELLxGENE Census - Dataset Exploration

This directory contains tools and examples for exploring the Chan Zuckerberg Initiative's CELLxGENE Census, a comprehensive collection of single-cell RNA sequencing data.

## What is CELLxGENE Census?

The CELLxGENE Census is:
- A unified collection of single-cell RNA-seq data from the CELLxGENE Discover database
- Contains billions of cells from human and mouse organisms
- Data is harmonized using standard ontologies (cell types, tissues, diseases)
- Efficiently queryable using the TileDB-SOMA technology
- Regularly updated with new datasets

## Installation

The main Python package for accessing the Census is `cellxgene-census`:

```bash
pip install cellxgene-census
```

### System Requirements
- Python 3.10 to 3.12
- Recommended: >16 GB RAM and >5 Mbps internet connection

## Available Datasets

The Census contains data for two organisms:
1. **Homo sapiens** (Human)
2. **Mus musculus** (Mouse)

### Data Types Available:
- **Cell Metadata (obs)**: Cell type, tissue, disease, donor information, experimental metadata
- **Gene Metadata (var)**: Gene names, IDs, and other gene-level information
- **Expression Matrix (X)**: Raw count data for gene expression

### Key Statistics (as of 2025-01-30 stable release):
- Billions of cellular observations
- Thousands of unique datasets
- Comprehensive coverage of human and mouse tissues
- Multiple disease states and conditions

## Exploring the Data

### Option 1: Web Interface
Visit [CELLxGENE Discover](https://cellxgene.cziscience.com/) to explore datasets visually.

### Option 2: Python API
Use the scripts in this directory:

- **list_datasets.py** - Get information about available census versions
- **simple_query_example.py** - Basic querying examples
- **explore_datasets.py** - Comprehensive dataset exploration

### Running the Examples

```bash
# List available census versions and information
python3 list_datasets.py

# Run simple query examples
python3 simple_query_example.py
```

## Project Ideas

Here are some small project ideas you can build with this data:

### 1. **Cell Type Classifier** (Beginner)
- **Description**: Build a machine learning model to classify cells by type based on gene expression
- **Data**: Human blood cells from the census
- **Skills**: Python, scikit-learn, pandas
- **Output**: A classifier that can predict cell types from expression data

### 2. **Disease Signature Finder** (Intermediate)
- **Description**: Identify differentially expressed genes between healthy and diseased tissue
- **Data**: Compare disease vs normal samples for a specific tissue
- **Skills**: Statistical analysis, data visualization
- **Output**: List of genes that are markers for specific diseases

### 3. **Tissue-Specific Gene Expression Atlas** (Intermediate)
- **Description**: Create visualizations showing which genes are expressed in which tissues
- **Data**: Cell metadata and expression data across multiple tissues
- **Skills**: Data visualization (matplotlib, seaborn, plotly)
- **Output**: Interactive heatmaps and charts

### 4. **Cell Type Co-occurrence Network** (Intermediate)
- **Description**: Analyze which cell types appear together in the same tissues/samples
- **Data**: Cell metadata from multiple datasets
- **Skills**: Network analysis, graph visualization
- **Output**: Network graph showing cell type relationships

### 5. **Custom Dataset Explorer Dashboard** (Advanced)
- **Description**: Build a Streamlit or Dash web app to interactively query the census
- **Data**: Real-time queries to the census
- **Skills**: Web development, Python, Streamlit/Dash
- **Output**: Interactive web dashboard

### 6. **Gene Expression Anomaly Detector** (Advanced)
- **Description**: Detect unusual expression patterns that might indicate rare cell states
- **Data**: Expression matrices from specific tissues
- **Skills**: Unsupervised learning, anomaly detection
- **Output**: Tool to identify outlier cells

### 7. **Cross-Species Gene Expression Comparator** (Advanced)
- **Description**: Compare human and mouse gene expression for the same tissues
- **Data**: Both human and mouse data from census
- **Skills**: Comparative genomics, data analysis
- **Output**: Analysis of conserved vs divergent expression patterns

## Example Code Snippets

### Basic Query
```python
import cellxgene_census

with cellxgene_census.open_soma(census_version="stable") as census:
    # Get human data
    human = census["census_data"]["homo_sapiens"]

    # Query specific cells
    cells = human["obs"].read(
        column_names=["cell_type", "tissue"],
        value_filter="tissue == 'brain'"
    ).concat().to_pandas()

    print(f"Found {len(cells)} brain cells")
```

### Get Expression Data
```python
import cellxgene_census

with cellxgene_census.open_soma(census_version="stable") as census:
    # Query for expression data
    query = cellxgene_census.get_anndata(
        census,
        organism="homo_sapiens",
        obs_value_filter="tissue == 'lung' and disease == 'COVID-19'",
        var_value_filter="feature_name in ['ACE2', 'TMPRSS2']"
    )

    print(f"Retrieved data shape: {query.shape}")
```

## Recommended Project Structure

For a small project, consider this structure:

```
my-census-project/
├── README.md
├── requirements.txt
├── data/
│   └── (cache and intermediate results)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── analysis.py
│   └── visualization.py
└── results/
    ├── figures/
    └── reports/
```

## Resources

- **Official Documentation**: https://chanzuckerberg.github.io/cellxgene-census/
- **GitHub Repository**: https://github.com/chanzuckerberg/cellxgene-census
- **CELLxGENE Discover**: https://cellxgene.cziscience.com/
- **CZI Science Slack**: https://czi.co/science-slack (#cellxgene-census-users channel)

## Next Steps

1. Run the example scripts in this directory
2. Browse the CELLxGENE Discover web portal
3. Choose a project idea that interests you
4. Create a new directory for your project
5. Start with a small query and iteratively expand

## Notes

- Queries can take time and bandwidth - start small!
- Use the `value_filter` parameter to limit data retrieval
- Cache intermediate results to avoid re-downloading
- Specify `census_version="stable"` for reproducibility
