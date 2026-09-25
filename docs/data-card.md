# Data Card

This project provides four data domains for practicing Python and SQL
with related tables.

## Retail

**Source:** Synthetic data generated for this course.
The data is designed for practicing SQL joins, grouping,
filtering, aggregation, and visualization.

Files:

- **region.csv** - one row per business region
- **store.csv** - one row per store
- **employee.csv** - one row per employee
- **sale.csv** - one row per sale

Relationships:

- region → store → employee
- A region has many stores (1:M).
- A store has many employees (1:M).
- A store can also have many sales (1:M).

## Library

**Source:** Synthetic data generated for this course.
The data is designed for practicing SQL joins, grouping,
filtering, aggregation, and visualization.

Files:

- **state.csv** - one row per state
- **branch.csv** - one row per library branch
- **book.csv** - one row per book
- **review.csv** - one row per book review

Relationships:

- state → branch → book → review

## Medical Informatics

**Source:** Synthetic data generated for this course.
No records represent real patients or healthcare encounters.
The data is designed for practicing SQL with related
healthcare-style data without using real patient information.

Files:

- **clinic.csv** - one row per clinic
- **patient.csv** - one row per synthetic patient
- **visit.csv** - one row per visit
- **lab_result.csv** - one row per lab result

Relationships:

- clinic → patient → visit → lab_result

## MovieLens

**Source:** MovieLens Latest Small dataset from GroupLens Research.
The dataset was last updated in September 2018. :contentReference[oaicite:0]{index=0}

MovieLens Latest datasets may change over time and are not intended
for reporting research results. :contentReference[oaicite:1]{index=1}

The dataset contains approximately:

- 100,000 movie ratings
- 3,600 tag applications
- 9,000 movies
- 600 users

### Source and documentation

MovieLens Latest Datasets
<https://grouplens.org/datasets/movielens/latest/>

This project uses MovieLens for learning and practicing
data analysis with related tables.
