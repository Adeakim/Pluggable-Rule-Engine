# Django Pluggable Rule Engine

A simple Django project with a pluggable rule engine for order validation.

## Features

- **Order Model**: Stores orders with `total` and `items_count` fields
- **Pluggable Rule Engine**: Auto-registration system for adding new rules without modifying existing code
- **Three Built-in Rules**:
  - `min_total_100`: Total must be > 100
  - `min_items_2`: Items count must be >= 2
  - `divisible_by_5`: Total must be divisible by 5
- **REST API**: Endpoint to check which rules pass for a given order

## Setup

1. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create and apply migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Seed the database** (creates 3 example orders):
```bash
python manage.py seed_orders
```

5. **Run the server**:
```bash
python manage.py runserver
```

## Usage

### API Endpoint

**POST** `/rules/check/`

Request body:
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2"]
}
```

Response:
```json
{
  "passed": true,
  "details": {
    "min_total_100": true,
    "min_items_2": false
  }
}
```

### Example with curl

Test Order 1 (total=$150.00, items=3):
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["min_total_100", "min_items_2"]}'

# Response: {"passed":true,"details":{"min_total_100":true,"min_items_2":true}}
```

Test Order 2 (total=$75.50, items=1) with all rules:
```bash
curl -X POST http://localhost:8000/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 2, "rules": ["min_total_100", "min_items_2", "divisible_by_5"]}'

# Response: {"passed":false,"details":{"min_total_100":false,"min_items_2":false,"divisible_by_5":false}}
```

## Adding New Rules

To add a new rule, simply create a new class in `orders/rules.py`:

```python
class NewRule(BaseRule):
    rule_name = "new_rule"
    
    def check(self, order):
        # Your logic here
        return True  # or False
```

The rule will automatically register itself - no other code changes needed!

## Project Structure

```
sbsc_assessment/
├── config/              # Django settings and URL configuration
├── orders/              # Main app
│   ├── management/      # Custom management commands
│   ├── models.py        # Order model
│   ├── rule_engine.py   # Rule engine base classes and registry
│   ├── rules.py         # Rule implementations
│   ├── views.py         # API endpoint
│   └── urls.py          # URL routing
├── manage.py
└── requirements.txt
```

