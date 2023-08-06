#!/usr/bin/env python3

"""
comboboxtext:an enriched Gtk.ComboBoxText class
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import bisect

# Assume gtk availability check done at application level
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ComboBoxText(Gtk.ComboBoxText):
    """Enriched combox, which allows for better manipulation of entries.
       The basic idea is that the list of entries is maintained within 
       the class. Some functions are overwritten to maintain this list
       of entries. Additional functions include: 
       - text_already_present
       - insert_text_sorted
       - text_remove_text
       - update_entries
       - entries"""

    def __init__(self):
        self._entries = []
        super().__init__()

    def insert_text(self, pos, text_id, text):
        super().insert(pos, text_id, text)
        npos = len(self._entries) if pos < 0 else pos
        self._entries.insert(npos, text)

    def append_text(self, text):
        super().append_text(text)
        self._entries.append(text)

    def text_already_present(self, text):
        "Returns a Bool indicating of the text is already in the entries"
        return text in self._entries

    def insert_text_sorted(self, text, duplicates=False):
        "Inserts text sorted into the combobox"
        if not duplicates and self.text_already_present(text):
            return
        pos = bisect.bisect_left(self._entries, text)
        self.insert_text(pos, None, text)

    def text_remove(pos):
        super().text_remove(pos)
        self._entries.pop(pos)

    def remove_all(self):
        super().remove_all()
        self._entries = []

    def text_remove_text(self, text):
        "Removes the text if if is already in the list of entries"
        pos = 0
        for entry in self._entries:
            if entry == text:
                self.test_remove(pos)
                return
            pos += 1

    def update_entries(self, entries):
        "Updates the complete list of entries with a new list"
        active_entry = self.get_active_text()
        self.remove_all()
        for entry in entries:
            self.append_text(entry)
        pos = 0
        for entry in self._entries:
            if entry == active_entry:
                self.set_active(pos)
                return
            pos += 1
        if len(self._entries) > 0:
            self.set_active(0)

    def entries(self):
        "Returns a list of entries"
        return self._entries


