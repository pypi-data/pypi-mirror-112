"""
    Copyright 2015-2021 Stephane De Mita, Mathieu Siol

    This file is part of EggLib.

    EggLib is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EggLib is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with EggLib.  If not, see <http://www.gnu.org/licenses/>.
"""

from .. import eggwrapper as _eggwrapper
from .. import _interface

def _align_has_non_single_digit_data(align):
    for item in align:
        for x in item.sequence:
            if x < 0 or x > 1: return True
    else:
        return False

def to_ms(data, fname=None, positions=None, spacer=None, recode=False):
    """
    Export data in the format used by the ms program (Hudson 2002
    *Bioinformatics* **18**: 337-338). The original format is designed
    for binary (0/1) allelic values. This implementation will export any
    allelic values that are present in the provided alignment (but
    always as integers; if sequence data is included, they will be
    represented by their corresponding integer values). In addition, it
    is possible to insert spaces between all loci to accomodate allelic
    values exceeding the range [0,9] (outside this range, it is not
    possible anymore to discriminate loci using the standard format).
    See the *spacer* option.

    :param data: Alignment(s) to export, either as a :class:`.Align`
        instance or as an iterable of :class:`.Align` instances. In the
        latter case, all instances are exported consecutively.

    :param fname: Name of the file to export data to. By default, the
        file is created (or overwritten if it already exists). If the
        option *append* is ``True``, data is appended at the end of the
        file (and it must exist). If *fname* is ``None`` (default), no
        file is created and the formatted data is returned as a
        :class:`str`. In the alternative case, nothing is returned.

    :param positions: The list of site positions, with length matching
        the alignment length. Positions are required to be in the [0,1]
        range but the order is not checked. By default (if the argument
        value is ``None``, sites are supposed to be evenly spread over
        the [0,1] interval. The value for this argument should match
        exactly the value for the argument *data*: if *data* is a single
        :class:`.Align`, *positions* should be a single list of
        positions and if *data* is a list of :class:`.Align` instances
        (even if the length of this list is one), then *positions*
        should be a list (of lists of positions) of the same length. If
        a list is provided, any of its items (supposed to represent a
        list of positions) can be replaced by ``None``.

    :param spacer: Define if a space must be inserted between each
        allelic value. If ``None``, the space is inserted only if at
        least one allele at any locus is outside the range [0,9]. If
        ``True``, the space is always inserted. If ``False``, the space
        is not inserted. The automatic detection of out-of-range allelic
        values comes with the cost of increased running time.

    :param recode: If ``True``, all allelic values are recoded such as
        the first encountered values is 0, the second is 1, and so on.
        The original alignments are left unmodified.

    The format is as follows:

    * One line with two slashes.
    * One line with the number of sites
    * One line with the positions, or an empty line if the number of
        sites is zero.
    * The matrix of genotypes (one line per sample), only if the number
        of sites is larger than zero.
    """

    export = _eggwrapper.Export()

    if fname != None:
        if export.open_file(fname) == False:
            raise ValueError('cannot open {0}'.format(fname))
    else:
        export.to_str()

    if isinstance(data, _interface.Align):
        data = [data]
        positions = [positions]

    if positions is None:
        positions = [None] * len(data)
    else:
        if len(data) != len(positions):
            raise ValueError('the length of the values for arguments `data` and `positions` are required to match')

    if recode:
        align = _eggwrapper.DataHolder(True)

    for item, pos in zip(data, positions):
        if not isinstance(item, _interface.Align):
            raise TypeError('expect an Align')
        n = item.ls
        if pos is None:
            export.ms_auto_positions(n)
        else:
            if len(pos) != n:
                raise ValueError('invalid number of positions (must be equal to the number of sites)')
            export.ms_num_positions(n)
            [export.ms_position(i, p) for (i,p) in enumerate(pos)]

        if spacer is None:
            spacer_this_one = _align_has_non_single_digit_data(item)
        else:
            spacer_this_one = spacer

        if recode:
            align.set_nsit(n)
            align.set_nsam_i(item._ns)
            for i in range(n):
                alleles = []
                for j in range(item._ns):
                    a = item._obj.get_sample(j, i)
                    if a not in alleles: alleles.append(a)
                    align.set_sample(j, i, alleles.index(a))
            export.ms(align, spacer_this_one)
        else:
            export.ms(item._obj, spacer_this_one)

    if fname is None: return export.get_str()
