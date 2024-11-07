# prompt_manager.py

class PromptManager:
    """
    Manages prompt generation and updates, including initializing prompt templates
    and creating task-specific prompts based on the current task, previous actions,
    and available choices.
    """

    def __init__(self, config):
        """
        Initializes the PromptManager with configuration settings and prepares initial prompts.

        Args:
            config (dict): Configuration dictionary containing prompt settings.
        """
        self.config = config
        self.prompts = self._initialize_prompts()

    def _initialize_prompts(self):
        """
        Sets up the initial prompts with action descriptions and system instructions.
        
        Returns:
            dict: A dictionary of initial prompts with descriptions for each prompt type.
        """
        action_format = "ACTION: Choose an action from allowed actions."

        return {
            "system_prompt": '''You are assisting humans in web navigation tasks step by step. 
            At each stage, you can see the webpage by a screenshot and know the previous actions 
            that have been executed for this task. You need to decide on the next action to take.''',

            "action_space": '''
Here are the descriptions of all allowed actions:

No Value Operations:
- CLICK: Click on a webpage element using the mouse.
- HOVER: Move the mouse over a webpage element without clicking.
- PRESS ENTER: Press the Enter key to submit or confirm an input.
- SCROLL UP: Scroll up on the page.
- SCROLL DOWN: Scroll down on the page.
- PRESS HOME: Go to the top of the page.
- PRESS END: Go to the bottom of the page.
- PRESS PAGEUP: Scroll up by one page.
- PRESS PAGEDOWN: Scroll down by one page.
- CLOSE TAB: Close the current tab.
- NEW TAB: Open a new tab.
- GO BACK: Navigate to the previous page.
- GO FORWARD: Navigate to the next page.
- TERMINATE: End the task if completed or if the task is risky.
- NONE: Skip an action if unnecessary at this stage.

With Value Operations:
- SELECT: Choose an option from a dropdown menu.
- TYPE: Enter text into a text box.
- GOTO: Navigate to a specific URL.
- SAY: Output information to the user.
- MEMORIZE: Store content for reference.
''',

            "question_description": '''The screenshot below shows the webpage. Think through each step 
            before deciding on the next action. Clearly outline the element to interact with, 
            its location, and the action to perform. Follow these rules:
1. Issue only one valid action per step.
2. Handle dropdowns directly; options will be listed.
3. Avoid account creation, login, or final submissions.
4. Terminate if task is complete or requires potentially harmful actions.
5. Interact with floating banners, closing them if they cover content.
6. Type or select inputs directly, bypassing clicks when possible.
7. Avoid repeating the same failed action consecutively.
8. Ignore minor banners (e.g., cookie policies).
9. Press ENTER after typing in search or text inputs.
10. Choose the least obstructed clickable button if options are identical.''',

            "referring_description": """(Reiteration)
Reiterate your next target element, its location, and the corresponding action.

(Multi-choice Question)
Below is a multi-choice question with elements arranged by their height on the page, 
from top to bottom and left to right. From the screenshot, locate and match each choice 
with its corresponding element by examining the content and HTML details. Then choose the 
matching element based on your target action.""",

            "element_format": '''(Final Answer)
Conclude with the following format for the target element:

ELEMENT: The uppercase letter representing your choice.''',

            "action_format": action_format,
            "value_format": '''VALUE: Provide additional input as needed based on ACTION (if not needed, write "None")'''
        }

    def generate_prompt(self, task=None, previous=None, choices=None):
        """
        Creates a prompt based on the current task, previous actions, and available choices.
        
        Args:
            task (str): The current task description.
            previous (list): A list of previous actions taken.
            choices (list): A list of choices or elements available on the webpage.
        
        Returns:
            list: A list of prompt parts for the agent to process.
        """
        prompt_list = []

        # Access initial prompt parts
        system_prompt_input = self.prompts["system_prompt"]
        action_space_input = self.prompts["action_space"]
        question_description_input = self.prompts["question_description"]
        referring_input = self.prompts["referring_description"]
        element_format_input = self.prompts["element_format"]
        action_format_input = self.prompts["action_format"]
        value_format_input = self.prompts["value_format"]

        # Construct prompt sections based on task, previous actions, and choices
        prompt_list.extend(
            self._generate_new_query_prompt(
                system_prompt=system_prompt_input + "\n" + action_space_input,
                task=task,
                previous_actions=previous,
                question_description=question_description_input
            )
        )
        
        # Add referring description and choice-related formats
        prompt_list.append(
            self._generate_new_referring_prompt(
                referring_description=referring_input,
                element_format=element_format_input,
                action_format=action_format_input,
                value_format=value_format_input,
                choices=choices
            )
        )

        return prompt_list

    def update_prompt_part(self, part_name, new_text):
        """
        Updates a specific part of the prompt based on provided part name and text.
        
        Args:
            part_name (str): The name of the prompt part to update.
            new_text (str): The new text to replace the current prompt part.
        
        Returns:
            bool: True if the part was updated, False otherwise.
        """
        if part_name in self.prompts:
            self.prompts[part_name] = new_text
            return True
        else:
            print(f"Prompt part '{part_name}' not found.")
            return False

    def _generate_new_query_prompt(self, system_prompt, task, previous_actions, question_description):
        """
        Generates a query prompt with system prompt, task, previous actions, and question description.
        
        Args:
            system_prompt (str): The system's main guidance.
            task (str): The task description.
            previous_actions (list): The actions already taken by the agent.
            question_description (str): Detailed instructions on how to interpret the screenshot.
        
        Returns:
            list: A formatted query prompt for generating the next action.
        """
        # Combine system prompt, task, previous actions, and question description
        return [f"{system_prompt}\nTask: {task}\nPrevious Actions: {previous_actions}\n{question_description}"]

    def _generate_new_referring_prompt(self, referring_description, element_format, action_format, value_format, choices):
        """
        Generates a referring prompt to guide element selection based on choices and formats.
        
        Args:
            referring_description (str): Instructions for locating elements based on choices.
            element_format (str): The format for specifying the target element.
            action_format (str): The format for specifying the action.
            value_format (str): The format for specifying any input value.
            choices (list): Available element choices on the webpage.
        
        Returns:
            str: A formatted prompt string for element selection and action grounding.
        """
        choices_str = "\n".join(choices) if choices else "No choices available"
        return f"{referring_description}\nChoices:\n{choices_str}\n\n{element_format}\n{action_format}\n{value_format}"
