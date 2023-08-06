# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import numbers as nmbr
import tempfile as temp
from pathlib import Path as path_t
from typing import Union

import xlsxwriter as xlsx

from cell_tracking_BC.type.sequence import sequence_t


def SaveCellFeaturesToXLSX(path: Union[str, path_t], sequence: sequence_t) -> None:
    """"""
    if isinstance(path, str):
        path = path_t(path)
    if path.exists():
        print(f"{path}: File (or folder) already exists...")
        path = path_t(temp.mkdtemp()) / path.name
        print(f"Using {path} instead")

    workbook = xlsx.Workbook(str(path))

    for feature in sequence.AvailableCellFeatures():
        evolutions = sequence.FeatureEvolutionsOfAllCells(feature)
        if not isinstance(evolutions[1][0], nmbr.Number):
            continue

        worksheet = workbook.add_worksheet(feature)
        for label, data in evolutions.items():
            worksheet.write_column(0, label - 1, data)

    workbook.close()
