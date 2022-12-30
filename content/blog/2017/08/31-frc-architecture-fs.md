---
title: "FIRST Software Architecture: Programming in F#"
Category: code
Series: FIRST Software Architecture
Date: "2017-08-31"
Tags:
- frc
---

# Introduction

When writing code for a robot, there are a number of languages available for use.
While investigating C# for use, I decided to make a detour and attempt to create robot code using F#.
I found that it allowed for a surprising functional programming twist.

# The Code

F# code has a strict ordering - symbols are only visible if they occur before their use, both within a file and within the project's file list.
Because of this, I'm writing about the order that I found works best for my tests.

## `RobotMap`

The `RobotMap` is normally the simplest part of robot code - it stores the constants that map sensors and manipulators, so that two different subsystems don't try to use the same ones and cause conflict.
Declaring constants in F# is easy:

```fsharp
module RobotMap

module Driver =
    let leftJoystickPort  = 0
    let rightJoystickPort = 1
    let Joystick          = 1

module Copilot =
    let copilotPort = 2
    let Joystick    = 2

module Pwm =
    let LeftShooterMotor  = 4
    let RightShooterMotor = 3;
    let ShooterAngleMotor = 2;

    let leftTransmissionServoPort  = 7
    let rightTransmissionServoPort = 8

    let MainIntakeVictor  = 1
    let CrossIntakeVictor = 5
    let RollerVictor      = 0

module CAN =
    let leftTopDrive = 3
    let leftBotDrive = 4
    let rightTopDrive = 1
    let rightBotDrive = 2

// etc...
```

## Extensions

It's rare that a library provides everything needed, so naturally I felt that I had to roll my own for a few things.
The most relevant parts are provided below

```fsharp
open WPILib

let (+-) (grp : CommandGroup) (cmd : Command) =
    grp.AddSequential cmd
    grp
let (+|) (grp : CommandGroup) (cmd : Command) =
    grp.AddParallel cmd
    grp

let timeout (length : double) (cmd : Command) =
    {new TimedCommand(length) with
    override this.Initialize () = cmd.Start ()
    override this.End () = if cmd.IsRunning() then cmd.Cancel ()
    }
```

The two strange definitions will be used and explained below.

The definition of `timeout` shows a few important things:

* The function takes two curried arguments, and returns a new `TimedCommand`
* F# allows creation of a derived type as an expression
* The value of a function (the "return type") is the result of the last expression run in the function

This function is roughly equivalent to the C# code:

```csharp
public class TimeoutCommand : TimedCommand {
	Command _cmd;

	public TimeoutCommand(double length, Command cmd)
		: base(length)
	{
		_cmd = cmd;
	}
	override void Initialize() => _cmd.Start()
	override this.End() {
		if (cmd.IsRunning()) cmd.Cancel();
	}
}
```

## Operator Interface

Not much to explain with the OI - `member`s are publicly accessible, which is needed later on in the code

```fsharp
module OI

open WPILib

type OI() =

    static member val Instance : OI = new OI()

    member this.driverLeft = Joystick(RobotMap.Driver.leftJoystickPort)
    member this.driverRight = Joystick(RobotMap.Driver.rightJoystickPort)
    member this.copilotStick = Joystick(RobotMap.Copilot.copilotPort)

    member this.LeftYAxis                with get() = this.driverLeft.GetRawAxis(1)
    member this.RightYAxis               with get() = this.driverRight.GetRawAxis(1)
    member this.CopilotRightTrigger      with get() = this.copilotStick.GetRawAxis(3)
    member this.CopilotLeftTrigger       with get() = this.copilotStick.GetRawAxis(2)
    member this.CopilotLeftJoyUpDownAxis with get() = -this.copilotStick.GetRawAxis(1)
```

## Subsystems

Finally, on to the interesting stuff.
I'll only show one, but it'll demonstrate the core concepts.

```fsharp
// A new class is made with the type keyword
type AManipulators() =
	// The type AManipulators inherits from Subsystem
    inherit Subsystem()

	// The AManipulators has a double-solenoid with ports from RobotMap
    let solenoid = new DoubleSolenoid(RobotMap.Solenoid.AManipulatorForward,
                                      RobotMap.Solenoid.AManipulatorReverse)

	// A property representing the state of the manipulators
	// F# doesn't declare a "this" keyword, it's manually specified
    member this.State
		// When you read the state, it runs this
        with get() =
            if solenoid.Get() = DoubleSolenoid.Value.Reverse
            then Lowered else Raised
		// When you set the state, it runs this
        and set value =
            solenoid.Set(match value with
                         | Lowered -> DoubleSolenoid.Value.Reverse
                         | Raised -> DoubleSolenoid.Value.Forward)

	// A private method creating a new command
	// Note that this is internal to the class, instead of declaring the commands as classes separately
	// This allows the rest of the robot to access the commands as members of an instance of the subsystem
    member private this.SetState state =
        {new InstantSubsystemCommand(this) with
         override cmd.Initialize() = this.State <- state}

	// Here are public accessors for SetState
	// These will be used when calling and constructing commands
    member this.Lower () = this.SetState Lowered
    member this.Raise () = this.SetState Raised

	// This subsystem doesn't do anything until commanded
    override this.InitDefaultCommand() = ()

	// Properly manage cleanup code in .NET land
    interface IDisposable with
        override this.Dispose() =
            solenoid.Dispose()
```

The most important part here is that *the subsystem owns all of the commands that can operate on it*.
This means that all subsystem logic is tracked together.

## Program

The main body of the program, `Program.fs`, contains not just the main robot class, but also the definitions for all complex commands

```fsharp
open OI
open Extensions
open Subsystems
open WPILib
open WPILib.Buttons
open WPILib.Commands
open WPILib.Extras
open WPILib.SmartDashboard

type Robot() =
    inherit CommandRobot()
    let mutable autonomousCommand : Command option = None
    let oi = OI.Instance

    let drive = new Drive.Drive()
    let intake = new Subsystems.Intake();
    let shooter = new Subsystems.Shooter();
    let aimShooter = new Subsystems.AimShooter();
    let vision = new Vision.Vision();
    let intakeRoller = new Subsystems.IntakeRoller();
    let aManipulators = new Subsystems.AManipulators();
    let shooterLock = new Subsystems.ShooterLock();


    override this.RobotInit() =
        // Shorten, because it gets used a lot
        let driveDistance = drive.DriveDistanceCmd
        let wait time = new WaitCommand(time)

        let moveActuatorsDown () =
            new CommandGroup()
            +- shooterLock.Unlock ()
            +- aManipulators.Lower ()
            +- intake.Lower ()
            +- aimShooter.AimToAngle 43.0
        let moveActuatorsUp () =
            new CommandGroup()
            +- aManipulators.Raise ()
            +- intake.Raise ()
            +- aimShooter.AimToMinimumAngle 55.0
            +- shooterLock.Lock ()
        let moveBallIntoStorage () =
            new CommandGroup()
            +- intake.SetMotor Forward
            +- intakeRoller.LoadBall ()
        let moveBallIntoShooter () =
            new CommandGroup()
            +- intake.SetMotor Forward
            +- intakeRoller.ShootBall ()
        let cancelShot () =
            new CommandGroup()
            +- aimShooter.Cancel ()
            +- intakeRoller.Cancel ()
            +- intake.SetMotor Stopped
            +- shooter.SetSpeed 0.0

        let mediumRangeShot () =
            new CommandGroup()
            +- shooterLock.Unlock () // Release shooter piston

            +- shooter.SetSpeed 0.9 // Set shooter wheel PIDs
            +| aimParallel ()
            +- drive.TurnToGoalWithGyro vision

            // Adjust shooter angle based on distance algorithm
            +- aimVision ()
            // Drive feeder roller until ball leaves
            +- moveBallIntoStorage ()
            +- moveBallIntoShooter ()
            // Guarantee ball has left
            +- wait 0.25
            +- shooter.SetSpeed 0.0
            // Free up shooting subsystems
            +- cancelShot ()
		// etc
```

This code snippet shows off the fun part - declaring command groups.
In C#, as well as the Java and C++ versions of WPILib, command groups are declared by inheriting from `CommandGroup`, and then in the constructor adding calls to `addSequential` and `addParallel`.
With the definitions of the `+-` and `+|` operators, from the `Extensions.fs`, each call to `addSequential` can be chained together in a less verbose way.
Each of these are also converted to functions, instead of subclassing, because it's the more idiomatic way to do so within F#.

Again, each command is accessed via the subsystem that it belongs to.
Because of this, the code reads more intuitively, with an ironically more object-oriented seeming interface than is possible in any other language.

