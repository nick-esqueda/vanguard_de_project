# Welcome to the Data Engineering Take Home Project!

This is my submission for Vanguard's Data Engineering Apprenticeship take home project. 

## Important:

If you would like to see all of the git commit and branch history, please stop by the original version of this repo! This fork was created to submit the project after completion, but all of the git history exists in my personal repo here:
> [Nick Esqueda - Vanguard DE Project](`https://github.com/nick-esqueda/vanguard_de_project`)

## About Me:

> [Nick Esqueda](https://www.nickesqueda.com/) (my portfolio site!)

> Here's a link to my [GitHub](https://github.com/nick-esqueda).

> Say hi on [LinkedIn](https://www.linkedin.com/in/nick-esqueda/)!


# Quick Start

Here are a series of steps to run the project! This project was created to be somewhat interactive from the command line - after running one command, all processes will run (ingestion, transformation, loading, and analytics), and feedback on the progress of the program will be output to your terminal!

## Setup

1. Create a file named `.env`.

2. Copy and paste everything from `.env.example` into your `.env` file.

3. Provide your spotify client id and client secret keys to the `.env` file.

## Running the Program

1. `cd` into the root directory.
2. Run `pipenv install` to create the virtual environment and install all project dependencies.
3. There are 2 different ways you can run this program. From the root directory, you can either:
    1. Run `pipenv run python -m app`.
- OR:
	1. Run `pipenv shell` to enter the shell subprocess.
	2. Then, run `python -m app` to run the program!

After the program has been run, you can check the *app/images* directory to see the visualizations that have been created as a result of the program.
