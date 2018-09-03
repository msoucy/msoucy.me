---
Title: FIRST Software Architecture: Command Based Programming Summary
Category: code
Series: FIRST Software Architecture
Tags: frc
---

*This post is a modified and expanded form of a [REDDIT post] I wrote a while ago, and serves as a complement to a more in-depth post*

The important thing about the command model is that it's all about abstraction.
A subsystem is a concept representing a section of the robot.
It has information about the hardware, and includes methods to get relevant information and do certain actions.
A subsystem won't have a method called `isUpperLimitSwitchPressed` though - apart from being really verbose, it also tells the rest of the code too much about the subsystem.
You'd want `isAtTop` or similar.

From that point on, anything that wants to know if it's at the top (say it's a sensor to detect that it's done climbing) would use `Robot.climber.isAtTop()`.
Only the subsystem needs to know about the hardware, everything else only needs to know about what the subsystem can do.

Most commands should be simple, when using that style.
A climb command, for instance, would tell the climber subsystem to start from its initialize function, have `isFinished` return true when `Robot.climber.isAtTop()`, and in the end and interrupt methods just `Robot.climber.stop()`.
In many cases, the end and interrupt will want to do the same things - you might as well just have one call the other.

One of the other benefits of subsystems is that you can have multiple of the same type - for example, two shooters to fire in two different directions at the same time, or increase throughput.
Ignoring that the shooter should probably have been designed differently, your Robot class would have two Shooter instances with different parameters - and then from there you treat each one as its own entity.

Note that most commands will be very simple, because really they all follow the same pattern - set up, run, check to see if it should keep running, cleanup.
The command never needs to know the details about how something works, only what it does. That's the purpose of a subsystem.

A command group is just a command that runs other commands.
When you give your command constructors parameters, then you can use just a few commands to do many things (for example, see the Wait Command).
Command groups are how you sequence your actions. Autonomous is pretty much just a command group.

Because the subsystems hide knowledge about the hardware, there's a chance that two subsystems will try to use the same ports and fail (usually during testing).
This is why the robot map exists. You store the constants there, in one place, to make it easier to find conflicts.

[REDDIT post]: https://www.reddit.com/r/FRC/comments/5sigju/how_is_everyones_team_doing/ddg38en/
