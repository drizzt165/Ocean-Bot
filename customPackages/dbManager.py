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

    def init_table(self,ctx): #really, only needs to be ran once ever.
        guild = ctx.guild
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

    async def init_rows(self,ctx):
        guild = ctx.guild
        channels = guild.text_channels
        
        myCursor = self.database.cursor(dictionary = True)

        myCursor.execute(
        f"SELECT * FROM `{self.msgCountTableName}` "
        f"WHERE `Server ID` = {guild.id} "
        )
        curGuildDict = myCursor.fetchall()
        chanIDs = [row['Channel ID'] for row in curGuildDict] #slow when we start talking about large amounts of servers
        
        for chan in channels:
            if str(chan.id) not in chanIDs:
                msgCount = await self.countMsgs(chan)
                myCursor.execute(
                    f"INSERT INTO `{self.msgCountTableName}` (`Server Name`, `Server ID`, `Channel Name`, `Channel ID`, `Channel MsgCount`) "
                    f"VALUES ('{guild.name}', '{guild.id}', '{chan.name}', '{chan.id}', {msgCount}) "
            )
                
        self.database.commit() 

    def updateDB(self,ctx):
        myCursor = self.database.cursor(dictionary = True)
        



        # Increment msg counter in database
        myCursor.execute(
            f"SELECT `Channel MsgCount` "
            f"FROM `{self.msgCountTableName}` "
            f"WHERE `Server ID` = {ctx.guild.id} "
                f"AND `Channel ID` = {ctx.channel.id}"
        )
        t = myCursor.fetchall()

        currentMsgCount = t[0]['Channel MsgCount']
        myCursor.execute(
            f"UPDATE `{self.msgCountTableName}` "
            f"SET `Channel MsgCount` = {currentMsgCount+1} "
            f"WHERE `Server ID` = {ctx.guild.id} "
                f"AND `Channel ID` = {ctx.channel.id} "
        )
        self.database.commit()