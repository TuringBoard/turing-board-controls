# Turning Board Controls
Software responsible for controlling the wheels and turning mechanism of the Turning Board.

### Dependencies
- `pip install crccheck`
- `pip install Pyrebase`
- PyVESC - A modified version of the library has been added inside of this project.

### Usage
After turning the Jetson TX2 on, open Terminal and `cd` into `Desktop/turing_board/turing-board-controls/src/Controls`.

```
$ cd Desktop/turing_board/turing_board_controls/src/Controls
```

Run the bash file to list all devices connected via ttyACM. 

```
$ bash ./list_devices.sh
```

Look for two devices and see what serial ports they are assigned, 
- The red board, labeled as 'Texas Instruments...' (usually ttyACM0)
- The VESC motors, labeled as 'STM Microelectronics...' (usually ttyACM1)

Make sure the serial port numbers are aligned with what's in line ~35 of `turing_board_motor_test.py`. The value provided to the argument `vesc_serial_port` in the constructor of the `Controls` class should match what was observed after running the batch file. Same for `follow_me_serial_port`. 


Also ensure the port number matches in `turing-board-controls/src/Communication/uart0Communication.py` on line 4. This is the port number for the red board. 

Once the correct port numbers are verified, ensure the RealSense camera is connected. 

Then run the following commands to enable sudo access to the serial ports. 

```
$ sudo chmod 666 /dev/ttyACM0
$ sudo chmod 666 /dev/ttyACM1
```

> Note: Change port number at the end of the above commands according to what is the current port number of the red board and the VESC. Also, these two commands can be ignored if the current user is added to the sudoers list. 


Run the python file to initialize the Turing board. 

```
$ python3 turing_board_motor_test.py
```

You will know the Turing board has been initialized correctly when you see something along the following lines echoed on the terminal screen: 

```
Initializing VESC...
```

This is where you take advantage of the lovely Turing Board app to interface with the Turing Board. In order to pair the Turing Board app with your board, contact Sahaj to obtain instructions. 

> Note: There is a particular error you may sometimes see after running the python file, it may be because you have not enabled sudo access to the serial ports with the commands above. You will be familiar with what the error looks like after enough suffering and pain, I do not have the error text handy at the moment. 

Enjoy your Turing Board!

### References
- https://en.ans.wiki/419/what-is-the-formula-to-convert-revolutions-per-minute-rpm-to-kilometers-per-hour-km-slash-h/
