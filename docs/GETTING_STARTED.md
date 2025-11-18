# Getting Started with CZI CELLxGENE Census

## What Was Installed

✅ **cellxgene-census** - Python package for accessing CZI's single-cell RNA-seq data
✅ **Dependencies** - All required packages including pandas, matplotlib, seaborn, etc.

## What You Have

### 1. Main Directory Structure
```
vcp dataset exploration/
├── README.md                    # Overview and project ideas
├── GETTING_STARTED.md          # This file
├── list_datasets.py            # Script to list available datasets
├── simple_query_example.py     # Basic query examples
└── starter-project/            # Ready-to-use project template
```

### 2. Starter Project
A complete, working project located in `starter-project/`:

```
starter-project/
├── README.md                               # Project documentation
├── requirements.txt                        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── data_loader.py                     # Functions to load Census data
│   ├── analyze_cell_types.py             # Main analysis script
│   └── visualization.py                   # Plotting functions
├── notebooks/
│   └── cell_type_exploration.ipynb       # Interactive Jupyter notebook
├── data/                                  # For cached data
└── results/
    └── figures/                           # Output visualizations
```

## Quick Start

### Step 1: Run Example Scripts

Try the simple examples first:

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"

# List available datasets and census versions
python3 list_datasets.py

# Run simple query examples (may take a few minutes)
python3 simple_query_example.py
```

### Step 2: Explore the Starter Project

```bash
cd starter-project

# Run the full analysis (this will download data and create visualizations)
python3 src/analyze_cell_types.py
```

Expected output:
- CSV file: `results/cell_type_summary.csv`
- Visualizations in: `results/figures/`
  - Cell type heatmap
  - Top cell types bar chart
  - Tissue composition pie charts
  - Tissue comparison charts

### Step 3: Interactive Exploration

Use Jupyter notebook for interactive analysis:

```bash
cd starter-project

# Start Jupyter
jupyter notebook notebooks/cell_type_exploration.ipynb
```

## Available Datasets

The CELLxGENE Census contains:

### Organisms
- **Homo sapiens** (Human)
- **Mus musculus** (Mouse)

### Data Types
1. **Cell Metadata** (`obs`)
   - Cell type
   - Tissue
   - Disease state
   - Sex
   - Assay type
   - And more...

2. **Gene Metadata** (`var`)
   - Gene names
   - Gene IDs
   - Feature information

3. **Expression Matrix** (`X`)
   - Raw count data
   - Billions of cells

### Example Tissues Available
- Blood
- Lung
- Brain
- Heart
- Liver
- Kidney
- Pancreas
- Muscle
- Skin
- And many more...

## Project Ideas

See [README.md](README.md) for detailed project ideas, including:

1. **Cell Type Classifier** (Beginner) - ML model to classify cells
2. **Disease Signature Finder** (Intermediate) - Identify disease markers
3. **Tissue-Specific Gene Expression Atlas** (Intermediate) - Visualize gene expression
4. **Cell Type Co-occurrence Network** (Intermediate) - Network analysis
5. **Custom Dataset Explorer Dashboard** (Advanced) - Web app with Streamlit
6. **Gene Expression Anomaly Detector** (Advanced) - Detect unusual patterns
7. **Cross-Species Comparator** (Advanced) - Compare human vs mouse

## Where to Create Your Project

### Option 1: Use the Starter Project
Modify the existing starter project:

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration/starter-project"
# Modify src/analyze_cell_types.py to fit your needs
```

### Option 2: Create a New Project
Create a new directory for a fresh project:

```bash
cd "/Users/sakeeb/Code repositories"
mkdir my-census-project
cd my-census-project

# Copy the starter project as a template
cp -r "vcp dataset exploration/starter-project/"* .

# Or start from scratch
pip install cellxgene-census pandas matplotlib
# ... your code here
```

### Option 3: Inside This Directory
Create a new subdirectory here:

```bash
cd "/Users/sakeeb/Code repositories/vcp dataset exploration"
mkdir my-analysis
cd my-analysis
# ... your code here
```

## Recommended Next Steps

1. **Browse the Web Portal**
   - Visit https://cellxgene.cziscience.com/
   - Explore datasets visually
   - Identify interesting datasets for your project

2. **Run the Examples**
   - Execute the example scripts
   - Understand how queries work
   - Modify parameters to explore different data

3. **Choose a Project**
   - Pick one of the project ideas from README.md
   - Or come up with your own question
   - Start small and iterate

4. **Read the Documentation**
   - Official docs: https://chanzuckerberg.github.io/cellxgene-census/
   - GitHub repo: https://github.com/chanzuckerberg/cellxgene-census
   - Join Slack: https://czi.co/science-slack (#cellxgene-census-users)

## Tips for Success

### Start Small
- Query a limited number of cells initially (1,000-10,000)
- Use specific tissue filters to reduce data size
- Test your analysis on a subset before scaling up

### Use Filters
```python
# Good: Specific query
cell_data = human["obs"].read(
    column_names=["cell_type", "tissue"],
    value_filter="tissue == 'blood' and disease == 'normal'"
)

# Bad: No filter (downloads everything!)
cell_data = human["obs"].read()  # Don't do this!
```

### Cache Your Data
```python
# Save intermediate results
cell_data.to_csv("data/cached_cells.csv")

# Load from cache later
cell_data = pd.read_csv("data/cached_cells.csv")
```

### Specify Version
```python
# Always specify version for reproducibility
census = cellxgene_census.open_soma(census_version="stable")
# Or specific version:
census = cellxgene_census.open_soma(census_version="2025-01-30")
```

## Troubleshooting

### Memory Issues
If you run out of memory:
- Reduce `max_cells_per_tissue` parameter
- Query fewer tissues at once
- Use more specific filters
- Process data in chunks

### Slow Queries
If queries are slow:
- Check your internet connection
- Reduce the amount of data requested
- Use column filters to select only needed fields
- Consider caching results

### Version Conflicts
If you see version errors:
```bash
pip install --upgrade cellxgene-census tiledbsoma
```

## Example: Quick Analysis

Here's a minimal example to get started:

```python
import cellxgene_census
import pandas as pd

# Open census
with cellxgene_census.open_soma(census_version="stable") as census:
    # Get human data
    human = census["census_data"]["homo_sapiens"]

    # Query blood cells
    cells = human["obs"].read(
        column_names=["cell_type", "disease"],
        value_filter="tissue == 'blood'"
    ).concat().to_pandas()

    # Analyze
    print(f"Found {len(cells):,} blood cells")
    print("\nTop cell types:")
    print(cells['cell_type'].value_counts().head(10))
```

## Resources

- **This Directory**: [README.md](README.md) - Comprehensive overview
- **Starter Project**: `starter-project/README.md` - Project-specific docs
- **Official Docs**: https://chanzuckerberg.github.io/cellxgene-census/
- **Web Portal**: https://cellxgene.cziscience.com/
- **GitHub**: https://github.com/chanzuckerberg/cellxgene-census
- **Community**: https://czi.co/science-slack

---

**Happy exploring! 🔬🧬**
