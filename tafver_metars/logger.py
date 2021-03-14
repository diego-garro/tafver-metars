import logging
import subprocess

output = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True)

logger = logging
if output == "main":
    logging_level = logging.INFO
else:
    loggin_level = logging.DEBUG

logger.basicConfig(
    level=loggin_level,
    format="%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    handlers=[
        logging.FileHandler("./logging.log"),
        logging.StreamHandler(),
    ],
)

if __name__ == "__main__":
    logging.warning("warning level message")
    logging.info("info level message")
    logging.debug("debug level message")
    logging.error("error level message")
