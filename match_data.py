from prettytable import PrettyTable

from player_stats import PlayerStats
class GameData:
    def __init__(self,players_score,enemy_score,map,date_time,players_team_stats,enemy_team_stats) -> None:
        self.players_score =players_score
        self.enemy_score =enemy_score
        self.map = map
        self.date_time = date_time
        self.players_team_stats =players_team_stats
        self.enemy_team_stats =enemy_team_stats

    def find_player_stats(self,player_name:str) -> PlayerStats:
        for cur in self.players_team_stats:
            if cur.name.strip() == player_name:
                print("\t",player_name)
                return cur

        for cur in self.enemy_team_stats:
            if cur.name.strip() == player_name:
                print("\t",player_name)
                return cur
        
        return None

    def to_string(self):
        print("==================================================================")
        print(self.players_score,"-",self.enemy_score)
        print(self.map)
        print(self.date_time)

        table = PrettyTable()
        table.field_names = ["NAME","ACS","K","D","A","+/-","K/D", "ADR","HS%","KAST","FK","FD","MK","ECON"]
        for cur_player in self.players_team_stats:
            table.add_row([cur_player.name+cur_player.tag,cur_player.acs,cur_player.kills,cur_player.deaths,cur_player.assists,cur_player.plus_minus,cur_player.kd,cur_player.adr,cur_player.hs,cur_player.kast,cur_player.fk,cur_player.fd,cur_player.mk,cur_player.econ])
        table.add_row([""]*14)
        for cur_player in self.enemy_team_stats:
            table.add_row([cur_player.name+cur_player.tag,cur_player.acs,cur_player.kills,cur_player.deaths,cur_player.assists,cur_player.plus_minus,cur_player.kd,cur_player.adr,cur_player.hs,cur_player.kast,cur_player.fk,cur_player.fd,cur_player.mk,cur_player.econ])
        print(table)
        print("==================================================================")