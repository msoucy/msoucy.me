---
title: "FIRST Software Architecture: Command Based Programming"
categories: [code]
Series: FIRST Software Architecture
Date: "2017-08-28"
Tags:
- frc
---

*This post is a modified and expanded form of a [presentation] given to my FIRST Robotics Competition team*

# Introduction

When writing code for a robot, there are a number of ways to organize the code.
The form that's become the most prolific, though, is command-based programming.

Command-based programming is a step more abstract than imperative programs such as what might be done by a beginner.
This can lead to some confusion, as most individual robot tasks can be viewed linearly:

* Drive the motor until the arm goes to a position
* Climb until we are at the top

These ideas seem to fit into the iterative model provided by WPILib, but fall apart when multiple concepts are joined.
One method has to keep track of all the logic for multiple subsystems on the robot, how they all interact, etc.
This is why the command-based model exists.

The command model breaks robot code into a few different layers: components, subsystems, and commands.
The main idea is that a robot is made of several subsystems, each of which has several sensors and manipulators ("components"), and some number of actions that it can perform ("commands").
A command is a process that has a definite beginning, middle, and end, that doesn't care about what's using it.
This allows for an autonomous method to easily be written, using existing commands made for teleoperated use.

# Components

A "component" is a term for the code interface to a sensor or motor.
Any form of input or output that the robot deals with, could be seen as dealing with a component of some kind.
Some example components:

* `Joystick`
* `TalonSRX`
* `CANTalon`
* `Victor`
* `RobotDrive`

There can also be custom components - in the past, the Chop Shop has used a `MultiSpeedController`, which behaves as a speed controller, but controls several `SpeedController` instances together.
This is useful for locking two motors to the same speed.

# Subsystems

A `Subsystem` is made of components, and adds a layer of **abstraction**. This is important, because it allows the overall robot code to not have to deal with individual sensors and motors.

## Subsystems and Abstraction

Let's say we have an arm on a robot.
This arm was designed to use a motor to raise and lower it.
So we write the outline of our subsystem:

```java
public class ClawArm extends Subsystem {
    Victor motor;

    public ClawArm()
    {
        motor = new Victor(RobotMap.Pwm.RollerVictor);
    }
}
```

Now, the subsystem can't do much until we have a way to control it:

```java
public class ClawArm extends Subsystem {
    Victor motor;

    public ClawArm()
    {
        motor = new Victor(RobotMap.Pwm.RollerVictor);
    }

    public void moveForward()
    {
        motor.setSpeed(1);
    }

    public void moveBackward()
    {
        motor.setSpeed(-1);
    }
}
```

In order for the rest of the robot to use this new functionality, we need to create a `Command`:

```java
public class RaiseArm extends Command {

    public RaiseArm() {
        requires(Robot.arm);
    }

    protected void initialize() {
        Robot.arm.moveForward();
    }

    protected void execute() { }

    protected boolean isFinished() {
        return true;
    }

    protected void end() { }

    protected void interrupted() { }
}
```

Now comes the problem - what if the design changes? What direction is "forward"?

## Designing For Reusability

After some deliberation, the design for the arm has been changed to use a solenoid instead.

What needs to change?

* `RobotMap` (but this would happen no matter what)
* `ClawArm` - the subsystem
* `RaiseArm` - the command

This can be done by making changes such as:

```java
public class ClawArm extends Subsystem {
    DoubleSolenoid solenoid;

    public ClawArm()
    {
        solenoid = new Victor(RobotMap.Digital.ArmUp,
                              RobotMap.Digital.ArmDown);
    }

    public void moveForward()
    {
        solenoid.set(DoubleSolenoid.Value.kForward);
    }

    public void moveBackward()
    {
        solenoid.set(DoubleSolenoid.Value.kReverse);
    }
}
```

While not horrible, because the command doesn't have to change, it's still limiting because of the concept of "forward" and "backward".

This can be improved by changing the names:

```java
public class ClawArm extends Subsystem {
    DoubleSolenoid solenoid;

    public ClawArm()
    {
        solenoid = new Victor(RobotMap.Digital.ArmUp,
                              RobotMap.Digital.ArmDown);
    }

    public void raise()
    {
        solenoid.set(DoubleSolenoid.Value.kForward);
    }

    public void lower()
    {
        solenoid.set(DoubleSolenoid.Value.kReverse);
    }
}
```

Only by changing the names, the resulting command is much clearer:

```java
public class RaiseArm extends Command {

    public RaiseArm() {
        requires(Robot.arm);
    }

    protected void initialize() {
        Robot.arm.raise();
    }

    protected void execute() { }

    protected boolean isFinished() {
        return true;
    }

    protected void end() { }

    protected void interrupted() { }
}
```

The command itself is still only one line, but it's obvious what it's intended to do.

**This would never have had to change if the subsystem had called the method `.raise()` in the first place!**

## Lessons Learned for Subsystems

* Abstraction is GOOD
* Any code working with a subsystem should have no idea HOW the subsystem works
* A subsystem can do one thing at a time
    * To put it another way, if you want part of the robot to do two things at once, look to see if it should be two subsystems

# Commands

A command is:

- Something that you can execute
- A single action that a subsystem performs
- Something the operator (or autonomous) can start
- A description of the robot's behavior

They can be simple, just calling one method of one subsystem:

- `RaiseArm`
- `DriveWithJoysticks`

Or they might be complex, with sequencing and tasks in parallel:

- `AimAndThenShoot`
- `CollectBall` (sequence of `StartCollector`, `LowerArm`, `WaitUntilBallCollected`, `RaiseArm`, and `StopCollector`)
- `Autonomous`

## Command Parts

When creating a command, you have to think carefully about its behavior:

```java
public class CustomCommand extends Command {

    public CustomCommand() {
		// Tell the command which subsystem it uses
        requires(Robot.mysubsystem);
    }

    protected void initialize() {
		// Happens once, when the command is first run
    }

    protected void execute() {
		// Happens on loop for as long as the command is active
	}

    protected boolean isFinished() {
		// Tells the command when to finish
        return true;
    }

    protected void end() {
		// Runs after the command is finished
	}

    protected void interrupted() {
		// Runs if another command wants to use its subsystem
	}
}
```

There's a definitive flow to each command.
Each command is created, then initalizes.
It runs a chunk of code until it determines that it's finished, and then ends.
If it gets interrupted, it knows how to clean up after itself.
Almost every command can be reduced to this pattern.

## Using Commands

In general, there are three kinds of command:

- Commands that happen instantaneously (such as "shoot ball")
- Commands that run continuously (such as "move arm to specific point")
- Commands that are made of other commands (doing several things, in sequence or parallel)

Depending on what kind of command you have, your command class can look very different.

## Instant Commands

An instant command has behavior that happens once, when the command first executes.

```java
public class ShootBall extends Command {

    public ShootBall() {
        requires(Robot.shooter);
    }

    protected void initialize() {
        Robot.shooter.shoot();
    }

    protected void execute() { }

    protected boolean isFinished() {
        return true;
    }

    protected void end() { }

    protected void interrupted() { }
}
```

The relevant methods are `initialize()`, `isFinished()`, and the constructor!
The rest can be empty.
Returning true from `isFinished()` just runs initialize() and exits.

This can be made even simpler:

```java
public class ShootBall extends InstantCommand {

    public ShootBall() {
        requires(Robot.shooter);
    }

    protected void initialize() {
        Robot.shooter.shoot();
    }
}
```

`InstantCommand` takes care of `execute()` and `isFinished()`, and by default `end()` and `interrupted()` do nothing.

## Continuous Command

A continuous command does one thing, until a condition is met.

```java
public class RaiseElevatorToTop extends Command {

    public RaiseElevatorToTop() {
        requires(Robot.elevator);
    }

    protected void initialize() { }

    protected void execute() {
        Robot.elevator.raise();
	}

    protected boolean isFinished() {
        return Robot.elevator.isAtTop();
    }

    protected void end() { Robot.elevator.halt(); }

    protected void interrupted() { Robot.elevator.halt(); }
}
```

Some important details to note:

- Since this gets run continuously, `initialize()` doesn't need to do much in this situation.
- `execute()` sets the speed each cycle
- `end()` and `interrupted()` handle cleanup
- `isFinished()` is essential here

## Command Groups

A command group is a way to combine multiple **related** things, at once or sequentially:

```java
public class AutoScoreHigh extends CommandGroup {

    public AutoScoreHigh() {
        // No requires() call, the subcommands do that
		addParallel(new PrepareBallRollers());
		addSequential(new AlignRobotWithTarget());
		addSequential(new WaitForChildren()); // Wait half a second
		addSequential(new PrintCommand("Fire in the hole!"));
		addSequential(new LaunchBall());
		addSequential(new WaitCommand(0.5)); // Wait half a second
		addSequential(new StopBallRollers());
    }

}
```

- `addSequential()` waits until the command finishes before moving on
- `addParallel()` launches its command and then moves on
- `PrintCommand`, `WaitCommand`, `WaitForChildren` are built in to WPILib (along with others)

# Further development

In my next post, I'll analyze the gains made by switching language from Java to C#. Later on, I'll demonstrate robot code built using what I refer to as "functional command programming", by rewriting the same robot into F#.

[presentation]: https://github.com/chopshop-166/SoftwareTraining/blob/master/presentations/content/architecture.md

