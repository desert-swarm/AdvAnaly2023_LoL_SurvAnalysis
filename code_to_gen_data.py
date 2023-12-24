# getting player data:
# originally done in Jupyter NB

import requests 
import json
import pandas as pd
import numpy as np
import time as tm

api_key = ""
startTime = '1641038400'# jan 1, 2022
endTime = '1641790800' # jan 1, 2023

def to_datetime(ts):
    import datetime
    
    timestamp = ts / 1000
    date = datetime.datetime.utcfromtimestamp(timestamp)
    return date


def get_puuid(sum_name):
    resp1 = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{sum_name}?api_key={api_key}")
    
    return resp1.json()['puuid']

def get_matches3(puuid, startTime, endTime):
    import time
    match_info = []
    match_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{str(puuid)}/ids?startTime={startTime}&endTime={endTime}&start=0&count=100&api_key={api_key}&sort=asc"
    
    # Retry up to 3 times with exponential backoff
    for retry in range(3):
        matches = requests.get(match_url)
        
        if matches.status_code == 200:
            print("found", len(matches.json()), "matches")
            for mid in matches.json():
                info_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{mid}?api_key={api_key}"

                resp_info = requests.get(info_url)
                if resp_info.status_code == 200:
                    match_info.append({
                        'matchID': mid,
                        'gameStart': to_datetime(resp_info.json()['info']['gameStartTimestamp']), 
                        'gameEnd': to_datetime(resp_info.json()['info']['gameEndTimestamp']), 
                        'participants_puuid': resp_info.json()['metadata']['participants']
                    })
                else: 
                    return "FAILED TO GET MATCH INFO"
                
                # Introduce a delay of 1 second between API calls
                time.sleep(1)
            
            return match_info
        elif matches.status_code == 429:
            # Retry with exponential backoff
            wait_time = 2**retry
            print(f"Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return f"Failed to get match IDs. Status Code: {matches.status_code}"
    
    return "Max retries reached. Unable to fetch data."
    
    
player_puuid_1 = [
    "pmNjMN4uWCAoqTof_CRrHmDL5OrudKgxgh6mQcQTSIyYaPbJDmeOAAwUaQMoa6O98Q7XgSwXDdF-1Q",
            "kKzedb-ZBGnCQImezs4F6BEHNdg8IhjV88t0KhAJU4bjZeK28lg8MGhKrr644w72A1Kp76CIgBDfDw",
            "fB4mOyTTe94ZnrIC2BLn_DAa57TpcKwRePyrhcLAy7_I-LrqbkxRYSeod0jqc5W53rOht-d3vXckmg",
            "0E5VaDtD25aKvApaibvuZPtQe__MqgUe92LAChMC-OufQeUzXWLZ_2rP_2VMo9NnCrJkkAipbTnraQ",
            "eLK_XFIhij0PQLJmeLp47ohiA2r6WBJGB6AgKnHLwHMIxOPcofD8bM_b7iZnLol6G7L3tntNsNMyJQ",
            "dttb1FkUnwlvtC1ceQNtwWDIZovqbhGa5KdUbm-yIsxtzKhwZxLmFagVc7fdUoOcxwTVNLj21iPBGA",
            "68J2Wr4oOhUUWLYvuuIo8P1MJIA2_RqFq4lPZVpuLLMKy2coSJcNiJ_P0OEPv32V59K-ccuBFmK6Bg",
            "XMA9RwjGNP7GdAYOmXhX2nHoyhTxN2rfbofoLHpQdnHQilEoiXFC-11ctd8ieeN-oGG9amPUjcV0mQ",
            "584tuqnMZ6HRfYBq7fwrl4FTuc-kvtt689bsgbYiu0SW52B-CefVisIraZcqMQu8niy2fNhkjTcnSw",
            "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng"
]

player_puuid_2 = [
    "e_TPCmVFwCi9ODYR1YznVn8xyEQZybsz1wLWRqRyrjBL9Ueq7dc6TX_D721Ax0P7ZFk1BOGCk_lIcw",
            "6zlpDigOxtcqxTTuRb-8fWa0IUIYYLXCDDFjVcNlD2OPYE8QPYVeBso7yb8lAEH_VnfIlTP9JvKKpQ",
            "584tuqnMZ6HRfYBq7fwrl4FTuc-kvtt689bsgbYiu0SW52B-CefVisIraZcqMQu8niy2fNhkjTcnSw",
            "lv1OuOsaQFj6m1hEMwHi88VndFsfcSgix1NQV_hL4qAibfaEi_sPt2YUfcKAa9rQpuMCB8Agsr1ecQ",
            "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng",
            "b1K4xXY-kWeEu9DWm4YZjCLEl0VUfkc8us_yn3dEzSQPITs5HJFMtZ8MLwpK_UE0k-oaEIp1x5rUuw",
            "LFrR6XfT6LIRJMjT2ZjNe8sQOwQ2NaktPK9iSR3iQciMxH0QCDco4Svox_UB6RJ4Cdpodpt5U3Td3Q",
            "HOc5Nsf6k8KxCPb--tLgqCWqJfPBPvWB6sM0XudcA6jjEjYazj3czoxGQpKJ9pB_W2PyjQiPMIZqfQ",
            "bFB3RgpIm6Q4DGYX-bcYhJB_Kc7sAOPJMpvV-5Cki9BITVIhYL-SrQiRRNhkpp7UsJ3Nw8WPEoYdWQ",
            "w7ztYQcs5bkm0q97dkQH092ERtdz28BKJCLfxxg956DUUzEtfEy4BtGRJ3zK8mCH5QrYPPjeDZgOtA"
]

player_puuid_3 = ["xhh_--INaingUVUCcZZKwksZXqK4TmVqk8EQsvRwdoPHak7NrSPUGwFVmZzR18M7QacEW8kBcIk2yQ",
            "am5zs3HcmpMrsmQRgnr1nqS6LX7aGNI7T-2mGkS0Qbp2QfzHCVBLNlFVdvPZ2XVmyxlRKeJV2p_vww",
            "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng",
            "gLTg6u75CXiZXDL-vw1HoBWJLA5QdAG57yMb-XtyLmGNU0ZFtkqlPJ3FnZQ2_jZ5SKeDWo7TNMZClQ",
            "aBajVJnqEMcWf35guJ35fo7UWqdI-OFjytRTnsxu528q0JQs6ecA6P8oqjUyHm8ADOLwhwjq16Roag",
            "pQGfaMCEBDYSn6AtBzd-ZPM96jPU4E4F6d5qs_FrPTdgxC-PVNBWvnRnzztAummwC6X1YG1L1wihHg",
            "OdYWj3dFDlc4kRS2fWHyl43R9QyEZ6KCvCPJVZpUSh9gzDkZ-Pjr130O-9zfF0ZcW6SMDbpExYnYWA",
            "PVuv6Ik25ioWi8VuFI850fVrH2WbMWcZ8-I-OXhl-YQLoYtlHW-b7MVFxD8r7OH1TmEnON5shJ6SXw",
            "e5KKi15Gy4sbG0BPI3v6rqI2cIt0aAvTaY3BTJYtVjA26fuir6TvTn3nqfIfCb-Q8lTHu3t6p0bV6Q",
            "_BbEjnQ-2gImhkkWA3tMDRwXlJ66ZnTKdTkyRZJu3YwAB9sEv9QnP_6JlB6dc7dBxgJsTYgmT6HEZA",
            "X8KiFuGmkR0MEb34B2ntn1shdo3zXTprXemXRA4gRneQcOK56OFFju0k42JxKTJLsD1-9UpoYpdRDw",
            "vIN_qwe3I2j6smsmyMXw6F5JHdX-_54wAA-3G1OQeaWpalS-sKVw7OzlB4D0qe5EdXaEAS_ylsd_Vw",
            "MLzfjYwlAvyrbKJQoFmstpAu0bmHyNT-gEOefmWuSBg69dZOg6LiP-pdfciZtGgcojg_1AQJWPT-aQ",
            "ownWhFdJ2MAngTHv6Z3QH_EFGnbR-XrtTxF-xieOF7Ou3xbUQKsPxKQMVsf8Wh7FwnH9fYLeUqtzNQ",
            "D7xAw3D78vdRh9leUTV8gNCkymEUnapc3P6LaeM2MyiCDd0kCviKOZcKIlNdhXyrGOkHd5-w0ZyVfg",
            "xhh_--INaingUVUCcZZKwksZXqK4TmVqk8EQsvRwdoPHak7NrSPUGwFVmZzR18M7QacEW8kBcIk2yQ",
            "gLTg6u75CXiZXDL-vw1HoBWJLA5QdAG57yMb-XtyLmGNU0ZFtkqlPJ3FnZQ2_jZ5SKeDWo7TNMZClQ",
            "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng",
            "vIBye2aw2VqOG0S7YNpYZWaeJHxwQAdF4KqHl2fTt378fZt1cp1sh-n4wSNSxbZ1HkDUMDG1cG28PA",
            "aBajVJnqEMcWf35guJ35fo7UWqdI-OFjytRTnsxu528q0JQs6ecA6P8oqjUyHm8ADOLwhwjq16Roag",
            "lKyzj6_Z-sfvlT3pZUVoHxFsez0-gnYAG5Bd8U1_JjUEyengCXnU8uKd8LVE6dOQ6R70WmQ2D1LQ1A",
            "zc37OTeDDHhdI-RXHEEm-AekClFfjy5M783lXopgK9MgYlP1ClHXzUaSOqHJm-R9QJNgIOLRGWr_iQ",
            "Y-cLjlyAtesg3_nmYN0DReh73YvWHGZUHQa_Cf1T1xr0Fh2cvvkjddpSaZdMg5uV5p2sVYuFZRmsFA",
            "4cQT2jI6Fc18dIqWwpN5D1EV5oAhTk_VvkYkDt3Zs5v080L_cOdv9ifBCJGOiERenbSu8uSjDJIIEQ",
            "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng",
            "3SCss5USdjOgqNoRuPe9CZUaZF3KbzwXdgjTJmrGd0pVhpJVd_01830GoSV98yPBpDythOtyn0wtyQ",
            "dMEZItym5wp2NtqcmlwPJP50dDR3BhGRhfiVjYN8Mz1mNJcvSvUqYzdp_r4JhSNU_4_LVDeaPgkcxA",
            "eOr5LA1B1rvel2dSs3lZlufpYoj3DDfcV1dV_dnZPj1i5mSEhFeDQcBKjMEiIyFFY6PIA_FgzMxRnQ",
            "DG7H-gk4AxbLtP2CQRl8suUjDJoDFOi-spaWLVAIUE7PhkVRLNqsuH8DEBInxDVgD8XS7pz977ZUKw",
            "U1u06p7wHn2mEpOcVimhELjIWO72kq1BnnWdf_4bJj1FLp8Q7cZI07C15yvL-K0-DpT4bbpzh-1Jbw",
             "QUqq9ZybSfqRGJu_g7GNkTUWV5AQxUfHuyBOjADz8yTvLAmN9cdRuBGW7LxW_U9yrqvqqSh0sZPJng",
            "gLTg6u75CXiZXDL-vw1HoBWJLA5QdAG57yMb-XtyLmGNU0ZFtkqlPJ3FnZQ2_jZ5SKeDWo7TNMZClQ",
            "Wh0faEQk3f-7EWTZPtZjRZWOC9xlu4WmS2LMKzglzfRDK80napy-akEDIvPzdKv6cFilp_YvuzWdAg",
            "xOBjsbfz2Vtr9jNsYxM0O9Vj8rD8Eztj_vYFu1wsZNToUM2q5yl7ERdTPXZugmweX3McMbXtmtZ2Dw",
            "584tuqnMZ6HRfYBq7fwrl4FTuc-kvtt689bsgbYiu0SW52B-CefVisIraZcqMQu8niy2fNhkjTcnSw",
            "3tM8Movt8jemPrWuO1aDsjVUBNO4k6EK1S1_xvAnnsZZmL0gz3YK-jPq2ptwq5G79np5FxkoyUvn0Q",
            "98jBqtlXic9wW2qa199qF5w_rt2SrXZxCK9dgbDBREe5m8iTaIkBbekOF4_RBTKLGEYRzXs_y1lt1w",
            "aIuDy1_NX_XhHDs1_cyziCZYoFfg32EWFNPc3LnBO6bK6sA06gxuq3c6M4wRPdmZ8zCKbZ0VFCGrfw",
            "QA9S3zNvRwVQ6_wgMi5leq-aHL5VSiw7b_Hb3Wya0EH7QT75i7XK3OBP3rLvqKqRJK3_6m2xAdQjxw",
            "mQdeHgemxyUuf70JclJltwnucEP8LUtmRCPzlOVLqrcUuhZXL6w7TvR70qlHAgh2TNfRqtiU_Q1FUQ"
            
]

player_list = new_list = player_puuid_1 + player_puuid_2 + player_puuid_3




# Start with the provided epoch timestamp for January 1, 2023
start_time = 1672574400

# Calculate the epoch timestamp for the end of December 2022
end_time = int(time.mktime(time.strptime("2022-12-31", "%Y-%m-%d")))

# Create a list of pairs of consecutive epoch timestamps incremented by 10 days until the end of December 2022
timestamp_pairs = [(timestamps[i], timestamps[i+1]) for i in range(0, len(timestamps)-1, 2)]

# Print the resulting list of pairs
print(timestamp_pairs)

for tm in timestamp_pairs:
    print(tm)
    startTime = tm[0]
    endTime = tm[1]
    for summoner in player_list:
 
        mat_by_puuid.append({summoner: get_matches3(summoner, startTime, endTime)})
        print('********added')
        time.sleep(1)