# Phase 7: Performance Profiling & Optimization Guide

## Objective
Measure GEESP-Angola's critical performance paths, identify bottlenecks, and validate optimization improvements.

## Quick Start

### 1. Run Performance Benchmarks
```bash
# Execute all performance tests
python tests/test_performance_profiling.py

# Expected output:
# - Detailed timing measurements
# - Profile analysis with call hierarchy
# - Performance summary table
# - PERFORMANCE_REPORT.md generated
```

### 2. Expected Performance Targets

| Operation | Target Time | Dataset Size |
|-----------|-------------|--------------|
| MCDA Weighted Overlay | <5ms | 280x300 (84K pixels) |
| Array Normalization | <1ms | 280x300 (84K pixels) |
| Batch Normalization (5 rasters) | <10ms | 280x300 × 5 |
| Complete MCDA Workflow | <100ms | Full site analysis |

### 3. Interpreting Results

**Green Indicators** ✅
- MCDA weighted overlay: <5ms
- Normalization operations: <1ms per operation
- Memory usage: <50MB for standard 280x300 workflows
- Vectorization speedup: >10x vs loop-based

**Yellow Warnings** ⚠️
- Any operation: 5-20ms
- Memory usage: 50-200MB
- Speedup: 5-10x

**Red Flags** 🔴
- MCDA overlay: >20ms
- Memory usage: >300MB
- No speedup from vectorization

## Detailed Optimization Strategies

### Strategy 1: Vectorized Operations
**Goal**: Replace Python loops with numpy operations

**Implementation** (Already in place):
```python
# OLD (Loop - slow)
normalized = np.zeros_like(raster)
for i in range(raster.shape[0]):
    for j in range(raster.shape[1]):
        normalized[i, j] = (raster[i, j] - arr_min) / (arr_max - arr_min)

# NEW (Vectorized - 50x faster)
normalized = (raster - arr_min) / (arr_max - arr_min)
```

**Expected Improvement**: 10-50x speedup

**Files Affected**:
- mcda_analysis.py (weighted overlay)
- data_loaders_async.py (array normalization)
- performance.py (normalization cache)

---

### Strategy 2: Float32 Precision
**Goal**: Reduce memory by 50% without sacrificing accuracy

**Implementation** (Already in place):
```python
# OLD (Double precision - 8 bytes per value)
raster = np.array(data)  # defaults to float64

# NEW (Single precision - 4 bytes per value)
raster = np.array(data, dtype=np.float32)
```

**Memory Savings**: 280x300 raster saves 336 KB → 168 KB per array

**Affected Files**:
- data_loaders_async.py (raster loading)
- mcda_analysis.py (normalized arrays)
- enhanced_maps_to_pdf.py (image processing)

---

### Strategy 3: Result Caching
**Goal**: Cache frequently accessed computations

**Implementation**:
```python
cache = {}

# First call: compute and cache
result1 = cached_normalize_raster(data, cache=cache, key='solar_normalized')

# Second call: retrieve from cache (instant)
result2 = cached_normalize_raster(data, cache=cache, key='solar_normalized')
```

**Test Case**: Sensitivity analysis with 10 parameter variations
- WITHOUT cache: 10 × 100ms = 1 second
- WITH cache: 100ms + 9 × 1ms = ~110ms
- **Improvement**: 9x speedup for sensitivity analysis

**File**: tests/test_optimizations.py

---

### Strategy 4: Batch Processing
**Goal**: Process multiple rasters together for cache efficiency

**Implementation**:
```python
rasters = {
    'solar': solar_irr_array,
    'population': pop_density_array,
    'slope': slope_array
}

# Batch normalize all together
normalized = batch_normalize_rasters(rasters)
```

**Expected Improvement**: 10-20% speedup for I/O-bound operations

---

### Strategy 5: Lazy Loading
**Goal**: Only load/compute data when needed

**When to Apply**:
- Large GeoTIFF files (>100MB)
- Multiple site analysis runs
- Sensitivity analysis with many parameters

**Implementation Not Applied Yet** (Roadmap):
```python
# Would use rasterio with windowed reading
with rasterio.open(file_path) as src:
    window = from_bounds(*bounds, transform=src.transform)
    data = src.read(1, window=window)  # Only read subset
```

---

## Performance Profiling Results Interpretation

### Understanding the Profile Output

```
Profile for mcda_workflow:
[Function Name] [Num Calls] [Total Time] [Per-Call Time]
__init__         1          0.001s       0.001s
normalize_raster 5          0.045s       0.009s     ← Potential bottleneck
weighted_overlay 1          0.012s       0.012s     
generate_maps    4          0.030s       0.007s
```

**Interpretation**:
- `normalize_raster` called 5 times, taking 45ms total
  - Could benefit from caching or vectorization
- `weighted_overlay` at 12ms is acceptable for 280x300
  - Original loop-based version would be 100-200ms
  - Current vectorized version is on target

### Hotspot Analysis

**Find hotspots in profile output**:
1. Sort by "Total Time" descending
2. Look for functions >5% of total time
3. Check if they're called repeatedly (candidates for caching)
4. Check if they use loops (candidates for vectorization)

### Profile Data Files

When running `profile_mcda_workflow()`:
- Creates `mcda_profile.prof` (cProfile binary format)
- Can be viewed with: `python -m pstats mcda_profile.prof`
- Commands: `sort cumtime`, `print10`, `callers`, `callees`

---

## Validation Checklist

### Before Optimization
- [ ] Run baseline benchmarks: `python tests/test_performance_profiling.py`
- [ ] Record times in PERFORMANCE_REPORT.md
- [ ] Identify hotspots from profile
- [ ] Prioritize by impact (execution time × frequency)

### During Optimization
- [ ] Implement one optimization at a time
- [ ] Run benchmarks after each change
- [ ] Measure improvement percentage
- [ ] Verify correctness (results match original output)

### After Optimization
- [ ] Run full test suite: `pytest tests/`
- [ ] Compare performance: `diff PERFORMANCE_REPORT_OLD.md PERFORMANCE_REPORT.md`
- [ ] Validate results against baselines
- [ ] Document optimizations in PR

---

## Common Performance Issues & Solutions

### Issue 1: High Normalization Time
**Symptoms**: normalize_raster taking >2ms per call

**Solution**:
1. Add caching for repeated normalizations
2. Use vectorized operations (if not already)
3. Batch multiple rasters together

**File**: tests/test_optimizations.py → `cached_normalize_raster()`

---

### Issue 2: High Memory Usage
**Symptoms**: >100MB for single 280x300 workflow

**Solution**:
1. Switch from float64 to float32
2. Clear intermediate results
3. Streaming/windowed processing for large files

**Files**: data_loaders_async.py, mcda_analysis.py

---

### Issue 3: Slow MCDA Overlay
**Symptoms**: MCDA weighted overlay >20ms

**Solution**:
1. Verify vectorized operations are in place
2. Check for unnecessary copies
3. Use float32 instead of float64
4. Consider GPU acceleration if criteria >10

**File**: mcda_analysis.py → `weighted_overlay()` function

---

## Next Steps After Phase 7

### Phase 8: QA Report
Generate comprehensive report including:
- [ ] Performance metrics (before/after)
- [ ] Test coverage statistics
- [ ] Code quality metrics
- [ ] Production readiness assessment

### Future Optimizations
1. **GPU Acceleration** (for >100MB datasets)
   - CUDA-enabled numpy operations
   - 50-100x potential speedup

2. **Numba JIT Compilation**
   - @numba.jit decorator for hot loops
   - 10-50x potential speedup

3. **Dask for Distributed Processing**
   - Multi-machine processing for 10+ sites
   - Linear scaling with machine count

---

## Performance Profiling Tools Reference

### Using Python's cProfile
```bash
# Profile a script
python -m cProfile -s cumtime script.py

# Profile with output to file
python -m cProfile -o output.prof script.py

# View profile interactively
python -m pstats output.prof
> sort cumtime
> print10
> quit()
```

### Using line_profiler
```bash
# Install
pip install line_profiler

# Profile line-by-line
kernprof -l -v script.py
```

### Using memory_profiler
```bash
# Install
pip install memory_profiler

# Profile memory usage
python -m memory_profiler script.py
```

---

## Expected Results

After Phase 7 completion, you should see:

### Performance Improvements
- MCDA weighted overlay: **10-20x faster**
- Array normalization: **50x faster**
- Complete workflow: **10x faster**

### Code Quality Improvements
- **100% type hints** (already in Phase 4)
- **100% constant centralization** (Phase 3B)
- **100+ test cases** (Phase 6)

### Documentation
- PERFORMANCE_REPORT.md with detailed metrics
- Optimization recommendations for future work
- QA report for production readiness

---

## Troubleshooting

**Q: Import errors when running benchmarks?**
A: Ensure you're in the geesp-angola directory and all dependencies are installed:
```bash
cd Full project/02_Code/geesp-angola
pip install -r requirements.txt
python tests/test_performance_profiling.py
```

**Q: Benchmarks running very slowly?**
A: If MCDA overlay is >100ms:
1. Check if vectorized operations are in place (look for np.stack, np.dot)
2. Verify float32 is being used
3. Profile to identify bottleneck

**Q: Results show no improvement?**
A: Possible causes:
1. Optimizations not applied to critical path
2. Benchmark not isolating the operation
3. Python version differences (3.8 vs 3.9+ have different optimizations)

---

## Success Criteria

✅ **Phase 7 Complete When**:
1. All benchmarks run successfully
2. MCDA operations meet performance targets
3. Vectorization provides 10x+ speedup
4. Test suite passes 100%
5. PERFORMANCE_REPORT.md generated with recommendations

---

**Phase 7 Status**: Ready to Execute Benchmarks
**Next Command**: `python tests/test_performance_profiling.py`
