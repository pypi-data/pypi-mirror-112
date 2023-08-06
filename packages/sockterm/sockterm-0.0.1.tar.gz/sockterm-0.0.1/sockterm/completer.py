from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder
from sockterm.commands import Commands

command_keywords = ["connect", "subscribe", "emit", "disconnect", "call"]

class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, command_keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))
