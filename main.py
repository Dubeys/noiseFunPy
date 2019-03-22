import sys, pygame, noise, math, time, random

from lib.utilities.utils import *
from lib.objects.particles import *


size = width, height = int(1080 / 2.5), int(1080 / 2.5)
screen = pygame.display.set_mode(size)

screen.set_alpha(None)

pygame.init()

# seed = math.floor(random.random() * 10000)
seed = 312 #noiseScale movement 5 #noiseScale particles .02
print("seed: ",seed)
noiseScale = 5
# loopedNoise = loop(600, lambda x, y: (noise.pnoise2(x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5 )
# loopedNoiseLength = len(loopedNoise)

pygame.display.update()
perf = Performance()

targetFPS = 30
particles = []
maxDistance = 199 * 199
clusterCenter = width/2

delta_time = 0.000001
time = 0

noiseValue = loopValueAtTime(time/20, lambda x, y: (noise.pnoise2(
    x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)
noiseValueOffset = loopValueAtTime((time + 200)/20, lambda x, y: (noise.pnoise2(
    x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)

for i in range(2000): 
    rndradius = random.random()
    radius = math.sqrt(rndradius) * 200
    angle = random.random() * math.tau

    x = math.sin(angle) * radius + clusterCenter
    y = math.cos(angle) * radius + clusterCenter

    particles.append(Particle(x, y, 2, rnd=seed+1))
    particles[i].setRandomDir(scale=.01)


# def renderToImages(path):
#     alreadyRendered = False
#     time = 0
#     delta_time = 1 / 60
#     imageNameCounter = 0
#     while time / 20.0 < 1:
#         screen.fill((0, 0, 0))
#         counter = 0

#         noiseValue = loopValueAtTime(time/20, lambda x, y: (noise.pnoise2(x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)
#         noiseValueOffset = loopValueAtTime((time + 200)/20, lambda x, y: (noise.pnoise2(x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)

#         for part in particles:

#             unclampedNudge = mapPolar(noiseValueOffset) * 200
#             x, y = part.testNudge(unclampedNudge)
#             ox, oy = part.getPosition()
#             distanceToCenterAfter = ((x - clusterCenter) * (x - clusterCenter)) + ((y - clusterCenter) * (y - clusterCenter))
#             distanceToCenterBefore = ((ox - clusterCenter) * (ox - clusterCenter)) + ((oy - clusterCenter) * (oy - clusterCenter))
#             clampedNudge = unclampedNudge * clamp(1 - (distanceToCenterAfter / maxDistance), 0, 1) * clamp(1 - (distanceToCenterBefore / maxDistance), 0, 1)

#             part.setRandomDir(math.cos(noiseValueOffset * math.tau), .01 +mapLinear(math.cos(((time+seed) / 20) * math.tau)) * .015)
#             part.rotateDirection((time / 20) * math.tau)

#             part.nudge(clampedNudge, delta_time, noiseValue * -.2, not alreadyRendered)
#             # part.nudge(lerp(unclampedNudge, clampedNudge, 0))
#             counter += 1
#             part.draw(screen)

#         pygame.image.save(screen, './' + path + '/render_' + str(imageNameCounter).zfill(4) + '.png' )
#         alreadyRendered = True
#         time += delta_time
#         print(imageNameCounter)
#         imageNameCounter += 1
         

# renderToImages('renders/render1')

alreadyRendered = False
time = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0,0,0))

    elapsedTime = delta_time

    counter = 0
    angle = ((time / 20) % math.tau )
    lerpFactor = mapLinear(math.sin(angle))

    noiseValue = loopValueAtTime(time/20, lambda x, y: (noise.pnoise2(x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)
    noiseValueOffset = loopValueAtTime((time + 200)/20, lambda x, y: (noise.pnoise2(x*noiseScale, y*noiseScale, 5, 0.2, 1.5, 1024, 1024, seed) * .5) + .5)

    # print('-----------------------------------------------------------------------------------------------------------------------------')

    for part in particles:
        unclampedNudge = mapPolar(noiseValueOffset) * 200
        x, y = part.testNudge(unclampedNudge)
        ox, oy = part.getPosition()
        distanceToCenterAfter = ((x - clusterCenter) * (x - clusterCenter)) + ((y - clusterCenter) * (y - clusterCenter))
        distanceToCenterBefore = ((ox - clusterCenter) * (ox - clusterCenter)) + ((oy - clusterCenter) * (oy - clusterCenter))
        clampedNudge = unclampedNudge * clamp(1 - (distanceToCenterAfter / maxDistance), 0, 1) * clamp(1 - (distanceToCenterBefore / maxDistance), 0, 1)

        part.setRandomDir(math.cos(noiseValueOffset * math.tau), .01 + mapLinear(math.cos(((time+seed) / 20) * math.tau)) * .015)
        part.rotateDirection((time/ 20) * math.tau)

        part.nudge(clampedNudge, (elapsedTime / (1/targetFPS)), noiseValue * -.5, not alreadyRendered)
        # part.nudge(lerp(unclampedNudge, clampedNudge, 0))
        counter += 1
        part.draw(screen)
    
    if not alreadyRendered:
        alreadyRendered = True

    pygame.display.update()
    fps, delta_time, prev_time = perf.fpsLimiter(targetFPS)
    time += delta_time
    # pygame.display.set_caption("{0}: {1:.2f}".format("fps: ", fps))
