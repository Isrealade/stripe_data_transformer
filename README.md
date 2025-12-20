# Stripe Data Transformer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A robust Python application that fetches Stripe payment data, transforms it into clean CSV reports, and optionally uploads to AWS S3. Perfect for analytics, finance, and bookkeeping workflows.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Error Handling](#-error-handling)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

## ✨ Features

- **🔍 Complete Data Fetching**: Fetches all Stripe charges with automatic pagination support
- **🔄 Data Transformation**: Converts raw Stripe JSON data into clean, structured CSV files
- **💰 Financial Formatting**: Automatically converts amounts from cents to dollars
- **📅 Date Handling**: Converts Unix timestamps to readable datetime formats
- **☁️ Cloud Integration**: Optional upload to AWS S3 for data warehousing
- **📊 Column Mapping**: Customizable column names for better readability
- **🛡️ Error Handling**: Comprehensive error handling for API failures, timeouts, and AWS errors
- **📝 Logging**: Detailed logging for debugging and monitoring
- **🧪 Test Coverage**: Comprehensive test suite with 41+ test cases

## 🔧 Prerequisites

- Python 3.8 or higher
- Stripe API key (test or live)
- (Optional) AWS credentials and S3 bucket for cloud storage

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Isrealade/stripe_data_transformer.git
cd stripe_data_transformer
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
STRIPE_API_KEY=sk_test_your_stripe_api_key_here
DEBUG=false
BUCKET_NAME=your-s3-bucket-name  # Optional, only if using S3 upload
```

**Important**: 
- Never commit your `.env` file to version control (already in `.gitignore`)
- Use test mode API keys (`sk_test_...`) for development
- Get your Stripe API key from [Stripe Dashboard](https://dashboard.stripe.com/apikeys)

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `STRIPE_API_KEY` | Yes | Your Stripe API key (test or live) | - |
| `DEBUG` | No | Enable debug logging (`true`/`false`) | `false` |
| `BUCKET_NAME` | No | AWS S3 bucket name for uploads | - |

### AWS S3 Configuration (Optional)

If you want to upload CSV files to S3, configure AWS credentials using one of these methods:

1. **AWS Credentials File** (`~/.aws/credentials`):
   ```ini
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

2. **Environment Variables**:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **IAM Role** (if running on EC2)

## 🚀 Usage

### Basic Usage

Run the application from the project root:

```bash
python -m src.stripe_data_transformer.main
```

Or if installed as a package:

  ```bash
python -m stripe_data_transformer.main
```

### What Happens

1. **Fetch**: The application connects to Stripe API and fetches all charges (with pagination)
2. **Transform**: Raw JSON data is normalized, columns are renamed, amounts converted, dates formatted
3. **Export**: A CSV file (`stripe_data.csv`) is created in the current directory
4. **Upload** (Optional): If `BUCKET_NAME` is set, the CSV is uploaded to S3

### Output CSV Format

The generated CSV file includes the following columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| Transaction ID | Stripe charge ID | `ch_1234567890` |
| Amount ($) | Transaction amount in dollars | `20.00` |
| Currency | Currency code | `usd` |
| Date | Transaction date/time | `2021-01-01 00:00:00` |
| Status | Charge status | `succeeded` |
| Payment Method ID | Stripe payment method ID | `pm_1234567890` |
| Card Brand | Card brand | `visa` |
| Last 4 Digits | Last 4 digits of card | `4242` |

### Example Output

```csv
Transaction ID,Amount ($),Currency,Date,Status,Payment Method ID,Card Brand,Last 4 Digits
ch_1234567890,20.00,usd,2021-01-01 00:00:00,succeeded,pm_1234567890,visa,4242
ch_0987654321,50.00,usd,2021-01-02 00:00:00,succeeded,pm_0987654321,mastercard,1234
```

## 📁 Project Structure

```
stripe_data_transformer/
├── src/
│   └── stripe_data_transformer/
│       ├── __init__.py
│       ├── config.py              # Configuration and environment variables
│       ├── main.py                 # Main entry point
│       ├── services/
│       │   ├── fetch_charges.py    # Stripe API fetching logic
│       │   ├── data_transformer.py # Data transformation and CSV export
│       │   └── loader.py           # S3 upload functionality
│       └── utils/
│           └── logger.py           # Logging utility
├── tests/
│   ├── conftest.py                 # Shared test fixtures
│   ├── test_fetch_charges.py       # Tests for API fetching
│   ├── test_data_transformer.py   # Tests for data transformation
│   ├── test_loader.py              # Tests for S3 uploads
│   ├── test_main.py                # Integration tests
│   └── test_logger.py              # Tests for logging
├── .env                            # Environment variables (not in repo, create from .env.example)
├── stripe_data.csv                 # Generated CSV file (created at runtime)
├── requirements.txt                # Python dependencies
├── pytest.ini                     # Pytest configuration
├── pyproject.toml                  # Project metadata
├── LICENSE                         # MIT License
└── README.md                       # This file
```

**Note**: The `stripe_data.csv` file is generated when you run the application. You may want to add it to `.gitignore` if you don't want to commit generated files.

## 🧪 Testing

The project includes a comprehensive test suite with 41+ test cases covering all major functionality.

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=src/stripe_data_transformer --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run Specific Test Files

```bash
# Test API fetching
pytest tests/test_fetch_charges.py -v

# Test data transformation
pytest tests/test_data_transformer.py -v

# Test S3 uploads
pytest tests/test_loader.py -v

# Test main integration
pytest tests/test_main.py -v
```

### Test Coverage

- ✅ API fetching with pagination
- ✅ Error handling (HTTP errors, timeouts, JSON decode errors)
- ✅ Data transformation and CSV export
- ✅ Amount and date conversions
- ✅ S3 upload functionality
- ✅ Error scenarios (missing credentials, bucket errors)
- ✅ Logging functionality

See [tests/README.md](tests/README.md) for detailed testing documentation.

## 🛡️ Error Handling

The application includes robust error handling for common scenarios:

### Stripe API Errors

- **HTTP Errors**: Handles 401 (Unauthorized), 429 (Rate Limit), 500 (Server Error)
- **Timeout Errors**: Handles request timeouts gracefully
- **JSON Decode Errors**: Handles malformed API responses
- **Network Errors**: Handles connection failures

### AWS S3 Errors

- **Missing Credentials**: Returns `False` and logs error
- **Bucket Not Found**: Handles `NoSuchBucket` errors
- **Access Denied**: Handles permission errors
- **Other Client Errors**: Catches and logs all S3 errors

### Data Errors

- **Empty Results**: Handles empty charge lists gracefully
- **Missing Columns**: Column mapping handles missing fields
- **Invalid Data**: Type conversions handle invalid data

All errors are logged with appropriate detail levels for debugging.

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Keep API keys and secrets out of version control
2. **Use test keys for development** - Use Stripe test mode keys during development
3. **Rotate credentials regularly** - Update API keys and AWS credentials periodically
4. **Limit API key permissions** - Use keys with minimal required permissions
5. **Monitor usage** - Check Stripe dashboard and AWS CloudWatch for unusual activity

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests before committing
pytest

# Check code formatting (if using black)
black src/ tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Future Enhancements

Potential features for future versions:

- [ ] Date range filtering (`--from-date`, `--to-date`)
- [ ] Customer data enrichment
- [ ] Refund data integration
- [ ] Excel export format
- [ ] CLI interface with argument parsing
- [ ] Multiple export formats (JSON, Parquet)
- [ ] Incremental sync (only fetch new/updated records)
- [ ] Direct database export (PostgreSQL, MySQL)
- [ ] Scheduled runs (cron-like scheduling)
- [ ] Email notifications on completion

## 🐛 Troubleshooting

### Common Issues

**Issue**: `KeyError: 'STRIPE_API_KEY'`
- **Solution**: Ensure `.env` file exists and contains `STRIPE_API_KEY`

**Issue**: `401 Unauthorized` from Stripe API
- **Solution**: Verify your Stripe API key is correct and has proper permissions

**Issue**: S3 upload fails with `NoCredentialsError`
- **Solution**: Configure AWS credentials using one of the methods in the Configuration section

**Issue**: CSV file is empty
- **Solution**: Check if your Stripe account has charges. Verify API key has read permissions.

**Issue**: Tests fail with import errors
- **Solution**: Ensure you're running tests from the project root directory

## 📞 Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/Isrealade/stripe_data_transformer/issues)
- **Author**: Isreal Adenekan

## 🙏 Acknowledgments

- [Stripe](https://stripe.com/) for the excellent API
- [pandas](https://pandas.pydata.org/) for data manipulation
- [pytest](https://pytest.org/) for testing framework

---

**Made with ❤️ for better financial data management**