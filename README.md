
# Boeing Portfolio Analytics Dashboard

## Overview
This project provides a professional Python analytics dashboard for tracking a Boeing (BA) investment portfolio.

### Portfolio Structure
- Boeing Investment: $700,000
- Cash Buffer: $300,000
- Shares Held: 3,043
- Average Purchase Price: $230/share

---

## Features
- Real-time Boeing stock tracking
- Portfolio valuation
- Gain/loss monitoring
- Rolling volatility analysis
- Hedge monitoring alerts
- Interactive charts
- CSV export functionality

---

## Installation

### 1. Create Virtual Environment (Optional)
```bash
python -m venv venv
```

### 2. Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Run Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your browser automatically.

---

## Technologies Used
- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- Yahoo Finance API

---

## Future Enhancements
- Monte Carlo simulations
- Options pricing models
- Value at Risk (VaR)
- Benchmark comparison
- Live websocket market feeds
- Portfolio optimization tools
