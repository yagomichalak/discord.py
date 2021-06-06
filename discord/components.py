from __future__ import annotations

from . import utils
from typing import Any, Dict, List, Union
import requests

import discord


def convert_emoji_to_dict(emoji) -> Dict[str, Union[str, int]]:

    emoji_dict = {}
    emoji = emoji.strip("<>")

    emoji_parts = emoji.split(":", 2)

    if len(emoji_parts) == 1:
        emoji_dict['name'] = emoji_parts[0]

    if len(emoji_parts) >= 2:
        emoji_dict['name'] = emoji_parts[1]

    if len(emoji_parts) >= 3:
        emoji_dict['id'] = emoji_parts[2]

        if emoji_parts[0] == 'a':
            emoji_dict['animated'] = True
    return emoji_dict

class Component:

    def __init__(self) -> None:
        self.__components: List[Dict[str, Union[int, str]]] = {'type': 1, 'components': []}

    @property
    def components(self) -> List[Dict[str, Union[int, str]]]:
        
        return self.__components

    @components.setter
    def components(self, value: List[Dict[str, Union[int, str]]]) -> None:
        
        self.__components = value

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
            emoji = convert_emoji_to_dict(emoji)

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

        self.components = {'type': 1, 'components': []}

        try:
            value = data['components']
        except KeyError:
            pass
        else:
            self.components['components'] = value

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
        :param response: The response data. """

        url = f"https://discord.com/api/v8/interactions/{response['id']}/{response['token']}/callback"

        json = {
            "type": 4,
            "data": {
                "content": "Congrats on sending your command!",
                "flags": 64
            }
        }
        requests.post(url, json=json)

    def defer(self, response):
        """ Waits for 15 minutes maximum to answer the interaction.
        :param response: The response data. """

        url = f"https://discord.com/api/v8/interactions/{response['id']}/{response['token']}/callback"

        json = {
            "type": 5,
            "data": {
                "content": None,

            }
        }
        requests.post(url, json=json)

    def ping(self, response):
        """ Waits for 15 minutes maximum to answer the interaction.
        :param response: The response data. """

        url = f"https://discord.com/api/v8/interactions/{response['id']}/{response['token']}/callback"

        json = {
            "type": 6,
        }
        requests.post(url, json=json)
    
    def update(self, response, content: str):
        """ Edits the interaction's original message.
        :param response: The response data. """

        url = f"https://discord.com/api/v8/interactions/{response['id']}/{response['token']}/callback"

        json = {
            "type": 7,
            "data": {
                "content": content
            }
            
        }
        requests.post(url, json=json)

    def update_response(self, response, content: str):
        """ Edits the interaction's original message.
        :param response: The response data. """

        url = f"https://discord.com/api/v8/webhooks/{response['application_id']}/{response['token']}/messages/@original"

        payload = {
            "content": content
            
        }
        requests.patch(url, data=payload)

    