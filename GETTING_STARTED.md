# Open Device Database - Getting Started

## 1. Setup Environment
```bash
# Create project directory
mkdir open-device-db && cd open-device-db

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas requests beautifulsoup4 openai
```

## 2. Initialize Database
```bash
sqlite3 device_database.db < device_database_schema.sql
```

## 3. Run the AI Population Script
```bash
# Set your API key
export OPENAI_API_KEY=your_key_here

python populate_agent.py
```

## 4. Launch Web App
```bash
streamlit run streamlit_app.py
```

## 5. Seed Initial Data
Manually insert a few rows or extend the populate script.

## Contribution Workflow
1. Fork the repo
2. Add/edit data via app or script
3. Submit PR
4. For bulk: Use AI agents with the prompts below
