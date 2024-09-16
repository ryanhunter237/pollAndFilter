import random
import string
import time

import requests

NUM_GROUP_IDS = 3
FILES_PER_GROUP_ID = 4
EXTENSIONS = [".pdf", ".txt", ".png"]
TAGS = ["SMALL", "MEDIUM", "LARGE", "OLD", "NEW"]


def insert_file(group_id, filename, md5):
    data = {"group_id": group_id, "filename": filename, "md5": md5}
    requests.put("http://localhost:5000/api/files", json=data)


def insert_tag(md5, sequence, tag):
    data = {"md5": md5, "sequence": sequence, "tag": tag}
    r = requests.put("http://localhost:5000/api/tags", json=data)


def insert_data():
    for _ in range(NUM_GROUP_IDS):
        group_id = "".join(random.choices(string.hexdigits, k=32))
        for _ in range(FILES_PER_GROUP_ID):
            base = "".join(random.choices(string.ascii_letters, k=12))
            extension = random.choice(EXTENSIONS)
            filename = base + extension
            md5 = "".join(random.choices(string.hexdigits, k=32))
            insert_file(group_id, filename, md5)
            for i, tag in enumerate(random.choices(TAGS, k=2), start=1):
                insert_tag(md5, i, tag)
                time.sleep(0.2)
            time.sleep(1)
        time.sleep(2)


if __name__ == "__main__":
    insert_data()
