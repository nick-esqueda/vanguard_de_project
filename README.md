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

> Note: a `.cache` file may be created in the root directory after the extraction phase. This is created as a result of (and to the benefit of) querying the Spotify API and can largely be ignored.

# About

This is an overview of the different stages/processes involved in this project and how each of them get executed.

> The entry point of this program is `app/__main__.py`. Feel free to take a look at it to see the flow of the application from a high level. 
> 
> This file imports and runs all of the functions required to run the program at each phase: 
>
> _Ingestion -> Transformation -> Storage -> Analytics / Visualization_.

## Ingestion / Transformation

For the ingestion phase, the program runs a series of functions, such as `extract_artists()`, `extract_artists_albums()`, and more to fetch data from the Spotify API. That data, after being received, is then pruned down to only the desired fields, using `prune()` and `prune_all()`. At this point, the data is ready to be cleaned and transformed to fit specifications.

### Note:
After a certain set of data has been received and pruned, it is immediately cleaned/transformed and deduplicated. This strategy is used to save unnecessary requests to Spotify's API - without deduplication, requests for resources that depend on the results of a previous request might ask for the same data multiple times, slowing down the program. 

> Ex: the request for `albums_tracks()` requires album ids as input. If there are duplicate album ids, then those duplicates will each be fetched, even though only response for that album is needed.

Cutting down on unnecessary queries allows the program to avoid wasting time waiting for the API request to finish. This is why both the ingestion and transformation phases will be executed "at the same time".

## Storage
The storage phase, starting off from the call to `load_all()` in `\__main__.py`, simply takes all of the cleaned and transformed data and stores it inside of the SQLite database file, located in `app/data/spotify.db`. 

To dive deeper, first, a connection needs to be made to the SQLite database. The `DB` class from `app/utils/db.py` serves this purpose, and an instance of that class is then used to run SQL statements against the database to create these tables:

* `artists` 
* `albums` 
* `tracks` 
* `track_features`

The `create_tables()` function inside of `load.py` runs that SQL.

Then, the `load_data()` function is used to insert the cleaned and transformed data into those newly created tables, using the same `DB` instance.

## Analytics / Visualization

