from PIL import Image
import numpy
import os, sys, argparse

RESTORE_DIR = "restored"
BASIC_IMAGE_NAME = "im"
BASIC_EXTENSION = ".png"

parser = argparse.ArgumentParser()

parser.add_argument("--prep", action="store_true", help="Execute preprocessing. Convert images into black-white images and create file with vectors.", default=None)
parser.add_argument("--resource", help="Path to directory with files supposed to be the same size.", default=None)

parser.add_argument("--posp", action="store_true", help="Execute postprocessing. Convert vectors into black-white images.", default=None)

parser.add_argument("--width", help="Width of image.", default=None, type=int)
parser.add_argument("--height", help="Height of image.", default=None, type=int)
parser.add_argument("--vectors", help="Path to file with vectors.", default=None)

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



def vectorize(path):
    if not os.path.isdir(path):
        print("Directory does not exists.", file=sys.stderr)
    bw_path = path + "_bw_preproc"
    vec_path = path + "_vec_preproc"

    if not os.path.isdir(bw_path):
        os.mkdir(bw_path)

    if not os.path.isdir(vec_path):
        os.mkdir(vec_path)

    vectors = []

    contents = os.listdir(path)
    for c in contents:
        bw_image = bw_cast(path + "/" + c)
        bw_image.save(bw_path + '/' + c)
        vectors.append(image_to_vector(bw_image))

    with open(vec_path + '/vectors', 'w') as vecs:
        for vec in vectors:
            vecs.write(" ".join(vec) + "\n")


def vec_to_image(path, w, h):
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
    if args.prep != None:
        if args.resource != None:
            vectorize(args.resource)
        else:
            print("Resource parameter is required.", file=sys.stderr)
            exit(1)

    if args.posp != None:
        if args.width != None and args.height != None and args.vectors != None:
            vec_to_image(args.vectors, args.width, args.height)
        else:
            print("Size and path to vectors are required.", file=sys.stderr)
            exit(1)
