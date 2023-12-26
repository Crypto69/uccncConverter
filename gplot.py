# Draws a picture using turtle graphics based on G-Code input.
import turtle
import re
import math
import re
import argparse

# If True, the path will be drawn. If False, only the cutting moves will be drawn.
draw_path = True
# color used for plotting moves when Laser is enabled
cutColor = "black"
# color used for plotting moves when the Laser is disabled (and drawTravel is True)
travelColor = "orange"
# speed for plotting travel Moves (based on G-Code G0, not Laser state)
travelSpeed = 10
# speed for plotting cutting Moves (based on G-Code G1, not Laser state)
cutSpeed = 8
# name of the file to plot
fileName = "Lasertest.nc"   

def parse_gcode_line(line):
    """
    Parses a single line of G-code and extracts relevant command and parameters using regular expressions.
    """
    plot_scale = 2
    command = None
    x = y = i = j = m = q = None
    is_cut_line = is_move_line = False

    # Extract the command
    command_match = re.search(r'G\d+', line)
    if command_match:
        command = command_match.group()

    # Extract coordinates and parameters
    x_match = re.search(r'X(-?\d+(\.\d+)?)', line)
    y_match = re.search(r'Y(-?\d+(\.\d+)?)', line)
    i_match = re.search(r'I(-?\d+(\.\d+)?)', line)
    j_match = re.search(r'J(-?\d+(\.\d+)?)', line)
    m_match = re.search(r'M(\d+)', line)
    q_match = re.search(r'Q(\d+(\.\d+)?)', line)

    if x_match:
        x = float(x_match.group(1)) * plot_scale
    if y_match:
        y = float(y_match.group(1)) * plot_scale
    if i_match:
        i = float(i_match.group(1)) * plot_scale
    if j_match:
        j = float(j_match.group(1)) * plot_scale
    if m_match:
        m = int(m_match.group(1)) * plot_scale
    if q_match:
        q = float(q_match.group(1)) * plot_scale

   # Determine if it's a cut line or a move line Based on G0/G1
    if command == 'G0':
        is_move_line = True 
    elif command in ['G1', 'G2', 'G3']:
        is_cut_line = True

    # Determine if it's a cut line or a move line Based on laser on/off
    if m == 10:
        if q == 255:
            is_cut_line = True
        elif q == 0:
            is_move_line = True

    return command, x, y, is_cut_line, is_move_line, i, j

def draw_arc(turtle, center_x, center_y, radius, start_angle, end_angle, clockwise):
    """
    Draws an arc using the Turtle graphics.
    """
    turtle.pendown()
    print("t.pendown()")

    if clockwise:
            # Handle the case for clockwise arcs
            if start_angle < end_angle:
                start_angle += 360
            while start_angle > end_angle:
                x = center_x + radius * math.cos(math.radians(start_angle))
                y = center_y + radius * math.sin(math.radians(start_angle))
                turtle.goto(x, y)
                print("t.goto("+str(x)+","+str(y)+")")
                start_angle -= 1
    else:
            # Handle the case for counterclockwise arcs
            if start_angle > end_angle:
                end_angle += 360
            while start_angle < end_angle:
                x = center_x + radius * math.cos(math.radians(start_angle))
                y = center_y + radius * math.sin(math.radians(start_angle))
                turtle.goto(x, y)
                print("t.goto("+str(x)+","+str(y)+")")
                start_angle += 1


def draw_with_turtle(gcode_file, draw_path=False):
    """
    Parses G-code and uses Turtle to draw the paths.
    """
   
    screen = turtle.Screen()
    screen.setup(width=2000, height=2000, startx=None, starty=None) 
    print("turtle.Screen()") 
    t = turtle.Turtle()
    print("turtle.Turtle()")
    t.speed(cutSpeed)
    print("t.speed("""+str(cutSpeed)+")")

    current_x, current_y = 0, 0
    try:
        with open(gcode_file) as file:
            fileList = file.readlines()
    except FileNotFoundError:
        print(f"The file {gcode_file} was not found.")

    for line in fileList:
        command, x, y, is_cut_line, is_move_line, i, j = parse_gcode_line(line)

        if x is not None and y is None:
            y = current_y
        elif y is not None and x is None:
            x = current_x

        if is_cut_line:
            t.pencolor(cutColor)
            print("t.pencolor("+cutColor+")")
            t.pendown()
            print("t.pendown()")
        elif is_move_line:
            if draw_path:
                t.pencolor(travelColor)
                print("t.pencolor("+travelColor+")")
                t.pendown()
                print("t.pendown()") 
            else:
                t.penup()
                print("t.penup()")
                t.pencolor(travelColor)
                print("t.pencolor("+travelColor+")")

        if command in ['G0', 'G1'] and x is not None and y is not None:
            t.goto(x, y)
            print("t.goto("+str(x)+","+str(y)+")")
        elif command in ['G2', 'G3']:
            center_x = current_x + (i if i is not None else 0)
            center_y = current_y + (j if j is not None else 0)
            radius = math.sqrt((current_x - center_x) ** 2 + (current_y - center_y) ** 2)
            start_angle = math.degrees(math.atan2(current_y - center_y, current_x - center_x))
            end_angle = math.degrees(math.atan2(y - center_y, x - center_x))

            clockwise = command == 'G2'
            draw_arc(t, center_x, center_y, radius, start_angle, end_angle, clockwise)

        if is_move_line and not draw_path:
            t.penup()
            print("t.penup()")

        if x is not None and y is not None:
            current_x, current_y = x, y

    screen.mainloop()

# Create the parser
parser = argparse.ArgumentParser(description="Name of the gcode file to plot:")

# Add the positional argument
parser.add_argument('file', nargs='?', default=fileName)

# Parse the arguments
args = parser.parse_args()

#  args.file is the file name given on the command line, or fileName Variable at the beginning of the code if no file name was given
print(args.file)
fileName = args.file
draw_with_turtle(fileName, draw_path)
