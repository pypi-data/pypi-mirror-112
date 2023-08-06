import cv2 as cv
import numpy as np
import identifyPeople


def apply_kernel(image, a=-4, b=1, c=0):
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    kernel = np.array(([c, b, c], [b, a, b], [c, b, c]), dtype='int')

    result = cv.filter2D(image, -1, kernel)
    # identifyPeople.show_img(result)

    return result


def get_sharpness_score(transformed_image):
    # A sharp image will have a lot of variation
    # A blurry image will be uniform in more places, meaning its variance will be lower
    return transformed_image.var()


def evaluate_sharpness(image):
    return get_sharpness_score(apply_kernel(image))


def normalize_sharpness_scores(group_scores):
    max_val = max(group_scores)

    if not max_val:
        return [1.0] * len(group_scores)

    normalized_scores = [float(score) / float(max_val)
                         for score in group_scores]
    return normalized_scores


if __name__ == '__main__':
    img = identifyPeople.read_img(
        './bestOf/resources/examples/IMG_1667.jpg')
    s = evaluate_sharpness(img)
    print(s)
    img = identifyPeople.read_img(
        './bestOf/resources/examples/IMG_1668.jpg')
    s = evaluate_sharpness(img)
    print(s)
