import asyncio
import json
import ssl
import time
from datetime import datetime
from typing import Set
import pause
import aiohttp

ssl = ssl.SSLContext()


async def fetch(session, url):
    async with session.get(url, ssl=ssl) as response:
        print("Get", response.status)
        return await response.json()


async def fetch_post(session, request_data):
    url, headers, payload = request_data
    async with session.post(url, ssl=ssl, headers=headers, data=payload) as response:
        print("Post", response.status)
        return await response.json()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], return_exceptions=True
        )
        return results


async def fetch_all_post(request_data, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch_post(session, r) for r in request_data],
            return_exceptions=True,
        )
        return results


def get(urls: list) -> list:
    s = time.perf_counter()
    loop = asyncio.get_event_loop()
    resps = loop.run_until_complete(fetch_all(urls, loop))
    print(f"Get execution time: {time.perf_counter() - s:.6f} sec")
    return resps


def post(request_data: list[set]) -> list:
    s = time.perf_counter()
    loop = asyncio.get_event_loop()
    resps = loop.run_until_complete(fetch_all_post(request_data, loop))
    print(f"Post execution time: {time.perf_counter() - s:.6f} sec")
    return resps


def get_headers():
    # Test account
    bearer = "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl9pZCI6IjIxMDJjZTEzMmYwMDQ1MDRiM2U0MWY1NGZjNDM4Zjg2IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Im1hcmNvZGlmcmFuQGhvdG1haWwuY29tIiwic3ViIjoibWFyY29kaWZyYW5AaG90bWFpbC5jb20iLCJ1c2VyX2lkIjoiMTBlNzE3MzUtM2UxZi00Y2Y2LTkwMjYtN2M0NjE4N2U0Njg5IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiMCIsIm5iZiI6MTY2NDAxNTIzNiwiZXhwIjoxNjc5NTY3MjM2LCJpc3MiOiJodHRwczovL2F1dGgua2lkZS5hcHAiLCJhdWQiOiI1NmQ5Y2JlMjJhNTg0MzJiOTdjMjg3ZWFkZGEwNDBkZiJ9.6q7kj5yc45ct9xEVPGcx6bNV2lpBNdL5MpBZXTWVvyRjySSrGic_7Y-PgbwG-67cEoBI3ohpjnm1npiPdjTNuQ"
    # marcodifran@gmail.com
    # bearer = "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl9pZCI6ImM1OGJkZGZjNzY3NDQ0ZGJiZjVhNTJiOWRkMGZiZjY4IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Im1hcmNvZGlmcmFuQGdtYWlsLmNvbSIsInN1YiI6Im1hcmNvZGlmcmFuQGdtYWlsLmNvbSIsInVzZXJfaWQiOiI3MDhiZTg4MS05ODkwLTRjMjktYTkyOC1lNmU5Nzg0Y2RhYTMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiIwIiwibmJmIjoxNjY0MDI4Nzk2LCJleHAiOjE2Nzk1ODA3OTYsImlzcyI6Imh0dHBzOi8vYXV0aC5raWRlLmFwcCIsImF1ZCI6IjU2ZDljYmUyMmE1ODQzMmI5N2MyODdlYWRkYTA0MGRmIn0.IX0YrJMXg_vIrOzKjil6UJj70Nu_t5wG6DUziOJAPmjWFF7F6jZcLWdRa-IVQn6eDY002SobCzoTTye4Fd0prw"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7",
        "authorization": bearer,
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-requested-with": "XMLHttpRequest",
    }
    return headers


def get_payload(variant_id: str):
    payload = {
        "toCreate": [
            {
                "inventoryId": variant_id,
                "quantity": 1,
                "productVariantUserForm": None,
            }
        ],
        "toCancel": [],
    }
    return json.dumps(payload)


def reserve_tickets(variant_ids: list[str]):
    requests = []
    for variant_id in variant_ids:
        reserv_url = "https://api.kide.app/api/reservations"
        headers = get_headers()
        payload = get_payload(variant_id)
        requests.append((reserv_url, headers, payload))
    return post(requests)



# 17ms to get until here (+2ms python to start)
pause.until(datetime(2022, 9, 25, 12, 30, 0))
# 0.045ms for pause() to start
# 0.003ms for assignments of event_id and event_url
# 0.524ms for get() to start, time for the request to be sent

# Get event data
event_id = "1c4af541-e2a7-4c55-8a61-27e64063a68e"
event_url = f"https://api.kide.app/api/products/{event_id}"
details = get([event_url])
# First because we have 1 url
details = details[0]
variants = details["model"]["variants"]
variant_ids = [variant["inventoryId"] for variant in variants]
# 0.031ms from get to here - list extraction and iteration
reserve_tickets(variant_ids)
