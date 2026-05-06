# Contributing to GEESP-Angola

Thank you for your interest in contributing to the GEESP-Angola project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Report any inappropriate behavior to the maintainers

## Ways to Contribute

### 1. Report Bugs
- Use the GitHub Issues page
- Provide clear description, steps to reproduce, and expected behavior
- Include Python version, OS, and relevant dependencies
- Attach screenshots or error traces if helpful

### 2. Suggest Features
- Submit ideas via GitHub Issues
- Describe the use case and benefits
- Provide examples of how it would work
- Be open to feedback and discussion

### 3. Submit Code
- Fork the repository
- Create a feature branch: `git checkout -b feature/my-feature`
- Make changes following coding standards (see below)
- Write/update tests as needed
- Submit a Pull Request with clear description

### 4. Improve Documentation
- Fix typos and clarify explanations
- Add examples and usage guides
- Translate documentation to other languages
- Create tutorials or blog posts

### 5. Review Pull Requests
- Test proposed changes
- Provide constructive feedback
- Help discuss design decisions
- Share your expertise

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/geesp-angola.git
cd geesp-angola

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 jupyter

# Create feature branch
git checkout -b feature/my-feature
```

## Coding Standards

### Python Style Guide
- Follow PEP 8 (https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Write docstrings for all public functions and classes
- Maximum line length: 100 characters (except URLs)

### Code Format
```bash
# Format code with Black
black scripts/ dashboard/

# Check code style with flake8
flake8 scripts/ dashboard/ --max-line-length=100

# Run tests
pytest
```

### Docstring Format
```python
def calculate_lcoe(self, solar_irradiance: float, capacity_kw: float) -> dict:
    """
    Calculate Levelized Cost of Electricity (LCOE).
    
    Parameters
    ----------
    solar_irradiance : float
        Average solar irradiance in kWh/m²/day
    capacity_kw : float
        System capacity in kilowatts
        
    Returns
    -------
    dict
        Dictionary with LCOE, CAPEX, OPEX, and other financial metrics
        
    Raises
    ------
    ValueError
        If irradiance or capacity are negative
        
    Examples
    --------
    >>> calc = LCOECalculator("PV_Fixed")
    >>> result = calc.calculate_lcoe(6.0, 50)
    >>> print(f"LCOE: {result['lcoe_usd_kwh']:.2f} USD/kWh")
    LCOE: 0.22 USD/kWh
    """
```

## Testing

### Writing Tests
- Create tests in `tests/` directory
- Use pytest framework
- Test both success and error cases
- Aim for >80% code coverage

```python
# Example test
def test_normalization():
    from scripts.mcda_analysis import MCDAnalyzer
    import numpy as np
    
    analyzer = MCDAnalyzer()
    data = np.array([1, 2, 3, 4, 5], dtype=float)
    normalized = analyzer.normalize_raster(data)
    
    assert normalized.min() == 0.0
    assert normalized.max() == 1.0
    assert len(normalized) == 5
```

### Running Tests
```bash
pytest tests/
pytest -v  # Verbose output
pytest --cov=scripts/  # With coverage
```

## Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Build tools, dependencies, etc.

### Examples
```
feat(mcda): add sensitivity analysis for weights

Implement ±20% weight variation analysis to test robustness
of MCDA results. Returns table with aptitude ranges.

Closes #42
```

```
fix(dashboard): correct LCOE calculator currency display
```

## Pull Request Process

1. **Before Starting**
   - Check existing issues and PRs
   - Discuss major changes via issue first
   - Ensure no conflicts with main branch

2. **While Developing**
   - Create feature branch from latest `main`
   - Make focused, logically related commits
   - Update documentation as you go
   - Write/update tests for your changes

3. **Before Submitting**
   - Run tests: `pytest`
   - Format code: `black scripts/ dashboard/`
   - Check style: `flake8 scripts/ dashboard/`
   - Update CHANGELOG.md
   - Write clear PR description

4. **PR Description Template**
   ```
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation
   
   ## Related Issues
   Closes #(issue number)
   
   ## Testing
   How was this tested?
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] All tests pass
   ```

5. **After Submission**
   - Respond to review comments promptly
   - Make requested changes in new commits
   - Don't force-push after review starts
   - Be patient - maintainers volunteer their time

## Documentation

When making changes:

1. **Update docstrings** in affected functions/classes
2. **Update README.md** if functionality changes
3. **Update QUICKSTART.md** if workflow changes
4. **Update CHANGELOG.md** with summary
5. **Create/update examples** if adding features

## Questions?

- Ask in GitHub Discussions (when available)
- Open an issue with your question
- Check existing documentation
- Contact maintainers via email

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Thank you for contributing!** 🎉

---

**Última atualização**: Fevereiro, 2026
