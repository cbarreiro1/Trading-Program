#!/usr/bin/env python3

from subprocess import call

call(["wscat", "-c", "wss://paper-api.alpaca.markets/v2/iex"])

