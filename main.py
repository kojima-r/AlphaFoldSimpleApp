from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import lib.db as db
from lib.models import Task
import datetime

import sys

import werkzeug
import subprocess
import glob
import json
import hashlib
import random, string
import os
import psutil

import subprocess
import asyncio
from subprocess import PIPE

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

def calculate_key(filename):
    text=(filename+randomname(5)).encode('utf-8')
    result = hashlib.md5(text).hexdigest()
    saveFileName = werkzeug.utils.secure_filename(result)
    return saveFileName


app = FastAPI()
router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
class RunOption(BaseModel):
    q:str="abc"
DATA_DIR="/data1/AlphaFold/api/static/data"
LOG_DIR ="/data1/AlphaFold/api/static/log"
procs={}

@app.get("/")
async def read_root(request: Request):
    task = db.session.query(Task).filter(Task.valid == True).all()
    db.session.close()
    pid_list=[proc.pid for proc in psutil.process_iter()]
    pid_list=set(pid_list)
    for t in task:
        if int(t.pid) in pid_list:
            t.done=False
        else:
            t.done=True
    return templates.TemplateResponse('tasks.html',
                                      {'request': request,
                                       'task': task})
@app.post("/run")
async def read_run(request: Request):
    data = await request.form()
    q = data.get('q')
    ##
    q_list=[]
    for line in q.split("\n"):
        if len(line)>0 and line[0]!=">":
            q_list.append(line.strip())
    q="".join(q_list)
    ##
    fileName="file"
    uid=calculate_key(fileName)
    ###
    path=os.path.join(DATA_DIR, uid+".fasta")
    N=40
    with open(path,"w") as fp:
        fp.write(">")
        fp.write(uid)
        fp.write("\n")
        lq=q.upper()
        n_line=len(lq)//N
        for i in range(n_line):
            fp.write(q[i*N:(i+1)*N])
            fp.write("\n")
        fp.write(q[n_line*N:])
        fp.write("\n")
    ###
    cmd='sh run.sh '+path+" "+uid
    proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    pid=proc.pid
    ###
    task = Task(
        uid=uid,
        pid=str(pid),
        command=cmd,
        deadline=datetime.datetime.now()+datetime.timedelta(days=1)
    )
    db.session.add(task)
    db.session.commit()
    db.session.close()
    ###
    return {"q": q}


@app.get("/result/{task_uid}")
def read_item(task_uid: str,request: Request):
    task = db.session.query(Task).filter(Task.uid == task_uid).filter(Task.valid == True).all()
    db.session.close()
    #return {"task_id": task_uid, "q": str(task[0])}
    #
    return templates.TemplateResponse('result.html',
                                      {'request': request,
                                       'task': task[0]})
