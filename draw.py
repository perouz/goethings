import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def draw_points(points, color='b'):
    map(lambda p: p.draw(color), points)


def fancy_draw_chain(chain, figure='1', facecolor='orange'):
    vertices = chain.vertices
    codes = [Path.MOVETO]
    for i in range(1, chain.n):
        codes.append(Path.LINETO)

    path = Path(vertices, codes)

    fig = plt.figure(figure)
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor=facecolor, lw=2)
    ax.add_patch(patch)

    ax.set_xlim(min(chain.X), max(chain.X))
    ax.set_ylim(min(chain.Y), max(chain.Y))
    plt.show()
