'''
  Modified version of Tolga Atam's ColabTurtle library, MIT License
  @link https://github.com/tolgaatam/ColabTurtle
'''
from IPython.display import display, HTML
import time
import math
import re
import typing

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'white'
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = 'black'
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
# all 140 color names that modern browsers support. taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white')
VALID_COLORS_SET = set(VALID_COLORS)
DEFAULT_TURTLE_SHAPE = 'turtle'
VALID_TURTLE_SHAPES = ('turtle', 'circle')
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
        {lines}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style=" stroke:none;fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" d="M 18.214844 0.632812 C 16.109375 1.800781 15.011719 4.074219 15.074219 7.132812 L 15.085938 7.652344 L 14.785156 7.496094 C 13.476562 6.824219 11.957031 6.671875 10.40625 7.066406 C 8.46875 7.550781 6.515625 9.15625 4.394531 11.992188 C 3.0625 13.777344 2.679688 14.636719 3.042969 15.027344 L 3.15625 15.152344 L 3.519531 15.152344 C 4.238281 15.152344 4.828125 14.886719 8.1875 13.039062 C 9.386719 12.378906 10.371094 11.839844 10.378906 11.839844 C 10.386719 11.839844 10.355469 11.929688 10.304688 12.035156 C 9.832031 13.09375 9.257812 14.820312 8.96875 16.078125 C 7.914062 20.652344 8.617188 24.53125 11.070312 27.660156 C 11.351562 28.015625 11.363281 27.914062 10.972656 28.382812 C 8.925781 30.84375 7.945312 33.28125 8.238281 35.1875 C 8.289062 35.527344 8.28125 35.523438 8.917969 35.523438 C 10.941406 35.523438 13.074219 34.207031 15.136719 31.6875 C 15.359375 31.417969 15.328125 31.425781 15.5625 31.574219 C 16.292969 32.042969 18.023438 32.964844 18.175781 32.964844 C 18.335938 32.964844 19.941406 32.210938 20.828125 31.71875 C 20.996094 31.625 21.136719 31.554688 21.136719 31.558594 C 21.203125 31.664062 21.898438 32.414062 22.222656 32.730469 C 23.835938 34.300781 25.5625 35.132812 27.582031 35.300781 C 27.90625 35.328125 27.9375 35.308594 28.007812 34.984375 C 28.382812 33.242188 27.625 30.925781 25.863281 28.425781 L 25.542969 27.96875 L 25.699219 27.785156 C 28.945312 23.960938 29.132812 18.699219 26.257812 11.96875 L 26.207031 11.84375 L 27.945312 12.703125 C 31.53125 14.476562 32.316406 14.800781 33.03125 14.800781 C 33.976562 14.800781 33.78125 13.9375 32.472656 12.292969 C 28.519531 7.355469 25.394531 5.925781 21.921875 7.472656 L 21.558594 7.636719 L 21.578125 7.542969 C 21.699219 6.992188 21.761719 5.742188 21.699219 5.164062 C 21.496094 3.296875 20.664062 1.964844 19.003906 0.855469 C 18.480469 0.503906 18.457031 0.5 18.214844 0.632812"/>
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """
      <g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
        <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
        <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
      </g>
    """


SPEED_TO_SEC_MAP = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}

class Window:

    #Constructor
    def __init__(self, window_size : tuple = DEFAULT_WINDOW_SIZE):
        if not (isinstance(window_size, tuple) and len(window_size) == 2 and isinstance(
                window_size[0], int) and isinstance(window_size[1], int)):
            raise ValueError('window_size must be a tuple of 2 integers')

        self.window_size = window_size     
        self.background_color = DEFAULT_BACKGROUND_COLOR
        self.turtles = []
        self.drawing_window = display(HTML(self._generateSvgDrawing()), display_id=True)


    # helper function that maps [1,13] speed values to ms delays
    def _speedToSec(self, speed):
        return SPEED_TO_SEC_MAP[speed]


    # helper function for generating svg string of the turtles
    def _generateTurtleSvgDrawing(self):
        res = ""
        for turtle in self.turtles:
            if turtle.is_turtle_visible:
                vis = 'visible'
            else:
                vis = 'hidden'

            turtle_x = turtle.turtle_pos[0]
            turtle_y = turtle.turtle_pos[1]
            degrees = turtle.turtle_degree
            template = ''

            if turtle.turtle_shape == 'turtle':
                turtle_x -= 18
                turtle_y -= 18
                degrees += 90
                template = TURTLE_TURTLE_SVG_TEMPLATE
            else: #circle
                degrees -= 90
                template = TURTLE_CIRCLE_SVG_TEMPLATE

            res += template.format(turtle_color=turtle.pen_color, turtle_x=turtle_x, turtle_y=turtle_y, \
                                            visibility=vis, degrees=degrees, rotation_x=turtle.turtle_pos[0], rotation_y=turtle.turtle_pos[1])
        return res


    # helper function for linking svg strings of text
    def _generateSvgLines(self):
        res = ""
        for turtle in self.turtles:
            res+=turtle.svg_lines_string 
        return res


    # helper function for generating the whole svg string
    def _generateSvgDrawing(self):
        return SVG_TEMPLATE.format(window_width=self.window_size[0], window_height=self.window_size[1],
                                background_color=self.background_color, lines=self._generateSvgLines(),
                                turtle=self._generateTurtleSvgDrawing())


    # helper functions for updating the screen using the latest positions/angles/lines etc.
    def _updateDrawing(self, turtle=None):
        if turtle is None:
            time.sleep(self._speedToSec(4))
        else:
            time.sleep(self._speedToSec(turtle.turtle_speed))
        self.drawing_window.update(HTML(self._generateSvgDrawing()))


    # helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
    def _moveToNewPosition(self, new_pos, turtle):
        # rounding the new_pos to eliminate floating point errors.
        new_pos = ( round(new_pos[0],3), round(new_pos[1],3) )

        start_pos = turtle.turtle_pos
        if turtle.is_pen_down:
            turtle.svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
                x1=start_pos[0], y1=start_pos[1], x2=new_pos[0], y2=new_pos[1], pen_color=turtle.pen_color, pen_width=turtle.pen_width)

        turtle.turtle_pos = new_pos
        self._updateDrawing(turtle)

    def _validateColorString(self, color):
        if color in VALID_COLORS_SET: # 140 predefined html color names
            return True
        if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
            return True
        if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
            return True
        return False

    def _validateColorTuple(self, color):
        if len(color) != 3:
            return False
        if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
            return False
        if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
            return False
        return True

    def _processColor(self, color):
        if isinstance(color, str):
            color = color.lower()
            if not self._validateColorString(color):
                raise ValueError('color is invalid. it can be a known html color name, 3-6 digit hex string or rgb string.')
            return color
        elif isinstance(color, tuple):
            if not self._validateColorTuple(color):
                raise ValueError('color tuple is invalid. it must be a tuple of three integers, which are in the interval [0,255]')
            return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
        else:
            raise ValueError('the first parameter must be a color string or a tuple')

    # change the background color of the drawing area
    # if no params, return the current background color
    def bgcolor(self, color = None, c2 = None, c3 = None):
        if color is None:
            return self.background_color
        elif c2 is not None:
            if c3 is None:
                raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
            color = (color, c2, c3)

        self.background_color = self._processColor(color)
        self._updateDrawing()        

    # return turtle window width
    def window_width(self):
        return self.window_size[0]

    # return turtle window height
    def window_height(self):
        return self.window_size[1]

    def add(self, turtle):
        self.turtles.append(turtle)
        self._updateDrawing()
        
class Turtle:
    
    #Constructor
    def __init__(self, window, speed : int = DEFAULT_SPEED, position : tuple = None):
    
        if isinstance(speed,int) == False or speed not in range(1, 14):
            raise ValueError('initial_speed must be an integer in interval [1,13]')
        self.turtle_speed = speed

        self.is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
        self.pen_color = DEFAULT_PEN_COLOR
        self.turtle_degree = DEFAULT_TURTLE_DEGREE
        self.svg_lines_string = DEFAULT_SVG_LINES_STRING
        self.is_pen_down = DEFAULT_IS_PEN_DOWN
        self.pen_width = DEFAULT_PEN_WIDTH
        self.turtle_shape = DEFAULT_TURTLE_SHAPE

        if not isinstance(window, Window) == True:
            raise TypeError("window must be a window object")

        if position is not None:
            if not (isinstance(position, tuple) and len(position) == 2 and isinstance(position[0], int) and isinstance(position[1], int)):
                raise ValueError('position must be a tuple of 2 integers')    
            else:
                self.turtle_pos = position     
        else:
            self.turtle_pos = (window.window_size[0] // 2, window.window_size[1] // 2)            
        self.drawing_window = window
        window.add(self)

    # makes the turtle move forward by 'units' units
    def forward(self, units):
        if not isinstance(units, (int,float)):
            raise ValueError('units must be a number.')

        alpha = math.radians(self.turtle_degree)
        ending_point = (self.turtle_pos[0] + units * math.cos(alpha), self.turtle_pos[1] + units * math.sin(alpha))

        self.drawing_window._moveToNewPosition(ending_point, self)

    fd = forward # alias

    # makes the turtle move backward by 'units' units
    def backward(self, units):
        if not isinstance(units, (int,float)):
            raise ValueError('units must be a number.')
        self.forward(-1 * units)

    bk = backward # alias
    back = backward # alias


    # makes the turtle move right by 'degrees' degrees (NOT radians)
    def right(self, degrees):
        if not isinstance(degrees, (int,float)):
            raise ValueError('degrees must be a number.')

        self.turtle_degree = (self.turtle_degree + degrees) % 360
        self.drawing_window._updateDrawing(self)

    rt = right # alias

    # makes the turtle face a given direction
    def face(self, degrees):
        if not isinstance(degrees, (int,float)):
            raise ValueError('degrees must be a number.')

        self.turtle_degree = degrees % 360
        self.drawing_window._updateDrawing(self)

    setheading = face # alias
    seth = face # alias

    # makes the turtle move right by 'degrees' degrees (NOT radians, this library does not support radians right now)
    def left(self, degrees):
        if not isinstance(degrees, (int,float)):
            raise ValueError('degrees must be a number.')
        self.right(-1 * degrees)

    lt = left

    # raises the pen such that following turtle moves will not cause any drawings
    def penup(self):
        self.is_pen_down = False
        # TODO: decide if we should put the timout after lifting the pen
        # _updateDrawing()

    pu = penup # alias
    up = penup # alias

    # lowers the pen such that following turtle moves will now cause drawings
    def pendown(self):
        self.is_pen_down = True
        # TODO: decide if we should put the timout after releasing the pen
        # _updateDrawing()

    pd = pendown # alias
    down = pendown # alias

    def isdown(self):
        return self.is_pen_down

    # update the speed of the moves, [1,13]
    # if argument is omitted, it returns the speed.
    def speed(self, speed = None):
        if speed is None:
            return self.turtle_speed

        if isinstance(speed,int) == False or speed not in range(1, 14):
            raise ValueError('speed must be an integer in the interval [1,13].')
        self.turtle_speed = speed
        # TODO: decide if we should put the timout after changing the speed
        # _updateDrawing()


    # move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
    def setx(self, x):
        if not isinstance(x, (int,float)):
            raise ValueError('new x position must be a number.')
        if x < 0:
            raise ValueError('new x position must be non-negative.')
        self.drawing_window._moveToNewPosition((x, self.turtle_pos[1]), self)


    # move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
    def sety(self, y):
        if not isinstance(y, (int,float)):
            raise ValueError('new y position must be a number.')
        if y < 0:
            raise ValueError('new y position must be non-negative.')
        self.drawing_window._moveToNewPosition((self.turtle_pos[0], y), self)


    def home(self):
        self.turtle_degree = DEFAULT_TURTLE_DEGREE
        self.drawing_window._moveToNewPosition( (self.drawing_window.window_size[0] // 2, self.drawing_window.window_size[1] // 2), self ) # this will handle updating the drawing.

    # retrieve the turtle's currrent 'x' x-coordinate
    def getx(self):
        return(self.turtle_pos[0])

    xcor = getx # alias

    # retrieve the turtle's currrent 'y' y-coordinate
    def gety(self):
        return(self.turtle_pos[1])

    ycor = gety # alias

    # retrieve the turtle's current position as a (x,y) tuple vector
    def position(self):
        return self.turtle_pos

    pos = position # alias

    # retrieve the turtle's current angle
    def getheading(self):
        return self.turtle_degree

    heading = getheading # alias

    # move the turtle to a designated 'x'-'y' coordinate
    def goto(self, x, y=None):
        if isinstance(x, tuple) and y is None:
            if len(x) != 2:
                raise ValueError('the tuple argument must be of length 2.')

            y = x[1]
            x = x[0]

        if not isinstance(x, (int,float)):
            raise ValueError('new x position must be a number.')
        if x < 0:
            raise ValueError('new x position must be non-negative')
        if not isinstance(y, (int,float)):
            raise ValueError('new y position must be a number.')
        if y < 0:
            raise ValueError('new y position must be non-negative.')
        self.drawing_window._moveToNewPosition((x, y), self)

    setpos = goto # alias
    setposition = goto # alias

    # switch turtle visibility to ON
    def showturtle(self):
        self.is_turtle_visible = True
        self.drawing_window._updateDrawing(self)

    st = showturtle # alias

    # switch turtle visibility to OFF
    def hideturtle(self):
        self.is_turtle_visible = False
        self.drawing_window._updateDrawing(self)

    ht = hideturtle # alias

    def isvisible(self):
        return self.is_turtle_visible

    def _validateColorString(self, color):
        if color in VALID_COLORS_SET: # 140 predefined html color names
            return True
        if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
            return True
        if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
            return True
        return False

    def _validateColorTuple(self, color):
        if len(color) != 3:
            return False
        if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
            return False
        if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
            return False
        return True

    def _processColor(self, color):
        if isinstance(color, str):
            color = color.lower()
            if not self._validateColorString(color):
                raise ValueError('color is invalid. it can be a known html color name, 3-6 digit hex string or rgb string.')
            return color
        elif isinstance(color, tuple):
            if not self._validateColorTuple(color):
                raise ValueError('color tuple is invalid. it must be a tuple of three integers, which are in the interval [0,255]')
            return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
        else:
            raise ValueError('the first parameter must be a color string or a tuple')

    # change the color of the pen
    # if no params, return the current pen color
    def color(self, color = None, c2 = None, c3 = None):
        if color is None:
            return self.pen_color
        elif c2 is not None:
            if c3 is None:
                raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
            color = (color, c2, c3)

        self.pen_color = self._processColor(color)
        self.drawing_window._updateDrawing()

    pencolor = color

    # change the width of the lines drawn by the turtle, in pixels
    # if the function is called without arguments, it returns the current width
    def width(self, width = None):

        if width is None:
            return self.pen_width
        else:
            if not isinstance(width, int):
                raise ValueError('new width position must be an integer.')
            if not width > 0:
                raise ValueError('new width position must be positive.')

            self.pen_width = width
            # TODO: decide if we should put the timout after changing the pen_width
            # _updateDrawing()

    pensize = width

    # calculate the distance between the turtle and a given point
    def distance(self, x, y=None):
        if isinstance(x, tuple) and y is None:
            if len(x) != 2:
                raise ValueError('the tuple argument must be of length 2.')

            y = x[1]
            x = x[0]

        if not isinstance(x, (int,float)):
            raise ValueError('new x position must be a number.')
        if x < 0:
            raise ValueError('new x position must be non-negative')
        if not isinstance(y, (int,float)):
            raise ValueError('new y position must be a number.')
        if not y < 0:
            raise ValueError('new y position must be non-negative.')

        point = (x,y)
        if not isinstance(point, tuple) or len(point) != 2 or (not isinstance(point[0], int) and not isinstance(point[0], float)) or (not isinstance(point[1], int) and not isinstance(point[1], float)):
            raise ValueError('the vector given for the point must be a tuple with 2 numbers.')

        return round(math.sqrt( (self.turtle_pos[0] - x) ** 2 + (self.turtle_pos[1] - y) ** 2 ), 4)

    # clear any text or drawing on the screen
    def clear(self):
        self.svg_lines_string = ""
        self.drawing_window._updateDrawing()

    def write(self, obj, **kwargs):
        text = str(obj)
        font_size = 12
        font_family = 'Arial'
        font_type = 'normal'
        align = 'start'

        if 'align' in kwargs and kwargs['align'] in ('left', 'center', 'right'):
            if kwargs['align'] == 'left':
                align = 'start'
            elif kwargs['align'] == 'center':
                align = 'middle'
            else:
                align = 'end'

        if "font" in kwargs:
            font = kwargs["font"]
            if len(font) != 3 or isinstance(font[0], int) == False or isinstance(font[1], str) == False or font[2] not in {'bold','italic','underline','normal'}:
                raise ValueError('font parameter must be a triplet consisting of font size (int), font family (str) and font type. font type can be one of {bold, italic, underline, normal}')
            font_size = font[0]
            font_family = font[1]
            font_type = font[2]
            
        style_string = ""
        style_string += "font-size:" + str(font_size) + "px;"
        style_string += "font-family:'" + font_family + "';"

        if font_type == 'bold':
            style_string += "font-weight:bold;"
        elif font_type == 'italic':
            style_string += "font-style:italic;"
        elif font_type == 'underline':
            style_string += "text-decoration: underline;"

        
        self.svg_lines_string += """<text x="{x}" y="{y}" fill="{fill_color}" text-anchor="{align}" style="{style}">{text}</text>""".format(x=self.turtle_pos[0], y=self.turtle_pos[1], text=text, fill_color=self.pen_color, align=align, style=style_string)
        
        self.drawing_window._updateDrawing()

    def shape(self, shape=None):
        if shape is None:
            return self.turtle_shape
        elif shape not in VALID_TURTLE_SHAPES:
            raise ValueError('shape is invalid. valid options are: ' + str(VALID_TURTLE_SHAPES))
        
        self.turtle_shape = shape
        self.drawing_window._updateDrawing()

