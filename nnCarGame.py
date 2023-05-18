import pygame
import random
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from classes.car import Car
from constants.colors import white
from mapGen import generateRandomMap

pygame.init()
img = 0
size = width, height = 1600, 900

generation = 1
mutationRate = 90
FPS = 30
selectedCars = []
selected = 0
lines = True  # If true then lines of player are shown
player = True  # If true then player is shown
display_info = True
frames = 0
number_track = 1

white_small_car = pygame.image.load("Images/Sprites/white_small.png")
white_big_car = pygame.image.load("Images/Sprites/white_big.png")
green_small_car = pygame.image.load("Images/Sprites/green_small.png")
green_big_car = pygame.image.load("Images/Sprites/green_big.png")

bg = pygame.image.load("bg7.png")
bg4 = pygame.image.load("bg4.png")


def mutateOneWeightGene(parent1, child1):
    sizenn = len(child1.sizes)

    # Copy parent weights into child weights
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]

    # Copy parent biases into child biases
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            child1.biases[i][j] = parent1.biases[i][j]

    genomeWeights = (
        []
    )  # This will be a list containing all weights, easier to modify this way

    for i in range(sizenn - 1):  # i=0,1
        for j in range(child1.sizes[i] * child1.sizes[i + 1]):
            genomeWeights.append(child1.weights[i].item(j))

    # Modify a random gene by a random amount
    r1 = random.randint(0, len(genomeWeights) - 1)
    genomeWeights[r1] = genomeWeights[r1] * random.uniform(0.8, 1.2)

    count = 0
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = genomeWeights[count]
                count += 1
    return


def mutateOneBiasesGene(parent1, child1):
    sizenn = len(child1.sizes)

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            child1.biases[i][j] = parent1.biases[i][j]

    genomeBiases = []

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            genomeBiases.append(child1.biases[i].item(j))

    r1 = random.randint(0, len(genomeBiases) - 1)
    genomeBiases[r1] = genomeBiases[r1] * random.uniform(0.8, 1.2)

    count = 0
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            child1.biases[i][j] = genomeBiases[count]
            count += 1
    return


def uniformCrossOverWeights(
    parent1, parent2, child1, child2
):  # Given two parent car objects, it modifies the children car objects weights
    sizenn = len(child1.sizes)  # 3 si car1=Car([2, 4, 3])

    # Copy parent weights into child weights
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child2.weights[i][j][k] = parent2.weights[i][j][k]

    # Copy parent biases into child biases
    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            child1.biases[i][j] = parent1.biases[i][j]

    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            child2.biases[i][j] = parent2.biases[i][j]

    genome1 = []  # This will be a list containing all weights of child1
    genome2 = []  # This will be a list containing all weights of child2

    for i in range(sizenn - 1):  # i=0,1
        for j in range(child1.sizes[i] * child1.sizes[i + 1]):
            genome1.append(child1.weights[i].item(j))

    for i in range(sizenn - 1):  # i=0,1
        for j in range(child2.sizes[i] * child2.sizes[i + 1]):
            genome2.append(child2.weights[i].item(j))

    # Crossover weights
    alter = True
    for i in range(len(genome1)):
        if alter == True:
            aux = genome1[i]
            genome1[i] = genome2[i]
            genome2[i] = aux
            alter = False
        else:
            alter = True

    # Go back from genome list to weights numpy array on child object
    count = 0
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = genome1[count]
                count += 1

    count = 0
    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            for k in range(child2.sizes[i]):
                child2.weights[i][j][k] = genome2[count]
                count += 1
    return


def uniformCrossOverBiases(
    parent1, parent2, child1, child2
):  # Given two parent car objects, it modifies the children car objects biases
    sizenn = len(parent1.sizes)

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            for k in range(child1.sizes[i]):
                child2.weights[i][j][k] = parent2.weights[i][j][k]

    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            child1.biases[i][j] = parent1.biases[i][j]

    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            child2.biases[i][j] = parent2.biases[i][j]

    genome1 = []
    genome2 = []

    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            genome1.append(child1.biases[i].item(j))

    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            genome2.append(child2.biases[i].item(j))

    alter = True
    for i in range(len(genome1)):
        if alter == True:
            aux = genome1[i]
            genome1[i] = genome2[i]
            genome2[i] = aux
            alter = False
        else:
            alter = True

    count = 0
    for i in range(sizenn - 1):
        for j in range(child1.sizes[i + 1]):
            child1.biases[i][j] = genome1[count]
            count += 1

    count = 0
    for i in range(sizenn - 1):
        for j in range(child2.sizes[i + 1]):
            child2.biases[i][j] = genome2[count]
            count += 1
    return


nnCars = []  # List of neural network cars
num_of_nnCars = 50  # Number of neural network cars
alive = num_of_nnCars  # Number of not collided (alive) cars
collidedCars = []  # List containing collided cars

# These is just the text being displayed on pygame window
infoX = 1365
infoY = 600
font = pygame.font.Font("freesansbold.ttf", 18)
text1 = font.render("0..9 - Change Mutation", True, white)
text2 = font.render("LMB - Select/Unselect", True, white)
text3 = font.render("RMB - Delete", True, white)
text4 = font.render("L - Show/Hide Lines", True, white)
text5 = font.render("R - Reset", True, white)
text6 = font.render("B - Breed", True, white)
text7 = font.render("C - Clean", True, white)
text8 = font.render("N - Next Track", True, white)
text9 = font.render("A - Toggle Player", True, white)
text10 = font.render("D - Toggle Info", True, white)
text11 = font.render("M - Breed and Next Track", True, white)
text1Rect = text1.get_rect().move(infoX, infoY)
text2Rect = text2.get_rect().move(infoX, infoY + text1Rect.height)
text3Rect = text3.get_rect().move(infoX, infoY + 2 * text1Rect.height)
text4Rect = text4.get_rect().move(infoX, infoY + 3 * text1Rect.height)
text5Rect = text5.get_rect().move(infoX, infoY + 4 * text1Rect.height)
text6Rect = text6.get_rect().move(infoX, infoY + 5 * text1Rect.height)
text7Rect = text7.get_rect().move(infoX, infoY + 6 * text1Rect.height)
text8Rect = text8.get_rect().move(infoX, infoY + 7 * text1Rect.height)
text9Rect = text9.get_rect().move(infoX, infoY + 8 * text1Rect.height)
text10Rect = text10.get_rect().move(infoX, infoY + 9 * text1Rect.height)
text11Rect = text11.get_rect().move(infoX, infoY + 10 * text1Rect.height)


def displayTexts():
    infotextX = 20
    infotextY = 600
    infotext1 = font.render("Gen " + str(generation), True, white)
    infotext2 = font.render("Cars: " + str(num_of_nnCars), True, white)
    infotext3 = font.render("Alive: " + str(alive), True, white)
    infotext4 = font.render("Selected: " + str(selected), True, white)
    if lines == True:
        infotext5 = font.render("Lines ON", True, white)
    else:
        infotext5 = font.render("Lines OFF", True, white)
    if player == True:
        infotext6 = font.render("Player ON", True, white)
    else:
        infotext6 = font.render("Player OFF", True, white)
    # infotext7 = font.render('Mutation: '+ str(2*mutationRate), True, white)
    # infotext8 = font.render('Frames: ' + str(frames), True, white)
    infotext9 = font.render("FPS: 30", True, white)
    infotext1Rect = infotext1.get_rect().move(infotextX, infotextY)
    infotext2Rect = infotext2.get_rect().move(
        infotextX, infotextY + infotext1Rect.height
    )
    infotext3Rect = infotext3.get_rect().move(
        infotextX, infotextY + 2 * infotext1Rect.height
    )
    infotext4Rect = infotext4.get_rect().move(
        infotextX, infotextY + 3 * infotext1Rect.height
    )
    infotext5Rect = infotext5.get_rect().move(
        infotextX, infotextY + 4 * infotext1Rect.height
    )
    infotext6Rect = infotext6.get_rect().move(
        infotextX, infotextY + 5 * infotext1Rect.height
    )
    # infotext7Rect = infotext7.get_rect().move(infotextX,infotextY+6*infotext1Rect.height)
    # infotext8Rect = infotext8.get_rect().move(infotextX,infotextY+7*infotext1Rect.height)
    infotext9Rect = infotext9.get_rect().move(
        infotextX, infotextY + 6 * infotext1Rect.height
    )

    gameDisplay.blit(text1, text1Rect)
    gameDisplay.blit(text2, text2Rect)
    gameDisplay.blit(text3, text3Rect)
    gameDisplay.blit(text4, text4Rect)
    gameDisplay.blit(text5, text5Rect)
    gameDisplay.blit(text6, text6Rect)
    gameDisplay.blit(text7, text7Rect)
    gameDisplay.blit(text8, text8Rect)
    gameDisplay.blit(text9, text9Rect)
    gameDisplay.blit(text10, text10Rect)
    gameDisplay.blit(text11, text11Rect)

    gameDisplay.blit(infotext1, infotext1Rect)
    gameDisplay.blit(infotext2, infotext2Rect)
    gameDisplay.blit(infotext3, infotext3Rect)
    gameDisplay.blit(infotext4, infotext4Rect)
    gameDisplay.blit(infotext5, infotext5Rect)
    gameDisplay.blit(infotext6, infotext6Rect)
    # gameDisplay.blit(infotext7, infotext7Rect)
    # gameDisplay.blit(infotext8, infotext8Rect)
    gameDisplay.blit(infotext9, infotext9Rect)
    return


gameDisplay = pygame.display.set_mode(size)  # creates screen
clock = pygame.time.Clock()

inputLayer = 6
hiddenLayer = 6
outputLayer = 4
car = Car([inputLayer, hiddenLayer, outputLayer])
auxcar = Car([inputLayer, hiddenLayer, outputLayer])

for i in range(num_of_nnCars):
    nnCars.append(Car([inputLayer, hiddenLayer, outputLayer]))


def redrawGameWindow():  # Called on very frame
    global alive
    global frames
    global img

    frames += 1

    gameD = gameDisplay.blit(bg, (0, 0))

    # NN cars
    for nncar in nnCars:
        if not nncar.collided:
            nncar.update()  # Update: Every car center coord, corners, directions, collision points and collision distances

        if nncar.collision():  # Check which car collided
            nncar.collided = True  # If collided then change collided attribute to true
            if nncar.yaReste == False:
                alive -= 1
                nncar.yaReste = True

        else:  # If not collided then feedforward the input and take an action
            nncar.feedforward()
            nncar.takeAction()
        nncar.draw(gameDisplay)

    # Same but for player
    if player:
        car.update()
        if car.collision():
            car.resetPosition()
            car.update()
        car.draw(gameDisplay)
    if display_info:
        displayTexts()
    pygame.display.update()  # updates the screen
    # Take a screenshot of every frame
    # pygame.image.save(gameDisplay, "pygameVideo/screenshot" + str(img) + ".jpeg")
    # img += 1


while True:
    # now1 = time.time()

    for event in pygame.event.get():  # Check for events
        if event.type == pygame.QUIT:
            pygame.quit()  # quits
            quit()

        if event.type == pygame.KEYDOWN:  # If user uses the keyboard
            if event.key == ord("l"):  # If that key is l
                car.showLines()
                lines = not lines
            if event.key == ord("c"):  # If that key is c
                for nncar in nnCars:
                    if nncar.collided == True:
                        nnCars.remove(nncar)
                        if nncar.yaReste == False:
                            alive -= 1
            if event.key == ord("a"):  # If that key is a
                player = not player
            if event.key == ord("d"):  # If that key is d
                display_info = not display_info
            if event.key == ord("n"):  # If that key is n
                number_track = 2
                for nncar in nnCars:
                    nncar.velocity = 0
                    nncar.acceleration = 0
                    nncar.x = 140
                    nncar.y = 610
                    nncar.angle = 180
                    nncar.collided = False
                generateRandomMap(gameDisplay)
                bg = pygame.image.load("randomGeneratedTrackFront.png")
                bg4 = pygame.image.load("randomGeneratedTrackBack.png")

            if event.key == ord("b"):
                if len(selectedCars) == 2:
                    for nncar in nnCars:
                        nncar.score = 0

                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    nnCars.clear()

                    for i in range(num_of_nnCars):
                        nnCars.append(Car([inputLayer, hiddenLayer, outputLayer]))

                    for i in range(0, num_of_nnCars - 2, 2):
                        uniformCrossOverWeights(
                            selectedCars[0], selectedCars[1], nnCars[i], nnCars[i + 1]
                        )
                        uniformCrossOverBiases(
                            selectedCars[0], selectedCars[1], nnCars[i], nnCars[i + 1]
                        )

                    nnCars[num_of_nnCars - 2] = selectedCars[0]
                    nnCars[num_of_nnCars - 1] = selectedCars[1]

                    nnCars[num_of_nnCars - 2].car_image = green_small_car
                    nnCars[num_of_nnCars - 1].car_image = green_small_car

                    nnCars[num_of_nnCars - 2].resetPosition()
                    nnCars[num_of_nnCars - 1].resetPosition()

                    nnCars[num_of_nnCars - 2].collided = False
                    nnCars[num_of_nnCars - 1].collided = False

                    for i in range(num_of_nnCars - 2):
                        for j in range(mutationRate):
                            mutateOneWeightGene(nnCars[i], auxcar)
                            mutateOneWeightGene(auxcar, nnCars[i])
                            mutateOneBiasesGene(nnCars[i], auxcar)
                            mutateOneBiasesGene(auxcar, nnCars[i])
                    if number_track != 1:
                        for nncar in nnCars:
                            nncar.x = 140
                            nncar.y = 610

                    selectedCars.clear()

            if event.key == ord("m"):
                if len(selectedCars) == 2:
                    for nncar in nnCars:
                        nncar.score = 0

                    alive = num_of_nnCars
                    generation += 1
                    selected = 0
                    nnCars.clear()

                    for i in range(num_of_nnCars):
                        nnCars.append(Car([inputLayer, hiddenLayer, outputLayer]))

                    for i in range(0, num_of_nnCars - 2, 2):
                        uniformCrossOverWeights(
                            selectedCars[0], selectedCars[1], nnCars[i], nnCars[i + 1]
                        )
                        uniformCrossOverBiases(
                            selectedCars[0], selectedCars[1], nnCars[i], nnCars[i + 1]
                        )

                    nnCars[num_of_nnCars - 2] = selectedCars[0]
                    nnCars[num_of_nnCars - 1] = selectedCars[1]

                    nnCars[num_of_nnCars - 2].car_image = green_small_car
                    nnCars[num_of_nnCars - 1].car_image = green_small_car

                    nnCars[num_of_nnCars - 2].resetPosition()
                    nnCars[num_of_nnCars - 1].resetPosition()

                    nnCars[num_of_nnCars - 2].collided = False
                    nnCars[num_of_nnCars - 1].collided = False

                    for i in range(num_of_nnCars - 2):
                        for j in range(mutationRate):
                            mutateOneWeightGene(nnCars[i], auxcar)
                            mutateOneWeightGene(auxcar, nnCars[i])
                            mutateOneBiasesGene(nnCars[i], auxcar)
                            mutateOneBiasesGene(auxcar, nnCars[i])

                    for nncar in nnCars:
                        nncar.x = 140
                        nncar.y = 610

                    selectedCars.clear()

                    number_track = 2
                    for nncar in nnCars:
                        nncar.velocity = 0
                        nncar.acceleration = 0
                        nncar.x = 140
                        nncar.y = 610
                        nncar.angle = 180
                        nncar.collided = False
                    generateRandomMap(gameDisplay)
                    bg = pygame.image.load("randomGeneratedTrackFront.png")
                    bg4 = pygame.image.load("randomGeneratedTrackBack.png")
            if event.key == ord("r"):
                generation = 1
                alive = num_of_nnCars
                nnCars.clear()
                selectedCars.clear()
                for i in range(num_of_nnCars):
                    nnCars.append(Car([inputLayer, hiddenLayer, outputLayer]))
                for nncar in nnCars:
                    if number_track == 1:
                        nncar.x = 120
                        nncar.y = 480
                    elif number_track == 2:
                        nncar.x = 100
                        nncar.y = 300
            if event.key == ord("0"):
                mutationRate = 0
            if event.key == ord("1"):
                mutationRate = 10
            if event.key == ord("2"):
                mutationRate = 20
            if event.key == ord("3"):
                mutationRate = 30
            if event.key == ord("4"):
                mutationRate = 40
            if event.key == ord("5"):
                mutationRate = 50
            if event.key == ord("6"):
                mutationRate = 60
            if event.key == ord("7"):
                mutationRate = 70
            if event.key == ord("8"):
                mutationRate = 80
            if event.key == ord("9"):
                mutationRate = 90

        if event.type == pygame.MOUSEBUTTONDOWN:
            # This returns a tuple:
            # (leftclick, middleclick, rightclick)
            # Each one is a boolean integer representing button up/down.
            mouses = pygame.mouse.get_pressed()
            if mouses[0]:
                pos = pygame.mouse.get_pos()
                point = Point(pos[0], pos[1])
                # Revisar la lista de autos y ver cual estaba ahi
                for nncar in nnCars:
                    polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
                    if polygon.contains(point):
                        if nncar in selectedCars:
                            selectedCars.remove(nncar)
                            selected -= 1
                            if nncar.car_image == white_big_car:
                                nncar.car_image = white_small_car
                            if nncar.car_image == green_big_car:
                                nncar.car_image = green_small_car
                            if nncar.collided:
                                nncar.velocity = 0
                                nncar.acceleration = 0
                            nncar.update()
                        else:
                            if len(selectedCars) < 2:
                                selectedCars.append(nncar)
                                selected += 1
                                if nncar.car_image == white_small_car:
                                    nncar.car_image = white_big_car
                                if nncar.car_image == green_small_car:
                                    nncar.car_image = green_big_car
                                if nncar.collided:
                                    nncar.velocity = 0
                                    nncar.acceleration = 0
                                nncar.update()
                        break

            if mouses[2]:
                pos = pygame.mouse.get_pos()
                point = Point(pos[0], pos[1])
                for nncar in nnCars:
                    polygon = Polygon([nncar.a, nncar.b, nncar.c, nncar.d])
                    if polygon.contains(point):
                        if nncar not in selectedCars:
                            nnCars.remove(nncar)
                            alive -= 1
                        break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.rotate(-5)
    if keys[pygame.K_RIGHT]:
        car.rotate(5)
    if keys[pygame.K_UP]:
        car.set_accel(0.2)
    else:
        car.set_accel(0)
    if keys[pygame.K_DOWN]:
        car.set_accel(-0.2)

    redrawGameWindow()

    clock.tick(FPS)
