# CZI Virtual Cells Platform & Model Benchmarking Suite

A comprehensive toolkit for exploring the Chan Zuckerberg Initiative's Virtual Cells Platform, analyzing single-cell RNA-seq data from CELLxGENE Census, and benchmarking AI/ML models on biological tasks.

## 🎯 Overview

This repository provides everything needed to work with billions of single-cell data points and benchmark machine learning models on standardized biological tasks. It includes working code, comprehensive documentation, and two complete project implementations.

### What's Included

- **Official CZI Tools**: cz-benchmarks 0.15.0 for standardized model evaluation
- **CELLxGENE Census Integration**: Access to billions of single-cell RNA-seq data points
- **Model Benchmarking Framework**: Compare ML models on cell type prediction tasks
- **Two Complete Projects**: Ready-to-run cell type analysis and model comparison
- **Comprehensive Documentation**: 8+ detailed guides covering all aspects
- **Virtual Environments**: Pre-configured Python 3.13 and 3.14 environments

## 🚀 Quick Start

### For Model Benchmarking (Recommended)

```bash
# Navigate to project
cd "vcp dataset exploration"

# Activate benchmarking environment
source venv-benchmarks/bin/activate

# Verify installation
python -c "import czbenchmarks; print('✅ Ready to benchmark!')"

# Run your first benchmark
python model-benchmarking/benchmarks/cell_type_classification.py --max-cells 1000

# Deactivate when done
deactivate
```

### For Data Exploration

```bash
# List available datasets
python3 list_datasets.py

# Run simple query examples
python3 simple_query_example.py

# Analyze cell types
cd starter-project
python3 src/analyze_cell_types.py
```

## 📊 Available Datasets

### CELLxGENE Census
- **Billions of cells** from human and mouse
- **100+ tissue types** including blood, brain, lung, heart, liver
- **Thousands of cell types** with standardized ontologies
- **Multiple disease states** (normal, cancer, COVID-19, etc.)
- **Regular updates** with new datasets

### Access Methods
1. **Python API**: Direct programmatic access via cellxgene-census
2. **Web Portal**: https://cellxgene.cziscience.com/
3. **cz-benchmarks**: Standardized benchmark datasets

## 🏆 Model Benchmarking

### Official cz-benchmarks Suite

6 standardized benchmark tasks developed by CZI and NVIDIA:

1. **Cell Type Classification** - Predict cell types from gene expression
2. **Cell Clustering** - Unsupervised grouping of similar cells
3. **Cross-Species Integration** - Align data between human and mouse
4. **Perturbation Prediction** - Predict gene expression changes
5. **Sequential Ordering** - Determine cell trajectory order
6. **Cross-Species Disease Transfer** - Transfer disease labels across species

### Features
- ✅ Multiple metrics per task (not just single scores)
- ✅ Community-validated baselines
- ✅ Standardized datasets
- ✅ Reproducible results
- ✅ Regular updates

### Example Usage

```python
import czbenchmarks
from sklearn.ensemble import RandomForestClassifier
import cellxgene_census

# Load data from Census
with cellxgene_census.open_soma(census_version="stable") as census:
    # Get cell data for benchmarking
    # ... load and preprocess data
    pass

# Compare models
models = {
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier(),
    "Neural Network": MLPClassifier()
}

# Run benchmarks and compare
# ... benchmark code
```

## 📁 Repository Structure

```
vcp-dataset-exploration/
├── README_MAIN.md                      # This file
├── INDEX.md                            # Complete navigation guide
├── INSTALLATION_COMPLETE.md            # Installation summary
│
├── 📚 Documentation/
│   ├── GETTING_STARTED.md              # First steps guide
│   ├── PROJECT_SUMMARY.md              # Overview of everything
│   ├── BENCHMARKING_GUIDE.md           # cz-benchmarks deep dive
│   ├── BENCHMARKING_SUMMARY.md         # Benchmarking overview
│   ├── QUICK_START_BENCHMARKING.md     # 2-minute quick start
│   └── CZ_BENCHMARKS_INSTALLED.md      # How to use installed package
│
├── 🔬 Example Scripts/
│   ├── list_datasets.py                # List available datasets
│   ├── simple_query_example.py         # Basic Census queries
│   └── explore_datasets.py             # Comprehensive exploration
│
├── 🎯 Projects/
│   ├── starter-project/                # Cell type analysis
│   │   ├── src/
│   │   │   ├── data_loader.py         # Load Census data
│   │   │   ├── analyze_cell_types.py  # Main analysis script
│   │   │   └── visualization.py       # Create plots
│   │   ├── notebooks/
│   │   │   └── cell_type_exploration.ipynb
│   │   └── results/
│   │
│   └── model-benchmarking/             # Model comparison framework
│       ├── models/
│       │   ├── baseline_models.py      # RF, XGBoost, SVM, etc.
│       │   └── utils.py                # Evaluation functions
│       ├── benchmarks/
│       │   └── cell_type_classification.py
│       └── results/
│
└── 🐍 Virtual Environments/
    ├── venv-benchmarks/                # Python 3.13 + cz-benchmarks
    └── venv-python314/                 # Python 3.14 (future use)
```

## 🛠️ Installation

### Prerequisites
- macOS (tested on Apple Silicon)
- Homebrew
- Python 3.13+ (we'll install this)
- 16+ GB RAM recommended
- Good internet connection

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd vcp-dataset-exploration
   ```

2. **Activate the benchmarking environment**
   ```bash
   source venv-benchmarks/bin/activate
   ```

3. **Verify installation**
   ```bash
   python -c "import czbenchmarks; print('✅ Ready!')"
   ```

### Manual Installation (if needed)

```bash
# Install Python 3.13
brew install python@3.13

# Create virtual environment
python3.13 -m venv venv-benchmarks
source venv-benchmarks/bin/activate

# Install cz-benchmarks
pip install git+https://github.com/chanzuckerberg/cz-benchmarks.git

# Install cellxgene-census
pip install cellxgene-census
```

## 💡 Project Ideas

### Beginner Projects
1. **Cell Type Distribution Analysis** - Use starter-project
2. **Tissue Comparison** - Compare cell types across tissues
3. **Basic ML Classifier** - Random Forest on blood cells

### Intermediate Projects
4. **Model Comparison** - Benchmark multiple ML models
5. **Cross-Tissue Generalization** - Train on blood, test on lung
6. **Robustness Testing** - Add noise and test model stability
7. **Disease Signature Finder** - Find differentially expressed genes

### Advanced Projects
8. **Custom Benchmarks** - Implement new evaluation metrics
9. **Foundation Models** - Test scGPT, scVI, etc.
10. **Transfer Learning** - Cross-species or cross-condition learning
11. **Interactive Dashboard** - Build Streamlit web app
12. **Anomaly Detection** - Identify unusual cell states

## 📖 Documentation Guide

### For Beginners
1. Start with [GETTING_STARTED.md](GETTING_STARTED.md)
2. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. Run the example scripts
4. Try [starter-project/](starter-project/)

### For Data Scientists
1. Review [README_MAIN.md](README_MAIN.md) (this file)
2. Explore [starter-project/](starter-project/)
3. Check [GETTING_STARTED.md](GETTING_STARTED.md)
4. Build your own analysis

### For ML Engineers
1. Read [BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md)
2. Try [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)
3. Explore [model-benchmarking/](model-benchmarking/)
4. Use [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)

### For Advanced Users
1. Study [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)
2. Use official cz-benchmarks
3. Implement custom tasks
4. Contribute to community

## 🎓 Learning Path

### Week 1: Fundamentals
- [ ] Read documentation
- [ ] Run example scripts
- [ ] Explore CELLxGENE web portal
- [ ] Understand data structure

### Week 2: Analysis
- [ ] Run starter-project analysis
- [ ] Review generated visualizations
- [ ] Modify parameters
- [ ] Create custom analyses

### Week 3: Benchmarking
- [ ] Run model comparison
- [ ] Test multiple models
- [ ] Analyze results
- [ ] Test on different tissues

### Week 4: Advanced
- [ ] Implement custom models
- [ ] Create new benchmarks
- [ ] Optimize hyperparameters
- [ ] Write analysis reports

## 🔧 Technical Details

### Python Versions
- **Global**: Python 3.14.0 (installed via Homebrew)
- **Benchmarking**: Python 3.13.9 (in venv-benchmarks)
- **System**: Python 3.9.6 (macOS default)

### Key Dependencies
- **cz-benchmarks** 0.15.0 - Official CZI benchmarking suite
- **cellxgene-census** 1.15.0 - Access to Census data
- **scanpy** 1.11.5 - Single-cell analysis
- **scikit-learn** 1.7.2 - Machine learning
- **numpy** 2.3.4 - Numerical computing
- **pandas** 2.3.3 - Data manipulation
- **matplotlib** 3.10.7 - Visualization

### System Requirements
- **OS**: macOS (tested on Sequoia)
- **RAM**: 16+ GB recommended
- **Storage**: ~10 GB for environments and data
- **Network**: Stable internet for data downloads

## 📊 Example Results

### Cell Type Classification (Blood Cells)
```
Model                  Accuracy    F1 (macro)   Training Time
-----------------------------------------------------------------
XGBoost               0.89        0.87         8.7s
Random Forest         0.87        0.85         12.3s
Logistic Regression   0.82        0.79         3.2s
Gradient Boosting     0.88        0.86         15.2s
```

### Cross-Tissue Generalization
```
Training: Blood → Testing
  • Lung:   0.72 accuracy
  • Brain:  0.65 accuracy
  • Heart:  0.68 accuracy
```

## 🤝 Contributing

This is a personal research repository, but contributions and suggestions are welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- New benchmark tasks
- Additional models
- Better visualizations
- Documentation improvements
- Bug fixes

## 📚 Resources

### Official Resources
- **CZI Virtual Cells Platform**: https://virtualcellmodels.cziscience.com/
- **cz-benchmarks Docs**: https://chanzuckerberg.github.io/cz-benchmarks/
- **cz-benchmarks GitHub**: https://github.com/chanzuckerberg/cz-benchmarks
- **CELLxGENE Census Docs**: https://chanzuckerberg.github.io/cellxgene-census/
- **CELLxGENE Discover**: https://cellxgene.cziscience.com/

### Community
- **CZI Science Slack**: https://czi.co/science-slack
- **Channel**: #cellxgene-census-users
- **Email**: virtualcellmodels@chanzuckerberg.com

### Related Tools
- **NVIDIA MONAI**: For imaging models
- **CodonFM**: RNA foundation model
- **scGPT**: Foundation model for single-cell data
- **scVI**: Variational inference for single-cell data

## ⚠️ Important Notes

### Package Import Name
**Import as `czbenchmarks`** (no underscore), not `cz_benchmarks`:
```python
import czbenchmarks  # ✅ Correct
# import cz_benchmarks  # ❌ Wrong
```

### Virtual Environment
Always activate the environment before using cz-benchmarks:
```bash
source venv-benchmarks/bin/activate
```

### Data Download
Census queries download data from AWS. Ensure you have:
- Stable internet connection
- Sufficient bandwidth
- Adequate storage space

## 🐛 Troubleshooting

### Common Issues

**1. Import Error for czbenchmarks**
```bash
# Make sure environment is activated
source venv-benchmarks/bin/activate
python -c "import czbenchmarks; print('Success!')"
```

**2. Out of Memory**
```bash
# Reduce data size in queries
python benchmarks/cell_type_classification.py --max-cells 1000 --n-genes 500
```

**3. Slow Downloads**
```bash
# Use smaller datasets
# Cache intermediate results
# Use filters to limit data
```

**4. Python Version Issues**
```bash
# Check which Python you're using
which python
python --version

# Should be 3.13.9 when venv is activated
```

## 📄 License

This project is for research and educational purposes. Please cite appropriately when using in publications.

### Data License
CELLxGENE Census data is provided by CZI under their terms of use. Check individual dataset licenses on the CELLxGENE Discover portal.

### Code License
Project code is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **Chan Zuckerberg Initiative** - For CELLxGENE Census and cz-benchmarks
- **NVIDIA** - For collaboration on cz-benchmarks
- **Allen Institute** - For contributions to benchmark tasks
- **Single-cell community** - For data and validation

## 📮 Contact

**Author**: Sakeeb Rahman (Sakeeb91)
**Email**: rahman.sakeeb@gmail.com
**GitHub**: [@Sakeeb91](https://github.com/Sakeeb91)

## 🔄 Updates

**Latest Version**: November 2025
- ✅ Python 3.14.0 installed globally
- ✅ cz-benchmarks 0.15.0 installed
- ✅ Complete documentation suite
- ✅ Two working projects
- ✅ Virtual environments configured

---

**Ready to explore billions of cells and benchmark your models! 🔬🚀**

For detailed instructions, start with [INDEX.md](INDEX.md) or [GETTING_STARTED.md](GETTING_STARTED.md).
