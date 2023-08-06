#### Code taken directly from IPython.lib.pretty ####
#
# This snippet is here for pretty printing in the ipython console
# see here https://github.com/ipython/ipython/blob/master/IPython/lib/pretty.py
# it's copied here instead of imported, because the underscore at the beginning
# of function name IPython.lib.pretty._seq_pprinter_factory implies it's just
# internal code and should not be assumed to be a stable API (even though the
# function signature hasn't changed in 4 years)
#
# BSD 3-Clause License
# 
# - Copyright (c) 2008-Present, IPython Development Team
# - Copyright (c) 2001-2007, Fernando Perez <fernando.perez@colorado.edu>
# - Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
# - Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

def _seq_pprinter_factory(start, end):
    """
    Factory that returns a pprint function useful for sequences.  Used by
    the default pprint for tuples, dicts, and lists.
    """
    def inner(obj, p, cycle):
        if cycle:
            return p.text(start + '...' + end)
        step = len(start)
        p.begin_group(step, start)
        for idx, x in p._enumerate(obj):
            if idx:
                p.text(',')
                p.breakable()
            p.pretty(x)
        if len(obj) == 1 and isinstance(obj, tuple):
            # Special case for 1-item tuples.
            p.text(',')
        p.end_group(step, end)
    return inner

def _dict_pprinter_factory(start, end):
    """
    Factory that returns a pprint function used by the default pprint of
    dicts and dict proxies.
    """
    def inner(obj, p, cycle):
        if cycle:
            return p.text('{...}')
        step = len(start)
        p.begin_group(step, start)
        keys = obj.keys()
        for idx, key in p._enumerate(keys):
            if idx:
                p.text(',')
                p.breakable()
            p.pretty(key)
            p.text(': ')
            p.pretty(obj[key])
        p.end_group(step, end)
    return inner
