---
Title: Java Interfaces and Extensions
Category: code
Tags:
- java
---

Recently I ran into a small issue in Java.

A library that I needed to use, and couldn't modify, had a particular class that I wanted to make a mock of.
My desire was to have either a real version of this class, or a fake version for testing purposes.
While there are some tools that can do this (like [Mockito]), they're either a large dependency, or specifically state you shouldn't mock something you don't own.
Luckily, I found an interesting solution that suited my needs much more easily, with zero libraries required.

Assume you have a class that you can't modify:

```java
public class Foo {
    private int value;
    public Foo(int value) {
        this.value = value;
    }
    public void foo() {
        System.out.println("I'm a real Foo with value = " + value);
    }
    public void incr() {
        value++;
    }
}
```

How can we make this testable?
One way is to derive from `Foo`, and override every method to do nothing.
This could work, but it has a few flaws:

- Requires use of any constructors that the base class has
- Carries around internal state that never gets used

A more convenient way to do similar is to create an interface first:

```java
public interface FooLike {
    void foo();
    void incr();
}
```

This is the interface that we'll be using.
Now, we create a new class that extends `Foo` and implements `FooLike`:

```java
public class FooWrapped extends Foo implements FooLike {
    // Forward all constructors
    public FooWrapped(int value) {
        super(value);
    }
}
```

There's no more setup that needs to be done!
Java deduces that `foo` and `incr` from the base class `Foo` fulfil the requirements for the methods from `FooLike`.
There's no need to forward or override any calls.

Now, writing the mock class is easy:

```java
public class MockFoo implements FooLike {
    private int value;
    public void setValue(int value) {
        this.value = value;
    }
    @Override
    public void foo() {
        System.out.println("I'm a mock with value = " + value);
    }
    @Override
    public void incr() {
        value++;
    }
}
```

---

So what happens if the base class you want to use is `final`?
Then, you have to go for more of a wrapper class:

```java
public class FooWrapped implements FooLike {

    private Foo fooValue;

    public FooWrapped(int value) {
        fooValue = new Foo(value);
    }

    // For passing into any API functions that use the raw class,
    // since inheritance isn't applicable here
    public Foo getRaw() {
        return fooValue;
    }

    @Override
    public void foo() {
        fooValue.foo();
    }

    @Override
    public void incr() {
        fooValue.incr();
    }
}
```

The end result is similar, just with a lot more boilerplate.
The number of constructors can potentially be brought down by having the caller create the raw `Foo` instance.

[Mockito]: https://site.mockito.org/
