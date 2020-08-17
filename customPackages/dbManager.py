import mysql.connector

class dbManager():
    """Manage database from MySQL"""
    def __init__(self,host = None,user = None,passwd = None,schema = None):
        self.set_DB(host,user,passwd,schema)
        self.msgCountTableName = 'Discord Message Count Table'
    
    def set_DB(self,host = None,user = None,passwd = None,schema = None):
        """Set the database to another database after object has been made if needed."""
        self.host = host
        self.user = user
        self.passwd = passwd
        self.schema = schema

        self.database = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database = schema
        )
    
    def get_tables(self):
        myCursor = self.database.cursor(dictionary = True)
        myCursor.execute(
            "SHOW TABLES"
        )
        tables = myCursor.fetchall()
        tableSet = set()
        for t in tables:
            tableSet.add(t[f'Tables_in_{self.schema}'])
        return(tableSet)

    async def init_table(self):
        myCursor = self.database.cursor(dictionary = True)
        try:
            myCursor.execute(
                f"CREATE TABLE `{self.msgCountTableName}` (`Server Name` VARCHAR(100), `Server ID` VARCHAR(100), `Channel Name` VARCHAR(100), `Channel ID` VARCHAR(100), `Channel MsgCount` INTEGER) "
            )
        except mysql.connector.errors.ProgrammingError as e:
            pass #ignore error with table already exists
    
    async def countMsgs(self,channel):
        count = 0
        async for msg in channel.history(limit = None):
            if not msg.author.bot:
                count+=1
        return count

    async def init_Server(self,guild):
        channels = guild.text_channels
        
        myCursor = self.database.cursor(dictionary = True)

        # check that we are not adding additional rows
        myCursor.execute(
        f"SELECT * FROM `{self.msgCountTableName}` "
        f"WHERE `Server ID` = {guild.id} "
        )
        curGuildDict = myCursor.fetchall()
        chanIDs = [row['Channel ID'] for row in curGuildDict] #slow when we start talking about large amounts of servers
        
        for chan in channels:
            if str(chan.id) not in chanIDs:
                msgCount = await self.countMsgs(chan)
                self.addChannel(chan,msgCount)
                
        self.database.commit() 

    async def get_channelMsgCount(self,ctx):
        myCursor = self.database.cursor(dictionary = True)
        myCursor.execute(
            f"SELECT `Channel MsgCount` "
            f"FROM `{self.msgCountTableName}` "
            f"WHERE `Server ID` = {ctx.guild.id} "
                f"AND `Channel ID` = {ctx.channel.id}"
        )
        t = myCursor.fetchall()

        if t:
            return t[0]['Channel MsgCount']
        else:
            print("Initializing rows.")
            await self.init_Server(ctx.guild)
            await self.get_channelMsgCount(ctx)

    async def updateDB(self,ctx,change = 1):
        myCursor = self.database.cursor(dictionary = True)

        # Add a change to msg counter in database
        currentMsgCount = await self.get_channelMsgCount(ctx)

        myCursor.execute(
            f"UPDATE `{self.msgCountTableName}` "
            f"SET `Channel MsgCount` = {currentMsgCount+change} "
            f"WHERE `Server ID` = {ctx.guild.id} "
                f"AND `Channel ID` = {ctx.channel.id} "
        )
        self.database.commit()

    def removeChannel(self,chan):
        myCursor = self.database.cursor(dictionary = True)

        myCursor.execute(
            f"DELETE FROM `{self.msgCountTableName}` "
            f"WHERE `Channel ID` = {chan.id} "
        )
        self.database.commit()

    def addChannel(self,chan,msgCount = 0):
        myCursor = self.database.cursor(dictionary = True)

        myCursor.execute(
            f"INSERT INTO `{self.msgCountTableName}` (`Server Name`, `Server ID`, `Channel Name`, `Channel ID`, `Channel MsgCount`) "
            f"VALUES ('{chan.guild.name}', '{chan.guild.id}', '{chan.name}', '{chan.id}', {msgCount}) "
            )
        self.database.commit()

    async def removeServer(self,guild):
        myCursor = self.database.cursor(dictionary = True)

        myCursor.execute(
            f"DELETE FROM `{self.msgCountTableName}` "
            f"WHERE `Server ID` = {guild.id} "
        )
        self.database.commit()