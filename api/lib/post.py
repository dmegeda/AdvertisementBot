from pymongo.database import Database


def get_next_post_id(db: Database) -> int:
    counter = db.counters.find_one_and_update(
        {"_id": "post_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )

    if not counter or "seq" not in counter:
        raise ValueError("Failed to get or increment post_id counter")

    return counter["seq"]
