import os
import logging

class ActionManager:
    """
    Manages all actions that the agent can perform on webpage elements,
    including tracking action history.
    """

    def __init__(self, config, logger=None):
        """
        Initializes the ActionManager with configuration settings and an optional logger.

        Args:
            config (dict): Configuration dictionary to set up available actions.
            logger (logging.Logger, optional): A logger instance for recording actions.
        """
        self.config = config
        self.logger = logger or logging.getLogger("ActionManager")
        # Initialize action types from configuration or with default values
        self.action_space = config.get("action_space", ["CLICK", "PRESS ENTER", "HOVER", "SCROLL UP", 
                                                        "SCROLL DOWN", "NEW TAB", "CLOSE TAB", 
                                                        "GO BACK", "GO FORWARD", "TERMINATE", 
                                                        "SELECT", "TYPE", "GOTO", "MEMORIZE"])
        self.no_value_op = ["CLICK", "PRESS ENTER", "HOVER", "SCROLL UP", "SCROLL DOWN", "NEW TAB", 
                            "CLOSE TAB", "PRESS HOME", "PRESS END", "PRESS PAGEUP", "PRESS PAGEDOWN", 
                            "GO BACK", "GO FORWARD", "TERMINATE", "NONE"]
        self.with_value_op = ["SELECT", "TYPE", "GOTO", "MEMORIZE", "SAY"]
        self.no_element_op = ["PRESS ENTER", "SCROLL UP", "SCROLL DOWN", "NEW TAB", "CLOSE TAB", 
                              "GO BACK", "GOTO", "PRESS HOME", "PRESS END", "PRESS PAGEUP", 
                              "PRESS PAGEDOWN", "GO FORWARD", "TERMINATE", "NONE", "MEMORIZE", "SAY"]
        self.taken_actions = []

    def perform_action(self, target_element=None, action_name=None, value=None, element_repr=""):
        """
        Executes a specified action on a webpage element or the page itself.
        
        Args:
            target_element (dict, optional): Element details for interaction (if required).
            action_name (str): The type of action to perform (e.g., CLICK, TYPE).
            value (str, optional): Any additional value required for the action (e.g., text to type).
            element_repr (str, optional): A string representation of the target element.
        
        Returns:
            str: A description of the action taken.
        """
        if target_element:
            selector = target_element.get('selector')
            element_repr = target_element.get('description', element_repr)
        else:
            selector = None

        # Perform action based on action_name
        try:
            if action_name == "CLICK" and selector:
                selector.click()
                self.logger.info(f"Clicked on element: {element_repr}")
            elif action_name == "HOVER" and selector:
                selector.hover()
                self.logger.info(f"Hovered over element: {element_repr}")
            elif action_name == "TYPE" and selector and value:
                selector.fill(value)
                self.logger.info(f"Typed '{value}' into element: {element_repr}")
            elif action_name == "SCROLL UP":
                selector.evaluate("window.scrollBy(0, -window.innerHeight / 2)")
                self.logger.info("Scrolled up")
            elif action_name == "SCROLL DOWN":
                selector.evaluate("window.scrollBy(0, window.innerHeight / 2)")
                self.logger.info("Scrolled down")
            elif action_name == "PRESS HOME":
                selector.keyboard.press("Home")
                self.logger.info("Pressed Home key")
            elif action_name == "PRESS END":
                selector.keyboard.press("End")
                self.logger.info("Pressed End key")
            elif action_name == "PRESS PAGEUP":
                selector.keyboard.press("PageUp")
                self.logger.info("Pressed PageUp key")
            elif action_name == "PRESS PAGEDOWN":
                selector.keyboard.press("PageDown")
                self.logger.info("Pressed PageDown key")
            elif action_name == "NEW TAB":
                selector.context.new_page()
                self.logger.info("Opened a new tab")
            elif action_name == "CLOSE TAB":
                selector.close()
                self.logger.info("Closed the current tab")
            elif action_name == "GO BACK":
                selector.go_back()
                self.logger.info("Navigated back")
            elif action_name == "GO FORWARD":
                selector.go_forward()
                self.logger.info("Navigated forward")
            elif action_name == "GOTO" and value:
                selector.goto(value)
                self.logger.info(f"Navigated to {value}")
            elif action_name == "PRESS ENTER" and selector:
                selector.press('Enter')
                self.logger.info(f"Pressed Enter on element: {element_repr}")
            elif action_name == "SELECT" and selector and value:
                selector.select_option(value)
                self.logger.info(f"Selected option '{value}' from element: {element_repr}")
            elif action_name == "TERMINATE":
                self.logger.info("Task has been marked as complete. Terminating...")
            elif action_name == "NONE":
                self.logger.info("No action necessary at this stage. Skipped.")
            elif action_name == "SAY" and value:
                self.logger.info(f"Saying to the user: {value}")
            elif action_name == "MEMORIZE" and value:
                self.logger.info(f"Memorized content: {value}")
            else:
                raise ValueError(f"Unsupported or improperly specified action: {action_name}")
            
            # Log the action and return a summary
            action_summary = f"{action_name}: {element_repr or 'No Element'} -> {value or 'No Value'}"
            self.taken_actions.append(action_summary)
            return action_summary
        
        except Exception as e:
            error_msg = f"Error performing {action_name} on {element_repr}: {e}"
            self.logger.error(error_msg)
            return error_msg

    def update_action_space(self, new_actions):
        """
        Updates the list of allowed actions for the agent.

        Args:
            new_actions (list): A new list of actions to replace the current action space.
        """
        if isinstance(new_actions, list) and all(isinstance(action, str) for action in new_actions):
            self.action_space = new_actions
            self.logger.info("Action space updated.")
        else:
            self.logger.warning("Invalid action space provided. Must be a list of strings.")

    def get_action_space(self):
        """
        Returns the current list of allowed actions.
        
        Returns:
            list: The current action space.
        """
        return self.action_space

    def save_action_history(self, filename="action_history.txt"):
        """
        Saves the history of actions taken by the agent to a file.

        Args:
            filename (str): Name of the file to save the history to.
        """
        directory = self.config.get("basic", {}).get("save_file_dir", "seeact_agent_files")
        if not os.path.exists(directory):
            os.makedirs(directory)

        history_path = os.path.join(directory, filename)
        with open(history_path, 'w') as f:
            for action in self.taken_actions:
                f.write(action + '\n')
        
        self.logger.info(f"Action history saved to {history_path}")

    def clear_action_history(self):
        """
        Clears the history of actions taken by the agent.
        """
        self.taken_actions.clear()
        self.logger.info("Action history cleared.")
