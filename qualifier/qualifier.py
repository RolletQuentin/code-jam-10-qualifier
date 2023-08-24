from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """

    # we need to verify if there isn't reminder when you divide image size by tile size
    if (image_size[0] % tile_size[0] != 0) or (image_size[1] % tile_size[1] != 0):
        return False
    else:
        number_of_tiles = (
            image_size[0] // tile_size[0]) * (image_size[1] // tile_size[1])

    # we need to verify if the ordering list is valid
    if (len(ordering) != number_of_tiles):
        return False
    else:
        sortedOrdering = ordering.copy()
        sortedOrdering.sort()
        for i in range(number_of_tiles):
            if i != sortedOrdering[i]:
                return False

    return True


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    # load the image
    image = Image.open(image_path)

    if not (valid_input(image.size, tile_size, ordering)):
        raise ValueError(
            "The tile size or ordering are not valid for the given image")

    # divide the image in tiles
    number_of_tiles_width = image.size[0] // tile_size[0]
    number_of_tiles_height = image.size[1] // tile_size[1]
    number_of_tiles = number_of_tiles_width * number_of_tiles_height
    tiles = []

    for i in range(number_of_tiles):
        tiles.append(image.crop((
            (i % number_of_tiles_width) * tile_size[0],
            (i // number_of_tiles_width) * tile_size[1],
            ((i % number_of_tiles_width)+1) * tile_size[0],
            ((i // number_of_tiles_width)+1) * tile_size[1])
        ))

    # build a new image ordered
    orderedImage = Image.new(image.mode, image.size)
    for i in range(number_of_tiles):
        orderedImage.paste(tiles[ordering[i]],
                           ((i % number_of_tiles_width) * tile_size[0],
                           (i // number_of_tiles_width) * tile_size[1],
                           ((i % number_of_tiles_width)+1) * tile_size[0],
                           ((i // number_of_tiles_width)+1) * tile_size[1]))

    # save the new image
    orderedImage.save(out_path)

    image.close()
    orderedImage.close()


if __name__ == "__main__":
    # print(valid_input(image_size=(256, 256),
    #       tile_size=(128, 128), ordering=[1, 0, 3, 5]))

    # with open("images/great_wave_order.txt", 'r') as f:
    #     ordering = [int(x) for x in f.read().strip().splitlines()]

    # rearrange_tiles("images/great_wave_scrambled.png",
    #                 (16, 16), ordering, "images/test.png")
    ()
