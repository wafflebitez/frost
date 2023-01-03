
# Frost

Frost is a Discord bot utilizing the `discord.py` library. It was originally designed to serve my specific server, but has since been redesigned since the v2.0.0 update to include support for serving several guild configurations.

This repo is an entirely new rewrite from v2.1.1, although aimed to have the same features and be more extensible, as I'm finally commiting to making Frost an open-source project. 

It's pretty barebones at the moment. Don't expect too much.

## Features

- Server:
    - Configurable prefix that overrules the global: `.prefix {new_prefix}`
    - Configurable moderation roles (controls access to specific commands): `.addmod @role/.removemod {role}/.listmods`
    - Custom Channels!
        - Daily Message: `.dailymessage {enable/disable/setchannel #channel/removecooldown @user}`
            - Allows users to send only 1 message per 24 hours.
        - Counting: `.counting {enable/disable/setchannel #channel/setnumber 123/setuser @user/blacklist @user`
            - The same user can't count twice in a row, and anything besides the next number in the sequence is deleted.
            - Features a configurable blacklist for those pesky users
        - Suggestions: `.suggestions {enable/disable/setchannel #channel/blacklist @user}`
            - Enable users to submit suggestions for whatever.
            - Messages sent in this channel are immediately deleted and replaced by the bot for users to vote upon.
            - Also features a configurable blacklist
- Global:
    - `ping`: View the bot's ping
    - `userinfo`: Displays a user's username, user ID, account creation date, and server join date


## Installation

Fill out `config.json`, replacing `token` with your bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

Ensure the bot also has **all Privileged Gateway Intents enabled**.

To deploy this project, run

```bash
  pip install -r requirements.txt

  py app.py
```

Add the bot to your server using this URL, replacing `{YOUR_CLIENT_ID}` with your client ID
```
 https://discord.com/oauth2/authorize?client_id={YOUR_CLIENT_ID}&scope=bot&permissions=26688
 ```


## Feedback

If you have any feedback, please reach out to us on [our Discord](https://discord.gg/PtexjU6vAW) or directly: `wafflebitez#0001` 

I have no clue what I'm doing tbh, please help