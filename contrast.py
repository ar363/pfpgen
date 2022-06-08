def check_contrast(rgb1, rgb2):
    l1 = _relative_luminance(*rgb1)
    l2 = _relative_luminance(*rgb2)

    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)


def _relative_luminance(r, g, b):
    r = _linearize(r)
    g = _linearize(g)
    b = _linearize(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _linearize(v):
    if v <= 0.03928:
        return v / 12.92
    else:
        return ((v + 0.055) / 1.055) ** 2.4
