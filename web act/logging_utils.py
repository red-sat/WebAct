import os
from datetime import datetime

def setup_logger(log_dir, filename="agent.log", redirect_to_dev_log=False):
    """
    Sets up and configures the logging system for the agent, creating log files
    and managing output formatting. Allows logs to be redirected to a development
    log if specified.

    Args :
        log_dir (str): The directory path where log files will be saved.
        filename (str): The name of the main log file. Defaults to 'agent.log'.
        redirect_to_dev_log (bool): If True, logs are redirected to 'dev.log' in
            the same directory for development purposes. Defaults to False.

    Returns:
        logging.Logger: A configured logger instance for tracking agent activities.
    """
    # Create log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define log file path based on whether we're redirecting to dev log
    log_file = os.path.join(log_dir, "dev.log" if redirect_to_dev_log else filename)

    # Initialize the logger and set its level
    logger = logging.getLogger("AgentLogger")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if logger is already set up
    if not logger.handlers:
        # Create file handler to write logs to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Create a console handler to output logs to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Define the logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Apply formatter to both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # Initial log message indicating the logger has been set up
    logger.info(f"Logging setup complete. Logs are being saved to {log_file}")

    return logger
