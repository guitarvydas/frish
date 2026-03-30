# Simple Forth written in a portable meta-language (frish)

Forth written in file `forthish.frish.m4`, using the meta-language `frish` (very similar to Python).

Uses a diagram to specify one routine. The diagram is `xinterpret.drawio`. 

The diagram is transmogrified to python using the dtree tool resulting in `xinterpret.frish`

`M4` is used to include `xinterpret.frish` into `forthish.frish.m4` resulting in `forthish.frish`.

`Forthish.frish` is then transmogrified into runnable python code via `frish.drawio`.

Run `frish.py` --> forth REPL on the command line.





repo: https://github.com/guitarvydas/frish

# status Mar 29, 2026
- on branch `debugdefsynonym`
- rewriting the "Pre Optimize" part
- youtube of twitch-like video of beginnings of the code rewrite https://youtu.be/05UxokdnUbI
- substack article containing a justification for discarding the code https://programmingsimplicity.substack.com/p/working-on-rewriting-the-preoptimizer?r=1egdky
