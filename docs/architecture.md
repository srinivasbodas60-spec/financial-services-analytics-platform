# Architecture notes

## Layer contracts

| Layer | Responsibility | Example output |
| --- | --- | --- |
| Bronze | Preserve source shape and ingestion metadata | Raw API/CSV landing |
| Silver | Standardize types, deduplicate, validate domains | Clean transaction events |
| Gold | Publish stable business entities and measures | `fact_transaction` + dimensions |

## Production mapping

- **Microsoft Fabric:** Data Factory pipelines land source data in OneLake; notebooks or Dataflows Gen2 apply silver rules; Fabric Warehouse publishes gold tables; Power BI consumes a governed semantic model.
- **Snowflake:** Stages and streams replace the landing layer; tasks or dbt-style transformations publish dimensional tables.
- **Operations:** Pipeline row counts and quality summaries would be written to an audit table and connected to alerting.

## Data quality ownership

Critical checks are designed to stop publication: duplicate event IDs, orphan foreign keys, invalid statuses, and negative raw amounts. Non-critical warnings, such as late-arriving events, should be measured and surfaced without silently dropping records.

