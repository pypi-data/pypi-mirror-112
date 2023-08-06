import math


def euclidean(coord1, coord2):
    return math.sqrt(((coord1[0] - coord2[0]) ** 2) + ((coord1[1] - coord2[1]) ** 2))


def evaluate_centering(bounds_list, image):
    im_height, im_width, _ = image.shape
    center = (im_width / 2, im_height / 2)
    total_dist = 0

    for bounds in bounds_list:
        x, y, w, h = int(bounds.xmin * im_width), int(bounds.ymin * im_height), int(
            bounds.width * im_width), int(bounds.height * im_height)
        coord = (x + w, y + h)
        dist = euclidean(coord, center)
        total_dist += dist

    return total_dist / len(bounds_list) if len(bounds_list) else None
