---
Title: Searching through a file with Python
Category: code
Date: "2014-07-06"
Tags:
- python
---

At work, I had to deal with a situation involving scanning a file to find matches.

The basic idea was that I wanted to find two things:

- Lines that start with `"CATEGORY"`
- Lines that start with a specific string (part of the filename)

From these two pieces of data, I needed:

- If any of the lines start with the given string
- If the given string appears as many times as the `"CATEGORY"` string

I wanted to try to do it as nicely as possible. I had two possible starting points:

	:::python

	def driver(func):
		'''
		Driver for testing all these functions:
		Used as driver(get_info_func)(lines, header)
		'''
	    def _use(lines, header):
			ctg, hdr = func(lines, header)
			return bool(hdr), hdr == ctg
		return _use

	def get_info1(lines, header):
		# Using an ordinary for loop - the "straightforward" way
		ctg, hdr = 0, 0
		for line in lines:
			if line.startswith("CATEGORY"):
				ctg += 1
			if line.startswith(header):
				hdr += 1
		return ctg, hdr
	
	def get_info2(lines, header):
		# Using sum and generators
		ctg = sum(line.startswith("CATEGORY") for line in lines)
		hdr = sum(line.startswith(header) for line in lines)
		return ctg, hdr

There are problems, in my opinion, with each one. `get_info1` is extremely verbose, and `get_info2` iterates over the lines twice. Ideally, the final result would incorporate the better parts of both: the efficiency of `get_info1` and the succinctness of `get_info2`.

With these ideas in mind, I had to look for other options:

	:::python
	def get_info3(lines, header):
		# Using reduce:
		return reduce(lambda a, line: (a[0]+line.startswith("CATEGORY"), a[1]+line.startswith(header)), lines, (0, 0))

This was almost good, but reduce tends to make code extremely verbose and illegible.

To get (what I feel is) the ideal solution, I realised that I was, for lack of a better term, thinking vertically instead of horizontally. Python has a function that changes "rows of columns" into "columns of rows", called `zip`. By taking advantage of `zip` and `map`, it was possible to create a solution that was very short and still efficient:

	:::python
	def get_info4(lines, header):
		# Using zip:
		return map(sum, zip(*((line.startswith("CATEGORY"), line.startswith(header)) for line in lines)))

Unfortunately, the resulting function does seem to get a bit cluttered, though still more legible than the reduce version (`get_info3`). The easiest way to explain it is to decompose the functions:

	:::python

	def get_info4_expanded(lines, header):
		# Get the basic info for each line
		linedata = ((line.startswith("CATEGORY"), line.startswith(header)) for line in lines)
		# Transpose the columns and rows
		columns = zip(*linedata)
		# Sum the columns
		return map(sum, columns)

This final function can be made somewhat lazy by using the excellent `itertools` module, and made cleaner by extracting the lambda:

	:::python
	from itertools import imap, izip
	def get_info5(lines, header):
		# Using itertools
		f = lambda l: (l.startswith("CATEGORY"), l.startswith(header))
		return imap(sum, izip(*imap(f, lines)))

If it weren't for the need to do anything with that data immediately, the function would be nice and lazy! This seems to be significantly easier to read than the original two functions, at least for a developer who's familiar with the built-in functions (`zip` and `map` specifically).
