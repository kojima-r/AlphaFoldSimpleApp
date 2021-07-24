from lib.models import *
import lib.db as db
import os
 
 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        # テーブルを作成する
        Base.metadata.create_all(db.engine)

    # サンプルタスク
    task = Task(
        uid='xxxxxxx',
        pid=-1,
        command='1111',
        deadline=datetime(2019, 12, 25, 12, 00, 00),
    )
    db.session.add(task)
    db.session.commit()
 
    print(task)
    db.session.close()  
