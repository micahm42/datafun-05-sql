# Concepts

> Key concepts introduced in this module.

<!--
Only the first sentence/paragraph of h3 entries
are used for the integrated quiz.

Wrap code terms in double asterisks
rather than single backtics so they can be read aloud.
-->

## Relational Data Terms

### Relational data

Data organized into tables that are linked to one another through shared values.

### Table

A structured collection of related records.

### Row (record)

One observation, entity, or event in a table.

### Column (field)

One attribute describing the records in a table.

## Keys and Relationships

### Related tables

Tables that store different kinds of information
and can be connected through shared keys.

### One-to-many relationship

A relationship where one row in one table can be related
to many rows in another table.

### Primary key

A column, or set of columns, that uniquely identifies each row in a table.

### Foreign key

A column that references another table's primary key to link the two.

### Relationship

A logical connection between tables, established through keys.

## SQL

### SQL (Structured Query Language)

A declarative language for querying and manipulating relational data.

### Declarative language

A language for describing _what_ result is wanted, not _how_ to compute it.

## Core SQL Clauses

| Clause       | Purpose                                            |
| ------------ | -------------------------------------------------- |
| **SELECT**   | Chooses which columns to return.                   |
| **FROM**     | Specifies the table or tables being queried.       |
| **WHERE**    | Filters rows based on conditions.                  |
| **GROUP BY** | Groups rows so aggregate functions can be applied. |
| **ORDER BY** | Sorts the results.                                 |
| **LIMIT**    | Restricts the number of rows returned.             |

## Grouping and Aggregation

### Aggregation

Summarizing data across rows, usually within groups.

### Aggregate function

A function that summarizes many rows into one value,
such as **COUNT**, **SUM**, **AVG**, **MIN**, or **MAX**.

## Joins

### JOIN

Combines rows from two or more tables based on a related column.

### INNER JOIN

Returns only the rows that match in both tables.

### LEFT JOIN

Returns every row from the left table, with matching data from the right
where it exists and empty values where it does not.

## Parameterized Queries

### Parameterized query

A query that uses placeholders for values supplied when it runs.

### Placeholder

A marker such as **?** in SQL that is replaced with a bound value.

### Bound parameter

A value passed separately to the database engine to fill a placeholder.

### SQL injection

A security risk that occurs when untrusted input is
inserted directly into SQL text, letting that input change what the query
does rather than only what it returns.
Parameterized queries prevent it, because a bound value can never be read as SQL.

## Databases and Engines

### Database

An organized collection of structured data managed by a database engine.

### Database engine

Software that stores, retrieves, and manages data, such as SQLite.

### File-based database

A database stored in a single file on disk rather than run as a separate server.

### SQLite

A lightweight, embedded, file-based relational database used widely in applications.

### DuckDB

A file-based SQL engine built for analytics and data-analysis workflows.

## Using Python and SQL Together

### SQL for related data

SQL is especially useful when information needed for an analysis
is stored across related tables.

### Python with SQL

Python can load data, open a database connection, run SQL,
receive the query result as a DataFrame, and continue the analysis.

### Orchestration

Using Python to control execution, manage inputs, and run SQL.

## Result Terms

### Query result

The table returned by a SQL query.

### SQL result in Python

A SQL query result can be loaded into a pandas DataFrame
so analysis and visualization can continue in Python.

## Governance Terms

### Data provenance

Where data came from and how it was obtained.

### Data governance

The rules and practices for responsible data use, access, and management.
