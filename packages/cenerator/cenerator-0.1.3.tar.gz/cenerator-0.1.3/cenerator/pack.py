"""
Copyright (c) 2021 Zakru

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
"""

from contextlib import contextmanager
import json
from numbers import Real
from pathlib import Path
import shutil
from typing import Callable, Generator, List, Optional, Union

from .identifier import Identifier
from .value import StorageValue


class C:

    def __init__(self, pack: 'Pack', c: Callable[[str], None]):
        self.pack = pack
        self.c = c

    def __call__(self, *args, **kwargs) -> None:
        self.c(*args, **kwargs)

    @contextmanager
    def ex(self, setup: str = '') -> Generator['C', None, None]:
        identifier = self.pack.parse_identifier(f'ex_{self.pack._ex_c}')
        self.pack._ex_c += 1

        file_path = self.pack._data_dir / self.pack.parse_identifier(f"{identifier.namespace}:{'functions/' + identifier.name}").data_path('.mcfunction')
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            yield C(self.pack, lambda c: file.write(f'{c}\n'))
        self(f'execute {setup} run function {identifier}')

    def store_storage(self, type: str, command: str, scale: float = 1) -> StorageValue:
        """Store the result of a command in storage and return its reference"""
        p = self.pack.st_path()
        self(f'execute store result storage cen:{self.pack.default_namespace} {p} {type} {scale} run {command}')
        return StorageValue(f'cen:{self.pack.default_namespace}', p, type)

    def storage_value(self, value: str) -> StorageValue:
        """Store a value in storage and return its reference"""
        p = self.pack.st_path()
        self(f'data modify storage cen:{self.pack.default_namespace} {p} set value {value}')
        return StorageValue(f'cen:{self.pack.default_namespace}', p, type)


class Pack:

    def __init__(self, pack_dir: str, default_namespace: str = 'minecraft', description: str = ''):
        self.pack_dir = Path(pack_dir)
        self.default_namespace = default_namespace

        self.pack_dir.mkdir(parents=True, exist_ok=True)
        self._data_dir = self.pack_dir / 'data'
        self._data_dir.mkdir(exist_ok=True)
        self._open_tags = {}
        self._ex_c = 1 # execute counter
        self._st_c = -1 # storage variable counter
        with (self.pack_dir / 'pack.mcmeta').open('w') as meta:
            json.dump({
                'pack': {
                    'pack_format': 7,
                    'description': description,
                },
            }, meta)

        @self.func(name = 'cenerator:scoreboard', tags = ['minecraft:load'])
        def _scoreboard(c):
            c('scoreboard objectives add _cen dummy')

    def parse_identifier(self, s: str) -> Identifier:
        return Identifier(s, self.default_namespace)

    def func(self, name: Optional[str] = None, tags: List[str] = []) -> Callable[[Callable[[C], None]], Callable[[], str]]:
        def inner(f: Callable[[C], None]) -> Callable[[], str]:
            identifier = self.parse_identifier(name or f.__name__)
            def call() -> str:
                return f'function {identifier}'

            
            file_path = self._data_dir / self.parse_identifier(f"{identifier.namespace}:{'functions/' + identifier.name}").data_path('.mcfunction')
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open('w') as file:
                f(C(self, lambda c: file.write(f'{c}\n')))

            for tag in tags:
                t = self.parse_identifier(tag)
                t.name = 'functions/' + t.name
                self.add_to_tag(t, str(identifier))

            return call
        
        return inner
    
    def add_to_tag(self, tag: Identifier, item: str) -> None:
        tag.name = f'tags/{tag.name}'
        values = self._open_tags[str(tag)] if str(tag) in self._open_tags else []
        file_path = self._data_dir / tag.data_path('.json')
        file_path.parent.mkdir(parents=True, exist_ok=True)
        values.append(item)
        self._open_tags[str(tag)] = values
        with file_path.open('w') as f:
            json.dump({ 'values': values }, f)
    
    def st_path(self) -> str:
        """Return a unique generated storage path"""
        self._st_c += 1
        return f'_gen_{self._st_c}'

    def include_all(self, directory: str) -> None:
        """Copy files from the specified directory into the datapack"""
        shutil.copytree(directory, self.pack_dir, dirs_exist_ok=True)
