"""Command-line entry point for the ipdma package.

The ``ipdma`` console script declared in ``pyproject.toml`` resolves to the
:func:`cli` callable below. The package is currently an API-first scaffold, so
the CLI intentionally exposes only version reporting; it exists so that
``pip install`` ships a console command that runs instead of failing to
import a missing module.
"""

from __future__ import annotations

import sys

from ipdma import __version__


def cli(argv: list[str] | None = None) -> int:
    """Minimal CLI: print the installed ipdma version.

    Parameters
    ----------
    argv:
        Argument list (defaults to ``sys.argv[1:]``).

    Returns
    -------
    int
        Process exit code.
    """
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in {"-h", "--help"}:
        print("usage: ipdma [--version]")
        return 0
    print(f"ipdma {__version__}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(cli())
