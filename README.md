# AI PRD Generator

Turn a rough feature idea into a structured Product Requirements Document in seconds using Claude AI.

## What it does

Paste a feature request, add context about your product and users, and get a complete PRD with:

- Problem statement
- Goals & success metrics
- User stories
- Functional & non-functional requirements
- Acceptance criteria
- Edge cases & risks
- Out of scope definition
- Open questions
## Built with
- [Streamlit](https://streamlit.io/) — UI and deployment
- [Anthropic Claude API](https://www.anthropic.com/) — PRD generation
- Python 3.9+

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/capsaarang/ai-prd-generator.git
cd ai-prd-generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**

Create a `.streamlit/secrets.toml` file:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

Or set it as an environment variable:
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

**4. Run the app**
```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `ANTHROPIC_API_KEY` in the Secrets section
5. Deploy

## Project context
Built as part of my exploration into AI-powered product tooling. The goal was to demonstrate how LLMs can accelerate early-stage product work — specifically the requirements gathering and documentation phase that typically takes PMs hours to complete manually.

This project complements [Forensic-AI](https://github.com/capsaarang/forensic-ai), an agentic RAG pipeline for financial document auditing.

## Author

Saarang Govinda Rajan  
MS Information Science, UW-Madison  
[Portfolio](https://capsaarang.github.io/myportfolio) · [LinkedIn](https://linkedin.com/in/saarang-g-rajan)
