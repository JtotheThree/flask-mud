from markdown import markdown
from flask import Markup

def markdown_filter(text):
    return Markup(markdown(text))