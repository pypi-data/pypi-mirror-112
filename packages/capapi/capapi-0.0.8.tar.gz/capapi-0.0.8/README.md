# CapAPI
### Short for "Capitalism API for Python"

This is a simple, free-to-use, API wrapper for the [Capitalism Bots API](https://discord.capitalismbot.repl.co/beta/api/v1)

Source Code: https://github.com/drapespy/CapAPI

### Some Examples

```py
# Basic get user data example
from capapi import get_user

user = get_user(763854419484999722)

print(user.wallet) # Prints the amount in wallet
```

```py
# has_x examples
from capapi import get_user

user = get_user(763854419484999722)

print(user.is_admin()) # Same functionality as
print(user.has_badge("admin"))

print(user.has_item("kirk_juice"))
```