#!/usr/bin/env python
import sys
import os
import time
import click
import logging

@click.command()
@click.option('-c', '--count', default=1, type=int,
              help='count of print a log and a sleep')
@click.option('-s', '--sleep', default=1, type=float,
              help='sleep time in one interation')
@click.option('-l', '--last-sleep', default=0, type=float,
              help='last sleep time')
@click.option('-e', '--with-stderr', default=False, type=bool,
              help='whether to print to stderr')
def main(count, sleep, last_sleep, with_stderr):
    for i in range(count):
        output = sys.stderr if with_stderr and (i % 2) else sys.stdout
        print(f"{i} line", file=output)
        sys.stdout.flush()
        sys.stderr.flush()
        time.sleep(sleep)
    if last_sleep:
        print(f"last line", file=sys.stdout)
        sys.stdout.flush()
        time.sleep(last_sleep)


if __name__ == '__main__':
    main()