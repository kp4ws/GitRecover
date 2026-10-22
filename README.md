# Git Recover
This project provides a GUI program to aid users in resolving any issues they may have in one of their projects that has a git repo. 

Issues that users may run into, include some of the following scenarios:
- Lost work, due to a hard reset
- 

## Repository Structure
`GitRecover/`: The package directory, containing the source code of the application.  
`GitRecover/ai`: Subpackage for LLM-related code.    
`GitRecover/git`: Subpackage for Git-related functionality.    
`GitRecover/gui`: Subpackage for the user interface.  
`GitRecover/services`: Subpackage for app services.  
`GitRecover/workers`: Subpackage for background workers.  
`GitRecover/config.toml`: Configuration file for the app.  
`GitRecover/config.py`: Module for loading and managing the configuration file.  
`GitRecover/main.py`:  Entry point of the application. Instantiates the GUI and injects dependencies.      
`run.py`: Script at the project root for launching or building the application.  
`tests/`: The tests directory, containing all of the use case scenarios for evaluating and testing the system.

## Setup & Installation
1. Open your terminal window and **create a virutal environment**

## Activating Virtual Environment
### Windows

### Linux
`. venv/bin/activate`

## Build Instructions
`pyinstaller --name git-recover --onefile run.py`

## Running Program
`py -m GitRecover.main`

## Configuration Settings
config.toml contains the default configuration for the program, specifically the local LLM model. These settings can be adjusted as needed.

### LLM configuration
- `model_path` The path where the local LLM .gguf file is stored (by default, it's located in GitRecover/models)
- `n_ctx` Context Size (the max number of tokens)
- `n_threads` Number of CPU threads

---


## Program Pipeline
The general program pipeline follows these steps:  
1. The user encounters a problem in their git repo so they run GitRecover software.
2. In the console window of GitRecover, they enter a prompt and submit a recovery request.
3. Behind the scenes, the system collects relevant data from the .git directory and extracts it into a JSON payload.
4. The payload is sent off to the local LLM for inference.
5. The LLM contains specific instructions to act as a git recovery agent and analyzes the JSON payload, and determines the sequence of steps the user can do to resolve their problem.
6. Once LLM response is complete, it's transmitted back, filtered, and presented to the user.
7. Using the sequence of steps, the user can attempt to fix their problem or continue prompting the system for more help.

## Program Inputs & Outputs
### Inputs:
- Git repo file path.
- User prompt.

### Outputs:
- Sequence of steps to try and resolve the user's issue.


## Local LLM Models
By default the program uses ______ model, retrieved from ""...  

### Loading a new model
To use a separate model, the user can provide ...

## Troubleshooting & Known Issues
- Must supply the system with the local .gguf model
- LLM response can sometimes take some time to process