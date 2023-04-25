import numpy
import pandas as pd

def pd_date(sts):
    return pd.DataFrame(sts,dtype=float)

def get_wci(item):

    d = 1  # 时间 单位天
    n = float(item['publish_num_change'])  # 发文数
    if n == 0:
        return 0.00
    R = float(item['read_num'])  # 阅读数
    Z = float(item['look_num'])  # 在看数
    L = float(item['likes_num'])  # 点赞数
    Rt = float(item['top_read_num'])  # 头条阅读数
    Zt = float(item['top_look_num'])  # 头条在看数
    Lt = float(item['top_likes_num'])  # 头条点赞数
    Rmax = float(item['max_read_num'])  # 最高阅读数
    Zmax = float(item['max_look_num'])  # 最高在看数
    Lmax = float(item['max_likes_num'])  # 最高点赞数
    # 整体传播力

    O = 0.85 * numpy.log(R / d + 1) + 0.09 * numpy.log(Z / d * 10 + 1) + 0.06 * numpy.log(L / d * 10 + 1)
    # 篇均传播力
    A = 0.85 * numpy.log(R / n + 1) + 0.09 * numpy.log(Z / n * 10 + 1) + 0.06 * numpy.log(L / n * 10 + 1)
    # 头条传播力
    H = 0.85 * numpy.log(Rt / d + 1) + 0.09 * numpy.log(Zt / d * 10 + 1) + 0.06 * numpy.log(Lt / d * 10 + 1)
    # 峰值传播力
    P = 0.85 * numpy.log(Rmax + 1) + 0.09 * numpy.log(Zmax * 10 + 1) + 0.06 * numpy.log(Lmax * 10 + 1)
    WCI = O * 0.6 + A * 0.2 + H * 0.1 + P * 0.1
    return float(numpy.log10(WCI*WCI*12))

def get_wci_ph(item):

    d = 1  # 时间 单位天
    n = float(1)  # 发文数
    R = float(item['read_count'])  # 阅读数
    Z = float(item['looking_count'])  # 在看数
    L = float(item['good_count'])  # 点赞数
    if item['is_top'] == 1:
        Rt = float(item['read_count'])  # 头条阅读数
        Zt = float(item['looking_count'])  # 头条在看数
        Lt = float(item['good_count'])  # 头条点赞数
        Rmax = float(item['read_count'])  # 最高阅读数
        Zmax = float(item['looking_count'])  # 最高在看数
        Lmax = float(item['good_count'])  # 最高点赞数
    else:
        Rt = float(0)  # 头条阅读数
        Zt = float(0)  # 头条在看数
        Lt = float(0)  # 头条点赞数
        Rmax = float(0)  # 最高阅读数
        Zmax = float(0)  # 最高在看数
        Lmax = float(0)  # 最高点赞数
    # 整体传播力

    O = 0.85 * numpy.log(R / d + 1) + 0.09 * numpy.log(Z / d * 10 + 1) + 0.06 * numpy.log(L / d * 10 + 1)
    # 篇均传播力
    A = 0.85 * numpy.log(R / n + 1) + 0.09 * numpy.log(Z / n * 10 + 1) + 0.06 * numpy.log(L / n * 10 + 1)
    # 头条传播力
    H = 0.85 * numpy.log(Rt / d + 1) + 0.09 * numpy.log(Zt / d * 10 + 1) + 0.06 * numpy.log(Lt / d * 10 + 1)
    # 峰值传播力
    P = 0.85 * numpy.log(Rmax + 1) + 0.09 * numpy.log(Zmax * 10 + 1) + 0.06 * numpy.log(Lmax * 10 + 1)
    WCI = O * 0.6 + A * 0.2 + H * 0.1 + P * 0.1
    return float(numpy.log10(WCI*WCI*12))

def get_bci(item):
    # print(1111,item)
    if item['forward_num'] == None:
        return 0.00
    # if item['original_forward_num'] == None:
    #     item['original_forward_num'] = 0
    # if item['original_comments_num'] == None:
    #     item['original_comments_num'] = 0

    X1 = float(item['publish_num'])  # 发博数
    X2 = float(item['original_publish_num_change'])  # 原创微博数
    X3 = float(item['forward_num'])  # 转发数
    X4 = float(item['max_read_num'])  # 评论数
    X5 = float(item['original_forward_num'])  # 原创微博转发数
    X6 = float(item['original_comments_num'])  # 原创微博评论数
    X7 = float(item['likes_num'])  # 点赞数
    W1 = 0.3 * numpy.log(X1 + 1) + 0.7 * numpy.log(X2 + 1)
    W2 = 0.2 * numpy.log(X3 + 1) + 20 * numpy.log(X4 + 1) + 0.25 * numpy.log(X5 + 1) + 0.25 * numpy.log(
        X6 + 1) + 0.1 * numpy.log(X7 + 1)
    BCI = (0.2 * W1 + 0.8 * W2) * 160
    # print(type(BCI))
    return float(numpy.log10(BCI))


def get_dci(item):
    # if item['publish_num'] == None:
    #     return 0.00
    # if item['comments_num'] == None:
    #     item['comments_num'] = 0
    # if item['forward_num'] == None:
    #     item['forward_num'] = 0

    # print((publish_num,all_likes_num,comments_num,forward_num,fans_change,fans))
    X1 = float(item['publish_num'])  # 发文数
    X2 = float(item['all_likes_num'])  # 点赞数
    X3 = float(item['comments_num'])  # 评论数
    X4 = float(item['forward_num'])  # 分享数
    X5 = float(item['fans_change'])  # 新增粉丝数
    if X5 <0:
        X5 = 0
    X6 = float(item['fans'])  # 总粉丝数
    DCI = ((0.1 * numpy.log(X1 + 1)) + (
            0.76 * (0.17 * numpy.log(X2 + 1)) + 0.37 * numpy.log(X3 + 1) + 0.46 * numpy.log(X4 + 1)) + (
                   0.14 * (0.11 * numpy.log(X5 + 1)) + 0.89 * numpy.log(X6 + 1))) * 100

    return float(numpy.log10(DCI))
