import os
import pytest
import pandas as pd
from data_ingestion import DataIngestion

@pytest.fixture
def ingestion():
    base_path = os.path.join(os.getcwd(), "datasets")
    json_path = os.path.join(base_path, "dataset1.json")
    csv_path = os.path.join(base_path, "dataset2.csv")
    pdf_path = os.path.join(base_path, "dataset3.pdf")
    pptx_path = os.path.join(base_path, "dataset4.pptx")
    return DataIngestion(json_path=json_path, csv_path=csv_path, pdf_path=pdf_path, pptx_path=pptx_path)

def test_load_json(ingestion):
    data = ingestion.load_json()
    # Ensure that the JSON data is a dictionary and contains the key 'companies'
    assert isinstance(data, dict), "JSON data should be a dictionary."
    assert "companies" in data, "JSON data should include a 'companies' key."
    assert len(data["companies"]) > 0, "There should be at least one company in the JSON data."

def test_load_csv(ingestion):
    df = ingestion.load_csv()
    # Ensure that CSV data is loaded as a DataFrame
    assert isinstance(df, pd.DataFrame), "CSV data should be returned as a DataFrame."
    # Verify that column names are normalized to lowercase
    for col in df.columns:
        assert col == col.lower(), f"Column '{col}' should be lowercase."

def test_load_pdf(ingestion):
    pdf_data = ingestion.load_pdf()
    # Verify that PDF data is returned as a list
    assert isinstance(pdf_data, list), "PDF data should be a list."
    # If the list is non-empty, each row should be a dictionary containing expected keys
    if pdf_data:
        assert isinstance(pdf_data[0], dict), "Each row from the PDF should be a dictionary."
        expected_keys = ["Year", "Quarter", "Revenue (in $)", "Memberships Sold"]
        for key in expected_keys:
            assert key in pdf_data[0], f"Expected key '{key}' not found in PDF data row."

def test_load_pptx(ingestion):
    pptx_data = ingestion.load_pptx()
    # Verify that PPTX data is returned as a dictionary
    assert isinstance(pptx_data, dict), "PPTX data should be a dictionary."
    # Check for the required keys in the PPTX output
    for key in ["summary_metrics", "quarterly_metrics", "revenue_breakdown"]:
        assert key in pptx_data, f"Expected key '{key}' not found in PPTX data."
