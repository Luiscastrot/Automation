import logging
import logging.handlers
import os
from datetime import datetime
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=52.52&longitude=13.41')
    if r.status_code == 200:
        data = r.json()
        elevation = data["elevation"]
        logger.info(f'Elevation: {elevation}')
        timestamp = datetime.now().isoformat()
        output_file = "elevation_data.txt"
        print(f'Writting into file {timestamp}, {elevation}\n')
        with open(output_file, "w", encoding="utf8") as file:
            file.write(f"{timestamp}, {elevation}\n")
        print(f'Writting done')
        logger.info(f"Data written to {output_file}")