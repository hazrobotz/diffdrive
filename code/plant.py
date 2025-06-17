# Licence?
import os
import atexit
import signal
import timeit
import warnings
from sys import exc_info
import numpy as np


def save():
    np.save("saved/state.npy", xx, allow_pickle=True)
    warnings.warn("Saving plant state")


atexit.register(save)

try:
    savedstate = np.load("saved/state.npy", ndmin=2)
except:
    savedstate = None

N = 1
try:
    if "NUM_PLANTS" in os.environ.keys():
        N = int(os.environ["NUM_PLANTS"])
        warnings.warn("Using %s plants" % N)
except:
    warnings.warn("Not able to access the number of plants to generate, using %s" % N)

h = 0.05
try:
    if "SAMPLE_PERIOD" in os.environ.keys():
        _h = float(os.environ["SAMPLE_PERIOD"])
        if 0 < _h < 2:
            h = _h
        else:
            raise ValueError("Requested duration %s is not acceptable", _h)

        warnings.warn("Using %s as sample period" % h)
except:
    warnings.warn("Not able to access the suggested sample period. Using %s" % h)
clock = timeit.default_timer

# Set model parameters
r_R = 0.075
r_L = 0.075
b = 0.3/2


# plant_state = [x, y, theta]
x = np.zeros((3, 1))
# plant_input= [phidot_r, phidot_l]
u = np.zeros((2, 1))

xx = np.tile(x, N)

t0 = clock()
t = 0
uu = np.tile(u, N)

if savedstate is not None and savedstate.shape == xx.shape and np.isreal(uu).all():
    xx = savedstate


def update(_, __):
    global xx, t
    try:
        theta = xx[2, :]
        new_t = clock() - t0

        left_wheel_vels = uu[0, :]
        right_wheel_vels = uu[1, :]


        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        dx_dt = (r_R / 2 * cos_theta * right_wheel_vels) + \
                (r_L / 2 * cos_theta * left_wheel_vels)

        dy_dt = (r_R / 2 * sin_theta * right_wheel_vels) + \
                (r_L / 2 * sin_theta * left_wheel_vels)

        dtheta_dt = (r_R / (2 * b) * right_wheel_vels) + \
                    (-r_L / (2 * b) * left_wheel_vels)



        d_xx_dt = np.stack([dx_dt, dy_dt, dtheta_dt], axis=0)
        xx = xx + (new_t-t) * d_xx_dt
        xx[2, :] = np.arctan2(np.sin(xx[2, :]), np.cos(xx[2, :]))
        t = new_t        
    except Exception as e:
        print(exc_info(), xx, uu, "in update")


def init(data, idx=0):
    global uu, xx, t0
    data = data.split("&")
    assert 0<=idx<N, "Invalid sub-system"
    try:
        x0 = float(data[0].split("=")[1])
        x1 = float(data[1].split("=")[1])
    except ValueError:
        x0 = 0
        x1 = 0
    uu[0, idx] = 0
    uu[1, idx] = 0
    xx[0, idx] = x0
    xx[1, idx] = x1
    t0 = clock()  # Time at which the controller called to initialize the plant
    return " ".join([str(i) for i in xx[:, idx]])

def state(idx=0):
    assert 0<=idx<N, "Invalid sub-system"
    return " ".join([str(i) for i in xx[:, idx]])

def control(controldata, idx=0):
    global uu
    data = controldata.split("&")
    assert 0<=idx<N, "Invalid sub-system"

    # we will assume that all the data are present value0, and time
    try:
        u0 = float(data[0].split("=")[1])
        u1 = float(data[1].split("=")[1])
        c_t = float(data[2].split("=")[1])
        uu[0, idx] = u0
        uu[1, idx] = u1
        retval = " ".join([str(i) for i in xx[:, idx]])
    except (ValueError, IndexError):
        warnings.warn("%s %s %s %s" % (exc_info(), idx, "couldn't update the plant", controldata))
        retval = ""
    return retval


# method that parses the request and sends to the appropriate handler
# needed for non web triggers
def interpret(whole_data, idx):
    assert 0<=idx<N, "Invalid sub-system"
    split_data = whole_data.split("]")
    last_complete_packet = split_data[len(split_data) - 2]
 
    query_string = last_complete_packet.split('?')
 
    datahandler = query_string[0].split('/')[-1]
 
    if datahandler == "init":
        return "["+init(query_string[1], idx)+"]"
    elif datahandler == "u":
        return "["+control(query_string[1], idx)+"]"
    elif datahandler == "state":
        return "["+state(idx)+"]"
    else:
        return "["+"NOT VALID"+"]"


signal.signal(signal.SIGALRM, update)
signal.setitimer(signal.ITIMER_REAL, h, h)

if __name__ == "__main__":
    while True:
        pass
