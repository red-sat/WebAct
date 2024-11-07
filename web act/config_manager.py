import os
import toml

class ConfigManager:
    """
    Handles the loading and management of configuration settings for the agent.
    """

    def __init__(self, config_path=None):
        """
        Initializes the ConfigManager with an optional path to a configuration file.
        If no path is provided, default settings will be used.
        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        Loads the configuration from a TOML file if provided; otherwise, falls back to default settings.

        Returns:
            dict: The loaded or default configuration.
        """
        if self.config_path and os.path.isfile(self.config_path):
            try:
                with open(self.config_path, 'r') as config_file:
                    print(f"Configuration File Loaded - {self.config_path}")
                    return toml.load(config_file)
            except toml.TomlDecodeError:
                print(f"Error: File '{self.config_path}' is not a valid TOML file.")
            except FileNotFoundError:
                print(f"Error: File '{self.config_path}' not found.")
        # Return default configuration if file loading fails
        return self.default_config()

    def default_config(self):
        """
        Provides a default configuration in case no configuration file is found or loading fails.

        Returns:
            dict: The default configuration settings.
        """
        return {
            "basic": {
                "save_file_dir": "seeact_agent_files",
                "default_task": "Find the pdf of the paper 'GPT-4V(ision) is a Generalist Web Agent, if Grounded'",
                "default_website": "https://www.google.com/",
                "crawler_mode": False,
                "crawler_max_steps": 10
            },
            "agent": {
                "input_info": ["screenshot"],
                "grounding_strategy": "text_choice_som",
                "max_auto_op": 50,
                "max_continuous_no_op": 5,
                "highlight": False
            },
            "openai": {
                "rate_limit": -1,
                "model": "gpt-4o",
                "temperature": 0.9
            },
            "browser": {
                "headless": False,
                "args": [],
                "browser_app": "chrome",
                "persistant": False,
                "persistant_user_path": "",
                "save_video": False,
                "viewport": {
                    "width": 1280,
                    "height": 720
                },
                "tracing": False,
                "trace": {
                    "screenshots": True,
                    "snapshots": True,
                    "sources": True
                }
            }
        }

    def validate_config(self, config):
        """
        Validates the provided configuration to ensure it meets required structures and value ranges.
        Can add specific checks here based on anticipated fields and their acceptable values.

        Args:
            config (dict): The configuration dictionary to validate.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        # Check required top-level sections
        required_sections = ["basic", "agent", "openai", "browser"]
        for section in required_sections:
            if section not in config:
                print(f"Warning: Missing '{section}' section in configuration.")
                return False

        # Example validation for specific fields
        if "crawler_max_steps" in config["basic"] and not isinstance(config["basic"]["crawler_max_steps"], int):
            print("Error: 'crawler_max_steps' must be an integer.")
            return False
        if "model" in config["openai"] and not isinstance(config["openai"]["model"], str):
            print("Error: 'model' must be a string.")
            return False
        if "viewport" in config["browser"] and not isinstance(config["browser"]["viewport"], dict):
            print("Error: 'viewport' must be a dictionary.")
            return False

        # All checks passed
        return True
