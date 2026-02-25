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
      github_service.py   # Fetch the repository and extract its main information components
      summarizer.py       # Use the LLM for generating a summary descrition of the repo, based on the prompt and the repo's componenets


# LLM Choice
I chose to use OpenAI, as I'm most familiar with it for similar task, and it is also known to be
rather competative regarding code generation and analysis tasks.
The specific model I chose is gpt-4o-mini, which is known to be a good choice, from cost-performance perspective.

# Handle Repository Content
First I used the packages *httpx* and urllib
