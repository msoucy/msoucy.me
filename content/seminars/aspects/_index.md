+++
title = "Aspect-based events in Python"
author = "Matt Soucy"
outputs = ["Reveal"]
date = "December 9, 2014"
+++

# What are events?

The super simple explaination: "on this, do this"

Functions are added to a "callback list" that happen when an event is triggered

---

# Event sample usage

```python
def foo():
	print("Hello, events!")

myButton.onClick.add(foo)
```

---

# Observer pattern

Events are sort of a variation of the observer pattern

Observer:

> It's not about calling a function, it's about sending a message...

Observer/events about "something alerts callbacks that something changed/happened"

---

# What are aspects?

Aspects are "cross-cutting concerns"

Things that weave their way throughout the program:

- Logging
- Security/access restriction

---

# Sample aspect usage

```python
# In a totally-made-up "AspectPY", based on AspectJ
class MyAdvice(apy.Aspect):
	my_pointcut = apy.call("itertools.*")

	@apy.before(my_pointcut, target="target")
	def my_advice(self, **env):
		print("Calling", env["target"])

itertools.chain("abc", "def")
# Prints: `Calling itertools.chain`
```

---

# Why are these two in one presentation?

When refactoring code, you might accidentally stumble upon this.

[Original motivation](https://github.com/msoucy/Harold/blob/4f002f714bce7761d152bead3e870acf1a7656cb/main.py)

This code has all of these together:

- GPIO
- Serial I/O
- ALSA volume management
- Logging
- etc...

---

# Wait!

"Logging" was a "cross-cutting concern"

> Aspects

"Logging" was spread throughout the entire codebase

---

# Splitting logging out

Let's not care about calling it, at first.

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
```

---

# Other "cross-cutting" concerns

GPIO is a nice one

Different circumstances trigger different GPIO reactions:

```python
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

Both happen at the "same time"!

---

# Triggering our events

We have cross-cutting concerns located in their own aspect classes

Let's make a function to call them:

```python
class AspectWeaver(object):
	# ...
	def trigger(self, func, *args, **kwargs):
		for a in self.aspects:
			if hasattr(a, "on_"+func):
				getattr(a, "on_"+func)(*args, **kwargs)
```

---

# What happened to aspects?

The two were put together pretty seamlessly:

- Aspects are used to isolate sets of commands (`template method` design pattern)
	- Aspects "horizontal"
- Events are used to trigger sets of aspects
	- Events "vertical"

---

# Unplanned design

The original code was designed as "what's architecture?"

- This wasn't planned to be "Event/Aspect" oriented
- Partway through refactor, "pivoted" to fit the paradigm better

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
	- My design is essentially `before` calls for `lambda:None`{.python}
- AOP allows adding methods/values to classes
	- Monkey Patching, so built-in language support

---

# Future work

- Use exceptions to allow for more discrete control
	- Return values
	- Better simulate `around` pointcuts
