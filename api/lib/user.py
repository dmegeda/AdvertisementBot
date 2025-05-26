from pymongo.database import Database


def get_next_user_id(db: Database) -> int:
    counter = db.counters.find_one_and_update(
        {"_id": "user_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )

    if not counter or "seq" not in counter:
        raise ValueError("Failed to get or increment user_id counter")

    return counter["seq"]
