# Author: Jeff Lucca
# Created 07/19/2018
# script.py

import requests
from datetime import datetime

def unixToStd(unixTime):
    stdTime = datetime.fromtimestamp(int(unixTime))
    return(stdTime.strftime('%Y-%m-%d'))

def main():
    matchTotal = 0
    repeatIDs = {}
    file = open('matchdata.tsv', 'w')
    file.write('match_id' + '\t' + 'match_seq_num' + '\t' + 'radiant_win' + '\t' +
            'start_time' + '\t' + 'duration' + '\t' + 'avg_mmr' + '\t' + 'num_mmr' + '\t' +
            'lobby_type' + '\t' + 'game_mode' + '\t' + 'avg_rank_tier' + '\t' + 'num_rank_tier' + 
            '\t' + 'cluster' + '\t' + 'radiant_team' + '\t' 'dire_team' + '\n')
    #while(matchTotal < 200):
    response = requests.get("https://api.opendota.com/api/publicMatches")
    matches = response.json()
    print(matches)
    print(response.status_code)
    for i in range(len(matches)):
        if((matches[i]['avg_mmr'] != None) & (matchTotal < 200)):
            if(int(matches[i]['avg_mmr']) > 3000):
                print(matchTotal)
                matchData = [str(matches[i]['match_id']), str(matches[i]['match_seq_num']),
                        str(matches[i]['radiant_win']), str(unixToStd(matches[i]['start_time'])),
                        str(matches[i]['duration']), str(matches[i]['avg_mmr']),
                        str(matches[i]['num_mmr']), str(matches[i]['lobby_type']),
                        str(matches[i]['game_mode']), str(matches[i]['avg_rank_tier']),
                        str(matches[i]['num_rank_tier']), str(matches[i]['cluster']),
                        str(matches[i]['radiant_team']), str(matches[i]['dire_team'])]
                for a in range(len(matchData)):
                    file.write(matchData[a]+'\t')
                # append match ID to repeatIDs
                file.write('\n')
                matchTotal += 1
    file.close()

if __name__ == '__main__':
    main()
