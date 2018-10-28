import requests, bs4, datetime, json, os
from pymongo import MongoClient


def get_latest_prices():
    res = requests.get('https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary/GB0032089863GBGBXSET1.html')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    table = soup.select('table')[0]
    price = (table.find_all('td')[1]).get_text()
    price = price.replace(',', '')
    price = price.split('.')[0]
    current_price = int(price)
    sharesave_price = 3825
    total_paid_in = 900000
    shares_bought_at_end = int(total_paid_in / sharesave_price)
    total_cashout = (current_price * shares_bought_at_end) / 100
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    latest_prices = {   "current_price": current_price, 
                        "total_cashout": total_cashout,
                        "update_time": update_time
                    }

    return json.dumps(latest_prices)

def post_to_db(post):
    mongo = os.environ['MONGO']
    client = MongoClient(mongo, 27017)
    db = client.sharescraper
    posts = db.posts

    result = posts.insert_one(json.loads(post))
    return result

def get_posts_from_db():
    mongo = os.environ['MONGO']
    client = MongoClient(mongo, 27017)
    db = client.sharescraper
    posts = db.posts

    cursor = posts.find().sort([("_id", -1)]).limit(28)

    results = []

    for document in cursor:
        document['_id'] = str(document['_id'])
        results.append(document)
    
    result = {"name": "history", "history": results}
    result = json.dumps(result)

    return result


def refresh_db():
    post_to_db(get_latest_prices())
    return 


if __name__ == "__main__":
    client = MongoClient()
    db = client.sharescraper
    posts = db.posts

    latest_prices = get_latest_prices()
    print(latest_prices)
    post_to_db(latest_prices)

    print(type(get_posts_from_db()))