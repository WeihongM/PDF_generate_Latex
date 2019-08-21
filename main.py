import argparse
from PIL import Image
import json, sys, os
import numpy as np
from tqdm import tqdm

from scripts.config import config
from scripts.modules import *
import scripts.utils as utils

def main(config, args, layouts):
    # init elements
    img_base_dir = args.img_dir
    graph_base_dir = args.graph_dir
    text_path = args.txt

    figures = [os.path.join(img_base_dir, file) for file in os.listdir(img_base_dir)]
    tables = [os.path.join(graph_base_dir, file) for file in os.listdir(graph_base_dir)]
    text = open(text_path).read().splitlines()

    # main
    config.pageWidth = config.pageWidth * config.inches2Pt
    config.pageHeight = config.pageHeight * config.inches2Pt

    for it_page in tqdm(range(args.pageNum)):
        sec_ele_num = 0

        # try:
        fout_name = '{}{}.tex'.format(config.prefix, it_page)

        groundtruth = {}
        groundtruth['type'] = 'Doc'
        groundtruth['structure'] = []
        groundtruth_element_count = {'figure': 0, 'table': 0, 'caption': 0,
                                     'section': np.random.randint(1, 10), 'subsection': np.random.randint(1, 10),
                                     'subsubsection': np.random.randint(1, 10), 'list': 0, 'text': 0}

        output = ''

        # font_size = np.random.randint(config.fontSizeMin, config.fontSizeMax+1)
        font_size = 10
        margin = np.random.random() * (config.marginMax - config.marginMin) + config.marginMin
        marginPt = margin * config.inches2Pt
        # marginPt = 30   # margin between left and right
        indent = np.random.choice([True, False])
        output += utils.gen_str_config(font_size, margin, indent,
                                       [groundtruth_element_count['section'],
                                        groundtruth_element_count['subsection'],
                                        groundtruth_element_count['subsubsection']])

        output += utils.gen_str_begin()
        output += utils.gen_str_openfile(fout_name + '.out')

        offset_x = marginPt
        offset_y = marginPt

        # border line
        if np.random.random() < config.hasColors:
            color = np.random.choice(config.colors)
        else:
            color = 'black'

        line_width = np.random.randint(1, config.borderLineMaxWidth)
        if np.random.random() < config.hasHorizonBorder:
            output += utils.gen_str_rectangle(offset_x, np.random.randint(1, offset_y-line_width), config.pageWidth - 2 * marginPt, line_width, color)
        if np.random.random() < config.hasHorizonBorder:
            output += utils.gen_str_rectangle(offset_x, np.random.randint(config.pageHeight-marginPt, config.pageHeight-line_width), config.pageWidth - 2 * marginPt, line_width, color)
        if np.random.random() < config.hasVerticalBorder:
            output += utils.gen_str_rectangle(np.random.randint(1, offset_y-line_width), offset_y, line_width, config.pageHeight - 2 * marginPt, color)
        if np.random.random() < config.hasVerticalBorder:
            output += utils.gen_str_rectangle(np.random.randint(config.pageWidth-marginPt, config.pageWidth-line_width), offset_y, line_width, config.pageHeight - 2 * marginPt, color)

        # add element
        it_element = 0
        margin_delta = np.random.random() * config.marginMin * config.inches2Pt
        column_layout = np.random.choice(layouts)
        for index in range(len(column_layout)):
            num_columns = sum(column_layout)
            unit_column_width =(config.pageWidth - 2 * marginPt - num_columns * margin_delta) / num_columns
            column_width = column_layout[index] * unit_column_width
            offset_x = marginPt + sum(column_layout[:index]) * unit_column_width + index * margin_delta
            offset_y = marginPt
            column_right = marginPt + sum(column_layout[:(index+1)]) * unit_column_width + index * margin_delta
            it_column = index

            while offset_y < (config.pageHeight - marginPt):

                if it_element > config.maxNumElements:
                    break

                opt = np.random.random()

                if opt < config.distribution['figure']:
                    # add figure
                    param_list = \
                    [column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count]
                    val = add_figure(output, param_list, figures, text, config)
                    if val is not None:
                        offset_x, offset_y, groundtruth, groundtruth_element_count, output \
                        = val
                        it_element += 1
                    else:
                        # mean enough figure same column
                        break
                elif opt < config.distribution['table']:
                    # add table
                    param_list = \
                    [column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count]
                    val = add_table(output, param_list, tables, config)
                    if val is not None:
                        offset_x, offset_y, groundtruth, groundtruth_element_count, output \
                        = val
                        it_element += 1
                    else:
                        # mean enough figure same column
                        break
                elif opt < config.distribution['list']:
                    # add list
                    param_list = \
                    [column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count]
                    val = add_list(output, param_list, text, config)
                    if val is not None:
                        offset_x, offset_y, groundtruth, groundtruth_element_count, output \
                        = val
                        it_element += 1
                    else:
                        break
                elif opt < config.distribution['text']:
                    # add text 
                    param_list = \
                    [column_width, offset_x, offset_y, marginPt, font_size, groundtruth, groundtruth_element_count]
                    val = add_text(output, param_list, text, config)
                    if val is not None:
                        offset_x, offset_y, groundtruth, groundtruth_element_count, output \
                        = val
                        it_element += 1
                    else:
                        break
                elif opt < config.distribution['line']:
                    param_list = \
                        [column_width, offset_x, offset_y, line_width, font_size, groundtruth, groundtruth_element_count]
                    val = add_line(output, param_list, config)
                    offset_x, offset_y, groundtruth, groundtruth_element_count, output \
                    = val
                    it_element += 1


        # finalize output string
        output += utils.gen_str_closefile()
        output += utils.gen_str_end()

        # filename
        groundtruth['filename'] = fout_name

        # save tex file
        with open(fout_name, 'w') as fout:
            fout.write(output)
        # save groundtruth to json
        with open(fout_name + '.json', 'w') as fout:
            json.dump(groundtruth, fout, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate PDF')

    parser.add_argument('--img-dir', default="data/Images", type=str,
                        help="dir path to load images")
    parser.add_argument('--graph-dir', default="data/Graphs", type=str,
                        help="dir path to load graphs")
    parser.add_argument('--txt', default="data/Doc/out_wiki.en.txt", type=str,
                        help="txt path to load wiki txt content")
    parser.add_argument('--pageNum', default=1, type=int,
                        help="page number to generate")
    args = parser.parse_args()

    layouts = [[1], [1], [1,1], [1,1,1], [1,2], [1,2], [2,1], [2,1]]

    main(config, args, layouts)