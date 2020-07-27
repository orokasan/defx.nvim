# ============================================================================
# FILE: type.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from defx.base.column import Base, Highlights
from defx.context import Context
from defx.util import Nvim, Candidate, len_bytes
from defx.view import View

import re
import typing


class Column(Base):

    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = 'type'
        types = [
            {
                'name': 'text', 'globs': ['*.txt', '*.md', 'README'],
                'icon': '[T]', 'highlight': 'Constant'
            },
            {
                'name': 'image', 'globs': ['*.jpg'],
                'icon': '[I]', 'highlight': 'Type'
            },
            {
                'name': 'archive', 'globs': ['*.zip'],
                'icon': '[A]', 'highlight': 'Special'
            },
            {
                'name': 'executable', 'globs': ['*.exe'],
                'icon': '[X]', 'highlight': 'Statement'
            },
        ]
        self.vars = {
            'types': types,
        }
        self.has_get_with_highlights = True

        self._length: int = 0

    def on_init(self, view: View, context: Context) -> None:
        self._length = max([self.vim.call('strwidth', x['icon'])
                            for x in self.vars['types']])

    def get_with_highlights(
        self, context: Context, candidate: Candidate
    ) -> typing.Tuple[str, Highlights]:
        for t in self.vars['types']:
            for glob in t['globs']:
                if not candidate['action__path'].match(glob):
                    continue
                return (str(t['icon']), [
                    (t['highlight'], self.start, len_bytes(t['icon']))
                ])

        return (' ' * self._length, [])

    def length(self, context: Context) -> int:
        return self._length

    def syntaxes(self) -> typing.List[str]:
        return [self.syntax_name + '_' + x['name'] for x
                in self.vars['types']]

    def highlight_commands(self) -> typing.List[str]:
        commands: typing.List[str] = []
        for t in self.vars['types']:
            commands.append(
                ('syntax match {0}_{1} /{2}/ ' +
                 'contained containedin={0}').format(
                    self.syntax_name, t['name'], re.escape(t['icon'])))
            commands.append(
                'highlight default link {}_{} {}'.format(
                    self.syntax_name, t['name'], t['highlight']))
        return commands
