"""DuckDB analysis of related healthcare clinic data.

This project demonstrates how an analyst can use DuckDB to
query related CSV data with SQL and return the results to
Python as a pandas DataFrame.

Domain relationships:

clinic -> patient -> visit -> lab_result

Analytical question:

How many visits does each clinic have, and what is the
average visit length?

The SQL query demonstrates:

- SELECT
- JOIN
- WHERE
- GROUP BY
- ORDER BY
- parameterized queries

The final SQL result is returned to Python as a DataFrame.
"""

from pathlib import Path

import duckdb

# ============================================================
# 1. DEFINE PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "health"

DATABASE_PATH = PROJECT_ROOT / "data" / "health" / "clinic.duckdb"

CLINIC_FILE = DATA_DIR / "clinic.csv"
PATIENT_FILE = DATA_DIR / "patient.csv"
VISIT_FILE = DATA_DIR / "visit.csv"
LAB_RESULT_FILE = DATA_DIR / "lab_result.csv"


# ============================================================
# 2. CHECK THAT THE DATA FILES EXIST
# ============================================================

required_files = [
    CLINIC_FILE,
    PATIENT_FILE,
    VISIT_FILE,
    LAB_RESULT_FILE,
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(f"Required data file was not found: {file_path}")


print("=" * 60)
print("DUCKDB HEALTHCARE CLINIC ANALYSIS")
print("=" * 60)


# ============================================================
# 3. CONNECT TO DUCKDB
# ============================================================

print("\nConnecting to DuckDB...")

connection = duckdb.connect(str(DATABASE_PATH))

print(f"DuckDB database: {DATABASE_PATH}")


# ============================================================
# 4. CREATE TABLES FROM CSV FILES
# ============================================================

print("\nLoading CSV files into DuckDB...")

connection.execute(
    """
    CREATE OR REPLACE TABLE clinic AS
    SELECT *
    FROM read_csv_auto(?)
    """,
    [str(CLINIC_FILE)],
)

connection.execute(
    """
    CREATE OR REPLACE TABLE patient AS
    SELECT *
    FROM read_csv_auto(?)
    """,
    [str(PATIENT_FILE)],
)

connection.execute(
    """
    CREATE OR REPLACE TABLE visit AS
    SELECT *
    FROM read_csv_auto(?)
    """,
    [str(VISIT_FILE)],
)

connection.execute(
    """
    CREATE OR REPLACE TABLE lab_result AS
    SELECT *
    FROM read_csv_auto(?)
    """,
    [str(LAB_RESULT_FILE)],
)

print("All four tables loaded successfully.")


# ============================================================
# 5. DESCRIBE THE TABLE RELATIONSHIPS
# ============================================================

print("\n" + "=" * 60)
print("TABLE RELATIONSHIPS")
print("=" * 60)

print(
    """
clinic
    |
    | clinic_id
    v
patient
    |
    | patient_id
    v
visit
    |
    | visit_id
    v
lab_result

One clinic can have many patients.
One patient can have many visits.
One visit can have many lab results.
"""
)


# ============================================================
# 6. SHOW TABLE COUNTS
# ============================================================

print("=" * 60)
print("TABLE COUNTS")
print("=" * 60)

table_counts = connection.sql(
    """
    SELECT
        (SELECT COUNT(*) FROM clinic) AS clinic_count,
        (SELECT COUNT(*) FROM patient) AS patient_count,
        (SELECT COUNT(*) FROM visit) AS visit_count,
        (SELECT COUNT(*) FROM lab_result) AS lab_result_count
    """
).df()

print(table_counts.to_string(index=False))


# ============================================================
# 7. SQL ANALYTICAL QUESTION
# ============================================================

print("\n" + "=" * 60)
print("ANALYTICAL QUESTION")
print("=" * 60)

print(
    """
How many visits does each clinic have,
and what is the average visit length?

The query uses JOIN, WHERE, GROUP BY, and ORDER BY.
"""
)


# ============================================================
# 8. PARAMETERIZED SQL QUERY
# ============================================================

minimum_visit_minutes = 0

sql_query = """
SELECT
    c.clinic_name,
    c.city,
    COUNT(v.visit_id) AS visit_count,
    ROUND(AVG(v.visit_minutes), 1) AS average_visit_minutes
FROM clinic AS c
JOIN patient AS p
    ON c.clinic_id = p.clinic_id
JOIN visit AS v
    ON p.patient_id = v.patient_id
WHERE v.visit_minutes >= ?
GROUP BY
    c.clinic_name,
    c.city
ORDER BY
    visit_count DESC;
"""


# ============================================================
# 9. RUN SQL AND RETURN RESULT TO PYTHON
# ============================================================

result_df = connection.execute(
    sql_query,
    [minimum_visit_minutes],
).df()


# ============================================================
# 10. DISPLAY THE RESULT
# ============================================================

print("=" * 60)
print("SQL RESULT")
print("=" * 60)

print(result_df.to_string(index=False))


# ============================================================
# 11. PYTHON ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PYTHON ANALYSIS")
print("=" * 60)

if not result_df.empty:
    busiest_clinic = result_df.loc[result_df["visit_count"].idxmax()]

    longest_average_visit = result_df.loc[result_df["average_visit_minutes"].idxmax()]

    print(f"\nClinic with the most visits: {busiest_clinic['clinic_name']}")

    print(f"Number of visits: {busiest_clinic['visit_count']}")

    print(
        f"\nClinic with the highest average visit length: "
        f"{longest_average_visit['clinic_name']}"
    )

    print(
        f"Average visit length: "
        f"{longest_average_visit['average_visit_minutes']} minutes"
    )


# ============================================================
# 12. DUCKDB VS SQLITE
# ============================================================

print("\n" + "=" * 60)
print("DUCKDB VS SQLITE")
print("=" * 60)

print(
    """
SQLite and DuckDB can both execute SQL and return results
that Python can analyze.

SQLite is commonly used as a lightweight transactional
database and works well for applications that need a
traditional relational database.

DuckDB is designed specifically for analytical workloads.
It can efficiently query structured data such as CSV files
and return analytical results directly to Python.

In this project, DuckDB provides a convenient way to load
CSV data, perform SQL joins and aggregations, and return
the analytical result as a pandas DataFrame.
"""
)


# ============================================================
# 13. WHY AN ANALYST MIGHT CHOOSE DUCKDB
# ============================================================

print("=" * 60)
print("WHY CHOOSE DUCKDB?")
print("=" * 60)

print(
    """
One reason an analyst might choose DuckDB is its strong
support for analytical SQL.

DuckDB can query files such as CSV and Parquet directly,
perform joins and aggregations efficiently, and return the
results to Python for further analysis.

This makes DuckDB useful when the main goal is analyzing
data rather than running an application database.
"""
)


# ============================================================
# 14. CLOSE DATABASE
# ============================================================

connection.close()

print("\nDuckDB connection closed.")
print("Analysis complete.")
