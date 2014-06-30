import sys
from PIL import Image
import numpy as np

chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

if len(sys.argv) != 4:
    print('Usage: ./asciinator.py image scale factor')
    sys.exit()

image = sys.argv[1]
scale = float(sys.argv[2])
factor = float(sys.argv[3])
wcf = 7/4


img = Image.open(image)
S = int(round(img.size[0] * scale * wcf)), int(round(img.size[1] * scale))
img = np.sum(np.asarray(img.resize(S)), axis=2)
img -= img.min()

img = (1.0 - img/img.max()) ** factor * (chars.size - 1)

print("\n".join(("".join(r) for r in chars[img.astype(int)])))
