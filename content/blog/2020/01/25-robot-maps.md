---
Title: Robot Maps in FRC Code
Category: code
Tags:
- frc
- java
---

One of the things that my robotics team does differently from other teams, is that we've created an abstraction layer for the hardware.
To do this, we leveraged the official concept of a "robot map", but converted it to a more conventional dependency injection structure.

Historic Robot Maps
-------------------

Historically, the official `RobotMap` recommendation looks something like this:

```java
public class RobotMap {
    public static final int FRONT_LEFT_DRIVE_MOTOR = 1;
    public static final int FRONT_RIGHT_DRIVE_MOTOR = 2;
    public static final int REAR_LEFT_DRIVE_MOTOR = 3;
    public static final int REAR_RIGHT_DRIVE_MOTOR = 4;
    // ... Insert many other constants ...
    public static final int ARM_PISTON_A = 1;
    public static final int ARM_PISTON_B = 2;
}
// Elsewhere, in the subsystem:
public class Arm {
    private DoubleSolenoid piston = new DoubleSolenoid(RobotMap.ARM_PISTON_A, RobotMap.ARM_PISTON_B);
}
```

This had several flaws that we noticed:

- It didn't seem to scale very well
- It didn't have any grouping of items
- There was no way to tell how the constants were supposed to be used
- We had to rewrite the entire `RobotMap` for each chassis, where the arrangement might be different or missing entirely

Grouped Robot Maps
------------------

We addressed those issues first by grouping the constants into "namespaces" based on how they were grouped (digital i/o, <abbr title="Pulse Width Modulation">PWMs</abbr>, CAN bus addresses):

```java
public class RobotMap {
    public static class PWM {
        public static final int FRONT_LEFT_DRIVE = 1;
        public static final int FRONT_RIGHT_DRIVE = 2;
        public static final int REAR_LEFT_DRIVE = 3;
        public static final int REAR_RIGHT_DRIVE = 4;
    }
    // ... Insert many other constants ...
    public static class DIO {
        public static final int ARM_A = 1;
        public static final int ARM_B = 2;
    }
}
// Elsewhere, in the subsystem:
public class Arm {
    private DoubleSolenoid piston = new DoubleSolenoid(RobotMap.DIO.ARM_A, RobotMap.DIO.ARM_B);
}
```

This was better, but still had most of the same issues.
Using dependency injection, we could solve most of those in one go.

Robot Map Interface
-------------------

First, we can convert the `RobotMap` class to an interface.
This allows for creating multiple maps, to handle the different chassis.
Next, we arrange the values into static interfaces based on subsystem.

```java
public interface RobotMap {
    public static interface ArmMap {
        int getArmA();
        int getArmB();
    }

    ArmMap getArmMap();
}
// Elsewhere, in the subsystem:
public class Arm {
    private DoubleSolenoid piston;

    public Arm(RobotMap.ArmMap map) {
        piston = new DoubleSolenoid(map.getArmA(), map.getArmB());
    }
}
```

A downside to this is that it moves initialization from the members to the constructor - but this is also positive, as it means that we can theoretically create two instances of a subsystem.
(In practice, this is unlikely, but it's still a good mentality to teach)
The main benefit of this, is that it allows creating maps (and sub-maps) for each chassis, if necessary.

The next step is to abstract it from returning addresses, to returning hardware objects itself.

```java
public interface RobotMap {
    public static interface ArmMap {
        DoubleSolenoid getPiston();
    }

    ArmMap getArmMap();
}
// Sample robot map
public class Tempest implements RobotMap {
    @Override
    public ArmMap getArmMap() {
        return new ArmMap() {
            @Override
            public DoubleSolenoid getPiston() {
                return new DoubleSolenoid(1, 2);
            }
        };
    }
}
// Elsewhere, in the subsystem:
public class Arm {
    private DoubleSolenoid piston;

    public Arm(RobotMap.ArmMap map) {
        piston = map.getPiston();
    }
}
```

This allows for some more growth, and even allows for mocking entire subsystems to test their functionality without running on hardware.
We have several classes at our disposal in [chopshoplib](https://github.com/chopshop-166/chopshoplib), our year-agnostic library.
Unfortunately the official library doesn't quite have the level of abstraction that we need to fully utilize this technique, so the result is creating a bunch of [wrapper classes].

Future Work
-----------

- For small maps (consisting of just one member) you could use `@FunctionalInterface` and a lambda to reduce boilerplate
- Kotlin allows the same concepts but substantially smaller

[chopshoplib]: https://github.com/chopshop-166/chopshoplib
[wrapper classes]: {filename}/2018/08/09-intersecting-interfaces.md
