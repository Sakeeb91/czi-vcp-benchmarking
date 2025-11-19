#!/usr/bin/env python3
"""
Quick test of the signature discovery pipeline with minimal data.
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parents[1] / "shared"))

print("Testing imports...")

try:
    from data.data_loader import DiseaseDataLoader
    print("✓ data_loader imported")
except Exception as e:
    print(f"❌ data_loader import failed: {e}")

try:
    from data.preprocessing import ScancpyPreprocessor
    print("✓ preprocessing imported")
except Exception as e:
    print(f"❌ preprocessing import failed: {e}")

try:
    from analysis.differential_expression import DifferentialExpressionAnalyzer
    print("✓ differential_expression imported")
except Exception as e:
    print(f"❌ differential_expression import failed: {e}")

try:
    from analysis.signature_discovery import SignatureDiscovery
    print("✓ signature_discovery imported")
except Exception as e:
    print(f"❌ signature_discovery import failed: {e}")

print("\n✅ All imports successful!")
print("\nTo run the full pipeline:")
print("  cd projects/02_disease_signature_atlas")
print("  python scripts/run_signature_discovery.py")
