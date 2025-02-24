import pandas as pd
from fastapi import FastAPI
import uvicorn
import numpy as np
from data_ingestion import DataIngestion
from data_processor import DataProcessor
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Software Developer Intern Assessment API")

# Instantiate DataIngestion with updated paths
ingestion = DataIngestion(
    json_path="datasets/dataset1.json",
    csv_path="datasets/dataset2.csv",
    pdf_path="datasets/dataset3.pdf",
    pptx_path="datasets/dataset4.pptx"
)

# Load data
json_data = ingestion.load_json()
try:
    csv_df = ingestion.load_csv()
except Exception as e:
    print("Error loading CSV:", e)
    csv_df = None
pdf_data = ingestion.load_pdf()
pptx_data = ingestion.load_pptx()

# Process and merge JSON & CSV data
processor = DataProcessor(json_data, csv_df, pdf_data, pptx_data)
unified = processor.merge_all_data()


@app.get("/api/data")
def get_all_data():
    """
    Return the unified composite dataset, converting DataFrames to dicts
    and ensuring NaN values become null.
    """
    # Convert DataFrames to dictionaries, replacing NaN and pd.NA with None.
    if unified.get("company_info") is not None:
        unified["company_info"] = unified["company_info"].replace({pd.NA: None, np.nan: None}).to_dict(orient="records")
    if unified.get("employee_data") is not None:
        unified["employee_data"] = unified["employee_data"].replace({pd.NA: None, np.nan: None}).to_dict(
            orient="records")
    if unified.get("company_performance") is not None:
        unified["company_performance"] = unified["company_performance"].replace({pd.NA: None, np.nan: None}).to_dict(
            orient="records")
    if unified.get("membership_activity") is not None:
        unified["membership_activity"] = unified["membership_activity"].replace({pd.NA: None, np.nan: None}).to_dict(
            orient="records")
    if unified.get("aggregated_performance") is not None:
        unified["aggregated_performance"] = unified["aggregated_performance"].replace(
            {pd.NA: None, np.nan: None}).to_dict(orient="records")

    # Use jsonable_encoder to safely convert the unified data.
    return {"data": jsonable_encoder(unified)}

@app.get("/api/data/pdf")
def get_pdf_data():
    """
    Return the PDF table data as-is.
    """
    return {"data": pdf_data}

@app.get("/api/data/pptx")
def get_pptx_data():
    """
    Return the parsed PPTX data, which includes summary metrics, quarterly metrics, revenue breakdown, and raw slide data.
    """
    return {"data": pptx_data}

@app.get("/api/data/json")
def get_json_data():
    """
    Return the raw JSON data.
    """
    return {"data": json_data}

@app.get("/api/data/csv")
def get_csv_data():
    """
    Return the CSV data (if available), with NaN replaced by None.
    """
    if csv_df is not None:
        return {"data": csv_df.replace({np.nan: None}).to_dict(orient="records")}
    else:
        return {"error": "CSV data not available"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
