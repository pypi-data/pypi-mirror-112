import argparse
from pathlib import Path
import sys
import fire
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from sockterm.completer import CommandCompleter
from sockterm.version import VERSION
from sockterm import commands

session = PromptSession(history=FileHistory(str(Path.home() / ".sockterm_history")))

def main():
    print(f"welcome to sockterm version {VERSION}")
    print("for help, type help")
    print("")
    while True:
        try:
            user_input = session.prompt("sockterm>",
                                        auto_suggest=AutoSuggestFromHistory(),
                                        completer=CommandCompleter())
            fire_obj = fire.Fire(commands.Commands(), command=user_input, name="sockterm")
        except Exception as e:
            if isinstance(e, EOFError):
                print("Bye!")
                sys.exit()
            else:
                print(e)
        except fire.core.FireExit:
            pass
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()
