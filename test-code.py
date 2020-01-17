import numpy as np

gameDirectory = {
    1217: np.arange(1740201,1740218),
    1219: np.arange(1740219,1740245)
}

regno = 1740242

for gameid in gameDirectory:
    if regno in gameDirectory[gameid]:
        print(regno,'\ngameid:',gameid)
        break
    else:
        print('regno illa')