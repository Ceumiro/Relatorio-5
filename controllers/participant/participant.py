"""Sample Webots controller for the pick and place benchmark."""

from controller import Robot

# Create the Robot instance.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
print (timestep)

# Initialize base motors.
wheels = []
wheels.append(robot.getDevice("wheel1"))
wheels.append(robot.getDevice("wheel2"))
wheels.append(robot.getDevice("wheel3"))
wheels.append(robot.getDevice("wheel4"))
for wheel in wheels:
    # Activate controlling the motors setting the velocity.
    # Otherwise by default the motor expects to be controlled in force or position,
    # and setVelocity will set the maximum motor velocity instead of the target velocity.
    wheel.setPosition(float('+inf'))

# Initialize arm motors.
armMotors = []
armMotors.append(robot.getDevice("arm1"))
armMotors.append(robot.getDevice("arm2"))
armMotors.append(robot.getDevice("arm3"))
armMotors.append(robot.getDevice("arm4"))
armMotors.append(robot.getDevice("arm5"))
# Set the maximum motor velocity.
armMotors[0].setVelocity(0.2)
armMotors[1].setVelocity(0.5)
armMotors[2].setVelocity(0.5)
armMotors[3].setVelocity(0.3)

# Initialize arm position sensors.
# These sensors can be used to get the current joint position and monitor the joint movements.
armPositionSensors = []
armPositionSensors.append(robot.getDevice("arm1sensor"))
armPositionSensors.append(robot.getDevice("arm2sensor"))
armPositionSensors.append(robot.getDevice("arm3sensor"))
armPositionSensors.append(robot.getDevice("arm4sensor"))
armPositionSensors.append(robot.getDevice("arm5sensor"))
for sensor in armPositionSensors:
    sensor.enable(timestep)

# Initialize gripper motors.
finger1 = robot.getDevice("finger1")
finger2 = robot.getDevice("finger2")
# Set the maximum motor velocity.
finger1.setVelocity(0.05)
finger2.setVelocity(0.05)
# Read the minium and maximum position of the gripper motors.
fingerMinPosition = finger1.getMinPosition()
fingerMaxPosition = finger1.getMaxPosition()

#temporizador = angulo percorrido/omega
#angulo percorrido = 520*0.016*7 = 58.24 rad
#distancia percorrida = raio roda * angulo percorrido
#distancia percorrida = 0.05*58.24 = 2.912m
#https://github.com/cyberbotics/pick-and-place-competition/blob/main/controllers/participant/participant.py#L61
omega=7.0 #mudar este valor para os valores pedidos no enunciado
angulo_percorrido=2.912/0.05

temporizador = angulo_percorrido/omega
# Move forward.
for wheel in wheels:
    wheel.setVelocity(omega)
# Wait until the robot is in front of the box.
robot.step(int(temporizador*1000)+16)

# Stop moving forward.
for wheel in wheels:
    wheel.setVelocity(0.0)

# Move arm and open gripper.
armMotors[0].setPosition(0.05)
armMotors[1].setPosition(-0.55)
armMotors[2].setPosition(-0.9)
armMotors[3].setPosition(-1.5)
finger1.setPosition(fingerMaxPosition)
finger2.setPosition(fingerMaxPosition)

# Controlo em malha fechada, utilizando o sensor de posição do angulo do motor
delta_angulo = 0.25
while robot.step(timestep) != -1:
    if abs(armPositionSensors[3].getValue() - (-1.5)) < delta_angulo:
        # Motion completed.
        break

# Close gripper.
finger1.setPosition(0.013)
finger2.setPosition(0.013)
# Wait until the gripper is closed.
robot.step(50 * timestep)

# Lift arm.
armMotors[1].setPosition(0)
# Wait until the arm is lifted.
robot.step(200 * timestep)

# Rotate the robot.
#temporizador = 690*.016= 11.04seg
#angulo rotacao = omega * temporizador
#angulo rotacao = 2.5*11.04 = 27.6 radianos
#https://github.com/cyberbotics/pick-and-place-competition/blob/main/controllers/participant/participant.py#L97

omega_rot = 7
temporizador_rot = 27.5/omega_rot
wheels[0].setVelocity(omega_rot)
wheels[1].setVelocity(-omega_rot)
wheels[2].setVelocity(omega_rot)
wheels[3].setVelocity(-omega_rot)
# Wait for a fixed amount to step that the robot rotates.
robot.step(int(temporizador_rot*1000))

for wheel in wheels:
    wheel.setVelocity(0.0)
#andar para a frente
#temporizador = angulo percorrido/omega
#angulo percorrido = 900*0.016*2.5 = 36 rad
#distancia percorrida = raio roda * angulo percorrido
#distancia percorrida = 0.05*36 = 1.8m
# Move forward.
omega=2.5
angulo_percorrido=1.8/0.05
temporizador = angulo_percorrido/omega
wheels[0].setVelocity(omega)
wheels[1].setVelocity(omega)
wheels[3].setVelocity(omega)
wheels[2].setVelocity(omega)
robot.step(int(temporizador*1000))

# Rotate the robot.
wheels[0].setVelocity(1.0)
wheels[1].setVelocity(-1.0)
wheels[2].setVelocity(1.0)
wheels[3].setVelocity(-1.0)
robot.step(200 * timestep)

# Move forward.
wheels[1].setVelocity(1.0)
wheels[3].setVelocity(1.0)
robot.step(300 * timestep)

# Rotate the robot.
wheels[0].setVelocity(1.0)
wheels[1].setVelocity(-1.0)
wheels[2].setVelocity(1.0)
wheels[3].setVelocity(-1.0)
robot.step(130 * timestep)

# Move forward.
wheels[1].setVelocity(1.0)
wheels[3].setVelocity(1.0)
robot.step(310 * timestep)

# Stop.
for wheel in wheels:
    wheel.setVelocity(0.0)

# Move arm down
armMotors[3].setPosition(0)
armMotors[2].setPosition(-0.3)
robot.step(200 * timestep)

armMotors[1].setPosition(-1.0)
robot.step(200 * timestep)
# Controle em malha fechada
armMotors[3].setPosition(-1.0)
delta_angulo = 0.25  # Tolerância para considerar a posição atingida
while robot.step(timestep) != -1:
    if abs(armPositionSensors[3].getValue() - (-1.0)) < delta_angulo:
        # Movimento concluído
        break
armMotors[2].setPosition(-0.4)
delta_angulo = 0.25  # Tolerância para considerar a posição atingida
while robot.step(timestep) != -1:
    if abs(armPositionSensors[2].getValue() - (-0.4)) < delta_angulo:
        # Movimento concluído
        break


# Open gripper.
finger1.setPosition(fingerMaxPosition)
finger2.setPosition(fingerMaxPosition)
robot.step(50 * timestep)

# Lift arm.
armMotors[1].setPosition(0)
# Wait until the arm is lifted.
robot.step(200 * timestep)
