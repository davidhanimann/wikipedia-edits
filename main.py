import requests
import psycopg2

title = 'Bitcoin'


def query(title, cont):
    continues = '&rvcontinue={}'.format(cont) if len(cont) > 0 else ''
    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={}&rvlimit=500&rvprop=timestamp|user|comment&rvdir=older{}".format(
        title, continues)

    payload = {}
    headers = {
        'Cookie': 'WMF-Last-Access=19-Jan-2021; WMF-Last-Access-Global=19-Jan-2021; GeoIP=CH:ZH:Zurich:47.36:8.54:v4'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


conn = psycopg2.connect("dbname=postgres user=davidhanimann password=postgres")
cur = conn.cursor()

cur.execute(
    '''INSERT INTO wikipage("title") values('{}') RETURNING "id", "title"'''.format(title))

wikipage = cur.fetchone()
wikipage_id = wikipage[0]

continues = ''

while True:
    print(continues)
    data = query(title, continues)
    # print(data['query'])
    pages = list(data['query']['pages'].keys())
    revisions = data['query']['pages'][pages[0]]['revisions']
    # print(revisions)

    for revision in revisions:
        timestamp = revision['timestamp'].replace("'", "")
        user = revision['user'].replace("'", "") if 'user' in revision else ''
        comment = revision['comment'].replace(
            "'", "") if 'comment' in revision else ''

        sql = '''INSERT INTO revision("wikipage_id", "timestamp", "user", "comment") values ('{}', '{}', '{}', '{}')'''.format(
            wikipage_id, timestamp, user, comment)
        cur.execute(sql)

    if 'continue' in data:
        continues = data['continue']['rvcontinue']
    else:
        conn.commit()
        cur.close()
        conn.close()
        break
