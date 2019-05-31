import os
import argparse
from PIL import Image
import numpy as np

def dhash(image, hash_size=16):
    image = image.convert('LA').resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    mat = np.array(
        list(map(lambda x: x[0], image.getdata()))
    ).reshape(hash_size, hash_size + 1)

    return ''.join(
        map(
            lambda x: hex(x)[2:].rjust(2, '0'),
            np.packbits(np.fliplr(np.diff(mat) < 0))
        )
    )

def hamming_dist(h1, h2):
    if len(h1) != len(h2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(h1, h2))


parser = argparse.ArgumentParser(description='First test task on images similarity.')
parser.add_argument('--path', required=True, help='folder with images')
args = parser.parse_args()
files = os.listdir(args.path)
pairs = []
threshold = 0.3
for i in range(len(files)):
    img1 = Image.open(args.path + '/' + files[i])
    image_hash = dhash(img1)
    for j in range(len(files)):
        img2 = Image.open(args.path + '/' + files[j])
        image_hash2 = dhash(img2)
        dist = hamming_dist(image_hash, image_hash2) / len(image_hash)
        if dist < threshold and files[i] != files[j] and sorted([files[i], files[j]]) not in pairs:
            pairs.append(sorted([files[i], files[j]]))
            print(files[i], files[j])