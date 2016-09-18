import colorsys


# rgb_val is between 0 and 255
def val_to_hex_str(rgb_val):
    print('rgb_val:{0}\n'.format(rgb_val))

    representation = str(hex(rgb_val))[2:]
    if (len(representation) == 1):
        representation = "0" + representation
    return representation


def hsv_to_hex_rgb_str(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    (R, G, B) = int(255 * r), int(255 * g), int(255 * b)
    hexval = "#" + val_to_hex_str(R) + val_to_hex_str(G) + val_to_hex_str(B)
    return hexval


def rgb_to_hex(rgb):
    print('rgb:{0}\n'.format(rgb))
    return '#' + ''.join(map(val_to_hex_str, rgb))


def hex_to_rgb(hex_str):
    if hex_str[0] == ord('#'):
        hex_str = hex_str[1:]
    r_str, g_str, b_str = hex_str[0:2], hex_str[2:4], hex_str[4:6]
    return (int(r_str, 16), int(g_str, 16), int(b_str, 16))
