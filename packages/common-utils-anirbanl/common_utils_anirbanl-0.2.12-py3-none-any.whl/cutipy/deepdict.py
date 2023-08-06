class deepdict:
    def __init__(self, _dictlike=None, **items):
        self.Storage = dict()

        if isinstance(_dictlike, deepdict):
            for path, value in _dictlike.Leaves():
                self[path] = value
        elif _dictlike is not None:
            for key, value in dict(_dictlike).items():
                self[key] = value
        for key, value in items.items():
            self[key] = value

    def __str__(self):
        return "deepdict{%s}" % ", ".join(f"{path}: {value}" for path, value in self.Leaves())
    def __repr__(self):
        return "deepdict({%s})" % ", ".join(f"'{path}': {value!r}" for path, value in self.Leaves())

    def __eq__(self, other):
        if not isinstance(other, deepdict):
            return False
        if set(self.Storage) != set(other.Storage):
            return False

        for key, value in self.Storage.items():
            equality = value == other.Storage[key]

            if not isinstance(equality, bool):
                # broken __eq__ on arrays turns everything from gold into lead
                assert hasattr(equality, "dtype")
                equality = equality.all()

            if not equality:
                return False

        return True

    @classmethod
    def FromKwargs(cls, **items):
        return cls(items)

    # access a subtree, creating it if needed
    def Scope(self, *names):
        dd = self
        for name in names:
            dd = dd.Setdefault(name, deepdict)
        return dd

    # create a deepdict instance like self but including only nodes at or under
    # `paths`, or vice versa
    def Include(self, paths):
        return deepdict({path: self[path] for path in paths})
    def Exclude(self, paths):
        paths = list(paths)
        return deepdict({path: x for path, x in self.Leaves() if path not in paths})
    Narrow = Include

    # getitem/setitem allow deep indexing through forward-slash paths
    def __getitem__(self, key):
        parts = str(key).split("/")
        result = self
        for part in parts:
            try: result = result.Storage[part]
            except (KeyError, AttributeError): raise KeyError(key)
        return result
    def __setitem__(self, key, value):
        parts = str(key).split("/")
        dd = self
        for part in parts[:-1]:
            try: dd = dd.Scope(part)
            except (KeyError, AttributeError): raise KeyError(key)
        dd.Storage[parts[-1]] = value

    def __contains__(self, key):
        try: self[key]
        except KeyError: return False
        else: return True

    def Get(self, key, default):
        try: return self[key]
        except KeyError: return default

    # immediate children are exposed as attributes (leading capitals disallowed
    # to avoid clashes)
    def __getattr__(self, key):
        if key[0].isupper():
            raise AttributeError(key)
        return self[key]
    def __setattr__(self, key, value):
        if key[0].isupper():
            super().__setattr__(key, value)
        else:
            self[key] = value

    # shallow iteration
    def Keys(self):
        for key, child in self.Children():
            yield key
    def Children(self):
        yield from self.Storage.items()

    # deep iteration (path is to leaf as key is to value)
    def Paths(self):
        for path, leaf in self.Leaves():
            yield path
    def Leaves(self):
        for key, node in self.Storage.items():
            if isinstance(node, deepdict):
                for path, leaf in node.Leaves():
                    yield f"{key}/{path}", leaf
            else:
                yield key, node

    def Mapleaves(self, fn, fanout=None, splat=False):
        result = deepdict({path: fn(*leaf) if splat else fn(leaf)
                                             for path, leaf in self.Leaves()})
        return result if fanout is None else result.Unzip(rank=fanout)
    def Mapchildren(self, fn, fanout=None):
        result = deepdict({key: fn(child) for key, child in self.Children()})
        return result if fanout is None else result.Unzip(rank=fanout)
    def Unzip(self, rank):
        results = tuple(deepdict() for _ in range(rank))
        for path, xs in self.Leaves():
            assert isinstance(xs, tuple) and len(xs) == rank
            for i in range(rank):
                results[i][path] = xs[i]
        return results
    @classmethod
    def Zip(cls, *xss, mode="strict", default=None):
        assert xss
        pathss = tuple(set(xs.Paths()) for xs in xss)
        if mode == "strict":
            assert all(paths == pathss[0] for paths in pathss)
            paths = pathss[0]
        elif mode == "inner":
            paths = set.intersection(*pathss)
        elif mode == "outer":
            paths = set.union(*pathss)
        return cls({path: tuple(xs.Get(path, default) for xs in xss)
                                for path in paths})
    @classmethod
    def ZipMapl(cls, fn, *xss, mode="strict", default=None, fanout=None, splat=False):
        return cls.Zip(*xss, mode=mode, default=default).Mapleaves(fn, fanout=fanout, splat=splat)
    @classmethod
    def ZipMapc(cls, fn, *xss, mode="strict", default=None, fanout=None, splat=False):
        return cls.Zip(*xss, mode=mode, default=default).Mapchildren(fn, fanout=fanout, splat=splat)

    def Clone(self):
        return self.Mapleaves(lambda x: x)
    def AsDict(self):
        return dict(self.Leaves())
    def AsNestedDict(self):
        return {key: value.AsNestedDict() if isinstance(value, deepdict) else value
                        for key, value in self.Children()}

    def Get(self, key, default=None):
        try: return self[key]
        except KeyError: return default
    def Setdefault(self, key, factory):
        try: return self[key]
        except KeyError:
            self[key] = factory()
            return self[key]

    def IsEmpty(self):
        return not any(self.Leaves())
    def __len__(self):
        return len(tuple(self.Leaves()))

    def __getstate__(self):
        return self.Storage
    def __setstate__(self, state):
        self.Storage = state


    def _structure(self):
        return {path: (type(x), getattr(x, "shape", "<>"))
                        for path, x in sorted(self.Leaves(), key=lambda kv: kv[0])}

