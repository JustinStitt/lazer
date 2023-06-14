# Demo

## Dummy App

Go check `lazer/demo/app.py` for a dummy app

To run this `python -m demo.app`

## GPT Command Interpreter

Go check `lazer/demo/gptbackdoor.py` for a GPT app that acts as a natural
language command interpreter.

To run this `python -m demo.gptbackdoor`

### Example

```
> What is in lazer/__init__.py
< The `lazer/__init__.py` file contains the initialization of the `Lazer` and `LazerConversation` classes. 

The `Lazer` class is responsible for managing the functions and their schemas. It initializes with an empty list of functions and a mapping of function names to functions. It also has methods to dispatch function calls, retrieve the list of functions, and add new functions to the list.

The `LazerConversation` class represents a conversation with the `Lazer` instance. It initializes with an empty list of messages, a reference to the `Lazer` instance, and the chat completion arguments provided. It has a `talk` method that takes user input and uses the OpenAI Chat API to generate a response. The conversation messages and function calls are stored in the `self.messages` list.

> Write a README for this code and write that into the README.md file.
< I have written the README and saved it in the README.md file.
```

### Exposed APIs

```
> The source code for your exposed functions are at demo/gptbackdoor.py. What functions are exposed to you?
< The exposed functions are:
1. ls: List files in the current directory.
2. cat: Read the content of a file.
3. override_file: Override a file with new content.
4. quit: Quit the program.
5. calculate: Calculate an expression using the bc command.
```

