* how to make/run your code (a script or makefile is appreciated!)

Entry point: mini-vemo.py, you need to have python(version 2.7) on your machine.
Could be run using "python mini-vemo.py" or "python mini-venmo.py filename"
It may take a file name as input then execute every line of that file, otherwise it reads from standard input then execute.



* your design decisions
First of all, it is about money, so no floating number. Balance is an integer, $100.01 will be saved as 10001 (cents).

I wanted to do it in the MVC way, so after reading the instrutions, I made the model layer- models.py

State needs to be persisted, so there is a storage layer- storage.py, which is fully extensible. I tried to make a singleton class of storage, 
but then use the module as a singleton instead of writing a class . All its variables would be bound to the module, which could not be instantiated repeatedly anyways.
All data is stored in memory,  it doesn't make copys of instances. It is more like providing a lookup table right now,
The storage provides two functions, put will save an instance to "tables" under a list of its class name.
get_all will return a list of instances of that class.

View layers and control layers are in utils.py and mini-venmo.py

All meaningful strings has been moved to settings.py, which is easy to maintain.


I am in the final week, don't have too much time to write tests.
Run test using "python test.py" or you could choose any of the test class.
 
* the language you chose, and why you chose it
The script is in python, I like python.

