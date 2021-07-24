from lib.models import *
import lib.db as db
import os
import glob
import datetime
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        # テーブルを作成する
        Base.metadata.create_all(db.engine)

    task = db.session.query(Task).filter(Task.valid == True).all()
    db.session.close()

    uid_list=set([t.uid for t in task])
    print(uid_list)
    results=[]
    for path in glob.glob("static/result/*"):
        if os.path.isdir(path):
            b=os.path.basename(path)
            print(b,path)
            results.append(b)
    for r in results:
        if r not in uid_list:
            print(r)
            task = Task(
                uid=r,
                pid=0,
                command="",
                deadline=datetime.datetime.now()+datetime.timedelta(days=1)
            )
            db.session.add(task)
            db.session.commit()
 
    db.session.close()  
