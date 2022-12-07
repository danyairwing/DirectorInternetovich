from telethon import events
async def call(main):

    client = main.client
    """
        TODO: /top; автоматитческий сейв
    """


    @client.on(events.NewMessage())
    async def new_message(event):

        """
            считание сообщений
        """

        msg = event.message
        user_id = msg.from_id.user_id
        chat_id = msg.id

        main.db_cursor.execute(f"SELECT messages_sent FROM users WHERE id={user_id}")
        msg_count = main.db_cursor.fetchone()
        
        if msg_count == None: 
            msg_count = 0 
        else:
            msg_count = msg_count[0]

        print(f"{user_id} - {msg_count}msg - {chat_id}")

        main.db_cursor.execute(f"INSERT OR REPLACE INTO users (id, messages_sent) VALUES ({user_id}, {msg_count+1}); ")

    @client.on(events.NewMessage(pattern="/stats"))
    async def return_stat(event):

        """
            статистика участника чата
        """

        main.db_cursor.execute(f"SELECT messages_sent FROM users WHERE id={event.from_id.user_id}")
        msg_count = main.db_cursor.fetchone()

        await event.reply(f"вы насрали целых {msg_count[0]} сообщений")

    
    @client.on(events.NewMessage(pattern="/commit_db"))
    async def commit_db(event):

        """
            сэйв датабазы
        """

        main.db_connection.commit()


        await event.reply(f"датабаза сахранена на дисковой Drive")



