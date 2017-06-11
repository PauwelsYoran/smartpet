from MCP import Channel
import time
c= Channel(0)

while True:
    print(c.data())
    time.sleep(0.5)