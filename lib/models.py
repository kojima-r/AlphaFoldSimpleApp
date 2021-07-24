from datetime import datetime

from .db import Base

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.dialects.mysql import INTEGER, BOOLEAN

import hashlib

SQLITE3_NAME = "./db.sqlite3"

class Task(Base):
    """
    ToDoタスク
    id       : 主キー
    uid  : 外部キー
    pid  : 外部キー
    content  : 内容
    deadline : 締め切り
    date     : 作成日
    done     : タスクを終了したか
    """
    __tablename__ = 'task'
    id = Column(
        'id',
        INTEGER(unsigned=True),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    uid = Column('uid', String(64))
    pid = Column('pid', INTEGER())
    name = Column('name', String(256))
    command = Column('command', String(256))
    result  = Column('result', String(1024))
    deadline = Column(
        'deadline',
        DateTime,
        default=None,
        nullable=False,
    )
    date = Column(
        'date',
        DateTime,
        default=datetime.now(),
        nullable=False,
        server_default=current_timestamp(),
    )
    done = Column('done', BOOLEAN, default=False, nullable=False)
    valid = Column('valid', BOOLEAN, default=True, nullable=False)

    def __init__(self, name: str, uid: str, pid: str, command: str, deadline: datetime, date: datetime = datetime.now()):
        self.uid =uid 
        self.name=name
        self.pid =pid 
        self.command = command
        self.deadline = deadline
        self.date = date
        self.done = False

    def __str__(self):
        return str(self.uid) + \
               ', command -> ' + self.command + \
               ', deadline -> ' + self.deadline.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', date -> ' + self.date.strftime('%Y/%m/%d - %H:%M:%S') + \
               ', done -> ' + str(self.done)

               #', result -> ' + self.result + \
