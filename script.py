import requests
from datetime import datetime

def unixToStandard(unixTime):
    standardTime = datetime.fromtimestamp(int(unixTime))
    return(standardTime.strftime('%Y-%m-%d'))

def main():
    response = requests.get("https://api.opendota.com/api/publicMatches")
    matches = response.json()
    print(data)
    print(response.status_code)
    dataIndex = 0
    for i in range(len(matches)):
        if(matches[i]['avg_mmr'] != None):
            if(int(matches[i]['avg_mmr']) > 3000):
                print(dataIndex)
                print(unixToStandard(data[i]['start_time']))
                dataIndex += 1

if __name__ == '__main__':
    main()
