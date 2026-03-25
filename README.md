![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)

# Python Process Automation Suite

A modular Python-based automation platform for building scalable workflows, data pipelines, and API integrations.

## Overview

The **Python Process Automation Suite** is designed to automate repetitive processes, integrate external systems, and process structured and unstructured data efficiently.

This project centralizes multiple automation workflows into a reusable and extensible architecture, enabling the development of robust automation solutions.

## Key Features

* Process automation for repetitive and operational tasks
* Integration with external systems via REST APIs and Webhooks
* Data processing and ETL pipelines using Python and Pandas
* Modular architecture for scalability and reusability
* Support for web automation (Selenium) and API-driven workflows
* CNPJ validation and company data enrichment

## Architecture

The project follows a **clean modular architecture**:

```
python-process-automation-suite/
│
├── automation/
│   ├── api/                    # HTTP client and API communication
│   │   ├── __init__.py
│   │   └── client.py           # Generic HTTP client
│   │
│   ├── pipelines/              # Automation workflows and data pipelines
│   │   ├── __init__.py
│   │   ├── base_pipeline.py    # Abstract base class for pipelines
│   │   └── cnpj_pipeline.py    # CNPJ processing pipeline
│   │
│   ├── services/               # Business logic and external integrations
│   │   ├── __init__.py
│   │   ├── brasil_api.py       # BrasilAPI integration for company data
│   │   ├── data_processor.py   # Data transformation and processing
│   │   └── web_scraper.py      # Selenium-based web scraping
│   │
│   ├── utils/                  # Utility modules and helpers
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging configuration
│   │   └── validators.py       # CPF/CNPJ validation utilities
│   │
│   └── __init__.py
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Application configuration
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Documentation
```

## Technologies

* Python 3.10+
* Pandas
* Requests
* Selenium WebDriver
* FastAPI (optional)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DBCBR/python-process-automation-suite
cd python-process-automation-suite
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Example `.env`:
```env
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
LOG_LEVEL=INFO
DEBUG=False
ENVIRONMENT=development
```

### 4. Run the application

#### Using CLI (Recommended)

```bash
# List available pipelines
python main.py --list

# Run CNPJ pipeline with single CNPJ
python main.py --pipeline cnpj --input "12.345.678/0001-90"

# Run CNPJ pipeline with multiple CNPJs
python main.py --pipeline cnpj --input "12.345.678/0001-90,11.222.333/0001-81"

# Run CNPJ pipeline from file
python main.py --pipeline cnpj --file "cnpjs.txt"
```

## 📦 Available Pipelines

### CNPJ Pipeline

**Description:** Validates and enriches CNPJ data using BrasilAPI

**Usage:**
```bash
python main.py --pipeline cnpj --input "12.345.678/0001-90"
```

**Input formats:**
- Single CNPJ: `"12.345.678/0001-90"`
- Multiple CNPJs: `"12.345.678/0001-90,11.222.333/0001-81"`
- File with text: `--file "path/to/file.txt"` (extracts CNPJs using regex)

**Features:**
- ✓ CNPJ validation and cleaning
- ✓ Automatic company data enrichment
- ✓ Text-based CNPJ extraction using regex
- ✓ Error handling and logging
- ✓ ETL pipeline architecture

## Usage Examples

### Processing CNPJ Data

```python
from automation.pipelines.cnpj_pipeline import CNPJPipeline

# Create pipeline with list of CNPJs
cnpj_list = ['00.000.000/0000-91', '11.222.333/0001-81']
pipeline = CNPJPipeline(cnpj_list=cnpj_list)

# Execute pipeline using ETL pattern
result = pipeline.run()

print(f"Total processed: {result['total_processed']}")
print(f"Results: {result['results']}")
```

### Validating Documents

```python
from automation.utils.validators import ValidadorCNPJ, ValidadorCPF

# Validate CNPJ
cnpj = ValidadorCNPJ('00.000.000/0000-91')
cleaned = cnpj.limpar()  # Returns '00000000000191'
formatted = cnpj.formatar()  # Returns '00.000.000/0000-91'

# Validate CPF
cpf = ValidadorCPF('123.456.789-09')
cleaned = cpf.limpar()  # Returns '12345678909'
formatted = cpf.formatar()  # Returns '123.456.789-09'
```

### Web Scraping

```python
from automation.services.web_scraper import capturar_texto_da_web

url = 'https://example.com'
text_content = capturar_texto_da_web(url)
print(text_content)
```

## Project Components

### Pipelines

**CNPJPipeline**: Processes a list of CNPJ numbers, validates them, and enriches data from BrasilAPI.

```python
from automation.pipelines.cnpj_pipeline import CNPJPipeline

pipeline = CNPJPipeline(['00.000.000/0000-91'])
result = pipeline.execute()
```

### Services

* **brasil_api.py**: Query company data from BrasilAPI
* **web_scraper.py**: Capture web page content using Selenium
* **data_processor.py**: Process and transform data

### Utils

* **validators.py**: Validate and format CPF/CNPJ documents
* **logger.py**: Logging configuration

## Configuration

Configure your application via environment variables or `config/settings.py`:

```python
from config.settings import settings

print(settings.API_BASE_URL)
print(settings.DEBUG)
print(settings.ENVIRONMENT)
```

## Future Improvements

* Unit tests and integration tests
* Task scheduling (APScheduler)
* Advanced logging and monitoring
* Docker containerization
* CI/CD pipeline with GitHub Actions
* Additional pipeline implementations
* REST API layer for pipeline exposure
* Database persistence layer

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

David Barcellos Cardoso  
Python Backend Developer | Automation | Generative AI

GitHub: https://github.com/DBCBR  
LinkedIn: https://www.linkedin.com/in/david-barcellos-cardoso/
