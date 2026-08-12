class CursorTools:
    def __init__(self,request):
        print("OPENED")
        self.conn = request.app.state.pool.get_connection()
        self.cursor = self.conn.cursor(buffered=True)

    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, SQLquery, params=None):
        self.cursor.execute(SQLquery, params)

    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()