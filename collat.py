import os
import argparse
import shutil
import voc2yolo_tree
# 指定文件夹路径
path = ''
path_list = ['/annotation','/JPEGImages','/labels','/test']

def save_file(source_file,destination_file):
    shutil.copyfile(source_file, destination_file)
# 使用os.mkdir()方法创建文件夹
def makedir(path):
    if not os.path.exists(path):
        # 如果文件夹不存在，则创建文件夹
        os.mkdir(path)

def make_dir(path):
    ALL_path = path + '/ALL'
    makedir(ALL_path)
    for p in path_list:
        path_name = ALL_path + p
        makedir(path_name)
        if p != '/test':
            path_name_T =path_name + '/TEST'
            makedir(path_name_T)
import os

def search_dirty(directory,lables_path,class_name,val_path):
    path_list_1 = []
    # 遍历目录中的所有文件和子目录
    # print(directory)
    # 遍历源文件夹中的所有文件和文件夹
    for item in os.listdir(directory):
        # 构建源文件/文件夹的完整路径
        file_path = os.path.join(directory, item)
        if os.path.isfile(file_path):
            if file_path.endswith('.xml'):
                # 打开文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 逐行读取文件内容
                    n_label = 0

                    for line in file:
                        for c in class_name:
                            if c in line:
                                n_label = n_label + 1
                    if n_label > 0:
                        #保存xml
                        path_1 = file_path.split('/xml')[1]
                        save_path = path + '/ALL/annotation/TEST' + path_1
                        destination_folder = os.path.dirname(save_path)
                        os.makedirs(destination_folder, exist_ok=True)
                        save_file(file_path,save_path)
                        with open(lables_path, 'a') as file:
                            # 不断写入新数据，这里假设有一个数据源 data_source
                            # 如果你有实时数据，可以根据实际情况进行写入
                            new_data = save_path
                            if new_data.lower() == 'exit':
                                break
                            else:
                                file.write(new_data + '\n')

                        #保存图片
                        try:
                            path_11 = path_1.replace('.xml','.jpg')
                            img_path = path + path_11
                            save_img_path = path + '/ALL/JPEGImages/TEST' + path_11
                            destination_folder_img = os.path.dirname(save_img_path)
                            os.makedirs(destination_folder_img, exist_ok=True)
                            save_file(img_path,save_img_path)
                        except:
                            path_11 = path_1.replace('.xml', '.png')
                            img_path = path + path_11
                            save_img_path = path + '/ALL/JPEGImages/TEST' + path_11
                            destination_folder_img = os.path.dirname(save_img_path)
                            os.makedirs(destination_folder_img, exist_ok=True)
                            save_file(img_path, save_img_path)
                        with open(val_path, 'a') as file:
                            # 不断写入新数据，这里假设有一个数据源 data_source
                            # 如果你有实时数据，可以根据实际情况进行写入
                            new_data = save_img_path
                            if new_data.lower() == 'exit':
                                break
                            else:
                                file.write(new_data + '\n')



            pass
        # 如果是文件夹，则递归调用函数处理子文件夹
        elif os.path.isdir(file_path):
            search_dirty(file_path,lables_path,class_name,val_path)
def path_name(path_new):
    # 使用 global 关键字声明变量为全局变量
    global path
    path = path_new


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", "--path", type=str, help="输入路径", default="/home/spring/mnt/sda3/JPEGImages/TRAIN/18_rubby")
    class_name = ['bed','chair','couch','desk']

    args = parser.parse_args()
    path_name(args.path)
    make_dir(path)
    class_path = path + '/ALL/test/classes.names'
    val_images_path = path + '/ALL/test/val_images.txt'
    with open(class_path, 'w') as file:
        for cn in class_name:
            file.write(cn + '\n')

    with open(val_images_path, 'w') as file:
        # 可以选择在这里写入初始数据，如果不需要，可以留空
        pass
    lables_path = path + '/labels.txt'

    with open(lables_path, 'w') as file:
        # 可以选择在这里写入初始数据，如果不需要，可以留空
        pass

    search_dirty(path+'/xml',lables_path,class_name,val_images_path)
    voc2yolo_tree.voc2yolox(lables_path,classes=class_name)