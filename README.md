# Git Recover
This project provides a desktop GUI application to assist users in resolving any git-related issues in their projects. 

Common Git issues that users may run into include the following:
- Lost work, due to a `git reset --hard`
- Merge conflict confusion
- Accidental branch deletions

## Repository Structure
- `GitRecover/`: The package directory, containing the source code of the application.  
    - `ai`: Subpackage for LLM-related code.    
    - `git`: Subpackage for Git-related functionality.    
    - `gui`: Subpackage for the user interface.  
    - `services`: Subpackage for app services.  
    - `workers`: Subpackage for background workers.  
    - `config.toml`: Configuration file for the app.  
    - `config.py`: Module for loading and managing the configuration file.  
    - `main.py`:  Entry point of the application. Instantiates the GUI and injects dependencies.  
    - `utils.py`: Utility module containing helper functions for the application.     
- `run.py`: Script at the project root for launching or building the application.  
- `tests/`: The tests directory, containing all of the use case scenarios for evaluating and testing the system.

## Setup & Installation
**Create a Virutal Environment:**  
Open a terminal window at the project root and run:
`python -m venv venv`

**Activate the Virtual Environment:**  
Windows: `venv\Scripts\activate`  
Linux/ macOS: `. venv/bin/activate`  

**Install Dependencies:**  
`pip install -r requirements.txt` (ensure virtual environment is activate prior to running this command)

## Build Instructions
To compile the application into a standalone executable using PyInstaller:  
`pyinstaller --name git-recover --windowed --onefile run.py`

## Running the Program
`python run.py` OR `python -m GitRecover.main`

## Configuration Settings
config.toml contains the default configuration for the program, specifically the local LLM model settings.

### LLM configuration
- `model_path`: The file path where the local LLM `.gguf` file is stored (by default, it's located in `GitRecover/models/`)
- `n_ctx`: Context Size (the max number of tokens)
- `n_threads`: Number of CPU threads

---


## Program Pipeline
The general program pipeline follows these steps:  
1. The user encounters a problem in their git repo so they run GitRecover software.
2. In the console window of GitRecover, they enter a prompt and submit a recovery request.
3. Behind the scenes, the system collects relevant data from the .git directory and extracts it into a JSON payload.
4. The payload is sent off to the local LLM for inference.
5. The LLM contains specific instructions to act as a git recovery agent and analyzes the JSON payload, and determines the sequence of steps the user can do to resolve their problem.
6. Once LLM response is complete, it's sent back, filtered, and presented to the user.
7. Using the sequence of steps, the user can attempt to fix their problem or continue prompting the system for more help.

## Program I/O
### Inputs:
- Absolute path to the target Git Repository.
- User prompt, describing the issue.

### Outputs:
- Sequence of steps to help resolve the user's issue.


## Local LLM Models
By default, the program is configured to use **Qwen3-4B-Q4_K_M.gguf** retrieved from HuggingFace in `.gguf` format.

### Loading a new model
To use a different model:
1. Download a `.gguf model` from HuggingFace.
2. Place the file inside the `GitRecover/models/` directory.
3. Open `config.toml` and adjust the LLM settings accordingly (specifically the model_path to point to the new filename).

## Troubleshooting & Known Issues
- **Missing Model:** The application will fail to generate responses if a valid .gguf model is not supplied in the designated models directory.
- **Inference Delay:** Because the AI runs entirely locally on CPU/RAM, generating a response may take some time.

## Stretch Goals / Ideas
- Helper utility to help with git cherrypicking