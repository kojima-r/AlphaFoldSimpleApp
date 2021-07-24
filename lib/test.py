import db
from models import Task
from datetime import datetime
# サンプルタスク
task = Task(
    command='1112',
    deadline=datetime(2019, 12, 25, 12, 00, 00),
)
db.session.add(task)
db.session.commit()

task = db.session.query(Task).filter(Task.valid == True).all()
db.session.close()
print(task[0])
print(task)
db.session.close()  


