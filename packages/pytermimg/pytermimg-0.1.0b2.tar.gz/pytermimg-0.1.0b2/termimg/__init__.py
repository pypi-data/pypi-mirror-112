import os
import typing as t

from .printers import ITerm2Printer, SixelPrinter, UTF8Printer
from .printers._base import ImagePrinterBase


def get_printer(override: t.Optional[str] = None) -> t.Optional[ImagePrinterBase]:
    override = override or os.getenv("TERMIMG_PRINTER")
    if override == "iterm2":
        return ITerm2Printer()
    elif override == "sixel":
        return SixelPrinter()
    elif override == "utf8" or override == "utf-8":
        return UTF8Printer()

    if ITerm2Printer.supported():
        return ITerm2Printer()
    elif SixelPrinter.supported():
        return SixelPrinter()
    elif UTF8Printer.supported():
        return UTF8Printer()
    return None


__all__ = ["get_printer"]
