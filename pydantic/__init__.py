class _Field:
    def __init__(self, default=None, default_factory=None): self.default=default; self.default_factory=default_factory
def Field(default=None, default_factory=None): return _Field(default, default_factory)
class BaseModel:
    def __init__(self, **kw):
        anns={}
        for c in reversed(self.__class__.mro()): anns.update(getattr(c,'__annotations__',{}))
        for k in anns:
            if k in kw: v=kw[k]
            else:
                d=getattr(self.__class__, k, None)
                if isinstance(d,_Field): v=d.default_factory() if d.default_factory else d.default
                else: v=d
            setattr(self,k,v)
        for k,v in kw.items():
            if not hasattr(self,k): setattr(self,k,v)
    def model_dump(self):
        def conv(x):
            if isinstance(x, BaseModel): return x.model_dump()
            if isinstance(x, list): return [conv(i) for i in x]
            if isinstance(x, dict): return {k:conv(v) for k,v in x.items()}
            return x
        return {k:conv(v) for k,v in self.__dict__.items()}
