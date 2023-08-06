## discord-ext-cli

A CLI to talk through console.

# Installation

```shell
python3 -m pip install discord-ext-cli
```

## Example

```python
import discord
from discord.ext import cli

# Enable gateway intents on the developer portal

bot = cli.CLI(channel_id="Channel ID", intents=discord.Intents.all())

bot.run("Token Here")