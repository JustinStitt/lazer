# Lazer

Lazer is a Python library that provides a convenient way to expose Python functions as schemas for OpenAI chat models.

### What it Does

Allows you to more easily inform GPT about your

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
response = await conversation.talk("What is the qux of 3 and steven")
print(response)
# ... 117 ...
```

### Demo

Go check `lazer/demo/app.py` for a dummy app

To run this `python -m demo.app`


#### Authors:

* @JustinStitt
* @diamondburned
