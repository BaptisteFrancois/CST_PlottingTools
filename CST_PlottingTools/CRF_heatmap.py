
import numpy as np
import math
from matplotlib import colormaps as cmaps
from CST_PlottingTools.utils import CenteredColorMap
import matplotlib.pyplot as plt


def Heatmap(data, x_labels, y_labels, title='', xlabel='', ylabel='', cmap='coolwarm', colorbar_label='',
            vmin=None, vmax=None, vcenter=None, alpha=1, grid=False, fontsize_labels=13, 
            fontsize_ticklabels=12, fontsize_title=14, fontsize_cbar_label=13, figsize=(6,6), 
            savepath=None, show=False):
        
    """ Create a heatmap plot of the data.

    Parameters
    ----------

    data : 2D array
        The data to be plotted.
    x_labels : 1D array
        The labels for the x-axis.
    y_labels : 1D array
        The labels for the y-axis.
    title : str (Optional)
        The title of the plot.
    xlabel : str (Optional)
        The label of the x-axis.
    ylabel : str (Optional)
        The label of the y-axis.
    cmap : str (Optional; default value is 'coolwarm')
        The colormap to be used.
    colorbar_label : str (Optional)
        The label of the colorbar.
    vmin : float (Optional)
        The minimum value of the colorbar.
    vmax : float (Optional)
        The maximum value of the colorbar.
    vcenter : float (Optional)
        The center value of the colormap.
    alpha : float (Optional; default value is 1)
        The transparency of the colors.
    grid : bool (Optional; default value is False)
        Whether to add a grid to separate the cells.
    fontsize_labels : int
        The fontsize of the labels.
    fontsize_ticklabels : int
        The fontsize of the tick labels.
    fontsize_title : int
        The fontsize of the title.
    fontsize_cbar_label : int
        The fontsize of the colorbar label.
    figsize : tuple
        The size of the figure.
    savepath : str
        The path to save the figure.
    show : bool
        Whether to show the plot.
    """
    # Check that labels are regularly spaced
    if not np.all(np.diff(x_labels) == np.diff(x_labels)[0]):
        raise ValueError('x_labels must be regularly spaced.')
    if not np.all(np.diff(y_labels) == np.diff(y_labels)[0]):
        raise ValueError('y_labels must be regularly spaced.')

    # Get the colormap
    if vcenter:
        # Get 'vmax' value
        if not vmax:
            vmax = math.ceil(data.max())
        # Get 'vmin' value
        if not vmin:
            vmin = math.floor(data.min())
        # if the data is constant, return the original colormap and disregard the requested 'vcenter' value
        if vmin == vmax: 
            cmap = cmaps.get(cmap)
        else:
            cmap = CenteredColorMap(cmaps.get(cmap), vmin=vmin, vmax=vmax, vcenter=vcenter)

    # Not centered colormap requested   
    else:
        cmap = cmaps.get(cmap)
        norm = None

    # Calculate the extent of the grid
    grid_x_resolution = np.diff(x_labels)[0]
    grid_y_resolution = np.diff(y_labels)[0]
    grid_extent = (
        min(x_labels)-grid_x_resolution/2,
        max(x_labels)+grid_x_resolution/2, 
        min(y_labels)-grid_y_resolution/2,
        max(y_labels)+grid_y_resolution/2
        )
    
    # Create the heatmap plot
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(data, extent=grid_extent, cmap=cmap, aspect='auto', origin='lower', 
                   alpha=alpha)
    ax.set_xticks(x_labels)
    ax.set_yticks(y_labels)
    ax.set_xticklabels(x_labels, fontsize=fontsize_ticklabels)
    ax.set_yticklabels(y_labels, fontsize=fontsize_ticklabels)
    ax.set_xlabel(xlabel, fontsize=fontsize_labels)
    ax.set_ylabel(ylabel, fontsize=fontsize_labels)
    ax.set_title(title, fontsize=fontsize_title)

    # Add the color bar
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.tick_params(labelsize=fontsize_ticklabels)
    cbar.set_label(colorbar_label, fontsize=fontsize_cbar_label)

    # Add a grid to separate the cells
    if grid:
        ax.vlines(x=np.arange(min(x_labels),max(x_labels)+1,grid_x_resolution)+grid_x_resolution/2, 
                 ymin=np.full(len(x_labels), min(y_labels))-grid_y_resolution/2,
                 ymax=np.full(len(x_labels), max(y_labels))+grid_y_resolution/2, color="lightgrey", linewidth=0.3)
        
        ax.hlines(y=np.arange(min(y_labels), max(y_labels)+1)+grid_y_resolution/2,
                 xmin=np.full(len(y_labels), min(x_labels))-grid_x_resolution/2,
                 xmax=np.full(len(y_labels), max(x_labels))+grid_x_resolution/2,
                 color="lightgrey", linewidth=0.3)
    
    fig.tight_layout()

    if savepath:
        plt.savefig(savepath)
    if show:
        plt.show()
    plt.close()

    return fig, ax

if __name__ == "__main__":

    data = np.random.rand(10,10)
    x_labels = np.arange(10)
    y_labels = np.arange(10)
    Heatmap(data, x_labels, y_labels, title='Random data', xlabel='X-axis', ylabel='Y-axis', 
            cmap='coolwarm', colorbar_label='Colorbar label', savepath='../figures/heatmap.png',
            show=True)