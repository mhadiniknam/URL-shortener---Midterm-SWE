import os
from urllib.parse import quote_plus

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD', ''))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# TTL configuration for bonus feature
MINUTES_TTL_APP = int(os.getenv('MINUTES_TTL_APP', 1440))  # Default to 24 hours