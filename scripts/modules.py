import math, re
from .utils import *
from PIL import Image

def add_figure(output, param_list, figures, text, config):
    column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count \
    = param_list

    # figure no caption
    img_caption = ''

    chose_id = np.random.randint(1, len(figures))
    img_path = figures[chose_id]

    img_width_ratio = gen_random(config.imgWidthMinRatio, config.imgWidthMaxRatio)
    img_width = int(img_width_ratio * column_width)

    img = Image.open(img_path)
    img_height = img_width * img.size[1] / img.size[0]
    if img_height > config.imgHeightMaxRatio * column_width:
        img_height = img_height * 0.8
        img_width = img_width * 0.8
    if img_height > config.pageHeight - offset_y - marginPt:
        return None

    # add figure no caption
    cur_img_offset = offset_x + (column_width - img_width) / 2
    output += gen_str_fig(img_width, cur_img_offset, offset_y, img_width, img_height, img_path)
    # groundtruth
    update_groundtruth(groundtruth, groundtruth_element_count,
                             'figure', img_path, '', [offset_y, offset_y + img_height,
                                                      cur_img_offset, cur_img_offset + img_width])
    # adjust
    offset_x = offset_x
    offset_y += img_height + font_size * config.paraSkipRatio

    return offset_x, offset_y, groundtruth, groundtruth_element_count, output


def add_table(output, param_list, tables, config):
    column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count \
    = param_list

    # table no caption
    img_caption = ''
    chose_id = np.random.randint(1, len(tables))
    img_path = tables[chose_id]

    img_width_ratio = gen_random(config.imgWidthMinRatio, config.imgWidthMaxRatio)
    img_width = int(img_width_ratio * column_width)

    img = Image.open(img_path)
    img_height = img_width * img.size[1] / img.size[0]
    if img_height > config.imgHeightMaxRatio * column_width:
        img_height = img_height * 0.8
        img_width = img_width * 0.8
    if img_height > config.pageHeight - offset_y - marginPt:
        return None

    # add table(table is also an image)
    cur_img_offset = offset_x + (column_width - img_width) / 2
    output += gen_str_fig(img_width, cur_img_offset, offset_y, img_width, img_height, img_path)
    # groundtruth
    update_groundtruth(groundtruth, groundtruth_element_count,
                             'table', img_path, '', [offset_y, offset_y + img_height,
                                                      cur_img_offset, cur_img_offset + img_width])
    # adjust
    offset_x = offset_x
    offset_y += img_height + font_size * config.paraSkipRatio

    return offset_x, offset_y, groundtruth, groundtruth_element_count, output


def add_list(output, param_list, text, config):
    column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count \
    = param_list

    chose_id = np.random.choice(range(len(text)))
    text_length = 500
    while len(text[chose_id])<text_length:
        chose_id = np.random.choice(range(len(text)))
    words = text[chose_id].split(' ')
    chose_text = words[0]
    index = 0
    while len(chose_text) < text_length:
        index += 1
        chose_text += ' '+words[index]

    chose_text = re.sub('[^a-zA-Z0-9\.\?,;! ]', '', chose_text)

    item_sep = 0
    list_type = np.random.choice(config.listType)

    # print('column_width:', column_width)
    text_width = column_width - 4*(font_size * config.fontHorizonCoeff)
    # print('text_width:', text_width)
    fonts_unit_row = int(text_width / (font_size * config.fontHorizonCoeff))
    height_unit_font = 0

    item_length = np.random.randint(config.itemLengthMin, config.itemLengthMax)
    item_start = 0
    content = ''
    item_nb = np.random.randint(1, config.itemNumberMax + 1)

    if np.random.random() < config.hasColors:
        color = np.random.choice(config.colors)
    else:
        color = 'black'

    ratios = [1.5, 2.7, 3.7,]
    for ii in range(item_nb):
        ratio = np.random.choice(ratios)
        item_length_current = int(ratio * fonts_unit_row)
        tmp = chose_text[item_start:(item_start + item_length_current)]

        if (len(tmp)/fonts_unit_row > 1) and (0.3<(len(tmp)/fonts_unit_row)-int(len(tmp)/fonts_unit_row)<0.8):
            content += gen_str_item(tmp, color)
            height_unit_font += math.ceil(len(tmp) * 1.0 / fonts_unit_row)
            # print('list height: ', math.ceil(len(tmp) * 1.0 / fonts_unit_row))
        else:
            continue
        item_start += item_length_current
    if not len(content):
        return None

    list_height = font_size * 1.3 * (height_unit_font)
    if offset_y + list_height > config.pageHeight - marginPt:
        return None

    # add element
    str_itemize = gen_str_itemize(column_width, list_type, offset_x, offset_y, item_sep, content)  # TODO
    output += str_itemize

    list_id = 'list' + str(groundtruth_element_count['list'])
    # add calculation
    # output += gen_str_itemize_size(column_width,
    #                                      list_type,
    #                                      item_sep,
    #                                      content,
    #                                      list_id)
    # groundtruth
    update_groundtruth(groundtruth, groundtruth_element_count, 'list', '', content,
                             [offset_y+10, offset_y + 10 + list_height, offset_x, offset_x + column_width])
    # adjust
    offset_y += list_height + font_size * (config.paraSkipRatio + 1)
    return offset_x, offset_y, groundtruth, groundtruth_element_count, output


def add_text(output, param_list, text, config):
    column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count \
    = param_list

    text_width = column_width
    try:
        text_line = (config.pageHeight - offset_y - marginPt) / font_size
        text_line_current = np.random.randint(10, min(text_line, config.textMaxLine))
        text_height = text_line_current * font_size * config.fontVerticalCoeff
    except:
        return None

    text_length = int(text_width / (font_size * config.fontHorizonCoeff)) * text_line_current
    chose_id = np.random.choice(range(len(text)))
    while len(text[chose_id])<text_length:
        chose_id = np.random.choice(range(len(text)))
    words = text[chose_id].split(' ')
    chose_text = words[0]
    index = 0
    while len(chose_text) < text_length:
        index += 1
        chose_text += ' '+words[index]

    chose_text = re.sub('[^a-zA-Z0-9\.\?,;! ]', '', chose_text)
    chose_text = text[chose_id][:text_length]
    chose_text = chose_text.replace(chose_text.split(' ')[-1], '')

    # add element
    if np.random.random() < config.hasColors:
        color = np.random.choice(config.colors)
    else:
        color = 'black'
    output += gen_str_text(text_width, offset_x, offset_y, chose_text, color=color)

    # add calculation
    text_id = 'text' + str(groundtruth_element_count['text'])
    output += gen_str_text_size(text_width, chose_text, text_id)
    # groundtruth
    update_groundtruth(groundtruth, groundtruth_element_count, 'text', '', chose_text,
                             [offset_y, offset_y + text_height, offset_x, offset_x + min(text_width, len(text) * font_size * config.fontHorizonCoeff)])
    # adjust
    offset_y += text_height + font_size * (config.paraSkipRatio - 1)
    return offset_x, offset_y, groundtruth, groundtruth_element_count, output


def add_line(output, param_list, config):
    column_width, offset_x, offset_y, line_width, font_size, groundtruth, groundtruth_element_count \
    = param_list
    if np.random.random() < config.hasColors:
        color = np.random.choice(config.colors)
    else:
        color = 'black'
    line_width = np.random.randint(1, config.borderLineMaxWidth / 2)
    output += gen_str_rectangle(offset_x, offset_y, column_width, line_width, color)
    offset_y += line_width + font_size * config.paraSkipRatio

    return offset_x, offset_y, groundtruth, groundtruth_element_count, output