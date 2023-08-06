import logging
import os
from collections import defaultdict as dd
from functools import reduce
from io import StringIO
from typing import Dict, List, Tuple

import numpy as np
import numpy.lib.recfunctions as rfn

from femap_neutral_parser import blocks


class Parser:
    def __init__(self, fpath: str, autotranslate=True) -> None:
        self.autotranslate = autotranslate
        self.fpath = os.path.expanduser(fpath)
        self._toc = dd(list)
        if not os.path.isfile(self.fpath):
            raise ValueError(f'file path "{fpath}" not found')
        self._build_toc()
        self._parse_header()
        # self.blocks = {}
        # ---------------------------------------------------------------------
        # collect available defined blocks (code-wise, **not** neutral file wise)
        # this will create once self.__getattr__ will be called:
        #  * `self.header` from B100
        #  * `self.output_sets` from B450
        #  * `self.output_vectors` from B451
        self._defined_block_names = {
            getattr(blocks, b).NAME: getattr(blocks, b)
            for b in dir(blocks)
            if b.startswith("B")
        }

    def info(self, doprint=True):
        msg = []
        if 450 in self._toc:
            msg.append("\nAnalysis")
            msg.append("========")
            for lcid, lc_data in self.output_sets.items():
                msg.append(
                    f" * subcase {lcid}: {lc_data['title']} ({lc_data['anal_type']})"
                )
        if 451 in self._toc:
            msg.append("\nOutputs")
            msg.append("=======")
            msg.append(
                "access to one of them using `.output_vectors[<title>][<SubcaseID>]['record']\n"
            )

            for output_title, output_data in self.output_vectors.items():
                # lcids = ", ".join(map(str, output_data.keys()))
                msg.append(f" * {output_title}")
        if doprint:
            print("\n".join(msg))
            return
        return msg

    def vectors(self, titles, SubcaseIDs=None):
        if not SubcaseIDs:
            SubcaseIDs = tuple(self.output_sets.keys())
        if isinstance(SubcaseIDs, int):
            SubcaseIDs = (SubcaseIDs,)
        recs = []
        key = None
        for SubcaseID in SubcaseIDs:
            arrays = []
            for title in titles:
                try:
                    arrays.append(
                        self.output_vectors[title.lower()][SubcaseID]["record"]
                    )
                except KeyError as exc:
                    logging.error(f"{title=} is not found")
                    raise
            if not key:
                key = "NodeID" if "NodeID" in arrays[0].dtype.names else "ElementID"
            arr = reduce(lambda a1, a2: rfn.rec_join(key, a1, a2), arrays)
            arr = rfn.append_fields(
                arr, "SubcaseID", [SubcaseID] * len(arr), asrecarray=True, usemask=False
            )
            recs.append(arr)
        arr = rfn.stack_arrays(recs, asrecarray=True, usemask=False)
        return arr

    def available_blocks(self) -> Dict[int, str]:
        return {
            getattr(blocks, b).NAME: getattr(blocks, b).id()
            for b in dir(blocks)
            if b.startswith("B")
        }

    def __getattr__(self, key: str):
        # look for blocks having key as NAME
        try:
            block_id = self._defined_block_names[key].id()
        except KeyError as exc:
            selfattrs = [attr for attr in dir(self) if attr.startswith("get_")]
            msg = f"'{key}' not found in _defined_block_names."
            # msg += f"\n  available keys are: {list(self._defined_block_names.keys())}"
            msg += f"\n  available attributes are {selfattrs}"

            raise KeyError(msg)
        block = self._parse_blocks(block_id)
        if block_id == 451:
            data = block.digest(autotranslate=self.autotranslate)
        else:
            data = block.digest()
        setattr(self, key, data)
        return data

    def _parse_header(self):
        """parse block 100. This needs to be done at low-level since we will
        pick FEMAP's version number from there."""
        txt = tuple(self._get_block_raw_data(100))[0]
        b100 = blocks.B100(version=0)  # we do not have correct version at this point
        b100.parse(txt)
        self.header = b100.data[0]
        # also assign directly for convenieance
        self.femap_version = b100.data[0]["femap_version"]
        self.db_title = b100.data[0]["db_title"]

    def _build_toc(self):
        """parse the document to retrieve blocks locations"""
        nb_lines = 0
        current_block = None
        for line_nb, line in enumerate(open(self.fpath, "r")):
            # if line_nb == 1598:
            #     breakpoint()
            line = line.strip()
            if line == "-1":
                if not current_block:
                    # ---------------------------------------------------------
                    # new block is coming, block ID known the line after
                    # ---------------------------------------------------------
                    current_block = -1  # set waiting status
                    continue
                else:
                    # ---------------------------------------------------------
                    # block is finishing
                    # ---------------------------------------------------------
                    self._toc[current_block][-1].append(line_nb)
                    current_block = None
                    continue
            if current_block == -1:
                # -------------------------------------------------------------
                # waiting status
                current_block = int(line)
                self._toc[current_block].append([line_nb + 1])
            nb_lines += 1
        # ---------------------------------------------------------------------
        # EOF
        # we sometimes miss trailing "-1". fix it:
        if current_block is not None and current_block > 0:
            self._toc[current_block][-1].append(line_nb)
        self._toc = dict(self._toc)
        logging.info("parsed %d lines", nb_lines)

    def _get_block_raw_data(self, block_id, as_file_like=False):
        """yield file-like objects containing block data"""
        fh = open(self.fpath)
        line_offset = 0
        for line_start, line_end in self._toc[block_id]:
            lines = range(line_start, line_end)
            lines_content = []
            for line_nb, line in enumerate(fh, start=line_offset):
                if line_nb > line_end:
                    line_offset = line_nb + 1
                    break
                if line_nb in lines:
                    lines_content.append(line)
            if as_file_like:
                txt = StringIO()
                txt.writelines(lines_content)
                txt.seek(0)
            else:
                txt = lines_content
            yield txt
        fh.close()

    def _parse_blocks(self, block_id: int) -> None:
        """instantiate a block and feed it with relevant raw block text.
        Next step is supposed to be block.digest()
        """
        block = getattr(blocks, f"B{block_id}")(version=self.femap_version)
        for txt in self._get_block_raw_data(block_id=block_id):
            block.parse(txt)
        return block

    # =========================================================================
    # engineering shortcuts
    # =========================================================================
    def get_displacements(self, raw=False):
        neutral_headers = [
            "T1 translation",
            "T2 translation",
            "T3 translation",
            "R1 rotation",
            "R2 rotation",
            "R3 rotation",
        ]
        data = self.vectors(neutral_headers)
        if not raw:
            data = rfn.rename_fields(
                data, dict(zip(neutral_headers, ("t1", "t2", "t3", "r1", "r2", "r3")))
            )
        return data

    # -------------------------------------------------------------------------
    # reactions
    def get_reactions(self, raw=False):
        neutral_headers = [
            "T1 SPC force",
            "T2 SPC force",
            "T3 SPC force",
            "R1 SPC moment",
            "R2 SPC moment",
            "R3 SPC moment",
        ]
        data = self.vectors(neutral_headers)
        if not raw:
            data = rfn.rename_fields(
                data, dict(zip(neutral_headers, ("t1", "t2", "t3", "r1", "r2", "r3")))
            )
        return data

    def get_cbar_force(self, raw=False):
        neutral_headers = [
            "BAR EndA Plane1 Moment",
            "BAR EndA Plane2 Moment",
            "BAR EndB Plane1 Moment",
            "BAR EndB Plane2 Moment",
            "BAR EndA Pl1 Shear Force",
            "BAR EndA Pl2 Shear Force",
            "BAR EndA Axial Force",
            "BAR EndA Torque",
            # "BAR EndB Axial Force",
            # "BAR EndB Pl1 Shear Force",
            # "BAR EndB Pl2 Shear Force",
            # "BAR EndB Torque",
        ]
        data = self.vectors(neutral_headers)
        if not raw:
            data = rfn.rename_fields(
                data,
                dict(
                    zip(
                        neutral_headers,
                        [
                            "bending_moment_a1",
                            "bending_moment_a2",
                            "bending_moment_b1",
                            "bending_moment_b2",
                            "shear1",
                            "shear2",
                            "axial",
                            "torque",
                        ],
                    )
                ),
            )
        return data

    def get_cbush_force(self, raw=False):
        neutral_headers = [
            "BUSH Force XE",
            "BUSH Force YE",
            "BUSH Force ZE",
            "BUSH Moment XE",
            "BUSH Moment YE",
            "BUSH Moment ZE",
        ]
        data = self.vectors(neutral_headers)
        if not raw:
            data = rfn.rename_fields(
                data,
                dict(zip(neutral_headers, ["fx", "fy", "fz", "mx", "my", "mz"])),
            )
        return data

    # # -------------------------------------------------------------------------
    # # Bar engineering forces
    # def get_cbar_forces(self, raw=False):
    #     vectorsA = [
    #         "BAR EndA Axial Force",
    #         "BAR EndA Pl1 Shear Force",
    #         "BAR EndA Pl2 Shear Force",
    #         "BAR EndA Plane2 Moment",
    #         "BAR EndA Plane1 Moment",
    #         "BAR EndA Torque",
    #     ]
    #     pntA = self.vectors(vectorsA)
    #     vectorsB = [
    #         "BAR EndB Axial Force",
    #         "BAR EndB Pl1 Shear Force",
    #         "BAR EndB Pl2 Shear Force",
    #         "BAR EndB Plane2 Moment",
    #         "BAR EndB Plane1 Moment",
    #         "BAR EndB Torque",
    #     ]
    #     pntB = self.vectors(vectorsB)
    #     if not raw:
    #         cols = ("1", "2", "3", "4", "5", "6", "SubcaseID", "eid")
    #         pntA = rfn.rename_fields(
    #             pntA, dict(zip(vectorsA + ["SubcaseID", "ElementID"], cols))
    #         )
    #         pntB = rfn.rename_fields(
    #             pntB, dict(zip(vectorsB + ["SubcaseID", "ElementID"], cols))
    #         )
    #     # ---------------------------------------------------------------------
    #     # keep track of extremity
    #     pntA = rfn.append_fields(
    #         pntA, "ga/gb", ["A"] * len(pntA), asrecarray=True, usemask=False
    #     )
    #     pntB = rfn.append_fields(
    #         pntB, "ga/gb", ["B"] * len(pntA), asrecarray=True, usemask=False
    #     )
    #     # ---------------------------------------------------------------------
    #     # stack
    #     data = rfn.stack_arrays((pntA, pntB), asrecarray=True, usemask=False)
    #     return data


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
