Author: Christian Fayolle


# How to run the code (after starting the command line/terminal from the app directory):   

1) Install dependencies in requirements.txt using "pip3 install -r requirements.txt" (with python 3.11, 3.12 struggles with certain installations)  
2) Add your github_access_key and openai_api_key to the relavant variables in .env  
3) Run python3 with "python3 src/main.py {GITHUB_REPO_URL}" (e.g. "python3 src/main.py https://github.com/github/rest-api-description")

This will open a terminal conversation window for you to question the repo the URL points to.


# Limitations & Improvements:

+ This app only considers content from the .md files to provide answers from so it is very sensitive to poor documentation and repo-specific questions unrelated to .md file content

+ Due to file chunking, long .md files (over 1024 characters long) may be misinterpreted

+ Running in the terminal is a poor user experience, given more time I'd look to provide a more welcoming front end with a framework like streamlit

+ The current app is not containerised, given more time I'd definitely look into creating a docker container around this app to get it ready for production

+ As a point of risk: this app uses openai's embedding and text-davinci-003 models via API calls. So if there's an issue connecting to these models, the app would not function properly.  Pricing information for the models is available [here] (https://openai.com/pricing)