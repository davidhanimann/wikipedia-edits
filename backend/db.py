import psycopg2


def get(title):
    conn = psycopg2.connect(
        "dbname=postgres user=davidhanimann password=postgres")
    cur = conn.cursor()

    sql = """select 
                title,
                extract(YEAR from to_date(substring(timestamp, 0, 10), 'YYYY-MM-DD')) as yr, 
                extract(MONTH from to_date(substring(timestamp, 0, 10), 'YYYY-MM-DD')) as mt, 
                count(*)
            from revision
            inner join wikipage on wikipage.id = wikipage_id
            where title = '{}'
            group by title, yr, mt
            order by title, yr, mt asc;""".format(title)
    cur.execute(sql)

    result = {
        'title': title,
        'values': []
    }
    for entry in cur:
        result['values'].append({
            'year': int(entry[1]),
            'month': int(entry[2]),
            'value': entry[3]
        })

    cur.close()
    return result
