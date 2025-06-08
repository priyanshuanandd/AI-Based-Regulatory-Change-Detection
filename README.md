# AI-Based Regulatory Change Detection

An AI-powered solution designed to automate regulatory document change analysis and impact assessment for Quality Assurance and Regulatory Affairs teams.

## Problem Statement

### The Challenge
Manual document comparison is slow, tedious, error-prone, and risky. This tool:
- Detects changes between document versions
- Assesses their impact using AI
- Categorizes and summarizes changes
- Streamlines compliance review

### The Solution
This AI-powered tool automates the initial steps of regulatory document comparison by:
- **Automatically identifying** what has changed between document versions
- **Providing intelligent impact analysis** of detected changes
- **Categorizing changes** by type and significance
- **Streamlining the review process** for compliance teams

A comprehensive document analysis system that identifies and analyzes differences between document versions using AI-powered insights. Perfect for regulatory documents, contracts, policies, and any text-based content that requires detailed change tracking.

## Features
### User Interface 
[![Screenshot-8-6-2025-141647-localhost.jpg](https://i.postimg.cc/Y9qBHfxp/Screenshot-8-6-2025-141647-localhost.jpg)](https://postimg.cc/kVZpNSZZ)
[![Screenshot-8-6-2025-141720-localhost.jpg](https://i.postimg.cc/Qd13kMtr/Screenshot-8-6-2025-141720-localhost.jpg)](https://postimg.cc/pmW4PRz0)
### Key Functions
- Section & Paragraph Comparison
- AI-Powered Change Categorization
- Step-by-Step Workflow in Streamlit
- REST API with FastAPI backend

### Analysis Types
1. Section Comparison
2. Paragraph Comparison
3. Added Content AI Analysis
4. Modified Content AI Analysis

## 🏗️ Architecture
[![image.png](https://i.postimg.cc/YqyPGBzB/image.png)](https://postimg.cc/GHGKVNfX)The project consists of two main components:

### Backend (FastAPI)
- RESTful API endpoints for document processing
- Integration with local LLM (Ollama)
- Advanced text preprocessing and comparison algorithms
- Structured data models using Pydantic
[![Screenshot-2025-06-08-143813.png](https://i.postimg.cc/WbK9p6s2/Screenshot-2025-06-08-143813.png)](https://postimg.cc/nC4K0ms5)
### Frontend (Streamlit)
- Interactive web interface
- Progressive workflow with step-by-step guidance
- Real-time results visualization
- Tabbed results organization

## 📁 Project Structure

```
document-comparison-tool/
├── backend/
│   ├── main.py              # FastAPI application and endpoints
│   ├── difference_utility.py # Core comparison algorithms
│   ├── llm_utility.py       # AI analysis integration
│   └── __pycache__/
├── frontend/
│   ├── main.py              # Streamlit application
│   ├── api_client.py        # Backend API communication
│   ├── formatters/          # Result formatting modules
│   │   ├── __init__.py
│   │   ├── sections.py
│   │   ├── paragraphs.py
│   │   ├── added_ai.py
│   │   └── modified_ai.py
│   └── __pycache__/
├── requirements.txt
## 📊 Sample Data Included

The project includes two sample regulatory document files to demonstrate functionality:
- **`text_v1.txt`**: Snippet from an older version of a regulatory guideline
- **`text_v2.txt`**: Snippet from a newer version with identified changes

These files can be used immediately to test the tool's capabilities and understand its output format.
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** installed and running locally
3. **TinyLlama model** (or preferred model) available in Ollama

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd document-comparison-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Ollama**
```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/

# Pull the TinyLlama model
ollama pull tinyllama
```

### Running the Application

1. **Start the Backend API**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Launch the Frontend** (in a new terminal)
```bash
cd frontend
streamlit run main.py
```

3. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 💡 Usage

### Web Interface Workflow

1. **Upload Documents**: Upload original and updated versions (`.txt` files)
2. **Sequential Analysis**: Complete the 4-step analysis process:
   - Step 1: Compare Sections
   - Step 2: Compare Paragraphs  
   - Step 3: Analyze Added Content (AI)
   - Step 4: Analyze Modified Content (AI)
3. **Review Results**: View organized results in dedicated tabs

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/compare/sections` | POST | Basic section comparison |
| `/compare/paragraphs` | POST | Detailed paragraph analysis |
| `/added/ai` | POST | AI analysis of added sections |
| `/modified/ai` | POST | AI analysis of modified sections |
| `/health` | GET | Health check |

### Example API Usage

```python
import requests

# Compare sections using provided sample files
files = {
    'old_version': open('text_v1.txt', 'rb'),
    'new_version': open('text_v2.txt', 'rb')
}
response = requests.post('http://localhost:8000/compare/sections', files=files)
results = response.json()
```

### Testing with Sample Data

1. **Use Provided Files**: Load `text_v1.txt` and `text_v2.txt` to see the tool in action
2. **Follow Complete Workflow**: Execute all 4 analysis steps to see comprehensive results
3. **Review Impact Assessment**: Examine AI-generated change categorization and impact analysis
4. **Understand Output Format**: See how results would appear for your regulatory documents


## Output

- Section/Paragraph differences
- Change Type (e.g., New, Stricter, Minor)
- Impact Level (Low, Medium, High)
- Similarity Scores


## Configuration

### LLM Settings
Modify `llm_utility.py` to customize AI analysis:

```python
# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"  # Change to your preferred model
```

### Supported Models
- TinyLlama (default)
- Llama 2
- Mistral
- Any Ollama-compatible model

## 📊 Analysis Output

### Section Changes
- **Added Sections**: New content identified
- **Deleted Sections**: Removed content
- **Modified Sections**: Changed existing content

### AI Analysis Results
- **Change Summary**: One-sentence description of modifications
- **Change Type**: Categorized as:
  - New Requirement
  - Clarification of Existing Requirement
  - Deletion of Requirement
  - Minor Edit
  - Stricter/Looser Requirement
- **Impact Assessment**: Low/Medium/High impact rating

### Paragraph Analysis
- **Similarity Scores**: Quantified change measurement
- **Added/Deleted Paragraphs**: Granular content tracking
- **Modified Paragraphs**: Before/after comparison

## 🔍 Advanced Features

### Text Preprocessing
- Smart section detection with regex patterns
- Paragraph boundary identification
- Content normalization and cleanup

### Similarity Algorithms
- Sequence matching for content comparison
- Configurable similarity thresholds
- Intelligent change detection

### Caching Support
- MD5-based cache key generation
- Optimized for repeated comparisons


## 📋 Dependencies

### Backend
- FastAPI
- Pydantic
- Python-multipart
- Requests
- Difflib (built-in)

### Frontend  
- Streamlit
- Requests
