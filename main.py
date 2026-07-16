import re


def get_tokens(text, level="word"):
    """
    文本预处理与分词
    :param text: 输入字符串
    :param level: "char" 字符级别, "word" 词语级别
    :return: 处理后的词元列表
    """
    # 1. 统一转为小写
    text = text.lower()

    # 2. 去除标点符号和特殊字符，只保留字母、数字、中文和空格
    text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)

    if level == "char":
        # 字符级别：直接返回字符列表
        return list(text)
    elif level == "word":
        # 词语级别：尝试使用 jieba 进行中文分词
        try:
            import jieba
            # jieba.lcut 返回分词后的列表
            return list(jieba.lcut(text))
        except ImportError:
            # 如果没有安装 jieba，则按空格和中文单字拆分
            return text.split()
    else:
        raise ValueError("level 参数必须是 'char' 或 'word'")


def jaccard_similarity(str1, str2, level="word"):
    """
    计算 Jaccard 相似度
    :param str1: 字符串1
    :param str2: 字符串2
    :param level: "char" 字符级别, "word" 词语级别
    :return: 相似度分数 (0.0 到 1.0 之间)
    """
    # 获取词元
    tokens1 = get_tokens(str1, level)
    tokens2 = get_tokens(str2, level)

    # 转换为集合
    set1 = set(tokens1)
    set2 = set(tokens2)

    # 计算交集和并集
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # 处理两个空字符串的情况，避免除以0
    if len(union) == 0:
        return 1.0

    # 计算 Jaccard 相似度
    similarity = len(intersection) / len(union)
    return similarity


# ================= 测试代码 =================
if __name__ == "__main__":
    # 测试 1：英文词语级别
    s1 = "I love programming!"
    s2 = "I love coding."
    sim = jaccard_similarity(s1, s2, level="word")
    print(f"英文词语级别 ('{s1}' vs '{s2}'): {sim:.4f}")

    # 测试 2：英文字符级别
    sim_char = jaccard_similarity(s1, s2, level="char")
    print(f"英文字符级别 ('{s1}' vs '{s2}'): {sim_char:.4f}")

    # 测试 3：中文词语级别 (需要安装 jieba: pip install jieba)
    s3 = "我喜欢写代码！"
    s4 = "我喜欢听音乐。"
    sim_cn = jaccard_similarity(s3, s4, level="word")
    print(f"中文词语级别 ('{s3}' vs '{s4}'): {sim_cn:.4f}")

    # 测试 4：中文字符级别
    sim_cn_char = jaccard_similarity(s3, s4, level="char")
    print(f"中文字符级别 ('{s3}' vs '{s4}'): {sim_cn_char:.4f}")
##准备发布第一个版本
# 这是dev分支上新增的注释，用于演示PR流程
