#!/usr/bin/env python3
"""
Test script to verify the Stock Record Keeping application functionality.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import StockDatabase
from stock_data import StockDataFetcher

def test_database():
    """Test database operations."""
    print("Testing database...")
    
    # Initialize database
    db = StockDatabase("test_stocks.db")
    
    # Add a stock
    stock_id = db.add_stock(
        stock_name="Apple Inc.",
        ticker="AAPL",
        price_paid=150.00,
        amount=10,
        position_status="HOLD (Green)",
        notes="Tech giant",
        current_value=175.00
    )
    print(f"✓ Added stock with ID: {stock_id}")
    
    # Get the stock
    stock = db.get_stock(stock_id)
    assert stock is not None
    assert stock['ticker'] == "AAPL"
    print(f"✓ Retrieved stock: {stock['stock_name']}")
    
    # Update the stock
    db.update_stock(
        stock_id=stock_id,
        stock_name="Apple Inc.",
        ticker="AAPL",
        price_paid=150.00,
        amount=15,
        position_status="INCREASE",
        current_value=180.00
    )
    print("✓ Updated stock")
    
    # Get all stocks
    stocks = db.get_all_stocks()
    assert len(stocks) >= 1
    print(f"✓ Found {len(stocks)} stock(s)")
    
    # Update last reviewed
    db.update_last_reviewed(stock_id)
    print("✓ Updated last reviewed date")
    
    # Delete the stock
    db.delete_stock(stock_id)
    print("✓ Deleted stock")
    
    # Cleanup
    os.remove("test_stocks.db")
    print("✓ Database test completed successfully!\n")

def test_stock_data():
    """Test stock data fetcher."""
    print("Testing stock data fetcher...")
    
    fetcher = StockDataFetcher()
    
    # Test with a known stock
    ticker = "AAPL"
    
    # Get current price
    price = fetcher.get_current_price(ticker)
    if price:
        print(f"✓ Fetched current price for {ticker}: ${price:.2f}")
    else:
        print(f"⚠ Could not fetch price for {ticker} (might be network issue)")
    
    # Get stock info
    info = fetcher.get_stock_info(ticker)
    if info and info.get('name'):
        print(f"✓ Fetched stock info: {info['name']}")
    else:
        print(f"⚠ Could not fetch info for {ticker} (might be network issue)")
    
    # Test calculations
    change, change_percent = fetcher.calculate_price_change(100.0, 120.0)
    assert change == 20.0
    assert change_percent == 20.0
    print(f"✓ Price change calculation: ${change:.2f} ({change_percent:.2f}%)")
    
    total_value = fetcher.calculate_total_value(10, 150.0)
    assert total_value == 1500.0
    print(f"✓ Total value calculation: ${total_value:.2f}")
    
    gain_loss, gain_loss_percent = fetcher.calculate_total_gain_loss(10, 100.0, 120.0)
    assert gain_loss == 200.0
    assert gain_loss_percent == 20.0
    print(f"✓ Gain/loss calculation: ${gain_loss:.2f} ({gain_loss_percent:.2f}%)")
    
    print("✓ Stock data fetcher test completed successfully!\n")

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import database
        print("✓ database module imported")
        
        import stock_data
        print("✓ stock_data module imported")
        
        # Try to import stock_app, but it's okay if tkinter is not available
        try:
            import stock_app
            print("✓ stock_app module imported")
        except ImportError as e:
            if 'tkinter' in str(e).lower():
                print("⚠ stock_app requires tkinter (GUI) - skipping (normal for headless environment)")
            else:
                raise
        
        print("✓ Core imports successful!\n")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Stock Record Keeping Application - Test Suite")
    print("=" * 60 + "\n")
    
    try:
        # Test imports first
        if not test_imports():
            sys.exit(1)
        
        # Test database
        test_database()
        
        # Test stock data fetcher
        test_stock_data()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print("\nYou can now run the application with: python stock_app.py")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
