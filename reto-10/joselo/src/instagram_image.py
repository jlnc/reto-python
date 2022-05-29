#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reto 10: clase InstagramImage."""

# Copyright (c) 2022 José Lorenzo Nieto Corral <a.k.a. jlnc> <a.k.a. JoseLo>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from functools import reduce
from pathlib import Path
from typing import Optional
from PIL import Image
import pilgram
import pilgram.css


class InstagramImage:
    """InstagramImage."""

    # Un diccionario cuyas claves son conjuntos con los nombres de
    # los filtros de un módulo dado y cuyos valores son el módulo que
    # proporciona dichos filtros.
    _FILTROS: dict[frozenset[str], str] = {
        frozenset(
            ["_1977", "aden", "brannan", "brooklyn", "clarendon", "earlybird",
             "gingham", "hudson", "inkwell", "kelvin", "lark", "lofi",
             "maven", "mayfair", "moon", "nashville", "perpetua", "reyes",
             "rise", "slumber", "stinson", "toaster", "valencia", "walden",
             "willow", "xpro2"]
            ): "pilgram",
        frozenset(
            ["contrast", "grayscale", "hue_rotate", "saturate", "sepia"]
            ): "pilgram.css",
        }

    def __init__(self, filein: Path, fileout: Path,
                 args: Optional[dict[str, str]] = None) -> None:

        self.__filein = Path(filein)
        self.__fileout = Path(fileout)
        self.__filter = None

        try:
            filtro = args['filter']
        except KeyError:
            filtro = None

        if filtro in self.filtros():
            for item in InstagramImage._FILTROS:
                if filtro in item:
                    modulo = InstagramImage._FILTROS[item]
                    break
            self.__filter = f"{modulo}.{filtro}"

    # Por conveniencia para que la función test pueda ejecutar todos los
    # filtros, uno detrás de otro.
    @classmethod
    def filtros(cls):
        """La unión de todos los subconjuntos de filtros."""
        return reduce(set.union, cls._FILTROS, set())

    def check(self) -> bool:
        """check."""
        return self.__filter is not None \
            and self.__filein.is_file() \
            and not self.__filein.is_symlink() \
            and not self.__fileout.exists()

    def execute(self) -> None:
        """execute."""
        import ast
        try:
            image = Image.open(self.__filein)
            func_call = f"{self.__filter}(image)"
            image = ast.literal_eval(func_call)
            image.save(self.__fileout)
        except Exception:
            pass


def main():  # noqa
    filter_name = "lofi"
    filein = Path("/home/lorenzo/kk/bb.jpg")
    fileout = Path(f"/home/lorenzo/kk/bb_{filter_name}.jpg")
    action = InstagramImage(filein, fileout, {'filter': filter_name})
    if action.check():
        action.execute()


def test():  # noqa
    filein = Path("/home/lorenzo/kk/bb.jpg")
    for filter_name in InstagramImage.filtros():
        fileout = Path(f"/home/lorenzo/kk/bb_{filter_name}.jpg")
        action = InstagramImage(filein, fileout, {'filter': filter_name})
        if action.check():
            action.execute()


if __name__ == '__main__':
    # main()
    test()
