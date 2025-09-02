import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Any
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class FinanceTools:
    """Tools for fetching financial data from Yahoo Finance."""
    
    def __init__(self):
        self.timeout = settings.YAHOO_FINANCE_TIMEOUT
    
    def get_current_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current stock price and basic market data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT.NS')
            
        Returns:
            Dictionary with current price and market data
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'previous_close': info.get('previousClose', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'day_high': info.get('dayHigh', 'N/A'),
                'day_low': info.get('dayLow', 'N/A'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching current stock price for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to fetch data: {str(e)}",
                'timestamp': pd.Timestamp.now().isoformat()
            }
    
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive company information.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with company information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'company_name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'country': info.get('country', 'N/A'),
                'website': info.get('website', 'N/A'),
                'business_summary': info.get('longBusinessSummary', 'N/A'),
                'employees': info.get('fullTimeEmployees', 'N/A'),
                'founded': info.get('founded', 'N/A'),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to fetch company info: {str(e)}",
                'timestamp': pd.Timestamp.now().isoformat()
            }
    
    def get_income_statements(self, symbol: str, periods: int = 4) -> Dict[str, Any]:
        """
        Get income statements for the specified number of periods.
        
        Args:
            symbol: Stock symbol
            periods: Number of periods to fetch (default: 4)
            
        Returns:
            Dictionary with income statement data
        """
        try:
            ticker = yf.Ticker(symbol)
            income_stmt = ticker.income_stmt
            
            if income_stmt.empty:
                return {
                    'symbol': symbol,
                    'error': 'No income statement data available',
                    'timestamp': pd.Timestamp.now().isoformat()
                }
            
            # Get the most recent periods
            recent_data = income_stmt.head(periods)
            
            # Convert to more readable format
            income_data = {}
            for period in recent_data.columns:
                period_data = {}
                for metric in recent_data.index:
                    value = recent_data.loc[metric, period]
                    if pd.notna(value):
                        period_data[metric] = value
                income_data[str(period.date())] = period_data
            
            return {
                'symbol': symbol,
                'income_statements': income_data,
                'periods': periods,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching income statements for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to fetch income statements: {str(e)}",
                'timestamp': pd.Timestamp.now().isoformat()
            }
    
    def get_balance_sheet(self, symbol: str, periods: int = 4) -> Dict[str, Any]:
        """
        Get balance sheet data for the specified number of periods.
        
        Args:
            symbol: Stock symbol
            periods: Number of periods to fetch (default: 4)
            
        Returns:
            Dictionary with balance sheet data
        """
        try:
            ticker = yf.Ticker(symbol)
            balance_sheet = ticker.balance_sheet
            
            if balance_sheet.empty:
                return {
                    'symbol': symbol,
                    'error': 'No balance sheet data available',
                    'timestamp': pd.Timestamp.now().isoformat()
                }
            
            # Get the most recent periods
            recent_data = balance_sheet.head(periods)
            
            # Convert to more readable format
            balance_data = {}
            for period in recent_data.columns:
                period_data = {}
                for metric in recent_data.index:
                    value = recent_data.loc[metric, period]
                    if pd.notna(value):
                        period_data[metric] = value
                balance_data[str(period.date())] = period_data
            
            return {
                'symbol': symbol,
                'balance_sheet': balance_data,
                'periods': periods,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching balance sheet for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to fetch balance sheet: {str(e)}",
                'timestamp': pd.Timestamp.now().isoformat()
            }
