# Nebius Assignment

# Description
Implementation of the Nebius assignment task, which serves as a preliminary qualification test
for Nebius Agenitc AI course.

# Repository Content
Root Folder
  app.py                  # FastAPI application
  requirements.txt
  src
    auxiliary
      config.py           # parameters initialized either by enviromental parameters or hard-coded
      utils.py            # Definition of some classes and functions
    llm
      base.py             # LLM inteface definition
      openai_provider.py  # Implementation of OpenAI LLM
    prompts
      consider_src.txt    # A prompt to the LLM, which consider source files
      ignore_src.txt      # A prompt that ignores source files
    services
      github_service.py   # 
    
