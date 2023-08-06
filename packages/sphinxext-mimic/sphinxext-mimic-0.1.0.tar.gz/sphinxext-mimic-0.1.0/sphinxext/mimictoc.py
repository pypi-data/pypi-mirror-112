from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx import addnodes
from docutils.nodes import Element, Node
from sphinx.directives.other import TocTree

from typing import Any, Dict, List, Set, Tuple, overload


class mimictoc(TocTree):

    # Override normal Sphinx ToC checking for warning removal
    def parse_content(self, toctree: addnodes.toctree) -> List[Node]:
        suffixes = self.config.source_suffix

        # glob target documents
        all_docnames = self.env.found_docs.copy()
        all_docnames.remove(self.env.docname)  # remove current document

        ret: List[Node] = []
        excluded = Matcher(self.config.exclude_patterns)
        for entry in self.content:
            if not entry:
                continue
            # look for explicit titles ("Some Title <document>")
            explicit = explicit_title_re.match(entry)
            if (
                toctree["glob"]
                and glob_re.match(entry)
                and not explicit
                and not url_re.match(entry)
            ):
                patname = docname_join(self.env.docname, entry)
                docnames = sorted(patfilter(all_docnames, patname))
                for docname in docnames:
                    all_docnames.remove(docname)  # don't include it again
                    toctree["entries"].append((None, docname))
                    toctree["includefiles"].append(docname)
                if not docnames:
                    ret.append(
                        self.state.document.reporter.warning(
                            "toctree glob pattern %r didn't match any documents"
                            % entry,
                            line=self.lineno,
                        )
                    )
            else:
                if explicit:
                    ref = explicit.group(2)
                    title = explicit.group(1)
                    docname = ref
                else:
                    ref = docname = entry
                    title = None
                # remove suffixes (backwards compatibility)
                for suffix in suffixes:
                    if docname.endswith(suffix):
                        docname = docname[: -len(suffix)]
                        break
                # absolutize filenames
                docname = docname_join(self.env.docname, docname)
                if url_re.match(ref) or ref == "self":
                    toctree["entries"].append((title, ref))
                elif docname not in self.env.found_docs:
                    if excluded(self.env.doc2path(docname, None)):
                        message = "toctree contains reference to excluded document %r"
                    else:
                        message = (
                            "toctree contains reference to nonexisting document %r"
                        )

                    ret.append(
                        self.state.document.reporter.warning(
                            message % docname, line=self.lineno
                        )
                    )
                    self.env.note_reread()
                else:
                    all_docnames.remove(docname)

                    toctree["entries"].append((title, docname))
                    toctree["includefiles"].append(docname)

        # entries contains all entries (self references, external links etc.)
        if "reversed" in self.options:
            toctree["entries"] = list(reversed(toctree["entries"]))
            toctree["includefiles"] = list(reversed(toctree["includefiles"]))

        return ret


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive("mimictoc", mimictoc)
