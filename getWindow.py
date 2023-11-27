def getWindow(**kwargs):

    from psychopy import logging, clock, visual

    if 'useMetropsis' in kwargs:
        if kwargs['useMetropsis']:
            screenNumber = 1
            screenSize = [1920, 1080]
            screenDiagonal_cm = 31.5 * 2.54
        else:
            screenNumber = 0
            screenSize = [1440, 900]
            screenDiagonal_cm = 13.3 * 2.54
    else: # No 'useMetropsis' specified; using default 'useMetropsis' True
        screenNumber = 1
        screenSize = [1920, 1080]
        screenDiagonal_cm = 31.5 * 2.54

    if 'useFullScreen' in kwargs:
        if kwargs['useFullScreen']:
            fullScreen = True
        else:
            fullScreen = False
    else: # No 'fullScreen' option specified; using default 'fullScreen' = True
        fullScreen = True

    units = 'pix'

    mywin = visual.Window(screenSize, fullscr=fullScreen, monitor='testMonitor', screen=screenNumber,
                          units=units)

    return mywin, screenSize, fullScreen, screenNumber, screenDiagonal_cm, units