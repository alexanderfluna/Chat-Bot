import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

# discord.py API
client = discord.Client()

# Startings words
sad_words = [
  "sad", "upset", "depressed", "unhappy", "angry", "furious", "miserable", "depressing", "melancholy"
]
starter_encouragements = [
    "Feel better!", "Don't give up!", "Cheer up!", "Hang in there.", "You are a great person!", "You're doing great!"
]

# Bot will only respond with encouragements if True
if "responding" not in db.keys():
  db["responding"] = True

# Fetches quqote from ZenQuotes API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return (quote)

# Adds new encouraging message
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

# Deletes encouraging message
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

# discord.py API 
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

# Event for different commands
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
 
  # Inspirational quote
  if msg.startswith("!inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    # Prints encouragement if there is a sad word
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  # Adds encouragement
  if msg.startswith("!new"):
    encouraging_message = msg.split("!new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  # Deletes encouragement
  if msg.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # Prints list of encouragements
  if msg.startswith("!list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # Turns on and off responding feature
  if msg.startswith("!responding"):
    value = msg.split("!responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")

# Will keep web server running
keep_alive()
# discord.py API
client.run(os.environ["TOKEN"])
