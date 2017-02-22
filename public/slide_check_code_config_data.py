#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

"""
    slide_check_code_config_data.py
    ~~~~~~~~~

    配合 slide_check_code_recognition.py 的配置数据

    :copyright: (c) 2016 by LEI Li.
    :license: MIT, see LICENSE for more details.
"""

__versions__ = '0.0.2'


REBUILD_ORDER = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28,
                 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22,
                 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4,
                 5, 19, 18, 16, 17]
IMG_DIST_DICT = {
    (0, 12): 158 - 6,
    (0, 264): 143 - 6,
    (1, 15): 184 - 6,
    (1, 295): 168 - 6,
    (2, 117): 134 - 6,
    (2, 89): 143 - 6,
    (3, 124): 162 - 6,
    (3, 220): 178 - 6,
    (4, 225): 46 - 6,
    (4, 73): 87 - 6,
    (5, 171): 112 - 6,
    (5, 40): 45 - 6,
}
TRACK_MOVEMENT_DICT = {
    53: (691, 'D,0/11.0(!!9t)(!)()(!)vzsvz(!!($/K6?9IJ7D99A:9Z'),
    96: (917, 'D./00.10.0//.(!!9t)!)()(!)(()(((tu~ttust~su~s(!!($/K3418AB1FK@I@F9A@A:?A98:@9Z'),
    85: (919, 'D-11.0/././.-(!!9t)((((((!)((()uvzsvu~z~s(!!($/KD4@BIJBJDJ7DA@?A@@?8:@Z'),
    145: (1146, 'D..0.0.0/.1000./...-(!!9t)(((!)()((!))!))!))((!)~z)z~uvssztvutvszttvu~(!!($/K@641922722EFCKB:43CCFA@A@8A89:9:9@AA99?9Z'),
    138: (1142, 'D/..1001.1100./.1-(!!9t)!))!))!)()(!))(!))!))!)s~tsutttsvzssvzvtus(!!($/KB4IC22HGFAJ1B:AAF98?A@@A::@@8989@A@AZ'),
    121: (1107,
          'D./101.0.1.0/00-(!!9t(()!))(!)(()!)(((t(tvtssstsusstvutsss(!!($/K1:@5E3GDBKCE8HBE9@A@A899@?9@?8AA9:Z'),
    122: (1107, 'D./101.0.1.0/00-(!!9t(()!))(!)(()!)(((t(tvtssstsusstvutsss(!!($/K1:@5E3GDBKCE8HBE9@A@A899@?9@?8AA9:Z'),
    42: (688, 'D-10./(!!9t)!))!)(y~stus(!!($/KG7DFBC@@:@?Z'),
    109: (984, 'D/.0/.10101//0(!!9t()(!)()(!))!)()!)sss~u~ussttsttv(!!($/KH7IGB6@866C7K@?8A8:?@:::?@:?Z'),
    73: (772, 'D///01/./0(!!9t(((()!)()!)tttvzttv(!!($/KD2G7JD19H9988@8@:Z'),
    95: (933, 'D//////100/..(!!9t)(!))(!))(!)()!)tvtsstzvz~tu(!!($/KIJ8K7J4:4FJ4@A@?@8A:?A?9Z'),
    83: (820, 'D/.10//./.1,(!!9t()(!)()(((!)~!)t~ttzt~(!!($/K@CA24HCK88E??:@@@98Z'),
    74: (830, 'D./1.0111,(!!9t((()!)(((~!)vttsu~ssu(!!($/KGH4G8KB4B??8::@?A?:Z'),
    48: (626, 'D//0/10(!!9t()!))(!)s~ut(!!($/K29I:42A@:8Z'),
    60: (724, 'D01011/(!!9ty()!))!)(vsz~ssts(!!($/K:C@3G51?@@8??@@Z'),
    65: (758, 'D-/./111/(!!9t)(!))!))((utvztstv(!!($/KF98AH1B@89@@?:@@Z'),
    125: (1032, 'D..01.11//..1/./-,(!!9t(()(!))!))!)(()(!))!))utvttsztsvz~stu(!!($/K478784:HF23I7CDCE99:99?98AAAA@@?Z'),
    46: (693, 'D1//0.(!!9ty)!)()!)~zvszs(!!($/KJC3H?8:@:A9?Z'),
    153: (1263,
          'D./01.101/.00/00/1,(!!9ty)!))!))(!)((()((!))!)()zvuttss~suvtzsvsstuvutss(!!($/K@7D63CAGF7C?IDA@@GC?8:@989??A??8:?::A9:8A@9Z'),
    137: (1109,
          'D-1010.0/..101.1.,(!!9t(((((()(((((!))!))t!)ss~ustvzt~zttt~uv(!!($/KE5963KCBB5@FG8JACA8:99889A9:8A:??@:Z'),
    112: (1014,
          'D-001/.0./0/0/.(!!9t)!))!))!))(!)()!)((~zsvustvzvstzvtsu(!!($/KE@6@B9B3G@K?3::A::A:8@8::8898?9Z'),
    130: (1067,
          'D.11/010.//1/1/.(!!9t)(!))((!))(!)(()!)(ttstt~sz~tz~tsz~(!!($/K93J?FD@56JI3CIDCA?9AAAA:98@AA9?Z'),
    174: (1271,
          'D-/1//.00.1./11.0./.1.-(!!9t)(((!))((!)(()!)()!)()!)((t)tsu~zts~szttvtuvsusvztts(!!($/K::CAA::6533?@43?6DB7DC8:?A?8@?9A?:::9@@898AA???Z'),
    126: (1044,
          'D..011////.11.11(!!9t()!)((((((()!))!)(~tszvu~sutvtssz~s(!!($/K5EB8A@AD45F:KC199:?A9?@9?A:A?8:@Z'),
    35: (639, 'D-100(!!9t()((zsssss(!!($/K@5?7A@A9??Z'),
    200: (1426,
          'D,110000.00..01/..00.110,-(!!9t)!)()(!))!)((()(!))!)(()((!))!)~y!)s~uvtssuvzstvut~ztstssst~u(!!($/KG2K2K1H69JKB5?3F9KJE3239?8@A889?:@9@@?:@:8A8A8A9A::8:Z'),
    37: (679, 'D-..//(!!9t((()!)tvzvsz(!!($/KB84KKE?:8:9Z'),
    143: (1188,
          'D,..1.0///00//.0.10-(!!9t)!)()!)()((!))(!))(!))((tus~utvzt~suvtuvzvus(!!($/K5DJC43GI8A1@CBIB4A:9A???:@@?@@9@8:9:A@AZ'),
    45: (673, 'D//../0(!!9t)((!))!)tvu~ss(!!($/K2G288K:::?9@Z'),
}
