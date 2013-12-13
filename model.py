import web, datetime

web.config.debug_sql = False 
db_debug_mode = True

if(db_debug_mode):
    db = web.database(dbn="sqlite", db="/tmp/test.db")
else:
    db = web.database(dbn="sqlite", db=":memory:")

def init_db():
    db._db_cursor().execute("""
CREATE TABLE IF NOT EXISTS `task`  (
  `idtask` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `title` varchar(85) NOT NULL,
  `status` int(11) DEFAULT NULL,
  `srcname` varchar(45) DEFAULT NULL,
  `resname` varchar(45) DEFAULT NULL
)
""")    

def new_task(title, status, src_file):
    return db.insert('task', title=title, status=status, srcname=src_file)
    