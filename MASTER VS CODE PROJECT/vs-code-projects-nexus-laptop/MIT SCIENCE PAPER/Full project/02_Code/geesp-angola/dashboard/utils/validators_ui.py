"""
UI Input Validators
Validates and sanitizes user inputs
"""

import streamlit as st
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


def validate_raster(uploaded_file) -> Optional[Tuple[np.ndarray, dict]]:
    """
    Validate uploaded raster file
    Returns: (raster_array, metadata_dict) or None if invalid
    """
    if uploaded_file is None:
        st.error("❌ Nenhum arquivo foi carregado.")
        return None
    
    try:
        # Check file extension
        file_ext = Path(uploaded_file.name).suffix.lower()
        if file_ext not in [".tif", ".tiff", ".npy"]:
            st.error(f"❌ Formato de arquivo não suportado: {file_ext}")
            return None
        
        # Try to load
        if file_ext == ".npy":
            import io
            arr = np.load(io.BytesIO(uploaded_file.read()))
        else:
            # For GeoTIFF, would need rasterio
            st.error("❌ GeoTIFF requer rasterio. Use .npy para testes.")
            return None
        
        # Validate shape
        if arr.ndim not in [2, 3]:
            st.error(f"❌ Array deve ser 2D ou 3D, recebeu {arr.ndim}D")
            return None
        
        metadata = {
            "shape": arr.shape,
            "dtype": str(arr.dtype),
            "min": float(np.nanmin(arr)) if np.any(np.isfinite(arr)) else None,
            "max": float(np.nanmax(arr)) if np.any(np.isfinite(arr)) else None,
        }
        
        return arr, metadata
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
        return None


def validate_weights(weights: dict) -> bool:
    """Validate that weights sum to appropriate value"""
    try:
        total = sum(weights.values())
        if not (99 < total < 101):  # Allow small floating point error
            st.error(f"❌ Pesos devem somar 100% (recebeu {total:.1f}%)")
            return False
        return True
    except Exception as e:
        st.error(f"❌ Erro ao validar pesos: {str(e)}")
        return False


def validate_lcoe_parameters(capacity: float, irradiance: float, 
                            discount_rate: float, lifetime: int) -> bool:
    """Validate LCOE parameters"""
    if not (0.1 <= capacity <= 100):
        st.error("❌ Capacidade deve estar entre 0.1 e 100 MW")
        return False
    
    if not (1000 <= irradiance <= 3000):
        st.error("❌ Irradiância deve estar entre 1000 e 3000 kWh/m²/ano")
        return False
    
    if not (1 <= discount_rate <= 15):
        st.error("❌ Taxa de desconto deve estar entre 1 e 15%")
        return False
    
    if not (10 <= lifetime <= 40):
        st.error("❌ Vida útil deve estar entre 10 e 40 anos")
        return False
    
    return True
