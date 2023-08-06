# neocrym-sphinx-theme

This is a modified version of the [Furo theme](https://github.com/pradyunsg/furo) for internal use at [Neocrym](https://www.neocrym.com).

## Differences from Furo

### Absolute URLs for logos and favicons

The `light_logo` and `dark_logo` keys in the `html_theme_options` variable are ABSOLUTE URLs. Do not use relative URLs.

For example, this is an example `conf.py` that sets a light and dark logo:
```python
html_theme_options = dict(
    light_logo="https://static.neocrym.com/images/scalarstop/v1/1x/scalarstop-wordmark-color-black-on-transparent--1x.png",
    dark_logo="https://static.neocrym.com/images/scalarstop/v1/1x/scalarstop-wordmark-color-white-on-transparent--1x.png",
    sidebar_hide_name=True,
)
```

The `html_favicon` variable also now only accepts absolute URLs.