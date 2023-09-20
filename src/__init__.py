import os
import openai
import logging
import logging.handlers
from dotenv import load_dotenv

load_dotenv()

current_directory = os.getcwd()
if os.path.isdir(current_directory+"/logs/") == False:
	os.makedirs(current_directory+"/logs/")

my_logger = logging.getLogger("logger")
my_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(message)s")
handler = logging.handlers.RotatingFileHandler(
	current_directory+"/logs/logs.log", maxBytes=5000000, backupCount=5)
handler.setFormatter(formatter)
my_logger.handlers = []
my_logger.addHandler(handler)
my_logger.addHandler(logging.StreamHandler())

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
chromadb_path = current_directory+"/src/embeddings/chromadb"
openai_embedding_model = "text-embedding-ada-002"