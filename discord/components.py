from __future__ import annotations

import datetime
from discord.errors import HTTPException

from . import utils
from typing import Any, Dict, List, Union
import requests
import json


class Component:

    def __init__(self) -> None:
        self.__components: List[Dict[str, Union[int, str]]] = {'type': 1, 'components': []}

    @property
    def components(self) -> List[Dict[str, Union[int, str]]]:
        
        return self.__components

    def add_button(self, *, style: int, custom_id: str = '', label: str = '', url: str = '', emoji: str = None, type: int = 2, disabled: bool = False) -> object:

        """Adds a button to the component object.

        This function returns the class instance to allow for fluent-style
        chaining.

        Parameters
        -----------

        style: :class:`int`
            The style of the button.
        custom_id: :class:`int`
            The custom ID for the button. (Required/Optional)
        label: :class:`str`
            The label for the button.
        url: :class:`str`
            The redirect link for the button (Required/Optional)
        emoji: :class:`str`
            The emoji for the button. [Optional]
        type: :class:`int`
            Type of component. (Default = 2)
        disabled: :class:`bool`
            Whether the button is disabled. (Default = False)
        """

        if emoji is not None:
            emoji = {'name': emoji}

        if (style in (1, 2, 3, 4) and not custom_id) or (style == 5 and not url) or (custom_id and url):
            raise requests.HTTPError

        button = {
            'type': 2, 'label': label, 'style': style, 'custom_id': custom_id, 'url': url, 'emoji': emoji, 'disabled': disabled
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
        """ Removes all buttons from the component."""

        try:
            self.__components['components'].clear()
        except AttributeError:
            self.__components['components'] = [] 



class Button:

    # __slots__ = ('label', 'style', 'custom_id', 'url', 'emoji', 'type', 'disabled')

    def __init__(self, style: int, custom_id: str = '', label: str = '', url: str = '', emoji: Dict[str, str] = None, type: int = 2, disabled: bool = False) -> None:
        self.label = label
        self.style = style
        self.custom_id = custom_id
        self.url = url
        self.emoji = emoji
        self.type = type
        self.disabled = disabled

        
    def success(self, response):
        """ Marks the interaction as a success.
        :param The response data. """

        url = f"https://discord.com/api/v8/interactions/{response['id']}/{response['token']}/callback"

        json = {
            "type": 4,
            "data": {
                "content": "Congrats on sending your command!",
                "flags": 64
            }
        }
        r = requests.post(url, json=json)