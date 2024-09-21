# AI Agent for PDF Answer Extraction (Slack Bot)

This project features an AI agent that utilizes a large language model to extract answers from the content of extensive PDF documents. The extracted results are then posted directly to Slack, facilitating seamless communication and information sharing.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Contact](#contact)


## Features
- Extract answers from large PDF documents using a OpenAI large language model.
- Once the PDF is uploaded we will keep it the Cache to reduce the load for the next time.
- Not Used Any Chaining Approach Created Entire Pipeline to get the Answer.
- Slack Bot will post the Answers to the Channel.

## Installation

To get started, clone this repository and install the necessary dependencies:

- If you are going to use Docker to run the application, please refer to the [SetupContainer](#setupcontainer)

### Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### Install the dependencies using Conda (Anaconda / Miniforge)

- For installing the environment:

```bash
conda env create -f environment.yml
```
- For updating the environment:

```bash
conda env update --file environment.yml --prune
```

### Install the dependencies using Pip

```bash
pip install -r requirements.txt
```

## SetupContainer

- If you have Docker installed on your machine, you can run the container using the following command:

```bash
docker-compose up --build
```

- If you want to run it in the detached mode, you can use the following command:

```bash
docker-compose up --build -d
```

## Configuration

### Setup the environment variables

- Create .env file

```bash
touch .env
```

- Copy the .env.example file to .env or take it from here

```bash
OPENAI_API_KEY=<PAST_YOUR_OPENAI_API_KEY>
SLACK_API_TOKEN=<PAST_YOUR_SLACK_API_TOKEN>
SLACK_CHANNEL=<'REPLACE_WITH_YOUR_SLACK_CHANNEL'>
CORS_ORIGINS=<'REPLACE_WITH_YOUR_CORS_ORIGINS'>
```

### How to setup Slack Bot

- Go to this website: https://api.slack.com/apps/new

1. Create an app by choosing the from the scratch > Name for the app & Choose workspace

<img width="520" alt="Screenshot 2024-09-21 at 2 23 58 PM" src="https://github.com/user-attachments/assets/497ead5e-cbb7-42d2-bbb3-a0bed49579a4">

2. Go to OAuth & Permissions section of the side panel setup the Scope

<img width="661" alt="Screenshot 2024-09-21 at 2 29 31 PM" src="https://github.com/user-attachments/assets/078d4e78-9433-486f-a632-a78c0a798939">

3. Now click the Install button under the OAuth Tokens section

4. Now you will get an Bot User OAuth Token

5. Copy it and paste it in .env file

6. Now go to the Workspace and Select Any Channel if there is no one Create one

7. After Selecting the Channel use @you-bot-name and add the Bot to the Channel


## Contact

- If you have any questions or suggestions, please feel free to reach out to me on [Twitter](https://twitter.com/thanseefpptwitt) or [GitHub](https://github.com/thanseefpp)