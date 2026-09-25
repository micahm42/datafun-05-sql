# Project-Specific Instructions

## Phase 4: First Technical Modification

Make one small technical change.
Run the project again and see what happens.
If your change causes an error, read the message, correct the problem,
and rerun the project.
You can always revert (CTRL z) changes or return to the example code.
Follow this debugging process
until your initial technical modification runs successfully.

The focus here is on related tables.
Take any two related tables, join them using SQL, and provide information that
requires both tables.

Use the examples provided.

Suggestions:

- Change the Marimo notebook opening or closing.
- Change the Marimo notebook chart presentation.
- Change the selected region or SQL filter.
- Change the SQL query to answer a different question.
- Change which related tables are joined.

Confirm the project runs successfully after your change.

## Phase 5 Suggestions

### Phase 5 Suggestion: Different Domain

Implement the same Python and SQL pattern
for one of the provided non-retail domains.
See the **data** folder.

Then:

- Describe the tables in your domain.
- Identify the one-to-many relationships.
- Write one SQL query that answers a question about your data.
- Use SQL to join the related tables needed for your question.
- Return the SQL result to Python as a DataFrame.
- Visualize or otherwise interpret the result.
- Explain why SQL is useful for this question.

The table names and column names will change,
but the related-table pattern should be very similar.

### Phase 5 Suggestion: Explore DuckDB

Apply the same analytical idea using DuckDB instead of SQLite.

Good options:

- **DuckDB with a persistent file** - stores the database in a local file.
- **DuckDB with an in-memory database** - useful for temporary exploration.

Then:

- Run a SQL query against related tables.
- Return the result to Python.
- Compare the DuckDB workflow with the SQLite example.
- Explain one reason an analyst might choose DuckDB.

## Key Skill Focus

Your goal is to use SQL when an analytical question
requires information from related tables.
As you work, focus on:

- how **SELECT**, **WHERE**, **GROUP BY**, **ORDER BY**, and **JOIN**
  answer analytical questions
- how primary and foreign keys connect related tables
- how a one-to-many relationship is represented
- how Python runs SQL and receives the result as a DataFrame
- how the SQL result can continue through the usual Python analytics workflow
- how parameterized queries safely provide values to SQL
- you do NOT need to implement a Marimo version of your custom work

## Professional Communication

Make sure your repository correctly presents and reflects **your work**.
Remove educational instructions that are no
longer needed and verify key areas **showcase your skills**:

- README.md
- docs/
- src/

The example projects are MIT licensed.
You are free to use and modify as you like.

---

[◄ Back to Home](index.md)
