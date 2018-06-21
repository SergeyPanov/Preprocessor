from PIL import Image
import numpy
import os, sys, argparse

RESTORE_DIR = "restored"
BASIC_IMAGE_NAME = "im"
BASIC_EXTENSION = ".png"

parser = argparse.ArgumentParser()

parser.add_argument("--greyscale", action="store_true", help="Execute greyscaling.", default=None)
parser.add_argument("--path", help="Path to source.", default=None)

parser.add_argument("--posp", action="store_true",
                    help="Execute postprocessing. Convert vectors into black-white images.", default=None)

parser.add_argument("--width", help="Width of image.", default=None, type=int)
parser.add_argument("--height", help="Height of image.", default=None, type=int)

parser.add_argument("--vec", action="store_true", help="Execute vectorization.", default=None)

args = parser.parse_args()


def bw_cast(image):
    image_file = Image.open(image)  # open colour image
    image_file = image_file.convert('1')  # convert image to black and white
    return image_file

def image_to_vector(image):
    vector = []
    for i in numpy.asarray(image.convert('L')).tolist():
        for ii in i:
            if ii == 0:
                vector.append("-1")
            else:
                vector.append('1')
    return vector


def greyscale(path):
    if not os.path.isdir(path):
        print("Directory does not exists.", file=sys.stderr)
    bw_path = "bw_preproc_" + path

    if not os.path.isdir(bw_path):
        os.mkdir(bw_path)

    contents = os.listdir(path)
    for c in contents:
        bw_image = bw_cast(path + "/" + c)
        bw_image.save(bw_path + '/' + c)


def vectorize(path):
    if not os.path.isdir(path):
        print("File does not exists.", file=sys.stderr)
    vec_path = "vec_preproc_" + path
    if not os.path.isdir(vec_path):
        os.mkdir(vec_path)
    vectors = []
    contents = os.listdir(path)
    for image in contents:
        vectors.append(image_to_vector(Image.open(path + image)))

    with open(vec_path + '/vectors', 'w') as vecs:
        for vec in vectors:
            vecs.write(" ".join(vec) + "\n")


def vec_to_image(path, w, h):
    if not os.path.exists(RESTORE_DIR):
        os.mkdir(RESTORE_DIR)
    with open(path, "r") as input_file:
        lines = input_file.readlines()

    index = 0
    for line in lines:
        vec = [255 if int(n) == 1 else 0 for n in line.split(" ")]
        image = numpy.zeros([w, h], dtype=numpy.uint8)

        for x in range(w):
            for y in range(h):
                image[x, y] = vec[x * w + y]
        im = Image.fromarray(image)

        im.save(RESTORE_DIR + "/" + BASIC_IMAGE_NAME + "_" + str(index) + BASIC_EXTENSION)
        index += 1


if __name__ == '__main__':

    if args.path != None:
        if args.greyscale != None:
            greyscale(args.path)
        if args.vec != None:
            if args.path != None:
                vectorize(args.path)
        if args.posp != None and args.width != None and args.height != None:
            vec_to_image(args.path, args.width, args.height)
