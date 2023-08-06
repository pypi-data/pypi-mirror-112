# disbotlist 
useful library for [disbots.xyz](https://disbots.xyz)

## Installation
```
pip install disbots
```
## example 
Server Count Post :
```python
from disbots import disbots
from discord.ext import commands

client = commands.Bot(command_prefix="!") 
dbl = disbots(client,"token of disbots")

@client.event
async def on_ready():
  x = await dbl.serverCountPost()
  print(x)

client.run("token")
```
