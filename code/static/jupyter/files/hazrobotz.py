import requests
import dataclasses
from datetime import datetime
from time import sleep

@dataclasses.dataclass
class state:
    x: float
    y: float
    theta: float

def get_state(idx):
    data=requests.get(f"http://127.0.0.1:8080/{idx}/state")
    if data.status_code == 200:
        x,y,theta = map(float, data.text.split())
        return state(x,y,theta)

def get_target(idx):
    data=requests.get(f"http://127.0.0.1:8080/{idx}/target")
    if data.status_code == 200:
        x,y,theta = map(float, data.text.split())
        return state(x,y,theta)

def get_objects(idx):
    data=requests.get(f"http://127.0.0.1:8080/{idx}/object-detection")
    if data.status_code == 200:
        return data.json()

def _move(idx, left, right):
    t = datetime.now().timestamp()
    data=requests.get(f"http://127.0.0.1:8080/{idx}/u?value0={left}&value1={right}&t={t}")
    if data.status_code == 200:
        x,y,theta = map(float, data.text.split())
        return state(x,y,theta)

def move_forward(idx):
    return _move(idx,1,1)

def turn_right(idx):
    return _move(idx,1,-1)

def turn_left(idx):
    return _move(idx,-1,1)

def stop(idx):
    return _move(idx,0,0)

