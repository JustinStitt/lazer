# WIP


User will add `@lazer` to functions they want GPT to be able to use

Now, we have some options...

how do we inform OpenAI of our functions?

1) Expose some sort of `Lazer.functions` or `lazer.get_functions()` and allow the user to pass into `ChatComplete.create()` themselves
2) Hook the OpenAI wrapper and automatically inject `functions=our_stuff`
