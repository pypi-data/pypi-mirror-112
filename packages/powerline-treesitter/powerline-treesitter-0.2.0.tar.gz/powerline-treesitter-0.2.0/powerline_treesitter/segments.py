# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

try:
    import vim
except ImportError:
    vim = object()

from powerline.theme import requires_segment_info

@requires_segment_info
def treesitter(pl, segment_info):
    '''Return treesitter status for the current position.
    Highlight groups used: ``treesitter_identifier`` or ``file_name``.
    '''
    if vim.current.window.number != segment_info['window'].number:
        return None

    winwidth = vim.eval('nvim_win_get_width(0)')
    treesitter_status = vim.eval('nvim_treesitter#statusline(' +
                                 winwidth + ')')
    pl.debug('Current nvim_treesitter#statusline(): %s.' % treesitter_status)

    if treesitter_status is None or not treesitter_status:
        return None
    else:
        return [{
            'contents': treesitter_status,
            'highlight_groups': ['treesitter_status', 'file_name']
        }]
