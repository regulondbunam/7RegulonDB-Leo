import html
import  os
import re

def find_html_files(input_path):
    """
    inputh
    :param input_path:
    :return:
    """
    dir_list = os.listdir(input_path)
    html_file_list = []

    for dir_name in dir_list:
        dir_list2 = os.listdir(input_path + "/" + dir_name)

        for dir_name2 in dir_list2:
            dir_list3 = os.listdir(input_path + "/" + dir_name + "/" + dir_name2)
            for dir_name3 in dir_list3:
                if os.path.isdir(input_path + "/" + dir_name + "/" + dir_name2 + "/" + dir_name3):
                    dir_list4 = os.listdir(input_path + "/" + dir_name + "/" + dir_name2 + "/" + dir_name3)
                    for file_name in dir_list4:
                        if re.match(".+.html", file_name):
                            html_file = input_path + "/" + dir_name + "/" + dir_name2 + "/" + dir_name3 + "/" + file_name
                            html_file_list.append(html_file)

    return html_file_list