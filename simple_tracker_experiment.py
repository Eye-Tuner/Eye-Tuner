# edited to be compatible with python 3.8
# example script for using PyGaze
import random
import sys


# 이 class 내용은 constants.py 라는 모듈 내용이었는데 제가 한 파일로 합쳤어요
class _Constant:
    __getattribute__ = object.__getattribute__
    __doc__ = """instead of importing constants.py file, I made settings class and registered it into sys.modules.
default way to set constants is making constants.py file in base directory,
and importing that module in main function: >>> import constants

maybe settings below seems to be retrieved from pygaze.defaults: the default setting module is pygaze.defaults
"""

    # MAIN
    DUMMYMODE = True  # False for gaze contingent display, True for dummy mode (using mouse or joystick)
    LOGFILENAME = 'default'  # logfilename, without path
    LOGFILE = LOGFILENAME[:]  #
    # .txt; adding path before logfilename is optional;
    # logs responses (NOT eye movements, these are stored in an EDF file!)
    TRIALS = 5

    # DISPLAY
    # used in libscreen, for the *_display functions. The values may be adjusted,
    # but not the constant's names
    SCREENNR = 0  # number of the screen used for displaying experiment
    DISPTYPE = 'pygame'  # either 'psychopy' or 'pygame'
    DISPSIZE = (1920, 1080)  # canvas size
    SCREENSIZE = (34.5, 19.7)  # physical display size in cm
    MOUSEVISIBLE = False  # mouse visibility
    BGC = (125, 125, 125, 255)  # backgroundcolour
    FGC = (0, 0, 0, 255)  # foregroundcolour

    # SOUND
    # defaults used in libsound. The values may be adjusted, but not the constants'
    # names
    SOUNDOSCILLATOR = 'sine'  # 'sine', 'saw', 'square' or 'whitenoise'
    SOUNDFREQUENCY = 440  # Herz
    SOUNDLENGTH = 100  # milliseconds (duration)
    SOUNDATTACK = 0  # milliseconds (fade-in)
    SOUNDDECAY = 5  # milliseconds (fade-out)
    SOUNDBUFFERSIZE = 1024  # increase if playback is choppy
    SOUNDSAMPLINGFREQUENCY = 48000  # samples per second
    SOUNDSAMPLESIZE = -16  # determines bit depth (negative is signed
    SOUNDCHANNELS = 2  # 1 = mono, 2 = stereo

    # INPUT
    # used in libinput. The values may be adjusted, but not the constant names.
    MOUSEBUTTONLIST = None  #
    # None for all mouse buttons; list of numbers for buttons of choice (e.g. [1,3] for buttons 1 and 3)
    MOUSETIMEOUT = None  # None for no timeout, or a value in milliseconds
    KEYLIST = None  #
    # None for all keys; list of keynames for keys of choice (e.g. ['space','9',':'] for space, 9 and ; keys)
    KEYTIMEOUT = 1  # None for no timeout, or a value in milliseconds
    JOYBUTTONLIST = None  #
    # None for all joystick buttons; list of button numbers (start counting at 0) for buttons of choice
    # (e.g. [0,3] for buttons 0 and 3 - may be reffered to as 1 and 4 in other programs)
    JOYTIMEOUT = None  # None for no timeout, or a value in milliseconds

    # EYETRACKER
    # general
    TRACKERTYPE = 'smi'  #
    # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
    SACCVELTHRESH = 35  # degrees per second, saccade velocity threshold
    SACCACCTHRESH = 9500  # degrees per second, saccade acceleration threshold
    # EyeLink only
    # SMI only
    SMIIP = '127.0.0.1'
    SMISENDPORT = 4444
    SMIRECEIVEPORT = 5555

    # FRL
    # Used in libgazecon.FRL. The values may be adjusted, but not the constant names.
    FRLSIZE = 200  # pixles, FRL-size
    FRLDIST = 125  # distance between fixation point and FRL
    FRLTYPE = 'gauss'  # 'circle', 'gauss', 'ramp' or 'raisedCosine'
    FRLPOS = 'center'  #
    # 'center', 'top', 'topright', 'right', 'bottomright', 'bottom', 'bottomleft', 'left', or 'topleft'

    # CURSOR
    # Used in libgazecon.Cursor. The values may be adjusted, but not the constants' names
    CURSORTYPE = 'cross'  # 'rectangle', 'ellipse', 'plus' (+), 'cross' (X), 'arrow'
    CURSORSIZE = 20  # pixels, either an integer value or a tuple for width and height (w,h)
    CURSORCOLOUR = 'pink'  # colour name (e.g. 'red'),
    # a tuple RGB-triplet (e.g. (255, 255, 255) for white or (0,0,0) for black),
    # or a RGBA-value (e.g. (255,0,0,255) for red)
    CURSORFILL = True  # True for filled cursor, False for non filled cursor
    CURSORPENWIDTH = 3  # cursor edge width in pixels (only if cursor is not filled)


sys.modules['constants'] = _Constant  # NOQA
del _Constant
import constants  # noqa


# 이거 먼저 해야 pygaze 오류 안 나요
def patch_pygaze_libtime():
    import sys
    import time
    from pygaze._time import pygametime  # NOQA
    old_class = pygametime.PyGameTime
    def new_constructor(self):  # NOQA
        old_class.__init__(self)
        # On Windows, time.clock() provides higher accuracy than time.time().
        if sys.platform == "win32":
            self._cpu_time = time.perf_counter
        else:
            self._cpu_time = time.time
    time.clock = time.perf_counter  # Patch time module first
    pygametime.PyGameTime = type('PyGameTime', (old_class,), {'__init__': new_constructor})  # Patch pygametime module
    return pygametime  # return patched module


patch_pygaze_libtime()

from pygaze import libscreen
from pygaze import libtime
from pygaze import liblog
from pygaze import libinput
from pygaze import eyetracker

# # # # #
# experiment setup

# start timing
libtime.expstart()

# create display object
disp = libscreen.Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# create keyboard object
keyboard = libinput.Keyboard(keylist=['space'], timeout=None)

# create logfile object
log = liblog.Logfile()
log.write(["trialnr", "trialtype", "endpos", "latency", "correct"])

# create screens
inscreen = libscreen.Screen()
inscreen.draw_text(
    text="When you see a cross, look at it and press space. Then make an eye movement to the black circle when it appears.\n\n(press space to start)",
    fontsize=24)
fixscreen = libscreen.Screen()
fixscreen.draw_fixation(fixtype='cross', pw=3)
targetscreens = {}
targetscreens['left'] = libscreen.Screen()
targetscreens['left'].draw_circle(pos=(int(constants.DISPSIZE[0] * 0.25), constants.DISPSIZE[1] / 2), fill=True)
targetscreens['right'] = libscreen.Screen()
targetscreens['right'].draw_circle(pos=(int(constants.DISPSIZE[0] * 0.75), constants.DISPSIZE[1] / 2), fill=True)
feedbackscreens = {}
feedbackscreens[1] = libscreen.Screen()
feedbackscreens[1].draw_text(text='correct', colour=(0, 255, 0), fontsize=24)
feedbackscreens[0] = libscreen.Screen()
feedbackscreens[0].draw_text(text='incorrect', colour=(255, 0, 0), fontsize=24)

# # # # #
# run the experiment

# calibrate eye tracker
tracker.calibrate()

# show instructions
disp.fill(inscreen)
disp.show()
keyboard.get_key()

# run 20 trials
for trialnr in range(1, 21):
    # prepare trial
    trialtype = random.choice(['left', 'right'])

    # drift correction
    checked = False
    while not checked:
        disp.fill(fixscreen)
        disp.show()
        checked = tracker.drift_correction()

    # start eye tracking
    tracker.start_recording()
    tracker.status_msg("trial %d" % trialnr)
    tracker.log("start_trial %d trialtype %s" % (trialnr, trialtype))

    # present fixation
    disp.fill(screen=fixscreen)
    disp.show()
    tracker.log("fixation")
    libtime.pause(random.randint(750, 1250))

    # present target
    disp.fill(targetscreens[trialtype])
    t0 = disp.show()
    tracker.log("target %s" % trialtype)

    # wait for eye movement
    t1, startpos = tracker.wait_for_saccade_start()
    endtime, startpos, endpos = tracker.wait_for_saccade_end()

    # stop eye tracking
    tracker.stop_recording()

    # process input:
    if (trialtype == 'left' and endpos[0] < constants.DISPSIZE[0] / 2) or (
            trialtype == 'right' and endpos[0] > constants.DISPSIZE[0] / 2):
        correct = 1
    else:
        correct = 0

    # present feedback
    disp.fill(feedbackscreens[correct])
    disp.show()
    libtime.pause(500)

    # log stuff
    log.write([trialnr, trialtype, endpos, t1 - t0, correct])

# end the experiment
log.close()
tracker.close()
disp.close()
libtime.expend()
