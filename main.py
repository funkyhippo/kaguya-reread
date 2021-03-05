import requests
import time
import json

API_URL = "https://guya.moe/api/series/Kaguya-Wants-To-Be-Confessed-To/"
FILENAME = "kaguya.json"


def read_from_file(filename):
    with open(filename, "r") as f:
        return json.load(f)


def write_to_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)


def main():
    current_time = int(time.time())
    current_data = read_from_file(FILENAME)
    data = requests.get(API_URL)
    data = json.loads(data.text)
    slug = data["slug"]
    group_mapping = data["groups"]
    processed_volumes = [
        int(v["volume"] if "volume" in v else -1)
        for v in current_data["chapters"].values()
    ]
    next_volume = max(processed_volumes) + 1 if len(processed_volumes) else 1
    chapter_set = set(
        [
            k
            for k, v in data["chapters"].items()
            if "volume" in v and v["volume"] == str(next_volume)
        ]
    )
    for d in sorted(chapter_set, key=lambda a: float(a)):
        current_chapter_groups = data["chapters"][d]["groups"]
        current_chapter_folder = data["chapters"][d]["folder"]
        current_data["chapters"][d] = {
            "title": data["chapters"][d]["title"],
            "volume": data["chapters"][d]["volume"],
            "groups": {
                group_mapping[group]: list(
                    map(
                        lambda p: f"/media/manga/{slug}/chapters/{current_chapter_folder}/{group}/{p}",
                        pages,
                    )
                )
                for group, pages in current_chapter_groups.items()
            },
            "last_updated": current_time,
        }

    write_to_file(FILENAME, json.dumps(current_data, sort_keys=True))


if __name__ == "__main__":
    main()
