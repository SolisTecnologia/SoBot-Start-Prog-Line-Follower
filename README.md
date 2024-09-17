# SoBot-Start-Prog-Line-Follower
# Solis Robot - SoBot
![](https://github.com/SolisTecnologia/SoBot-Start-Prog-Line-Follower/tree/master/png/SoBotSingleLF.png)
# Introduction

AMR (autonomous mobile robotics) platform equipped with a camera system, ultrasonic and photoelectric sensors, works with a high rate of precision and repeatability of its movements, as it uses stepper motors in its movement and navigation, the SoBot also can be termed as a research and development interface, as it facilitates the practical experimentation of algorithms from the simplest to the most complex level.

This product was developed 100% by Solis Tecnologia, and has a lot of technology employing cutting-edge concepts, such as:

The motors can be controlled simultaneously or individually.
The user can select different accessories to implement to the robot.
Several programming languages can be used to connect via API.

# Components

* Main structure in aluminum
* Robot Control Driver
* Raspberry Pi 4B board <img align="center" height="30" width="40" src="https://github.com/devicons/devicon/blob/master/icons/raspberrypi/raspberrypi-original.svg">
* 2x NEMA-23 Stepper Motors
* 2x 12V/5A battery
* Wireless Gamepad F710  <img align="center" height="40" width="40" src="https://github.com/SolisTecnologia/SoBot-Basic-Control-Logitech-F710/blob/main/png/control.png">

# Programming Example
## Line Follower - [Start_prog_SL.py](https://github.com/SolisTecnologia/SoBot-Start-Prog-Line-Follower/blob/master/Start_prog_SL.py)

Programming example to control "SoBot" using the Logitech F710 controller and enable line follower mode.

This code implements a remote control for the "SoBot", using the Logitech controller to perform functions such as moving, adjusting speed and changing LED colors. It uses serial communication to send commands to the robot and is able to read and react to line sensors to allow the robot to follow a track automatically when enabled by the controller.

Controller button functions:
BTN_X – Configure LED Strip in Blue color
BTN_Y – Configure LED Strip in Yellow color
BTN_A – Configure LED Strip in Green color
BTN_B – Configure LED Strip in Red color
BTN_START – Enables wheel motors
BTN_BACK – Enable and Disables line follower mode
BTN_R1 – Configure curve mode on the same axis
BTN_L1 – Configure differential curve mode
BTN_R2 – Sets speed 8cm/s
BTN_L2 – Sets speed 4cm/s
BTN_UP – Moves the robot forward
BTN_DOWN – Moves the robot backwards
BTN_LEFT – Moves the robot to the left
BTN_RIGTH – Moves the robot to the right


### Main Functions:

**Read_Gamepad:** This function reads the inputs from the Logitech controller and maps the button actions to the corresponding functions of the robot. This includes movement, speed control, LED activation, among others.
**Read_Line:** Function that controls the robot based on the line sensor data, allowing the robot to follow lines on the floor. The robot adjusts its direction based on this data, moving forward or correcting the trajectory to the left or right.


### Programming Principles Involved:

**Concurrency:** The code uses the **"multiprocessing"** library to execute parallel tasks, such as reading events from the controller and reading line sensors, ensuring that both can happen at the same time.

**Timers and Events:** Timers and flags are used to determine the robot's behavior and respond to controller inputs in a non-blocking manner.


For more information about the commands used, check the Robot Commands Reference Guide.



# Reference Link
[SolisTecnologia website](https://solistecnologia.com/produtos/robotsingle)

# Please Contact Us
If you have any problem when using our robot after checking this tutorial, please contact us.

### Phone:
+55 1143040786

### Technical support email: 
contato@solistecnologia.com.br

![](https://github.com/SolisTecnologia/SoBot-Line-Follower/blob/master/png/logo.png)