from threading import Thread
import time, requests

# Get cookie from file
cookie = ""
with open("cookie.txt", "r") as file:
	cookie = file.read()

# Get userid from users api
userid = requests.get(
	"https://users.roblox.com/v1/users/authenticated", 
	cookies={".ROBLOSECURITY": cookie}
).json()["id"]

# Get token every minute
token = ""
def getToken():
	global token, cookie
	token = requests.post(
		"https://auth.roblox.com/v2/logout", 
		cookies={".ROBLOSECURITY": cookie}
	).headers["x-csrf-token"]
getToken()