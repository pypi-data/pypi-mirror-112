'''
MIT License

Copyright (c) 2020 - Present nxtlo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from typing import Any, overload

__all__ = (
    'InvalidInput', 'InvalidTime',
    'PlayerNotFound', 'HashError',
    'ActivityNotFound', 'CharacterTypeError',
    'JsonError', 'ClanNotFound', 'CharacterNotFound',
    'NotFound', 'HTTPException'
)
class InvalidInput(Exception):
    pass

class InvalidTime(Exception):
    pass

class PlayerNotFound(Exception):
    pass

class HashError(Exception):
    pass

class ActivityNotFound(Exception):
    pass

class CharacterTypeError(Exception):
    pass

class JsonError(Exception):
    pass

class CharacterNotFound(Exception):
    pass

class HTTPException(Exception):
    pass

class ClanNotFound(Exception):
    pass


class NotFound(Exception):
    pass