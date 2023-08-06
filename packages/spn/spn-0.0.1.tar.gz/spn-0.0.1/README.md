# spn

A simple CLI for the Wayback Machine's Save Page Now (SPN) API

## install
```bash
pip install spn
```

## usage
```
Usage: spn [OPTIONS] [URLS]...

Options:
  --access-key TEXT              [required]
  --secret-key TEXT              [required]
  --verify
  --capture-all
  --capture-outlinks
  --capture-screenshot
  --delay-wb-availability
  --force-get
  --skip-first-archive
  --if-not-archived-within TEXT
  --outlinks-availability
  --email-result
  --js-behavior-timeout INTEGER
  --capture-cookie TEXT
  --target-username TEXT
  --target-password TEXT
  --help                         Show this message and exit.
```

## example
```bash
export SPN_ACCESS_KEY=YOUR_ACCESS_KEY
export SPN_SECRET_KEY=YOUR_SECRET_KEY

spn https://some.site/ https://some.site/some/page/
```
