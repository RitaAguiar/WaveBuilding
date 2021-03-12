using Khepri
backend(autocad)

############################

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

############################

#LAYERS

slab_layer = create_layer("Slab")
column_layer = create_layer("Column")
facade_layer = create_layer("Facade")
floor_layer = create_layer("Floor")
ceiling_layer = create_layer("Ceiling")

############################

delete_all_shapes()

#FUNCTIONS

#building floors

level(p) =
    let slab() =
        with(current_layer, slab_layer) do
            box(p, length, width, h_slab)
    end

    let columns() =
        let column(x, y) =
            with(current_layer, column_layer) do
                cylinder(xyz(x + d_column/2, y + d_column/2, 0) + vz(h_slab + p.z),
                d_column/2, height/n_floors - h_slab)
        end
        map_division(column,
        0, length - d_column, n_column_x - 1, 0, width - d_column, n_column_y - 1)
    end

    with(current_layer, column_layer) do
        columns()
    end

    slab()
    end

end

#interior columns

# p = u0()

building_interior(p, a, w, fi, dfi) =
     with(current_layer, slab_layer) do
         box(p + vz(height - h_slab), length, width, h_slab)
     end
    let floors(z_floor) =
        level(p + vz(z_floor))
    map_division(floors, 0, height, n_floors, false)
    end

#facade elements

facade(p, a, w, fi, dfi) =
    let m = length/n_curtain_x,
    d_element = height/n_elements/2,
    c = 2 * sqrt((d_element/2) ^ 2/2)
        let element(p, dfi) =
            with(current_layer, facade_layer) do
                right_cuboid(p + vz(d_element/2),
                d_element, d_element,
                p + vz(d_element/2) + vx(m/2 + c) + vy(-abs(a*cos(p.z*w + fi + dfi) + c)))
                right_cuboid(p + vz(d_element/2) + vx(m) + vz(d_element),
                d_element, d_element,
                p + vz(d_element/2) + vx(m/2 - c) + vy(-abs(a*cos(p.z*w + fi + dfi) + c)) + vz(d_element))
            end
        if n_elements == 0
            pass
        else
            let elements_x(x, z) =
                begin
                    circle()
                    element(p + vxz(x,z), dfi*x)
                    element(loc_from_o_phi(p + vxy(length, width), pi/2) + vxz(x,z), dfi*x)
                end
            map_division(elements_x, 0, length, n_curtain_x, false, 0, height, n_elements, false)
            end
            let elements_y(x, z) =
                begin
                    element(loc_from_o_phi(p + vx(length), pi/4) + vxz(x,z), dfi*x)
                    element(loc_from_o_phi(p + vy(width), 3*pi/4) + vxz(x,z), dfi*x)
                end
            map_division(elements_y, 0, width, n_curtain_y, false, 0, height, n_elements, false)
            end
        end
    end
end
#building generation

building(p, a, w, fi, dfi) =
    begin
        building_interior(p, a, w, fi, dfi)
        facade(p, a, w, fi, dfi)
    end

############################

#EXECUTIONS

building(u0(), 2, 0.5, pi/8, pi/16)
