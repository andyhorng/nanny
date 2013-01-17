# coding: utf-8

import argparse
import os
from scaffolding import Templater
from scaffolding import Generator
from scaffolding import TEMPLATES

def templater_command_handler(args):
    templater = Templater(template=args.template)
    templater.build_template()

def generator_command_handler(args):
    generator = Generator(template=args.template, verbose=args.verbose)
    generator.generate()

def list_command_handler(args):
    templates = os.listdir(TEMPLATES)
    for template in templates:
        print template

def main():
    parser = argparse.ArgumentParser(description='nanny')

    subparsers = parser.add_subparsers(help='subcommand help')

    templater_parser = subparsers.add_parser('create')
    templater_parser.add_argument("template")
    templater_parser.set_defaults(handler=templater_command_handler)

    generator_parser = subparsers.add_parser('generate')
    generator_parser.add_argument("template")
    generator_parser.add_argument("--verbose", default=False, action="store_true")
    generator_parser.set_defaults(handler=generator_command_handler)

    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(handler=list_command_handler)

    args = parser.parse_args()
    args.handler(args)

if __name__ == '__main__':
    main()
