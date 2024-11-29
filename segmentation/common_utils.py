import logging


def setup_logger():
    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum logging level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            logging.StreamHandler(),  # Log to the console
        ],
    )

    # Create a logger instance
    logger = logging.getLogger(__name__)
    return logger
