import logging
import subprocess

is_git_repo = subprocess.run(
    ["git", "rev-parse"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

logger = logging
if is_git_repo.returncode == 0:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

logger.basicConfig(
    level=logging_level,
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
