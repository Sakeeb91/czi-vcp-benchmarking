"""
ML Model Predictor Page

Explore the trained Random Forest classifier and feature importance.
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Add project paths
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root / "src"))

st.set_page_config(page_title="ML Predictor", page_icon="🤖", layout="wide")

st.title("🤖 Machine Learning Predictor")
st.markdown("Explore the trained Random Forest classifier for COVID-19 detection")

# Load model
model_path = Path("/Users/sakeeb/Code repositories/vcp dataset exploration/projects/02_disease_signature_atlas/results/models/disease_classifier_rf.joblib")

if not model_path.exists():
    st.error("❌ Model not found. Please run the ML validation pipeline first.")
    st.code("python scripts/run_ml_validation.py")
    st.stop()

try:
    with st.spinner("Loading model..."):
        clf = joblib.load(model_path)
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Model Info
st.markdown("---")
st.subheader("📊 Model Information")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Type", "Random Forest")
with col2:
    st.metric("Training Tissue", "Blood")
with col3:
    st.metric("Training Accuracy", "77.5%")

# Feature Importance
st.markdown("---")
st.subheader("🔬 Top Predictive Genes")

if hasattr(clf, 'genes') and hasattr(clf.model, 'feature_importances_'):
    importance_df = pd.DataFrame({
        'Gene': clf.genes,
        'Importance': clf.model.feature_importances_
    }).sort_values('Importance', ascending=False).head(20)
    
    # Interactive bar chart
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Gene',
        orientation='h',
        title='Top 20 Predictive Genes',
        labels={'Importance': 'Feature Importance', 'Gene': 'Gene Symbol'},
        color='Importance',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Table
    st.markdown("### 📋 Detailed Table")
    st.dataframe(importance_df, use_container_width=True)
    
    # Biological Interpretation
    st.markdown("---")
    st.subheader("🧬 Biological Interpretation")
    
    st.markdown("""
    **Key Gene Categories:**
    
    - **Ribosomal Proteins (RPL23, RPL26, RPS10)**: Involved in protein synthesis. COVID-19 hijacks cellular machinery.
    - **S100A8**: Immune response marker. Elevated in inflammation and viral infections.
    - **Long Non-Coding RNAs (SNHG5, GAS5)**: Regulate gene expression and immune responses.
    - **Mitochondrial Genes (MT-CO3, MT-ND2)**: Energy production. COVID-19 causes mitochondrial dysfunction.
    
    These genes represent a **systemic immune response** signature in blood.
    """)
else:
    st.warning("Feature importance not available for this model.")

# Cross-Tissue Performance
st.markdown("---")
st.subheader("🌍 Cross-Tissue Performance")

performance_data = {
    'Tissue': ['Blood', 'Lung', 'Heart'],
    'Accuracy': [0.955, 0.570, 0.970],
    'Samples': [200, 200, 100],
    'Note': [
        '✅ Excellent (trained on this tissue)',
        '⚠️ Poor generalization (tissue-specific)',
        '❌ Misleading (no disease samples)'
    ]
}

perf_df = pd.DataFrame(performance_data)

# Bar chart
fig2 = px.bar(
    perf_df,
    x='Tissue',
    y='Accuracy',
    color='Tissue',
    title='Model Performance Across Tissues',
    labels={'Accuracy': 'Accuracy', 'Tissue': 'Tissue Type'},
    text='Accuracy'
)
fig2.update_traces(texttemplate='%{text:.1%}', textposition='outside')
fig2.update_layout(showlegend=False, yaxis_range=[0, 1.1])
st.plotly_chart(fig2, use_container_width=True)

# Table with notes
st.dataframe(perf_df, use_container_width=True)

st.markdown("""
**Interpretation:**
- The model performs excellently on **Blood** (the training tissue).
- **Lung** performance is near random (57%), indicating tissue-specific signatures.
- **Heart** results are misleading due to missing COVID-19 samples in the dataset.
""")
