Title: FIRST Architecture: Back to Java
Category: code
Series: FIRST Software Architecture
Tags: frc

# 2018 Season

After all of the prior discussion and training in teaching the students the basics of C#, we had a slight change of plans.
As it turned out, the [dotnet implementation of WPILib][robotdotnet] wasn't updated in time to stay up to date with the newest version of the core library.
While this did cause problems at first, there are some benefits that we discovered that couldn't have been done with C# alone.

# GradleRIO

[GradleRIO][] is a tool that wraps around the Gradle build tool, extending it for use with FRC robots.
It's designed to be fairly simple to use, and takes care of the usual headache we have of installing all of the dependencies.

# Libraries

WPILib can't handle every case and paradigm that teams might want.
While my team has found the command-based model to be good, there are a few things that the mentors wanted to add to make programming the robot even more straightforward for the students.

## `SubsystemCommand`

Making an appearance first in my blog posts, the [SubsystemCommand][] class has been fleshed out more.
Its primary purpose is to allow commands to be written inline with the subsystem that they depend on:

```java
class Lift {
	// ...

    public Command GoUp() {
        return new SubsystemCommand(this) {
            @Override
            protected void initialize() {
                disengageBrake();
            }

            @Override
            protected void execute() {
                setSetpointRelative(Preferences.getInstance().getDouble(PreferenceStrings.LIFT_UP_DOWN_INCREMENT, 1));
            }

            @Override
            protected boolean isFinished() {
                return false;
            }
        };
	}
}
```

The extra class is required because when you create an anonymous class, you don't have the ability to customize the contructor.
The `requires()` function needs to be run as part of the constructor.

## `ActionCommand`

[ActionCommand][] is a similar class that harnesses the power of Java 8's function references.
It's designed for instant commands that just call a single function:

```java
class Lift {
	// ...
	public Command Brake() {
        return new ActionCommand("Brake", this, this::engageBrake);
	}
}
```

It's also easily used with another one of Java 8's useful features - lambda functions.
Instead of passing in a function reference, a developer can pass a lambda directly, which can be useful for creating families of commands:

```java
class Lift {
	// ...
	public Command GoHigh() {
		return new ActionCommand("Go High", this, () -> setHeight(Heights.HIGH));
	}
}
```

## `CommandChain`

Where the other two are mainly meant for running single actions, [CommandChain][] is meant for replacing long custom classes to create `CommandGroup`s.

```java
class Lift {
	// ...
	public Command ClimbUp() {
			return new CommandChain("Climb Up")
						.then(DisengageBrake())
						.then(ShiftToHighGear())
						.then(GoToHeight(LiftHeights.kClimb, true))
						.then(ShiftToLowGear())
						.then(GoToHeight(LiftHeights.kScaleLow, false))
						.then(Brake());
	}
}
```

It's designed for sets of commands that get run in sequence, allowing the same inline pattern as the other two classes.

[robotdotnet]: https://github.com/robotdotnet/WPILib
[GradleRIO]: https://github.com/Open-RIO/GradleRIO
[SubsystemCommand]: https://github.com/chopshop-166/frc-2018/blob/master/src/main/java/frc/team166/chopshoplib/commands/SubsystemCommand.java
[ActionCommand]: https://github.com/chopshop-166/frc-2018/blob/master/src/main/java/frc/team166/chopshoplib/commands/ActionCommand.java
[CommandChain]: https://github.com/chopshop-166/frc-2018/blob/master/src/main/java/frc/team166/chopshoplib/commands/CommandChain.java
