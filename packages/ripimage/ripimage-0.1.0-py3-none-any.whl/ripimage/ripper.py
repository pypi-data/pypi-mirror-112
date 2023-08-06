import numpy as np
import cv2
import os
from math import sqrt, ceil, floor
from alive_progress import alive_bar
def get_basename(filename):
    """Strip path and extension. Return basename."""
    return os.path.splitext(os.path.basename(filename))[0]

class Tile(object):

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    @property
    def basename(self):
        """Strip path and extension. Return base filename."""
        return get_basename(self.filename)
    
    def generate_filename(
        self, directory=os.getcwd(), prefix="tile", format="png", path=True
    ):
        """Construct and return a filename for this tile."""
        filename = prefix + "_{col:02d}_{row:02d}.{ext}".format(
            col=self.column, row=self.row, ext=format.lower().replace("jpeg", "jpg")
        )
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format="png"):
        if not filename:
            filename = self.generate_filename(format=format)
        cv2.imwrite(filename, self.image)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return "<Tile #{} - {}>".format(
                self.number, os.path.basename(self.filename)
            )
        return "<Tile #{}>".format(self.number)

def calc_columns_rows(n):
    """
    Calculate the number of columns and rows required to divide an image
    into ``n`` parts.

    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)


def validate_image(image, number_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99

    try:
        number_tiles = int(number_tiles)
    except BaseException:
        raise ValueError("number_tiles could not be cast to integer.")

    if number_tiles > TILE_LIMIT or number_tiles < 2:
        raise ValueError(
            "Number of tiles must be between 2 and {} (you \
                          asked for {}).".format(
                TILE_LIMIT, number_tiles
            )
        )

def validate_image_col_row(image, col, row):
    """Basic checks for columns and rows values"""
    SPLIT_LIMIT = 99

    try:
        col = int(col)
        row = int(row)
    except BaseException:
        raise ValueError("columns and rows values could not be cast to integer.")

    if col < 1 or row < 1 or col > SPLIT_LIMIT or row > SPLIT_LIMIT:
        raise ValueError(
            f"Number of columns and rows must be between 1 and"
            f"{SPLIT_LIMIT} (you asked for rows: {row} and col: {col})."
        )
    if col == 1 and row == 1:
        raise ValueError("There is nothing to divide. You asked for the entire image.")

def slice(
    filename,
    number_tiles=None,
    col=None,
    row=None,
    save=True,
    DecompressionBombWarning=True,
):
    """
    Split an image into a specified number of tiles.

    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.

    Kwargs:
       save (bool): Whether or not to save tiles to disk.
       DecompressionBombWarning (bool): Whether to suppress
       Pillow DecompressionBombWarning

    Returns:
        Tuple of :class:`Tile` instances.
    """
    '''if DecompressionBombWarning is False:
        Image.MAX_IMAGE_PIXELS = None'''

    im = cv2.imread(filename)
    im_w, im_h, = im.shape[:2]
    columns = 0
    rows = 0
    if number_tiles:
        validate_image(im, number_tiles)
        columns, rows = calc_columns_rows(number_tiles)
    else:
        validate_image_col_row(im, col, row)
        columns = col
        rows = row

    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    with alive_bar(columns*rows) as bar:
        for pos_y in range(0, im_h - rows, tile_h):  # -rows for rounding error.
            for pos_x in range(0, im_w - columns, tile_w):  # as above.
                area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
                image = im[area[0]:area[2], area[1]:area[3]]
                position = (int(floor(pos_x / tile_w)) + 1, int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)
                tile = Tile(image, number, position, coords)
                tiles.append(tile)
                number += 1
                bar()
    if save:
        save_tiles(
            tiles, prefix=get_basename(filename), directory=os.path.dirname(filename)
        )
    return tuple(tiles)

def save_tiles(tiles, prefix="", directory=os.getcwd(), format="png"):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.

    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.

    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.

    Returns:
        Tuple of :class:`Tile` instances.
    """
    for tile in tiles:
        tile.save(
            filename=tile.generate_filename(
                prefix=prefix, directory=directory, format=format
            ),
            format=format,
        )
    return tuple(tiles)

if __name__ == "__main__":
    print("oi")
    tiles = slice("nirvana_smile.png", number_tiles=9, save=False)
    save_tiles(tiles)