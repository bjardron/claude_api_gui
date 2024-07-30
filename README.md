## Claude API GUI Application

This project is a GUI application for interacting with the Claude API. It allows users to send messages, review files, and perform code reviews. The application is built using Python and the Tkinter library for the GUI.

## Features
`Send Messages`: Send messages to the Claude API with customizable system prompts, models, temperature settings, and max tokens.

`Review Files`: Stage individual files for review by the Claude API.

`Code Review`: Stage entire directories of code files for review by the Claude API.

`Save Conversations`: Save the conversation history to a text file.

`Drag and Drop Support`: Drag and drop files into the staging area for review.


## Installation
### Clone the repository:


```git clone https://github.com/bjardron/claude_api_gui.git ```

```cd claude_api_gui```
                

### Install the dependencies:

```pip install -r requirements.txt```

### Create config.py in project root

```API_KEY = "YOUR_API_KEY_HERE"```

Use `config.py.example` as reference

## Using the GUI:

`System Prompt`: Enter a custom system prompt for the API.


`Model`: Select the Claude model to use.


`Temperature`: Set the temperature for the API responses.


`Max Tokens`: Set the maximum number of tokens for the API responses.


`Message`: Enter your message in the message entry area and click "Send".


`Staged Files`: Click "Review File" to stage individual files or "Code Review" to stage entire directories.


`Save Conversation`: Click "Save Conversation" to save the chat history to a text file.


`Start New Chat`: Click "Start New Chat" to clear the conversation and start over.

`Review File`: Click "Review File" to send any file to the staging area for Claude

`Review Code`: Select an entire directory, it will pull any files 
on `allowed_extensions.py`, scrape the contents and send it in a message along with a system prompt to review the entire code base.

### File Structure

`main.py`: Entry point of the application.

`gui.py`: Defines the GUI and its functionalities.

`gui_layout.py`: Defines the layout of the GUI elements.

`file_manager.py`: Manages file operations.

`claude_api.py`: Handles interactions with the Claude API.

`allowed_extensions.py`: Contains the list of allowed file extensions for code review.

`config.py`: config file for storing the API key.




