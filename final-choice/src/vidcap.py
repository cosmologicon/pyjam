# Module for capturing video of pygame games running on Linux, by Christopher Night (CC0)
# https://github.com/cosmologicon/pygame-vidcap

# Basic usage:
# 1. sudo apt-get install imagemagick vorbis-tools mencoder
# 2. Place this file into your source directory. Call import vidcap before calling pygame.init().
# 3. Play your game.
# 4. python vidcap.py

# To delete a video and all of its files, simply remove the directory.


# Advanced API:

# vidcap.record() : begin recording
# vidcap.stop() : stop recording
# vidcap.toggle() : toggle recording
# vidcap.cap() : explicitly capture a frame. You don't need to call this directly, it's done
#   automatically whenever you call pygame.display.flip().

# TODO: also wrap pygame.display.update

wrappygame = True  # Should this module wrap pygame.display.flip and pygame.init so that the video
                   # is automatically recorded when you call these functions? If this is False,
                   # you'll need to call vidcap.cap() once per frame
                   # Audio will not work if this is set to False.

viddir = None  # You can set this to an explicit directory path if you like
               # Otherwise it will default to a directory with a current timestamp

recordsymbol = True  # Put a "recording" symbol in the corner when recording
                     # The symbol itself doesn't get recorded

usepng = False  # Use png rather than bmp (takes less disk space but is slower)

drawmouse = True  # Draw the mouse cursor onto the recording

# The fixed framerate of the video to produce. This will change the passage of time during your
# gameplay. Set to None to record realtime.
fps = 25

import pygame, datetime, os, inspect, subprocess, glob


_recording = True
_recordaudio = True
_logging = True

def timestamp(t = None):
    """10-digit timestamp"""
    return "%010d" % (pygame.time.get_ticks() if t is None else t)

def defaultdir():
    """Default (timestamp-based) directory name"""
    return datetime.datetime.now().strftime("vidcap-%Y%m%d%H%M%S")

def checkdir():
    """Make sure viddir is set and the path exists"""
    global viddir
    if viddir is None: viddir = defaultdir()
    if not os.path.exists(viddir):
        os.mkdir(viddir)

def lastdir():
    """The latest timestamp-based directory"""
    dirs = [d for d in os.listdir(".") if d.startswith("vidcap-")]
    return max(dirs) if dirs else None

def currentimagepath(exten = None, t = None):
    checkdir()
    if exten is None: exten = "png" if usepng else "bmp"
    fname = "frame-" + timestamp(t) + "." + exten
    return os.path.join(viddir, fname)

def isimagepath(path, exten = "png"):
    """Does the path describe a timestamped image?"""
    return path.endswith("." + exten) and path[-14:-4].isdigit() and path[-20:-14] == "frame-"

def isaudiopath(path, exten = "ogg"):
    """Does the path describe a timestamped audio?"""
    return path.endswith("." + exten) and path[-14:-4].isdigit() and path[-20:-14] == "audio-"

def blankpath():
    """Pathname of the blank frame"""
    checkdir()
    return os.path.join(viddir, "frame-blank.png")

def makeblankframe(anyframe, color=(0,0,0)):
    """Make the blank frame. Must be passed some image to get the dimensions right"""
    surf = pygame.image.load(anyframe)
    surf.fill(color)
    pygame.image.save(surf, blankpath())

def fadepath(basefile, (r, g, b, a)):
    """Return the path to a copy of the given image overwritten with the given color (and create
    the image if it doesn't exist)"""
    if a == 0: return basefile
    cstr = "0x" + hex((1 << 32) + (r << 24) + (g << 16) + (b << 8) + a)[3:]
    filename = basefile[:-4] + "-" + cstr + basefile[-4:]
    if os.path.exists(filename): return filename
    color = pygame.Color(r, g, b, a)
    img = pygame.image.load(basefile).convert_alpha()
    img2 = img.copy()
    img2.fill(color)
    img.blit(img2, (0, 0))
    pygame.image.save(img, filename)
    return filename

def framelistpath():
    return os.path.join(viddir, "framelist.txt")

def currentaudiopath():
    checkdir()
    return os.path.join(viddir, "audio-%s.raw" % timestamp())

def logpath():
    checkdir()
    return os.path.join(viddir, "log.txt")

def log(line):
    if not _logging: return
    f = open(logpath(), "a")
    f.write(timestamp() + " " + line + "\n")
    f.close()

def getcursorimg(cache = {}):
    key = pygame.mouse.get_cursor()
    if key in cache: return cache[key]
    (mx, my), (hx, hy), xormasks, andmasks = key
    img = pygame.Surface((mx, my)).convert_alpha()
    img.fill((0,0,0,0))
    for y in range(my):
        for x in range(mx):
            j = y * mx + x
            if andmasks[j/8] & (1 << (7-j%8)):
                img.set_at((x, y), (255, 255, 255))
            if xormasks[j/8] & (1 << (7-j%8)):
                img.set_at((x, y), (0, 0, 0))
    cache[key] = img, (hx, hy)
    return cache[key]

_mousevisible = True
def addcursor(surf):
    if drawmouse and _mousevisible and pygame.mouse.get_focused():
        img, (hx, hy) = getcursorimg()
        px, py = pygame.mouse.get_pos()
        rect = img.get_rect(topleft = (px-hx, py-hy))
        surf.blit(img, rect)

pmsvis = pygame.mouse.set_visible
def setmousevis(vis):
    global _mousevisible
    _mousevisible = vis
    return pmsvis

def stop():
    global _recording
    if not _recording: return
    _recording = False
    log("event stop")
    log("event fadetoblack 500")
    log("event fadeoutaudio 500")

def record():
    global _recording
    if _recording: return
    _recording = True
    log("event record")
    log("event fadefromblack 1000")
    log("event fadeinaudio 1000")

def toggle():
    if _recording:
        stop()
    else:
        record()

def getmonitorsource():
    p = subprocess.Popen("pactl list".split(), stdout = subprocess.PIPE)
    out, err = p.communicate()
    mlines = [line for line in out.splitlines() if "Monitor Source: " in line]
#    assert len(mlines) == 1
    mline = mlines[0]
    _, _, monitorsource = mline.partition("Monitor Source: ")
    return monitorsource

def unmutemonitorsource(monitorsource = None):
    if monitorsource is None: monitorsource = getmonitorsource()
    stdin = "set-source-mute %s false" % monitorsource
    p = subprocess.Popen(["pacmd"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    _, _ = p.communicate(stdin)

_audioprocess = None  # Set to None when audio recording is off
                      # Set to the AudioProcess instance when audio recording is in progress
                      # Module-level private because we need it to be GC'd, so please don't make
                      #   reference to it.
class AudioProcess(object):
    """Use RAII to make sure the audio recording gets shut down when we're done"""
    format = "s16ne"
    def __init__(self, filename = None, monitorsource = None):
        self.filename = filename or currentaudiopath()
        self.monitorsource = monitorsource or getmonitorsource()
        self.com = "parec --latency-msec=10 --format=%s --device=%s" % (self.format, self.monitorsource)
        self.com += " --volume=240000"
        log("audiostart %s %s" % (self.filename, self.format))
        self.file = open(self.filename, "wb")
        self.process = subprocess.Popen(self.com.split(), stdout = self.file)
    def terminate(self):
        if self.process:
            log("audiostop")
            self.process.terminate()
            self.process, self.file = None, None
    def __del__(self):
        self.terminate()

def startaudiorecording(filename = None, monitorsource = None):
    global _audioprocess
    if not _recordaudio: return
    if _audioprocess: return  # Already recording
    if monitorsource is None: monitorsource = getmonitorsource()
    unmutemonitorsource(monitorsource)
    _audioprocess = AudioProcess(filename = filename, monitorsource = monitorsource)

def stopaudiorecording():
    global _audioprocess
    _audioprocess.terminate()
    _audioprocess = None

def cap(screen = None):
    """Call this once a frame to capture the screen"""
    if not _recording:
        log("cap")
        return
    if screen is None: screen = pygame.display.get_surface()
    fname = currentimagepath()
    log("cap " + fname)
    addcursor(screen)
    pygame.image.save(screen, fname)
    if recordsymbol and pygame.time.get_ticks() / 250 % 2:
        pygame.draw.circle(screen, (255, 0, 0), (14, 14), 10, 0)
    startaudiorecording()

pdflip = pygame.display.flip
def capandflip():
    cap()
    pdflip()

pinit = pygame.init
def init():
    log("init")
    log("alias pygame.init()")
    startaudiorecording()
    pinit()

ptime = pygame.time
class _WrapTime(object):
    _accumulator = 0
    def Clock(self, *args, **kwargs):
        return _WrapClock(*args, **kwargs)
    def get_ticks(self):
        return self._accumulator
    def __getattr__(self, name):
        return getattr(ptime, name)
class _WrapClock(object):
    def __init__(self, *args, **kwargs):
        self.clock = ptime.Clock(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(self.clock, name)
    def tick(self, *args, **kwargs):
        if fps is not None:
            self.clock.tick(fps)
            dt = int(1000 / fps)
            _WrapTime._accumulator += dt
            return dt
        else:
            return self.clock.tick(*args, **kwargs)

def convertallbmps():
    """Convert all bmps in the vidcap directory into pngs (requires mogrify) - slow!"""
    if not glob.glob(os.path.join(viddir, "*.bmp")): return
    com = "mogrify -format png " + os.path.join(viddir, "*.bmp")
    print com
    os.system(com)
    os.system("rm " + os.path.join(viddir, "*.bmp"))

def convertaudio():
    """Convert raw audio in the vidcap directory into oggs"""
    print "FFFF", os.listdir(viddir)
    for f in os.listdir(viddir):
        if not f.endswith(".raw"): continue
        rawfile = os.path.join(viddir, f)
        oggfile = rawfile[:-4] + ".ogg"
        if os.path.exists(oggfile): continue
#        os.system("sox -r 44100 -e signed-integer -b 16 -c 2 %s %s" % (rawfile, oggfile))
        os.system("oggenc --raw --quiet -o %s %s" % (oggfile, rawfile))

def interpolateframes(fts, nframes, dt, t0 = 0):
    # TODO: better interpolation function
    iframes = []
    index = 1  # The first frame that's later than the current timestamp 
    for jframe in range(nframes):
        t = float(jframe) * dt + t0
        while index < len(fts) and t > fts[index][0]:
            index += 1
        iframes.append([t, fts[index-1][1]])
    return iframes

# The following class is used for logging commands and events needed to re-generate the audio track.
# It creates a series of commands to be exec'd, that *should* produce the same audio as was produced
# during the recording. It does this in a general way by generating references to objects that are
# used and placing them within an array objs. Every time an attribute is accessed, it adds another
# element to the array, and every time a function is called (assuming the arguments are either
# repr-able or LogAlias instances themselves), a line is generated that will reproduce the
# appropriate function call using the objs array. For instance, the following commands made within a
# game:
#     sound1 = pygame.mixer.Sound("abc.wav")
#     sound1.play(10)
# will result in the following logged commands:
#     objs[0] = pygame.mixer
#     objs[1] = objs[0].Sound
#     objs[2] = objs[1]("abc.wav")
#     objs[3] = objs[2].play
#     objs[3](10)

class LogAlias(object):
    """An alias to an object that logs all calls made."""
    _aliasList = {}
    _listname = "objs"  # How the array should be written in the log
    _nAlias = 0
    def __init__(self, obj, name, ongetattr = None):
        self._obj = obj
        self._name = name  # This is a string that can be eval'd to give self._obj later
        self._n = self._nAlias
        self._aliasList[LogAlias._nAlias] = self
        self._log("%s[%s] = %s" % (self._listname, self._n, self._name))
        self._ongetattr = ongetattr  # Callback when self.__getattr__ is called
        LogAlias._nAlias += 1
    @staticmethod
    def _lname(obj):
        """This is the name of this object via the alias list, if applicable"""
        return "%s[%s]" % (LogAlias._listname, obj._n) if isinstance(obj, LogAlias) else repr(obj)
    @staticmethod
    def _cvalue(obj):
        """Wrapped value for a LogAlias object, otherwise the object itself."""
        return obj._obj if isinstance(obj, LogAlias) else obj
    def __getattr__(self, attr):
        """self.x is a LogAlias wrapper around self._obj.x"""
        if self._ongetattr: self._ongetattr()
        if attr not in self.__dict__:
            obj = getattr(self._obj, attr)
            name = LogAlias._lname(self) + "." + attr
            self.__dict__[attr] = LogAlias(obj, name)
        return self.__dict__[attr]
    def __call__(self, *args, **kw):
        argstr = ", ".join(LogAlias._lname(arg) for arg in args)
        kwstr = ", ".join("%s = %s" % (key, LogAlias._lname(value)) for key, value in kw.items())
        callstr = "%s(%s%s%s)" % (LogAlias._lname(self), argstr, (", " if argstr and kwstr else ""), kwstr)
        args = [LogAlias._cvalue(obj) for obj in args]
        kw = { k: LogAlias._cvalue(v) for k, v in kw.items() }
        ret = self._obj(*args, **kw)
        # Need to wrap anything that's not repr-able, in case it gets used in an argument for a
        # later call to a LogAlias object.
        # This test works fine in practice.
        if not isinstance(ret, (int, float, type(None), str, bytes)):
            return LogAlias(ret, callstr)
        self._log(callstr)
        return ret
    def __repr__(self):
        return "LogAlias(%r)" % repr(self._obj)
    def _log(self, text):
        """Add the specified text to the log along with timestamp"""
        log("alias " + text)

_wrapped = False
if __name__ != "__main__":
    if wrappygame and not _wrapped:
        pygame.mixer = LogAlias(pygame.mixer, "pygame.mixer")
        pygame.display.flip = capandflip
        pygame.init = init
        pygame.time = _WrapTime()
        pygame.mouse.set_visible = setmousevis
        _wrapped = True


if __name__ == "__main__":
    # Encode the images and audio into an AVI file
    import sys, numpy

    audiofreq = 44100
    remakeaudio = False
    
    _logging = False
    
    viddir = sys.argv[1] if len(sys.argv) > 1 else lastdir()
    if not viddir:
        print "Vidcap directory not found!"
        print "Please specify a directory on the command line."
        sys.exit()
    print "vidcap directory is %s" % viddir

    print "Converting BMPs into PNGs...."
    convertallbmps()
    
    # Analyze log file
    objs = {}
    logcomms = []
    audiorecs = []
    captimes = []
    events = []
    for line in open(logpath(), "r"):
        words = line.split()
        if len(words) < 2: continue
        t = int(words[0])
        action = words[1]
        if action == "init":
            pass
        if action == "audiostart":
            audiorecs.append((t, words[2]))
        if action == "alias":
            logcomms.append((t, " ".join(words[2:]).strip()))
        if action == "cap":
            captimes.append(t)
        if action == "event":
            events.append((t, " ".join(words[2:]).strip()))

    print "Number of frames captured: %d" % (len(captimes),)

    if fps is not None:
        import bisect
        print "Rescaling timestamps to fixed %.1ffps" % (fps,)
        def fixt(t):
            """Convert a timestamp into a fixed-fps timestamp"""
            dt = 1000. / fps
            i1 = bisect.bisect(captimes, t)
            if i1 == 0: return t - captimes[0]
            if i1 == len(captimes): return (len(captimes) - 1) * dt + t - captimes[-1]
            i0 = i1 - 1
            t0, t1 = captimes[i0], captimes[i1]
            jframe = i0 + (t - t0) / float(t1 - t0)
            return int(jframe * dt)
        audiorecs = [(fixt(t), rec) for t, rec in audiorecs]
        logcomms = [(fixt(t), comm) for t, comm in logcomms]
        events = [(fixt(t), event) for t, event in events]
    events = [(t, event) for t, event in events if t >= 0]

    fades = []
    audiofades = []
    for t, event in events:
        if event.startswith("fadetoblack"):
            dt = int(event.partition(" ")[2])
            fades.append((t-dt, t, 0, 255, 0, 0, 0))
        if event.startswith("fadefromblack"):
            dt = int(event.partition(" ")[2])
            fades.append((t, t+dt, 255, 0, 0, 0, 0))
        if event.startswith("fadeoutaudio"):
            dt = int(event.partition(" ")[2])
            audiofades.append((t-dt, t, 1, 0))
        if event.startswith("fadeinaudio"):
            dt = int(event.partition(" ")[2])
            audiofades.append((t, t+dt, 0, 1))
    
    frames0 = sorted(filter(isimagepath, os.listdir(viddir)))
    fts = [(int(frame[6:16]), os.path.join(viddir, frame)) for frame in frames0]
    if fps is not None:
        fts = [(fixt(t), f) for t, f in fts]
    tend = fts[-1][0]

    if remakeaudio:
        basename = os.path.join(viddir, "audio-re" + str(fps or "") + "-%s.raw")
        print "audio basename", basename
        existing = glob.glob(basename % "*")
        if existing:
            assert len(existing) == 1
            filename = existing[0]
            print "Audio found at %s" % filename
        else:
            filename = basename % timestamp()
            print "Re-recording audio to %s...." % filename
            import time
            t0 = time.time()
            startaudiorecording(filename = filename)
            while pygame.time.get_ticks() < tend:
                pygame.time.delay(1)
                while logcomms and 1000 * (time.time() - t0) >= logcomms[0][0]:
                    t, comm = logcomms.pop(0)
#                    print pygame.time.get_ticks(), int(1000 * (time.time() - t0)), t, comm
                    exec(comm)
            stopaudiorecording()
            print "Recording time: %.3fs" % (time.time() - t0)
            pygame.mixer.quit()
        t = int(filename[-14:-4])
        audiorecs = [(t, filename)]
    else:
        assert len(audiorecs) == 1
        print "Audio found at %s" % audiorecs[0][1]

    starts = [t for t, e in events if e == "record"] or [0]
    ends = [t for t, e in events if e == "stop"] or [tend]
    if min(ends) <= min(starts): starts = [0] + starts
    if max(starts) >= max(ends): ends = ends + [tend]
    intervals = [(start, int((end - start) * fps / 1000.)) for start, end in zip(starts, ends)]

    screensize = pygame.image.load(fts[0][1]).get_size()
    screen = pygame.display.set_mode(screensize)
    makeblankframe(fts[0][1])
    fts = [(-1, blankpath())] + fts

    print "Number of clips: %s" % len(intervals)
    ftlist = []
    for jclip, (start, nframes) in enumerate(intervals):
        print "Number of frames in clip #%s: %s" % (jclip+1, nframes)
        ftlist += interpolateframes(fts, nframes, 1000. / fps, start)
    for j in range(len(ftlist)):
        t, f = ftlist[j]
        for t1, t2, a1, a2, r, g, b in fades:
            if t1 <= t <= t2:
                a = int(a1 + float(t - t1) * (a2 - a1) / (t2 - t1))
                f = fadepath(f, (r, g, b, a))
        ftlist[j] = t, f
    if fades:
        t1, t2, a1, a2, r, g, b = fades[-1]
        t, f = ftlist[-1]
        if t2 > t:
            ftlist.append((t2, fadepath(f, (r, g, b, 255))))

    _, framelist = zip(*ftlist)
    open(framelistpath(), "w").write("\n".join(framelist))

    # TODO: probably not necessary to do this every time
    if False:
        print "Converting frames...."
        for jframe, frame in enumerate(framelist):
            img = pygame.image.load(frame).convert()
            pygame.image.save(img, frame)
            if jframe % 2 == 0:
                screen.blit(img, (0,0))
                pygame.display.flip()

        print "Combining audio..."
        naudiosamp = int(audiofreq * tend / 1000.)
        print "Freq = %s : length = %.2fs : #samp = %d" % (audiofreq, tend / 1000., naudiosamp)
        audioarr = numpy.zeros((naudiosamp, 2), dtype = numpy.int16)
        for t, afilename in audiorecs:
            aclip = numpy.reshape(numpy.fromfile(open(afilename, "rb"), dtype = numpy.int16), (-1, 2))
            print "  Clip: %d samples from %s" % (aclip.shape[0], afilename)
            s0 = int(audiofreq * t / 1000.)
            s1 = s0 + aclip.shape[0]
            if s1 > naudiosamp:
                aclip = aclip[:naudiosamp-s1,]
                s1 = naudiosamp
            audioarr[s0:s1,] = aclip
        for t1, t2, v1, v2 in audiofades:
            s1 = int(audiofreq * t1 / 1000.)
            s2 = int(audiofreq * t2 / 1000.)
            n = s2 - s1
            fac = numpy.transpose([v1 + numpy.arange(n) * ((v2 - v1) / float(n))] * 2)
            if s2 > naudiosamp:
                fac = fac[:naudiosamp-s2,]
                s2 = naudiosamp
    #        print s1, s2, n, audioarr.shape, fac.shape, audioarr[s1:s2,].shape
            audioarr[s1:s2,] *= fac

        print audioarr.shape
        print audioarr[0::2345,0]

    if False:
        rawfile = os.path.join(viddir, "audio.raw")
        oggfile = os.path.join(viddir, "audio.ogg")
        aindices = [(int(audiofreq * t / 1000.), int(nframes * audiofreq / fps)) for t, nframes in intervals]
        numpy.concatenate([audioarr[i:i+j,] for i, j in aindices]).tofile(open(rawfile, "wb"))
    #    audioarr.tofile(open(rawfile, "wb"))

        com = "oggenc --raw --raw-rate=%d -o %s %s" % (audiofreq, oggfile, rawfile)
        print(com)
        os.system(com)
        exit()

    rawfile = os.path.join(viddir, "audio.raw")
    wavfile = os.path.join(viddir, "audio.wav")
    oggfile = os.path.join(viddir, "audio.ogg")
    if False:
        aindices = [(int(audiofreq * t / 1000.), int(nframes * audiofreq / fps)) for t, nframes in intervals]
        numpy.concatenate([audioarr[i:i+j,] for i, j in aindices]).tofile(open(rawfile, "wb"))
        com = "sox -r %d --encoding signed-integer --bits 16 --channels 2 %s %s" % (audiofreq, rawfile, wavfile)
        print(com)
        os.system(com)
	convertaudio()
    
    com = []
    com.append("mencoder")
#    com.append("mf://%s/*.png" % viddir)
    com.append("mf://@%s" % framelistpath())
    com.append("-mf fps=%s:type=png" % fps)
    com.append("-ovc copy")
    com.append("-oac pcm -audiofile %s" % oggfile if oggfile else "-oac copy")
#    com.append("-oac pcm -audiofile %s" % wavfile if wavfile else "-oac copy")
    com.append("-o %s/vidcap.avi" % viddir)

    com = " ".join(com)
    print
    print "Encoding video...."
    print com
    os.system(com)  # TODO: check for errors
    
    print
    print "Video created:", os.path.join(viddir, "vidcap.avi")

