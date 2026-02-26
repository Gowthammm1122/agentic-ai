# ⚡ Axon — The intelligence hub

## An AI-powered multi-agent orchestration platform built with Streamlit, LangGraph, and Gemini.

### Prerequisites
- Python 3.11+
- Gemini API Key (in `.env` file)

### Setup
1. **Create and Activate Virtual Environment**:
   ```powershell
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the project directory and add your key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Project
Run the Streamlit application:
```powershell
streamlit run main.py
```
