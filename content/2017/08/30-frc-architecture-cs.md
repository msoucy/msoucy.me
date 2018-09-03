---
Title: FIRST Software Architecture: Programming in C#
Category: code
Series: FIRST Software Architecture
Tags: frc
---

# Introduction

When writing code for a robot, there are a number of languages available for use.
My team alone has used three different languages so far, and is planning on switching to another this year.
This is our rationale for wanting to teach programming in C# starting in the 2018 season.

# Language

C# recently received a [port][] of WPILib, the standard library made available to FIRST teams.
This combined with both the Mono and Dotnet Core projects, allows a team to do their robot development in any .NET-based language.
Alone, though, this doesn't provide enough reason for a team to change, if they are already using one of the other available languages.
There are other reasons that are less immediately visible, however.

## Expression-bodied methods

When creating a command, one will often make trivial bodies for the methods, such as:

```java
public class RaiseElevator extends Command {

    public RaiseArm() {
        requires(Robot.arm);
    }

    protected void initialize() {
        Robot.arm.raise();
    }

    protected void execute() { }

    protected boolean isFinished() {
		Robot.arm.isAtTop();
    }

    protected void end() {
		return Robot.arm.stop();
	}

    protected void interrupted() {
		end();
	}
}
```

While this is concise, it can be made even more clear and easy to read:

```csharp
public class RaiseElevator extends Command {

    public RaiseArm() {
        requires(Robot.arm);
    }

    protected void initialize() => Robot.arm.raise();

    protected void execute() { }

    protected boolean isFinished() => Robot.arm.isAtTop();

    protected void end() => Robot.arm.stop();

    protected void interrupted() => end();
}
```

Admittedly, the benefit for this is small, and mainly useful for `isFinished`. However, when used it can make the code easier to read.

## Namespacing

C#'s namespace and import rules help cut down on one of the issues that we frequently saw: two team members would commit changes to a file, and the import lists would clobber each other, because each class was being listed individually.
In C#, if one imports a namespace, all names in that namespace are made available - similar to Java's `import x.y.*;`, but less frowned upon.
When working on a class within a namespace, that namespace is automatically made available as well, which reduces confusion.

Unlike C++, C# imports are *not* textual, so there's no danger about importing other classes in the wrong order.

## Properties

In Java code, there's often a push to write "getters" and "setters" - for a variable `foo`, writing functions `getFoo()` and `setFoo(Foo newFoo)`.
I consider this to be poor form, because as trivial accessors they expose too much information about the inner workings of the class.
More acceptable, however, is if one or the other does nontrivial operations, such as in the following snippet:

```csharp
		public enum Gear
        {
            Low,
            Neutral,
            High,
        }

        Gear _gear;

        public Gear GearValue
        {
            get { return _gear; }
            set
            {
                _gear = value;
                SmartDashboard.PutString("Gear", _gear.ToString());
                switch (_gear)
                {
                    case Gear.High:
                        leftTransmissionServo.Set(highGearValue);
                        rightTransmissionServo.Set(highGearValue);
                        leftEncoder.DistancePerPulse = distancePerPulse;
                        rightEncoder.DistancePerPulse = distancePerPulse;
                        break;
                    case Gear.Low:
                        leftTransmissionServo.Set(lowGearValue);
                        rightTransmissionServo.Set(lowGearValue);
                        leftEncoder.DistancePerPulse = distancePerPulse * 2.5;
                        rightEncoder.DistancePerPulse = distancePerPulse * 2.5;
                        break;
                    case Gear.Neutral:
                        leftTransmissionServo.Set(0.5);
                        rightTransmissionServo.Set(0.5);
                        break;
                }
            }
        }
```

Ignoring some of the quirks with the code, the most important part is how the gear value is accessed:

```csharp
drive.Gear = Drive.Gear.Low;
```

That single line would (assuming `drive` to be a variable of the appropriate class) tell the drive system to switch to low gear.
This would in turn move the transmissions into the proper position, set the encoder scale, etc...
This would be doable using a more conventional "setter", but would look much less proper when reading.

```java
drive.setGear(Drive.Gear.Low);
```

One treats the hardware as if it were a property of the code, the other is more of an "imperative" style.

## Lambdas

C# provides a convenient syntax for anonymous function literals - lambdas.
This, combined with one of the `WPILib.Extras` classes `ActionCommand`, allows students to write a variation of an instant command all in one expression:

```csharp
	AddSequential(new ActionCommand(() => Robot.arm.raise()));
```

# Tools

C# is primarily backed by Visual Studio, published by Microsoft.
While Java has numerous IDEs and environments surrounding it, most are considered unwieldy or aren't supported for FIRST development.
The largest and most noticeable offender of this is Eclipse, which is often criticised for being unintuitive and bloated.

Anecdotally, my team had numerous issues with Eclipse, where it would hang or crash for seemingly no reason, and consume so many resources that the computer was rendered unusable.
Visual Studio, though tied to Windows only, is one of the most commonly used environments available, is free for noncommercial use (including educational), and is less prone to crashing from the mentors' experience.
It also has a nice ability to automatically format code, without needing to manually enable it, which means that all code in the repository should be legible and sanely organized.

As an additional bonus, the libraries made available to .NET packages are accessible with much less initial setup - meaning automatic integration and testing is much more possible.
This is useful when using github as a central git server, where the students can submit their changes as pull requests and have a CI tool such as TravisCI automatically build and sanity-check the code.

# Further development

In my next post, I'll demonstrate robot code built using what I refer to as "functional command programming", by rewriting the same robot into F#.


[port]: https://github.com/robotdotnet/WPILib
