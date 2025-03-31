
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def CenteredColorMap(cmap, vmin, vcenter, vmax, start=0, stop=1.0, name='centered_cmap'):
    '''
    Function to offset the "center" of a colormap. Useful for highlighting the change in a variable
    from a reference value. 
    Adapted from https://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
      vmin : the value to be used to match the 'start' of the colormap
      vcenter : the value to be used to match the 'midpoint' of the colormap. Here, the colormap will
              be centered around this value.
      vmax : the value to be used to match the 'stop' of the colormap
    
       Note that 'start' and 'stop' are values in the range [0, 1] that determine how much the colormap
         will be shifted towards the lower and upper limits, while 'vmin', 'vcenter' and 'vmax' 
         are the values that will be used to match the colormap to the data. Typical values for 
         'vmin' and 'vmax' are the minimum and maximum values of the data, while 'vcenter' is the
         value around which the colormap will be centered. Typically, 'vcenter' could be set to 0
         where interested about the analysis of the change of a variable, or to a reference value
         when interested in the deviation from a reference value.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 513)

    # Calculate the index for the midpoint
    midpoint = np.diff([vmin, vcenter])[0] / np.diff([vmin, vmax])[0]


    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 256, endpoint=False), 
        np.linspace(midpoint, 1.0, 257, endpoint=True)
    ])

    
    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)
        #
        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mcolors.LinearSegmentedColormap(name, cdict)

    
    return newcmap