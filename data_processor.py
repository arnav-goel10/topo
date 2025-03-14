import pandas as pd


class DataProcessor:
    """
    Processes and merges data from multiple sources into a unified composite structure.
    """

    def __init__(self, json_data: dict, csv_df: pd.DataFrame = None,
                 pdf_data: list = None, pptx_data: dict = None):
        """
        Parameters:
          json_data: Dictionary containing company data (with nested employees and performance).
          csv_df: DataFrame for detailed membership activity.
          pdf_data: List of dictionaries representing the aggregated quarterly performance report.
          pptx_data: Dictionary with presentation summary (summary_metrics, quarterly_metrics, revenue_breakdown).
        """
        self.json_data = json_data
        self.csv_df = csv_df
        self.pdf_data = pdf_data
        self.pptx_data = pptx_data

    def process_json_data(self) -> dict:
        """
        Processes the company JSON data:
          - Flattens company-level data.
          - Extracts employee records.
          - Converts the performance dict (per company) into a list of records.
        """
        # Normalize company-level data
        companies = pd.json_normalize(self.json_data["companies"], sep="_")

        # Normalize employees data (keeping a reference to the company id)
        employees = pd.json_normalize(
            self.json_data["companies"],
            "employees",
            ["id"],
            meta_prefix="company_"
        )

        # Process performance: convert each company's performance dict into a list of records.
        performance_records = []
        for company in self.json_data["companies"]:
            comp_id = company.get("id")
            perf = company.get("performance")
            if isinstance(perf, dict):
                for quarter, metrics in perf.items():
                    record = {"company_id": comp_id, "quarter": quarter}
                    record.update(metrics)
                    performance_records.append(record)
        performance = pd.DataFrame(performance_records)

        return {
            "companies": companies,
            "employees": employees,
            "performance": performance
        }

    def process_membership_data(self) -> pd.DataFrame:
        """
        Processes detailed membership activity from CSV.
        Converts the 'date' column to a Python date object, then extracts year and quarter
        using standard Python methods.
        """
        df = self.csv_df.copy()

        # Standardize column names to lowercase.
        df.columns = [col.strip().lower() for col in df.columns]

        # Convert the 'date' column to datetime then extract the date portion.
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # Extract year and quarter from the Python date objects.
        df["year"] = df["date"].apply(lambda d: d.year)
        df["quarter"] = df["date"].apply(lambda d: f"Q{((d.month - 1) // 3) + 1}")

        # Process revenue
        if "revenue" in df.columns:
            df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
        else:
            df["revenue"] = None

        expected_cols = [
            "date", "membership_id", "membership_type", "activity",
            "revenue", "duration (minutes)", "location", "year", "quarter"
        ]
        return df[expected_cols]

    def process_aggregated_report(self) -> pd.DataFrame:
        """
        Processes the aggregated quarterly performance report from the PDF.
        The PDF data is assumed to be a list of dictionaries (one per row) with columns:
          Year, Quarter, Revenue (in $), Memberships Sold, Avg Duration (Minutes)
        """
        df = pd.DataFrame(self.pdf_data)
        # Standardize column names.
        df.columns = [col.strip() for col in df.columns]
        df["Year"] = df["Year"].astype(int)
        df["Revenue (in $)"] = df["Revenue (in $)"].str.replace(",", "", regex=False).astype(float)
        df["Memberships Sold"] = pd.to_numeric(df["Memberships Sold"], errors="coerce")
        df["Avg Duration (Minutes)"] = pd.to_numeric(df["Avg Duration (Minutes)"], errors="coerce")
        return df

    def process_pptx_data(self) -> dict:
        """
        Processes the PPTX data which is already structured as a composite dictionary.
        Optionally converts revenue strings to numeric in quarterly_metrics.
        """
        if isinstance(self.pptx_data, dict) and "data" in self.pptx_data:
            pptx = self.pptx_data["data"]
        else:
            pptx = self.pptx_data

        # Convert revenue in quarterly_metrics to float, if present.
        if "quarterly_metrics" in pptx:
            for record in pptx["quarterly_metrics"]:
                if "Revenue (in $)" in record:
                    record["Revenue (in $)"] = float(record["Revenue (in $)"].replace(",", ""))
        return pptx

    def merge_all_data(self) -> dict:
        """
        Merges all data sources into a unified composite structure.
        Returns a dictionary with the following keys:
          - company_info: Company metadata from JSON.
          - employee_data: Employee records from JSON.
          - company_performance: Performance details extracted from JSON.
          - membership_activity: Detailed membership activity from CSV.
          - aggregated_performance: Aggregated quarterly performance from PDF.
          - presentation: PPTX summary metrics and related presentation data.
        """
        json_data = self.process_json_data()
        membership_activity = self.process_membership_data()
        aggregated_performance = self.process_aggregated_report()
        presentation = self.process_pptx_data()

        company_performance = json_data["performance"]

        return {
            "company_info": json_data["companies"],
            "employee_data": json_data["employees"],
            "company_performance": company_performance,
            "membership_activity": membership_activity,
            "aggregated_performance": aggregated_performance,
            "presentation": presentation
        }

    def process_all(self) -> dict:
        """
        Single entry point to process and merge all data sources.
        """
        return self.merge_all_data()
