import requests, sys

class Ratelimit(Exception):
    pass

def get_user(user_id):
    return User(user_id)

def banner():
    # Some consoles are **** so I don't know why they are so **** so so so so I used std::cout
    sys.stdout.buffer.write('''\
   _____                    _____ _____ 
  / ____|             /\   |  __ \_   _| Version 0.0.8
 | |     __ _ _ __   /  \  | |__) || |   Made by drapes#0001
 | |    / _` | '_ \ / /\ \ |  ___/ | |   
 | |____ (_| | |_) / ____ \| |    _| |_  Python wrapper for the
  \_____\__,_| .__/_/    \_\_|   |_____| Capitlism API
             | |                        
             |_|   
'''.encode('utf8'))

class User:
    
    def __init__(self, user_id: int):
        self.user_id  = user_id

    @property
    def wallet(self):
        """`property` Returns int of the money in the users wallet"""
        
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=wallet")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank(self):
        """`property` Returns int of the money in the users bank"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank_max(self):
        """`property` Returns int of the users max bank size"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_max")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def inventory(self):
        """`property` Returns json of the users inventory. 
        To get a value use `get_user(x).inventory["beef"]`.
        I will add full inventory support after release."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=inventory")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def inv(self):
        """`property` Returns json of the users inventory. To get a value use `get_user(x).inventory["beef"]`.
        I will add full inventory support after release."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=inventory")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bitcoin(self):
        """`property` Returns int of the users bitcoin"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bitcoin")
        if resp.status_code == 200:        
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def exp(self):
        """`property` Returns int of the users experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def xp(self):
        """`property` Returns int of the users experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def multiplier(self):
        """`property` Returns float of the users multiplier"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def multi(self):
        """`property` Returns float of the users multiplier"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")
    
    @property
    def bank_colour(self):
        """`property` Returns str of the users bank colour"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank_color(self):
        """`property` Returns str of the users bank color"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def ads(self):
        """`property` Returns int of the users ads."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=ads")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def job(self):
        """`property` Returns str of the users job."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=job")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def badges(self):
        """`property` Returns json of the users badges. To get a value use `get_user(x).badges["RICH"]`.
        I will add full badge support later."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=badges")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    # Has Stuff
    def has_item(self, item:str):
        """Returns True if the user has a the given item in their inventory"""
        inventory = self.inventory
        try:
            result = inventory[str(item)]
            if result > 0:
                return True
            else:
                return False
        except:
            return False

    def has_badge(self, item:str):
        """Returns True if the user has the given badge."""
        badges = self.badges
        try:
            result = badges[str(item)]
            if result > 0:
                return True
            else:
                return False
        except:
            return False

    def is_admin(self):
        """Returns True if the user has the badge "admin\""""
        return self.has_badge("admin")
