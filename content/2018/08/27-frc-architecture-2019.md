---
Title: FRC Programming Ideas for 2019
Category: code
Series: FIRST Software Architecture
Tags:
- frc
- java
---

# 2019 Season

In preparation for the 2019 FRC season, some of the mentors have been toying with new concepts to apply for next year, to hopefully make the code cleaner.

# GradleRIO

[GradleRIO][] with Visual Studio Code is now the official way to build and deploy FRC code.
This is nice for my team, as this is the exact setup we were using last year, with great success.
Starting in 2019, there will be an additional plugin that more fully integrates the IDE with the build/deploy process.
Most likely, we will encourage but not mandate its use, as everything it does can be done via Gradle calls directly.

# Libraries

Leveraging 2018's evolving codebase, we've come up with some changes and improvements to apply in 2019.

## `SubsystemCommand`

The [SubsystemCommand][] that we created last year, is now [officially part of WPIlib][SubsystemCommand PR].
This means one fewer wrapper layer between our paradigms, and the official libraries.

## `ActionCommand`

The [ActionCommand][] is undergoing [a similar process][ActionCommand PR] to be merged into WPILib.
The original name was derived from the C# implementation of WPILib, so at first the name was changed to FunctionalCommand to better reflect its nature.
After some discussion, the pull request is now attempting to add the lambdas as arguments of InstantCommand directly.
This would allow some small boilerplate removal.

## Telemetry

A huge part of FIRST is collaboration.
Many teams make public posts on Chief Delphi, the unofficial forum for all things FIRST, to show off their code.
Sometimes, I like to peruse those posts to find interesting things that we can learn from.

[One of these posts][SERT post] was by a member of team 2521 ("SERT").
They stood out as having some unusual additions - including a Kotlin codebase, and version tracking.
While I'd love to play with Kotlin, I feel like my team is going through enough changes that I'm not willing to attempt it any time soon.
However, the version tracking looks nice.

Basically, it uses a new Gradle task to poll git for information about the current commit.
Then it bundles that data into the resources of the code's `.jar` file.
There's a small amount of Kotlin code (which I translated back to Java) that reads those resources and puts them somewhere.
In our integration tests, they were just printed out, but they could easily be modified to put the values onto the dashboard.

## Reflection

The way my team's code is set up, each subsystem contains a set of methods that return `Command` objects.
These objects are the public-facing API for the subsystem.
With a little tweaking, it was possible to annotate the method, and use reflection to automatically get the annotated methods.
For each of the custom annotation objects attached to the method, the [reflection code][] will automatically call the method with appropriate arguments, and push the resulting object onto the dashboard for use.

This should allow for nicer access, instead of having all of the commands added as a part of the subsystem's constructor.

Similarly, we determined that we could use reflection to get all members of a `Subsystem` that implement the `Sendable` interface.
All such objects are candidates for being added to the dashboard's live window as a child object of the subsystem.
By using reflection, we replaced a lot of redundant code with one "magic" function call.

## Toys

There were a few assorted things that were developed over the last year, that work out to either be impractical or not useful.
Most of them got migrated to the [chopshoplib][] repository, in case we want to leverage or improve them in the future.
Some things of note:

- A handful of wrappers around commands, to allow "for loops" and "while loops" made out of commands.
- A command that runs another command until it times out or the original command finishes. We haven't found an actual practical application of these, they were mainly written to experiment with the library.
- A scripting framework that's powered by Preferences. It turned out that it was no faster (and a lot less powerful) than just writing more Java and redeploying the code.
- A `CommandRobot` that just calls the scheduler at the appropriate times. It just removes some small boilerplate, but doesn't alter any major design decisions.

# `RobotMap`

One of the pain points in recent years has been the existence of a `RobotMap` class.
At its core, the idea is sound: make a central class that stores a mapping of ports/addresses to their assigned roles.
Unfortunately, we've discovered that it isn't very expandable.
It results in tons of constants with long names, none of which give actual useful information unless you wrap them in a class (`RobotMap.CAN.FRONT_RIGHT_DRIVE`) or similarly prepend the type of number to the name.

This year, we've decided to try a different approach.
`RobotMap` itself will become an interface, with sub-interfaces for maps for each subsystem.
Instead of returning a port number or CAN address, each method returns an actual instance of one of the appropriate interfaces.
If the particular object doesn't exist on the robot (missing hardware, for instance), then a mock type can be returned instead.

This has a few benefits:

- We can have multiple maps (perhaps determined by a Preference or some other specific data) for different robot layouts.
- We can stub out whole subsystems by just returning mock instances for everything.
- All the mappings are still in one (admittedly larger) location.

The only drawback that we've thought of that might arise, is that there might be sensor-specific setup.
But that can be done within the Map class, instead of the Subsystem.

# Preferences

Unfortunately, we found that Preferences are one of the biggest let-downs in WPILib.
At their core, the concept is nice - store a value on the robot itself, have the code pull that value.
Unfortunately, getting a value from the Preferences is verbose, and relies on a string key as well as a default value.
To avoid mistakes with the key, it makes sense to store the key in a constant, adding to the verbosity.

This would be acceptable, if there were more convenient ways to edit the preferences.
As it is, the preferences are stored in a file somewhere on the robot, and only otherwise acceptable via methods on a `Preferences` object.
We found that it was just as fast - if not faster - to change and redeploy the code.

We never managed to get preferences to integrate with the dashboard in an easy to use way.

It's possible that we were trying to use them for things that they aren't intended for, but I think that for the near future (unless a more convenient API for them is created) we'll be putting those values in the subsystem directly, or in `RobotMap` if it's hardware-dependant.

# Goals

This year, I have a few personal goals that I want to achieve with the students.

- Have some of them understand a PID controller (if not the math, at least the concept and when to use them) and hopefully use it on the robot.
- Learn how to use the built-in WPILib simulation, to be able to "run" an entire robot on a laptop. This might render a lot of the `RobotMap` obsolete, but can still prove helpful when integrating on an incomplete robot (like a driving chassis without a manipulator)
- I'd like to have enough time with the robot that we have a minimal autonomous before the first competition. Even if it's just crossing a line, most games give a few points for that. This is dependant on getting enough time with the robot that all the commands an autonomous might use are tested and integrated.

I also have a few goals that I'm less determined about, but would still like to see happen:

- Vision processing for game elements. Usually, there's some sort of vision target for the game piece or goal. It would be nice to have that highlighted on the dashboard, at least.
- [Pathfinder][] support in the robot. Pathfinder is a utility library that allows creating paths that the robot can move on. This will probably be useful to ease autonomous development.

[GradleRIO]: https://github.com/Open-RIO/GradleRIO
[SubsystemCommand]: https://github.com/chopshop-166/frc-2018/blob/master/src/main/java/frc/team166/chopshoplib/commands/SubsystemCommand.java
[SubsystemCommand PR]: https://github.com/wpilibsuite/allwpilib/pull/1275
[ActionCommand]: https://github.com/chopshop-166/frc-2018/blob/master/src/main/java/frc/team166/chopshoplib/commands/ActionCommand.java
[ActionCommand PR]: https://github.com/wpilibsuite/allwpilib/pull/1262
[SERT post]: https://www.chiefdelphi.com/forums/showthread.php?t=166163
[SERT]: https://github.com/SouthEugeneRoboticsTeam/PowerUp-2018/blob/development/build.gradle
[reflection code]: https://github.com/chopshop-166/chopshoplib/blob/master/src/main/java/frc/team166/chopshoplib/DashboardUtils.java
[chopshoplib]: https://github.com/chopshop-166/chopshoplib
[Pathfinder]: https://github.com/JacisNonsense/Pathfinder
