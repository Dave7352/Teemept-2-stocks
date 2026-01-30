"""
Demo script to populate the database with sample data.
This demonstrates the application's capabilities.
"""

from database import StockDatabase
from datetime import datetime, timedelta

def create_demo_data():
    """Create sample stock records for demonstration."""
    print("Creating demo data for Stock Record Keeping app...\n")
    
    db = StockDatabase()
    
    # Sample stocks with different statuses
    stocks = [
        {
            "stock_name": "Apple Inc.",
            "ticker": "AAPL",
            "price_paid": 150.00,
            "amount": 10,
            "current_value": 175.50,
            "position_status": "INCREASE",
            "notes": "Strong tech leader with solid fundamentals. Recent product launches performing well.",
            "earnings_date": "2026-02-28"
        },
        {
            "stock_name": "Microsoft Corporation",
            "ticker": "MSFT",
            "price_paid": 320.00,
            "amount": 5,
            "current_value": 340.25,
            "position_status": "HOLD (Green)",
            "notes": "Cloud business growing steadily. AI initiatives promising.",
            "earnings_date": "2026-02-15"
        },
        {
            "stock_name": "Tesla Inc.",
            "ticker": "TSLA",
            "price_paid": 250.00,
            "amount": 8,
            "current_value": 235.00,
            "position_status": "HOLD (Red)",
            "notes": "High volatility. Monitoring competition and delivery numbers.",
            "earnings_date": None
        },
        {
            "stock_name": "GameStop Corp.",
            "ticker": "GME",
            "price_paid": 45.00,
            "amount": 20,
            "current_value": 32.00,
            "position_status": "INVESTIGATION REQUIRED",
            "notes": "Significant decline. Need to review business transformation progress.",
            "earnings_date": "2026-03-15"
        },
        {
            "stock_name": "Nvidia Corporation",
            "ticker": "NVDA",
            "price_paid": 450.00,
            "amount": 3,
            "current_value": 520.00,
            "position_status": "INCREASE",
            "notes": "AI boom driving growth. Strong demand for GPUs.",
            "earnings_date": "2026-02-10"
        },
        {
            "stock_name": "General Electric",
            "ticker": "GE",
            "price_paid": 95.00,
            "amount": 15,
            "current_value": 85.00,
            "position_status": "DECREASE",
            "notes": "Underperforming. Consider reducing position.",
            "earnings_date": None
        },
        {
            "stock_name": "Netflix Inc.",
            "ticker": "NFLX",
            "price_paid": 380.00,
            "amount": 4,
            "current_value": 425.00,
            "position_status": "HOLD (Green)",
            "notes": "Subscriber growth positive. Content strategy working.",
            "earnings_date": "2026-02-20"
        },
        {
            "stock_name": "Alphabet Inc.",
            "ticker": "GOOGL",
            "price_paid": 130.00,
            "amount": 12,
            "current_value": 140.50,
            "position_status": "HOLD (Green)",
            "notes": "Search business solid. Cloud growing. AI integration ongoing.",
            "earnings_date": "2026-02-05"
        },
        {
            "stock_name": "Amazon.com Inc.",
            "ticker": "AMZN",
            "price_paid": 145.00,
            "amount": 7,
            "current_value": 155.75,
            "position_status": "INCREASE",
            "notes": "AWS strong. Retail recovering. Prime membership stable.",
            "earnings_date": "2026-02-08"
        },
        {
            "stock_name": "Zoom Video Communications",
            "ticker": "ZM",
            "price_paid": 120.00,
            "amount": 25,
            "current_value": 72.00,
            "position_status": "SOLD",
            "notes": "Sold due to post-pandemic decline. Realized loss.",
            "earnings_date": None
        }
    ]
    
    for stock in stocks:
        stock_id = db.add_stock(
            stock_name=stock["stock_name"],
            ticker=stock["ticker"],
            price_paid=stock["price_paid"],
            amount=stock["amount"],
            position_status=stock["position_status"],
            notes=stock["notes"],
            current_value=stock["current_value"],
            earnings_date=stock["earnings_date"]
        )
        
        # Calculate values for display
        total_paid = stock["amount"] * stock["price_paid"]
        total_current = stock["amount"] * stock["current_value"]
        gain_loss = total_current - total_paid
        gain_loss_pct = (gain_loss / total_paid * 100) if total_paid != 0 else 0
        
        print(f"✓ Added {stock['ticker']:6s} | {stock['stock_name']:30s}")
        print(f"  Status: {stock['position_status']:25s} | Total: ${total_current:10.2f} | G/L: {gain_loss_pct:+6.2f}%")
    
    print(f"\n✓ Created {len(stocks)} sample stock records!")
    print(f"\nTotal Portfolio Value: ${sum(s['amount'] * s['current_value'] for s in stocks):,.2f}")
    print(f"Total Amount Invested: ${sum(s['amount'] * s['price_paid'] for s in stocks):,.2f}")
    
    total_gain_loss = sum(s['amount'] * (s['current_value'] - s['price_paid']) for s in stocks)
    print(f"Total Gain/Loss: ${total_gain_loss:+,.2f}")
    
    print("\n" + "=" * 70)
    print("Demo data created successfully!")
    print("Run 'python stock_app.py' to view the application.")
    print("=" * 70)

if __name__ == "__main__":
    create_demo_data()
