"""
Stock data fetching utilities.
Uses free APIs to get current stock prices and information.
"""

import yfinance as yf
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta


class StockDataFetcher:
    """Fetches stock data from free APIs."""
    
    @staticmethod
    def get_current_price(ticker: str) -> Optional[float]:
        """Get current stock price."""
        try:
            stock = yf.Ticker(ticker)
            data = stock.info
            
            # Try different price fields
            price = data.get('currentPrice') or data.get('regularMarketPrice') or data.get('previousClose')
            return float(price) if price else None
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")
            return None
    
    @staticmethod
    def get_stock_info(ticker: str) -> Dict:
        """Get comprehensive stock information."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('longName', info.get('shortName', ticker)),
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose'),
                'earnings_date': StockDataFetcher._format_earnings_date(stock.calendar),
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD')
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return {'name': ticker, 'current_price': None}
    
    @staticmethod
    def _format_earnings_date(calendar) -> Optional[str]:
        """Format earnings date from yfinance calendar."""
        try:
            if calendar and 'Earnings Date' in calendar:
                earnings_dates = calendar['Earnings Date']
                if earnings_dates and len(earnings_dates) > 0:
                    # Get the first upcoming earnings date
                    date = earnings_dates[0]
                    if hasattr(date, 'strftime'):
                        return date.strftime('%Y-%m-%d')
                    return str(date)
        except (KeyError, IndexError, AttributeError, TypeError) as e:
            print(f"Error formatting earnings date: {e}")
        return None
    
    @staticmethod
    def get_price_history(ticker: str, period: str = "1mo") -> Optional[Dict]:
        """
        Get historical price data.
        period can be: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return None
            
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            change = end_price - start_price
            change_percent = (change / start_price) * 100 if start_price != 0 else 0
            
            return {
                'start_price': float(start_price),
                'end_price': float(end_price),
                'change': float(change),
                'change_percent': float(change_percent),
                'high': float(hist['High'].max()),
                'low': float(hist['Low'].min())
            }
        except Exception as e:
            print(f"Error fetching history for {ticker}: {e}")
            return None
    
    @staticmethod
    def calculate_price_change(price_paid: float, current_price: float) -> Tuple[float, float]:
        """Calculate price change and percentage."""
        change = current_price - price_paid
        change_percent = (change / price_paid) * 100 if price_paid != 0 else 0
        return change, change_percent
    
    @staticmethod
    def calculate_total_value(amount: int, current_price: float) -> float:
        """Calculate total value of stock holdings."""
        return amount * current_price
    
    @staticmethod
    def calculate_total_gain_loss(amount: int, price_paid: float, current_price: float) -> Tuple[float, float]:
        """Calculate total gain/loss and percentage."""
        total_paid = amount * price_paid
        total_current = amount * current_price
        gain_loss = total_current - total_paid
        gain_loss_percent = (gain_loss / total_paid) * 100 if total_paid != 0 else 0
        return gain_loss, gain_loss_percent
