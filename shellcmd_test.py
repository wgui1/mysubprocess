#!/usr/bin/env python
import sys
import os
import time
import click
import logging

logging.basicConfig(encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.info
log = print

@click.command()
@click.option('-c', '--count', default=1, type=int,
              help='count of print a log and a sleep')
@click.option('-s', '--sleep', default=1, type=float,
              help='sleep time in one interation')
@click.option('-l', '--last-sleep', default=0, type=float,
              help='last sleep time')
def main(count, sleep, last_sleep):
    for i in range(count):
        log(f"{i} line")
        sys.stdout.flush()
        time.sleep(sleep)
    if last_sleep:
        log("last line")
        sys.stdout.flush()
        time.sleep(last_sleep)


if __name__ == '__main__':
    main()