import sqlite3 as sql, os, sys, json
from telethon.sync import TelegramClient

cfg_file = open("config.json","r")
config = json.load(cfg_file)
cfg_file.close()

client = TelegramClient('bot', config["api_id"], config["api_hash"]).start(bot_token=config["token"])

class Main:
    async def main(self):
        self.config = config       
        self.db_connection = sql.connect("databaza.db")
        self.db_cursor = self.db_connection.cursor()

        self.client = client
        
        #датабазованные штуковины
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INT PRIMARY KEY NOT NULL,
                            messages_sent INT,
                            developer INT);""")

        #загрузка когоу
        sys.path.append('cogs/') 
        for cog in os.listdir("cogs/"):
            if cog.endswith(".py"): 
                cog_data = __import__(cog[:-3], globals(), locals(), [], 0)
                await cog_data.call(self)
                print(f"main <--> {cog[:-3]}")
    
        print("XxX_БоТ_ЗаПуЩеН_XxX")
            

with client:
    currentMain = Main()
    client.loop.run_until_complete(currentMain.main())
    client.run_until_disconnected()



