

import matplotlib.pyplot as plt


def TwoVarLineplot(
        array, x_axis, z_dim, title='', ylabel='', xlabel='', colors='k', caption_labels=None,
        threshold=None, color_threshold='red', label_threshold='Target', linewidth=2, figsize=(8, 5), 
        title_fontsize=14, label_fontsize=12, grid=True, facecolor='whitesmoke', 
        legend_facecolor='whitesmoke', subplot_adjust=(None, None, 0.18, None), savepath=None, 
        show=False):

    """ Create line plots for two-dimensional arrays

        Parameters
        ----------

        - array: array
            The array to be plotted. The dimensions must be (x_axis, z_dim)
        - x_axis: list or 1D array 
            List of the x_ticks to be plotted
        - z_dim: list or 1D array 
            List of the 'array' indices on the y-axis to be plotted
        - title: str (Optional)
            Title of the plot. Default is an empty string.
        - ylabel: str (Optional)
            Label of the y-axis. Default is an empty string.
        - xlabel: str (Optional)
            Label of the x-axis. Default is an empty string.
        - caption_labels: str (Optional)
            Label of the captions. This is the label of the lines in the plot that represent 
            the z_dim.
        - colors: str or list (Optional, default is 'k')
            List of colors to be used in the plot. If a str, the same color will be applied to all
            lines. 
        - threshold: float (Optional)
            Value to be plotted as a horizontal line. Default is None, which results in no horizontal
            line being plotted
        - color_threshold: str (Optional, only used if threshold is not None)
            Color of the threshold line. Default is 'red'
        - label_threshold: str (Optional, only used if threshold is not None, default is 'Target')
            Label of the threshold line.
        - linewidth: int (Optional, default is 2)
            Width of the lines
        - figsize: tuple (Optional, default is (8, 5))
            Size of the figure.
        - title_fontsize: int (Optional, default is 14)
            Fontsize of the title. 
        - label_fontsize: int (Optional, default is 12)
            Fontsize of the labels
        - grid: bool (Optional, default is True)
            If True, the grid is plotted. 
        - facecolor: str (Optional, default is 'whitesmoke')
            Background color of the plot.
        - legend_facecolor: str (OPtional, default is 'whitesmoke')
            Background color of the legend. 
        - subplot_adjust: tuple (Optional, default is (None, None, 0.18, None))
            Adjust the subplot (top, right, bottom, left)
        - savepath: str (Optional, default is None)
            Path to save the plot. If None, the figure is not saved
        - show: bool (Optional, default is False)
            If True, the plot is displayed
    """

    try:
        len(x_axis) == array.shape[0]
    except:
        raise ValueError('The x_axis must have the same length as the array')
    
    try:
        len(colors) == len(z_dim)
    except: 
        raise ValueError('The number of colors must be equal to the number of z_dim')
    
    try:
        max(z_dim) < array.shape[1]
    except:
        raise ValueError('The maximum value of z_dim must be less than the number of dimensions of the array')


    fig, ax = plt.subplots(figsize=figsize)

    for z in z_dim:
        if caption_labels:
            label = caption_labels[z]
        else:
            label = None
        ax.plot(x_axis, array[:,z], color=colors[z], label=label, lw=linewidth)

    if threshold:
        ax.axhline(threshold, color=color_threshold, linestyle='--', label=label_threshold)

    ax.set_title(title, fontsize=title_fontsize)
    ax.set_ylabel(ylabel, fontsize=label_fontsize)
    ax.set_xlabel(xlabel, fontsize=label_fontsize)
    
    if facecolor:
        ax.set_facecolor(facecolor)

    if caption_labels:
        handles, labels = ax.get_legend_handles_labels()
        legend = plt.figlegend(handles, labels, columnspacing=0.5, handletextpad=0.5, 
                               loc='lower center', ncol=len(z_dim), bbox_to_anchor=(0.5,-0.004),
                               fontsize=label_fontsize)
        if legend_facecolor:
            legend.get_frame().set_facecolor(legend_facecolor)
        
    if grid:
        ax.grid()

    plt.tight_layout()
    plt.subplots_adjust(top=subplot_adjust[0], 
                        right=subplot_adjust[1], 
                        bottom=subplot_adjust[2], 
                        left=subplot_adjust[3])
    
    if show:
        plt.show()

    if savepath:
        fig.savefig(savepath)
    plt.close()

    return fig, ax

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import seaborn as sns

    # Create a random dataset
    np.random.seed(0)
    x = np.linspace(0, 10, 100)
    y = np.random.rand(100, 5)
    y = np.cumsum(y, axis=0)
    y = y - y.mean(axis=0)

    # Create a random caption
    caption_labels = ['A', 'B', 'C', 'D', 'E']

    # Create a random threshold
    threshold = 0

    # Create a random color
    colors = sns.color_palette('husl', 5)

    TwoVarLineplot(y, x, z_dim=[0, 1, 2, 3, 4], title='Random data', ylabel='Y-axis', xlabel='X-axis',
                   caption_labels=caption_labels, threshold=threshold, colors=colors, 
                   savepath='../figures/TwoVarLineplot.png', show=True)