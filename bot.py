import discord
from discord.ext import commands
import json, os, requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f: json.dump({}, f)
    with open(file, "r") as f: return json.load(f)

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=2)

items = load_data("items.json")
users = load_data("users.json")

with open("config.json") as f:
    config = json.load(f)
API_KEY = config["nowpayments_api_key"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def shop(ctx):
    if not items:
        await ctx.send("No items available.")
        return
    embed = discord.Embed(title="🛒 BTC Shop")
    for iid, item in items.items():
        embed.add_field(name=f"{iid}: {item['name']}", value=f"{item['desc']} - ${item['price']}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx, item_id):
    item = items.get(item_id)
    if not item:
        await ctx.send("Item not found.")
        return
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": item["price"],
        "price_currency": "usd",
        "pay_currency": "btc",
        "order_id": f"{ctx.author.id}_{item_id}",
        "order_description": f"Buy {item['name']}",
        "ipn_callback_url": config["webhook_url"]
    }
    res = requests.post("https://api.nowpayments.io/v1/invoice", headers=headers, json=payload)
    data = res.json()
    if "invoice_url" in data:
        await ctx.send(f"Pay with BTC: {data['invoice_url']}")
    else:
        await ctx.send("Failed to create payment link.")

@bot.command()
async def inventory(ctx):
    user = users.get(str(ctx.author.id), {"inventory": []})
    if not user["inventory"]:
        await ctx.send("Your inventory is empty.")
        return
    names = [items[i]['name'] for i in user["inventory"] if i in items]
    await ctx.send("You own: " + ", ".join(names))

bot.run(config["discord_token"])