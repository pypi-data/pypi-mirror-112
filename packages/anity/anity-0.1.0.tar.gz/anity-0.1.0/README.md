# Anity CLI
[anity.io](https://anity.io) enables developers to monitor their APIs using system tests written in
Python rather than traditional ‘ping’ tests.

This CLI is used to deploy and invoke test suites for your monitors.

## Installation
```bash
  pip install anity
```

## Usage

### Deploy Test Suite
To deploy your test suite you'll first need to create a new monitor at
[anity.io](https://anity.io), where you'll be given an API key for the monitor.

Package up your test suite with `zip`. Anity runs test using a
custom implementation of `unittest discover` so anything that works with
`unittest` will work in Anity.
```bash
  zip -r mysuite.zip mysuite/
```

Then deploy your test suite to your monitor with
```bash
  anity update PATH API_KEY
```

For example
```bash
  anity update mysuite.zip 2a91-85ba-4ceb
```

## Help
If you have any problems getting setup please contact us at [info@anity.io](mailto:info@anity.io)
and we'll respond as soon as possible.
