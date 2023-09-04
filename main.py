from printstack import add, empty
from threading import Thread
from messages import msg
from bs4 import BeautifulSoup

import webbrowser as web
import requests as r
import json, time, uuid


"""
FIND OUT IF IT BLOCKS CATALOG SEARCHES BASED ON COOKIE OR IP
IF IP CREATE PROXIES
IF COOKIE CREATE ACCOUNTS MEANT FOR SEARCHING CATALOG
"""

cookie = ""
with open("cookie.txt", "r") as file:
	cookie = file.read()

userid = r.get(
	"https://users.roblox.com/v1/users/authenticated", 
	cookies={".ROBLOSECURITY": cookie}
).json()["id"]

token = ""
def getToken():
	global token
	token = r.post(
		"https://auth.roblox.com/v2/logout", 
		cookies={".ROBLOSECURITY": cookie}
	).headers["x-csrf-token"]

def tokenThread():
	while True:
		getToken()
		time.sleep(30)
Thread(target=tokenThread).start()
while token == "": time.sleep(0.1)


def getItemQuick(id):
	try:
		# info = r.post(
		# 	"https://catalog.roblox.com/v1/catalog/items/details",
		# 	json={"items": [{ "itemType": "Asset", "id": id }]},
		# 	headers={"x-csrf-token": token}, 
		# 	cookies={".ROBLOSECURITY": cookie}
		# ).json()

		info = r.get(
			f"https://rblx.trade/api/v2/catalog/asset-search/Asset/{id}/info"
		).json()
		add(msg("!", f"ITEM INFO: {info}\n", 0))
		return info
	except KeyError as e:
		print(msg("!", "Rate limited."))
		time.sleep(5)

def getItem(id):
	try:
		info = r.post(
			"https://catalog.roblox.com/v1/catalog/items/details",
			json={"items": [{ "itemType": "Asset", "id": id }]},
			headers={"x-csrf-token": token}, 
			cookies={".ROBLOSECURITY": cookie}
		).json()

		add(msg("!", f"ITEM INFO: {info}\n", 0))
		return info["data"][0]
	except KeyError as e:
		print(msg("!", "Rate limited."))
		time.sleep(5)

def getProduct(itemid):
	try:
		info = r.post(
			"https://apis.roblox.com/marketplace-items/v1/items/details",
			json={"itemIds": [itemid]},
			headers={"x-csrf-token": token}, 
			cookies={".ROBLOSECURITY": cookie}
		).json()
		add(msg("!", f"PRODUCT INFO: {info}\n", 0))
		return info[0]
	except KeyError as e:
		print(msg("!", "Rate limited."))
		time.sleep(5)

def getQuantity(id):
	try:
		return r.get("https://rblx.trade/api/v2/catalog/asset-search/Asset/13241161419/info")
	except KeyError as e:
		print(msg("!", "Something went wrong."))
		time.sleep(1)

def buy(id):
	info = getItemQuick(id)
	if info is None:
		return False

	itemid = info.get("collectibleItemId")
	if itemid is None:
		return False

	quantity = info.get("unitsAvailableForConsumption")
	if quantity == 0:
		return False

	productid = getProduct(itemid)["collectibleProductId"]
	creator = info["creatorTargetId"]

	data = {
		"collectibleItemId": itemid,
		"expectedCurrency": 1,
		"expectedPrice": 0,
		"expectedPurchaserId": userid,
		"expectedPurchaserType": "User",
		"expectedSellerId": creator,
		"expectedSellerType": "User",
		"idempotencyKey": "purchaseHandleId",
		"collectibleProductId": productid
	}

	while True:
		try:
			data["idempotencyKey"] = str(uuid.uuid4())

			bought = r.post(
				f"https://apis.roblox.com/marketplace-sales/v1/item/{itemid}/purchase-item", 
				json = data, 
				headers = {"x-csrf-token": token},
				cookies = {".ROBLOSECURITY": cookie}
			)
			
			add(msg("!", f"Reason: {bought.reason} {bought}\n", 0))
			add(msg("!", f"Headers: {bought.headers}\n", 0))

			if bought.reason == "Too Many Requests":
				return False

			bought = bought.json()
			add(msg("!", f"JSON: {bought}\n", 0))

			if bought["purchased"]:
				return True

			quantity = getItem(id)["unitsAvailableForConsumption"]
			if quantity == 0: 
				return False

		except Exception as e:
			print(e)


data = {
	"assetGenres": [],
	"assetTypes": [],
	"catalogMode": "Asset",
	"creators": [],
	"creatorsExclude": [],
	"cursor": "",
	"excludeCollectibles": False,
	"excludeNonCollectibles": True,
	"excludeReleased": False,
	"includeForSale": True,
	"includeLimitedItems": True,
	"includeNotForSale": True,
	"limit": 1,
	"maximumId": 0,
	"maximumOwnerCount": -1,
	"maximumPrice": -1,
	"minimumId": 0,
	"minimumOwnerCount": 0,
	"minimumPrice": 0,
	"query": "",
	"sortColumn": "Updated",
	"sortOrder": "Desc"
}

data = {
	"assetGenres": [],
	"assetTypes": [],
	"catalogMode": "Asset",
	"creators": [],
	"creatorsExclude": [],
	"cursor": "",
	"excludeCollectibles": False,
	"excludeNonCollectibles": True,
	"excludeReleased": False,
	"includeForSale": True,
	"includeLimitedItems": True,
	"includeNotForSale": True,
	"limit": 4,
	"maximumId": 0,
	"maximumOwnerCount": 0,
	"maximumPrice": -1,
	"minimumId": 0,
	"minimumOwnerCount": 0,
	"minimumPrice": 0,
	"query": "",
	"sortOrder": "Desc",
}

data = {
	"assetGenres": [],
	"assetTypes": [],
	"catalogMode": "Asset",
	"creators": [],
	"creatorsExclude": [],
	"cursor": "",
	"excludeCollectibles": False,
	"excludeNonCollectibles": True,
	"excludeReleased": False,
	"includeForSale": True,
	"includeLimitedItems": True,
	"includeNotForSale": True,
	"limit": 1,
	"maximumId": 0,
	"maximumOwnerCount": -1,
	"maximumPrice": 0,
	"minimumId": 13240548065,
	"minimumOwnerCount": 0,
	"minimumPrice": 0,
	"query": "",
	"sortColumn": "Updated",
	"sortOrder": "Desc"
}


history = ["", ""]
history1 = ["", ""]

def second():
	global history, history1
	while True:
		try:
			response = r.get("https://www.rolimons.com/marketplace/new")

			soup = BeautifulSoup(response.text, "html.parser")
			details = soup.select_one("#desktop_skin + script").text
			data = json.loads(details[details.find('{'):details.rfind('}')+1])

			id = list(data.keys())[1]
			name = data[id][0].replace("\n", "")
			price = data[id][1]

			if name != history1[0] and price == 0 and name != history[0]:
				try:
					purchased = buy(int(id))

					status = "Successful" if purchased else "Failed"
					msgtype = "+" if purchased else "-"
					print((msgtype, f"{name} [{status} Purchase - {price} RBX]"))

				except Exception as e:
					print(e)
				
				web.open(f"https://www.roblox.com/catalog/{id}")
			elif name != history1[0]:
				print(msg("i", f"{name} [Skipping - {price} RBX]"))

			history1[1], history1[0] = history1[0], name

			time.sleep(1)
		except Exception as e:
			print("MAIN CODE THREAD ERROR:")
			print(e)
#Thread(target=second).start()


while True:
	try:
		response = r.post(
			"https://rblx.trade/api/v2/catalog/asset-search/list",
			json=data
		)

		try:
			response = response.json()["data"][0]
		except Exception as e:
			print(e)
			continue

		id = response["id"]
		name = response["name"].replace("\n", "")
		price = response["price"]

		if name != history[0] and price == 0:
			try:
				purchased = buy(int(id))

				status = "Successful" if purchased else "Failed"
				msgtype = "+" if purchased else "-"
				print(msg(msgtype, f"{name} [{status} Purchase - {price} RBX]"))

			except Exception as e:
				print(e)
			
			web.open(f"https://www.roblox.com/catalog/{id}")
		elif name != history[0]:
			print(msg("i", f"{name} [Skipping - {price} RBX]"))

		empty()

		history[1], history[0] = history[0], name
		time.sleep(0.1)
	except Exception as e:
		print("MAIN CODE ERROR:")
		print(e)
