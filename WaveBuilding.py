from khepri.rhino import *

#--------------------------------#

#DEFINITIONS

height = 12.99   #building's height
n_floors = 3     #number of floors
length = 99.6    #building's length
width = 33.6     #building's width
h_slab = 0.3     #slab thickness
d_column = 0.5   #columns' width
n_column_x = 7   #number of columns in x axis reference
n_column_y = 12  #number of columns in y axis reference
d_element = 0.3  #wood elements' width
n_curtain_x = 25 #number of wood curtains in x axis reference
n_curtain_y = 8  #number of wood curtains in y axis reference
n_elements = 20  #number of wood elements per floor's height

a = 3            #wave amplitude of wood elements
w = 0.5          #wave frequency
fi = pi/8        #wave start angle
dfi = pi/16      #wave gap

#--------------------------------#

#LAYERS

slab_layer = create_layer('Slab')
column_layer = create_layer('Column')
facade_layer = create_layer('Facade')
floor_layer = create_layer('Floor')
ceiling_layer = create_layer('Ceiling')

#--------------------------------#

#FUNCTIONS

#building floors

def level(p):
    def slab():
        with current_layer(slab_layer):
            box(p, length, width, h_slab)
    def columns():
        def column(x, y):
                with current_layer(column_layer):
                    cylinder(xyz(x + d_column/2, y + d_column/2, 0) + vz(h_slab + p.z),
                    d_column/2, height/n_floors - h_slab)
        map_division(column,
        0, length - d_column, n_column_x - 1, 0, width - d_column, n_column_y - 1)
    slab()
    with current_layer(column_layer):
        columns()

#interior columns

def building_interior(p, a, w, fi, dfi):
    h_floor = height/n_floors
    with current_layer(slab_layer):
        box(p + vz(height - h_slab), length, width, h_slab)
    def floors(z_floor):
        level(p + vz(z_floor))
    map_division(floors, 0, height, n_floors, False)

#facade elements

def facade(p, a, w, fi, dfi):
    m = length/n_curtain_x
    d_element = height/n_elements/2
    c = 2 * sqrt((d_element/2) ** 2/2)
    def element(p, dfi):
        with current_layer(facade_layer):
            right_cuboid(p + vz(d_element/2),
            d_element, d_element,
            p + vz(d_element/2) + vx(m/2 + c) + vy(-abs(a*cos(p.z*w + fi + dfi) + c)))
            right_cuboid(p + vz(d_element/2) + vx(m) + vz(d_element),
            d_element, d_element,
            p + vz(d_element/2) + vx(m/2 - c) + vy(-abs(a*cos(p.z*w + fi + dfi) + c)) + vz(d_element))
    if n_elements == 0:
        pass
    else:
        def elements_x(x, z):
            element(p + vx(x) + vz(z), dfi*x)
            element(loc_from_o_phi(p + vx(length) + vy(width), pi) + vx(x) + vz(z), dfi*x)
        map_division(elements_x, 0, length, n_curtain_x, False, 0, height, n_elements, False)
        def elements_y(x, z):
            element(loc_from_o_phi(p + vx(length), pi/2) + vx(x) + vz(z), dfi*x)
            element(loc_from_o_phi(p + vy(width), 3*pi/2) + vx(x) + vz(z), dfi*x)
        map_division(elements_y, 0, width, n_curtain_y, False, 0, height, n_elements, False)

#building generation

def building(p, a, w, fi, dfi):
    building_interior(p, a, w, fi, dfi)
    facade(p, a, w, fi, dfi)

#--------------------------------#

#EXECUTIONS

building(u0(), 2, 0.5, pi/8, pi/16)

#--------------------------------#

#ANALYTICAL MODEL

def surfaces():
    with current_layer(floor_layer):
        surface_polygon(xyz(0, 0, h_slab), xyz(0, width, h_slab),
        xyz(length, width, h_slab), xyz(length, 0, h_slab))
        surface_polygon(xyz(0, 0, height/3 + h_slab), xyz(0, width, height/3 + h_slab),
        xyz(length, width, height/3 + h_slab), xyz(length, 0, height/3 + h_slab))
        surface_polygon(xyz(0, 0, 2*height/3 + h_slab), xyz(0, width, 2*height/3 + h_slab),
        xyz(length, width, 2*height/3 + h_slab), xyz(length, 0, 2*height/3 + h_slab))
        surface_polygon(xyz(0, 0, height + h_slab), xyz(0, width, height + h_slab),
        xyz(length, width, height + h_slab), xyz(length, 0, height + h_slab))
    with current_layer(ceiling_layer):
        surface_polygon(xyz(0, 0, 0), xyz(0, width, 0),
        xyz(length, width, 0), xyz(length, 0, 0))
        surface_polygon(xyz(0, 0, height/3), xyz(0, width, height/3),
        xyz(length, width, height/3), xyz(length, 0, height/3))
        surface_polygon(xyz(0, 0, 2*height/3), xyz(0, width, 2*height/3),
        xyz(length, width, 2*height/3), xyz(length, 0, 2*height/3))
        surface_polygon(xyz(0, 0, height), xyz(0, width, height),
        xyz(length, width, height), xyz(length, 0, height))
