import os
import pytest
import pandas as pd
import datetime
from data_ingestion import DataIngestion
from data_processor import DataProcessor


@pytest.fixture
def processor():
    base_path = os.path.join(os.getcwd(), "datasets")
    ingestion = DataIngestion(
        json_path=os.path.join(base_path, "dataset1.json"),
        csv_path=os.path.join(base_path, "dataset2.csv"),
        pdf_path=os.path.join(base_path, "dataset3.pdf"),
        pptx_path=os.path.join(base_path, "dataset4.pptx")
    )
    json_data = ingestion.load_json()
    csv_df = ingestion.load_csv()
    pdf_data = ingestion.load_pdf()
    pptx_data = ingestion.load_pptx()
    return DataProcessor(json_data, csv_df, pdf_data, pptx_data)


def test_process_json_data(processor):
    """
    Test that JSON processing returns DataFrames with expected keys.
    """
    result = processor.process_json_data()
    # Verify companies DataFrame is not empty and contains expected columns.
    companies = result.get("companies")
    assert isinstance(companies, pd.DataFrame), "Companies should be a DataFrame."
    for col in ["id", "name", "industry", "location"]:
        assert col in companies.columns, f"Column '{col}' should be in companies DataFrame."

    # Verify employees DataFrame
    employees = result.get("employees")
    assert isinstance(employees, pd.DataFrame), "Employees should be a DataFrame."
    assert "company_id" in employees.columns, "Employees DataFrame should contain 'company_id'."

    # Verify performance DataFrame and its expected columns.
    performance = result.get("performance")
    assert isinstance(performance, pd.DataFrame), "Performance should be a DataFrame."
    for col in ["company_id", "quarter", "revenue", "profit_margin"]:
        assert col in performance.columns, f"Column '{col}' should be in performance DataFrame."


def test_process_membership_data(processor):
    """
    Test that membership activity is processed correctly.
    """
    df = processor.process_membership_data()
    # Check that the 'date' column is a Python date object.
    assert isinstance(df.iloc[0]["date"], datetime.date), "The 'date' field should be a Python date object."

    # Check that year and quarter are correctly extracted.
    assert df.iloc[0]["year"] == 2024, "Year should be extracted correctly."
    # Quarter is computed using month; check that it equals "Q1" for January dates.
    assert df.iloc[0]["quarter"] == "Q1", "Quarter should be 'Q1'."

    # Check that revenue is numeric (not null, assuming CSV revenue exists).
    assert isinstance(df.iloc[0]["revenue"], float), "Revenue should be a float."

    expected_cols = [
        "date", "membership_id", "membership_type", "activity",
        "revenue", "duration (minutes)", "location", "year", "quarter"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Column '{col}' should exist in the membership DataFrame."


def test_process_aggregated_report(processor):
    """
    Test that the aggregated report from the PDF is processed correctly.
    """
    df = processor.process_aggregated_report()
    expected_cols = ["Year", "Quarter", "Revenue (in $)", "Memberships Sold", "Avg Duration (Minutes)"]
    for col in expected_cols:
        assert col in df.columns, f"Column '{col}' should be in the aggregated report DataFrame."
    sample_revenue = df.iloc[0]["Revenue (in $)"]
    assert isinstance(sample_revenue, float), "Revenue (in $) should be a float."
    assert sample_revenue > 0, "Revenue (in $) should be greater than zero."


def test_process_pptx_data(processor):
    """
    Test that the PPTX data is processed and contains the expected keys.
    """
    result = processor.process_pptx_data()
    # Ensure the result is a dictionary with the expected keys.
    assert isinstance(result, dict), "PPTX data should be returned as a dictionary."
    for key in ["summary_metrics", "quarterly_metrics", "revenue_breakdown"]:
        assert key in result, f"Key '{key}' should be present in the PPTX data."


def test_merge_all_data(processor):
    """
    Test that merging all data produces a unified composite structure with expected keys.
    """
    merged = processor.merge_all_data()
    expected_keys = [
        "company_info", "employee_data", "company_performance",
        "membership_activity", "aggregated_performance", "presentation"
    ]
    for key in expected_keys:
        assert key in merged, f"Merged data should contain the key '{key}'."

    assert isinstance(merged["company_info"], pd.DataFrame), "company_info should be a DataFrame."
    assert isinstance(merged["employee_data"], pd.DataFrame), "employee_data should be a DataFrame."
    assert isinstance(merged["company_performance"], pd.DataFrame), "company_performance should be a DataFrame."
    assert isinstance(merged["membership_activity"], pd.DataFrame), "membership_activity should be a DataFrame."
    assert isinstance(merged["aggregated_performance"], pd.DataFrame), "aggregated_performance should be a DataFrame."
    assert isinstance(merged["presentation"], dict), "presentation should be a dictionary."
