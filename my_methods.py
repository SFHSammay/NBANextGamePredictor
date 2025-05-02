import os
import pandas as pd
import nba_basics

def check_create_dir(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_df_to_dir(df: pd.DataFrame, file_name: str, directory: str) -> None:
    check_create_dir(directory)
    file_path = os.path.join(directory, file_name)
    df.to_csv(file_path, index=False)

def check_col_in_df(df, columns, message="Missing required columns {columns}."):
    col_missing = [col for col in columns if col not in df.columns]
    if col_missing:
        print(message.format(columns=col_missing))
        return False
    return True
    
def clean_raw_stats(games_raw: pd.DataFrame, team_name, team_column, flip_win=False):
    team_games = games_raw[games_raw[team_column] == team_name].copy()
    col_required = ['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'WL']
    check_col_in_df(team_games, col_required)
    team_games = team_games.sort_values(['GAME_DATE', 'GAME_ID']).reset_index(drop=True)    
    team_games['GAME_DATE'] = pd.to_datetime(team_games['GAME_DATE'])
    team_games['MIN'] = round(team_games['MIN'] / 5)
    team_games[nba_basics.col_traditional_percentage] = team_games[nba_basics.col_traditional_percentage] * 100
    team_games['DAYS_DIFF'] = team_games.groupby('SEASON_ID')['GAME_DATE'].diff().dt.days
    team_games['DAYS_DIFF'] = team_games['DAYS_DIFF'].fillna(0)
    team_games['BACK_TO_BACK'] = (team_games['DAYS_DIFF'] == 1).astype(int)
    team_games['GAMES_PLAYED'] = team_games.groupby('SEASON_ID').cumcount() + 1
    streaks = get_streaks(flip_win, team_games) 
    team_games['WIN_STREAK'], team_games['LOSS_STREAK'], team_games['LAST_10_WINS'], team_games['TOTAL_WINS'] = streaks
    col_no_wl = [col for col in nba_basics.col_traditional if col != 'WL']
    team_games = team_games[col_no_wl + ['DAYS_DIFF', 'BACK_TO_BACK', 'WIN_STREAK', 
                                         'LOSS_STREAK', 'LAST_10_WINS', 'TOTAL_WINS', 'GAMES_PLAYED'] + ['WL']]
    return team_games

def get_streaks(flip_win, team_games):
    last_season = None 
    win_streak = []
    loss_streak = []
    last_10_wins = []
    total_wins = []
    current_win_streak = 0
    current_loss_streak = 0
    win_history = []
    win_count = 0 
    
    for i, row in team_games.iterrows():
        if last_season is not None and row['SEASON_ID'] != last_season:
            current_win_streak = 0
            current_loss_streak = 0
            win_history = []
            win_count = 0  
        is_win = (row['WL'] == 'W') if not flip_win else (row['WL'] == 'L')
        if is_win:
            current_win_streak += 1 
            current_loss_streak = 0
            win_count += 1 
        else:  
            current_loss_streak += 1  
            current_win_streak = 0  
        win_streak.append(current_win_streak)
        loss_streak.append(current_loss_streak)
        total_wins.append(win_count)  
        win_history.append(is_win)
        if len(win_history) > 10:
            win_history.pop(0)
        last_10_wins.append(sum(win_history))
        last_season = row['SEASON_ID']
    return win_streak,loss_streak,last_10_wins,total_wins

def merge_csvs_dir(input_dir, sort_col, sort_col_2, sort_col_3):
    files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    all_data = []
    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        df = pd.read_csv(file_path)
        all_data.append(df)
    merged_df = pd.concat(all_data, ignore_index=True)
    merged_df = merged_df.sort_values([sort_col, sort_col_2, sort_col_3]).reset_index(drop=True)
    return merged_df

def merge_extend_csvs(df, df2, df_prefix, df_prefix2, drop_col=None, drop_prefix=None):
    if not check_col_in_df(df, columns=['SEASON_ID', 'GAME_ID', 'GAME_DATE', 'WL']):
        return
    extended_df = df.add_prefix(df_prefix).reset_index(drop=True)
    extended_df2 = df2.add_prefix(df_prefix2).reset_index(drop=True)
    extended_full = pd.concat([extended_df, extended_df2], axis=1).reset_index(drop=True)
    col_no_wl = [col for col in extended_full.columns if col != df_prefix + 'WL']
    extended_full = extended_full[col_no_wl + [df_prefix + 'WL']]
    extended_full_drop = drop_column(df_prefix2, drop_col, extended_full)
    extended_full_drop_prefix = drop_prefix_from_column(df_prefix, drop_prefix, extended_full_drop)
    return extended_full_drop_prefix

def merge_two_team_csvs(game_index, team_stats, df_prefix, df_prefix2, col_drop=None, prefix_drop=None):
    merged_games = []
    for row in game_index.itertuples(index=False):
        game_id = row.GAME_ID
        team1 = row.TEAM1
        team2 = row.TEAM2
        t1_stats = team_stats[(team_stats['GAME_ID'] == game_id) & (team_stats['TEAM1'] == team1)].add_prefix(df_prefix).reset_index(drop=True)
        t2_stats = team_stats[(team_stats['GAME_ID'] == game_id) & (team_stats['TEAM1'] == team2)].add_prefix(df_prefix2).reset_index(drop=True)
        merged_row = pd.concat([t1_stats, t2_stats], axis=1).reset_index(drop=True)
        merged_games.append(merged_row)
    merged_games_pd = pd.concat(merged_games, ignore_index=True)
    col_no_wl = [col for col in merged_games_pd.columns if col != df_prefix + 'WL']
    merged_games_pd = merged_games_pd[col_no_wl + [df_prefix + 'WL']]
    merged_games_drop = drop_column(df_prefix2, col_drop, merged_games_pd)
    merged_games_prefix = drop_prefix_from_column(df_prefix, prefix_drop, merged_games_drop)
    return merged_games_prefix

def drop_prefix_from_column(df_prefix, prefix_drop, df):
    df_to_drop_prefix = df.copy()
    if prefix_drop is not None:
        prefix_drop_prefix = [df_prefix + col for col in prefix_drop]
        col_no_prefix = {col: col.replace(df_prefix, "") for col in prefix_drop_prefix if col in df_to_drop_prefix.columns}
        df_to_drop_prefix.rename(columns=col_no_prefix, inplace=True)
    return df_to_drop_prefix

def drop_column(df_prefix2, col_drop, df):
    df_to_drop = df.copy()
    if col_drop is not None:
        col_drop_prefix = [df_prefix2 + col for col in col_drop]
        df_to_drop.drop(columns=col_drop_prefix, inplace=True)
    return df_to_drop

def convert_to_advanced(df_traditional):
    if not check_col_in_df(df_traditional, nba_basics.col_traditional_extended):
        return
    advanced_list = []
    
    poss = 0.5 * (
        (df_traditional['T_FGA'] + 0.4 * df_traditional['T_FTA'] - 1.07 * 
        (df_traditional['T_OREB'] / (df_traditional['T_OREB'] + df_traditional['O_DREB'])) * 
        (df_traditional['T_FGA'] - df_traditional['T_FGM']) + df_traditional['T_TOV']) +
        (df_traditional['O_FGA'] + 0.4 * df_traditional['O_FTA'] - 1.07 * 
        (df_traditional['O_OREB'] / (df_traditional['O_OREB'] + df_traditional['T_DREB'])) * 
        (df_traditional['O_FGA'] - df_traditional['O_FGM']) + df_traditional['O_TOV'])
    )

    pace = poss * 48 / df_traditional['MIN']
    off_rtg = df_traditional['T_PTS'] / poss * 100
    def_rtg = df_traditional['O_PTS'] / poss * 100
    net_rtg = off_rtg - def_rtg

    ast_pct = df_traditional['T_AST'] / df_traditional['T_FGM'] * 100
    ast_to = df_traditional['T_AST'] / df_traditional['T_TOV']
    ast_ratio = df_traditional['T_AST'] / (df_traditional['T_FGA'] + df_traditional['T_FTA'] * 0.44 + 
                                           df_traditional['T_TOV'] + df_traditional['T_AST']) * 100
    oreb_pct = df_traditional['T_OREB'] / (df_traditional['T_OREB'] + df_traditional['O_DREB']) * 100
    dreb_pct = df_traditional['T_DREB'] / (df_traditional['T_DREB'] + df_traditional['O_OREB']) * 100
    reb_pct = df_traditional['T_REB'] / (df_traditional['T_REB'] + df_traditional['O_REB']) * 100
    to_pct = df_traditional['T_TOV'] / (df_traditional['T_FGA'] + df_traditional['T_FTA'] * 0.44 + df_traditional['T_TOV']) * 100
    
    df_merger = pd.DataFrame({
        'SEASON_ID': df_traditional['SEASON_ID'], 'GAME_ID': df_traditional['GAME_ID'], 
        'GAME_DATE': df_traditional['GAME_DATE'], 'MIN': df_traditional['MIN'],
        'TEAM1': df_traditional['TEAM1'], 'TEAM2': df_traditional['TEAM2'], 'HOME': df_traditional['HOME'],
        'OFFRTG': off_rtg, 'DEFRTG': def_rtg, 'NETRTG': net_rtg,
        'AST_PCT': ast_pct, 'AST_TO': ast_to, 'AST_RATIO': ast_ratio,
        'OREB_PCT': oreb_pct, 'DREB_PCT': dreb_pct, 'REB_PCT': reb_pct,
        'TO_PCT': to_pct,
        'PACE': pace,
        'DAYS_DIFF': df_traditional['T_DAYS_DIFF'], 'BACK_TO_BACK': df_traditional['T_BACK_TO_BACK'],
        'WIN_STREAK': df_traditional['T_WIN_STREAK'], 'LOSS_STREAK': df_traditional['T_LOSS_STREAK'], 
        'LAST_10_WINS': df_traditional['T_LAST_10_WINS'], 'TOTAL_WINS': df_traditional['T_TOTAL_WINS'],
        'GAMES_PLAYED': df_traditional['T_GAMES_PLAYED'],
        'WL': df_traditional['WL']
    })

    advanced_list.append(df_merger)
    df_advanced = pd.concat(advanced_list, ignore_index=True)
    df_advanced = df_advanced.round(1)
    return df_advanced

def compute_moving_average(df, col_numeric, n):
    avg_data = df.copy()
    avg_data[col_numeric] = avg_data[col_numeric].astype(float)
    
    for i in range(len(df)):
        if i == 0:
            avg_data.loc[i, col_numeric] = df.loc[i, col_numeric]
        else:
            start_idx = max(0, i - n)
            avg_data.loc[i, col_numeric] = df.loc[start_idx:i-1, col_numeric].mean()
    
    avg_data[col_numeric] = avg_data[col_numeric].round(1)
    return avg_data

def compute_moving_streak(df, col_streak):
    streak_data = df.copy()
    streak_data[col_streak] = streak_data[col_streak].astype(int)
    
    for i in range(len(df)):
        if i == 0:
            streak_data.loc[i, col_streak] = df.loc[i, col_streak]
        else:
            streak_data.loc[i, col_streak] = df.loc[i-1, col_streak]
    return streak_data

def assign_tier(rank):
    if rank <= 6:
        return 1
    elif rank <= 12:
        return 2
    elif rank <= 16:
        return 3
    elif rank <= 24:
        return 4
    else:
        return 5