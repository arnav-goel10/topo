# AI Application Developer Intern Assessment

## Overview
This project is a data ingestion and visualization application built using FastAPI. It demonstrates the ability to:
- Ingest data from multiple formats (CSV, PPTX, JSON, PDF).
- Clean and merge the data into a unified structure.
- Visualize the processed data using dynamic charts and tables.
- Expose REST API endpoints to serve the unified dataset and individual data sources.
- Follow Object-Oriented Programming (OOP) principles and test-driven development (TDD) practices.

The solution is organized into modular classes:
- **DataIngestion:** Handles reading data from various file formats.
- **DataProcessor:** Cleans and merges the ingested data.
- **API Endpoints:** Built with FastAPI to serve both the unified data and individual datasets.
- **Frontend:** A simple web interface using Jinja2 templates, Bootstrap, Chart.js, and DataTables for interactive visualization.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/arnav-goel10/topo.git
   cd topo
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Ensure you have a `requirements.txt` file listing packages such as FastAPI, Uvicorn, Pandas, pdfplumber, python-pptx, etc.
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Dataset Files Are in Place:**
   Your project should include a `datasets/` folder containing:
   - `dataset1.json`
   - `dataset2.csv`
   - `dataset3.pdf`
   - `dataset4.pptx`

5. **Run the Application:**
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   The app will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

6. **Access the Frontend and API Endpoints:**
   - Frontend Dashboard: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - API Endpoints:
     - Unified data: [http://127.0.0.1:8000/api/data](http://127.0.0.1:8000/api/data)
     - Raw JSON: [http://127.0.0.1:8000/api/data/json](http://127.0.0.1:8000/api/data/json)
     - CSV: [http://127.0.0.1:8000/api/data/csv](http://127.0.0.1:8000/api/data/csv)
     - PDF: [http://127.0.0.1:8000/api/data/pdf](http://127.0.0.1:8000/api/data/pdf)
     - PPTX: [http://127.0.0.1:8000/api/data/pptx](http://127.0.0.1:8000/api/data/pptx)

## Testing Instructions
The project includes unit tests and integration tests using PyTest.

1. **Install PyTest (if not installed):**
   ```bash
   pip install pytest
   ```

2. **Run the Tests:**
   From the project root, run:
   ```bash
   pytest
   ```
   This will run all tests located in the `tests/` directory. The tests verify that:
   - Data ingestion from JSON, CSV, PDF, and PPTX works correctly.
   - Data is properly cleaned and merged.
   - API endpoints return the expected data structure.
   - Visualizations are rendered correctly (in integration tests).

## Assumptions and Challenges
- **Assumptions:**
  - The provided datasets (JSON, CSV, PDF, PPTX) follow a consistent structure similar to the sample files, so that the parsing and merging logic can be applied reliably.
  
- **Challenges:**
  - Extracting and parsing data from non-standard file format like PPTX was complex and required robust error handling.

## Dependencies
Key dependencies include:
- FastAPI
- Uvicorn
- Pandas
- pdfplumber
- python-pptx
- Jinja2
- Chart.js (loaded via CDN)
- Bootstrap (loaded via CDN)
- DataTables (loaded via CDN)
- PyTest (for testing)