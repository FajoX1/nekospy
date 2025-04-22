from nekospy import bot, dp

from nekospy import handlers, utils

import os 

from rich import print

async def run_bot():
    os.system("cls" if os.name == "nt" else "clear")

    git_info = await utils.get_git_info()

    print(f"""[sky_blue1] _   _      _        ____                ____    ___  
| \ | | ___| | _____/ ___| _ __  _   _  |___ \  / _ \ 
|  \| |/ _ \ |/ / _ \___ \| '_ \| | | |   __) || | | |
| |\  |  __/   < (_) |__) | |_) | |_| |  / __/ | |_| |
|_| \_|\___|_|\_\___/____/| .__/ \__, | |_____(_)___/ 
                          |_|    |___/                
          
Commit: #{git_info['last_commit_short']}
Github: https://github.com/fajox1/nekospy[/sky_blue1]
""")
    
    print("Starting the bot...")

    await dp.start_polling(bot, skip_updates=False)