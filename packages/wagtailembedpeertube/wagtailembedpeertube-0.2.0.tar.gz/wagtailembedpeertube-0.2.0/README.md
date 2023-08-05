# wagtailembedpeertube

Embed PeerTube videos into Wagtail.

## Introduction

Wagtail has a great [support of oEmbed][1] for embedding content. Unfortunately,
the oEmbed mechanism is based on services domain names and URI; and this is prone
to centralization since it limits to a short list of selected providers.

By the way, there is already hundreds instances and it will probably grow with
years - see [PeerTube instances](https://instances.joinpeertube.org).

This app brings oEmbed support for decentralized PeerTube instances. To do this,
it only focuses on a string URI filtering, allowing all services from any domain
name.

## Installation

1. Install using ``pip``:

   ```shell
   pip install wagtailembedpeertube
   ```

2. Add ``wagtailembedpeertube`` to your ``INSTALLED_APPS`` setting somewhere
   after ``wagtail.embeds``:

   ```python
   INSTALLED_APPS = [
       ...
       "wagtail.embeds",
       ...
       "wagtailembedpeertube",
       ...
   ]
   ```

3. Configure embed finders in ``WAGTAILEMBEDS_FINDERS`` setting to add PeerTube's
   one at the end, i.e.:

   ```python
   WAGTAILEMBEDS_FINDERS = [
       {
           "class": "wagtail.embeds.finders.oembed",
       },
       {
           "class": "wagtailembedpeertube.finders",
       },
   ]
   ```

   Since the first matching finder will be used, ``wagtailembedpeertube`` should
   be declared as last because others finders are matching domain names and may
   be more precise. See [Configuring embed “finders”][2] for more details.

## Usage

That's it! You should now be able to embed any PeerTube content using the
``EmbedBlock``:

```python
from wagtail.embeds.blocks import EmbedBlock

class MyStreamField(blocks.StreamBlock):
    ...

    embed = EmbedBlock()
```

## Development

To setup a development environment, clone this repository and follow the
installation steps but replace the installation from PyPi by:

```shell
pip install -e .[test]
```

The Python code is formatted and linted thanks to flake8, isort and black. To
ease the use of this tools, the following commands are available:
- `make lint`: check the Python code syntax and imports order
- `make format`: fix the Python code syntax and imports order

## License

This extension is mainly developed by [Cliss XXI](https://www.cliss21.com) and
licensed under the [AGPLv3+](LICENSE). Any contribution is welcome!

[1]: http://docs.wagtail.io/en/stable/advanced_topics/embeds.html
[2]: http://docs.wagtail.io/en/stable/advanced_topics/embeds.html#configuring-embed-finders
