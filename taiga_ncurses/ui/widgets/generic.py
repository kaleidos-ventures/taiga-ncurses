# -*- coding: utf-8 -*-

"""
taiga_ncurses.ui.widgets.generic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import urwid

from . import mixins, utils


def box_solid_fill(char, height):
    sf = urwid.SolidFill(char)
    return urwid.BoxAdapter(sf, height=height)


def wrap_in_whitespace(widget, cls=urwid.Columns):
    whitespace = urwid.SolidFill(" ")
    return cls([whitespace, widget, whitespace])


def center(widget):
    return wrap_in_whitespace(wrap_in_whitespace(widget), cls=urwid.Pile)


def banner():
    bt = urwid.BigText("Taiga", font=urwid.font.HalfBlock7x7Font())
    btwp = urwid.Padding(bt, "center", width="clip")
    return urwid.AttrWrap(btwp, "green")


def button(text, align=None):
    return PlainButton(text.upper(), align)


def editor(mask=None):
    if mask is None:
        return urwid.Edit()
    else:
        return urwid.Edit(mask=mask)


class Header(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self):
        text = urwid.Text("TAIGA")
        self.account_button = PlainButton("My account")
        cols = urwid.Columns([
            ("weight", 0.9, text),
            ("weight", 0.1, urwid.AttrMap(self.account_button, "account-button")),
        ])
        super().__init__(urwid.AttrMap(cols, "green-bg"))


class Notifier(mixins.NotifierMixin, mixins.NonSelectableMixin, urwid.Text):
    pass


class PlainButton(mixins.PlainButtonMixin, urwid.Button):
    ALIGN = "center"

    def __init__(self, text, align=None):
        super().__init__(text)
        self._label.set_align_mode(self.ALIGN if align is None else align)


class SubmitButton(PlainButton):
    def __init__(self, text, align=None):
        super().__init__(text, align)


class CancelButton(PlainButton):
    def __init__(self, text, align=None):
        super().__init__(text, align)


class FooterNotifier(Notifier):
    ALIGN = "left"
    ERROR_PREFIX = "[ERROR]: "
    ERROR_ATTR = "footer-error"
    INFO_PREFIX = "[INFO]: "
    INFO_ATTR = "footer-info"


class Footer(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self, notifier):
        assert isinstance(notifier, FooterNotifier)
        cols = urwid.Columns([
            ("weight", 0.9, urwid.AttrMap(notifier, "footer")),
            ("weight", 0.1, urwid.AttrMap(PlainButton("? Help"), "help-button")),
        ])
        super().__init__(cols)




class Grid(mixins.ViMotionMixin, mixins.EmacsMotionMixin, urwid.GridFlow):
    pass


class Tabs(mixins.NonSelectableMixin, urwid.WidgetWrap):
    def __init__(self, tabs, focus=0):
        self.tab_list = urwid.MonitoredFocusList(tabs)
        self.tab_list.focus = focus
        self.tab_list.set_focus_changed_callback(self.rebuild_tabs)

        cols = [urwid.AttrMap(self.tab(t), "active-tab" if i == self.tab_list.focus else "inactive-tab")
                                for i, t in enumerate(tabs)]
        self.columns = urwid.Columns(cols)

        super().__init__(self.columns)

    def rebuild_tabs(self, new_focus):
        for i, c in enumerate(self.columns.contents):
            widget, _ = c
            widget.set_attr_map({None: "active-tab" if i == new_focus  else "inactive-tab"})

    def tab(self, text):
        return urwid.LineBox(urwid.Text(text + " "))


class HelpPopup(urwid.WidgetWrap):
    # FIXME: Remove solid_fill and use the Fill decorator
    def __init__(self, title="Help", content={}):
        contents = [box_solid_fill(" ", 1)]

        for name, actions in content:
            contents += self._section(name, actions)
            contents.append(box_solid_fill(" ", 1))

        contents.append(self._buttons())
        contents.append(box_solid_fill(" ", 1))

        self.widget = urwid.Pile(contents)
        super().__init__(urwid.AttrMap(urwid.LineBox(urwid.Padding(self.widget, right=2, left=2),
                                                     title), "popup"))
    def _section(self, name, actions):
        items = [urwid.Text(("popup-section-title", name))]
        items.append(box_solid_fill(" ", 1))

        for keys, description in actions:
            colum_items = [(18, urwid.Padding(ListText(keys, align="center"), right=2))]
            colum_items.append(urwid.Text(description))
            items.append(urwid.Padding(urwid.Columns(colum_items), left=2))

        return items

    def _buttons(self):
        self.close_button = PlainButton("Close")

        colum_items = [("weight", 1, urwid.Text(""))]
        colum_items.append((15, urwid.AttrMap(urwid.Padding(self.close_button, right=1, left=2),
                                              "popup-cancel-button")))
        return urwid.Columns(colum_items)


class ListCell(urwid.WidgetWrap):
    def __init__(self, text):
        text_widget = urwid.AttrMap(ListText(text), "default")
        widget = urwid.AttrMap(urwid.LineBox(text_widget), "green")
        super().__init__(widget)


class ButtonCell(urwid.WidgetWrap):
    def __init__(self, button):
        text_widget = urwid.AttrMap(button, "default", "focus-header")
        widget = urwid.AttrMap(urwid.LineBox(text_widget), "green")
        super().__init__(widget)


class ListText(mixins.IgnoreKeyPressMixin, urwid.Text):
    def __init__(self, text, align="center"):
        super().__init__(text, align=align)


class RowDivider(urwid.WidgetWrap):
    def __init__(self, attr_map="default", div_char="-"):
        widget = urwid.AttrMap(urwid.Divider(div_char), attr_map)
        super().__init__(widget)


class SemaphorePercentText(ListText):
    """
    Get a number and a max_value and print it with a concrete color:
        * red: value <= 20%
        * yellos: 20% < vale < max_value
        * green: vale == max_vale

    If invert value is True red will be green and viceversa
    """
    def __init__(self, value, max_value=100.0, invert=False):
        color = "yellow"
        if value <= max_value * 0.2:
            color = "red" if not invert else "green"
        elif value == max_value:
            color = "green" if not invert else "red"
        text = [(color, str(value))]

        super().__init__(text)


class ComboBox(urwid.PopUpLauncher):
    """
    A button launcher for the combobox menu
    """
    signals = ["change"]

    def __init__(self, items, selected_value=None, style="default", enable_markup=False,
                 on_state_change=None, user_data=None):
        self.menu = ComboBoxMenu(items, style)

        self.enable_markup = enable_markup

        self.on_state_change = on_state_change
        self.user_data = user_data

        selected_item = utils.find(lambda x: x.value == selected_value, self.menu.items) or self.menu.items[0]
        selected_item.set_state(True)
        if self.enable_markup:
            self._button = ComboBoxButton(selected_item.get_label_markup(), align="left")
        else:
            self._button = ComboBoxButton(selected_item.get_label(), align="left")


        super().__init__(self._button)

        urwid.connect_signal(self.original_widget, "click", lambda b: self.open_pop_up())
        for i in self.menu.items:
            urwid.connect_signal(i, "click", self.item_changed)
            urwid.connect_signal(i, "quit", self.quit_menu)

    def create_pop_up(self):
        """
        Create the pop up widget
        """
        return self.menu

    def get_pop_up_parameters(self):
        """
        Configuration dictionary for the pop up
        """

        return {"left": 2,
                "top": 1,
                "overlay_width": max([len(i.get_label()) for i in self.menu.items]) + 7,
                "overlay_height": len(self.menu.items) + 2}

    def item_changed(self, item, state):
        if state:
            if self.enable_markup:
                selection = item.get_label_markup()
            else:
                selection = item.get_label()
            self._button.set_label(selection)

        if self.on_state_change:
            self.on_state_change(self, item, state, user_data=self.user_data)

        self.close_pop_up()
        self._emit("change", item, state)

    def quit_menu(self, widget):
        self.close_pop_up()

    def get_selected(self):
        return self.menu.get_selected()


class ComboBoxButton(PlainButton):
    combobox_mark = "▼"

    def set_label(self, label):
        s = " {}".format(self.combobox_mark)
        super().set_label([label, s])


class ComboBoxMenu(urwid.WidgetWrap):
    """
    A menu shown when parent is activated.
    """
    signals = ["close"]

    def __init__(self, items, style):
        """
        Initialize items list

        Item must be a list of dicts with "label" and "value" items.
        """
        self.group = []
        self.items = []

        for i in items:
            self.append(i)

        self.walker = urwid.Pile(self.items)
        super().__init__(urwid.AttrWrap(urwid.Filler(urwid.LineBox(self.walker)), "selectable", style))

    def append(self, item):
        """
        Append an item to the menu
        """
        r = MenuItem(self.group, item)
        self.items.append(r)

    def get_item(self, index):
        """
        Get an item by index
        """
        return self.items[index]

    def get_selected(self):
        """
        Return the index of the selected item
        """
        for index, item in enumerate(self.items):
            if item.state is True:
                return item
        return None


class MenuItem(urwid.RadioButton):
    """
    A RadioButton with a 'click' signal
    """
    signals = urwid.RadioButton.signals + ["click", "quit"]

    def __init__(self, group, label_value, state='first True', on_state_change=None, user_data=None):
        markup, value = label_value

        self._markup = markup
        self.value = value

        super().__init__(group, markup, state='first True', on_state_change=None, user_data=None)

    def get_label_markup(self):
        return self._markup

    def keypress(self, size, key):
        command = urwid.command_map[key]

        if command == "activate":
            self._emit("click", True)
        elif command == "menu":
            self._emit("quit")

        super(MenuItem, self).keypress(size, key)
        return key
