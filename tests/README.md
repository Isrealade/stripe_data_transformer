# Tests for Stripe Data Transformer

This directory contains comprehensive pytest tests for the Stripe Data Transformer application.

## Running Tests

### Install Dependencies

First, make sure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src/stripe_data_transformer --cov-report=html
```

This will generate an HTML coverage report in `htmlcov/index.html`.

### Run Specific Test Files

```bash
# Test fetch_charges module
pytest tests/test_fetch_charges.py

# Test data_transformer module
pytest tests/test_data_transformer.py

# Test loader module
pytest tests/test_loader.py

# Test main module
pytest tests/test_main.py

# Test logger module
pytest tests/test_logger.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_fetch_charges.py::TestFetchAllCharges

# Run a specific test function
pytest tests/test_fetch_charges.py::TestFetchAllCharges::test_fetch_all_charges_single_page
```

### Verbose Output

```bash
pytest -v
```

## Test Structure

- `conftest.py`: Shared fixtures used across all tests
- `test_fetch_charges.py`: Tests for Stripe API charge fetching
- `test_data_transformer.py`: Tests for data transformation and CSV export
- `test_loader.py`: Tests for S3 upload functionality
- `test_main.py`: Integration tests for the main run function
- `test_logger.py`: Tests for logging utility

## Test Coverage

The tests cover:

1. **fetch_charges.py**:
   - Single page fetching
   - Pagination handling
   - Error handling (HTTP errors, timeouts, JSON decode errors)
   - Authorization headers
   - Empty results

2. **data_transformer.py**:
   - JSON to DataFrame conversion
   - Column mapping and renaming
   - Amount conversion (cents to dollars)
   - Date conversion (Unix timestamp to datetime)
   - Nested data flattening
   - CSV file creation
   - Empty data handling

3. **loader.py**:
   - Successful S3 uploads
   - Missing bucket name handling
   - AWS credential errors
   - S3 client errors (bucket not found, access denied, etc.)
   - Unexpected errors

4. **main.py**:
   - Successful execution flow
   - Exception handling at each step
   - Empty charges list handling

5. **logger.py**:
   - Logger creation
   - Log level configuration
   - Handler setup
   - Formatter configuration

## Notes

- All external dependencies (Stripe API, S3) are mocked
- Tests use temporary directories for file operations
- No actual API calls or S3 uploads are made during testing
- Environment variables are mocked where necessary

