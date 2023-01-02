
# Frost

Frost is a Discord bot utilizing the `discord.py` library. It was originally designed to serve my specific server, but has since been redesigned since the v2.0.0 update to include support for serving several guild configurations.

This repo is an entirely new rewrite from v2.1.1, although aimed to have the same features and be more extensible, as I'm finally commiting to making Frost an open-source project. 

It's pretty barebones at the moment. Don't expect too much.

## Features

- Server:
    - Configurable prefix that overrules the global: `.prefix {new_prefix}`
    - Configurable moderation roles (controls access to specific commands): `.addmod {role} | .removemod {role} | .listmods`
    - Custom Channels!
        - Daily Message: `.dailymessage {enable/disable/setchannel/removecooldown} {channel/user}`
            - Allows users to send only 1 message per 24 hours.
        - Counting: `[NYI]`
            - The same user can't count twice in a row, and anything besides the next number in the sequence is deleted.
            - Features a configurable blacklist for those pesky users
        - Suggestions: `[NYI]`
            - Enable users to submit suggestions for whatever.
            - Messages sent in this channel are immediately deleted and replaced by the bot for users to vote upon.
            - Also features a configurable blacklist
- Global:
    - `ping`: View the bot's ping


## Installation

Fill out `config.json`, replacing `token` with your bot token from the [Discord Developer Portal](https://discord.com/developers/applications).

Ensure the bot also has **all Privileged Gateway Intents enabled**.

To deploy this project, run

```bash
  pip install -r requirements.txt

  py app.py
```


## Feedback

If you have any feedback, please reach out to me on Discord: `wafflebitez#0001`

I have no clue what I'm doing tbh pls help