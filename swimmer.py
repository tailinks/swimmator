from swim_ranking import get_pb
import pandas as pd
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class Swimmer:
    def __init__(self, date_of_birth: date, athlete_id:int, gender:str, name:str) -> None:
        self.date_of_birth = date_of_birth
        self.age = calculate_age(date_of_birth)
        self.id = athlete_id
        self.gender = gender
        self.pb = get_pb(athlete_id)
        self.name = name
        
    def get_regression_pb(self,)->pd.DataFrame:
        results = self.pb.pivot_table(values='Time', columns='Event', aggfunc='first')
        results.dropna(inplace=True)
        results.rename(index={'Time': self.name}, inplace=True)
        return results