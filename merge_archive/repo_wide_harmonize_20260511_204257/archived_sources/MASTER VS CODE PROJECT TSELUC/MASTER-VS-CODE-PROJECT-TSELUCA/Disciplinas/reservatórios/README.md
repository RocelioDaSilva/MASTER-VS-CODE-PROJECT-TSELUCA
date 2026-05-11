# Projeto: Cálculo do Fator Z (Reservatório)

[![Python tests](https://github.com/RocelioDaSilva/reservat-rios/actions/workflows/python-tests.yml/badge.svg)](https://github.com/RocelioDaSilva/reservat-rios/actions/workflows/python-tests.yml) [![Python versions](https://img.shields.io/badge/python-3.10%7C3.11-blue.svg)](https://www.python.org) [![codecov](https://codecov.io/gh/RocelioDaSilva/reservat-rios/branch/main/graph/badge.svg)](https://codecov.io/gh/RocelioDaSilva/reservat-rios)

Resumo rápido:

- `src/` : módulos de cálculo (`z_factor.py`, `corrections.py`, `numerical_methods.py`, `utils.py`).
- `tests/`: unidade de teste para o caso-exemplo.

Como executar os testes localmente:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -v
```

Para executar a GUI existente (arquivo original):

```powershell
python "projecto_de_codigo/projecto de código/projeto_z_factor.py"
```

Nova entrada GUI (refatorada para usar os módulos em `src/`):

```powershell
# Execute como módulo de pacote
python -m src.main
```
