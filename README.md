# PEDRO People Detection Robot Operations


## Introduction

![PEDRO](https://github.com/dodisbeaver/PEDRO/blob/main/PEDRO.gif?raw=true)

This is the installation instructions for **PEDRO**, the **P**eople **D**etection **R**obot **O**perations robot. Pedro was the result of a project course at Arcada university of applied sciences. Our group effort created a robot that can navigate, detect persons and communicate with simple sentences with persons. 

The idea of the project was to have a robot that can be used in various environments where it is too dangerous for a human to go and search for people and communicate safely with them. We came up with the robot **PEDRO** that is a proof of concept that a robot can be used in such tasks.

The base for the robot the Turtlebot3 burger development kit. https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/


## Pre-installation Requirements

![PEDRO](https://github.com/dodisbeaver/PEDRO/blob/main/PEDRO1.jpeg?raw=true)

Here is the list of hardware that is necessary for PEDRO to work.
You are not required to print out a shell.

    Hardware: 
        1. A PC, preferably a laptop if you want to chase PEDRO
        2. A display with HDMI input.
        3. A keyboard.
        4. Turtlebot3 burger development kit
        5. Raspberry pi 3<
        6. MicroSD card 16<
        7. Webcamera.(The original PEDRO worked with a Microsoft Lifecam
            NX-6000 and was tested with other various cameras with failed and 
            successful results.)
        8. 3.5mm speaker in a small form factor.
      

## Installation instructions and steps

The first thing to do is to remember to source the environment if something does not work. Remember to use the environment variables! ROS is very particular about environment variables. Another gotcha is that ubuntu does not make a swapfile. So following the turtlebot3 instructions for ubuntu 22.04 will fail very early if not done manually. It is also important to use the Humble tab in the e-manual on robotis. 

### Host PC
Follow the instrucions https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup for installation of the host PC on your computer that will work as the bridge between you and the robot. Remember to source. 

### Raspberry Pi
Next up is the SBC or in laymans terms the Raspberry Pi. https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup
My opinion is that it is easiest to install the imager mentioned in the manual on the computer that you have set up. 

A problem I had was with the ip address of the raspberry pi. I used a tool called nmap to search for it but this is a tool that should be used with care and only on your home network. Hopefully you have access to the admin panel of your router.

Follow the manual up until point 13. This is where a raspberry pi 3 will not work according to the manual, I have not tested with a newer raspberry pi but I suspect the issue is the same. This is an issue thread in the Turtlebot3 repository that solved my problems. https://github.com/ROBOTIS-GIT/turtlebot3/issues/965
In the ssh session you have started according to the tutorial se the command:

    sudo swapon --show

to check if you have a swapfile. This should not show any output.

Check how much space you have left on your sd card with:

    free -h

this will show something similar to 

    Output
    Filesystem      Size  Used Avail Use% Mounted on
    udev            474M     0  474M   0% /dev
    tmpfs            99M  932K   98M   1% /run
    /dev/vda1        25G  1.4G   23G   7% /
    tmpfs           491M     0  491M   0% /dev/shm
    tmpfs           5.0M     0  5.0M   0% /run/lock
    tmpfs           491M     0  491M   0% /sys/fs/cgro

The line we are intrested in is /dev/vda1 or sda1 or any other similar /dev/sd* mount.

To create the swapfile we use to create a 4GB swapfile:

    sudo fallocate -l 4G /swapfile

Verify that the swapfile was created with:

    ls -lh /swapfile

The output should be:

    -rw-r--r-- 1 root root 4.0G Apr 25 11:14 /swapfile

Make the swapfile only accessible by root by issuing the following command:

    sudo chmod 600 /swapfile

If you again test with ls -lh /swapfile the output should be:

    -rw------- 1 root root 4.0G Apr 25 11:14 /swapfile

To make the file a swapfile we use the command:

    sudo mkswap /swapfile

The output should be something similar to:

    Output
    Setting up swapspace version 1, size = 4000 MiB (3073737728 bytes)
    no label, UUID=6e965805-2ab9-450f-aed6-577e74089dbf

Then we enable the swapfile with:

    sudo swapon /swapfile

The output should be something similar to:

    Output
    NAME      TYPE  SIZE USED PRIO
    /swapfile file 4000M   0B   -2

To make the swapfile permanent we have to add it to our fstab

    sudo cp /etc/fstab /etc/fstab.bak

This copies the fstab for future reference and debugging.

Then we issue:

    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

To make changes to the fstab file.

After this we can continue with the tutorial from point 13 and forward without issue. But remember to source! https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup



### OpenCR

Continuing on the tutorial https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/#opencr-setup

I did not have issues with this but this could be a potential issue, if you have issues with the motors the tutorial is not very extensive and I could not get the right arduino packages anywhere. Hopefully this is fixed in the future.

### Hardware assembly

Assemble according to the tutorial. https://emanual.robotis.com/docs/en/platform/turtlebot3/hardware_setup/#hardware-assembly

After this your robot should be able to do anything related to the turtlebot3 Humble guide. But to continue installing PEDRO, read on.

Connect your webcamera to a free usb port on the raspberry pi. 
Attach it somewhere and try to put the cables somewhere so they don't tangle the wheels.

Install the speaker to the 3.5mm hole in the raspberry and try to attach it somewhere. Tape, glue. Whatever works.

### Webserver

To get the webcam view I have created a program script included in this repository. Start by running the following commands in your ssh connection to the raspberry pi:

    cd
    git clone https://github.com/Dodisbeaver/PEDRO.git
    cd PEDRO
    python3 -m pip install -r requirements.txt

For the audio to work, you need to record 7 voice lines as wav files inside the AUDIO folder. Each of the lines should be three versions or you can just copy the same voice line three times. This is how the output should look like after running ls in the terminal

    $ ls
    1.1.wav  1.3.wav  2.2.wav  3.1.wav  3.3.wav  4.2.wav  5.1.wav  5.3.wav  6.2.wav  7.1.wav  7.3.wav 1.2.wav  2.1.wav  2.3.wav  3.2.wav  4.1.wav  4.3.wav  5.2.wav  6.1.wav  6.3.wav  7.2.wav

This is the lines that we used:

    1: ["AUDIO/1.1.wav", "AUDIO/1.2.wav", "AUDIO/1.3.wav"], Hello
    2: ["AUDIO/2.1.wav", "AUDIO/2.2.wav", "AUDIO/2.3.wav"], Anyone here
    3: ["AUDIO/3.1.wav", "AUDIO/3.2.wav", "AUDIO/3.3.wav"], I seek people
    4: ["AUDIO/4.1.wav", "AUDIO/4.2.wav", "AUDIO/4.3.wav"], There is a person here
    5: ["AUDIO/5.1.wav", "AUDIO/5.2.wav", "AUDIO/5.3.wav"], Stay calm
    6: ["AUDIO/6.1.wav", "AUDIO/6.2.wav", "AUDIO/6.3.wav"], A rescuer is coming 
    7: ["AUDIO/7.1.wav", "AUDIO/7.2.wav", "AUDIO/7.3.wav"] My name is pedro, and I am here to help you

There are many ways to record but we used garageband to record the files and exported them as wav.

Copy the files to your ubuntu PC/laptop and issue the follwing command but you need to know where your files are and the ip to the raspberry pi.

    $ cd /home/$USER/path/to/files/in/a/folder
    $ rsync -zaPh ./* ubuntu@PI_IP:PEDRO/AUDIO

To rename a file in ubuntu use mv if needed:

    mv file_to_be_renamed.wav new_filename.wav

After this you should be able to test the PEDRO person detection system with this command:

    $ python3 main.py
    Hello from the pygame community. https://www.pygame.org/contribute.html
    * Serving Flask app 'main'
    * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://192.168.292.215:5000
    Press CTRL+C to quit

On your PC/laptop go to the ip address of the pi on port 5000 in a browser. In the example: http://192.168.292.215:5000

You should get the view of the webcamera and also hear PEDRO issuing your voice lines. If you have come this far congratulaitions! PEDRO is now ready to detect people. 

![PEDRO](https://github.com/dodisbeaver/PEDRO/blob/main/PEDRO.jpeg?raw=true)

## Post-Installation Tasks
The rest of the tutorial follows closely the SLAM tutorial on the Turtlebo3 e-manual 
https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#run-slam-node

Our project ran out of time so the scope of this tutorial will be less informative going forward. If you find something that is not mentioned you can place an issue here.

The following commands are ready to use when ros is installed correctly and the turtlebo3 library is built.

Open 4 new terminal windows on your host PC/Laptop. Connect all of them to your Raspberry Pi through ssh.

    ssh ubuntu@RASPBERRY_PI_IP
And in each window if you haven't added it to your .bashrc 

    export TURTLEBOT3_MODEL=burger

Then issue the following command in one window:

    ros2 launch turtlebot3_bringup robot.launch.py

This will bring up your turtlebot. Next window:

    ros2 launch nav2_bringup navigation_launch.py 

This will bring up the navigation package. Next window:

    ros2 launch slam_toolbox online_async_launch.py 

This will bring up the slam mapping for use in rviz. In the next window:

    ros2 run turtlebot3_teleop teleop_keyboard

This is for remotely controlling your robot.

Open a new terminal on your PC/Laptop. Don't connect to the raspberry pi.
Issue the following command:

    ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz

If everything is working according to plan, you should soon se a window with RViz opening on your computer. This is how far I have come and feel free to make a bash script to do everything more automatically. 

In RViz you can use the Nav2 tab in the upper right corner but it is not very reliable because we do not have a map for the robot yet.

Next steps would be to map out a room and try to get the robot to know its position better. One could also try to figure out how to make this a into a ROS package and building the person detection into a new library to use with ROS nodes. Hopefully this helps some poor IT student with the turtlebot3 burger at least.

For this project the MobilenetV2 pre trained model was used. 
https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNetV2

## Post-installation checklist
Remember to source ~/.baschrc
To start the flask person detection server remember to cd into it.

## Troubleshooting
Camera index not found is a common problem, It can be the camera not being supported or just the raspberry being too slow for the usb-bridge connection. 

Remember to source

When building the turtlebot library, not having enough memory in the swap file can be a problem.

A lot of bugs exists in this repository. Feel free to let me know or open a PR. 

Follow the correct version on ROS and Turtlebot3. You can use older versions but then remember to follow that tutorial.


## Further reading
Here are some useful links:

https://ros2-industrial-workshop.readthedocs.io/en/latest/_source/basics/ROS2-Filesystem.html

https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-22-04

https://roboticsbackend.com/ros2-nav2-generate-a-map-with-slam_toolbox/


https://navigation.ros.org/plugin_tutorials/docs/writing_new_bt_plugin.html#writing-new-nbt-plugin

https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

https://github.com/ROBOTIS-GIT/OpenCR?tab=readme-ov-file

https://github.com/Balzabu/disable-cloud-init

https://www.raspberrypi.com/software/

https://ros2-industrial-workshop.readthedocs.io/en/latest/_source/navigation/ROS2-Turtlebot.html

https://github.com/cyberbotics/webots_ros2/wiki/Navigate-TurtleBot3