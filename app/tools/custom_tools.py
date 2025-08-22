import datetime
import pytz
from smolagents import tool

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A tool that does nothing yet.
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return f"Tool received arg1={arg1}, arg2={arg2}"
