# Author: Jeff Lucca
# Created 07/20/2018
# script.py

# Collects information of 200 matches from the OpenDota Public Matches API and writes it into a tsv.
# Only records matches with an average MMR greater than 3000.

import requests
import time
from datetime import datetime

# Converts Unix timestamp to standard (YYYY-MM-DD).
def unixToStd(unixTime):
    stdTime = datetime.fromtimestamp(int(unixTime))
    return(stdTime.strftime('%Y-%m-%d'))

def main():
    matchTotal = 0 # Tracks the total number of matches so it can stop collecting after 200.
    repeatIDs = set() # Gets rid of repeat match IDs by checking if it exists in set before collecting.
    file = open('matchdata.tsv', 'w')
    file.write('match_id' + '\t' + 'match_seq_num' + '\t' + 'radiant_win' + '\t' +
            'start_time' + '\t' + 'duration' + '\t' + 'avg_mmr' + '\t' + 'num_mmr' + '\t' +
            'lobby_type' + '\t' + 'game_mode' + '\t' + 'avg_rank_tier' + '\t' + 'num_rank_tier' + 
            '\t' + 'cluster' + '\t' + 'radiant_team' + '\t' 'dire_team' + '\n')
    # The API only sends 100 matches back, some of which may not be usable.
    # To get enough matches, the API is called again, repeating until all 200 are collected.
    while(matchTotal < 200):
        response = requests.get("https://api.opendota.com/api/publicMatches")
        matches = response.json()
        for i in range(len(matches)):
            # If the match has no MMR, it isn't above 3000, so it fails.
            if(matches[i]['avg_mmr'] != None):
                # For a match to meet the criteria, it must be above 3000 MMR,
                # and there can't be over 200 total matches collected already.
                # In addition, it must not be a duplicate match (it can't exist in repeatIDs).
                if(int(matches[i]['avg_mmr']) > 3000 and matchTotal < 200 and
                        not matches[i]['match_id'] in repeatIDs):
                    # Stores all of the needed match data in correct order to prepare for writing to
                    # the tsv.
                    # start_time is passed through to unixToStd to convert it to standard time.
                    matchData = [str(matches[i]['match_id']), str(matches[i]['match_seq_num']),
                            str(matches[i]['radiant_win']), str(unixToStd(matches[i]['start_time'])),
                            str(matches[i]['duration']), str(matches[i]['avg_mmr']),
                            str(matches[i]['num_mmr']), str(matches[i]['lobby_type']),
                            str(matches[i]['game_mode']), str(matches[i]['avg_rank_tier']),
                            str(matches[i]['num_rank_tier']), str(matches[i]['cluster']),
                            str(matches[i]['radiant_team']), str(matches[i]['dire_team'])]
                    for a in range(len(matchData)):
                        file.write(matchData[a]+'\t')
                    file.write('\n') 
                    matchTotal += 1 # Increments by 1 to reflect new total number of matches.
                    repeatIDs.add(matches[i]['match_id']) # Records match as already collected.
                    print(str(matchTotal) + ' match(es) found')
        # In order to not spam the API, waits 20 seconds before calling again so it can update with
        # new matches.
        if(matchTotal < 200):
            time.sleep(20)
    file.close()

if __name__ == '__main__':
    main()
