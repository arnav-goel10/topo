import pandas as pd
from fastapi import FastAPI
import uvicorn
import numpy as np
from data_ingestion import DataIngestion
from data_processor import DataProcessor
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="AI Application Developer Intern Assessment API")

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

def convert_if_dataframe(item):
    """
    Converts a pandas DataFrame to a list of dictionaries,
    replacing NaN/NA with None. If the item is not a DataFrame,
    returns it unchanged.
    """
    if isinstance(item, pd.DataFrame):
        return item.replace({pd.NA: None, np.nan: None}).to_dict(orient="records")
    return item

@app.get("/api/data")
def get_all_data():
    """
    Return the unified composite dataset in JSON format.
    """
    # Create a new dictionary to hold the converted data.
    data = {
        "company_info": convert_if_dataframe(unified.get("company_info")),
        "employee_data": convert_if_dataframe(unified.get("employee_data")),
        "company_performance": convert_if_dataframe(unified.get("company_performance")),
        "membership_activity": convert_if_dataframe(unified.get("membership_activity")),
        "aggregated_performance": convert_if_dataframe(unified.get("aggregated_performance")),
        "presentation": unified.get("presentation")  # Already a dict.
    }
    return {"data": jsonable_encoder(data)}

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
