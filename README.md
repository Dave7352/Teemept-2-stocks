# Stock Record Keeping Application

A desktop application for tracking stock holdings with comprehensive portfolio management features.

## Features

- **Portfolio Management**: Track multiple stock holdings with detailed information
- **Real-time Price Updates**: Fetch current stock prices using free APIs (Yahoo Finance)
- **Position Status Tracking**: Monitor stocks with visual status indicators:
  - INCREASE (Green)
  - HOLD (Green/Red)
  - INVESTIGATION REQUIRED (Amber)
  - DECREASE (Orange)
  - SOLD (Gray)
- **Sorting Options**: Sort by value, price change, ticker, name, status, or last reviewed date
- **Review Tracking**: Monitor when stocks were last reviewed with alerts
- **Earnings Calendar**: Track upcoming earnings dates
- **Notes & Images**: Attach notes and images to each stock
- **Comprehensive Details**: View detailed information including gain/loss, total value, and historical data

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dave7352/Teemept-2-stocks.git
cd Teemept-2-stocks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python stock_app.py
```

### Adding a Stock

1. Click the "Add Stock" button
2. Fill in the required information:
   - Stock Name
   - Ticker Symbol
   - Price Paid per share
   - Number of Shares
   - Position Status
3. Optional: Click "Fetch Info" to automatically get current stock data
4. Optional: Add notes, earnings date, or attach an image
5. Click "Save"

### Managing Stocks

- **Edit Stock**: Select a stock and click "Edit Stock"
- **Delete Stock**: Select a stock and click "Delete Stock"
- **Mark Reviewed**: Update the last reviewed date for a stock
- **View Details**: Double-click a stock or click "View Details" to see comprehensive information
- **Refresh Prices**: Click "Refresh Prices" to update all stock prices
- **Check Alerts**: Click "Check Alerts" to see stocks needing review or upcoming earnings

### Sorting

Use the "Sort by" dropdown to organize your portfolio:
- Recent: Most recently added stocks first
- Name: Alphabetically by stock name
- Ticker: Alphabetically by ticker symbol
- Total Value: Highest total value first
- % Change: Highest percentage gain first
- Status: Grouped by position status
- Last Reviewed: Oldest reviewed first (stocks needing review)

## Database

The application uses SQLite to store all data locally in a `stocks.db` file. This file is created automatically on first run.

## Images

Stock images are stored in the `stocks_images/` directory, which is created automatically.

## Data Fields

Each stock record includes:
- Stock Name
- Ticker Symbol
- Price Paid (per share)
- Number of Shares
- Current Price (fetched from API)
- Total Value (calculated)
- Percentage Change (calculated)
- Position Status
- Last Reviewed Date
- Earnings Date
- Notes (text)
- Image attachment
- Created/Modified timestamps

## Technologies Used

- **Python**: Core programming language
- **tkinter**: GUI framework (built into Python)
- **SQLite**: Local database storage
- **yfinance**: Free stock data API
- **Pillow (PIL)**: Image handling
- **requests**: HTTP requests for API calls

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.