
import numpy as np
import math
import pandas as pd
from matplotlib import colormaps as cmaps
from CST_PlottingTools.utils import CenteredColorMap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def Heatmap(data, x_labels, y_labels, title='', xlabel='', ylabel='', cmap='coolwarm', colorbar_label='',
            vmin=None, vmax=None, vcenter=None, alpha=1, grid=False, fontsize_labels=13, 
            fontsize_ticklabels=12, fontsize_title=14, fontsize_cbar_label=13, figsize=None, 
            savepath=None, no_change=None, size_no_change_marker=200, contour_levels=None, 
            relative_contours=False, contour_unit=None, contour_linewidth=1, show=False,
            with_gcm_distribution_on_the_side=True, path_deltaT=None, path_deltaP=None,
            sheet_deltaT=None, sheet_deltaP=None, bin_widthT=None, bin_widthP=None, color_gcm=None, 
            color_map_gcm=None, gcm_overlay_heatmap=False):
        
    """ Create a heatmap plot of the data.

        Parameters
        ----------

        - data : 2D array
            The data to be plotted.

        - x_labels : 1D array
            The labels for the x-axis.

        - y_labels : 1D array
            The labels for the y-axis.

        - title : str (Optional)
            The title of the plot.

        - xlabel : str (Optional)
            The label of the x-axis.

        - ylabel : str (Optional)
            The label of the y-axis.

        - cmap : str (Optional; default value is 'coolwarm')
            The colormap to be used.

        - colorbar_label : str (Optional)
            The label of the colorbar.

        - vmin : float (Optional)
            The minimum value of the colorbar.

        - vmax : float (Optional)
            The maximum value of the colorbar.

        - vcenter : float (Optional)
            The center value of the colormap.

        - alpha : float (Optional; default value is 1)
            The transparency of the colors.

        - grid : bool (Optional; default value is False)
            Whether to add a grid to separate the cells.

        - fontsize_labels : int
            The fontsize of the labels.

        - fontsize_ticklabels : int
            The fontsize of the tick labels.

        - fontsize_title : int
            The fontsize of the title.

        - fontsize_cbar_label : int
            The fontsize of the colorbar label.

        - figsize : tuple
            The size of the figure.

        - savepath : str
            The path to save the figure.

        - no_change : tuple (Optional, default value is None)
            Coordinates of the 'no change' scenario.

        - size_no_change_marker : int (Optional, default value is 200)
            Size of the marker for the 'no change' scenario.

        - contour_levels : list (Optional, default value is None)
            List of levels to be plotted as contours. If relative_contours is True, the levels are
            relative to the data and must be expressed in percentage of the 'vcenter' value.
            For example, [-5, 0, 5] will plot contours at -5%, 0% and 5% of the 'vcenter' value.

        - relative_contours : bool (Optional, default value is False)
            Whether the contours are relative to the data.

        - contour_unit : str (Optional, default value is None)
            Unit of the contours.

        - contour_linewidth : float (Optional, default value is 1)
            Width of the contour lines.

        - show : bool
            Whether to show the plot.

        - with_gcm_distribution_on_the_side: bool (Optional, default is True)
            If True, the GCM distribution is plotted on the side of the plot. This function requires
            delta change factors to be pre-processed (typically using the 'ClimProjTools' package:
            https://github.com/BaptisteFrancois/ClimProjTools/tree/main). Delta change factors can
            be generated using another way, but the format must be the same as the one generated by
            the 'ClimProjTools' package.

        - path_deltaT: str (Optional)
            Path to the 'path_delta_change' file containing the delta change factors for temperature.

        - path_deltaP: str (Optional)
            Path to the 'path_delta_change' file containing the delta change factors for precipitation.

        - sheet_deltaT: str (Optional, default is None)
            Name of the sheet containing the delta change factors for temperature.

        - sheet_deltaP: str (Optional, default is None)
            Name of the sheet containing the delta change factors for precipitation.

        - bin_widthT: float (Optional, default is None)
            Width of the bins for the temperature distribution. If None, a default number of bins
            is used (20)

        - bin_widthP: float (Optional, default is None)
            Width of the bins for the precipitation distribution. If None, a default number of bins
            is used (20)

        - color_gcm: list (Optional, default is None)
            List of colors to be used for the GCM distribution. If None, the colors are generated
            from the 'YlOrBr' colormap.

        - color_map_gcm: str (Optional, default is None)
            Colormap to be used for the GCM distribution. If None, the 'YlOrBr' colormap is used.

        - gcm_overlay_heatmap: bool (Optional, default is False)
            If True, the GCM projections are overlayed on the heatmap.
    """
    # Check that labels are regularly spaced
    if not np.all(np.diff(x_labels) == np.diff(x_labels)[0]):
        raise ValueError('x_labels must be regularly spaced.')
    if not np.all(np.diff(y_labels) == np.diff(y_labels)[0]):
        raise ValueError('y_labels must be regularly spaced.')

    if with_gcm_distribution_on_the_side == False:
        if figsize is None:
            figsize = (6,6)
    elif with_gcm_distribution_on_the_side == True:
        if figsize is None:
            figsize = (8, 8)

    # Get the colormap
    if vcenter is not None:
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

    # Calculate the extent of the grid
    grid_x_resolution = np.diff(x_labels)[0]
    grid_y_resolution = np.diff(y_labels)[0]
    grid_extent = (
        min(x_labels)-grid_x_resolution/2,
        max(x_labels)+grid_x_resolution/2, 
        min(y_labels)-grid_y_resolution/2,
        max(y_labels)+grid_y_resolution/2
        )
    
    if with_gcm_distribution_on_the_side == False:
        
        # Create the heatmap plot
        fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
        im = ax.imshow(data, extent=grid_extent, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto', origin='lower', 
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
            
        # Add contours
        if contour_levels is not None:
            if relative_contours:
                if not vcenter:
                    raise ValueError('The colormap must be centered to plot relative contours.')
                levels = [vcenter + vcenter*level/100 for level in contour_levels]
            else:
                levels = contour_levels
            cp = ax.contour(x_labels, y_labels, data, levels=levels, colors='black',
                            linewidths=contour_linewidth)
            
            if contour_unit:
                # Add the unit to the contour labels
                contour_labels = [str(level)+' '+contour_unit for level in contour_levels]
            else:
                contour_labels = [str(level) for level in contour_levels]

            if relative_contours:    
                # Add a '+' sign to positive values
                contour_labels = \
                    ['+'+str(level) if not str(level).startswith('-') else str(level) for level in contour_labels]
            
            fmt = {}
            for l, s in zip(cp.levels, contour_labels):
                fmt[l] = s
            ax.clabel(cp, cp.levels, inline=1, fontsize=fontsize_ticklabels, fmt=fmt)
                
        # Add a star symbol to the 'no change' scenario
        if no_change:
            ax.scatter(no_change[0], no_change[1], marker='*', s=size_no_change_marker, color='yellow', 
                    edgecolors='black', zorder=10)
            

    elif with_gcm_distribution_on_the_side == True:

        fig = plt.figure(figsize=figsize, constrained_layout=True)
        gs = fig.add_gridspec(nrows=2, ncols=3, width_ratios=[2, 16, 0.75], height_ratios=[16, 2])

        ax1 = fig.add_subplot(gs[0:-1, 1]) # Main scatter plot
        ax2 = fig.add_subplot(gs[1, 1], sharex=ax1) # GCM distribution on the bottom
        ax3 = fig.add_subplot(gs[0:-1, 0], sharey=ax1) # GCM distribution on the side
        cbar_ax = fig.add_subplot(gs[0:-1, 2]) # Colorbar    

        # Create the heatmap plot
        im = ax1.imshow(data, extent=grid_extent, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto', origin='lower', 
                    alpha=alpha)
        ax1.set_xticks(x_labels)
        ax1.set_yticks(y_labels)
        ax1.set_xticklabels(x_labels, fontsize=fontsize_ticklabels)
        ax1.set_yticklabels(y_labels, fontsize=fontsize_ticklabels)

        # Create colorbar
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.set_label(colorbar_label, fontsize=fontsize_cbar_label)
        

        # Add a grid to separate the cells
        if grid:
            ax1.vlines(x=np.arange(min(x_labels),max(x_labels)+1,grid_x_resolution)+grid_x_resolution/2, 
                    ymin=np.full(len(x_labels), min(y_labels))-grid_y_resolution/2,
                    ymax=np.full(len(x_labels), max(y_labels))+grid_y_resolution/2, color="lightgrey", linewidth=0.3)
            
            ax1.hlines(y=np.arange(min(y_labels), max(y_labels)+1)+grid_y_resolution/2,
                    xmin=np.full(len(y_labels), min(x_labels))-grid_x_resolution/2,
                    xmax=np.full(len(y_labels), max(x_labels))+grid_x_resolution/2,
                    color="lightgrey", linewidth=0.3)
            
        # Add contours
        if contour_levels is not None:
            if relative_contours:
                if not vcenter:
                    raise ValueError('The colormap must be centered to plot relative contours.')
                levels = [vcenter + vcenter*level/100 for level in contour_levels]
            else:
                levels = contour_levels
            cp = ax1.contour(x_labels, y_labels, data, levels=levels, colors='black',
                            linewidths=contour_linewidth)
            
            if contour_unit:
                # Add the unit to the contour labels
                contour_labels = [str(level)+' '+contour_unit for level in contour_levels]
            else:
                contour_labels = [str(level) for level in contour_levels]

            if relative_contours:    
                # Add a '+' sign to positive values
                contour_labels = \
                    ['+'+str(level) if not str(level).startswith('-') else str(level) for level in contour_labels]
            
            fmt = {}
            for l, s in zip(cp.levels, contour_labels):
                fmt[l] = s
            ax1.clabel(cp, cp.levels, inline=1, fontsize=fontsize_ticklabels, fmt=fmt)
                
        # Add a star symbol to the 'no change' scenario
        if no_change:
            ax1.scatter(no_change[0], no_change[1], marker='*', s=size_no_change_marker, color='yellow', 
                    edgecolors='black', zorder=10)
            
        # Read the delta change factors
        deltaT = pd.read_excel(path_deltaT, sheet_name=f'{sheet_deltaT}', index_col='GCM')
        deltaP = pd.read_excel(path_deltaP, sheet_name=f'{sheet_deltaP}', index_col='GCM')

        # Find common models
        common_models = deltaT.index.intersection(deltaP.index)
        deltaT = deltaT.loc[common_models]
        deltaP = deltaP.loc[common_models]

        # Set the bins
        if bin_widthT is None:
            bins_T = 20
        else:
            bins_T = np.arange(y_labels.min(), y_labels.max(), bin_widthT)

        if bin_widthP is None:
            bins_P = 20
        else:
            bins_P = np.arange(x_labels.min(), x_labels.max(), bin_widthP)

        if len(deltaT.columns) == 1:
            alpha = [1]
        else:
            alpha = [1, 0.5]

        # Set the colors
        if color_gcm is not None:
            if len(color_gcm) != len(deltaT.columns):
                raise ValueError('The number of colors must be the same as the number of periods')
            else:
                color_gcm_hist = color_gcm
        else:
            # Generate a list of colors from the 'YlGnBU' colormap. The list has the same length as the number of periods
            if color_map_gcm is not None:
                color_gcm_hist = \
                    plt.cm.get_cmap(color_map_gcm)(np.linspace(0, 1, len(deltaT.columns)))
            else:
                color_gcm_hist = plt.cm.YlOrBr(np.linspace(0, 1, len(deltaT.columns)))

        for k, period in enumerate(deltaT.columns):
            
            if gcm_overlay_heatmap:
                ax1.scatter(deltaP[period], deltaT[period], s=120, c=color_gcm_hist[k], edgecolors='k', 
                            label=period, zorder=2)
            ax2.hist(deltaP[period].values.flatten(), bins=bins_P, color=color_gcm_hist[k], edgecolor='k', 
                     alpha=alpha[k], label=period)
            ax3.hist(deltaT[period].values.flatten(), bins=bins_T, color=color_gcm_hist[k], edgecolor='k', 
                     alpha=alpha[k], orientation='horizontal', label=period)
        

        plt.suptitle(title, fontsize=fontsize_title)

        ax2.set_xlabel(r'$\Delta P\ (\%)$', fontsize=fontsize_labels)
        ax2.set_ylabel('Nb of GCMs', fontsize=11)
        ax2.legend(fontsize=10)

        ax3.set_ylabel(r'$\Delta T\ (C)$', fontsize=fontsize_labels)
        ax3.set_xlabel('Nb of GCMs', fontsize=11)    

    #fig.tight_layout()

    if savepath:
        fig.savefig(savepath)
    if show:
        plt.show()
    plt.close()

    if with_gcm_distribution_on_the_side == False:
        return fig, ax, cbar
    else:
        return fig, ax1, ax2, ax3, cbar_ax

if __name__ == "__main__":

    data = np.random.rand(10,10)
    x_labels = np.arange(10)
    y_labels = np.arange(10)
    Heatmap(data, x_labels, y_labels, title='Random data', xlabel='X-axis', ylabel='Y-axis', 
            cmap='coolwarm', colorbar_label='Colorbar label', savepath='../figures/heatmap.png',
            alpha=1, grid=True, fontsize_labels=13,
            show=True, with_gcm_distribution_on_the_side=False)
    
    data = np.random.rand(9,10)
    x_labels = np.arange(-40,41,10)
    y_labels = np.arange(10)
    Heatmap(data, 
            x_labels,
             y_labels, title='Random data', xlabel='X-axis', ylabel='Y-axis', 
            cmap='coolwarm', colorbar_label='Colorbar label', savepath='../figures/heatmap_w_GCMs.png',
            show=True, with_gcm_distribution_on_the_side=True, 
            path_deltaT='../test/data/delta_tas.xlsx',
            path_deltaP='../test/data/delta_prcp.xlsx',
            sheet_deltaT='Delta T (C) -- ssp5_8_5', 
            sheet_deltaP='Delta P (%) -- ssp5_8_5',
            bin_widthT = 0.5,
            bin_widthP = 2.5,
            gcm_overlay_heatmap=True)
    
    data = np.array(pd.read_csv('../test/data/example_CRF.csv', index_col='prcp'))
    Heatmap(data.T, 
            x_labels= np.arange(-30,31,5),
            y_labels= np.arange(0,7,1),
            vmin=data.min(), vmax=data.max(), vcenter=data[6,0],
            title='Compact Flows Early Delta', xlabel='X-axis', ylabel='Y-axis', 
            cmap='coolwarm', colorbar_label='Colorbar label',
            show=True, with_gcm_distribution_on_the_side=False,
            savepath='../figures/heatmap_colorbar_centered_on_selected_value.png')