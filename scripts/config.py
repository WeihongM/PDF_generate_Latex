from easydict import EasyDict as edict

C = edict()
config = C
cfg = C

C.prefix = './output/'                  # dir to save output result

# font setting
C.fontSizeMin = 10                      # default:font_size=10
C.fontSizeMax = 12                      # default:font_size=10
C.fontHorizonCoeff = 0.5                # 'actual font size horizontally (e.g. font_size*0.5)'
C.fontVerticalCoeff = 1.1               # 'actual font size vertically (e.g. font_size*1.1)'
C.marginMin = 0.50                      # 'min margin (inches)'
C.marginMax = 1.25                      # 'max margin (inches)'
C.paraSkipRatio = 1.0                   # 'paragraph skipping ratio'

# img setting
C.imgWidthMinRatio = 0.7                # 'min img width (ratio\\textwidth)'
C.imgWidthMaxRatio = 1.0                # 'max img width (ratio\\textwidth)'
C.imgHeightMaxRatio = 0.5               # 'max img height (ratio\\textwidth)'

# list setting
C.listType = ['itemize', 'enumerate']   # 'list type'
C.itemNumberMax = 5                     # 'max number of items'
C.itemLengthMin = 10                    # 'min chars in item'
C.itemLengthMax = 200                   # 'max chars in item'

# text setting
C.textMaxLine = 70                      # 'max number of lines of text'

# borderline setting
C.colors = ['black', 'red', 'blue', 'green', 'cyan', 'magenta', 'yellow']   # 'colors supported in latex'
C.hasColors = 0.2                       # 'probability to have color'
C.hasHorizonBorder = 0.5                # 'prob of having border line'
C.hasVerticalBorder = 0.1               # 'prob of having border line'
C.borderLineMaxWidth = 8                # 'prob of having border line'

# other setting
C.inches2Pt = 72.27                     # 1 in = 72.27 pt
C.pageWidth = 8.3                       # 'page width (inches)'
C.pageHeight = 11.7                     # 'page height (inches)'

C.maxNumElements = 100                  

# distribution
C.distribution = {'figure': 0.45, 'table': 0.55, 'section': 0., 'list': 0.65, 'text': 0.98, 'line': 1.00}