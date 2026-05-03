"""
Cache Manager
Handles caching of expensive computations
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib
import json


class CacheManager:
    """Manages computation caching in session state"""

    @staticmethod
    def cache_key(operation: str, params: dict) -> str:
        """Generate cache key from operation and parameters"""
        param_str = json.dumps(params, sort_keys=True)
        hash_obj = hashlib.md5(param_str.encode())
        return f"{operation}_{hash_obj.hexdigest()}"

    @staticmethod
    def cache_analysis(operation: str, params: dict, result: Any, ttl_hours: int = 24):
        """Cache analysis result"""
        if "cache" not in st.session_state:
            st.session_state.cache = {}
        
        key = CacheManager.cache_key(operation, params)
        st.session_state.cache[key] = {
            "result": result,
            "timestamp": datetime.now(),
            "ttl_hours": ttl_hours,
        }

    @staticmethod
    def get_cached(operation: str, params: dict) -> Optional[Any]:
        """Retrieve cached result if valid"""
        if "cache" not in st.session_state:
            return None
        
        key = CacheManager.cache_key(operation, params)
        
        if key not in st.session_state.cache:
            return None
        
        cache_entry = st.session_state.cache[key]
        age = datetime.now() - cache_entry["timestamp"]
        
        if age > timedelta(hours=cache_entry["ttl_hours"]):
            del st.session_state.cache[key]
            return None
        
        return cache_entry["result"]

    @staticmethod
    def clear_cache():
        """Clear all cache"""
        if "cache" in st.session_state:
            st.session_state.cache = {}
