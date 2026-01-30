# Stock Record Keeping Application - User Guide

## Overview

This desktop application provides comprehensive stock portfolio management with real-time price tracking, alerts, and detailed record keeping.

## Main Window Features

### Stock List View
The main window displays all your stocks in a sortable table with:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT)
- **Stock Name**: Full company name
- **Shares**: Number of shares owned
- **Price Paid**: Purchase price per share
- **Current Price**: Latest market price (updated via Refresh Prices)
- **Total Value**: Shares × Current Price
- **% Change**: Percentage gain/loss from purchase price
- **Status**: Position status with color coding
- **Last Reviewed**: Days since last review

### Color-Coded Status System

The application uses color-coded rows to visualize position status:

| Status | Color | Meaning |
|--------|-------|---------|
| INCREASE | Green (#00C853) | Stock performing well, consider increasing position |
| HOLD (Green) | Light Green (#4CAF50) | Maintain position, performing as expected |
| HOLD (Red) | Red (#FF5252) | Maintain position but monitor closely |
| INVESTIGATION REQUIRED | Amber (#FFC107) | Needs immediate attention/research |
| DECREASE | Orange (#FF6D00) | Consider reducing position |
| SOLD | Gray (#9E9E9E) | Position closed, keeping for records |

## Sorting Options

Use the dropdown menu to sort your portfolio:

1. **Recent**: Shows most recently added stocks first
2. **Name**: Alphabetical by company name
3. **Ticker**: Alphabetical by ticker symbol
4. **Total Value**: Highest value positions first (helpful for portfolio weighting)
5. **% Change**: Best performers first
6. **Status**: Groups stocks by position status
7. **Last Reviewed**: Oldest first (identifies stocks needing review)

## Adding a Stock

1. Click **"Add Stock"** button
2. Enter required information:
   - **Stock Name**: Company name (e.g., "Apple Inc.")
   - **Ticker**: Stock symbol (e.g., "AAPL")
   - **Price Paid**: Your purchase price per share
   - **Shares**: Number of shares purchased
   - **Position Status**: Select from dropdown
3. Optional enhancements:
   - Click **"Fetch Info"** to automatically get current price and company name
   - Enter **Current Price** manually if known
   - Add **Earnings Date** (format: YYYY-MM-DD)
   - Write **Notes** about the investment thesis or important points
   - Attach an **Image** (charts, screenshots, etc.)
4. Click **"Save"**

## Managing Stocks

### Edit Stock
- Select a stock from the list
- Click **"Edit Stock"**
- Modify any fields
- Click **"Save"**

### Delete Stock
- Select a stock
- Click **"Delete Stock"**
- Confirm deletion
- Note: This permanently removes the record

### Mark Reviewed
- Select a stock
- Click **"Mark Reviewed"**
- Updates the "Last Reviewed" date to today
- Useful for tracking when you last analyzed each position

### View Details
- Double-click any stock OR select and click **"View Details"**
- Shows comprehensive information:
  - All basic data
  - Calculated total paid vs. current value
  - Total gain/loss ($ and %)
  - Created and modified timestamps
  - Full notes
  - Attached image (if any)

## Price Updates

### Refresh All Prices
- Click **"Refresh Prices"** button
- Application fetches current prices from Yahoo Finance API
- Updates all stocks automatically
- Shows progress bar during update
- Reports how many stocks were successfully updated

**Note**: Requires internet connection. Free API has no rate limits for basic usage.

## Alerts System

Click **"Check Alerts"** to see:

1. **Review Alerts**: Stocks not reviewed in 30+ days
2. **Earnings Alerts**: Upcoming earnings (within 7 days)
3. **Investigation Alerts**: Stocks marked as "INVESTIGATION REQUIRED"

Example alert output:
```
Alerts:

• GME (GameStop Corp.) - Not reviewed for 45 days
• NVDA - Earnings in 3 days (2026-02-10)
• GME - Investigation Required
```

## Data Storage

### Database
- All data stored locally in `stocks.db` (SQLite)
- No cloud connection required
- Automatic backups recommended (copy the .db file)

### Images
- Stored in `stocks_images/` directory
- Images are copied (not moved) when attached
- Organized by ticker and timestamp
- Safe to delete old images manually if needed

## Tips & Best Practices

### 1. Regular Review Schedule
- Set a reminder to review all positions monthly
- Use "Sort by: Last Reviewed" to find stocks needing attention
- Click "Check Alerts" weekly

### 2. Position Status Guidelines
- **INCREASE**: Stock exceeding expectations, fundamentals strong
- **HOLD (Green)**: Meeting expectations, no action needed
- **HOLD (Red)**: Underperforming but thesis intact, monitoring
- **INVESTIGATION REQUIRED**: Unexpected news/price movement
- **DECREASE**: Consider trimming, reallocating capital
- **SOLD**: Keep for tax records and performance tracking

### 3. Use Notes Effectively
Record:
- Investment thesis (why you bought)
- Price targets (entry/exit points)
- Important catalysts (earnings, product launches)
- Recent news or changes
- Personal observations

### 4. Track Earnings
- Add earnings dates when available
- Review positions before earnings
- Update notes after earnings calls

### 5. Image Attachments
Useful for saving:
- Technical analysis charts
- Fundamental analysis screenshots
- Product images
- Competitive comparisons

### 6. Sorting Strategies
- **Daily check**: Sort by "% Change" to spot big movers
- **Portfolio review**: Sort by "Total Value" to focus on largest positions
- **Maintenance**: Sort by "Last Reviewed" to stay current
- **Risk assessment**: Sort by "Status" to see problem areas

## Keyboard Shortcuts

- **Double-click** on any stock to view details
- Use **Tab** to navigate between fields in forms
- **Enter** submits forms when focused on buttons
- **Esc** closes dialogs (standard tkinter behavior)

## Backup & Recovery

### Creating Backups
```bash
# Backup database
cp stocks.db stocks_backup_$(date +%Y%m%d).db

# Backup images
tar -czf stocks_images_backup.tar.gz stocks_images/
```

### Restoring from Backup
```bash
# Restore database
cp stocks_backup_20260130.db stocks.db

# Restore images
tar -xzf stocks_images_backup.tar.gz
```

## Troubleshooting

### Problem: "Fetch Info" button doesn't work
- **Solution**: Check internet connection
- **Solution**: Verify ticker symbol is correct
- **Solution**: Some stocks may not be available in Yahoo Finance

### Problem: Prices not updating
- **Solution**: Click "Refresh Prices" button
- **Solution**: Manually enter current price in Edit dialog
- **Solution**: Check internet connectivity

### Problem: Application won't start
- **Solution**: Ensure Python 3.7+ is installed
- **Solution**: Run `pip install -r requirements.txt`
- **Solution**: Check that tkinter is installed (comes with Python on most systems)

### Problem: Image not displaying
- **Solution**: Verify image file exists in stocks_images/ directory
- **Solution**: Check image format (PNG, JPG, GIF supported)
- **Solution**: Re-attach image using Edit Stock dialog

## Advanced Usage

### Multiple Portfolios
Create multiple portfolio databases:
```bash
# Start with specific database
python stock_app.py  # Uses stocks.db (default)

# For multiple portfolios, modify database.py:
# Change DATABASE_FILE = "portfolio1.db" for different portfolios
```

### Export Data
Use SQLite tools to export:
```bash
sqlite3 stocks.db .dump > stocks_export.sql
```

### Bulk Price Updates
Run the demo data script approach to batch update:
```python
from database import StockDatabase
from stock_data import StockDataFetcher

db = StockDatabase()
fetcher = StockDataFetcher()

stocks = db.get_all_stocks()
for stock in stocks:
    price = fetcher.get_current_price(stock['ticker'])
    if price:
        change_pct = ((price - stock['price_paid']) / stock['price_paid'] * 100)
        db.update_current_values(stock['id'], price, change_pct)
```

## API Information

### Yahoo Finance (yfinance)
- **Free tier**: Unlimited basic requests
- **Data**: Real-time quotes (15-20 min delay)
- **Coverage**: All major exchanges
- **Rate limits**: None for reasonable use
- **Documentation**: https://github.com/ranaroussi/yfinance

## System Requirements

- **OS**: Windows 10/11, macOS 10.14+, Linux
- **Python**: 3.7 or higher
- **RAM**: 256 MB minimum
- **Disk**: 100 MB (plus image storage)
- **Internet**: Optional (for price updates)

## Getting Help

1. Check this guide first
2. Review the README.md file
3. Check application console for error messages
4. Verify all dependencies are installed: `pip list`
5. Test with demo data: `python demo_data.py`

## Version Information

- **Current Version**: 1.0.0
- **Last Updated**: January 2026
- **License**: MIT
