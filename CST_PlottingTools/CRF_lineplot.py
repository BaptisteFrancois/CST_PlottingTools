

import matplotlib.pyplot as plt


def TwoVarLineplot(
        array, x_axis, z_dim, title='', ylabel='', xlabel='', colors='k', caption_labels=None,
        threshold=None, color_threshold='red', label_threshold='Target', linewidth=2, figsize=(8, 5), 
        title_fontsize=14, label_fontsize=12, grid=True, facecolor='whitesmoke', 
        legend_facecolor='whitesmoke', subplot_adjust=(None, None, 0.18, None), savepath=None, 
        show=False):

    """ Create line plots for two-dimensional arrays
        - array: numpy array. The array to be plotted. The dimensions must be (x_axis, z_dim)
        - x_axis: list or one-dimensional numpy array. List of the xticks to be plotted
        - z_dim: list or one-dimensional numpy array. List of the 'array' indices on the y-axis to be plotted
        - title: str. Title of the plot. Default is an empty string.
        - ylabel: str. Label of the y-axis. Default is an empty string.
        - xlabel: str. Label of the x-axis. Default is an empty string.
        - caption_labels: str or None. Label of the captions. This is the label of the lines in the 
                          plot that represent the z_dim. If None, no label is plotted
        - colors: str or list. List of colors to be used in the plot. If a str, the same color will 
                  be applied to all lines. Default value is 'k' (black).
        - threshold: float. Value to be plotted as a horizontal line. Default is None, which results
                     in no horizontal line being plotted
        - color_threshold: str. Color of the threshold line. Default is 'red'
        - label_threshold: str. Label of the threshold line. Default is 'Target'
        - linewidth: int. Width of the lines. Default is 2
        - figsize: tuple. Size of the figure. Default is (12, 6).
        - title_fontsize: int. Fontsize of the title. Default is 14.
        - label_fontsize: int. Fontsize of the labels. Default is 12.
        - grid: bool. If True, the grid is plotted. Default is True
        - facecolor: str. Background color of the plot. Default is 'whitesmoke'
        - legend_facecolor: str. Background color of the legend. Default is 'whitesmoke'
        - subplot_adjust: tuple. Adjust the subplot (top, right, bottom, left).
                          Default is (None, None, 0.18, None) 
        - savepath: str. Path to save the plot. Default is None, which would result in the plot 
                    being displayed but not saved
        - show: bool. If True, the plot is displayed. Default is True
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