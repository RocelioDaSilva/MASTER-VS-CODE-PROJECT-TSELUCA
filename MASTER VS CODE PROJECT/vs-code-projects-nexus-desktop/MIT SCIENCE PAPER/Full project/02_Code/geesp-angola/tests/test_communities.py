import pandas as pd
from pathlib import Path


def test_communities_csv_exists_and_count():
    p = Path("data/processed/communities_45.csv")
    assert p.exists(), "communities_45.csv is missing"
    df = pd.read_csv(p)
    assert len(df) == 45, f"Expected 45 communities, found {len(df)}"
    assert set(
        ["name", "province", "latitude", "longitude", "population_est"]
    ).issubset(df.columns)
