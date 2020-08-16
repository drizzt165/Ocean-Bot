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
        

    def init_rows(self,ctx):
        guild = ctx.guild
        channels = guild.text_channels
        
        myCursor = self.database.cursor(dictionary = True)

        for chan in channels:
            try:
                myCursor.execute(
                f"SELECT * FROM `{self.msgCountTableName}` "
                f"WHERE `Server ID` = {guild.id} "
                )
            except Exception as e:
                print(e)

            myCursor.execute(
                f"INSERT INTO `{self.msgCountTableName}` (`Server Name`, `Server ID`, `Channel Name`, `Channel ID`, `Channel MsgCount`) "
                f"VALUES ({guild.name}, {guild.id}, {chan.name}, {chan.id}, 5) "
            )
                
        #self.database.commit() 

    def update_row(self,ctx):
        myCursor = self.database.cursor(dictionary = True)

        self.database.commit()