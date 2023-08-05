from pathlib import Path

import matplotlib
from matplotlib import font_manager
from distutils.version import LooseVersion


def init_matplotlib(weight='medium'):
    """
    Initialize matplotlib settings.
    :param weight: you can choose one weight from 'thin', 'light', 'regular', 'medium', 'bold', 'black'.
                   default is 'medium'
    :return:
    """
    FONTS_DIR = 'fonts'
    FONT_NAME = 'Noto Sans CJK JP'
    FONT_WEIGHT = weight

    font_settings = {
        'family': FONT_NAME,
        'weight': FONT_WEIGHT
    }

    font_dir_path = Path(__file__).parent.resolve() / Path(FONTS_DIR)
    font_dirs = [font_dir_path, ]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

    is_support_createFontList = LooseVersion(matplotlib.__version__) < '3.2'
    if is_support_createFontList:
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)
    else:
        for fpath in font_files:
            font_manager.fontManager.addfont(fpath)
    matplotlib.rc('font', **font_settings)
