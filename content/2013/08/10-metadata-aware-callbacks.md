---
Title: Metadata-aware Callbacks
Category: code
Tags: c++
---

The Problem
-----------

While working on a codebase at work, I came across a certain segment of code that did something close to the following:

- Create a stream to read message data
- Attach a callback for a special message type
- Start popping messages off the stream infinitely (until there are none left, but for this program that's theoretically infinite).
  After each message is popped, any callbacks for that message type are executed with a pointer to the popped message.

This seems straightforward.
However, the change I needed to make relied on one crucial feature: the ability to read what type of message was used.
The complication?
Not only is there no simple way in our library to do that, but the ONLY thing that differentiates the type of the message that was most recently read is the callback that is executed.
For compatibility reasons, I couldn't change this DataSource library, as other parts of the code rely on it having this structure. Here's a mockup of the initial code (C++):

	:::cpp
	// Code that is not essential to this problem has been simplified

	// Some example messages
	// These are read from a DataSource in a way that allows it to differentiate
	// between messages to determine the callback. (Not important for this code)
	class GameOverMessage{};

	class PlayerStatusMessage
	{
	public:
		unsigned lives;
	};

	// Example handlers
	void handleGameOverMessage(GameOverMessage*, void*)
	{
		cout << "Game over, you lose.\n";
	}

	void handlePlayerStatusMessage(PlayerStatusMessage* msg, void*)
	{
		cout << "Player has " << msg->lives << " lives\n";
	}

	class PopThread
	{
		void threadMain()
		{
			DataSource data;
			// tie is templated on the first parameter
			// Declaration:
			// template<typename MsgType> void tie(void(*)(MsgType*,void*),void*);
			data.tie(handleGameOverMessage, NULL);
			data.tie(handlePlayerStatusMessage, NULL);
			
			while(1)
			{
				data.pop();
			}
		}
	};


My Solution
-----------

### Original attempt

Looking at the above code, there's one thing that stands out as being useful for solving this problem: the `void*` arguments used in the callbacks. 
When tying the callback to the queue, the user specifies an argument (originally `NULL` in this example) that is passed to the callback each time the message type is received. 
With this in mind, I thought about ways to differentiate the types used. 
The easiest way I knew of for getting type information at runtime is the [type_info](http://cplusplus.com/type_info) class, but unfortunately in C++98 you can't store `type_info`.

However, you can store a `const char*`, which is exactly what the name method of a `type_info` returns.

With this in mind, I created the following:

	:::cpp
	class GameOverMessage{};

	class PlayerStatusMessage
	{
	public:
		unsigned lives;
	};

	void handleGameOverMessage(GameOverMessage* msg, void* typedata)
	{
		cout << "Game over, you lose.\n";
		// Here we assign the pointer to point to the info for this message type
		*(const char**)typedata = typeid(msg).name();
	}

	void handlePlayerStatusMessage(PlayerStatusMessage* msg, void* typedata)
	{
		cout << "Player has " << msg->lives << " lives\n";
		// Here we assign the pointer to point to the info for this message type
		*(const char**)typedata = typeid(msg).name();
	}

	class PopThread
	{
		const char* typedata(NULL);
		void threadMain()
		{
			DataSource data;
			// Notice the different arguments
			data.tie(handleGameOverMessage, &typedata);
			data.tie(handlePlayerStatusMessage, &typedata);
			
			while(1)
			{
				data.pop();
			}
		}
	};

### Generic attempt

Naturally, the original attempt had some issues, namely that I had to add that line to every callback.
However, I was only doing that as an intermediate step towards the final product.
Now that I knew what was needed, I wanted to write a wrapper around another callback.
I took a look at the argument types for hints about how this could be done:

- The function tying the callback to the message type takes a `void(*)(MessageType*, void*)`, the type of a callback
- Callbacks take `MessageType*` and `void*`, where the `void*` is used to pass an arbitrary argument
- MessageType in the above functions is the type of the specific message - the tie function is templated on `MessageType`
- We need to pass both the original argument, and the const `char*` that we used to store the type info

With these restrictions, I came up with the following:

	:::c++
	// Our message types are unchanged from the originals
	class GameOverMessage{};

	class PlayerStatusMessage
	{
	public:
		unsigned lives;
	};

	void handleGameOverMessage(GameOverMessage*, void*)
	{
		cout << "Game over, you lose.\n";
	}

	void handlePlayerStatusMessage(PlayerStatusMessage* msg, void*)
	{
		cout << "Player has " << msg->lives << " lives\n";
	}

	template<typename MsgType>
	class Callback
	{
	public:
		typedef void(*Function)(MsgType*, void*);
		Function func;
		const char** type;
		void* arg;

		Callback(Function f, const char** t, void* a)
		: func(f), type(t), arg(a)
		{}

		void operator()(MsgType* msg)
		{
			// Store our type info
			*type = typeid(MsgType).name();
			// Call with the required arguments
			func(msg, a);
		}
	}

	template<typename MsgType>
	void processCallback(MsgType* msg, void* callback)
	{
		// Unpack the callback structure and execute operator()
		(*(Callback<MsgType>*)callback)(msg);
	}

	class PopThread
	{
		const char* typedata(NULL);
		void threadMain()
		{
			DataSource data;

			// Create some Callback instances
			// As far as I saw, the template types must be specifically stated

			Callback<GameOverMessage> gameOverCallback(handleGameOverMessage, &typedata, NULL);
			data.tie(processCallback<GameOverMessage>, &gameOverCallback);

			Callback<PlayerStatusMessage> playerStatusCallback(handlePlayerStatusMessage, &typedata, NULL);
			data.tie(processCallback<PlayerStatusMessage>, &playerStatusCallback);
			
			while(1)
			{
				data.pop();
			}
		}
	};


Postmortem
----------

I wrote this month ago. What are my thoughts on it now?

- Creating a callback that hooks into this system now takes two full statements, which is a little more hassle for users
- Any callback using the system is supported, there are no special hooks in the code that need to be adjusted to make it work with a new type
- This callback system wraps the original callback system without modifying the interface, 
  so the use of any original callback can be changed to this system without changing the original callback
- The code isn't quite as intuitive as it could be
- Creating the callbacks involves lots of address-of operators (&amp;), which make the code a little bit harder to read. (This should be possible to change by passing the Callback constructor arguments by reference and using the address-of operator inside the constructor)
- Template arguments are used much more - more verbose
- If more metadata was required in the future, storage for them could be stored in the Callback interface

Was this a good idea?
I believe that it was, mainly because it was a convenient but powerful addition, but it could probably be cleaned up and simplified quite a bit.
I'd be interested in any improvements, though.

Here are some possibilities:

- Remove the need for the address-of operator during construction
- Create a CallbackUser interface that contains storage for the typeinfo string (and possibly any other metadata).
  A class that uses the Callback class could then inherit from CallbackUser,
  and then have a helper function like createCallback that only required the original arguments
- Remove the need to specify template arguments in some places
- Take advantage of C++11 features such as `auto` and `lambda functions` to ease the creation of new callbacks
