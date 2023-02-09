import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
from datetime import datetime,timedelta
import numpy as np

url = 'https://www.swimrankings.net/index.php?'

def build_athlete_url(athleteId: int, page='athleteDetail', athletePage=None)->str:
    """Builds the url for the athlete page"""
    params = {'page': page, 'athleteId': athleteId}
    if athletePage:
        params['athletePage'] = athletePage
    return url + urllib.parse.urlencode(params)

def parse_time(time_str):
    time_str = time_str.replace('M', '')
    try:
        time = datetime.strptime(time_str, "%M:%S.%f").time()
    except ValueError:
        time = datetime.strptime(time_str, "%S.%f").time()
    
        
    return timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)

def get_pb(athleteId:int, short_course=True)->pd.DataFrame:
    """Returns the PBs for an athlete"""
    url = build_athlete_url(athleteId)
    page = requests.get(url)

    dfs = pd.read_html(page.text)
    result = pd.concat(dfs)
    result.drop(columns=[0,1,2,'City (Nation)',	'Meet'],inplace=True)
    result.dropna(subset=['Time'],inplace=True)
    result['Date'] = pd.to_datetime(result['Date'], format='%d %b %Y')
    result['Date'] = result['Date'].dt.strftime('%d-%m-%Y')
    result['Time'] = result['Time'].apply(parse_time)
    result['Time'] = (result['Time'] / np.timedelta64(1, 's')).astype(float)

    result['Event'] = result['Event'].str.cat(result['Course'], sep=' ')
    result.drop(columns=['Course'],inplace=True)
    
    return result