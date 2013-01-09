# coding: utf-8

import argparse

def templater_command_handler(args):
    from builder import Templater
    templater = Templater(template=args.template)
    templater.build_template()

def builder_command_handler(args):
    from builder import Builder
    builder = Builder(template=args.template)
    builder.build()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='eztable scaffolding generator')

    subparsers = parser.add_subparsers(help='subcommand help')

    templater_parser = subparsers.add_parser('create_template')
    templater_parser.add_argument("template")
    templater_parser.set_defaults(handler=templater_command_handler)

    builder_parser = subparsers.add_parser('build')
    builder_parser.add_argument("template")
    builder_parser.set_defaults(handler=builder_command_handler)

    args = parser.parse_args()
    args.handler(args)

