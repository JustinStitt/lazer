# Lazer

Lazer is a Python library that provides a convenient way to expose Python functions as schemas for OpenAI chat models.

For those not in the know: [OpenAI - Function Calling](https://platform.openai.com/docs/guides/gpt/function-calling)

### What it Does

Allows you to more easily inform GPT about functions in your code 😊

> **Warning** don't RCE yourself lol

## Installation

To install Lazer, simply run:

```bash
pip install lazer
```

## Usage

Here is an example of how to use Lazer:

```python
from lazer import Lazer, LazerConversation

lazer = Lazer()

# GPT is now made aware of your function `qux`
@lazer.use
def qux(num: int, name: str) -> str:
    """Retrieve a number and a name from the user and compute the qux of it"""
    return str(num + len(name) * 13)

conversation = LazerConversation(lazer)
response = conversation.talk("What is the qux of 3 and steven")
print(response)
# ... 117 ...
```

> **Note** You do not have to use the LazerConversation GPT frontend, you can simply use
the Lazer functions `.use` (decorator) and `.get_functions()` as well as
`.dispatch()` to build your own GPT frontend utilizing Lazer.

> **Note** If you are using the LazerConversation frontend be sure to set an
`OPENAI_API_KEY` in a `.env` file somewhere in your directory.


## Demo

Go to [demo/](demo/) for some demo code.


## Authors:

* @JustinStitt
* @diamondburned
