import sys
import os
from pgzero.runner import prepare_mod, run_mod, set_my_root


mod = sys.modules['__main__']
if not getattr(sys, '_pgzrun', None):
    if not getattr(mod, '__file__', None):
        raise ImportError(
            "You are running from an interactive interpreter.\n"
            "'import pgzrun' only works when you are running a Python file."
        )
    prepare_mod(mod)


def go():
    """Run the __main__ module as a Pygame Zero script."""
    mymod = sys.modules['__main__']
    set_my_root(getattr(mymod, 'PATH', ''))
    if getattr(sys, '_pgzrun', None):
        return

    run_mod(mod)
