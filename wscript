# -*- mode: python -*-

# Compatible with Python 3.5

"""Waf build file"""

import os
import platform
import itertools
import zipfile

# Avoid having unnecessary public attributes in this file, else they will be
# picked up as Waf commands.

# Waf constants
APPNAME = '2DPlay Tanks Unified Remote'
VERSION = '0.1'
top = '.'
out = 'build'

def configure(ctx):
    ctx.env.SYSTEM = platform.system()
    ctx.env.APPNAME = APPNAME
    ctx.env.VERSION = VERSION
    # See here for a hint to installation prefixes:
    # https://www.unifiedremote.com/tutorials/how-to-create-a-custom-keyboard-shortcuts-remote
    try:
        _prefix = {
            'Windows': os.environ.get('ProgramData', r'C:\ProgramData'),
            'Darwin': os.path.expanduser('~/Library/Application Support')
        }[ctx.env.SYSTEM]
    except KeyError as exc:
        ctx.fatal("Operating system {} not supported".format(exc.args[0]))
    else:
        ctx.env.PREFIX = os.path.join(
            _prefix, 'Unified Remote', 'Remotes', 'Custom', 'TanksGame')
        ctx.msg('Setting install prefix to', ctx.env.PREFIX)

    if ctx.env.SYSTEM == 'Darwin':
        # For packaging
        ctx.env.ORG_ID = 'com.seanfisk'
        ctx.env.PKG_ID = ctx.env.ORG_ID + '.pkg.TanksGameUnifiedRemote'
        ctx.find_program('pkgbuild')
        ctx.find_program('productbuild')
        ctx.find_program('pandoc')
        ctx.find_program('dmgbuild')

def build(ctx):
    remote_nodes = ctx.path.ant_glob('TanksGame/*')

    # Build README
    readme_md_node = ctx.path.find_resource('README.md')
    css_node = ctx.path.find_resource(['css', 'modest', 'css', 'modest.css'])
    readme_html_node = readme_md_node.change_ext('.html')

    @ctx.rule(target=readme_html_node,
              source=[readme_md_node, css_node],
              vars=['PANDOC'])
    def _convert_readme(tsk):
        return tsk.exec_command(tsk.env.PANDOC + [
            '--from', 'markdown_github',
            '--to', 'html5',
            '--css', tsk.inputs[1].abspath(),
            '--self-contained',
            tsk.inputs[0].abspath(),
            '--output', tsk.outputs[0].abspath(),
        ], cwd=ctx.srcnode.abspath())

    # Build archive
    @ctx.rule(source=[readme_html_node] + remote_nodes,
              target='TanksGame-{}.zip'.format(ctx.env.VERSION))
    def _make_archive(tsk):
        readme_node = tsk.inputs[0]
        with zipfile.ZipFile(
                tsk.outputs[0].abspath(), 'w',
                compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(readme_node.abspath(),
                          arcname=os.path.join('TanksGame', readme_node.name))
            for node in tsk.inputs[1:]:
                archive.write(node.abspath(), node.relpath())

    if ctx.env.SYSTEM == 'Darwin':
        root_node = ctx.path.find_or_declare('root')
        root_node.mkdir()
        dest_dir = root_node.find_or_declare(os.path.relpath(
            ctx.env.PREFIX,
            os.path.commonprefix([os.path.expanduser('~'), ctx.env.PREFIX])))
        dest_dir.mkdir()

        dest_nodes = []
        for node in remote_nodes:
            dest_node = dest_dir.find_or_declare(node.name)
            ctx(features='subst', source=node, target=dest_node, is_copy=True)
            dest_nodes.append(dest_node)

        pkg_dir = ctx.path.find_dir(['pkg', 'osx'])
        pkg_dir.mkdir()
        # Put the flat package in its own directory so that the mpkg is not
        # picked up on successive builds.
        flat_pkg_node = pkg_dir.find_or_declare(['flat', 'flat.pkg'])
        @ctx.rule(source=dest_nodes, target=flat_pkg_node, vars=[
            'VERSION', 'PKGBUILD', 'PKG_ID'])
        def _make_flat_pkg(tsk):
            return tsk.exec_command(tsk.env.PKGBUILD + [
                '--root', root_node.abspath(),
                '--identifier', tsk.env.PKG_ID,
                '--version', tsk.env.VERSION,
                '--ownership', 'recommended',
                tsk.outputs[0].abspath(),
            ])

        xml_in_node = pkg_dir.find_resource('distribution.xml.in')
        xml_node = xml_in_node.change_ext('')
        ctx(features='subst',
            source=xml_in_node,
            target=xml_node,
            PKG_BASENAME=flat_pkg_node.name,
        )

        mpkg_node = pkg_dir.find_or_declare('Install {}.mpkg'.format(APPNAME))

        @ctx.rule(source=[xml_node, flat_pkg_node], target=mpkg_node, vars=[
            # This rule depends on PREFIX because we use the parent path of the
            # flat package.
            'VERSION', 'PRODUCTBUILD', 'PREFIX'])
        def _make_mpkg(tsk):
            return tsk.exec_command(tsk.env.PRODUCTBUILD + [
                '--distribution', tsk.inputs[0].abspath(),
                '--package-path', tsk.inputs[1].parent.abspath(),
                '--version', tsk.env.VERSION,
                tsk.outputs[0].abspath(),
            ])

        dmg_node = pkg_dir.find_or_declare(ctx.env.APPNAME + '.dmg')
        dmgbuild_settings_node = pkg_dir.find_resource('dmgbuild-settings.py')

        @ctx.rule(target=dmg_node,
                  source=[dmgbuild_settings_node, readme_html_node, mpkg_node],
                  vars=['DMGBUILD', 'APPNAME'])
        def _make_dmg(tsk):
            dmg_path = tsk.outputs[0].abspath()
            settings_path, readme_path, mpkg_path = (
                node.abspath() for node in tsk.inputs)
            return tsk.exec_command(tsk.env.DMGBUILD + [
                tsk.env.APPNAME, '--settings', settings_path, '--no-hidpi'
            ] + list(itertools.chain.from_iterable(
                ['-D', '{}={}'.format(key, val)]
                for key, val in dict(pkg=mpkg_path, readme=readme_path).items()
            )) + [dmg_path])

    # Installation via Waf
    ctx.install_files(ctx.env.PREFIX, remote_nodes)
