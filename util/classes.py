from discord import Member

import json, os, time

class Config:

    def __init__(self):
        if not os.path.exists("config.json"):
            self.prefix = '.'
            self.token = 'YOUR_TOKEN_HERE'
            self.status = 'Frost 2.1.2'
            self.owner_id = 0
            self.save()
        else:
            with open("config.json", "r") as f:
                self.__dict__ = json.load(f)

    def save(self):
        with open("config.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()




class Server:

    def __init__(self, frost, server_id):
        self.frost = frost
        self.server_id = server_id
        if not self.load():
            self.prefix = self.frost.config.prefix
            self.moderators = []
            self.daily_message = DailyMessage(self)
            self.counting = Counting(self)
            self.suggestions = Suggestions(self)
            self.save()

    def load(self) -> bool:
        if not os.path.exists("servers"):
            os.mkdir("servers")
        for file in os.listdir("servers"):
            if file.endswith(".json") and file.startswith(str(self.server_id)):
                with open(f"servers/{file}", "r") as f:
                    data = json.load(f)
                self.__dict__ = {
                    "frost": self.frost,
                    "server_id": self.server_id,
                    "prefix": data["prefix"],
                    "moderators": data["moderators"],
                    "daily_message": DailyMessage(self, **data["daily_message"]),
                    "counting": Counting(self, **data["counting"]),
                    "suggestions": Suggestions(self, **data["suggestions"]),
                }
                return True
        return False

    def save(self):
        dict = self.__dict__.copy()
        del dict["frost"]
        del dict["server_id"]
        dict["daily_message"] = self.daily_message.to_dict()
        dict["counting"] = self.counting.to_dict()
        dict["suggestions"] = self.suggestions.to_dict()

        with open(f"servers/{self.server_id}.json", "w") as f:
            json.dump(dict, f, indent=4)

    def is_mod(self, member: Member) -> bool:
        return member.guild_permissions.administrator or any(role.id in self.moderators for role in member.roles)

    def add_mod(self, role_id: int) -> bool:
        if role_id not in self.moderators:
            self.moderators.append(role_id)
            self.save()
            return True
        return False

    def remove_mod(self, role_id: int) -> bool:
        if role_id in self.moderators:
            self.moderators.remove(role_id)
            self.save()
            return True
        return False

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.save()


class DailyMessage:

    def __init__(self, server, enabled: bool = False, channel_id: int = 0, cooldowns: dict = {}):
        self.server = server
        self.enabled = enabled
        self.channel_id = channel_id
        self.cooldowns = cooldowns
        for key, value in self.cooldowns.copy().items():
            if not isinstance(key, str):
                continue
            self.cooldowns[int(key)] = value
            del self.cooldowns[key]


    def to_dict(self):
        return {
            "enabled": self.enabled,
            "channel_id": self.channel_id,
            "cooldowns": self.cooldowns
        }

    def toggle(self, enabled: bool):
        self.enabled = enabled
        self.server.save()

    def set_channel(self, channel_id: int):
        self.channel_id = channel_id
        self.server.save()

    def add_cooldown(self, user_id: int) -> bool:
        if user_id not in self.cooldowns or time.time() > self.cooldowns[user_id]:
            self.cooldowns[user_id] = time.time() + 86400
            self.server.save()
            return True
        return False

    def remove_cooldown(self, user_id: int) -> bool:
        if user_id in self.cooldowns:
            del self.cooldowns[user_id]
            self.server.save()
            return True
        return False



class Counting:

    def __init__(self, server, enabled: bool = False, channel_id: int = None, number: int = 0, last_user: int = 0, blacklist: list = []):
        self.server = server
        self.enabled = enabled
        self.channel_id = channel_id
        self.number = number
        self.last_user = last_user
        self.blacklist = blacklist

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "channel_id": self.channel_id,
            "number": self.number,
            "last_user": self.last_user,
            "blacklist": self.blacklist
        }

    def toggle(self, enabled: bool):
        self.enabled = enabled
        self.server.save()

    def set_channel(self, channel_id: int):
        self.channel_id = channel_id
        self.server.save()

    def set_number(self, number: int):
        self.number = number
        self.server.save()

    def set_last_user(self, user_id: int):
        self.last_user = user_id
        self.server.save()

    def add_blacklist(self, user_id: int) -> bool:
        if user_id not in self.blacklist:
            self.blacklist.append(user_id)
            self.server.save()
            return True
        return False

    def remove_blacklist(self, user_id: int) -> bool:
        if user_id in self.blacklist:
            self.blacklist.remove(user_id)
            self.server.save()
            return True
        return False

    def is_blacklisted(self, user_id: int) -> bool:
        return user_id in self.blacklist

    def increment(self, user_id: int, number: int) -> str:
        if self.is_blacklisted(user_id):
            return "blacklisted"
        if number != self.number + 1:
            return "wrong_number"
        if user_id == self.last_user:
            return "same_user"
        self.number = number
        self.last_user = user_id
        self.server.save()
        return "success"

    
class Suggestions:

    def __init__(self, server, enabled: bool = False, channel_id: int = None, blacklist: list = [], suggestions: dict = {}):
        self.server = server
        self.enabled = enabled
        self.channel_id = channel_id
        self.blacklist = blacklist
        self.suggestions = suggestions

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "channel_id": self.channel_id,
            "blacklist": self.blacklist,
            "suggestions": self.suggestions
        }

    def toggle(self, enabled: bool):
        self.enabled = enabled
        self.server.save()

    def set_channel(self, channel_id: int):
        self.channel_id = channel_id
        self.server.save()

    def add_blacklist(self, user_id: int) -> bool:
        if user_id not in self.blacklist:
            self.blacklist.append(user_id)
            self.server.save()
            return True
        return False

    def remove_blacklist(self, user_id: int) -> bool:
        if user_id in self.blacklist:
            self.blacklist.remove(user_id)
            self.server.save()
            return True
        return False

    def add_suggestion(self, user_id: int, suggestion: str) -> bool:
        if user_id in self.blacklist:
            return False
        suggestion_id = len(self.suggestions)
        self.suggestions[suggestion_id] = {
            "user_id": user_id,
            "suggestion": suggestion,
            "time": time.time()
        }
        self.server.save()
        return self.suggestions[suggestion_id]