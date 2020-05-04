# autohighlight

![Python package](https://github.com/zoonfafer/autohighlight/workflows/Python%20package/badge.svg)


## Introduction

(copied and adapted from https://code.google.com/archive/p/autohighlight/)

Of course, converting a context-free grammar to a regular grammar is not
possible in the general case; however, practical languages are highly regular
(otherwise regex-based syntax highlighting systems like Vim and Emacs wouldn't
work at all!)

Autohighlight generates vim and emacs syntax highlighting from a BNF grammar
and a description of which terms should be highlighted which colors.

This project originated from a student collaboration between Scotty Allen and
Scott Williams at the University of Colorado in 2006.

## Overview

To use autohighlighter, first you must generate an autohighlighter file.
This file specifies not only the specifics of the language you wish to color,
but how you would like that language to be colored.

## Syntax

There are three main sections to the autohighlighter file: the _gla_ section,
which contains regular expressions for terminal symbols, the _concrete syntax
tree_ section, which contains the BNF grammar for the language, and the
_coloring_ section, which provides definitions of custom colors, and dictates
which portions of the language will be colored which color.

The _gla_ section should consist of lines of the following format:

```autohighlight
  identifier: $regularexpression .
```

The _BNF grammar_ section should consist of lines of the following format:

```autohighlight
  symbol: symbol 'literal' symbol .
```

where the right hand side may be any combination of symbols and literals, with
literals enclosed in single quotes.

The _coloring_ section should consist of color definitions, and color
mappings.  Color definitions are of the form:

```autohighlight
  colorname {
      color: red;
      background: blue;
      text-decoration: underline;
  }
```

The complete list of attributes, with possible values are:

```autohighlight
  font-family: <fontname>
```

```autohighlight
  font-style: normal, italic
```

```autohighlight
  font-weight: bold, normal
```

```autohighlight
  font-size: <points>
```

```autohighlight
  text-decoration: underline, overline, line-through, inverse
```

```autohighlight
  color: Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, Brown, DarkYellow, LightGray, LightGrey, Gray, Grey, DarkGray, DarkGrey, Blue, LightBlue, Green, LightGreen, Cyan, LightCyan, Red, LightRed, Magenta, LightMagenta, Yellow, LightYellow, White
```

```autohighlight
  background-color: Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, Brown, DarkYellow, LightGray, LightGrey, Gray, Grey, DarkGray, DarkGrey, Blue, LightBlue, Green, LightGreen, Cyan, LightCyan, Red, LightRed, Magenta, LightMagenta, Yellow, LightYellow, White
```

Color mappings are of the form:

```
  colorname: symbol 'literal' symbol .
```


## Usage

Once the autohighlighter file has been generated, it should be given a `.ah`
file suffix.  Then, the compiler should be run.  The full command line syntax
is as follows:

```
  Usage: python ah.py [OPTION]... [FILE]
  Generates the specified syntax highlighting files from the given input FILE.

  Options:
    -h, --help  Prints this help
        --vim   Generates a vim syntax highlighting file
        --emacs Generates an emacs font locking file
        --error-checking Highlight all symbols not currently being colored as errors (currently works for vim only)
```

This will yield _filename_.vim and _filename_.el files for Vim and Emacs
respectively, named with respect to the input file.

## Installing the Vim syntax file

To install the generated Vim syntax file, place it in the `.vim/syntax`
directory in your home directory.  To activate it, run `:set filetype=filename`
in Vim, where _filename_ is the filename without the `.vim` ending.

## Credits

* Scotty Allen and Scott Williams for the [original code](https://code.google.com/p/autohighlight)
* [josephwecker](https://github.com/josephwecker) for the [GitHub fork](https://github.com/josephwecker/autohighlight)

## License

GNU Lesser General Public License 3.0 (See [`COPYING`](./COPYING) and
[`COPYING.LESSER`](./COPYING.LESSER))
