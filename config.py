"""
Configuration file for Supabase connection
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def validate_config():
    """Validate that required configuration variables are set"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False, "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
    return True, "Configuration valid"
