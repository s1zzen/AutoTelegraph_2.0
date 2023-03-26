import os
from dotenv import load_dotenv

REDIS_PATH = os.environ.get('REDIS_PATH') or 'redis://localhost'
load_dotenv('cfg.env')

BASE_PATH = os.getenv('BASE_PATH') or './src/'


SHORT_NAME = os.getenv('SHORT_NAME') or 'Jomics'
AUTHOR_NAME = os.getenv('AUTHOR_NAME') or 'Jomics'
AUTHOR_URL = os.getenv('AUTHOR_URL') or 'https://t.me/+ZothWDmxc8AxNmJk'
