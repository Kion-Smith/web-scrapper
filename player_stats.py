from prettytable import PrettyTable
class PlayerStats:
    def __init__(self,name,tag,acs,kills,deaths,assists,plus_minus,kd,adr,hs,kast,fk,fd,mk,econ) -> None:
        self.name = name
        self.tag = tag
        self.acs = acs
        self.kills =kills
        self.deaths =deaths
        self.assists =assists
        self.plus_minus =plus_minus
        self.kd = kd
        self.adr = adr
        self.hs = hs
        self.kast =kast
        self.fk = fk
        self.fd = fd
        self.mk = mk
        self.econ = econ

    def print_stats(self):
        table = PrettyTable()
        table.field_names = ["NAME","ACS","K","D","A","+/-","K/D", "ADR","HS%","KAST","FK","FD","MK","ECON"]
        table.add_row([self.name+self.tag,self.acs,self.kills,self.deaths,self.assists,self.plus_minus,self.kd,self.adr,self.hs,self.kast,self.fk,self.fd,self.mk,self.econ])
        print(table)