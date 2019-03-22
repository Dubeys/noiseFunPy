import time, math, colorsys

def vector2(x,y):
    return {"x": x, "y": y}


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def rotate(vecPoint, angle, vecOrigin=(0,0)):
    x,y = vecPoint
    ox, oy = vecOrigin

    qx = ox + math.cos(angle) * (x - ox) - math.sin(angle) * (y - oy)
    qy = oy + math.sin(angle) * (x - ox) + math.cos(angle) * (y - oy)
    return (qx, qy)

def lerp(a,b, factor = .5):
    return (a * factor) + (b * (1-factor))

def mapPolar(value):
    return value * 2 - 1

def mapLinear(value):
    return (value * .5) + .5

def bawColor(intensity, alpha = 255):
    baw = intensity * 255
    return (baw, baw, baw, alpha)

def clamp(value ,minimum, maximum): 
    if type(value) is tuple:
        return tuple(max(min(i, maximum),minimum) for i in value)
    return max(min(value, maximum),minimum)

def difference(new, old = []):
    diffs = []
    for x in range(len(new)):
        if new[x] != old[x]: 
            diffs.append((x, new[x]))
        
    return diffs


def loop(scale,callback):
    loopedNoise = []

    increment = 0
    loopingSteps = scale

    for i in range(loopingSteps):
        angle = (i / loopingSteps) * math.tau
        x = (math.sin(angle) + 1)
        y = (math.cos(angle) + 1)
        loopedNoise.append( callback(x,y) )

    return loopedNoise

def loopValueAtTime(phase, callback):
    angle = phase * math.tau
    x = (math.sin(angle) + 1)
    y = (math.cos(angle) + 1)
    return callback(x, y)

class Performance: 
    def __init__(self): 
        self.prev_time = time.time()

    def fpsLimiter(self,target_fps=60):
        curr_time = time.time()
        diff = curr_time - self.prev_time
        delay = max(1.0/target_fps - diff, 0)
        fps = 1.0/(delay + diff)
        self.prev_time = curr_time
        time.sleep(delay)
        return ( fps, delay + diff, self.prev_time )
