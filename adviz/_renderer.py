"""Custom `show_doc` renderer that restores the parameters table.

nbdev3's default `BasicMarkdownRenderer` renders parameters as inline comments
in the function signature. This renderer instead shows a plain signature
(one parameter per line) followed by a `Type | Default | Details` table plus a
Returns row — the classic, readable API layout.

Docs-only. Wired in via `[tool.nbdev] renderer = "adviz._renderer.TableRenderer"`
in pyproject.toml. If a future fastcore changes `DocmentTbl`, only docs
rendering is affected (a clear error at `nbdev-docs`), never the library.
"""

import inspect

from fastcore.docments import DocmentTbl
from nbdev.doclinks import NbdevLookup
from nbdev.showdoc import BasicMarkdownRenderer

__all__ = ["TableRenderer"]


class TableRenderer(BasicMarkdownRenderer):
    "show_doc renderer: plain signature (one param per line) + a parameters/returns table."

    def _repr_markdown_(self):
        doc = "---\n\n"
        src = NbdevLookup().code(self.fn)
        if src:
            doc += (
                f'[source]({src})'
                '{target="_blank" style="float:right; font-size:smaller"}\n\n'
            )
        doc += f"{'#' * self.title_level} {self.nm}\n\n"

        dm = self.dm
        param_strs = [fmt for fmt, _ in dm.params]
        ret_str = dm._ret_str.split(" # ", 1)[0]
        prefix = "async def" if inspect.iscoroutinefunction(self.sym) else "def"
        if param_strs:
            inner = ",\n    ".join(param_strs)
            sig = f"{prefix} {self.nm}(\n    {inner}\n{ret_str}"
        else:
            sig = f"{prefix} {self.nm}({ret_str}"
        doc += f"```python\n{sig}\n```"

        if self.docs:
            doc += f"\n\n*{self.docs.strip()}*"
        doc += "\n\n" + DocmentTbl(self.sym)._repr_markdown_()
        return doc
