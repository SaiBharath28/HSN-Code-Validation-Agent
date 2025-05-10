# HSN Code Validation Agent

> An intelligent agent for validating Harmonized System Nomenclature (HSN) codes built with Google's Agent Developer Kit (ADK) framework.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ADK Framework](https://img.shields.io/badge/Framework-ADK-orange)](https://google.github.io/adk-docs/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Overview

The HSN Code Validation Agent is a specialized tool designed to validate Harmonized System Nomenclature (HSN) codes against a master dataset. HSN codes are an internationally standardized system for classifying traded products, ranging from 2 to 8 digits, with each level representing a more specific classification. This agent supports GST compliance processes by automating HSN code validation.

## 🚀 Features

- **Intelligent Validation**: Validate single or multiple HSN codes against a master dataset
- **Multi-level Verification**:
  - Format validation (structure, length, numeric integrity)
  - Existence validation (direct match in the dataset)
  - Hierarchical validation (parent code relationships)
- **Interactive Interface**: User-friendly conversational agent for code validation
- **Flexible Input Handling**: Process individual codes or batch validate multiple codes
- **Detailed Responses**: Clear validation results with descriptions for valid codes
- **Robust Error Handling**: Specific feedback for invalid codes with error reasons
- **Dynamic Data Management**: Support for master data updates without redeployment

## 🏗️ Architecture

The agent is built using Google's ADK (Agent Developer Kit) framework with the following components:

```
HSN-Code-Validation-Agent/
│
├── config/
│   ├── config.yaml          # Agent configuration settings
│   └── intents.yaml         # Intent definitions
│
├── data/
│   └── HSN_Master_Data.xlsx # HSN master reference data
│
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── app.py           # Main ADK agent application
│   │   ├── intents/         # Intent handlers
│   │   │   ├── __init__.py
│   │   │   ├── validate_code.py
│   │   │   ├── validate_batch.py
│   │   │   └── help.py
│   │   └── entities/        # Entity extractors
│   │       ├── __init__.py
│   │       └── hsn_code.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_loader.py   # Loads and processes Excel data
│   │   ├── validator.py     # HSN code validation logic
│   │   └── response.py      # Response formatters
│   │
│   └── utils/
│       ├── __init__.py
│       ├── excel.py         # Excel handling utilities
│       └── logging.py       # Logging configuration
│
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_validator.py
│   └── test_data_loader.py
│
├── .env.example             # Environment variables template
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt         # Python dependencies
└── setup.py                 # Package installation script
```

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- ADK Framework
- Access to Google Cloud Platform (if deploying as a cloud agent)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/HSN-Code-Validation-Agent.git
   cd HSN-Code-Validation-Agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration settings
   ```

5. **Run the agent locally**
   ```bash
   python -m src.agent.app
   ```

## 💻 Usage

### Basic Validation

```python
from src.core.validator import validate_hsn_code

# Validate a single HSN code
result = validate_hsn_code("01012100")
print(result)
```

### Batch Validation

```python
from src.core.validator import validate_hsn_codes

# Validate multiple HSN codes
codes = ["01012100", "01011010", "99999999"]
results = validate_hsn_codes(codes)
for code, result in results.items():
    print(f"{code}: {result}")
```

### Command Line Interface

```bash
# Validate a single HSN code
python -m src.cli validate 01012100

# Validate multiple HSN codes from a file
python -m src.cli validate-batch codes.txt
```

### ADK Agent Interaction

The agent responds to the following intents:

- `validate_hsn_code`: Validate a single HSN code
- `validate_batch`: Validate multiple HSN codes
- `help`: Get information about how to use the agent

## 🧪 Validation Logic

The agent implements three levels of validation:

1. **Format Validation**:
   - Verifies if the code consists only of digits
   - Checks if the code length is valid (2, 4, 6, or 8 digits)

2. **Existence Validation**:
   - Checks if the exact HSN code exists in the master dataset

3. **Hierarchical Validation**:
   - For longer codes (e.g., 8 digits), verifies if parent codes (e.g., first 6, 4, or 2 digits) exist in the dataset
   - Ensures the code follows the proper classification hierarchy

## 📊 Data Management

### Loading Strategy

The agent uses an optimized data loading strategy:

- Initial loading of master data into memory for fast lookups
- Optional caching mechanism for frequent code validations
- Support for dynamic reloading when master data is updated

### Performance Considerations

- Efficient data structures for fast HSN code lookups
- Batch processing capability for validating multiple codes
- Configurable memory usage vs. performance trade-offs

## 🔍 Error Handling

The agent provides detailed error information:

- For format errors: Specifies which format rule was violated
- For existence errors: Indicates code was not found in the dataset
- For hierarchical errors: Identifies which parent code is missing

## 🔄 Extending the Agent

### Adding New Features

1. Define new intents in `config/intents.yaml`
2. Create corresponding intent handlers in `src/agent/intents/`
3. Update the agent's response templates as needed

### Updating Master Data

The agent supports runtime updates to the master HSN data:

```bash
# Update the master data source
python -m src.cli update-data path/to/new/HSN_Master_Data.xlsx
```

## 🔒 Security Considerations

- Input validation to prevent injection attacks
- Proper error handling to avoid information leakage
- Authentication for sensitive operations (if applicable)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

