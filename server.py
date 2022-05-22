import argparse
import asyncio
import websockets
import json
import random
import sys

server_status = {
	"waiting": {},
	"users": [],
	"invites": {}
}

def msgobj(msg_type, value=None):
	if value == None:
		return json.dumps({"type": msg_type})
	else:
		return json.dumps({"type": msg_type, "value": value})


async def connection(ws, path):
    user = {
		"ws": ws,
		"action": "ready",
		"session": False,
		"name": None,
		"don": None
	}
    server_status["users"].append(user)
    try:
        await ws.send(json.dumps({"ok": True, "message": "hi connet sucess"}))
        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=10)
            except asyncio.TimeoutError:
                # Keep user connected
                pong_waiter = await ws.ping()
                try:
                    await asyncio.wait_for(pong_waiter, timeout=10)
                except asyncio.TimeoutError:
                # Disconnect
                    break
            except websockets.exceptions.ConnectionClosed:
                # Connection closed
                break
            else:
                try:
                    data = json.loads(message)
                except json.decoder.JSONDecodeError:
                    data = {}
        
 
    # finally:
    #     # User disconnected
	# 	del user["ws"]
	# 	del server_status["users"][server_status["users"].index(user)]
	# 	if "other_user" in user and "ws" in user["other_user"]:
	# 		user["other_user"]["action"] = "ready"
	# 		user["other_user"]["session"] = False
	# 		await asyncio.wait([
	# 			user["other_user"]["ws"].send(msgobj("gameend")),
	# 			user["other_user"]["ws"].send(status_event())
	# 		])
	# 		del user["other_user"]["other_user"]
	# 	if user["action"] == "waiting":
	# 		del server_status["waiting"][user["gameid"]]
	# 		await notify_status()
	# 	elif user["action"] == "invite" and user["session"] in server_status["invites"]:
	# 		del server_status["invites"][user["session"]]



start_server = websockets.serve(hello, "localhost", 8888)

asyncio.get_event_loop().run_until_complete(start_server)
print("Server is running port:8888")
asyncio.get_event_loop().run_forever()



# async def hello(websocket, path):
#     while True:
#         name = await websocket.recv()
#         print(f"< {name}")
#         greeting = f"Hi {name}!"
#         print(greeting)
#         await websocket.send(greeting)
#         print(f"> {greeting}")
