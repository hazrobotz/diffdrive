from openloopLTIplant import plant as dcmotor

def main(request):
    y = []
    output = dcmotor.main(request["motordata"])
    motoroutput = np.array(output["data"]["y"])
    translationalvelocity = motoroutput[:,[1,3]].mean(axis=1)
    angularvelocity = np.diff(motoroutput[:,[1,3]], axis=1)
    xx=np.array(request["x0"])+ 0.
    count = motoroutput.shape[0]

    y.append(xx.flatten().round(4).tolist()+[np.round(motoroutput[0, -1], 4)])
    hh = np.diff(motoroutput[:,-1])
    for i in range(1, count):
        xx[0] = xx[0] + request["r"] * translationalvelocity[i] * np.cos(xx[2])*hh[i-1]
        xx[1] = xx[1] + request["r"] * translationalvelocity[i] * np.sin(xx[2])*hh[i-1]
        xx[2] = xx[2] + request["r"]/request["b"] * angularvelocity[i]*hh[i-1]
        y.append(xx.flatten().tolist()+[np.round(motoroutput[i, -1], 4)])

    return {"data": {"y": y}}

if __name__ == "__main__":
    # Set model parameters
    R = 4.67  # ohm
    L = 170e-3  # H
    J = 42.6e-6  # Kg-m^2
    f = 47.3e-6  # N-m/rad/sec
    K = 14.7e-3  # N-m/A
    Kb = 14.7e-3  # V-sec/rad
    testdata = {
        "u": [[ 5 ,  5. ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5 ,  5 ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 2. ,  -2. ],
       [ 2,  -2],
       [ 2,  -2],
       [ 2,  -2],
       [ 5 ,  5. ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5 ,  5 ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 2. ,  -2. ],
       [ 2,  -2],
       [ 2,  -2],
       [ 2,  -2],
       [ 5 ,  5. ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5 ,  5 ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 2. ,  -2. ],
       [ 2,  -2],
       [ 2,  -2],
       [ 2,  -2],
       [ 5 ,  5. ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5 ,  5 ],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 5,  5],
       [ 2. ,  -2. ],
       [ 2,  -2],
       [ 2,  -2],
       [ 2,  -2]],
        "x0": [[0], [0], [0], [0], [0], [0]],
        "A": [[0, 1, 0, 0, 0, 0], [0, -f/J, K/J, 0, 0, 0], [0, -K/L, -R/L, 0, 0, 0], 
        [0, 0, 0, 0, 1, 0], [0, 0, 0,0, -f/J, K/J], [0, 0, 0,0, -K/L, -R/L]],
        "B": [[0, 0], [0, 0], [1/L, 0], [0, 0], [0, 0], [0,1/L]],
        "C": [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0]],
        "D": [[0, 0], [0, 0], [0, 0], [0, 0]],
        "h": 0.02,
        "T": 5
    }

    testdata2 = {
        "x0":[0,0,0],
        "r": .3,
        "b": 1,
        "motordata": testdata
    }

    main(testdata2)
