# 📄 AI-Based Regulatory Change Detection

An AI-powered solution designed to automate regulatory document change analysis and impact assessment for Quality Assurance and Regulatory Affairs teams.

## 🎯 Problem Statement

### The Challenge
Currently, Quality Assurance and Regulatory Affairs teams must manually compare new document versions with older ones, line by line. This process is:
- **Time-consuming**: Hours of manual review for each document update
- **Tedious**: Repetitive line-by-line comparison work
- **Error-prone**: Human oversight can miss critical changes
- **High-risk**: Missing a single change can lead to non-compliance, audit findings, and significant business risk

After identifying changes, teams must then assess how those changes impact their internal procedures (SOPs), requiring further manual analysis.

### The Solution
This AI-powered tool automates the initial steps of regulatory document comparison by:
- **Automatically identifying** what has changed between document versions
- **Providing intelligent impact analysis** of detected changes
- **Categorizing changes** by type and significance
- **Streamlining the review process** for compliance teams

## 🚀 Mission Accomplished

A comprehensive document analysis system that identifies and analyzes differences between document versions using AI-powered insights. Perfect for regulatory documents, contracts, policies, and any text-based content that requires detailed change tracking.

## ✨ Features
### User Interface 
![Flowchart 1](https://i.postimg.cc/kVZpNSZZ/img.png)
![Flowchart 2](https://i.postimg.cc/pmW4PRz0/img2.png)

### Addressing Regulatory Compliance Needs
- **Automated Change Detection**: Eliminate manual line-by-line comparison
- **Risk Mitigation**: Comprehensive analysis reduces chance of missing critical changes
- **Compliance Support**: Structured categorization for audit trail documentation
- **Impact Assessment**: AI-powered evaluation of change significance
- **Time Savings**: Reduce document review time from hours to minutes

### Core Functionality
- **Section-Level Comparison**: Identifies added, deleted, and modified sections
- **Paragraph-Level Analysis**: Detailed paragraph changes with similarity scoring
- **AI-Powered Analysis**: Intelligent categorization and summarization of changes
- **Sequential Workflow**: Guided step-by-step analysis process
- **Interactive Web Interface**: User-friendly Streamlit frontend

### Analysis Types
1. **Section Comparison**: Detect structural changes between document versions
2. **Paragraph Analysis**: Fine-grained text modifications within sections
3. **Added Content Analysis**: AI categorization of new sections
4. **Modified Content Analysis**: Impact assessment of changed sections

## 🏗️ Architecture
![image.png](https://postimg.cc/GHGKVNfX)
The project consists of two main components:

### Backend (FastAPI)
- RESTful API endpoints for document processing
- Integration with local LLM (Ollama)
- Advanced text preprocessing and comparison algorithms
- Structured data models using Pydantic
![Screenshot-2025-06-08-143813.png](https://postimg.cc/nC4K0ms5)
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

## 🎯 For Regulatory Affairs Teams

### Business Impact
- **Reduced Review Time**: Automate the most time-consuming part of document comparison
- **Improved Accuracy**: AI-powered analysis reduces human error risk
- **Audit Preparedness**: Structured documentation of all changes and their impacts
- **Compliance Confidence**: Comprehensive analysis ensures no changes are missed
- **Resource Optimization**: Free up expert time for higher-value compliance activities

### Change Categories Detected
- **New Requirements**: Completely new regulatory obligations
- **Clarifications**: Updates that clarify existing requirements
- **Stricter Requirements**: Changes that make compliance more demanding
- **Looser Requirements**: Changes that relax previous restrictions
- **Minor Edits**: Formatting, typos, or non-substantive changes

## 🔧 Configuration

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

## 🛠️ Development

### Adding New Analysis Types

1. **Extend Backend**: Add new endpoints in `main.py`
2. **Update Utilities**: Modify comparison logic in `difference_utility.py`
3. **Frontend Integration**: Add new formatters and UI components
4. **AI Enhancement**: Extend LLM prompts in `llm_utility.py`

### Custom Formatting
Create new formatters in `frontend/formatters/` for specialized output formats.

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

## 🚨 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is running: `ollama serve`
   - Verify model availability: `ollama list`

2. **File Upload Issues**
   - Check file format (only `.txt` supported)
   - Verify file encoding (UTF-8 required)

3. **API Connection Problems**
   - Confirm backend is running on port 8000
   - Check firewall settings

### Performance Tips
- Use smaller documents for faster processing
- Consider model size vs. accuracy trade-offs
- Monitor system resources during AI analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/)
- AI analysis powered by [Ollama](https://ollama.ai/)
- Text comparison using Python's `difflib`

---

For more information or support, please open an issue on the repository.
