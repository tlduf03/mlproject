import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #log file title
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path, exist_ok=True) #keep on updating

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

#overriding logging config
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,

)

# test script for python3 src/logger.py
# if __name__=="__main__":
#     logging.info("Logging has started")