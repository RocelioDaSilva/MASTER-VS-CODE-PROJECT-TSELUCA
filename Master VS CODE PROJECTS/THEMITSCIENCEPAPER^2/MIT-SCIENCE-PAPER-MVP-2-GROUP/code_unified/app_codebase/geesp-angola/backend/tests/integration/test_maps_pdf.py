from pathlib import Path


def test_pdf_maps_exist():
    data_dir = Path("data/processed")
    pdfs = list(data_dir.glob("*.pdf"))
    assert len(pdfs) >= 4, "Expected at least 4 map PDF files in data/processed"
