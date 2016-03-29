# -*- mode: python -*-

"""Waf build file"""

import os
import platform

# Avoid having unnecessary public attributes in this file, else they will be
# picked up as Waf commands.

# Waf constants
APPNAME = '2dplay-tanks-unified-remote'
VERSION = '0.1'
top = '.'
out = 'build'

def configure(ctx):
    try:
        _prefix = {
            'Windows': os.environ.get('ProgramData', r'C:\ProgramData'),
            'Darwin': os.path.expanduser('~/Library/Application Support')
        }[platform.system()]
    except KeyError as exc:
        ctx.fatal("Operating system {} not supported".format(exc.args[0]))
    else:
        ctx.env.PREFIX = os.path.join(
            _prefix, 'Unified Remote', 'Remotes', 'Bundled', 'Examples')
        ctx.msg('Setting install prefix to', ctx.env.PREFIX)

def build(ctx):
    # See here for installation prefixes:
    # https://www.unifiedremote.com/tutorials/how-to-create-a-custom-keyboard-shortcuts-remote
    ctx.install_files(ctx.env.PREFIX, ctx.path.ant_glob('TanksGame/*'))
