from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from .config import load_config
from .constants import PROFILES
from .scan_repo import run_scan
from .compare import compare_outputs
app=typer.Typer(help="RealWorldBuilder local evidence-first readiness scanner.")
console=Console()

def _inside(child: Path, parent: Path) -> bool:
    try: child.resolve().relative_to(parent.resolve()); return True
    except ValueError: return False

@app.command()
def scan(target_repo: Path, output: Path|None=None, ci: bool=False, fail_on_critical: bool=False, profile: str="rag-agent", privacy: str="internal", include_hidden: bool=False, max_file_size_kb: int|None=None, max_files: int|None=None):
    if not target_repo.exists() or not target_repo.is_dir(): raise typer.Exit(2)
    if profile not in PROFILES or privacy not in {"public","internal"}: raise typer.BadParameter("invalid profile or privacy")
    cfg=load_config(target_repo); cfg.profile=profile; cfg.privacy=privacy; cfg.include_hidden=include_hidden or cfg.include_hidden
    if max_file_size_kb: cfg.max_file_size_kb=max_file_size_kb
    if max_files: cfg.max_files=max_files
    out=output or Path.cwd()/cfg.output_dir/target_repo.name
    if _inside(out, target_repo):
        console.print("Output path cannot be inside the read-only target repository."); raise typer.Exit(3)
    try:
        context, critical=run_scan(target_repo,out,cfg)
    except Exception as exc:
        console.print(f"Scanner failed: {exc}"); raise typer.Exit(5)
    console.print(f"Reports written to {out}")
    if ci and fail_on_critical and critical: raise typer.Exit(1)
    raise typer.Exit(0)

@app.command("compare")
def compare_cmd(before: Path=typer.Option(...), after: Path=typer.Option(...), output: Path|None=None):
    compare_outputs(before, after, output or after)
    console.print(f"Readiness delta written to {output or after}")

if __name__ == "__main__": app()
