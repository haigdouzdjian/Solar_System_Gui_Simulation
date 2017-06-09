
# Solar System Gui Simulation

# Haig Douzdjian

from math import sqrt

class Vector:
    '''
    A Vector is a 3-tuple of (x,y,z) coordinates
    '''
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def x(self):
        '''
        Accessor function for x.
        '''
        return self._x

    def y(self):
        '''
        Accessor function for y.
        '''
        return self._y

    def z(self):
        '''
        Accessor function for z.
        '''
        return self._z

    def __add__(self, blank):
        sideA = self._x + blank._x
        sideB = self._y + blank._y
        sideC = self._z + blank._z
        return Vector(sideA, sideB, sideC)

    def __eq__(self, blank):
        return (self._x == blank._x and self._y == blank._y and self._z == blank._z)

    def __repr__(self):
        return '({:.3g},{:.3g},{:.3g})'.format(self._x, self._y, self._z)

    def __sub__(self, blank):
        sideA = self._x - blank._x
        sideB = self._y - blank._y
        sideC = self._z - blank._z
        return Vector(sideA, sideB, sideC)
    def __mul__(self, blank):
        sideA = self._x * blank
        sideB = self._y * blank
        sideC = self._z * blank
        return Vector(sideA, sideB, sideC)
    def norm(self):
        '''
        Establishes the square root of the sum of the squared vector points x,y, and z.
        User inputs object (self). Returns the sqrt.
        '''
        return sqrt((self._x**2)+(self._y**2)+(self._z**2))
    def clear(self):
        '''
        Resets vector points x,y, and z to zero.
        User inputs object (self). Returns None.
        '''
        self._x = 0
        self._y = 0
        self._z = 0

G = 6.67E-11

class Body:
    """
    A Body object represents the state of a celestial body.  A body has mass
    (a scalar), position (a vector), and velocity (a vector).  A third vector,
    named force, is used when calculating forces acting on a body.
    """
    def __init__(self, mass = 0, position = Vector(0,0,0), velocity = Vector(0,0,0), force = Vector(0,0,0)):
        self._mass = mass
        self._position = position
        self._velocity = velocity
        self._force = force

    def __repr__(self):
        return '{:.3g}kg {} {}'.format(self._mass, self._position, self._velocity)

    def __eq__(self, blank):
        return (self._mass == blank._mass and self._position == blank._position and self._velocity == blank._velocity and self._force == blank._force)

    def mass(self):
        '''
        Accessor function for mass.
        '''
        return self._mass

    def position(self):
        '''
        Accessor function for position.
        '''
        return self._position

    def velocity(self):
        '''
        Accessor function for velocity.
        '''
        return self._velocity

    def force(self):
        '''
        Accessor function for force.
        '''
        return self._force

    def direction(self, blank):
        '''
        Subtracts points from one vector and another vector to establish a direction.
        User inputs objects (self and blank). Returns the direction.
        '''
        return blank.position() - self.position()

    def clear_force(self):
        '''
        Resets vector points x,y, and z to zero.
        User inputs object (self). Returns None.
        '''
        self.force().clear()

    def add_force(self, body):
        '''
        Establishes the force vector using given vector points and the equation below.
        User inputs object (self). Returns None.
        '''
        d_vec = self.direction(body)
        scalar = body.mass() / (d_vec.norm()**3)
        self._force += d_vec * scalar

    def move(self, dt):
        '''
        Moves and changes the velocity and posiiton of the vector using given vector points and the equation below.
        User inputs object (self), and a time step size (dt). Returns None.
        '''
        newG = self.force() * G
        self._velocity += newG * dt
        self._position += self.velocity() * dt


class Planet(Body):
    '''
    Extends the Body class by adding the attributes: name of planets and color used for GUI.
    '''
    def __init__(self, mass = 0, position = Vector(0,0,0), velocity = Vector(0,0,0), force = Vector(0,0,0), name = '', color = ''):
        Body.__init__(self, mass, position, velocity, force)
        self._name = name
        self._color = color
    def name(self):
        '''
        Accessor function for name.
        '''
        return self._name
    def color(self):
        '''
        Accessor function for color.
        '''
        return self._color

def step_system(bodies, dt=86459, nsteps=1):
    '''
    A function given with three arguments: bodies (list of Body objects), dt (a time step size),
    and nsteps (the number of steps to simulate). Function returns a list of Orbits.
    '''
    list_init = [[] for x in bodies]
    for i in range(nsteps):
        for z in bodies:
            for l in bodies:
                if z != l:
                    z.add_force(l)
        for z in range(len(bodies)):
            list_init[z].append((bodies[z].position().x(), bodies[z].position().y()))
            bodies[z].move(dt)
            bodies[z].clear_force()
    return list_init

IPython = (__doc__ is not None) and ('IPython' in __doc__)
Main    = __name__ == '__main__'

if IPython:
    get_ipython().magic('gui tk')

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from time import sleep

def read_bodies(filename, cls):
    '''
    Read descriptions of planets, return a list of body objects.  The first
    argument is the name of a file with one planet description per line, the
    second argument is the type of object to make for each planet.
    '''
    if not issubclass(cls, Body):
        raise TypeError('cls must be Body or a subclass of Body')

    bodies = [ ]

    with open(filename) as bodyfile:
        for line in bodyfile:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            name, m, rx, ry, rz, vx, vy, vz, rad, color = line.split()
            args = {
                'mass' : float(m),
                'position' : Vector(float(rx), float(ry), float(rz)),
                'velocity' : Vector(float(vx), float(vy), float(vz)),
            }
            opts = {'name': name, 'color': color, 'size': int(rad)}
            for x in opts:
                if getattr(cls, x, None):
                    args[x] = opts[x]
            bodies.append(cls(**args))

    return bodies

class TkPlanet(Planet):
    '''
    Extends the Planet class (which is an extension of the Body class)
    by adding the attribute: size which is used for the GUI.
    '''
    def __init__(self, mass = 0, position = Vector(0,0,0), velocity = Vector(0,0,0), name = '', color = '', size = 0):
        Planet.__init__(self, mass = mass, position = position, velocity = velocity, name = name, color = color)
        self._size = size
        self._graphic = None
    def size(self):
        '''
        Accessor function for size.
        '''
        return self._size
    def set_graphic(self, ID):
        '''
        Setter function for graphic.
        '''
        self._graphic = ID
    def graphic(self):
        '''
        Accessor function for graphic.
        '''
        return self._graphic


if IPython:
    b = TkPlanet(0, Vector(0,0,0), Vector(0,0,0), '', '', 0)

# Test

    assert isinstance(b, Planet)
    assert isinstance(b, TkPlanet)

# Test

    assert b.size() == 0
    assert b.graphic() is None

# Test

    b.set_graphic(0)
    assert b.graphic() == 0

if IPython:
    bodies = read_bodies('solarsystem.txt', TkPlanet)

# Test

    assert isinstance(bodies[0], TkPlanet)

# Test

    assert bodies[0].name() == 'sun'
    assert bodies[0].size() == 10
    assert bodies[0].color() == '#ffff00'

class SolarSystemCanvas(tk.Canvas):
    '''
    The SolarSystemCanvas class is a type of Canvas used to draw planets.
    '''
    def __init__(self, parent, height=600, width=600):
        tk.Canvas.__init__(self, parent, height=height, width=width, background='gray90', highlightthickness=0)
        self._planets = None
        self._outer = None
        self._scale = None
        self._offset = Vector(int(self['width'])/2, int(self['height'])/2, 0)

    def set_planets(self, lst):
        '''
        Setter function for planets.
        '''
        self._planets = lst
        self._outer = len(lst)
        self._compute_scale(lst)
        self.view_planets(len(lst))

    def view_planets(self, n):
        '''
        Draws circles representing the first n planets in the current list of TkPlanet
        objects (which have been saved in the instance variable self._planets).

        Bug: When 8 planets are shown, a few plot on top of the sun. With help, I could not figure out why this was.
        '''
        #nplanets = self._planets[:n]
        self._outer = n
        self._compute_scale(self._planets[:n])
        for i in self.find_all():
            self.delete(i)
        for z in range(n):
            pos = self._planets[z].position() * self._scale + self._offset
            x0 = pos.x() - self._planets[z]._size
            x1 = pos.x() + self._planets[z]._size
            y0 = pos.y() - self._planets[z]._size
            y1 = pos.y() + self._planets[z]._size
            circ = self.create_oval(x0, y0, x1, y1, fill = self._planets[z].color()) #creates the circle
            self._planets[z].set_graphic(circ) #establishes graphic for planet circle

    def move_planets(self, lst):
        '''
        Moves the circles for the first n of the list of TkPlanet objects, where n is the
        number of planets currently displayed on the canvas. Returns None.
        '''
        for z in lst[:self._outer]:
            cur_x, cur_y = self._current_loc(z)
            new_x, new_y = self._compute_loc(z)
            size = z.size()
            self.create_line(cur_x, cur_y, new_x, new_y)
            self.move(z.graphic(), new_x - cur_x, new_y - cur_y)
            #print('cur_x: {}, cur_y: {}, new_x: {}, new_y: {}'.format(cur_x, cur_y, new_x, new_y))

    def _compute_scale(self, bodies):
        '''
        Calculates a scaling factor so that when a body is displayed it is placed at the
        correct location on the screen (saved in self._scale). Returns None.
        '''
        minAtr = (min(int(self['height']), int(self['width']))) / 2
        my_max = bodies[0].position().norm()
        for z in range(len(bodies)):
            if bodies[z].position().norm() > my_max:
                my_max = bodies[z].position().norm()
        self._scale = (minAtr / my_max)

    def _compute_loc(self, p):
        '''
        Gets the x and y coordinates of the center of the circle representing planet p.
        '''
        pos = p.position() * self._scale + self._offset
        return pos.x(), pos.y()

    def _current_loc(self, p):
        '''
        Gets the x and y coordinates for the new center of the circle based on the position vector of planet p.
        '''
        ul, ur, _, _ = self.coords(p.graphic())
        return ul + p.size(), ur + p.size()

if IPython:
    canvas = SolarSystemCanvas(tk.Tk(), height=400, width=400)
    canvas.pack()
    bodies = read_bodies('solarsystem.txt', TkPlanet)

# Test

if IPython:
    canvas.set_planets(bodies)
    canvas.view_planets(2)
    assert [canvas.type(x) for x in canvas.find_all()].count('oval') == 2

# Test

if IPython:
    for i in range(10):
        step_system(bodies)
        canvas.move_planets(bodies)
    tk_objects = canvas.find_all()
    assert len(tk_objects) == 22
    assert [canvas.type(x) for x in tk_objects].count('line') == 20

class Viewbox(tk.Spinbox):
    '''
    A special type of Spinbox used to specify the number of planets to display on the canvas.
    '''
    def __init__(self, parent, callback):
        tk.Spinbox.__init__(self, parent, command=callback, width=3, state=tk.DISABLED)

    def set_limit(self, nbodies):
        '''
        A function that enables the spinbox, sets the lower bound to 2 and the upper bound to the number of
        bodies, and changes the value displayed in the spinbox to the number of bodies. Returns None.
        '''
        self['state'] = tk.NORMAL
        self['to'] = int(nbodies)
        self['from'] = 2
        for num in range(nbodies - 2):
            self.invoke('buttonup')

def vb_cb():
    global called
    called = True

if IPython:
    vb = Viewbox(tk.Tk(), vb_cb)
    vb.pack()

# Test

if IPython:
    called = False
    vb.invoke('buttondown')
    vb.invoke('buttonup')
    assert not called

# Test

if IPython:
    vb.set_limit(5)
    assert vb.get() == '5'
    assert vb['from'] == 2
    assert vb['to'] == 5

# Test

if IPython:
    called = False
    vb.invoke('buttondown')
    assert vb.get() == '4'
    vb.invoke('buttonup')
    assert vb.get() == '5'
    assert called

class RunFrame(tk.Frame):
    '''
    A container that has a run button, text entry boxes for the time step size and number of
    steps to run, and a progress bar to show how many steps have been executed.

    The class, RunFrame, uses tk.Frame and is implemented to setup the GUI that ties all of the previous parts together.
    It uses enable_button, init_progress, update_progress, and clear_progress
    '''
    def __init__(self, parent, callback):
        tk.Frame.__init__(self, parent)

        self['width'] = 200
        self['height'] = 100

        self._nsteps_entry = tk.Entry(self)
        self._nsteps_entry.pack()
        self._nsteps_entry.insert(0, '365')

        self._dt_entry = tk.Entry(self)
        self._dt_entry.pack()
        self._dt_entry.insert(0, '86459')

        self._run_button = tk.Button(self, text = 'Run', command = callback)
        self._run_button.pack()

        self._progress = ttk.Progressbar(self, orient = 'horizontal')
        self._progress.pack()

    def dt(self):
        '''
        Accessor function for dt.
        '''
        return int(self._dt_entry.get())

    def nsteps(self):
        '''
        Accessor function for nsteps.
        '''
        return int(self._nsteps_entry.get())

    def enable_button(self):
        '''
        A function that enables the _run_button. Returns None.
        '''
        self._run_button['state'] = tk.NORMAL

    def init_progress(self, n):
        '''
        A function that iniates the progress. Returns None.
        '''
        self._progress['maximum'] = n

    def update_progress(self, n):
        '''
        A function that updates the initiated progress. Returns None.
        '''
        self._progress['value'] += n

    def clear_progress(self):
        '''
        A funcion that clears all progress. Returns None.
        '''
        self._progress['value'] = 0

def rf_cb():
    global calls
    calls += 1

if IPython:
    rf = RunFrame(tk.Tk(), rf_cb)
    rf.pack()

# Test

if IPython:
    counts = { }
    for x in rf.children.values():
        counts.setdefault(type(x).__name__, 0)
        counts[type(x).__name__] += 1
    assert counts['Button'] == 1
    assert counts['Entry'] == 2
    assert counts['Progressbar'] == 1
    assert rf._dt_entry.get() == '86459'
    assert rf._nsteps_entry.get() == '365'

# Test

if IPython:
    calls = 0
    rf.enable_button()
    rf._run_button.invoke()
    rf._run_button.invoke()
    assert calls == 2

# Test

if IPython:
    rf._dt_entry.delete(0, tk.END)
    rf._dt_entry.insert(0, '100')
    assert rf.dt() == 100
    rf._nsteps_entry.delete(0, tk.END)
    rf._nsteps_entry.insert(0, '1000')
    assert rf.nsteps() == 1000

# Test

if IPython:
    rf.init_progress(100)
    for i in range(5):
        rf.update_progress(10)
    assert rf._progress['value'] == 50

root = tk.Tk()
root.title("Solar System")

bodies = None

def load_cb():
    global bodies
    fn = tk.filedialog.askopenfilename()
    bodies = read_bodies(fn, TkPlanet)
    canvas.set_planets(bodies)
    view_counter.set_limit(len(bodies))
    run_frame.enable_button()

def view_cb():
    canvas.view_planets(int(view_counter.get()))

def run_cb():

    def time_step():
        nonlocal nsteps
        step_system(bodies, dt)
        canvas.move_planets(bodies)
        run_frame.update_progress(1)
        sleep(0.02)
        if nsteps > 0:
            nsteps -= 1
            canvas.after_idle(time_step)
        else:
            run_frame.clear_progress()

    nsteps = run_frame.nsteps()
    run_frame.init_progress(nsteps)
    dt = run_frame.dt()
    canvas.after_idle(time_step)

canvas = SolarSystemCanvas(root)
canvas.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky="nsew")

tk.Button(root, text='Load', command=load_cb).grid(row=1, column=0, pady = 20)

view_frame = tk.Frame(root, width=100)
tk.Label(view_frame, text='Planets to View').pack()
view_counter = Viewbox(view_frame, view_cb)
view_counter.pack()
view_frame.grid(row=1, column=1, pady=20)

run_frame = RunFrame(root, run_cb)
run_frame.grid(row=1, column=2, pady=20)

if Main and not IPython:
    try:
        bodies = read_bodies("solarsystem.txt", TkPlanet)
        canvas.set_planets(bodies)
        view_count.reset(len(bodies))
        for i in range(5):
            view_count._spinbox.invoke('buttondown')
        run_frame._nsteps_entry.delete(0, tk.END)
        run_frame._nsteps_entry.insert(0,'100')
        root.update()
        run_frame._run_button.invoke()
    except Exception as err:
        print(err)
    input('hit return to continue...')
