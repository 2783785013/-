import numpy as np

def data_(data):
    if data == None:
        data = 0
    return data

def get_PSI(item):
    # 传播力指数 Propagation strength index (PSI)
    # 发稿指数
    if item == None:
        return 0.00
    X1 = float(item)  # 发布量
    X2 = float(1)  # 发布频次
    X3 = float(1)  # 平均篇幅
    X4 = float(1)  # 网站
    X5 = float(1)  # 论坛
    X6 = float(1)  # 微博
    X7 = float(1)  # 微信
    X8 = float(1)  # 总量
    X9 = float(1)  # 转载媒体总数
    X10 = float(1)  # 重点媒体指数

    W1 = np.log(X1 + 1) * 0.3 + np.log(X2 + 1) * 0.4 + np.log(X3 + 1) * 0.3  # 发稿指数
    W2 = np.log(X4 + 1) * 0.2 + np.log(X5 + 1) * 0.1 + np.log(X6 + 1) * 0.2 + np.log(X7 + 1) * 0.1 + np.log(
        X8 + 1) * 0.4  # 转载指数
    W3 = np.log(X9 + 1) * 0.6 + np.log(X10 + 1) * 0.4  # 路径指数
    PSI = W1 * 0.4 + W2 * 0.5 + W3 * 0.1
    return float(PSI)


def get_MII_wb(item,avg_likes_num,avg_read_num,avg_comment_num):
    # 影响力指数Media Influence Index (MII)
    X1 = float(item['read_num'])  # 日均阅读数
    X2 = float(data_(avg_read_num))  # 单篇平均阅读数
    X3 = float(item['max_read_num'])  # 最大单篇阅读数
    X4 = float(item['read_num'])  # 阅读总数
    X5 = float(item['comments_num'])  # 日均评论数
    X6 = float(data_(avg_comment_num))  # 单篇平均评论数
    X7 = float(item['max_comments_num'])  # 最大单篇评论数
    X8 = float(item['comments_num'])  # 评论总数
    X9 = float(item['likes_num'])  # 日均点赞数
    X10 = float(data_(avg_likes_num))  # 单篇平均点赞数
    X11 = float(item['max_likes_num'])  # 最大单篇点赞数
    X12 = float(item['likes_num'])  # 点赞总数
    X13 = float(1)  # 转载媒体总数
    X14 = float(1)  # 重点媒体指数
    W1 = np.log(X1 + 1) * 0.4 + np.log(X2 + 1) * 0.4 + np.log(X3 + 1) * 0.1 + np.log(X4 + 1) * 0.1  # 阅读指数
    W2 = np.log(X5 + 1) * 0.4 + np.log(X6 + 1) * 0.4 + np.log(X7 + 1) * 0.1 + np.log(X8 + 1) * 0.1  # 评论指数
    W3 = np.log(X9 + 1) * 0.4 + np.log(X10 + 1) * 0.4 + np.log(X11 + 1) * 0.1 + np.log(X12 + 1) * 0.1  # 点赞指数
    W4 = np.log(X13 + 1) * 0.6 + np.log(X14 + 1) * 0.4  # 路径指数
    MII = W1 * 0.6 + W2 * 0.2 + W3 * 0.1 + W4 * 0.1
    return float(MII)


def get_MII_wx(item,get_mii_wx_dict):
    # 影响力指数Media Influence Index (MII)
    X1 = float(item['read_num'])  # 日均阅读数
    X2 = float(get_mii_wx_dict['avg_read_num'])  # 单篇平均阅读数
    X3 = float(item['max_read_num'])  # 最大单篇阅读数
    X4 = float(item['read_num'])  # 阅读总数
    X5 = float(get_mii_wx_dict['comments_num'])  # 日均评论数
    X6 = float(get_mii_wx_dict['avg_comment_num'])  # 单篇平均评论数
    X7 = float(get_mii_wx_dict['max_comments_num'])  # 最大单篇评论数
    X8 = float(get_mii_wx_dict['comments_num'])  # 评论总数
    X9 = float(item['likes_num'])  # 日均点赞数
    X10 = float(get_mii_wx_dict['avg_likes_num'])  # 单篇平均点赞数
    X11 = float(get_mii_wx_dict['max_likes_num'])  # 最大单篇点赞数
    X12 = float(item['likes_num'])  # 点赞总数
    X13 = float(1)  # 转载媒体总数
    X14 = float(1)  # 重点媒体指数
    W1 = np.log(X1 + 1) * 0.4 + np.log(X2 + 1) * 0.4 + np.log(X3 + 1) * 0.1 + np.log(X4 + 1) * 0.1  # 阅读指数
    W2 = np.log(X5 + 1) * 0.4 + np.log(X6 + 1) * 0.4 + np.log(X7 + 1) * 0.1 + np.log(X8 + 1) * 0.1  # 评论指数
    W3 = np.log(X9 + 1) * 0.4 + np.log(X10 + 1) * 0.4 + np.log(X11 + 1) * 0.1 + np.log(X12 + 1) * 0.1  # 点赞指数
    W4 = np.log(X13 + 1) * 0.6 + np.log(X14 + 1) * 0.4  # 路径指数
    MII = W1 * 0.6 + W2 * 0.2 + W3 * 0.1 + W4 * 0.1
    return float(MII)

def get_MII_dy(item,avg_comment_num,avg_likes_num):
    # 影响力指数Media Influence Index (MII)

    X1 = float(1)  # 日均阅读数
    X2 = float(1)  # 单篇平均阅读数
    X3 = float(1)  # 最大单篇阅读数
    X4 = float(1)  # 阅读总数
    X5 = float(item['comments_num'])  # 日均评论数
    X6 = float(data_(avg_comment_num))  # 单篇平均评论数
    X7 = float(item['max_comments_num'])  # 最大单篇评论数
    X8 = float(item['comments_num'])  # 评论总数
    X9 = float(item['likes_num'])  # 日均点赞数
    X10 = float(data_(avg_likes_num))  # 单篇平均点赞数
    X11 = float(item['max_likes_num'])  # 最大单篇点赞数
    X12 = float(item['likes_num'])  # 点赞总数
    X13 = float(1)  # 转载媒体总数
    X14 = float(1)  # 重点媒体指数
    W1 = np.log(X1 + 1) * 0.4 + np.log(X2 + 1) * 0.4 + np.log(X3 + 1) * 0.1 + np.log(X4 + 1) * 0.1  # 阅读指数
    W2 = np.log(X5 + 1) * 0.4 + np.log(X6 + 1) * 0.4 + np.log(X7 + 1) * 0.1 + np.log(X8 + 1) * 0.1  # 评论指数
    W3 = np.log(X9 + 1) * 0.4 + np.log(X10 + 1) * 0.4 + np.log(X11 + 1) * 0.1 + np.log(X12 + 1) * 0.1  # 点赞指数
    W4 = np.log(X13 + 1) * 0.6 + np.log(X14 + 1) * 0.4  # 路径指数
    MII = W1 * 0.6 + W2 * 0.2 + W3 * 0.1 + W4 * 0.1
    return float(MII)

def get_GI(item):
    # 引导力指数Guidance Index (GI)
    if item == None:
        return 0.00
    X1 = float(item)  # 日均评论总数
    X2 = float(1)  # 日均正面评论数
    X3 = float(1)  # 日均反面评论数
    X4 = float(1)  # 日均关键词匹配数
    X5 = float(1)  # 日均词云创新数
    X6 = float(1)  # 日均关键词传播数
    W1 = np.log(X1 + 1) * 0.4 + np.log(X2 + 1) * 0.6 + np.log(X3 + 1) * 0.4  # 情绪指数
    W2 = np.log(X4 + 1) * 0.2 + np.log(X5 + 1) * 0.6 + np.log(X6 + 1) * 0.2  # 词云指数
    GI = W1 * 0.6 + W2 * 0.4
    return float(GI)


def get_CI(item):
    # 公信力指数 Credibility Index (CI)
    if item == None:
        return 0.00
    X1 = float(1)  # 日均怀疑评论数
    X2 = float(item)  # 被公信媒体转载的文章总数
    X3 = float(1)  # 关注及转载的公信媒体数
    W1 = np.log(X1 + 1)  # 质疑指数
    W2 = np.log(X2 + 1) * 0.2 + np.log(X3 + 1) * 0.8  # 公信指数
    CI = W1 * 0.4 + W2 * 0.6
    return float(CI)
