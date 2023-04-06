import freetype
import copy
import numpy as np
import cv2 as cv


class put_chinese_text(object):
    def __init__(self, ttf):
        self._face = freetype.Face(ttf)

    def draw_text(self, image, pos, text, text_size, text_color):
        '''
        draw chinese(or not) text with ttf
        :param image:  image(numpy.ndarray) to draw text
        :param pos:  where to draw text
        :param text:  the context, for chinese should be unicode type
        :param text_size: text size
        :param text_color:text color
        :return:   image
        '''
        self._face.set_char_size(text_size * 64)
        metrics = self._face.size
        ascender = metrics.ascender / 64.0

        # descender = metrics.descender/64.0
        # height = metrics.height/64.0
        # linegap = height - ascender + descender
        ypos = int(ascender)

        text = text
        img = self.draw_string(image, pos[0], pos[1] + ypos, text, text_color)
        return img

    def draw_string(self, img, x_pos, y_pos, text, color):
        '''
        draw string
        :param x_pos: text x-postion on img
        :param y_pos: text y-postion on img
        :param text: text (unicode)
        :param color: text color
        :return:  image
        '''
        prev_char = 0
        pen = freetype.Vector()
        pen.x = x_pos << 6 # div 64
        pen.y = y_pos << 6

        hscale = 1.0
        matrix = freetype.Matrix(int(hscale) * 0x10000, int(0.2 * 0x10000), \
             int(0.0 * 0x10000), int(1.1 * 0x10000))
        cur_pen = freetype.Vector()
        pen_translate = freetype.Vector()

        image = copy.deepcopy(img)
        for cur_char in text:
            #self._face.set_transform(matrix, pen_translate)

            self._face.load_char(cur_char)
            kerning = self._face.get_kerning(prev_char, cur_char)
            pen.x += kerning.x
            slot = self._face.glyph
            bitmap = slot.bitmap

            cur_pen.x = pen.x
            cur_pen.y = pen.y - slot.bitmap_top * 64
            self.draw_ft_bitmap(image, bitmap, cur_pen, color)

            pen.x += slot.advance.x
            prev_char = cur_char

        return image

    def draw_ft_bitmap(self, img, bitmap, pen, color):
        '''
        draw each char
        :param bitmap: bitmap
        :param pen: pen
        :param color: pen color e.g.(0,0,255) - red
        :return:  image
        '''
        x_pos = pen.x >> 6
        y_pos = pen.y >> 6
        cols = bitmap.width
        rows = bitmap.rows

        glyph_pixels = bitmap.buffer
        '''
        print(type(glyph_pixels))
        print(len(glyph_pixels))
        print("cols x rows:", cols*rows)
        '''
        print("cols:", cols)
        print("rows:", rows)
        print("y_pos:", y_pos)
        print("x_pos:", x_pos)
        if y_pos < 0:
            y_pos = 0
        np_list = np.array(glyph_pixels)
        np_array = np.reshape(np_list, [rows, cols])  # 得到的单个文字点阵
        img_little = img[y_pos:y_pos+rows, x_pos:x_pos+cols]
        img_little[np_array!=0] = np.array(color, dtype=np.uint8)
        img[y_pos:y_pos+rows, x_pos:x_pos+cols] = img_little
        '''
        for row in range(rows):
            for col in range(cols):
                if glyph_pixels[row * cols + col] != 0:
                    try:
                        img[y_pos + row][x_pos + col][0] = color[0]
                        img[y_pos + row][x_pos + col][1] = color[1]
                        img[y_pos + row][x_pos + col][2] = color[2]
                    except:
                        continue
        '''

if __name__ == '__main__':
    # just for test
    import cv2
    line = 'ttf文件读取字体的点阵'
    img = cv2.imread('./shana.jpg')

    color_ = (30, 50, 150) # Green
    pos = (3, 3)
    text_size = 150
    ft = put_chinese_text(r'.\FZXSSJW.TTF')
    image = ft.draw_text(img, pos, line, text_size, color_)

    cv2.imshow('ss', image)
    cv2.waitKey(0)