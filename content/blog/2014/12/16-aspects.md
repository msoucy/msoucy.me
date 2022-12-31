---
Title: Aspect-based events in Python
categories: [code]
Date: "2014-12-16"
Tags:
- advfoss
---

*This post is modified from a [presentation](/seminars/aspects) I gave a while back*

# What are events?

The super simple explanation, is "when this, do this"

Basically, functions are added to a "callback list" that happen when an event is triggered

```python
def foo():
	print("Hello, events!")

myButton.onClick.add(foo)
```

# What is the Observer pattern?

Events are sort of a variation of the observer pattern.

Observer:

> It's not about calling a function, it's about sending a message...
> - The Programming Joker

Basically, a class registers itself to receive messages when something changes.

---

# What are aspects?

Aspects are "cross-cutting concerns"

Things that weave their way throughout the program, for instance:

- Logging
- Security/access restriction

```python
# In a totally-made-up "AspectPY", based on AspectJ
# (There IS a real AspectPY, but I haven't looked at it yet)
class MyAdvice(apy.Aspect):
	my_pointcut = apy.call("itertools.*")

	@apy.before(my_pointcut, target="target")
	def my_advice(self, **env):
		print("Calling", env["target"])

itertools.chain("abc", "def")
# Prints: `Calling itertools.chain`
```

---

# How do these two work together?

I was refactoring code for a project, when I encountered this:

```python
class Harold(object):

    def __init__(self, mplfifo, ser, mpout, beep=True):
        self.playing = False
        self.mixer = Mixer(control='PCM')
        self.fifo = mplfifo
        self.ser = ser
        self.mpout = mpout
        self.beep = beep

    def write(self, *args, **kwargs):
        delay = kwargs.pop("delay", 0.5)
        kws = {"file": self.fifo}
        kws.update(kwargs)
        print(*args, **kws)
        time.sleep(delay)

    def __call__(self):
        if not self.playing:
            userlog = open("/home/pi/logs/user_log.csv", "a")
            # Lower the volume during quiet hours... Don't piss off the RA!
            self.mixer.setvolume(85 if quiet_hours() else 100)
            varID = self.ser.readline()
            print(varID)
            # mplayer will play any files sent to the FIFO file.
            if self.beep:
                self.write("loadfile", DING_SONG)
            if "ready" not in varID:
                # Turn the LEDs off
                GPIO.output(7, False)
                GPIO.output(11, False)
                # Get the username from the ibutton
                uid, homedir = read_ibutton(varID)
                # Print the user's name (Super handy for debugging...)
                print("User: '" + uid + "'\n")
                song = get_user_song(homedir)
                print("Now playing '" + song + "'...\n")
                varID = varID[:-2]
                userlog.write("\n" + time.strftime('%Y/%m/%d %H:%M:%S') + "," + varID + "," + uid + "," + song)
                self.write("loadfile '" + song.replace("'", "\\'") + "'\nget_time_length",
                           delay=0.0)

                line = self.mpout.readline()
                while not line.startswith("ANS_LENGTH="):
                    line = self.mpout.readline()
                duration = float(line.strip().split("=")[-1])

                self.starttime = time.time()
                self.endtime = time.time() + min(30, duration)
                self.playing = True
                userlog.close()
        elif time.time() >= self.endtime:
            self.write("stop")
            self.playing = False
            self.ser.flushInput()
            GPIO.output(7, True)
            GPIO.output(11, True)
            print("Stopped\n")

        elif time.time() >= self.starttime+28:
            # Fade out the music at the end.
            vol = int(self.mixer.getvolume()[0])
            while vol > 60:
                vol -= 1 + (100 - vol)/30.
                self.mixer.setvolume(int(vol))
                time.sleep(0.1)
```

This code has all of these together:

- GPIO
- Serial I/O
- ALSA volume management
- Logging
- etc...

Wait! "Logging" was a "cross-cutting concern" mentioned before.
Yet, "Logging" was spread throughout the entire codebase

---

# Splitting out logging and other "cross-cutting" concerns

Let's not care about calling them, at first.

```python
class LogFileAspect(HaroldAspect):
    def __init__(self, logfn):
        self.logfile = open(logfn, "a")
    def on_play(self, varID, uid, song):
		# I know...legacy reasons. I'll switch to csv module soon
        print(time.strftime('%Y/%m/%d %H:%M:%S,{0},{1},{2}'
              .format(varID, uid, song)), file=self.logfile)
    def on_terminate(self):
        self.logfile.close()

# Different circumstances trigger different GPIO reactions:
class GPIOAspect(HaroldAspect):
    def __init__(self, *pins):
        self.pins = pins
        GPIO.setmode(GPIO.BOARD)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, True)
    def setPins(self, val):
        for pin in self.pins:
            GPIO.output(pin, val)
    def on_play(self, varID, uid, song):
        self.setPins(False)
    def on_stop(self):
        self.setPins(True)
```

---

# What did these have in common?

Notice the `on_play` functions:

```python
class LogFileAspect(HaroldAspect):
	# ...
    def on_play(self, varID, uid, song):
		# I know...legacy reasons. I'll switch to csv module soon
        print(time.strftime('%Y/%m/%d %H:%M:%S,{0},{1},{2}'
              .format(varID, uid, song)), file=self.logfile)
# ...
class GPIOAspect(HaroldAspect):
	# ...
    def on_play(self, varID, uid, song):
        self.setPins(False)
```

Both happen at the "same time", or when the same thing triggers them!

Since they're "cross-cutting concerns", it doesn't REALLY matter which one happens in which order.

---

# Triggering our events

We have cross-cutting concerns located in their own aspect classes

Let's make a function to call them:

```python
class AspectWeaver(object):
	def trigger(self, func, *args, **kwargs):
		for a in self.aspects:
			if hasattr(a, "on_"+func):
				getattr(a, "on_"+func)(*args, **kwargs)
```

---

# What happened to aspects?

The two were put together pretty seamlessly:

- Aspects are used to isolate sets of commands (`template method` design pattern)
	- Aspects "horizontal" on a grid
- Events are used to trigger sets of aspects
	- Events "vertical" on a grid

---

# Unplanned design

The original code was designed as "what's architecture?"

- This wasn't planned to be "Event/Aspect" oriented
- Partway through a refactor, "pivoted" to fit the paradigm better

---

# Why does this design rock?

Code for each subsystem (GPIO, logging, etc) is in one place

Code triggering parts of each subsystem is in one place:

```python
class Harold(AspectWeaver):
     def __call__(self):
         if not self.playing:
			 # ...
             self.trigger("play", varID, uid, song)
             self.playing = True

         elif time.time() >= self.endtime:
             self.trigger("stop")
             self.playing = False

         elif time.time() >= self.fadetime:
             # Fade out the music at the end.
             self.trigger("fade")

```

---

# Why does this design not work all the time?

- Any sort of "inter-Aspect communication" requires intermediaries
	- Might not be considered "separate aspects" if that's needed
- Requires more thinking about "fitting code into a location"
- Reading through code relies on knowing which aspects are used/where they're declared

---

# Events vs AOP vs my design

- My `self.trigger` is a "call all aspects here"
- An AOP "Pointcut" injects itself into locations instead of relying on being called
- AOP allows you to introduce behavior `before/after/around` arbitrary calls
	- Python has decorators as a sort of `around`
	- My design's `trigger` is essentially `before` calls for `lambda:None`{.python}
- AOP allows adding methods/values to classes
	- Monkey Patching, so built-in language support

---

# Future work

- Use exceptions to allow for more discrete control
	- Return values
	- Better simulate `around` pointcuts
