# Contraction Cop Docs
This is a list of the commands and the setup for the bot! and just generalally helpful tips

# About
This is a discord bot that check every message sent to see if it has a contraction using this [list](contractions.txt) of contractions. And then either deletes the message or just points it out to the user depending on the delete setting.

# Commands

 - ## cc!help
  Help is used to show a simplified version of [this](#commands) in disord

***

 - ## cc!settings
 Settings is used to configure diffent aspects of the bot
 - ### usage:
   - cc!settings delete
       - cc!settings delete on
       - cc!settings delete off
   - cc!settings prefix
       - cc!settings prefix [new prefix]
 
 Delete changes if the bot deletes a message with a contraction or just warns the user.<br>
 Prefix changes the prefix of the bot, the default prefix is "cc!".

# Setup
There is some setup needed but the little bit at the top of [main.py](main.py) helps make it very minimal
1. Create a .env file in the base directory with [main.py](main.py) and fill make a line with:
   - `KEY=` and then your discord bot private key
2. Make sure that you only join servers when the bot is offline otherwise you have to manually input the server id and the corosponding setting<br>

And that is basically it! There is not much else to say about the setup

# Plans
- Dynamic contraction detection
  - Instead of checking list see if it has common contraction features
- More commands
  - Just more clear, less vague, and just more interactive
- More configurable
  - Add more settings like
    - Channel check blacklist
    - Add/remove contractions from the list
    - If i end up making dynamic contraction detection then a severity level
