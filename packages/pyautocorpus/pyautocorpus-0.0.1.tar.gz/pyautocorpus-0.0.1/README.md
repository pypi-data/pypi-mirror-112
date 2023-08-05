# PyAutoCorpus

A python interface to the excellent [AutoCorpus](https://github.com/mpacula/AutoCorpus) library.

Right now, it only supports the wiki markup `textify` function, which strips out
markup. From my benchmarks, this ends up being \~40x faster than methods to strip
markup using other libraries:

```bash
mwparserfromhell 0.208 sec/doc
wikitextparser 0.215 sec/doc
pyautocorpus 0.005 sec/doc
```

where:
 - `mwparserfromhell` is `mwparserfromhell.parse(x).strip_code()`
 - `wikitextparser` is `wikitextparser.parse(x).plain_text()`
 - `pyautocorpus` is `pyautocorpus.textify(x)`

## Installing

### From pypi:

Coming soon

### From source:

You will first need the `pcre` library installed.

```bash
python setup.py install
```

## Usage

Example:

```python
import pyautocorpus
pyautocorpus.textify("==Wiki Marked up text==\n [[Some Page|link text]] example.")
'Wiki Marked up text\n\n\n link text example.'
```

## Known issues

 - Windows is not yet supported

## Credits

[AutoCorpus](https://github.com/mpacula/AutoCorpus)

Contributors to this repository:

 - Sean MacAvaney (University of Glasgow)
 - Thomas Jänich (University of Glasgow)
