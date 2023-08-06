from __future__ import division
from docutils import nodes
from docutils.parsers.rst import Directive
from conf import html_template_url


class iframe(nodes.General, nodes.Element): pass


def skip_visit(self, node):
    # Function to skip the processing of the entire directive
    pass


def visit_iframe_node(self, node):
    element = """<iframe class="reauthoring" scrolling="no" frameBorder="0" id="%s" src="%s" width="100%%"
                  height="250px" marginheight="0"></iframe>"""

    # html_template_url for template path. Create variable html_template_url in conf.py and assign path to it.

    node["args"].append(html_template_url + node["args"][0])

    # Get the frame ID as first argument and the URL as second argument

    self.body.append(element % (node["args"][0], node["args"][1]))


def depart_iframe_node(self, node):
    pass


class Iframe(Directive):
    """
    Directive to insert an iframe with an id and a URL. URL is generated from id, meaning that the h5p folder name has to match with the id. The syntax
    is:

    .. iframe:: id

    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        return [iframe(args = self.arguments)]


def setup(app):
    app.add_node(iframe,
                 html = (visit_iframe_node,
                         depart_iframe_node),
                 latex = (skip_visit, skip_visit),
                 text = (skip_visit, skip_visit),
                 man = (skip_visit, skip_visit),
                 texinfo = (skip_visit, skip_visit))

    # Declaring the directive
    app.add_directive("iframe", Iframe)
