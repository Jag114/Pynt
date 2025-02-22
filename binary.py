from cv2.typing import MatLike
import colors
#poc3

def threshold(img_bin: MatLike, *args) -> MatLike:
    height, width, *rest = img_bin.shape
    #args = [lim_dol, lim_gora]
    if len(args) == 0:
        peak = colors.grey_histogram_fun(img_bin, False)
        for i in range(0, width - 1):
            for j in range(0, height - 1):
                if img_bin[j, i] > peak:
                    img_bin[j, i] = 255
                else:
                    img_bin[j, i] = 0
    elif len(args) == 1:
        for i in range(0, width - 1):
            for j in range(0, height - 1):
                if img_bin[j, i] > args[0]:
                    img_bin[j, i] = 255
                else:
                    img_bin[j, i] = 0
    else:
        for i in range(0, width - 1):
            for j in range(0, height - 1):
                if img_bin[j, i] > args[0] and img_bin[j, i] < args[1]:
                    img_bin[j, i] = 255
                else:
                    img_bin[j, i] = 0
    return img_bin