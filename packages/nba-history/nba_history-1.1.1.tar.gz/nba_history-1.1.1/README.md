![Alt text](https://raw.githubusercontent.com/odonnell31/nba_history/master/docs/img/logos/nba_history_logo_v3j.jpg)
-----------------
[![Version](https://badge.fury.io/py/nba-history.svg)](https://badge.fury.io/py/nba-history.svg)
[![Downloads](https://pepy.tech/badge/nba-history)](https://pepy.tech/project/nba-history)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://img.shields.io/badge/coverage-100%25-brightgreen)

**nba_history** is a python package for dynamically scraping NBA player, team, and draft data.

All nba_history functions return scraped data as a `pandas dataframe` with an option to also export to `CSV`.

## Example
A *short example for scaping NBA draft data* is below:

```python
from nba_history import player_data, team_data

# scrape 2013 NBA draft picks
df = player_data.scrape_draft_data(start_year = 2013,
	end_year = 2013,
	export = False)
	
print(df.head())
```


![Alt text](https://raw.githubusercontent.com/odonnell31/nba_history/master/docs/img/draft_picks_example.png)


## Installation
nba_history depends on the Python modules [requests](https://pypi.org/project/requests/), [beautifulsoup](https://pypi.org/project/beautifulsoup4/), and [pandas](https://pypi.org/project/pandas/)

**Installation with pip:** if you have ``pip`` installed, type this in a terminal:

```console
$ python -m pip install nba_history
```

**Installation by hand:** download the sources, either from [PyPI](https://pypi.org/project/nba-history/) or, if you want the development version, from [GitHub](https://github.com/odonnell31/nba_history), unzip everything into one folder, open a terminal and type:

```console
$ (sudo) python setup.cfg install
```

-----------------
# Documentation
The nba_history package has 2 modules, [player_data](https://raw.githubusercontent.com/odonnell31/nba_history/master/src/nba_history/player_data.py) and [team_data](https://raw.githubusercontent.com/odonnell31/nba_history/master/src/nba_history/team_data.py)

### List of all functions in player_data module

#### scrape_draft_data
Scrape NBA draft data by year, including:
* draft round
* draft pick number
* college
* years in the NBA
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*

```python
from nba_history import player_data

# scrape 2017-2020 NBA draft picks
df = player_data.scrape_draft_data(start_year = 2017,
	end_year = 2020,
	export = True)
```

#### scrape_player_total_stats
Scrape NBA player total stats by year, including:
* Points
* Rebounds
* Assists
* Minutes
* Games
* 3PA
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*
`sleep_time`: time to pause function between sraping each year. Default is set as 2 seconds, if scraping >10 years then changing to 1 second is recommended.

```python
from nba_history import player_data

# scrape 2011-2015 player total stats
df = player_data.scrape_player_total_stats(start_year = 2011,
	end_year = 2015,
	export = True,
	sleep_time = 2)
```

#### scrape_player_per_game_stats
Scrape NBA player per game stats by year, including:
* Points
* Rebounds
* FG%
* Minutes
* 3P%
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*
`sleep_time`: time to pause function between sraping each year. Default is set as 2 seconds, if scraping >10 years then changing to 1 second is recommended.

```python
from nba_history import player_data

# scrape 2000-2009 player per game stats
df = player_data.scrape_player_per_game_stats(start_year = 2000,
	end_year = 2009,
	export = True,
	sleep_time = 2)
```

#### scrape_player_advanced_stats
Scrape NBA player advanced stats by year, including:
* PER
* WS
* ORB%
* 3PAr
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*
`sleep_time`: time to pause function between sraping each year. Default is set as 2 seconds, if scraping >10 years then changing to 1 second is recommended.

```python
from nba_history import player_data

# scrape 1998-2001 player per game stats
df = player_data.scrape_player_advanced_stats(start_year = 1998,
	end_year = 2001,
	export = True,
	sleep_time = 2)
```

#### scrape_player_shooting_stats
Scrape NBA player shooting stats by year, including:
* Dunks
* FG% by distance
* % of FG by distance
* Corner 3PT%
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*
`sleep_time`: time to pause function between sraping each year. Default is set as 2 seconds, if scraping >10 years then changing to 1 second is recommended.

```python
from nba_history import player_data

# scrape 1980-1985 player per game stats
df = player_data.scrape_player_shooting_stats(start_year = 1980,
	end_year = 1985,
	export = True,
	sleep_time = 2)
```

#### scrape_all_stars
Scrape all NBA All-Stars for alltime, including:
* Hall of Fame status
* All Star appearances
* and more..

`export`: option to export to CSV. Default is set as *True*

```python
from nba_history import player_data

# scrape all NBA All-Stars alltime
df = player_data.scrape_all_stars(export = True)
```

### List of all functions in team_data module

#### scrape_nba_team_records
Scrape NBA team records by year, including:
* Playoff appearance
* Wins
* Losses
* PPG
* and much more..

`start_year`: first year to scrape
`end_year`: last year to scrape
`export`: option to export to CSV. Default is set as *True*

```python
from nba_history import team_data

# scrape 2010-2018 player per game stats
df = team_data.scrape_nba_team_records(start_year = 2010,
	end_year = 2018,
	export = True)
```
-----------------


## Contribute
nba_history is open-source library originally written by [odonnell31](https://github.com/odonnell31) and released under the MIT licence. The project is hosted on [GitHub](https://github.com/odonnell31/nba_history), where everyone is welcome to contribute, ask for help or simply give feedback.

## Maintainers
* [@odonnell31](https://github.com/odonnell31) (owner)