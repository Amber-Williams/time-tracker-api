# time-tracker-api

An app to track daily habits

### Requirements

1. Must have `poetry` installed on your system
2. To deploy app via serverless you'll need an AWS account and install `serverless` globally

### Set up

1. Activate the projects virtual environment - `poetry shell`
2. Install package dependencies - `poetry install`

### Running the application

1. `uvicorn app.main:app --reload`
2. (optional) visit http://127.0.0.1:8000/docs to see endpoint docs

### Deploying application

1. Run `serverless config credentials --provider aws --key YOUR_AWS_API_KEY --secret YOUR_AWS_API_SECRET`
2. At the repo root run `sls deploy`
3. Use endpoint that is logged following step 2 success
