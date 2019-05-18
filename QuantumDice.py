from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, IBMQ, execute
from qiskit.providers.aer import noise
from qiskit.providers.aer.noise import NoiseModel
from random import shuffle
import pygame as pg
import math
import time

runOnQuantumComputer=False

def QuantumDice():

    # begin with importing essential libraries for IBM Q
    from qiskit import IBMQ, BasicAer, Aer, execute
    from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit

    dice = 5
    # set up Quantum Register and Classical Register for 3 qubits
    q = QuantumRegister(dice)
    c = ClassicalRegister(dice)
    # Create a Quantum Circuit
    qc = QuantumCircuit(q, c)

    for j in range(dice):
        qc.h(q[j])

    qc.measure(q, c)

    if runOnQuantumComputer:
        try:
            pass
            # Obtain an available quantum computer
            ibmq_backends = IBMQ.backends()

            # define the least busy device
            from qiskit.providers.ibmq import least_busy
            from qiskit.tools.monitor import job_monitor, backend_monitor, backend_overview

            backend_overview()
            backend = least_busy(IBMQ.backends(simulator=False))
            #print("The least busy device:",backend.name())
            #backend_monitor(backend)

            #print("Running on device: ", backend)

            # Compile and execute the Quantum circuit on the quantum computer
            job_exp = execute(qc, backend, shots=1024, max_credits=10)
            result_exp = job_exp.result()

            # Render the output in the notebook user interface
            #print("experiment: ", result_exp)
            result_counts = result_exp.get_counts(qc)

        except:
            #print("All devices are currently unavailable, running locally on the simulator.")
            # Use Aer's qasm_simulator
            backend_sim = Aer.get_backend('qasm_simulator')

            # Execute the circuit on the qasm simulator.
            # We've set the number of repeats of the circuit
            # to be 1024, which is the default.
            job_sim = execute(qc, backend_sim, shots=1)

            # Grab the results from the job.
            result_sim = job_sim.result()
            #print("simulation: ", result_sim)
            result_counts = result_sim.get_counts(qc)
    else:
            #same as except above
            backend_sim = Aer.get_backend('qasm_simulator')
            job_sim = execute(qc, backend_sim, shots=1)
            result_sim = job_sim.result()
            result_counts = result_sim.get_counts(qc)


    def convert(list):

    # Converting integer list to string list
    # and joining the list using join()
        res = int("".join(map(str, list)),2)

        return res

    import operator
    result_counts_max = max(result_counts.items(), key=operator.itemgetter(1))[0]
    answer = convert(result_counts_max);
    
    return answer

from qiskit import IBMQ

def GetRandom():
    for j in range(1):
        while True:
            ans=QuantumDice()
            if ans > 19:
                continue
            else:
                return(ans)
                break

IBMQ.enable_account('ADD YOUR KEY')

pg.init()
pg.display.set_caption('Quantum Dice')
screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

COLOR_BLACK = pg.Color('black')
COLOR_BLUE = pg.Color('blue')
COLOR_ORANGE = pg.Color('orange')
COLOR_RED = pg.Color('red')
COLOR_GRAY = pg.Color('gray')

clock = pg.time.Clock()
pg.display.init()

DICE_NUMBERS = [pg.mixer.Sound('Audio/1.ogg'),
pg.mixer.Sound('Audio/2.ogg'),
pg.mixer.Sound('Audio/3.ogg'),
pg.mixer.Sound('Audio/4.ogg'),
pg.mixer.Sound('Audio/5.ogg'),
pg.mixer.Sound('Audio/6.ogg'),
pg.mixer.Sound('Audio/7.ogg'),
pg.mixer.Sound('Audio/8.ogg'),
pg.mixer.Sound('Audio/9.ogg'),
pg.mixer.Sound('Audio/10.ogg'),
pg.mixer.Sound('Audio/11.ogg'),
pg.mixer.Sound('Audio/12.ogg'),
pg.mixer.Sound('Audio/13.ogg'),
pg.mixer.Sound('Audio/14.ogg'),
pg.mixer.Sound('Audio/15.ogg'),
pg.mixer.Sound('Audio/16.ogg'),
pg.mixer.Sound('Audio/17.ogg'),
pg.mixer.Sound('Audio/18.ogg'),
pg.mixer.Sound('Audio/19.ogg'),
pg.mixer.Sound('Audio/20.ogg')]
pg.mixer.music.load('Audio/Loading.ogg')

x=0.0
y=0.0
prevX=0.0
prevY=0.0
getTicksLastFrame=0.0
t=0.0
generateNew=True
newNumberTimer=0.0
minWaitTime=1
framesSameNumerPresent=0
waitFrames=75

run=True
while run:

    if runOnQuantumComputer:
        screen.fill(COLOR_BLACK)
    else:
        screen.fill(COLOR_GRAY)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            if event.key == pg.K_q:
                runOnQuantumComputer = not runOnQuantumComputer

        if event.type == pg.MOUSEMOTION:
            x = pg.mouse.get_pos()[0]
            y = pg.mouse.get_pos()[1]

    t = pg.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    if newNumberTimer > minWaitTime:
        if x==prevX:
            if y==prevY:
                framesSameNumerPresent+=1
                if framesSameNumerPresent <= waitFrames:
                    print(framesSameNumerPresent)
                    screen.fill(COLOR_ORANGE)
                if framesSameNumerPresent >= waitFrames and generateNew:
                    generateNew=False
                    print("Generate new random number")
                    screen.fill(COLOR_BLUE)
                    pg.display.flip()
                    if runOnQuantumComputer:
                        pg.mixer.music.play(-1)
                    randonNumber=GetRandom()
                    if runOnQuantumComputer:
                        pg.mixer.music.stop()
                        time.sleep(2)
                    print(randonNumber)
                    DICE_NUMBERS[randonNumber].play()
                    newNumberTimer=0
            else:
                if generateNew==False:
                    print("Reset")
                generateNew=True
                framesSameNumerPresent=0
        else:
            if generateNew==False:
                print("Reset")
            generateNew=True
            framesSameNumerPresent=0
    else:
        newNumberTimer += deltaTime
    
    prevX = x
    prevY = y
    
    pg.display.flip()
    clock.tick(60)

screen.fill(COLOR_RED)
pg.display.flip()
print("Quit")
pg.quit()
