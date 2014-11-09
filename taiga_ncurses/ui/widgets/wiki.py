# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.wiki
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from taiga_ncurses import data

from . import generic


class WikiPage(urwid.WidgetWrap):
    on_wiki_page_change = None

    def __init__(self, project):
        self.project = project

        self.widget = urwid.Pile([generic.ListText("No page found")])
        super().__init__(self.widget)

    def populate(self, wiki_pages, wiki_page):
        items = tuple((data.slug(p), p) for p in wiki_pages)
        selected = wiki_page
        pages_combo = generic.ComboBox(items, selected_value=selected, style="cyan",
                                        on_state_change=self.on_wiki_page_change)

        page_combo_size = max([len(p["slug"]) for p in wiki_pages]) + 8

        content_widget = urwid.Edit(edit_text=data.content(wiki_page), multiline=True, wrap='any',
                                    allow_tab=True)

        self.widget.contents = [
            (generic.RowDivider(div_char=" "), ("weight", 0.1)),
            (urwid.Padding(urwid.LineBox(pages_combo), "center", page_combo_size, 10, 0, 0), ('weight', 1)),
            (generic.RowDivider(div_char=" "), ("weight", 0.1)),
            (content_widget, ('pack', None)),
            (generic.RowDivider(div_char=" "), ("weight", 0.1)),
            (urwid.Padding(self._buttons(), right=2, left=2), ('weight', 1)),
            (generic.RowDivider(div_char=" "), ("weight", 0.1))
        ]
        self.widget.contents.focus = 3

    def _buttons(self):
        self.save_button = generic.PlainButton("Save")
        self.reset_button = generic.PlainButton("Reset")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.save_button, right=2, left=2),
                                              "submit-button") ))
        colum_items.append((2, urwid.Text(" ")))
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.reset_button, right=1, left=2),
                                              "cancel-button") ))
        return urwid.Columns(colum_items)
