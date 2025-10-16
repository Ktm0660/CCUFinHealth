# CCUFinHealth

The CCU Financial Health Platform provides foundational APIs and analytics to evaluate a credit union member's financial wellness. This initial implementation focuses on debt-to-income, emergency fund coverage, savings progress, and credit utilization insights.

## Features

- **FastAPI backend** exposing routes to store financial profiles and generate reports.
- **Financial analytics service** encapsulating reusable calculations and recommendation logic.
- **Pydantic schemas** ensuring consistent validation for financial data structures.
- **Comprehensive tests** covering analytical calculations and HTTP endpoints.

## Getting Started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2. Run the application

```bash
uvicorn app.main:app --reload
```

The service will be available at `http://127.0.0.1:8000`. Swagger documentation can be found at `/docs`.

### 3. Execute tests

```bash
pytest
```

## API Overview

| Method | Endpoint           | Description                                  |
| ------ | ------------------ | -------------------------------------------- |
| GET    | `/api/health`      | Service heartbeat check.                     |
| POST   | `/api/profiles`    | Create or update a financial profile.        |
| GET    | `/api/profiles/{}` | Retrieve a stored financial profile.         |
| POST   | `/api/reports`     | Generate a financial health report summary.  |

## Next Steps

- Integrate persistent storage (PostgreSQL) for member profiles.
- Expand analytics to include credit score trends and spending categorization.
- Add authentication and role-based access control for staff vs. member views.
