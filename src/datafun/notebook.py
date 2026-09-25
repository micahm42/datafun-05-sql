# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "altair",
#     "marimo",
#     "pandas",
# ]
# ///
"""src/datafun/notebook.py - Reactive SQL explorer.

Author: Denise Case
Date: 2026-08

DOMAIN:

A small business with regions, stores, and employees.

The data is stored in three related tables.

One region can have many stores.
One store can have many employees.

EXPLORE:

The SQL query calculates the average number of employees
per store in each region.

The SQL query result is returned as a pandas DataFrame.
Python then visualizes the result.
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

    DATA_DIR = NOTEBOOK_LOCATION.parents[1] / "data" / "retail"
    PUBLIC_DIR = NOTEBOOK_LOCATION / "public"

    REGION_FILENAME = "region.csv"
    STORE_FILENAME = "store.csv"
    EMPLOYEE_FILENAME = "employee.csv"

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
    # Reactive Related Data Analysis

    Explore related business data interactively.

    The data has two one-to-many relationships:

    **region → store → employee**

    **Analysis:** Calculate the average number of employees
    per store in each region.

    SQL joins the related tables and calculates the
    average employees per store.

    The SQL query result is returned as a pandas DataFrame,
    and Python visualizes the results.

    | [Project Source](https://github.com/denisecase/datafun-05-sql/blob/main/src/datafun/notebook.py)
    | [Project Docs](https://denisecase.github.io/datafun-05-sql/)

    ---
    """)
    return


@app.cell
def _load_data():
    # === LOAD THE RELATED DATA ===

    regions_df = load_csv_for_notebook(
        local_path=DATA_DIR / REGION_FILENAME,
        public_path=PUBLIC_DIR / REGION_FILENAME,
    )

    stores_df = load_csv_for_notebook(
        local_path=DATA_DIR / STORE_FILENAME,
        public_path=PUBLIC_DIR / STORE_FILENAME,
    )

    employees_df = load_csv_for_notebook(
        local_path=DATA_DIR / EMPLOYEE_FILENAME,
        public_path=PUBLIC_DIR / EMPLOYEE_FILENAME,
    )
    return employees_df, regions_df, stores_df


@app.cell
def _create_database(employees_df, regions_df, stores_df):
    # === CREATE AN IN-MEMORY SQLITE DATABASE ===

    connection = sqlite3.connect(":memory:")

    regions_df.to_sql(
        "regions",
        connection,
        if_exists="replace",
        index=False,
    )

    stores_df.to_sql(
        "stores",
        connection,
        if_exists="replace",
        index=False,
    )

    employees_df.to_sql(
        "employees",
        connection,
        if_exists="replace",
        index=False,
    )

    mo.md("Database connected and tables loaded.")
    return (connection,)


@app.cell
def _run_query(connection):
    # === RUN SQL QUERY ===

    sql_query = """
    SELECT
        r.region_name,
        COUNT(DISTINCT s.store_id) AS store_count,
        COUNT(e.employee_id) AS employee_count,
        ROUND(
            CAST(COUNT(e.employee_id) AS REAL)
            / COUNT(DISTINCT s.store_id),
            2
        ) AS average_employees_per_store
    FROM regions AS r
    JOIN stores AS s
        ON r.region_id = s.region_id
    LEFT JOIN employees AS e
        ON s.store_id = e.store_id
    GROUP BY
        r.region_name
    ORDER BY
        average_employees_per_store DESC;
    """

    result_df = pd.read_sql_query(
        sql_query,
        connection,
    )
    return (result_df,)


@app.cell
def _show_selection():
    # === SHOW THE CURRENT ANALYSIS ===

    mo.md("""
    ## Average Employees per Store by Region

    This analysis compares regions based on the
    average number of employees working at each store.

    The SQL query calculates:

    - Number of stores
    - Total number of employees
    - Average employees per store
    """)
    return


@app.cell
def _show_df_table_and_chart(result_df):
    # === DISPLAY THE SQL QUERY RESULT ===

    region_chart = (
        alt.Chart(result_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "region_name:N",
                title="Region",
                sort="-y",
            ),
            y=alt.Y(
                "average_employees_per_store:Q",
                title="Average Employees per Store",
            ),
            tooltip=[
                alt.Tooltip(
                    "region_name:N",
                    title="Region",
                ),
                alt.Tooltip(
                    "store_count:Q",
                    title="Stores",
                ),
                alt.Tooltip(
                    "employee_count:Q",
                    title="Employees",
                ),
                alt.Tooltip(
                    "average_employees_per_store:Q",
                    title="Average Employees per Store",
                ),
            ],
        )
        .properties(
            title="Average Employees per Store by Region",
            width="container",
            height=400,
        )
    )

    mo.vstack(
        [
            result_df,
            region_chart,
        ]
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
