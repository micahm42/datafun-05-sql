# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair",
#     "marimo",
#     "pandas",
# ]
# ///

"""src/datafun/clinic_notebook.py - Reactive SQL clinic explorer.

Domain:

A healthcare clinic system containing clinics, patients,
visits, and laboratory results.

Tables:

clinic
    Stores information about each clinic.

patient
    Stores patients and the clinic they are associated with.

visit
    Stores visits made by patients.

lab_result
    Stores laboratory results associated with visits.

Relationships:

One clinic can have many patients.
One patient can have many visits.
One visit can have many lab results.

SQL Question:

How many visits does each clinic have, and what is
the average visit length?

SQL joins the related clinic, patient, and visit tables.
The SQL result is returned to Python as a pandas DataFrame
and visualized with an Altair bar chart.
"""

# === 0. DECLARE IMPORTS AND CREATE APP ===

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path
    import sqlite3
    import sys

    import altair as alt
    import marimo as mo
    import pandas as pd

    notebook_location = mo.notebook_location()

    if notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    NOTEBOOK_LOCATION = Path(notebook_location)

    DATA_DIR = NOTEBOOK_LOCATION.parents[1] / "data" / "health"

    CLINIC_FILENAME = "clinic.csv"
    PATIENT_FILENAME = "patient.csv"
    VISIT_FILENAME = "visit.csv"
    LAB_RESULT_FILENAME = "lab_result.csv"

    def load_csv_for_notebook(
        *,
        local_path: Path,
        public_path: Path,
    ) -> pd.DataFrame:
        """Load a CSV locally or in a deployed WASM app."""

        if sys.platform == "emscripten":
            from pyodide.http import open_url

            return pd.read_csv(open_url(str(public_path)))

        if not local_path.is_file():
            raise FileNotFoundError(f"Required data file not found: {local_path}")

        return pd.read_csv(local_path)


@app.cell
def _title():
    # === INTRODUCE THE EXPLORER ===

    mo.md(r"""
    # Clinic Related Data Analysis

    Explore related healthcare clinic data interactively.

    The data has three one-to-many relationships:

    **clinic → patient → visit → lab result**

    ### Tables

    **Clinic**
    - `clinic_id`
    - `clinic_name`
    - `city`

    **Patient**
    - `patient_id`
    - `clinic_id`
    - `age`
    - `age_group`

    **Visit**
    - `visit_id`
    - `patient_id`
    - `visit_type`
    - `visit_minutes`

    **Lab Result**
    - `lab_result_id`
    - `visit_id`
    - `test_name`
    - `result_value`
    - `unit`

    ### SQL Question

    **How many visits does each clinic have,
    and what is the average visit length?**

    SQL joins the related clinic, patient, and visit
    tables and calculates the number of visits and
    average visit length for each clinic.

    The SQL query result is returned as a pandas
    DataFrame and visualized with Python.
    """)


@app.cell
def _load_data():
    # === LOAD THE RELATED DATA ===

    clinic_df = load_csv_for_notebook(
        local_path=DATA_DIR / CLINIC_FILENAME,
        public_path=DATA_DIR / CLINIC_FILENAME,
    )

    patient_df = load_csv_for_notebook(
        local_path=DATA_DIR / PATIENT_FILENAME,
        public_path=DATA_DIR / PATIENT_FILENAME,
    )

    visit_df = load_csv_for_notebook(
        local_path=DATA_DIR / VISIT_FILENAME,
        public_path=DATA_DIR / VISIT_FILENAME,
    )

    lab_result_df = load_csv_for_notebook(
        local_path=DATA_DIR / LAB_RESULT_FILENAME,
        public_path=DATA_DIR / LAB_RESULT_FILENAME,
    )
    return clinic_df, lab_result_df, patient_df, visit_df


@app.cell
def _show_data():
    # === SHOW THE LOADED DATA ===

    mo.md("""
    ## Loaded Data

    The four CSV files have been loaded into pandas
    DataFrames before being inserted into SQLite.
    """)


@app.cell
def _create_database(clinic_df, lab_result_df, patient_df, visit_df):
    # === CREATE AN IN-MEMORY SQLITE DATABASE ===

    connection = sqlite3.connect(":memory:")

    clinic_df.to_sql(
        "clinic",
        connection,
        if_exists="replace",
        index=False,
    )

    patient_df.to_sql(
        "patient",
        connection,
        if_exists="replace",
        index=False,
    )

    visit_df.to_sql(
        "visit",
        connection,
        if_exists="replace",
        index=False,
    )

    lab_result_df.to_sql(
        "lab_result",
        connection,
        if_exists="replace",
        index=False,
    )

    mo.md(
        """
        **Database connected.**

        The clinic, patient, visit, and lab result
        tables are now available in SQLite.
        """
    )
    return (connection,)


@app.cell
def _run_query(connection):
    # === RUN SQL QUERY ===

    sql_query = """
    SELECT
        c.clinic_name,
        c.city,
        COUNT(v.visit_id) AS visit_count,
        ROUND(AVG(v.visit_minutes), 1)
            AS average_visit_minutes
    FROM clinic AS c
    JOIN patient AS p
        ON c.clinic_id = p.clinic_id
    JOIN visit AS v
        ON p.patient_id = v.patient_id
    GROUP BY
        c.clinic_name,
        c.city
    ORDER BY
        visit_count DESC;
    """

    result_df = pd.read_sql_query(
        sql_query,
        connection,
    )
    return result_df, sql_query


@app.cell
def _show_sql(sql_query):
    # === EXPLAIN THE SQL QUERY ===

    mo.md(
        f"""
        ## SQL Query

        The following SQL joins the three related tables
        needed to answer the question:

        ```sql
        {sql_query}
        ```

        The query:

        1. Joins each clinic to its patients.
        2. Joins each patient to their visits.
        3. Counts the visits for each clinic.
        4. Calculates the average visit length.
        5. Groups the results by clinic.
        6. Sorts clinics by the number of visits.
        """
    )


@app.cell
def _show_result():
    # === DISPLAY THE SQL RESULT ===

    mo.md("""
    ## SQL Result

    The SQL result is returned to Python as a
    pandas DataFrame.
    """)


@app.cell
def _show_df_and_chart(result_df):
    # === VISUALIZE THE RESULT ===

    clinic_chart = (
        alt.Chart(result_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "clinic_name:N",
                title="Clinic",
            ),
            y=alt.Y(
                "visit_count:Q",
                title="Number of Visits",
            ),
            tooltip=[
                alt.Tooltip(
                    "clinic_name:N",
                    title="Clinic",
                ),
                alt.Tooltip(
                    "city:N",
                    title="City",
                ),
                alt.Tooltip(
                    "visit_count:Q",
                    title="Visits",
                ),
                alt.Tooltip(
                    "average_visit_minutes:Q",
                    title="Average Visit Minutes",
                ),
            ],
        )
        .properties(
            title="Number of Visits by Clinic",
            width="container",
            height=400,
        )
    )

    mo.vstack(
        [
            result_df,
            clinic_chart,
        ]
    )


@app.cell
def _interpretation():
    # === INTERPRET THE RESULTS ===

    mo.md("""
    ## Interpretation

    The table and chart show the number of patient visits
    associated with each clinic. The average visit length
    provides an additional measure of how long visits
    typically last at each clinic.

    Clinics with more visits have a larger total patient
    visit volume. The average visit length can be used
    alongside the visit count to understand differences
    in clinic activity.

    ## Why SQL Is Useful

    SQL is useful for this question because the information
    is stored across multiple related tables.

    Instead of manually combining the clinic, patient, and
    visit DataFrames in Python, SQL can join the tables
    using their keys and calculate the required statistics
    with COUNT() and AVG().

    SQL also makes the relationship between the tables
    explicit and allows the analysis to be performed close
    to the database data before the results are returned
    to Python for visualization.
    """)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
