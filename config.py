import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATA_PATH = os.path.join('data', 'HSN_Master_Data.xlsx')
    CACHE_EXPIRY = 3600  # 1 hour cache expiry
    MAX_BATCH_SIZE = 100  # Maximum codes per batch request