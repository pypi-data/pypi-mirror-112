cctrlw
=========

Configurable Ctrl-W (see gifs to understand what that means).

# TODO: gifs

This project addresses the pitfalls of `xonsh <https://xon.sh/>`_ (a brilliant project btw) builtin Ctrl-W functionality.

What exactly was wrong? There was no way to configure which characters are considered equivalent (and hence, to be deleted on a Ctrl-W keystoke). Say you wanted to edit a 'cmd a/very/long/path' and press a C-W. Then everything till space is removed, which often is not the desired behaviour.

Ok, so how to configure such a thing? Mathematically such configuration is equivalent to a `partition <https://en.wikipedia.org/wiki/Partition_of_a_set>`_ of the set of all characters. In terms of implementation, `disjoint set union data structure <https://en.wikipedia.org/wiki/Disjoint-set_data_structure>`_ can be used to maintain partitions. Using a DSU is not really a requirement;  however it turns out to be the simplest and cleanest implementation.

See `docstring <https://github.com/ggdwbg/cctrlw/blob/main/cctrlw/algo.py#L148>`_ for `load_partitions` in `cctrlw/algo.py` to understand the approach used to define partitions.

Default `cw_modes.json` defines the following partitions:

   - `S`: singletons
   - `ldu`: `{{a..z}, {0..9}, {A..Z}}`
   - `ldup`: compared to ldu: elements of `{!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~}` are now equivalent
   - `Ldp`: compared to `ldup`: lower and upper letters are now merged
   - `Ap`: compared to `Ldp`: digits and letters are now merged
   - `W`: compared to `Ap`: digits and punctuation are merged

Xonsh default Ctrl-W corresponds to `W`, hence the name.

In terms of actual usage this module provides a CLI and a xontrib for use with xonsh:

   - CLI: run `python -m cctrlw.cli -h` for details.
   - Xontrib: add `xontrib load xonsh_cctrlw` to your `.xonshrc`. Then you can modify your config by setting `$CW_MODE` and `$CW_CONFIG` environment variables. Defaults are `$CW_MODE = 'Ap'` and `$CW_CONFIG = '<package location>/cw_modes.json'`.
