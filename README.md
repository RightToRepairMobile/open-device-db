# open-device-db
# Open Device Repair & Info Database

[![GitHub stars](https://img.shields.io/github/stars/yourusername/open-device-db)](https://github.com/yourusername/open-device-db)
[![License](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue)](LICENSE)

**A community-driven, open database for phone specs, repair info, firmware, blacklists, and right-to-repair resources.**

Perfect for repair technicians, phone buyers, modders, and resellers.

## Features
- Comprehensive device data (specs, repairability, red flags, tools)
- AI-powered population & enrichment
- Searchable web UI (Streamlit)
- SQLite backend (easy to export)
- Contribution friendly via GitHub PRs

## Quick Start

See `GETTING_STARTED.md` for detailed setup.

```bash
git clone https://github.com/yourusername/open-device-db.git
cd open-device-db
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sqlite3 device_database.db < device_database_schema.sql
sqlite3 device_database.db < sample_data.sql
streamlit run streamlit_app.py
```

## Tech Stack
- **Backend**: SQLite + Python
- **Frontend**: Streamlit
- **AI**: OpenAI / Grok / Claude (for enrichment)
- **Scraping**: BeautifulSoup + GSMArena

## Database Schema
Full schema in `device_database_schema.sql`

## Contributing
1. Fork the repo
2. Add/edit devices via the web app or `populate_agent.py`
3. Run AI enrichment
4. Submit Pull Request

**AI Prompts** are in `GETTING_STARTED.md`

## Monetization / Sustainability
- Donations via GitHub Sponsors / Patreon
- Future: API access for paid tiers, repair shop tools

## License
Data: CC BY-SA 4.0  
Code: MIT

Made with ❤️ for the right-to-repair movement.

