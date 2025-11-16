# Cell Type Distribution Analysis

A starter project for analyzing cell type distributions across different tissues using the CZI CELLxGENE Census.

## Project Goal

Analyze and visualize the distribution of different cell types across human tissues to understand cellular composition and identify tissue-specific patterns.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the analysis:
```bash
python src/analyze_cell_types.py
```

3. Or explore interactively:
```bash
jupyter notebook notebooks/cell_type_exploration.ipynb
```

## Project Structure

```
starter-project/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── data_loader.py                 # Functions to load Census data
│   ├── analyze_cell_types.py         # Main analysis script
│   └── visualization.py               # Plotting functions
├── notebooks/
│   └── cell_type_exploration.ipynb   # Interactive exploration
├── data/                              # Cached data (gitignored)
└── results/
    └── figures/                       # Output visualizations
```

## Analysis Steps

1. **Data Loading**: Query the Census for cell metadata from multiple tissues
2. **Data Processing**: Count cell types per tissue
3. **Visualization**: Create heatmaps and bar charts
4. **Analysis**: Identify tissue-specific cell populations

## Expected Outputs

- Heatmap of cell types vs tissues
- Bar charts showing cell type distributions
- CSV file with summary statistics
- PDF report with key findings

## Customization

You can modify this project to:
- Focus on specific tissues or cell types
- Add disease state comparisons
- Include gene expression analysis
- Compare human vs mouse data

## Resources

- [CELLxGENE Census Documentation](https://chanzuckerberg.github.io/cellxgene-census/)
- [Cell Ontology Browser](https://www.ebi.ac.uk/ols/ontologies/cl)
- [Tissue Ontology](https://www.ebi.ac.uk/ols/ontologies/uberon)
