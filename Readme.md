# Lightburn -> UCCNC Converter

This project includes Python scripts for parsing and visualizing G-Code files, as well as converting LightBurn G-Code files to UCCNC format.

## Installation

This project requires Python 3 and the following Python libraries installed:

- Turtle
- re
- math
- argparse

You can install these packages using pip:

```sh
pip install turtle re math argparse
```

## Files

### gplot.py

This script parses G-Code and uses Turtle graphics to visualize the paths. It takes a G-Code file as input and draws the paths based on the commands in the file. Provides a convenient way to verify what your output Will look like for laser engraving

To run this script, use the following command:

```sh
python gplot.py <filename>
```

Replace `<filename>` with the name of the G-Code file you want to visualize.

Running the command:

```sh
python gplot.py Lasertest.nc
```
produces the following image:

![Alternative text](Images/Lasertest.png)

The orange lines are the move lines and the black lines are cut lines. These can be changed to your liking changing the variables at the top of the script. If you do not want the move lines to be shown change the draw_path variable to equal false.

```python
# If True, the path will be drawn. If False, only the cutting moves will be drawn.
draw_path = False
# color used for plotting moves when Laser is enabled
cutColor = "black"
# color used for plotting moves when the Laser is disabled (and drawTravel is True)
travelColor = "orange"
# speed for plotting travel Moves (based on G-Code G0, not Laser state)
```

### uccncconverter.py

This script modifies LightBurn G-Code files to comply with UCCNC controllers. It takes a LightBurn GRBL-M3  G-Code file as input and modifies certain commands to make them compatible with UCCNC. (please note I've only tested this on a stepcraft M1000)

To run this script, use the following command:

```sh
python uccncconverter.py <filename>
```

Replace `<filename>` with the name of the LightBurn G-Code file you want to convert.

If you do not include a file name There is a variable in the script called file_path That will convert the sample File 'powerScale.gc' 

Converted files Will be saved In the same directory you run the script from and will be called  `<filename>_uccnc.nc`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[APACHE 2](https://choosealicense.com/licenses/apache-2.0)