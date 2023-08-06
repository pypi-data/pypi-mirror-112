#!/usr/bin/env python3
# Yonghang Wang

import sys
import argparse
import os
import re
import json
import traceback


def sting_main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "-X", "--debug", dest="debug", action="store_true", default=False, help="debug mode",)
    args = parser.parse_args()
    print("placeholder")


if __name__ == "__main__":
    sting_main()
