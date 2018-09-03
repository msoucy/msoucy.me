---
Title: Intersecting Interfaces in Java
Category: code
Tags: java
---

During the off-season for FIRST Robotics, I like to examine the code that was produced and try to find ways to improve.
Sometimes this involves looking at other teams' code.
Often it involves experimenting with the current code, trying to find new patterns and techniques.

One of the areas of the code that I wasn't ever really fond of, is the Robot Map.
For those unfamiliar, `RobotMap` is essentially a class that stores all the constants that the robot uses.
This includes things like which CAN address is associated with each motor.
This has some benefits, such as keeping a single list of all the addresses and ports to prevent two subsystems from accidentally reserving the same ones.
However, it has some annoying drawbacks:

- The entire class is locked to a particular implementation of the robot - every motor must be wired to the same port, with the same speed controller, for two different robots.
- It only shows the ports, not the actual types of controllers used in them.
- All the constants can get mixed up, unless you use nested static classes to group them like you would use an enumeration in C++.

One of the summer's experiments, therefore, was to try to find a way to reduce those complaints.
A potential solution was to not use constants at all.
`RobotMap` would become an interface, providing methods that return the particular instances.
There would then be new subclasses for each particular implementation (practice robot vs. competition robot).

Example:

```java
interface RobotMap {
    public SpeedController getLeftDrive();
    public SpeedController getRightDrive();
}

class Maverick implements RobotMap {
    // SpeedControllerGroup implements SpeedController as well as Sendable
    SpeedControllerGroup leftGroup = new SpeedControllerGroup(new WPI_TalonSRX(8), new WPI_TalonSRX(9));
    SpeedControllerGroup rightGroup = new SpeedControllerGroup(new WPI_TalonSRX(4), new WPI_TalonSRX(5));

    @Override
    public SpeedController getLeftDrive() {
        return leftGroup;
    }

    @Override
    public SpeedController getRightDrive() {
        return rightGroup;
    }
}
```

This seemed like a solution that we liked, though we quickly ran into a problem.
Within subsystem classes, there's a method called `addChild`.
This method takes an object that implements `Sendable`, and makes it a part of that subsystem on the dashboard.
In the implementation that we have above, `getLeftDrive` and `getRightDrive` both return `SpeedController` objects.
`SpeedController` is completely separate from `Sendable`, though *entirely coincidentally* everything that implements `SpeedController` also implements `Sendable`.
This is problematic, as by returning and storing a `SpeedController` we lose the ability to add it as a child!

[Dotty](http://dotty.epfl.ch/), a compiler that's designed to be the future of Scala, adds a new concept to its type system - Intersection Types.
From their [example on them](http://dotty.epfl.ch/docs/reference/intersection-types.html):

```scala
trait Resettable {
  def reset(): this.type
}
trait Growable[T] {
  def add(x: T): this.type
}
def f(x: Resettable & Growable[String]) = {
  x.reset()
  x.add("first")
}
```

In the function `f`, the variable `x` is required to implement **both** of the provided interfaces.
This seemed like a perfect solution to my problem, but of course I ran into a roadblock right away - Java doesn't support this functionality.

Or so I thought.

As it turns out, Java supports them in a few select situations - the one I care most about is in their generic constraints.
I decided that if I couldn't have intersection typed variables, I'd make my own.

Step one was to make a "combined" interface:

```java
interface A {
    public void doA();
}
interface B {
    public void doB();
}
interface AB extends A,B {
}
```

Step two was to provide a way to wrap something that's both an `A` and a `B`, into an `AB`.

```java
interface AB extends A,B {
    // This only works with Java 8+
    static <T extends A & B> AB wrap(T t) {
        return null;
    }
}
```

Step three was to use an anonymous class within the wrapper function, to dispatch calls from both interfaces to the wrapped object.

```java
interface AB extends A,B {
    // This only works with Java 8+
    static <T extends A & B> AB wrap(T t) {
        return new AB() {
            @Override
            public void doA() {
                t.doA();
            }
            @Override
            public void doB() {
                t.doB();
            }
        };
    }
}
```

This got slightly tedious with larger interfaces, such as `SpeedController` and `Sendable`, but has the nice benefit of not having the wrapper contain any state itself.

Finally, I used my new `SendableSpeedController` in places where I needed both sets of functionality:

```java
interface RobotMap {
    public SendableSpeedController getLeftDrive();
    public SendableSpeedController getRightDrive();
}

class Maverick implements RobotMap {
    // SpeedControllerGroup implements SpeedController as well as Sendable
    SpeedControllerGroup leftGroup = new SpeedControllerGroup(new WPI_TalonSRX(8), new WPI_TalonSRX(9));
    SpeedControllerGroup rightGroup = new SpeedControllerGroup(new WPI_TalonSRX(4), new WPI_TalonSRX(5));

    @Override
    public SendableSpeedController getLeftDrive() {
        return SendableSpeedController.wrap(leftGroup);
    }

    @Override
    public SendableSpeedController getRightDrive() {
        return SendableSpeedController.wrap(rightGroup);
    }
}
```
