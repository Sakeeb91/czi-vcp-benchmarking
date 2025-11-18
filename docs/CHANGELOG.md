# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-15

### Added - Initial Release

#### Documentation
- Comprehensive main README with project overview
- Complete navigation index (INDEX.md)
- Getting started guide with installation steps
- Project summary with recommended ideas
- Detailed benchmarking guide for cz-benchmarks
- Quick start benchmarking guide
- Installation completion summary
- cz-benchmarks usage guide

#### Projects
- **Starter Project**: Cell type distribution analysis
  - Data loading from CELLxGENE Census
  - Visualization module with 4 plot types
  - Main analysis script with CLI
  - Interactive Jupyter notebook

- **Model Benchmarking Framework**:
  - Baseline models registry (RF, XGBoost, LR, etc.)
  - Evaluation utilities with metrics
  - Cell type classification benchmark
  - Results export and visualization

#### Example Scripts
- list_datasets.py - List Census versions and metadata
- simple_query_example.py - Basic Census queries
- explore_datasets.py - Comprehensive data exploration

#### Configuration
- .gitignore for Python projects
- Requirements files for both projects
- Virtual environment support (Python 3.13 & 3.14)

### Technical Details

#### Python Versions
- Global Python 3.14.0 (Homebrew)
- Benchmarking Python 3.13.9 (venv-benchmarks)
- System Python 3.9.6 (macOS)

#### Key Dependencies
- cz-benchmarks 0.15.0
- cellxgene-census 1.15.0
- scanpy 1.11.5
- scikit-learn 1.7.2
- numpy 2.3.4
- pandas 2.3.3

#### Features
- Access to billions of single-cell RNA-seq data points
- 6 standardized benchmark tasks
- Multiple ML model comparison
- Publication-quality visualizations
- Comprehensive documentation

### System Requirements
- macOS (tested on Sequoia, Apple Silicon)
- 16+ GB RAM recommended
- Stable internet connection
- 10+ GB storage for environments

## Future Plans

### Planned Features
- [ ] Additional benchmark tasks (clustering, integration)
- [ ] Deep learning models (PyTorch/TensorFlow)
- [ ] Interactive Streamlit dashboard
- [ ] Automated result reporting
- [ ] CI/CD integration
- [ ] Docker support
- [ ] Additional example notebooks

### Potential Improvements
- [ ] Performance optimization for large datasets
- [ ] Caching layer for frequently used data
- [ ] Multi-species analysis tools
- [ ] Disease-specific benchmarks
- [ ] Transfer learning examples

## Notes

### Known Issues
- Python 3.14 not yet compatible with cz-benchmarks (use 3.13)
- Large dataset queries may be slow on limited bandwidth
- Some visualizations require manual color palette adjustment

### Breaking Changes
None (initial release)

---

**Maintained by**: Sakeeb Rahman (@Sakeeb91)
**Contact**: rahman.sakeeb@gmail.com
**Last Updated**: November 15, 2025
