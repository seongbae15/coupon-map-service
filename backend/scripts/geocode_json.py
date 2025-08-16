import os
import json
from pathlib import Path
import requests
from dotenv import load_dotenv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
load_dotenv(".env")

from locations.models import Location

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
GEOCODE_URL = os.getenv("GEOCODE_URL")

HEADERS = {
    "x-ncp-apigw-api-key-id": NAVER_CLIENT_ID,
    "x-ncp-apigw-api-key": NAVER_CLIENT_SECRET,
}


def geocode(address):
    try:
        response = requests.get(
            GEOCODE_URL,
            headers=HEADERS,
            params={"query": address},
            timeout=10,
        )
        result = response.json()
        if result.get("addresses"):
            addr = result["addresses"][0]
            return float(addr["y"]), float(addr["x"])

    except Exception as e:
        print(f"[Geocode Error] {address} - {e}")
    return None, None


def load_data_from_json():
    data_dir = Path(__file__).parent.parent.parent / "market-crawling"
    json_files = data_dir.glob("*.json")

    for json_file in sorted(json_files):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                store_list = json.load(f)
                for store in store_list:
                    name = store.get("가맹점")
                    address = store.get("주소")
                    market_type = store.get("업종")
                    lat, lng = geocode(address)
                    if lat is None and lng is None:
                        print(f"    [Skip] {name} - {address}")
                        continue

                    Location.objects.get_or_create(
                        name=name,
                        address=address,
                        lat=lat,
                        lng=lng,
                        market_type=market_type,
                    )
            except Exception as e:
                print(f"[File Error] {json_file} - {e}")


if __name__ == "__main__":
    load_data_from_json()
