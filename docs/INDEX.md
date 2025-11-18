# CZI Virtual Cells Platform - Complete Index

## 📖 Documentation Overview

This directory contains everything you need to work with the Chan Zuckerberg Initiative's Virtual Cells Platform, CELLxGENE Census data, and model benchmarking tools.

## 🎯 Start Here Based on Your Goal

### I Want to...

#### 1. Get Started with CZI Data
→ Read **[GETTING_STARTED.md](GETTING_STARTED.md)**
- Installation guide
- First steps
- Running examples
- Troubleshooting

#### 2. Understand What's Available
→ Read **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
- What was installed
- Available datasets
- Project ideas
- Quick start guide

#### 3. Explore Datasets
→ Read **[README.md](README.md)**
- Detailed overview of CELLxGENE Census
- 7 project ideas with descriptions
- Example code snippets
- Resources

#### 4. Benchmark AI Models
→ Read **[BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md)**
- Complete benchmarking overview
- What's possible
- Current vs future options
- Migration path

#### 5. Start Benchmarking RIGHT NOW
→ Read **[QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)**
- 2-minute quick start
- Copy-paste commands
- Immediate results

#### 6. Deep Dive into cz-benchmarks
→ Read **[BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)**
- Official cz-benchmarks package
- All 6 benchmark tasks
- Requirements and installation
- Detailed examples

## 📂 Directory Structure

```
vcp dataset exploration/
│
├── 📄 Documentation (You are here!)
│   ├── INDEX.md                        # This file - Start here!
│   ├── GETTING_STARTED.md              # First steps guide
│   ├── PROJECT_SUMMARY.md              # Overview of what's available
│   ├── README.md                       # Detailed project ideas
│   ├── BENCHMARKING_SUMMARY.md         # Benchmarking overview
│   ├── BENCHMARKING_GUIDE.md           # cz-benchmarks deep dive
│   └── QUICK_START_BENCHMARKING.md     # 2-min quick start
│
├── 🔬 Example Scripts
│   ├── list_datasets.py                # List available datasets
│   ├── simple_query_example.py         # Basic Census queries
│   └── explore_datasets.py             # Comprehensive exploration
│
├── 🎯 Starter Project (Cell Type Analysis)
│   └── starter-project/
│       ├── README.md
│       ├── requirements.txt
│       ├── src/
│       │   ├── data_loader.py
│       │   ├── analyze_cell_types.py
│       │   └── visualization.py
│       ├── notebooks/
│       │   └── cell_type_exploration.ipynb
│       └── results/
│
└── 🏆 Model Benchmarking Project
    └── model-benchmarking/
        ├── README.md
        ├── requirements.txt
        ├── models/
        │   ├── baseline_models.py      # RF, XGBoost, etc.
        │   └── utils.py                # Evaluation functions
        ├── benchmarks/
        │   └── cell_type_classification.py
        └── results/
```

## 🚀 Quick Navigation by Task

### Task 1: Explore Available Data
```bash
# See what's available
python3 list_datasets.py

# Run simple queries
python3 simple_query_example.py
```
**Learn More**: [GETTING_STARTED.md](GETTING_STARTED.md#exploring-the-data)

### Task 2: Analyze Cell Types
```bash
cd starter-project
python3 src/analyze_cell_types.py
```
**Learn More**: [starter-project/README.md](starter-project/README.md)

### Task 3: Compare ML Models
```bash
cd model-benchmarking
python3 benchmarks/cell_type_classification.py
```
**Learn More**: [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)

### Task 4: Interactive Exploration
```bash
cd starter-project
jupyter notebook notebooks/cell_type_exploration.ipynb
```
**Learn More**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#option-3-interactive-exploration-30-minutes)

## 📚 Documentation Guide

### For Beginners
1. [GETTING_STARTED.md](GETTING_STARTED.md) - Start here
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Understand what you have
3. Run the example scripts
4. Try [starter-project/](starter-project/)

### For Data Scientists
1. [README.md](README.md) - See project ideas
2. [GETTING_STARTED.md](GETTING_STARTED.md) - Setup guide
3. [starter-project/](starter-project/) - Working examples
4. Build your own project

### For ML Engineers
1. [BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md) - Overview
2. [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md) - Get started fast
3. [model-benchmarking/](model-benchmarking/) - Working project
4. [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md) - Deep dive

### For Advanced Users
1. [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md) - Official cz-benchmarks
2. Upgrade to Python 3.10+
3. Install cz-benchmarks from GitHub
4. Use standardized benchmarks

## 🎓 Learning Path

### Week 1: Basics
- [ ] Read [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Run `list_datasets.py`
- [ ] Run `simple_query_example.py`
- [ ] Explore web portal: https://cellxgene.cziscience.com/

### Week 2: Analysis
- [ ] Run `starter-project/src/analyze_cell_types.py`
- [ ] Review generated visualizations
- [ ] Open Jupyter notebook
- [ ] Modify analysis parameters

### Week 3: Benchmarking
- [ ] Read [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)
- [ ] Run `model-benchmarking/benchmarks/cell_type_classification.py`
- [ ] Compare different models
- [ ] Test on multiple tissues

### Week 4: Advanced
- [ ] Create your own project
- [ ] Implement custom models
- [ ] Upgrade to Python 3.10+
- [ ] Use official cz-benchmarks

## 🔑 Key Files

### Must Read
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Essential first steps
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What you have and how to use it

### Project-Specific
- **[starter-project/README.md](starter-project/README.md)** - Cell type analysis
- **[model-benchmarking/README.md](model-benchmarking/README.md)** - Model comparison

### Reference
- **[README.md](README.md)** - Comprehensive overview
- **[BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)** - cz-benchmarks reference

### Quick Reference
- **[QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)** - Fast commands
- **[INDEX.md](INDEX.md)** - This file (navigation hub)

## 💡 Suggested Projects

### Beginner
1. **Cell Type Distribution** - Use starter-project
2. **Tissue Comparison** - Compare cell types across tissues
3. **Basic ML Classifier** - Random Forest on blood cells

### Intermediate
4. **Model Comparison** - Use model-benchmarking project
5. **Cross-Tissue Generalization** - Train on blood, test on lung
6. **Robustness Testing** - Add noise and test stability

### Advanced
7. **Custom Benchmarks** - Implement new evaluation metrics
8. **Foundation Models** - Test scGPT, scVI, etc.
9. **Transfer Learning** - Cross-species or cross-condition

**Full list**: [README.md](README.md#project-ideas)

## 🛠️ Tools Installed

- ✅ **cellxgene-census** - Access billions of single-cell data points
- ✅ **scikit-learn, xgboost** - Machine learning models
- ✅ **pandas, numpy** - Data manipulation
- ✅ **matplotlib, seaborn** - Visualization
- ⏳ **cz-benchmarks** - Requires Python 3.10+ (placeholder installed)

## 📊 Available Data

### Organisms
- Human (Homo sapiens)
- Mouse (Mus musculus)

### Scale
- Billions of cells
- 100+ tissue types
- Thousands of cell types
- Multiple disease states

### Access Methods
- CELLxGENE Census Python API (installed)
- Web portal: https://cellxgene.cziscience.com/
- cz-benchmarks (Python 3.10+)

## 🎯 Your Answer: Model Benchmarking

**Your Question**: Can I benchmark AI models on biological tasks?

**Answer**: **YES!**

**Two Options**:

1. **Now (Python 3.9)**: Use [model-benchmarking/](model-benchmarking/)
   - Quick start: [QUICK_START_BENCHMARKING.md](QUICK_START_BENCHMARKING.md)

2. **Future (Python 3.10+)**: Use official cz-benchmarks
   - Guide: [BENCHMARKING_GUIDE.md](BENCHMARKING_GUIDE.md)

**Summary**: [BENCHMARKING_SUMMARY.md](BENCHMARKING_SUMMARY.md)

## 📞 Getting Help

### Documentation Issues
- Re-read [GETTING_STARTED.md](GETTING_STARTED.md)
- Check troubleshooting sections

### Technical Issues
- GitHub: https://github.com/chanzuckerberg/cellxgene-census/issues
- Email: virtualcellmodels@chanzuckerberg.com
- Slack: https://czi.co/science-slack

### Questions
- Check the relevant README files
- Review example code
- Ask in CZI Slack community

## 🌐 External Resources

- **CELLxGENE Discover**: https://cellxgene.cziscience.com/
- **Census Docs**: https://chanzuckerberg.github.io/cellxgene-census/
- **cz-benchmarks**: https://chanzuckerberg.github.io/cz-benchmarks/
- **Virtual Cells Platform**: https://virtualcellmodels.cziscience.com/
- **CZI Science Slack**: https://czi.co/science-slack

## ✅ Next Steps

### Immediate (Today)
1. [ ] Choose your starting point from "I Want to..." above
2. [ ] Read the recommended documentation
3. [ ] Run your first example script

### This Week
1. [ ] Complete the Week 1 learning path
2. [ ] Run starter-project analysis
3. [ ] Explore the Jupyter notebook

### This Month
1. [ ] Try model benchmarking
2. [ ] Create your own analysis
3. [ ] Consider upgrading to Python 3.10+

---

## 🎉 You Have Everything You Need!

- ✅ CELLxGENE Census installed and working
- ✅ Example scripts ready to run
- ✅ Two complete projects (starter + benchmarking)
- ✅ Comprehensive documentation
- ✅ Clear learning path

**Start exploring! 🔬**
