import inspect

from matplotlib import pyplot as plt
import matplotlib as mpl

from .antidot import square, circle, diamond, triangle
from .lattice import honeycomb_lattice, square_lattice, hexagon_lattice

antidots = {
    "square": square,
    "circle": circle,
    "triangle": triangle,
    "diamond": diamond,
}
lattices = {
    "square": square_lattice,
    "honeycomb": honeycomb_lattice,
    "hexagonal": hexagon_lattice,
}


class adl:
    def __init__(
        self, a=100, ad=40, ring=10, reps=4, lattice="square", antidot="square"
    ):
        self.s = ""
        self.a = a
        self.ad_size = ad
        self.ring_width = ring
        self.reps = reps
        self.lattice_name = lattice
        self.antidot_name = antidot
        self.lattice = lattices[lattice](self.a, self.reps)
        self.antidot = antidots[antidot](self.ad_size, self.ring_width)
        self._Nx = reps * a
        self._Ny = reps * a
        self._Nz = 1
        self.pre()
        self.geom()
        self.post()

    def save(self, dir):
        name = f"{self.lattice_name}_lat_{self.antidot_name}_ad_{self.reps}x{self.reps}_ring_{self.ring_width}nm_ad_{self.ad_size}nm_a_{self.a}nm"
        self.s = inspect.cleandoc(self.s)
        with open(f"{dir}/{name}.mx3", "w") as f:
            f.writelines(self.s)

    def preview(self):
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.set_xlim(0, self.a * self.reps)
        ax.set_ylim(0, self.a * self.reps)
        ax.patches.append(
            mpl.patches.Rectangle(
                (0, 0),
                self.a * self.reps,
                self.a * self.reps,
                color="k",
                transform=ax.transData,
            )
        )
        for x, y in self.lattice.coordinates:
            patch = self.antidot.get_patch(x, y, self.ad_size + self.ring_width)
            patch.set(transform=ax.transData, lw=0, facecolor="gray")
            ax.patches.append(patch)
        for x, y in self.lattice.coordinates:
            patch = self.antidot.get_patch(x, y, self.ad_size)
            patch.set(transform=ax.transData, lw=0, facecolor="w")
            ax.patches.append(patch)
        ax.set(xlabel="x (nm)", ylabel="y (nm)")
        fig.tight_layout()

    def pre(self):
        self.s += f"""
        dx := 1e-9
        dy := 1e-9
        dz := 4e-9
        Nx := {self._Nx}
        Ny := {self._Ny}
        Nz := {self._Nz}
        setgridsize(Nx,Ny, Nz)
        setcellsize(dx, dy, dz)
        edgesmooth = 8
        setPBC(32, 32, 0)

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

    def geom(self):
        self.s += self.antidot.s

        self.s += """
        p := Nx*dx/2
            """
        for i, (x, y) in enumerate(self.lattice.coordinates):
            if i == 0:
                q = ":"
            else:
                q = ""
            self.s += f"""
        inner_dot {q}= inner_geom.transl(-p+{x:.4g},p-{y:.4g},0)
        outer_dot {q}= outer_geom.transl(-p+{x:.4g},p-{y:.4g},0)
        adl = adl.add(outer_dot)
        adl = adl.sub(inner_dot)
        m.setInShape(outer_dot, vortex(1, -1).transl(-p+{x:.4g},p-{y:.4g},0))
        defregion(1, outer_dot)
        Ku1.SetRegion(1, 0)

                    """

    def post(self):
        self.s += """
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
