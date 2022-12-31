---
Title: Metadata-aware Callbacks Revised
categories: [code]
Date: "2014-04-01"
Tags:
- c++
---

As I mentioned in [an earlier post], I wasn't completely happy with the final result of my changes. There were a few things I felt were problematic:

- Creating a callback required two statements
- Code was less intuitive
- Many address-of operators (&amp;)
- Required visible template arguments
- Hard-coded to work with a single bit of "environment" information

After some playing around, I came up with some changes that made the code much nicer, in my opinion. There was jut one problem: A single function overload needed to be added to DataSource. Doing this, though, allowed for greatly simplified code overall while eliminating many problems.

	:::c++
	#include <iostream>
	#include <typeinfo>
	#include <functional>
	using namespace std;

	//----------------------------------------------------------------------------------------------
	// Required for testing - just the bare functions

	// Basic data source
	struct DataSource {
		// Set up a callback for a specific message type
		// The overloads are needed to be backwards-compatible using IFTI
		template<typename MsgType>
		void tie(void(*func)(MsgType*, void*), void* arg)
		{
			return this->tie(function<void(MsgType*,void*)>(func), arg);
		}
		template<typename MsgType>
		void tie(function<void(MsgType*,void*)>, void*)
		{
			// This contains the "real" implementation
		}
		// Remove a message from the queue and call the appropriate callback
		void pop() {};
	};

	//----------------------------------------------------------------------------------------------
	// Messages and handlers
	// Our message types are unchanged from the originals

	struct GameOverMsg {};
	void handleGameOver(GameOverMsg*, void*)
	{
		cout << "Game over, you lose.\n";
	}


	struct PlayerStatusMsg {
		unsigned lives;
	};
	void handlePlayerStatus(PlayerStatusMsg* msg, void*)
	{
		cout << "Player has " << msg->lives << " lives\n";
	}

	//----------------------------------------------------------------------------------------------
	// Wrapper code

	// Basic environment wrapper
	// This contains all of the "current running information"
	// Designed to be easily expandable and have context about the source
	class Environment
	{
	public:
		// Update the environment.
		// Parameters or logic can be added or changed as needed
		template<typename MsgType>
		void update()
		{
			m_typedata = typeid(MsgType).hash_code();
		}

		// Access the type data
		size_t typedata()
		{
			return m_typedata;
		}
	private:
		size_t m_typedata;
	};

	// Handle the actual tying
	// Creates a new function to use
	// The overloads are needed to be backwards-compatible using IFTI
	// These could be adapted to be overloads of DataSource::tie
	template<typename MsgType>
	void tie_cb(DataSource& data, void(*func)(MsgType*, void*), Environment& e, void* arg)
	{
		return tie_cb(data, function<void(MsgType*,void*)>(func), e, arg);
	}

	template<typename MsgType>
	void tie_cb(DataSource& data, function<void(MsgType*, void*)> func, Environment& e, void* arg)
	{
		data.tie<MsgType>([&](MsgType* msg, void* arg) {
			e.update<MsgType>();
			return func(msg, arg);
		}, arg);
	}

	//----------------------------------------------------------------------------------------------
	// New version of PopThread

	class PopThread
	{
		Environment e;
	public:
		void threadMain()
		{
			DataSource data;

			// This replaces the old "data.tie(...)" calls
			tie_cb(data, handlePlayerStatus, e, NULL);
			tie_cb(data, handleGameOver, e, NULL);

			while(true) {
				data.pop();
			}
		}
	};

All of the previous problems were addressed, at the expense of a single function overload in the DataSource. In my original scenario, this wasn't doable for the actual project.

These changes rely on a few C++11 features:

- `std::function`
- `type_info::hash_code`
- Lambdas
- Use of references instead of pointers (Not C++11, but still a useful change)

The big change I'm happy about is that the wrapper parts are still standalone, and require minimal changes to adapt old code to the new system, where "new system" means "tie_cb and Environment". Although those could be made part of the DataSource library anyways, that kind of puts too much functionality in places that it doesn't belong in. The way the code above behaves, it merely uses C++11 function types instead of direct function pointers, with a forwarding function in place to handle the IFTI and conversion, which is a non-breaking change that is (quite possibly) more maintainable.

[an earlier post]: {{< ref "/blog/2013/08/10-metadata-aware-callbacks.md" >}}
