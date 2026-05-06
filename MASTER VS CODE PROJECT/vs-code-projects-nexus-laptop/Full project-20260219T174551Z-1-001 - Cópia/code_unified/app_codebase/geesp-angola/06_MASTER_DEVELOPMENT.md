# 👨‍💻 Development & Coding Standards Guide

**Consolidated Master Guide** | Standards, conventions, and contribution guidelines  
**Last Updated**: March 6, 2026  
**Status**: Enforced ✅  

---

## 📝 Coding Standards

### Python Style Guide

All code follows **PEP 8** with these specifics:

```python
# Line length: 100 chars (soft), 120 (hard limit)
# Indentation: 4 spaces (never tabs)
# Imports: Alphabetically sorted, grouped

# CORRECT:
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from scripts.mcda_analysis import MCDAnalyzer
from utils.logging_config import setup_logging


# WRONG ❌:
from utils.logging_config import setup_logging
import os
import numpy
from scripts.mcda_analysis import MCDAnalyzer
```

---

### Type Hints (Mandatory)

Every function must have type hints:

```python
# ✅ CORRECT
def calculate_mcda_weights(
    comparison_matrix: Dict[tuple, float],
    normalize: bool = True
) -> Dict[str, float]:
    """Calculate weights from AHP comparison matrix.
    
    Args:
        comparison_matrix: Pairwise comparison values
        normalize: Whether to normalize to [0,1]
    
    Returns:
        Dictionary mapping criteria to weights
    
    Raises:
        ValueError: If matrix is invalid
    """
    weights = {}
    # implementation...
    return weights


# ❌ WRONG (no type hints)
def calculate_mcda_weights(comparison_matrix, normalize=True):
    weights = {}
    # implementation...
    return weights
```

---

### Docstrings (Mandatory)

Use Google-style docstrings:

```python
# ✅ CORRECT
def weighted_overlay(
    layers: Dict[str, np.ndarray],
    weights: Dict[str, float]
) -> np.ndarray:
    """Combine multiple layers with weights.
    
    Performs weighted overlay of raster layers using MCDA methodology.
    If sum of weights ≠ 1.0, auto-normalizes.
    
    Args:
        layers: Dictionary of {layer_name: raster_array}
        weights: Dictionary of {layer_name: weight_value}
    
    Returns:
        Combined raster array with values in [0, 1]
    
    Raises:
        ValueError: If layer and weight keys don't match
        TypeError: If arrays have different shapes
    
    Examples:
        >>> layers = {'Solar': solar_arr, 'Demand': demand_arr}
        >>> weights = {'Solar': 0.6, 'Demand': 0.4}
        >>> result = weighted_overlay(layers, weights)
    
    Note:
        Assumes input arrays are already normalized to [0, 1]
    """
    # implementation...
    return result
```

---

## 🔧 Project Setup for Developers

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/ISPTEC-Energy/geesp-angola.git
cd geesp-angola

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install black flake8 mypy pytest jupyter

# 4. Configure pre-commit hooks
pip install pre-commit
pre-commit install

# 5. Create feature branch
git checkout -b feature/my-feature
```

---

## 🤝 Contributing Guidelines

### Workflow

1. **Create branch from `develop`**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-feature
   ```

2. **Make changes** (follow standards below)

3. **Test locally**:
   ```bash
   pytest tests/ -v
   pytest --cov=scripts
   flake8 scripts/ --max-line-length=100
   mypy scripts/ --strict
   ```

4. **Commit with clear message**:
   ```bash
   git commit -m "feat: add MCDA weighting algorithm"
   ```

5. **Push and create Pull Request**:
   ```bash
   git push origin feature/my-feature
   # Then open PR on GitHub
   ```

6. **Request review** and address feedback

7. **Merge to `develop`** once approved

---

## 📐 Code Organization

### Module Structure

Each module should follow this structure:

```
scripts/my_module.py:
├── Imports (sorted, grouped)
├── Constants (UPPER_CASE)
├── Helper functions  (private funcs start with _)
├── Main class(es)
└── Public functions

Example:
from typing import Dict
import numpy as np

# Constants
DEFAULT_TIMEOUT = 30
MIN_WEIGHT = 0.01

# Private helper
def _validate_matrix(m: np.ndarray) -> bool:
    """Private - for internal use only"""
    return True

# Main class
class MCDAnalyzer:
    """Primary interface"""
    pass

# Public function
def analyze_mcda(data: Dict) -> np.ndarray:
    """Public - for external use"""
    pass
```

---

## 🧪 Testing Requirements

### Every New Feature Must Have Tests

```python
# tests/test_my_feature.py

import pytest
from scripts.my_module import my_function

class TestMyFeature:
    """Test suite for my feature"""
    
    def setup_method(self):
        """Run before each test"""
        self.sample_data = {...}
    
    def test_valid_input(self):
        """Test with valid input"""
        result = my_function(self.sample_data)
        assert result is not None
        assert len(result) > 0
    
    def test_invalid_input(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            my_function(invalid_data)
    
    def test_edge_case(self):
        """Test edge case"""
        result = my_function(edge_case_data)
        assert result == expected_result
    
    @pytest.mark.performance
    def test_performance(self):
        """Test execution time"""
        start = time.time()
        my_function(large_dataset)
        elapsed = time.time() - start
        assert elapsed < 1.0  # Must complete in <1 second
```

### Test Checklist
- [ ] Valid input test
- [ ] Invalid input test
- [ ] Edge case test
- [ ] Performance test (if applicable)
- [ ] Documentation test (docstring examples)

---

## 📚 Documentation Requirements

### Module Documentation

```python
"""
MCDA Analysis Module

Provides Multi-Criteria Decision Analysis using Analytic Hierarchy Process (AHP).
Combines multiple raster layers with weightings to create suitability maps.

Classes:
    AHPWeighter: Calculates weights from comparison matrices
    MCDAnalyzer: Performs weighted overlay analysis

Functions:
    normalize: Scale arrays to [0, 1]
    weighted_overlay: Combine layers with weights
    classify_suitability: Create classification zones

Example:
    >>> from scripts.mcda_analysis import MCDAnalyzer, normalize
    >>> mcda = MCDAnalyzer()
    >>> weights = {'Solar': 0.6, 'Demand': 0.4}
    >>> result = mcda.weighted_overlay(layers, weights)
"""
```

---

## 🔍 Code Review Checklist

When reviewing code, ensure:

- [ ] Follows PEP 8 style guide
- [ ] Has type hints on all functions
- [ ] Has docstrings (Google format)
- [ ] Has unit tests (>90% coverage)
- [ ] No hardcoded values (use config)
- [ ] Imports are sorted and grouped
- [ ] Error handling is comprehensive
- [ ] Performance is acceptable
- [ ] Security implications reviewed
- [ ] No duplicate code (DRY principle)
- [ ] Variable names are clear
- [ ] Comments explain "why", not "what"

---

## 🚀 Commit Message Format

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, test, chore
Scope: module name (mcda, lcoe, gee, etc)

Examples:
- feat(mcda): add sensitivity analysis
- fix(lcoe): correct financial formula
- docs: update API documentation
- refactor(utils): consolidate normalization
- test(security): add encryption tests
```

---

## 📦 Dependency Management

### Adding Dependencies

```bash
# Install new package
pip install package_name

# Save to requirements
pip freeze | grep package_name >> requirements.txt

# Or manually edit requirements.txt
# Then test
pip install -r requirements.txt
pytest tests/

# Commit
git add requirements.txt
git commit -m "chore: add new package"
```

### Security Updates

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update packages
pip install --upgrade pip
pip install --upgrade -r requirements.txt
pytest --cov  # Verify nothing broke
```

---

## 🔒 Security Best Practices

### Secrets Management

```python
# ✅ CORRECT - Use environment variables
import os
GEE_PROJECT_ID = os.getenv('GEE_PROJECT_ID')
if not GEE_PROJECT_ID:
    raise ValueError("GEE_PROJECT_ID not set")

# ❌ WRONG - Never hardcode secrets
GEE_PROJECT_ID = "my-project-12345"  # EXPOSED!
```

### Input Validation

```python
# ✅ CORRECT - Always validate
def process_user_input(data: str) -> str:
    if not isinstance(data, str):
        raise TypeError("Expected string")
    if len(data) > 1000:
        raise ValueError("Input too long")
    return data.strip()

# ❌ WRONG - No validation
def process_user_input(data):
    return data.strip()
```

### SQL Injection Prevention

```python
# ✅ CORRECT - Use parameterized queries
from sqlalchemy import text
query = text("SELECT * FROM results WHERE id = :id")
result = session.execute(query, {"id": user_id})

# ❌ WRONG - String concatenation
query = f"SELECT * FROM results WHERE id = {user_id}"  # VULNERABLE!
```

---

## 📊 Performance Guidelines

### Keep Functions Fast

```python
# ✅ CORRECT - Efficient algorithm
def normalize_fast(array: np.ndarray) -> np.ndarray:
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val)
# Time: 2ms for 1000x1000 array

# ❌ WRONG - Slow algorithm  
def normalize_slow(array: np.ndarray) -> np.ndarray:
    result = np.zeros_like(array)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            # Loop-based approach
            result[i,j] = array[i,j] / array.max()
    return result
# Time: 500ms for same array (250x slower!)
```

### Use Caching

```python
# ✅ CORRECT - Cache expensive results
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param: str) -> float:
    return complex_math(param)

# ❌ WRONG - Recalculate every time
def expensive_calculation(param: str) -> float:
    return complex_math(param)  # Called 1000x = slow
```

---

## 🎓 Learning Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [NumPy Best Practices](https://numpy.org/doc/stable/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Workflow](https://www.atlassian.com/git/tutorials)

---

**Next Steps**:
1. Read [07_MASTER_DASHBOARD.md](07_MASTER_DASHBOARD.md) for UI guidelines
2. Check [08_MASTER_ADVANCED.md](08_MASTER_ADVANCED.md) for optimization
