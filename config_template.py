import datetime

# Basic bot config, insert your token here, update description if you want
prefixes = ["."]
token = "token-goes-here"
bot_description = "Komet-CL (Lite)"

# If you forked robocop-ng, put your repo here
source_url = "https://git.nicholemattera.com/NicholeMattera/Komet-Lite"

# The bot description to be used in .robocop embed
embed_desc = (
    "Robocop-NG is developed by [Ave](https://github.com/aveao)"
    " and [tomGER](https://github.com/tumGER), and is a rewrite "
    "of Robocop.\nRobocop is based on Kurisu by 916253 and ihaveamac."
)

# The bot manager and staff roles
# Bot manager can run eval, exit and other destructive commands
# Staff can run administrative commands
bot_manager_role_id = 123456789098765432  # Bot management role in ReSwitched
staff_role_ids = [
    123456789098765432,
]

# Log channel used to log bot activity
botlog_channel = 123456789098765432

# Rules channel used by the List Cog
rules_channel = 123456789098765432 

# Used for uploading raw text files for list editing.
list_files_channel = 123456789098765432  

# Channels that are lists that are controlled by the lists cog.
list_channels = [123456789098765432]
