import enum
import json
import os

from . import helpers


__all__ = ('Level', 'Client', 'load', 'loads', 'loadf', 'loadd')


_nil = type('nil', (), {'__slots__': (), '__repr__': lambda s: 'nil'})()


class Level(enum.IntEnum):

    show = 0
    done = 1
    fail = 2


class Client:

    __slots__ = ('_root', '_path', '_active', '_default', '_fallback')

    def __init__(self, root, path, default = '?', fallback = helpers.noop):

        self._root = root

        self._path = path

        self._default = default
        self._fallback = fallback

        if path[-1] is None:
            return

        for key in self._path:
            root = root[key]

        self._active = root

    def bind(self, *, theme = _nil, language = _nil, context = _nil):

        binders = (theme, language, context)

        path = list(self._path)

        for (index, value) in enumerate(binders):
            if value is _nil:
                continue
            path[index] = value

        return self.__class__(self._root, path, self._default, self._fallback)

    def __call__(self, name, *args, level = Level.show):

        level = Level(level)

        try:
            levels = self._active[level.name]
        except KeyError:
            self._fallback(level, name, args)
            return

        template = levels[name]

        if template is None:
            return self._default

        value = template.format(*args)

        return value


def load(main, core,
         *args,
         theme = None, language = None, context = None,
         **kwargs):

    root = {None: {None: main}, **core}

    path = (theme, language, context)

    return Client(root, path, *args, **kwargs)


def loads(main, core, *args, **kwargs):

    main_root = json.loads(main)

    core_root = json.loads(core)

    return load(main_root, core_root, *args, **kwargs)


def loadf(main, core, *args, **kwargs):

    with open(main, mode = 'r') as file:
        main_root = json.load(file)

    with open(core, mode = 'r') as file:
        core_root = json.load(file)

    return load(main_root, core_root, *args, **kwargs)


def loadd(directory, main = 'main.json', core = 'core.json', *args, **kwargs):

    main_path = os.path.join(directory, main)

    core_path = os.path.join(directory, core)

    return loadf(main_path, core_path, *args, **kwargs)
