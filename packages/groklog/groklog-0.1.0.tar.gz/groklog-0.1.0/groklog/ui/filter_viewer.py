import copy
from queue import Queue

from asciimatics.parsers import AnsiTerminalParser
from asciimatics.strings import ColouredText
from asciimatics.widgets import TextBox

from groklog.process_node import GenericProcessIO, ProcessNode

_line_cache = {}


class FilterViewer(TextBox):
    def __init__(self, filter: GenericProcessIO, height: int):
        super().__init__(
            height,
            name=f"FilterViewer-{filter.name}-{filter.command})",
            readonly=True,
            as_string=False,
            line_wrap=True,
            parser=AnsiTerminalParser(),
        )
        self.filter = filter
        self._data_queue = Queue()
        self.custom_colour = "filter_viewer"
        self._value = [ColouredText("", self._parser, colour=None)]

        # Create subscriptions
        self._processed_data_queue = Queue()
        """self._add_stream pushes to here, and self.update pulls the results"""

        filter.subscribe_with_history(
            ProcessNode.Topic.STRING_DATA_STREAM, self._add_stream, blocking=False
        )

    def process_event(self, event):
        # TODO: Change keyboard up/down events to immediately move up/down a line.
        return super().process_event(event)

    def update(self, frame_no):
        changed = False
        while self._processed_data_queue.qsize():
            changed = True
            self._value += self._processed_data_queue.get_nowait()

        if changed:
            self.reset()

        return super().update(frame_no)

    def _add_stream(self, append_logs: str):
        """Append text to the log stream. This function should receive input from
        the filter and display it."""

        # TODO: Consider limiting split size on massive files?
        # TODO: Consider appending only after parsing colors

        last_colour = self._value[-1].last_colour

        # TODO: remove multiple newlines
        new_lines = []
        for line in append_logs.split("\n"):
            # TODO
            cache_key = (line, last_colour, self.filter.name)
            if cache_key in _line_cache:
                value = _line_cache[cache_key]
            else:
                try:
                    value = ColouredText(line, self._parser, colour=last_colour)
                except IndexError:
                    # TODO: Create an issue on github for this
                    continue
                _line_cache[cache_key] = value

            # value = ColouredText(line, self._parser, colour=last_colour)
            new_lines.append(value)
            last_colour = value.last_colour

            # Release chunks of values at a time, so the UI has something to update with
            if len(new_lines) > 100:
                self._processed_data_queue.put(new_lines)
                new_lines = []

        # Put this in a queue to be picked up by the main thread, in self.update
        self._processed_data_queue.put(new_lines)

    @property
    def value(self):
        self._value = [ColouredText("", self._parser, colour=None)]
        return self._value

    @value.setter
    def value(self, value):
        """This value should never be used. It's been replaced by _add_stream"""
        pass
