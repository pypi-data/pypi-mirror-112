import math


def pre(Nx, Ny, Nz):
    s = f"""
dx := 1e-9
dy := 1e-9
dz := 4e-9
Nx := {Nx}
Ny := {Ny}
Nz := {Nz}
setgridsize(Nx,Ny, Nz)
setcellsize(dx, dy, dz)
edgesmooth = 8 // to test
setPBC(32, 32, 0) // to test

// Py stripe
adl := rect(Nx*dx,Ny*dy)
m = uniform(0, 0, 1)
Msat = 810e3
aex = 13e-12
alpha = 0.01
Ku1 = 453195
anisU = vector(0, 0, 1)
alpha = 0.01

"""
    return s


class square:
    def __init__(self, ad_size, ring_width):
        self.name = "square"
        self.ad_size = ad_size
        self.ring_width = ring_width

    def make(self):
        s = f"""// Square
    inner_geom := rect({self.ad_size:.4g},{self.ad_size:.4g})
    outer_geom := rect({self.ad_size + self.ring_width * 2:.4g},{self.ad_size + self.ring_width * 2:.4g})
        """
        return s


class diamond:
    def __init__(self, ad_size, ring_width):
        self.name = "diamond"
        self.ad_size = ad_size
        self.ring_width = ring_width

    def make(self):
        s = f"""// Diamond
    inner_geom := rect({self.ad_size:.4g},{self.ad_size:.4g}).RotZ(pi/4)
    outer_geom := rect({self.ad_size + self.ring_width * 2:.4g},{self.ad_size + self.ring_width * 2:.4g}).RotZ(pi/4)
        """
        return s


class circle:
    def __init__(self, ad_size, ring_width):
        self.name = "circle"
        self.ad_size = ad_size
        self.ring_width = ring_width

    def make(self):
        s = f"""// Circle
    inner_geom := cylinder({self.ad_size:.4g},Nz*dz)
    outer_geom := cylinder({self.ad_size + self.ring_width * 2:.4g},Nz*dz)
        """
        return s


class triangle:
    def __init__(self, ad_size, ring_width):
        self.name = "triangle"
        self.ad_size = ad_size
        self.ring_width = ring_width

    def make(self):
        from math import sqrt

        ad_size = self.ad_size
        ring_width = self.ring_width
        ad_size_outer = ad_size + ring_width * 2
        s = f"""// Triangle
    rec_right := rect({ad_size:.4g}, {ad_size * 2:.4g}).RotZ(pi/6).transl({3/4*ad_size:.4g},{(2-sqrt(3))*ad_size:.4g}/4,0)
    rec_left := rect({ad_size:.4g}, {ad_size * 2:.4g}).RotZ(-pi/6).transl({-3/4*ad_size:.4g},{(2-sqrt(3))*ad_size:.4g}/4,0)
    inner_geom := rect({ad_size:.4g}, {ad_size:.4g}).sub(rec_right).sub(rec_left)
    rec_right = rect({ad_size_outer:.4g}, {ad_size_outer * 2:.4g}).RotZ(pi/6).transl({3/4*ad_size_outer:.4g},{(2-sqrt(3))*ad_size_outer:.4g}/4,0)
    rec_left = rect({ad_size_outer:.4g}, {ad_size_outer * 2:.4g}).RotZ(-pi/6).transl({-3/4*ad_size_outer:.4g},{(2-sqrt(3))*ad_size_outer:.4g}/4,0)
    outer_geom := rect({ad_size_outer:.4g}, {ad_size_outer:.4g}).sub(rec_right).sub(rec_left).transl(0,4e-9,0)
        """
        return s


# lattices


class square_lattice:
    def __init__(self, a, reps):
        self.name = "square"
        self.a = a
        self.reps = reps
        self.Nx = reps * self.a
        self.Ny = reps * self.a

    def make(self):
        coordinates = []
        for i in range(self.reps):
            for j in range(self.reps):
                x = i * self.a + self.a / 2
                y = j * self.a + self.a / 2
                coordinates.append((x, y))
        return make_adl(coordinates)


class hexagon_lattice:
    def __init__(self, a, reps):
        self.name = "hexagon"
        self.a = a
        self.reps = reps
        self.h = a * math.sin(60 * math.pi / 180)
        self.Nx = int(reps * self.h * 1e9)
        self.Ny = int(reps * self.h * 1e9)

    def make(self):
        coordinates = []
        for i in range(self.reps):
            for j in range(self.reps + 1):
                x = i * self.h + self.h / 2
                y = j * self.h + self.h / 2
                if i % 2 == 1:
                    y -= self.h / 2
                coordinates.append((x, y))
        return make_adl(coordinates)


class honeycomb_lattice:
    def __init__(self, a, reps):
        self.name = "honeycomb"
        self.a = a
        self.reps = reps
        self.h = a * math.sin(60 * math.pi / 180)
        self.Nx = int(reps * self.h * 1e9)
        self.Ny = int(reps * self.h * 1e9)

    def make(self):
        coordinates = []
        for i in range(self.reps):
            for j in range(self.reps + 1):
                x = i * self.h + self.h / 2
                y = j * self.h + self.h / 2
                if i % 2 == 1:  # rows 1,3,5 ...
                    y -= self.h / 2
                    if j % 3 == 1:  # col 1,4,7 ...
                        continue
                if i % 2 == 0:  # rows 0,2,4 ...
                    if j % 3 == 2:  # col 2,5,8 ...
                        continue
                coordinates.append((x, y))
        return make_adl(coordinates)


def make_adl(coordinates):
    s = """
p := Nx*dx/2
"""
    for i in range(len(coordinates)):
        y, x = coordinates[i]
        if i == 0:
            q = ":"
        else:
            q = ""
        s += f"""
inner_dot {q}= inner_geom.transl(-p+{x:.4g},p-{y:.4g},0)
outer_dot {q}= outer_geom.transl(-p+{x:.4g},p-{y:.4g},0)
adl = adl.add(outer_dot)
adl = adl.sub(inner_dot)
m.setInShape(outer_dot, vortex(1, -1).transl(-p+{x:.4g},p-{y:.4g},0))
defregion(1, outer_dot)
Ku1.SetRegion(1, 0)

    """
    return s


def post():
    s = """
setgeom(adl)
setsolver(4)
maxerr = 5e-5
MinimizerStop = 5e-7
minimize()
relax()
run(1e-10)
relax()
saveAs(m, "stable")

Amps := 0.5e-4
f_cut := 20e09
t_sampl := 0.5 / (f_cut * 1.4)
t0 := 50 / f_cut
Maxdt = t_sampl / 100
B_ext = vector(Amps*sinc(2*pi*f_cut*(t-t0)), 0, 0)

tableadd(B_ext)
tableautosave(t_sampl)
autosave(m, t_sampl)

run(1500 * t_sampl)
"""
    return s


for g in [square, circle, triangle, diamond]:
    for l in [honeycomb_lattice, square_lattice, hexagon_lattice]:
        ad_size = 40
        ring_width = 10
        a = 100
        reps = 6
        AD = g(ad_size * 1e-9, ring_width * 1e-9)
        lattice = l(a * 1e-9, reps)
        name = f"{lattice.name}_lat_{AD.name}_ad_{reps}x{reps}_{ring_width=}nm_{ad_size=}nm_{a=}nm"
        with open(f"jobs2/{name}.mx3", "w") as f:
            f.writelines(pre(lattice.Nx, lattice.Ny, 1))
            f.writelines(AD.make())
            f.writelines(lattice.make())
            f.writelines(post())