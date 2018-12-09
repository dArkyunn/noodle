# noodle

Noodle is a ssh wrapper and server manager written in Python.

## Installation

1. Clone this repository to a directory of your liking using `git clone https://github.com/dArkyunn/noodle.git`.
2. Create a sym-link of noodle.py to a directory in your `PATH` environmental variable.
3. Start using noodle!

Note that you need python3 for noodle to work.

## Usage

General form: `noodle [option] <arguments>`

Options:

```markdown
help, h - no arguments, shows help page
add, a - no arguments, prompts the user to add a new entry into the config
delete, del, d - one argument: <name> of an entry present in config, removes an entry from the config
edit, e - one argument: <name> of an entry present in config, prompts the user to enter new values for an entry
list, l - no arguments, lists out all entries in the config
connect, con, c - one argument: <name> of an entry present in config, connects to a server
```

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3](https://github.com/dArkyunn/noodle/blob/master/LICENSE)
