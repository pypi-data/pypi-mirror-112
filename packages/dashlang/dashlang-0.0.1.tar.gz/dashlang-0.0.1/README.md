# dashlang

 [![pipeline status](https://gitlab.com/runemaster/dashlang/badges/main/pipeline.svg)](https://gitlab.com/runemaster/dashlang/-/commits/main) 
[![coverage report](https://gitlab.com/runemaster/dashlang/badges/main/coverage.svg)](https://gitlab.com/runemaster/dashlang/-/commits/main) 

An experimental markup language for creating rich dashboards using Dash and Dash components.

## Introduction

Dashlang is a project that offers developers a set of tools to easily create complex layouts
of `Dash` components, using a syntax as close as possible to regular HTML. Its most simple usage
allows developers to create layouts using the dashlang declarative markup format and convert
the markup into a Python tree of Dash components in a simple and efficient way.

### Example

Take the following snippet written in the dashlang markup format. The format tries to stay as
close to HTML as possible, by using tags delimited by the `<` and `>` characters, and using opening
and closing tags to declare elements.

```
<Div id="root-container" className="fluid-container">
  <H1 id="title" className="text-bold">This is a title</H1>
  <P>This is a simple paragraph with a very very long text</P>
</Div>
```

This snippet can be easily converted to a Python component tree just by calling a function

```
from dash import Dash
from dashlang.parsers import MarkupParser

parser = MarkupParser()

app = Dash(__name__)

with open("snippet.dml") as fp:
    app.layout = parser.parse(fp.read()).to_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
```

Running the previous Python snippet will create a Dash application instance and load its layout from
the snippet file containing the layout in markup format.
