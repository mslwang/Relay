from dotenv import load_dotenv
load_dotenv()

import os
import pymongo

client = pymongo.MongoClient(os.getenv("CONNECT"))

