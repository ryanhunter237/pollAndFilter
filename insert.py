import random
import string
import time

import requests

GROUP_IDS = ["".join(random.choices(string.hexdigits, k=32)) for _ in range(3)]
EXTENSIONS = [".pdf", ".txt", ".png"]
MD5s = ["".join(random.choices(string.hexdigits, k=32)) for _ in range(12)]
TAGS = ["SMALL", "MEDIUM", "LARGE", "OLD", "NEW"]
NUM_FILES = 16


def insert_file(group_id, filename, md5):
    data = {"group_id": group_id, "filename": filename, "md5": md5}
    requests.put("http://localhost:5000/api/files", json=data)


def insert_tag(md5, sequence, tag):
    data = {"md5": md5, "sequence": sequence, "tag": tag}
    r = requests.put("http://localhost:5000/api/tags", json=data)


def insert_data():
    sequence = 1
    for _ in range(NUM_FILES):
        group_id = random.choice(GROUP_IDS)
        base = "".join(random.choices(string.ascii_letters, k=12))
        extension = random.choice(EXTENSIONS)
        filename = base + extension
        md5 = random.choice(MD5s)
        insert_file(group_id, filename, md5)
        for tag in random.choices(TAGS, k=2):
            time.sleep(0.2)
            insert_tag(md5, sequence, tag)
            sequence += 1
        time.sleep(1)


if __name__ == "__main__":
    insert_data()
