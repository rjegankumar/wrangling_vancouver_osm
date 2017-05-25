def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017')
    db = client.osm
    return db

if __name__ == "__main__":
    db = get_db()
