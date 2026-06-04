import sys, io, contextlib
class Exit(Exception):
    def __init__(self, code=0): self.exit_code=code
class BadParameter(Exception): pass
def Option(default=..., *args, **kwargs): return default
class Typer:
    def __init__(self, help=None): self.commands={}
    def command(self, name=None):
        def deco(fn): self.commands[name or fn.__name__.replace('_','-')]=fn; return fn
        return deco
    def __call__(self, args=None):
        interactive = args is None
        args=list(sys.argv[1:] if args is None else args)
        if not args: return 0
        cmd=args.pop(0); fn=self.commands.get(cmd)
        if not fn: raise Exit(2)
        try:
            if cmd=='scan':
                target=args.pop(0) if args else None; kwargs={}; flags={'--ci':'ci','--fail-on-critical':'fail_on_critical','--include-hidden':'include_hidden'}
                i=0
                while i < len(args):
                    a=args[i]
                    if a in flags: kwargs[flags[a]]=True; i+=1
                    elif a in ['--output','--profile','--privacy','--max-file-size-kb','--max-files']:
                        key=a[2:].replace('-','_'); val=args[i+1]; i+=2
                        if key in ['max_file_size_kb','max_files']: val=int(val)
                        kwargs[key]=val
                    else: i+=1
                from pathlib import Path
                if 'output' in kwargs: kwargs['output']=Path(kwargs['output'])
                return fn(Path(target), **kwargs)
            if cmd=='compare':
                kwargs={}; i=0
                from pathlib import Path
                while i < len(args):
                    key=args[i][2:].replace('-','_'); val=args[i+1]; i+=2; kwargs[key]=Path(val)
                return fn(**kwargs)
        except Exit as e:
            if interactive: sys.exit(e.exit_code)
            raise
        except BadParameter: raise Exit(2)
class Result:
    def __init__(self, exit_code, output): self.exit_code=exit_code; self.output=output; self.exception=None
class CliRunner:
    def invoke(self, app, args):
        buf=io.StringIO(); code=0
        with contextlib.redirect_stdout(buf):
            try: app(args)
            except Exit as e: code=e.exit_code
            except SystemExit as e: code=e.code or 0
            except Exception as e: code=1; print(e)
        return Result(code, buf.getvalue())
