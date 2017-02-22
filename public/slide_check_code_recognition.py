#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import pdb

"""
    slide_check_code_recognition.py
    ~~~~~~~~~

        通过模拟滑块验证码操作，得到最终加密结果。对于 offline，直接通过图片与距离字典得到距
    离作为参数传入函数。对于 online，通过处理实时图片得到距离并模拟滑动轨迹。
        1). 以为企业信用（云南）为例，offline 使用流程如下（* 部分为滑块验证码验证流程以外的
    业务流程）：
        * 1. challenge = fetch_challenge()  # 得到滑块验证码的参数 challenge
        2. POST_data = get_validate_data_based_offline(challenge)  # 传入
                                                                     challenge
                                                                     得到 data
        * 3. validation(POST_data)  # 将 post_data 作为 POST 参数在服务器端认证

        2). 以为企业信用（广西）为例，online 使用流程如下（* 部分为滑块验证码验证流程以外的
    业务流程）：
        * 1. gt, challenge(32) = fetch_init_params()  # 得到滑块验证码的参数 gt,
                                                        challenge
        * 2. img1_url, img2_url, challenge = fetch_params(gt, challenge(32))
        # 得到滑块验证码的参数 challenge, 两张图片网址
        3. GET_params = get_validate_data_based_online(img1_url, img2_url,
                                                       challenge)  # 得到 param
        * 4. validate = fetch_validate(GET_params)  # 将 GET_params 作为 GET 参数
                                                      得到 validate
        * 5. validation(POST_data)  # 将 validate 组合成为 POST_data 作为 POST 参
                                      数在服务器端认证
    :copyright: (c) 2016 by LEI Li.
    :license: MIT, see LICENSE for more details.
"""

__versions__ = '0.0.2'

import hashlib
import random
import time
import matplotlib.pyplot as plt
import numpy as np

from skimage import io
from slide_check_code_config_data import (REBUILD_ORDER, IMG_DIST_DICT,
                                          TRACK_MOVEMENT_DICT)


def c_getx_function(a):
    """改写自 offline.5.6.1.js 同名函数 ——> c.getX(a)

    :param a: 字符串
    :return: 单整型数
    """
    if 5 == len(str(a)):
        b = 200
        c = int(str(a), 16) if int(str(a), 16) else 0
        d = c % b
        return 40 if d < 40 else d


def c_gety_function(a):
    """改写自 offline.5.6.1.js 同名函数 ——> c.getY(a)

    :param a: 字符串
    :return: 单整型数
    """
    if 4 == len(str(a)):
        b = 70
        c = int(str(a), 16) if int(str(a), 16) else 0
        return c % b


def c_h_function_branch(f, g):
    """改写自 offline.5.6.1.js 同名函数 ——> c.h()

    :param f: md5(图片背景类型)
    :param g: md5(图片差异值)
    :return: 滑块移动距离
    """
    h = ''
    i = 0
    while i < 9:
        h += f[i] if i % 2 == 0 else g[i]
        i += 1
    j = h[:4]
    k = h[4:]
    l = c_getx_function(k)
    m = c_gety_function(j)
    return l


def c_h_function(d=int(6 * random.random()), e=int(300 * random.random())):
    """改写自 offline.5.6.1.js 同名函数 ——> c.h()

    :param d: 图片背景类型
    :param e: 图片差异值
    :return: d，e 为验证所使用参数，check_code_url 为验证码 bg 图
    """
    md1 = hashlib.md5()
    md1.update('{}'.format(d).encode('utf-8'))
    f = md1.hexdigest()[0:9]
    md2 = hashlib.md5()
    md2.update('{}'.format(e).encode('utf-8'))
    g = md2.hexdigest()[10:19]
    l = c_h_function_branch(f, g)
    return f, g, l


def ba_t_function(a, b):
    """改写 geetest.5.6.1.js 同名函数 ——> ba.t(a, b)

    :param a: 滑块距离
    :param b: 验证码给定参数
    :return: 加密后的字符串
    """
    c = b[32:]
    d = list()
    e = 0
    while e < len(c):
        f = ord(c[e])
        d.append(f - 87 if f > 57 else f - 48)
        e += 1
    c = 36 * d[0] + d[1]
    g = round(a) + c
    b = b[:32]
    i = [[], [], [], [], []]
    j = {}
    k = 0
    e = 0
    l = len(b)
    while e < l:
        h = b[e]
        if h not in j:
            j[h] = 1
            i[k].append(h)
            k += 1
            k = 0 if k == 5 else k
        e += 1
    n = g
    o = 4
    p = ''
    q = [1, 2, 5, 10, 50]
    while n > 0:
        if n - q[o] >= 0:
            m = int(random.random() * len(i[o]))
            p += i[o][m]
            n -= q[o]
        else:
            del i[o]
            del q[o]
            o -= 1
    return p


def get_user_response(distance, challenge):
    """同 ba_t_function()

    :param distance: 同 ba_t_function()
    :param challenge: 同 ba_t_function()
    :return: 同 ba_t_function()
    """
    return ba_t_function(distance, challenge)


def na_c_function(a):
    """改写 geetest.5.6.1.js 同名函数 ——> na.c(a)

    :param a: 二维数组
    :return: 处理后的数组
    """
    e = []
    f = 0
    g = []
    h = 0
    i = len(a) - 1
    while h < i:
        b = int(round(a[h + 1][0] - a[h][0]))
        c = int(round(a[h + 1][1] - a[h][1]))
        d = int(round(a[h + 1][2] - a[h][2]))
        g.append([b, c, d])
        if not (0 == b and 0 == c and 0 == d):
            if 0 == b and 0 == c:
                f += d
            else:
                e.append([b, c, d + f])
                f = 0
        h += 1
    if (type(0) != type(f)) or 0 != f:
        e.append([b, c, f])
    return e


def na_d_function(a):
    """改写 geetest.5.6.1.js 同名函数 ——> na.d(a)

    :param a: 单整型数
    :return: 单字符串
    """
    b = '()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqr'
    c = len(b)
    d = ''
    e = abs(a)
    f = int(e/c)
    if f >= c:
        f = c - 1
    if f:
        d = b[f]
        e %= c
    g = ''
    if a < 0:
        g += '!'
    if d:
        g += '$'
    return g + d + b[e]


def na_e_function(a):
    """改写 geetest.5.6.1.js 同名函数 ——> na.e(a)

    :param a: 一维数组
    :return: 处理后的数组
    """
    b = [[1, 0], [2, 0], [1, -1], [1, 1], [0, 1], [0, -1], [3, 0], [2, -1],
         [2, 1]]
    c = 'stuvwxyz~'
    d = 0
    e = len(b)
    while d < e:
        if a[0] == b[d][0] and a[1] == b[d][1]:
            return c[d]
        d += 1
    return 0


def na_f_function(a):
    """改写 geetest.5.6.1.js 同名函数 ——> na.f(a)

    :param a: 滑块移动轨迹的二维数组
    :return: 处理后的数组
    """
    f = na_c_function(a)
    g = []
    h = []
    i = []
    j = 0
    k = len(f)
    while j < k:
        b = na_e_function(f[j])
        if b:
            h.append(b)
        else:
            g.append(na_d_function(f[j][0]))
            h.append(na_d_function(f[j][1]))
        i.append(na_d_function(f[j][2]))
        j += 1
    return ''.join(g) + '!!' + ''.join(h) + '!!' + ''.join(i)


def break_image_to_chunk(img):
    """将原始图片切割为 52 块

    :param img: 原始验证码图片
    :return: 切割后的图片列表
    """
    img = io.imread(img)
    row_list = list()
    column_list = list()
    for i in range(1, 312, 12):
        row_list.append(img[0:58, i:i + 10, :])
        column_list.append(img[58:116, i:i + 10, :])
    return row_list + column_list


def rebuild_image(img_list):
    """将切割后的图片按新规则重组

    :param img_list: 切割后的图片列表
    :return: 重组后的验证码图片
    """
    rebuild_img = np.zeros(shape=(116, 260, 3), dtype=np.uint8)
    for i, j in enumerate(range(0, 260, 10)):
        rebuild_img[0:58, j:j + 10, :] = img_list[REBUILD_ORDER[i]]
        rebuild_img[58:116, j:j + 10, 0:3] = img_list[REBUILD_ORDER[i + 26]]
    return rebuild_img


def restore_image(img):
    """将原始验证码重组为正常图序的验证码

    :param img: 原始验证码图片
    :return: 重组后的验证码图片
    """
    img_list = break_image_to_chunk(img)
    return rebuild_image(img_list)


def image_transform_distance(source_img, chunk_img):
    """计算滑块滑动的距离

    :param source_img: 重组后未切割的验证码图片
    :param chunk_img: 重组后已切割的验证码图片
    :return: 滑块滑动的距离
    """
    # plt.subplot(121)
    # plt.imshow(source_img, plt.cm.gray)
    # plt.subplot(122)
    # plt.imshow(chunk_img, plt.cm.gray)
    # plt.show()
    for i in range(0, 260):
        if not (source_img[:, i, :] == chunk_img[:, i, :]).all():
            diff = (abs(source_img[:, i, :].astype(int) - chunk_img[:, i, :]
                        .astype(int)).max())
            if diff > 50:
                # return i if i >= 46 else 46
                return i
    return None


def raw_image_transform_distance(raw_source_img, raw_chunk_img):
    """计算原始验证码的滑动距离

    :param raw_source_img: 原始未切割的验证码图片
    :param raw_chunk_img: 原始已切割的验证码图片
    :return: 滑块滑动的距离
    """

    img_dist = image_transform_distance(restore_image(raw_source_img),
                                        restore_image(raw_chunk_img))
    # 计算出的距离与实际距离相差 6
    return img_dist - 6 if img_dist else img_dist


def get_slide_track_list(img_distance):
    """模拟得到滑块轨迹数组

    :param img_distance: 滑块移动距离
    :return: 滑块轨迹数组
    """
    # TODO: 迭代
    slide_track_list = [[-23, -16, 0], [0, 0, 0], [2, 0, 420]]
    x_distance = 0
    time_step = 420
    while True:
        x_distance += random.randint(8, 50)
        time_step += random.randint(8, 30)
        y_axis_step = random.randint(0, 1)
        if x_distance >= img_distance:
            slide_track_list.append([img_distance, y_axis_step, time_step])
            slide_track_list.append(list(np.array(slide_track_list[-1]) +
                                         [0, 0, 45]))
            break
        slide_track_list.append([x_distance, y_axis_step, time_step])
    return slide_track_list


def track_encryption(slide_track_list):
    """对滑块轨迹进行加密

    :param slide_track_list: 滑块轨迹列表
    :return: 加密后的字符串
    """
    return na_f_function(slide_track_list)


def get_validate_data_based_online(challenge, gt, raw_source_img,
                                   raw_chunk_img, show=False):

    """在线验证（需要实时计算滑块验证码的距离）

    :param challenge: 验证码给定参数
    :param gt: 验证码给定参数
    :param raw_source_img: 原始未切割的验证码图片
    :param raw_chunk_img: 原始已切割的验证码图片
    :param show: 是否展示图片，默认为否
    :return: validate POST 参数字典 (发生错误返回 None)
    """

    img_dist = raw_image_transform_distance(raw_source_img, raw_chunk_img)
    if not img_dist:
        return None
    if show:
        plt.subplot(121)
        plt.title('Source Image')
        plt.imshow(restore_image(raw_source_img), plt.cm.gray)

        plt.subplot(122)
        plt.title('Chunk Image')
        plt.imshow(restore_image(raw_chunk_img), plt.cm.gray)
        plt.show()
    if img_dist in TRACK_MOVEMENT_DICT:
        pass_time = TRACK_MOVEMENT_DICT[img_dist][0]
        a = TRACK_MOVEMENT_DICT[img_dist][1]
    else:
        track_list = get_slide_track_list(img_dist)
        pass_time = track_list[-1][2]
        a = track_encryption(track_list)
    user_resp = get_user_response(img_dist, challenge)
    time_stamp = int(time.time() * 1000)
    payload = {
        'gt': gt,
        'challenge': challenge,
        'userresponse': user_resp,
        'passtime': pass_time,
        'imgload': random.randint(80, 181),
        'a': a,
        'callback': 'geetest_{}'.format(time_stamp)
    }
    return payload


def get_validate_data_based_offline(challenge):
    """离线验证（不需要实时计算滑块验证码的距离，利用已有距离字典得到）

    :param challenge: 验证码给定参数
    :return: validate POST 参数字典
    """
    param_key = list(IMG_DIST_DICT.keys())[random.randint(0, 11)]
    user_resp = IMG_DIST_DICT[param_key]
    param_d = param_key[0]
    param_e = param_key[1]
    validate = (get_user_response(user_resp, challenge) + '_' +
                get_user_response(param_d, challenge) + '_' +
                get_user_response(param_e, challenge))
    seccode = validate + '|jordan'
    data = dict(geetest_challenge=challenge, geetest_validate=validate,
                geetest_seccode=seccode)
    return data


if __name__ == '__main__':
    # offline 测试
    challenge = 'd1e4d10768d54a0c85ee397df94ff684bf'
    # print challenge
    # print(get_validate_data_based_offline(challenge))

    # online 测试
    # challenge = ''
    # gt = ''
    # raw_source_img = 'a.jpg'
    # raw_chunk_img = 'b.jpg'
    # print(get_validate_data_based_online(challenge, gt, raw_source_img,
    #                                      raw_chunk_img))

