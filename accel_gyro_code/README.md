# Jerlen's Code Guide


### accel_gyro.py:  
This code requires the following pin connections:  
* (accel) vin   - 5V    (pin 2)
* (accel) gnd   - GND   (pin 6)
* (accel) scl   - GPIO2 (pin 5)
* (accel) sda   - GPIO3 (pin 3)
* (button) leg1 - GND   (pin 6)
* (button) leg2 - GPIO4 (pin 7)

After the scripts starts, press and hold the button to record the data.  
The code will record the readings during the button press onto a csv called "accel_data.csv".

### plot_data.py  
This code will ask for the file name and create a plot labeled "sample_plot.png."

## Viewing  
The file cannot be viewed on raspberry pi. To view the plot, enter the following command on the raspi:  `scp jacker{#}@jacker{#}.local:/home/jacker{#}/{enter_path_of_file/filename.png}`

## Version History  
2/24/25
* added files, updated readme with instructions

