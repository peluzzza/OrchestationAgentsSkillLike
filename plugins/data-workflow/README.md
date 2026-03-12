# Data Workflow

A specialized multi-agent orchestration system for data engineering and ML, following the bigguy345/Atlas conductor pattern.

## Architecture

```
Data-Atlas (Conductor - User Visible)
    ├── Data-Planner (Autonomous Planning)
    ├── Data-Architect (Data Modeling)
    ├── Pipeline-Builder (ETL/ELT)
    ├── Analytics-Engineer (BI & Metrics)
    ├── ML-Scientist (ML Development)
    ├── Data-Quality (Quality & Governance)
    └── Data-Reviewer (Code Review Gate)
    
    Handoffs → Backend-Atlas, DevOps-Atlas
```

## Agents

| Agent | Role | Model |
|-------|------|-------|
| **Data-Atlas** | Conductor - orchestrates the team | Claude Opus 4.5 |
| **Data-Planner** | Autonomous planning for complex tasks | GPT-5.2 |
| **Data-Architect** | Data modeling & schema design | GPT-5.2 |
| **Pipeline-Builder** | ETL/ELT pipeline development | Claude Sonnet 4.5 |
| **Analytics-Engineer** | BI, metrics, reporting | GPT-5.2 |
| **ML-Scientist** | Machine learning models | GPT-5.2 |
| **Data-Quality** | Quality checks & governance | GPT-5.2 |
| **Data-Reviewer** | Code review gate | GPT-5.2 |

## Workflow

1. **Planning Phase** (for complex tasks)
   - `Data-Planner` researches and creates phased plan
   - User reviews and approves plan

2. **Design Phase**
   - `Data-Architect` designs data models
   - Define data contracts and lineage
   - User approves architecture

3. **Implementation Phase**
   - `Pipeline-Builder` implements ETL/ELT
   - `Analytics-Engineer` builds analytics layer
   - `ML-Scientist` develops ML models (if needed)

3. **Quality Phase**
   - `Data-Quality` validates data quality
   - Governance policies enforced
   - `Data-Reviewer` reviews code

4. **Verification**
   - End-to-end pipeline testing
   - Data quality metrics validated
   - ML model performance confirmed

## Usage

```
@Data-Atlas Build a customer analytics data pipeline with churn prediction
```

Data-Atlas will:
1. Design data model with Data-Architect
2. Build pipelines with Pipeline-Builder
3. Create analytics layer with Analytics-Engineer
4. Develop ML model with ML-Scientist
5. Add quality checks with Data-Quality
6. Code review via Data-Reviewer

## Supported Technologies

### Processing
- Apache Spark
- dbt
- Airflow, Dagster, Prefect
- Databricks, Snowflake

### Storage
- Data Lakes (S3/GCS/ADLS)
- Delta Lake, Iceberg
- Data Warehouses (Snowflake, BigQuery, Redshift)

### ML
- scikit-learn, PyTorch, TensorFlow
- MLflow, Weights & Biases
- Feature stores

### BI
- Looker, Tableau, Power BI
- Metabase, Superset

## Data Quality Standards

All data pipelines must:
- Have automated quality checks
- Document data lineage
- Define data contracts
- Follow naming conventions
- Include proper tests
- Track freshness SLAs

## Installation

Copy the `agents/` folder to your workspace or VS Code prompts directory.
