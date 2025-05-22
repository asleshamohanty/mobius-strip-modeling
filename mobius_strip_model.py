import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import simpson

class MobiusStrip:
    def __init__(self, R=1.0, w=0.3, n=200):
        self.R = R
        self.w = w
        self.n = n
        self.u, self.v = np.meshgrid(
            np.linspace(0, 2 * np.pi, n),
            np.linspace(-w / 2, w / 2, n)
        )
        self.x, self.y, self.z = self._generate_mesh()

    def _generate_mesh(self):
        u, v = self.u, self.v
        x = (self.R + v * np.cos(u / 2)) * np.cos(u)
        y = (self.R + v * np.cos(u / 2)) * np.sin(u)
        z = v * np.sin(u / 2)
        return x, y, z

    def compute_surface_area(self):
        # surface area using simpson rule
        dxdu = np.gradient(self.x, axis=1)
        dxdv = np.gradient(self.x, axis=0)
        dydu = np.gradient(self.y, axis=1)
        dydv = np.gradient(self.y, axis=0)
        dzdu = np.gradient(self.z, axis=1)
        dzdv = np.gradient(self.z, axis=0)

        cross_x = dydu * dzdv - dzdu * dydv
        cross_y = dzdu * dxdv - dxdu * dzdv
        cross_z = dxdu * dydv - dydu * dxdv

        dA = np.sqrt(cross_x**2 + cross_y**2 + cross_z**2)

        area = simpson(
            simpson(dA, self.v[:, 0]), self.u[0, :]
        )
        return area

    def compute_edge_length(self):
        # find length of mobius strip 
        u_vals = np.linspace(0, 2 * np.pi, self.n)
        edge_pts = []
        for v in [-self.w / 2, self.w / 2]:
            x = (self.R + v * np.cos(u_vals / 2)) * np.cos(u_vals)
            y = (self.R + v * np.cos(u_vals / 2)) * np.sin(u_vals)
            z = v * np.sin(u_vals / 2)
            pts = np.stack((x, y, z), axis=1)
            edge_pts.append(pts)

        edge = np.concatenate(edge_pts)
        deltas = np.diff(edge, axis=0)
        segment_lengths = np.linalg.norm(deltas, axis=1)
        return np.sum(segment_lengths)

    def plot(self):
        # plot mobius strip
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.x, self.y, self.z, cmap='viridis', edgecolor='k', alpha=0.8)
        ax.set_title("Möbius Strip")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    mobius = MobiusStrip(R=1.0, w=0.3, n=300)
    mobius.plot()
    area = mobius.compute_surface_area()
    edge_len = mobius.compute_edge_length()

    print(f"Approximate Surface Area: {area:.4f}")
    print(f"Approximate Edge Length: {edge_len:.4f}")
