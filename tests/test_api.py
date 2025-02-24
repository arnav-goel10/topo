import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_data():
    response = client.get("/api/data")
    assert response.status_code == 200, "GET /api/data should return status code 200."
    data = response.json().get("data")
    # Check that the unified data contains all required keys.
    for key in [
        "company_info", "employee_data", "company_performance",
        "membership_activity", "aggregated_performance", "presentation"
    ]:
        assert key in data, f"Unified data should contain '{key}'."

def test_get_json_data():
    response = client.get("/api/data/json")
    assert response.status_code == 200, "GET /api/data/json should return status code 200."
    data = response.json().get("data")
    assert isinstance(data, dict), "Raw JSON data should be a dictionary."
    assert "companies" in data, "Raw JSON data should include 'companies'."

def test_get_csv_data():
    response = client.get("/api/data/csv")
    assert response.status_code == 200, "GET /api/data/csv should return status code 200."
    data = response.json().get("data")
    assert isinstance(data, list), "CSV endpoint should return a list of records."
    if data:
        assert "membership_id" in data[0], "Each CSV record should contain 'membership_id'."

def test_get_pdf_data():
    response = client.get("/api/data/pdf")
    assert response.status_code == 200, "GET /api/data/pdf should return status code 200."
    data = response.json().get("data")
    assert isinstance(data, list), "PDF endpoint should return a list."
    if data:
        assert "Year" in data[0], "Each PDF record should contain 'Year'."

def test_get_pptx_data():
    response = client.get("/api/data/pptx")
    assert response.status_code == 200, "GET /api/data/pptx should return status code 200."
    data = response.json().get("data")
    assert isinstance(data, dict), "PPTX endpoint should return a dictionary."
    assert "summary_metrics" in data, "PPTX data should contain 'summary_metrics'."
