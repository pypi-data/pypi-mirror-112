# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 11:45:09 2021

@author: Michael ODonnell

@purpose: scrape NBA draft picks by year
"""

# import needed libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# function to scrape a list of years of NBA Drafts
def scrape_draft_data(start_year = 2017, end_year = 2020, export = True):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty dataframe
    final_df = pd.DataFrame(columns = ['Pk', 'Tm', 'Player', 'College', 'Yrs',
                                       'G', 'MP', 'PTS', 'TRB', 'AST','FG%',
                                       '3P%', 'FT%', 'MP', 'PTS', 'TRB', 'AST',
                                       'WS', 'WS/48', 'BPM', 'VORP', 'round',
                                       'year'])
    # scape one year at a time
    for y in years:
    
        # define URL of draft class
        url = f'https://www.basketball-reference.com/draft/NBA_{y}.html'
        
        # create bs4 object using requests and bs4
        response = requests.get(url)
        
        # if response code != 200, print and exit
        if response.status_code != 200:  
            print("invalid url response code:", response.status_code)
            break
        
        html = response.text
        soup = BeautifulSoup(response.content, features = 'lxml')
        column_names = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
        table_rows = soup.findAll('tr')[0:]
        draft_picks = [[td.getText() for td in table_rows[i].findAll('td')]
                        for i in range(len(table_rows))]
        
        # function to find length of each draft round
        def find_draft_rounds(draft_picks:list):
            # this will store number of picks in each round
            round_cutoffs = []
            
            # find empty lists, they indicate new draft round
            for index, value in enumerate(draft_picks[2:]):
                if value == []:
                    round_cutoffs.append(index)
            
            # since there are always 2 empty lists in a row, only use 2nd
            round_cutoffs = round_cutoffs[::2]
            
            # print the total number of round in draft class
            print(f"total rounds of the {y} draft:", len(round_cutoffs)+1)
            print(f"picks per round in {y} draft:", round_cutoffs[0])
            
            return round_cutoffs
        
        
        # call find_draft_rounds on the data
        round_cutoffs = find_draft_rounds(draft_picks)
        
        # remove empty rows from draft_picks
        draft_picks = [e for e in draft_picks if len(e) > 10]
        
        # create dataframe for all draft_picks
        draft_picks_df = pd.DataFrame(draft_picks, columns = column_names[1:])
        print(f"total draft picks in the {y} draft:", len(draft_picks_df["Pk"]))
        
        # create column for draft round and draft year
        draft_picks_df["round"] = 1
        draft_picks_df["year"] = y
        
        # change column Pk to integer
        draft_picks_df["Pk"] = pd.to_numeric(draft_picks_df["Pk"])
        
        # assign correct draft round to each row
        for index, picks in enumerate(round_cutoffs):
            draft_picks_df.loc[(draft_picks_df.Pk > picks), "round"] = int(index)+2
        
        # add draft picks to final_df (with all draft picks)
        try:
            final_df = final_df.append(draft_picks_df)
            print(f"draft year {y} added to final dataframe")
            
        except:
            print(f"error with draft year {y}, data not collected")
        
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(2)
        
    # rename final_df columns
    final_df = final_df.rename(columns = {final_df.columns[0]: "Pick",
                                          final_df.columns[1]: "Team",
                                          final_df.columns[4]: "Years",
                                          final_df.columns[5]: "Career_Games",
                                          final_df.columns[8]: "Career_Rb",
                                          final_df.columns[9]: "Career_Ast",
                                          final_df.columns[13]: "MPG",
                                          final_df.columns[14]: "PPG",
                                          final_df.columns[15]: "RbsPG",
                                          final_df.columns[16]: "AstPG",
                                          final_df.columns[7]: "Career_Pts",
                                          final_df.columns[6]: "Career_Minutes"})
    # export and return the dataframe
    if export == True:
        export_name = f"nba_draft_data_{start_year}_to_{end_year}" + ".csv"
        final_df.to_csv(export_name, index = False)
        
    return final_df


# function to scrape a list of years for NBA PLayer total stats
def scrape_player_total_stats(start_year = 2017, end_year = 2020,
                              export = True, sleep_time = 2):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty final dataframe to append to in for loop
    player_total_stats = pd.DataFrame(columns = ['Player', 'Pos', 'Age', 'Tm', 'G',
                                           'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
                                           '3PA', '3P%', '2P', '2PA', '2P%',
                                           'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                                           'DRB', 'TRB', 'AST', 'STL', 'BLK',
                                           'TOV', 'PF', 'PTS', 'year'])
    
    # loop through each year in the list
    for y in years:
        
        # grab URLs for year y
        totals_url = f'https://www.basketball-reference.com/leagues/NBA_{y}_totals.html'
        
        # create bs4 object using requests and bs4
        totals_response = requests.get(totals_url)
        print(f"totals year {y} url response code:", totals_response.status_code)
        html = totals_response.text
        soup = BeautifulSoup(totals_response.content, features = 'lxml')
        
        # grab table column names and rows
        column_names = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        table_rows = soup.findAll('tr')[0:]
        player_stats = [[td.getText() for td in table_rows[i].findAll('td')]
                                for i in range(len(table_rows))]
        
        # drop empty rows
        player_stats = [e for e in player_stats if len(e) > 10]
        
        # create dataframe for stats
        player_stats_df = pd.DataFrame(player_stats, columns = column_names[1:])
        # add year to dataframe
        player_stats_df["year"] = y
        print(len(player_stats_df['Player']), f"in the {y} season added to dataframe")
        
        non_dup_stats = player_stats_df.drop_duplicates(subset = 'Player',
                                                        keep = 'first')
        
        # quick pause before scraping next year
        #print(f"pausing for {sleep_time} seconds")
        time.sleep(sleep_time)

        try:
            player_total_stats = player_total_stats.append(non_dup_stats)
            print(f"{y} total player stats data added to dataset")
            print("length of total dataframe:", len(player_total_stats['Player']))
            
        except:
            print(f"error with year {y}, data not collected")
            
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(sleep_time*.5)
            
    # export and return the dataframe
    if export == True:
        export_name = f"player_totals_{start_year}_to_{end_year}" + ".csv"
        player_total_stats.to_csv(export_name, index = False)
        
    return player_total_stats


# function to scrape a list of years for NBA PLayer per game stats
def scrape_player_per_game_stats(start_year = 2018, end_year = 2021,
                                 export = True, sleep_time = 2):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty final dataframe to append to in for loop
    player_per_game_stats = pd.DataFrame(columns = ['Player', 'Pos', 'Age', 'Tm', 'G',
                                           'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
                                           '3PA', '3P%', '2P', '2PA', '2P%',
                                           'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                                           'DRB', 'TRB', 'AST', 'STL', 'BLK',
                                           'TOV', 'PF', 'PTS', 'year'])
    
    # loop through each year in the list
    for y in years:
        
        # grab URLs for year y
        per_game_url = f'https://www.basketball-reference.com/leagues/NBA_{y}_per_game.html'
        
        # create bs4 object using requests and bs4
        per_game_response = requests.get(per_game_url)
        print(f"per game stats year {y} url response code:", per_game_response.status_code)
        html = per_game_response.text
        soup = BeautifulSoup(per_game_response.content, features = 'lxml')
        
        # grab table column names and rows
        column_names = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        table_rows = soup.findAll('tr')[0:]
        player_stats = [[td.getText() for td in table_rows[i].findAll('td')]
                                for i in range(len(table_rows))]
        
        # drop empty rows
        player_stats = [e for e in player_stats if len(e) > 10]
        
        # create dataframe for stats
        player_stats_df = pd.DataFrame(player_stats, columns = column_names[1:])
        # add year to dataframe
        player_stats_df["year"] = y
        print(len(player_stats_df['Player']), f"in the {y} season added to dataframe")
        
        non_dup_stats = player_stats_df.drop_duplicates(subset = 'Player',
                                                        keep = 'first')
        
        # quick pause before scraping next year
        #print(f"pausing for {sleep_time} seconds")
        time.sleep(sleep_time)

        try:
            player_per_game_stats = player_per_game_stats.append(non_dup_stats)
            print(f"{y} player per game stats data added to dataset")
            print("length of total dataframe:", len(player_per_game_stats['Player']))
            
        except:
            print(f"error with year {y}, data not collected")
            
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(sleep_time)
            
    # export and return the dataframe
    if export == True:
        export_name = f"player_per_game_{start_year}_to_{end_year}" + ".csv"
        player_per_game_stats.to_csv(export_name, index = False)
        
    return player_per_game_stats


# function to scrape a list of years for NBA PLayer total stats
def scrape_player_advanced_stats(start_year = 2019, end_year = 2021,
                                 export = True, sleep_time = 2):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty final dataframe to append to in for loop
    player_advanced_stats = pd.DataFrame(columns = ['Player', 'Pos', 'Age', 'Tm', 'G',
                                           'MP', 'PER', 'TS%', '3PAr', 'FTr',
                                           'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
                                           'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS',
                                           'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM',
                                           'VORP', 'year'])
    
    # loop through each year in the list
    for y in years:
        
        # grab URLs for year y
        advanced_url = f'https://www.basketball-reference.com/leagues/NBA_{y}_advanced.html'
        
        # create bs4 object using requests and bs4
        advanced_url = requests.get(advanced_url)
        print(f"per game stats year {y} url response code:", advanced_url.status_code)
        html = advanced_url.text
        soup = BeautifulSoup(advanced_url.content, features = 'lxml')
        
        # grab table column names and rows
        column_names = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        table_rows = soup.findAll('tr')[0:]
        player_stats = [[td.getText() for td in table_rows[i].findAll('td')]
                                for i in range(len(table_rows))]
        
        # drop empty rows
        player_stats = [e for e in player_stats if len(e) > 10]
        
        # create dataframe for stats
        player_stats_df = pd.DataFrame(player_stats, columns = column_names[1:])
        # drop empty columns
        player_stats_df = player_stats_df.drop(player_stats_df.columns[18],
                                               axis = 1)
        # add year to dataframe
        player_stats_df["year"] = y
        print(len(player_stats_df['Player']), f"in the {y} season added to dataframe")
        
        non_dup_stats = player_stats_df.drop_duplicates(subset = 'Player',
                                                        keep = 'first')
        
        # quick pause before scraping next year
        #print(f"pausing for {sleep_time} seconds")
        time.sleep(sleep_time)

        try:
            player_advanced_stats = player_advanced_stats.append(non_dup_stats,
                                                                 sort=False)
            print(f"{y} advanced player stats data added to dataset")
            print("length of total dataframe:", len(player_advanced_stats['Player']))
            
        except:
            print(f"error with year {y}, data not collected")
            
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(sleep_time)
            
    # export and return the dataframe
    if export == True:
        export_name = f"player_advanced_{start_year}_to_{end_year}" + ".csv"
        player_advanced_stats.to_csv(export_name, index = False)
        
    return player_advanced_stats


# function to scrape a list of years for NBA PLayer shooting stats
def scrape_player_shooting_stats(start_year = 2019, end_year = 2021,
                                 export = True, sleep_time = 2):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty final dataframe to append to in for loop
    player_shooting_stats = pd.DataFrame(columns = ['Player', 'Pos', 'Age', 'Tm',
                                                    'G', 'MP', 'FG%', 'Avg_Distance',
                                                    '3P_FGassisted%', '3-10_FG%',
                                                    '10-16_FG%', '16-3P_FG%', '3P_FG%',
                                                    'Dunk_attempt%', '3P_FGassisted%',
                                                    '3-10_FG%', '10-16_FG%', '16-3P_FG%',
                                                    '3P_FG%', 'Dunk_attempt%',
                                                    '3P_FGassisted%', 'Dunk_attempt%',
                                                    'Dunk_attempts', 'Heave_makes',
                                                    'Corener3_3P_attempt%', 'Corner3_FG%',
                                                    'Heave_attempts', 'Heave_makes',
                                                    'year'])
    
    # loop through each year in the list
    for y in years:
        
        # grab URLs for year y
        shooting_url = f'https://www.basketball-reference.com/leagues/NBA_{y}_shooting.html'
        
        # create bs4 object using requests and bs4
        shooting_url = requests.get(shooting_url)
        print(f"per game stats year {y} url response code:", shooting_url.status_code)
        html = shooting_url.text
        soup = BeautifulSoup(shooting_url.content, features = 'lxml')
        
        # grab table column names and rows
        column_names = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
        table_rows = soup.findAll('tr')[0:]
        player_stats = [[td.getText() for td in table_rows[i].findAll('td')]
                                for i in range(len(table_rows))]
        
        # drop empty rows
        player_stats = [e for e in player_stats if len(e) > 10]
        
        # create dataframe for stats
        player_stats_df = pd.DataFrame(player_stats, columns = column_names[1:])
        # drop empty columns
        player_stats_df = player_stats_df.drop(player_stats_df.columns[8],
                                               axis = 1)
        # rename columns
        column_mapping = {player_stats_df.columns[7]  : 'Avg_Distance',
                          player_stats_df.columns[8]  : '2P_attempt%',
                          player_stats_df.columns[9]  : '0-3_attempt%',
                          player_stats_df.columns[10] : '3-10_attempt%',
                          player_stats_df.columns[11] : '10-16_attempt%',
                          player_stats_df.columns[12] : '16-3P_attempt%',
                          player_stats_df.columns[13] : '3P_attempt%',
                          player_stats_df.columns[14] : '2P_FG%',                                                                                                                    9 : '0-3_attempt%',
                          player_stats_df.columns[15] : '3-10_FG%',
                          player_stats_df.columns[16] : '10-16_FG%',
                          player_stats_df.columns[17] : '16-3P_FG%',
                          player_stats_df.columns[18] : '3P_FG%',
                          player_stats_df.columns[19] : '2P_FGassisted%',
                          player_stats_df.columns[20] : '3P_FGassisted%',
                          player_stats_df.columns[21] : 'Dunk_attempt%',
                          player_stats_df.columns[22] : 'Dunk_attempts',
                          player_stats_df.columns[24] : 'Corener3_3P_attempt%',
                          player_stats_df.columns[25] : 'Corner3_FG%',
                          player_stats_df.columns[26] : 'Heave_attempts',
                          player_stats_df.columns[27] : 'Heave_makes'}
        player_stats_df = player_stats_df.rename(columns = column_mapping)
        # add year to dataframe
        player_stats_df["year"] = y
        print(len(player_stats_df['Player']), f"in the {y} season added to dataframe")
        
        non_dup_stats = player_stats_df.drop_duplicates(subset = 'Player',
                                                        keep = 'first')
        
        # quick pause before scraping next year
        #print(f"pausing for {sleep_time} seconds")
        time.sleep(sleep_time)

        try:
            player_shooting_stats = player_shooting_stats.append(non_dup_stats,
                                                                 sort=False)
            print(f"{y} player shooting stats data added to dataset")
            print("length of total dataframe:", len(player_shooting_stats['Player']))
            
        except:
            print(f"error with year {y}, data not collected")
            
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(sleep_time)
            
    # export and return the dataframe
    if export == True:
        export_name = f"player_shooting_{start_year}_to_{end_year}" + ".csv"
        player_shooting_stats.to_csv(export_name, index = False)
        
    return player_shooting_stats


# function to scrape All Stars by year
def scrape_all_stars(export = True):
        
    # grab wikipedia URL of all-stars
    url = 'https://en.wikipedia.org/wiki/List_of_NBA_All-Stars'
    
    # create bs4 object using requests and bs4
    response = requests.get(url)
    print(f"all-stars url response code:", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # grab full table
    nba_table = soup.findAll('table')[1]
    
    # turn table to dataframe
    all_stars_df = pd.read_html(str(nba_table))
    all_stars_df = pd.DataFrame(all_stars_df[0])
    
    # add hall of fame denomination to dataframe
    for idx, row in all_stars_df.iterrows():
        if '*' in row["Player"]:
            all_stars_df.loc[idx, "hall_of_fame"] = 1
            all_stars_df.loc[idx, "active_player"] = 0
            all_stars_df.loc[idx, "hof_eligible"] = 1
        elif '^' in row["Player"]:
            all_stars_df.loc[idx, "hall_of_fame"] = 0
            all_stars_df.loc[idx, "active_player"] = 1
            all_stars_df.loc[idx, "hof_eligible"] = 0
        elif '†' in row["Player"]:
            all_stars_df.loc[idx, "hall_of_fame"] = 0
            all_stars_df.loc[idx, "active_player"] = 0
            all_stars_df.loc[idx, "hof_eligible"] = 0
        else:
            all_stars_df.loc[idx, "hall_of_fame"] = 0
            all_stars_df.loc[idx, "active_player"] = 0
            all_stars_df.loc[idx, "hof_eligible"] = 1
    
    # remove extra characters from PLayer columns       
    for c in "*^†":     
        all_stars_df["Player"] = all_stars_df["Player"].str.replace(c, '')
        
    #for a in [r"[a]", r"[b]"]:
    #    #substring = f"[{a}]"
    #    all_stars_df["Player"] = all_stars_df["Player"].str.replace(a, '')
    
    # delete extra columns
    all_stars_df = all_stars_df.drop('Reference', 1)
    
    # rename columns
    # rename final_df columns
    all_stars_df = all_stars_df.rename(columns =
                                          {all_stars_df.columns[1]: "Selections",
                                          all_stars_df.columns[2]: "Years"})
    
    # export and return the dataframe
    if export == True:
        export_name = "nba_all_stars.csv"
        all_stars_df.to_csv(export_name, index = False)
        
    return all_stars_df


# function to scrape a list of years for NBA PLayer shooting stats
def scrape_player_contracts(start_year = 2015, end_year = 2016,
                                 export = True, sleep_time = 2):
    # turn inputs into a list of years
    if end_year > start_year:
        years = list(range(end_year, start_year-1,-1))
        
    elif end_year < start_year:
        years = list(range(end_year, start_year+1))
        
    else:
        years = [start_year]
    
    # create empty final dataframe to append to in for loop
    player_contracts = pd.DataFrame(columns = ['Player', 'Salary', 'Rank', 'Year'])
    
    # loop through each year in the list
    for y in years:
        
        # grab URLs for year y
        y1 = y+1
        contracts_url = f'https://hoopshype.com/salaries/players/{y}-{y1}/'
        
        # create bs4 object using requests and bs4
        response = requests.get(contracts_url)
        print(f"contracts year {y} url response code:", response.status_code)
        html = response.text
        soup = BeautifulSoup(html, features = 'html.parser')
        
        # grab table column names and rows
        salary_table = soup.find('table')
        length=len(salary_table.find_all("td"))
        players = [salary_table.find_all("td")[i].text.strip() for i in range(5,length,4)]
        salaries = [salary_table.find_all("td")[i].text.strip() for i in range(6,length,4)]
        
        # turn rows into dataframe
        salary_df = pd.DataFrame({"Player" : players,
                                  "Salary" : salaries,
                                  "Rank" : [i for i in range(1, len(salaries)+1)]})
        salary_df["Year"] = y

        # add year to dataframe
        print(len(salary_df['Player']), f"in the {y} season added to dataframe")
        
        # quick pause before scraping next year
        time.sleep(sleep_time)

        try:
            player_contracts = player_contracts.append(salary_df, sort=False)
            print(f"{y} player contracts added to dataset")
            print("length of total dataframe:", len(player_contracts['Player']))
            
        except:
            print(f"error with year {y}, data not collected")
            
        # sleep for short duration before moving onto next year
        print('='*5, f"end of year {y}", '='*5)
        time.sleep(sleep_time)
            
    # export and return the dataframe
    if export == True:
        export_name = f"player_contracts_{start_year}_to_{end_year}" + ".csv"
        player_contracts.to_csv(export_name, index = False)
        
    return player_contracts