import re
import seaborn as sns
import urllib.request as req
from IPython.core.display import HTML


current_theme = 'gray_area'

dynamic_colors_list = None


def load_css(theme=None, color_list=None):
    """
    Four themes available right now: 'cyan_sisters', 'dark_matter', 'genus_lavandula' and 'gray_area'.
    If you want your own color pallete use 'dynamic_colors' theme and pass list of 3 Hexcodes as a second parameter.
    [Background Color, Font & Border Color, Hover Color]
    """
    global current_theme

    response_main = req.urlopen(
        'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/main.css')

    if theme == 'dynamic_colors':
        if (color_list is not None) and (len(color_list) == 3):
            for color in color_list:
                match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
                if not match:
                    raise Exception(f"'{color}' is Invalid Color Code. Please Enter Hexcodes only.")

            current_theme = 'dynamic_colors'

            response_theme = req.urlopen(
                'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/dynamic_colors.css')

            response_theme_string = response_theme.read().decode('utf-8')
            response_theme_string = response_theme_string.replace('[#COLOR_ONE#]', color_list[0])
            response_theme_string = response_theme_string.replace('[#COLOR_TWO#]', color_list[1])
            response_theme_string = response_theme_string.replace('[#COLOR_THREE#]', color_list[2])

            global dynamic_colors_list
            dynamic_colors_list = color_list

            return HTML('<style>' + response_main.read().decode('utf-8') +
                        response_theme_string + '</style>')
        else:
            if color_list:
                raise Exception(f"When 'dynamic_colors' theme is selected the function excepts a color_list of length "
                                f"3. But got {len(color_list)}.")
            else:
                raise Exception(f"When 'dynamic_colors' theme is selected the function excepts a color_list of length "
                                f"3. But got None Instead.")
    elif theme == 'cyan_sisters':
        current_theme = 'cyan_sisters'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/cyan_sisters.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    elif theme == 'dark_matter':
        current_theme = 'dark_matter'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/dark_matter.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    elif theme == 'genus_lavandula':
        current_theme = 'genus_lavandula'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/genus_lavandula.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    else:
        current_theme = 'gray_area'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/gray_area.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')


def get_color_palette():
    if current_theme == 'cyan_sisters':
        return sns.color_palette(['#39ace7', '#0784b5'])
    elif current_theme == 'dark_matter':
        return sns.color_palette(['#757575', '#212121'])
    elif current_theme == 'genus_lavandula':
        return sns.color_palette(['#a176c6', '#8653af'])
    elif (current_theme == 'dynamic_colors') and dynamic_colors_list and len(dynamic_colors_list) == 3:
        return sns.color_palette([dynamic_colors_list[1], dynamic_colors_list[2]])
    else:
        return sns.color_palette(['#78909C', '#37474F'])


def get_background_color():
    if current_theme == 'cyan_sisters':
        return '#cadeef'
    elif current_theme == 'dark_matter':
        return '#e0e0e0'
    elif current_theme == 'genus_lavandula':
        return '#e9d5eb'
    elif (current_theme == 'dynamic_colors') and dynamic_colors_list and len(dynamic_colors_list) == 3:
        return dynamic_colors_list[0]
    else:
        return '#CFD8DC'


def get_font_color():
    global dynamic_colors_list
    if current_theme == 'cyan_sisters':
        return '#39ace7'
    elif current_theme == 'dark_matter':
        return '#757575'
    elif current_theme == 'genus_lavandula':
        return '#a176c6'
    elif (current_theme == 'dynamic_colors') and dynamic_colors_list and len(dynamic_colors_list) == 3:
        return dynamic_colors_list[1]
    else:
        return '#78909C'


def get_font_dict(fontsize=14, fontweight='light', font_color=None):
    if font_color is None:
        font_color = get_font_color()
    return {
                'fontsize': fontsize,
                'fontweight': fontweight,
                'fontfamily': 'serif',
                'horizontalalignment': 'center',
                'color': font_color
            }
