#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reto 08: clase ResizeImage."""

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

from dataclasses import dataclass  # , field
import os
from pathlib import Path
# from typing import Union
from wand.image import Image


# class BadSizeError(TypeError):  # noqa
#     def __init__(self,
#                  value: Union[dict, tuple, int], *args: object) -> None:
#         self.value = value
#         super().__init__(*args)


@dataclass(frozen=True)
class ResizeImage:
    """ResizeImage."""

    filein: Path
    fileout: Path
    args: dict[str, int]
    # width: int = field(init=False)
    # height: int = field(init=False)

    def __post_init__(self) -> None:  # noqa
        """Chequeo de los tipos de los argumentos."""
        if not isinstance(self.filein, Path):
            raise TypeError(
                "El primer argumento debe ser de tipo pathlib.Path.")
        if not isinstance(self.fileout, Path):
            raise TypeError(
                "El segundo argumento debe ser de tipo pathlib.Path.")
        if not isinstance(self.args, dict):
            raise TypeError("El tercer argumento debe ser de tipo dict.")
        if not all(isinstance(x, int) for x in self.args.values()):
            raise TypeError(
                "Los valores del tercer argumento tienen que ser "
                "de tipo entero.")

    def check(self) -> bool:
        """Chequeo de los valores."""
        if not self.filein.is_file():
            raise FileNotFoundError(f"No encuentro el fichero {self.filein}")

        if os.path.getsize(self.filein) == 0:
            raise ValueError(f"El fichero {self.filein} está vacio.")

        im = Image(filename=self.filein)
        if not im.mimetype.startswith("image"):
            raise ValueError(
                f"No parece que {self.filein} sea una imágen.")

        if self.fileout.is_file():
            raise FileExistsError(f"El fichero {self.fileout} ya existe.")

        if self.fileout.is_dir():
            raise ValueError(
                "'fileout' debe ser un fichero, no un directorio.")

        try:
            self.args["width"] == self.args["height"]
        except KeyError as k:
            raise RuntimeError(
                "No es posible determinar el tamaño de la imágen.") from k

        if not all(x > 0 for x in self.args.values()):
            raise ValueError(
                "'width' y 'height' tienen que ser enteros positivos.")

        return True

    def execute(self) -> None:
        """execute."""
        im = Image(filename=self.filein)
        im.resize(*self.args.values())
        im.save(filename=self.fileout)

    @property
    def size(self):
        """El tamaño de la imágen redimensionada [RO]."""
        return self.args.values()


def main():  # noqa
    # filein = Path('/home/lorenzo/kk/bb.png')
    # fileout = Path('/home/lorenzo/kk/salida.png')
    filein = Path("../test/proxy-image.png")
    fileout = Path("../test/proxy-image_200x200.png")
    args = {"width": 200, "height": 200}
    resize_image = ResizeImage(filein, fileout, args)
    if resize_image.check():
        resize_image.execute()


if __name__ == '__main__':
    main()
