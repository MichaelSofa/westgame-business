import freetype
import copy
import numpy as np
import cv2 as cv


class put_chinese_text(object):
    def __init__(self, ttf):  # 读取ttf文件
        self._face = freetype.Face(ttf)

    def generate_one(self, text, text_size, text_vscale, text_shear1, text_shear2, color_):
        self._face.set_char_size(text_size * 64)
        matrix = freetype.Matrix(int(0x10000), int(text_shear1 * 0x10000), \
             int(text_shear2 * 0x10000), int(text_vscale * 0x10000))
        pen_translate = freetype.Vector()

        images = []
        for cur_char in text:
            self._face.set_transform(matrix, pen_translate)

            self._face.load_char(cur_char)
            slot = self._face.glyph
            bitmap = slot.bitmap
            image = self.get_np_array_from_bitmap(bitmap)
            if color_ is None:
                images.append(image)
                continue
            image_rgb = np.stack([image, image, image], axis=2)
            '''
            image_rgb_float = image_rgb.astype(np.float64)
            image_rgb_float = image_rgb_float/255*color_
            image_rgb = image_rgb_float.astype(np.uint8)
            '''
            # 说明，这里暂时不用颜色信息，这个在外面调用的时候使用更方便
            # image_rgb[image!=0] = color_
            images.append(image_rgb)

        return images

    def get_np_array_from_bitmap(self, bitmap):
        cols = bitmap.width
        rows = bitmap.rows
        glyph_pixels = bitmap.buffer
        np_list = np.array(glyph_pixels, dtype=np.uint8)
        np_array = np.reshape(np_list, [rows, cols])  # 得到的单个文字点阵
        return np_array

if __name__ == '__main__':
    # just for test
    line = '葵花点穴手排山倒海惊涛骇浪降龙十八掌'

    color_ = (30, 50, 150) # Green
    pos = (3, 3)
    text_size = 150
    ft = put_chinese_text(r'.\FZXSSJW.TTF')
    images = ft.generate_one(line, text_size, 1.0, 0.1, 0.6, color_)
    index = 0
    for image in images:
        index += 1
        #cv.imwrite('ss'+str(index)+'.png', image)
        cv.imshow('show character', image)
        cv.waitKey(0)