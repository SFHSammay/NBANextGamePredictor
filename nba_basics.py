seasons = ['2021-22', '2022-23', '2023-24']
teams = [
    'BOS', 'BKN', 'NYK', 'PHI', 'TOR',
    'CHI', 'CLE', 'DET', 'IND', 'MIL',
    'ATL', 'CHA', 'MIA', 'ORL', 'WAS',
    'DEN', 'MIN', 'OKC', 'POR', 'UTA',
    'GSW', 'LAC', 'LAL', 'PHX', 'SAC',
    'DAL', 'HOU', 'MEM', 'NOP', 'SAS'
]
col_traditional = [  
    'SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'HOME',
    'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
    'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB',
    'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS', 'WL'  
]

col_traditional_numeric = [
        'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 
        'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 
        'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS' 
    ]

col_traditional_days_off = ['DAYS_DIFF', 'BACK_TO_BACK']

col_traditional_streak = ['WIN_STREAK', 'LOSS_STREAK', 'LAST_10_WINS', 'TOTAL_WINS']

col_traditional_percentage = ['FG_PCT', 'FG3_PCT', 'FT_PCT']

col_traditional_drop = [
    'SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 
    'TEAM1', 'TEAM2', 'HOME', 'WL', 'DAYS_DIFF',
    'BACK_TO_BACK', 'WIN_STREAK', 'LOSS_STREAK', 
    'LAST_10_WINS', 'TOTAL_WINS', 'GAMES_PLAYED'
]

col_traditional_drop_prefix = ['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'HOME', 'WL']

col_traditional_extended = [
    'SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'HOME',
    'T_PTS', 'T_FGM', 'T_FGA', 'T_FG_PCT', 'T_FG3M', 'T_FG3A', 'T_FG3_PCT',
    'T_FTM', 'T_FTA', 'T_FT_PCT', 'T_OREB', 'T_DREB', 'T_REB', 'T_AST',
    'T_STL', 'T_BLK', 'T_TOV', 'T_PF', 'T_PLUS_MINUS', 'T_DAYS_DIFF',
    'T_BACK_TO_BACK', 'T_WIN_STREAK', 'T_LOSS_STREAK', 'T_LAST_10_WINS',
    'T_TOTAL_WINS', 'O_PTS', 'O_FGM', 'O_FGA', 'O_FG_PCT', 'O_FG3M', 'O_FG3A',
    'O_FG3_PCT', 'O_FTM', 'O_FTA', 'O_FT_PCT', 'O_OREB', 'O_DREB', 'O_REB',
    'O_AST', 'O_STL', 'O_BLK', 'O_TOV', 'O_PF', 'O_PLUS_MINUS', 'WL'
]

col_traditional_diff = [
        'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 
        'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 
        'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS'
    ]

col_traditional_additional = ['BACK_TO_BACK', 'WIN_STREAK', 'LOSS_STREAK', 'LAST_10_WINS', 'TOTAL_WINS', 'GAMES_PLAYED']

col_basic_drop = ['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'HOME', 'WL']

col_advanced = [
    'OFFRTG', 'DEFRTG', 'NETRTG', 
    'AST_PCT', 'AST_TO', 'AST_RATIO', #stats adjusted for team-based stat
    'OREB_PCT', 'DREB_PCT', 'REB_PCT',  # stats adjusted for team-based stat
    'TO_PCT', # stat adjusted for team-based stat 
    'POSS', 'PACE'
]

col_advanced_clean = [
    'OFFRTG', 'DEFRTG', 'NETRTG', 
    'AST_PCT', 'AST_TO', 'AST_RATIO', #stats adjusted for team-based stat
    'OREB_PCT', 'DREB_PCT', 'REB_PCT',  # stats adjusted for team-based stat
    'TO_PCT', # stat adjusted for team-based stat 
    'PACE'
]

col_advanced_drop = ['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'HOME', 'WL']

col_advanced_drop_prefix = ['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'MIN', 'TEAM1', 'TEAM2', 'WL']

