from math import sqrt
import matplotlib as mpl


class square:
    def __init__(self, ad_size, ring_width):
        self.ad_size = ad_size
        self.ring_width = ring_width
        self.s = f"""// Square
        inner_geom := rect({ad_size:.4g},{ad_size:.4g})
        outer_geom := rect({ad_size + ring_width * 2:.4g},{ad_size + ring_width * 2:.4g})
        """

    def get_patch(self, center_x, center_y, ad_size):
        return mpl.patches.Rectangle(
            (center_x - ad_size / 2, center_y - ad_size / 2), ad_size, ad_size
        )


class diamond:
    def __init__(self, ad_size, ring_width):
        self.s = f"""// Diamond
        inner_geom := rect({ad_size:.4g},{ad_size:.4g}).RotZ(pi/4)
        outer_geom := rect({ad_size + ring_width * 2:.4g},{ad_size + ring_width * 2:.4g}).RotZ(pi/4)
        """

    def get_patch(self, center_x, center_y, ad_size):
        r = sqrt(2) * ad_size
        verts = [
            [center_x, center_y + r / 2],
            [center_x - r / 2, center_y],
            [center_x, center_y - r / 2],
            [center_x + r / 2, center_y],
            [center_x, center_y + r / 2],
        ]
        return mpl.patches.PathPatch(mpl.path.Path(verts, closed=True))


class circle:
    def __init__(self, ad_size, ring_width):
        self.s = f"""// Circle
        inner_geom := cylinder({ad_size:.4g},Nz*dz)
        outer_geom := cylinder({ad_size + ring_width * 2:.4g},Nz*dz)
        """

    def get_patch(self, center_x, center_y, ad_size):
        return mpl.patches.Circle((center_x, center_y), radius=ad_size / 2)


class triangle:
    def __init__(self, ad_size, ring_width):
        ad_size_outer = ad_size + ring_width * 2
        self.s = f"""// Triangle
        rec_right := rect({ad_size:.4g}, {ad_size * 2:.4g}).RotZ(pi/6).transl({3/4*ad_size:.4g},{(2-sqrt(3))*ad_size:.4g}/4,0)
        rec_left := rect({ad_size:.4g}, {ad_size * 2:.4g}).RotZ(-pi/6).transl({-3/4*ad_size:.4g},{(2-sqrt(3))*ad_size:.4g}/4,0)
        inner_geom := rect({ad_size:.4g}, {ad_size:.4g}).sub(rec_right).sub(rec_left)
        rec_right = rect({ad_size_outer:.4g}, {ad_size_outer * 2:.4g}).RotZ(pi/6).transl({3/4*ad_size_outer:.4g},{(2-sqrt(3))*ad_size_outer:.4g}/4,0)
        rec_left = rect({ad_size_outer:.4g}, {ad_size_outer * 2:.4g}).RotZ(-pi/6).transl({-3/4*ad_size_outer:.4g},{(2-sqrt(3))*ad_size_outer:.4g}/4,0)
        outer_geom := rect({ad_size_outer:.4g}, {ad_size_outer:.4g}).sub(rec_right).sub(rec_left).transl(0,4e-9,0)
        """

    def get_patch(self, center_x, center_y, ad_size):
        r = sqrt(3) * ad_size / 3
        verts = [
            [center_x, center_y + r],
            [center_x - ad_size / 2, center_y - r / 2],
            [center_x + ad_size / 2, center_y - r / 2],
            [center_x, center_y + r],
        ]
        return mpl.patches.PathPatch(mpl.path.Path(verts, closed=True))
