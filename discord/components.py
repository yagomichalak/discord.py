from __future__ import annotations

import datetime

from . import utils
from typing import Any, Dict, List, Union


class Component:

    def __init__(self) -> None:
        self.__components: List[Dict[str, Union[int, str]]] = {'type': 1, 'components': []}

    @property
    def components(self) -> List[Dict[str, Union[int, str]]]:
        
        return self.__components

    def add_button(self, *, index, type, label, style, custom_id, emoji = None) -> object:

        """Adds a button to the component object.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------
        index: :class:`int`
            The index of the component in which the button will be inserted.
        type: :class:`int`
            The type of the button.
        label: :class:`str`
            The label for the button.
        style: :class:`int`
            The style of the button.
        custom_id: :class:`int`
            The custom ID for the button.
        emoji: :class:`str`
            The emoji for the button. [Optional]
        """

        button = {
            'type': type, 'label': label, 'style': style, 'custom_id': custom_id, 'emoji': emoji
        }

        try:
            self.__components['components'].append(button)
        except Exception as e:
            print(e)

        return self

    
    @classmethod
    def from_dict(cls, data):
        """Converts a :class:`dict` to a :class:`Component` provided it is in the
        format that Discord expects it to be in.

        You can find out about this format in the `official Discord documentation`__.

        .. _DiscordDocs: https://discord.com/developers/docs/resources/channel#...

        __ DiscordDocs_

        Parameters
        -----------
        data: :class:`dict`
            The dictionary to convert into an component.
        """
        # we are bypassing __init__ here since it doesn't apply here
        self = cls.__new__(cls)

        # fill in the basic fields

        self.__components = {'type': 1, 'components': []}

        for attr in ('buttons',):
            try:
                value = data[attr]
            except KeyError:
                continue
            else:
                setattr(self, '_' + attr, value)

        return self

    def clear_buttons(self):
        """Removes all buttons from this component."""
        try:
            self.__components['components'].clear()
        except AttributeError:
            self.__components['components'] = [] 