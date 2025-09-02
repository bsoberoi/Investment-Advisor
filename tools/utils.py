import time
import functools
from typing import Callable, Any, TypeVar, Optional
from config.logging_config import get_logger

logger = get_logger(__name__)

T = TypeVar('T')

def retry_on_error(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay:.2f} seconds..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {e}"
                        )
                        raise last_exception
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

def safe_api_call(func: Callable[..., T], default_value: Any = None) -> T:
    """
    Safely execute an API call and return a default value on failure.
    
    Args:
        func: Function to execute
        default_value: Value to return if the function fails
        
    Returns:
        Result of the function or default_value on failure
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return default_value

def format_currency(value: float, currency: str = "USD") -> str:
    """
    Format a numeric value as currency.
    
    Args:
        value: Numeric value to format
        currency: Currency code (default: USD)
        
    Returns:
        Formatted currency string
    """
    if value is None or value == 'N/A':
        return 'N/A'
    
    try:
        if currency == "USD":
            return f"${value:,.2f}"
        elif currency == "INR":
            return f"₹{value:,.2f}"
        else:
            return f"{value:,.2f} {currency}"
    except (ValueError, TypeError):
        return str(value)

def format_percentage(value: float) -> str:
    """
    Format a numeric value as percentage.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted percentage string
    """
    if value is None or value == 'N/A':
        return 'N/A'
    
    try:
        return f"{value:.2f}%"
    except (ValueError, TypeError):
        return str(value)

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning a default value on division by zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return on division by zero
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default
