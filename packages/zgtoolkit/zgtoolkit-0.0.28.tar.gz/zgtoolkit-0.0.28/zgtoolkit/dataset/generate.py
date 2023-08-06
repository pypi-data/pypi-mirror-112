from pathlib import Path
import numpy as np
from shutil import rmtree, copy
from glob import glob
import os
import random
from typing import Union

from ..utils import track_iter_progress
from .parse import parse_label


def write_oneline(path, annofile, label_suffix, classes, is_need_dataprefix):
    path = Path(path)
    img_path = path if is_need_dataprefix else Path(path).name

    base_name = path.parent
    stem = path.stem
    annofile.write(str(img_path))

    if label_suffix is None:
        index = [i for i, x in enumerate(classes) if x in stem]
        assert len(index) == 1
        annofile.write(' ')
        annofile.write(str(index[0]))
        annofile.write('\n')
    elif 'xml' in label_suffix:
        anno_path = base_name / Path(stem + label_suffix)
        objs = parse_label(anno_path, label_suffix, classes)

        for obj in objs:
            annofile.write(' ')
            annofile.write(','.join([str(x) for x in obj]))
        annofile.write('\n')


def generate_annotxt(txt_path, root: Union[list, str], label_suffix, classes, image_format='jpg',
                     is_need_dataprefix=False):
    anno_txt = open('anno/train.txt', 'w', encoding='utf-8')

    if not isinstance(root, list):
        root = [root]
    image_paths = [glob(os.path.join(x, f'*.{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    random.shuffle(image_paths)

    for image_path in track_iter_progress(image_paths):
        write_oneline(image_path, anno_txt, label_suffix, classes, is_need_dataprefix)

    anno_txt.close()


def generate_annofile(root: Union[list, str], label_suffix, classes, image_format='jpg', is_need_dataprefix=False):
    if Path('anno').exists():
        rmtree('anno')
    os.mkdir('anno')

    train_anno = open('anno/train.txt', 'w', encoding='utf-8')
    test_anno = open('anno/test.txt', 'w', encoding='utf-8')

    if not isinstance(root, list):
        root = [root]
    image_paths = [glob(os.path.join(x, f'*.{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    random.shuffle(image_paths)

    total = len(image_paths)
    default_train = int(len(image_paths) * 0.8)
    default_test = total - default_train
    print(f'total: {total}, default_train: {default_train}, '
          f'default_test: {default_test}')
    test_num = input('input test_num:')
    if test_num is '':
        test_num = default_test

    test_image_paths = random.sample(image_paths, int(test_num))
    train_image_paths = list(set(image_paths) - set(test_image_paths))

    for train_image_path in track_iter_progress(train_image_paths):
        write_oneline(train_image_path, train_anno, label_suffix, classes, is_need_dataprefix)

    for test_image_path in track_iter_progress(test_image_paths):
        write_oneline(test_image_path, test_anno, label_suffix, classes, is_need_dataprefix)

    train_anno.close()
    test_anno.close()


def generate_annodataset(root: str, label_suffix, classes, image_format='jpg', is_need_dataprefix=False):
    if Path('anno').exists():
        rmtree('anno')
    os.mkdir('anno')

    train_anno = open('anno/train.txt', 'w', encoding='utf-8')
    test_anno = open('anno/test.txt', 'w', encoding='utf-8')

    train_image_paths = list(Path(Path(root) / 'train').glob('*.jpg'))
    test_image_paths = list(Path(Path(root) / 'test').glob('*.jpg'))

    for train_image_path in track_iter_progress(train_image_paths):
        write_oneline(train_image_path, train_anno, label_suffix, classes, is_need_dataprefix)

    for test_image_path in track_iter_progress(test_image_paths):
        write_oneline(test_image_path, test_anno, label_suffix, classes, is_need_dataprefix)

    train_anno.close()
    test_anno.close()


def generate_train_test_dataset(root: Union[list, str], dataset_path, label_suffix, image_format='.jpg'):
    assert '.' in label_suffix and '.' in image_format

    if not Path(dataset_path).exists():
        os.mkdir(dataset_path)
        os.mkdir(Path(dataset_path) / 'train')
        os.mkdir(Path(dataset_path) / 'test')

    if not isinstance(root, list):
        root = [root]
    image_paths = [glob(os.path.join(x, f'*{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    random.shuffle(image_paths)

    total = len(image_paths)
    default_train = int(len(image_paths) * 0.8)
    default_test = total - default_train
    print(f'total: {total}, default_train: {default_train}, '
          f'default_test: {default_test}')
    test_num = input('input test_num:')
    if test_num is '':
        test_num = default_test

    test_image_paths = random.sample(image_paths, int(test_num))
    train_image_paths = list(set(image_paths) - set(test_image_paths))
    train_anno = open(Path(dataset_path) / 'train.txt', 'w', encoding='utf-8')
    test_anno = open(Path(dataset_path) / 'test.txt', 'w', encoding='utf-8')

    for train_image_path in track_iter_progress(train_image_paths):
        src_path = train_image_path
        dst_path = Path(dataset_path) / 'train' / Path(src_path).name
        copy(src_path, dst_path)
        copy(Path(src_path).with_suffix(label_suffix), dst_path.with_suffix(label_suffix))

        train_anno.write(Path(src_path).name + '\n')

    for test_image_path in track_iter_progress(test_image_paths):
        src_path = test_image_path
        dst_path = Path(dataset_path) / 'test' / Path(src_path).name
        copy(src_path, dst_path)
        copy(Path(src_path).with_suffix(label_suffix), dst_path.with_suffix(label_suffix))

        test_anno.write(Path(src_path).name + '\n')

    train_anno.close()
    test_anno.close()
