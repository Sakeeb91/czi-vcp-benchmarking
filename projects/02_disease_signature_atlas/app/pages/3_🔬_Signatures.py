"""
Disease Signatures Page

View cross-tissue disease signatures and overlap analysis.
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3
import io

st.set_page_config(page_title="Signatures", page_icon="🔬", layout="wide")

st.title("🔬 Disease Signatures")
st.markdown("Explore cross-tissue COVID-19 gene signatures")

# Check for signature files
project_root = Path(__file__).resolve().parents[2]
figures_dir = project_root / "results" / "figures"

st.subheader("📊 Signature Visualizations")

# Display saved figures if they exist
if figures_dir.exists():
    signature_files = list(figures_dir.glob("*.png"))
    
    if signature_files:
        st.success(f"✅ Found {len(signature_files)} visualization(s)")
        
        for fig_path in sorted(signature_files):
            st.markdown(f"### {fig_path.stem.replace('_', ' ').title()}")
            st.image(str(fig_path), use_container_width=True)
            st.markdown("---")
    else:
        st.warning("⚠️ No signature visualizations found. Run the multi-tissue analysis pipeline.")
        st.code("python scripts/run_multi_tissue_analysis.py")
else:
    st.error("❌ Results directory not found.")

# Signature Summary
st.markdown("---")
st.subheader("📋 Signature Summary")

st.markdown("""
**Expected Signatures:**

1. **Cross-Tissue Signatures**: Genes consistently upregulated across all tissues
   - Interferon-stimulated genes (ISGs)
   - Viral response genes
   
2. **Tissue-Specific Signatures**: Genes unique to each tissue
   - Blood: Immune cell activation markers
   - Lung: Epithelial damage markers
   - Heart: Cardiac stress markers

3. **Overlap Analysis**: Venn diagrams showing shared vs unique genes

**Biological Interpretation:**
- Cross-tissue genes represent systemic viral response
- Tissue-specific genes indicate local pathology
""")

# Example signature table
st.markdown("### Example: Top Cross-Tissue Genes")
example_signatures = pd.DataFrame({
    'Gene': ['IFI27', 'ISG15', 'MX1', 'IFIT3', 'OAS1'],
    'Blood LogFC': [2.8, 2.5, 2.3, 2.1, 1.9],
    'Lung LogFC': [2.6, 2.3, 2.1, 1.8, 1.7],
    'Category': ['ISG', 'ISG', 'ISG', 'ISG', 'ISG']
})

st.dataframe(example_signatures, use_container_width=True)

st.info("""
💡 **Tip**: Run the full analysis pipeline to generate actual signature data and visualizations.
""")
