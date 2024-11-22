def format_players(player_data, team_id):
    insert_str = 'insert into players (bball_ref, player_pos, name_first, name_last, jersey_num, height_feet, height_inches, year, team_id) values'
    for player in player_data:
        insert_str += (f'("{player[0]}", '
                       f'"{player[1]}", '
                       f'"{player[2]}", '
                       f'"{player[3]}", '
                       f'{player[4] if str(player[4]) != "nan" else 0}, '
                       f'{player[5]}, '
                       f'{player[6]}, '
                       f'"{player[7]}", '
                       f'{team_id}), ')
    return insert_str[:-2]