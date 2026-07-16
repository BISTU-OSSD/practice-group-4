# 假设这是你的模型导入，如果模块名或函数名不同，请在此处修改
# from similarity_model import jaccard_similarity

# ----------------- 以下为模拟的 similarity_model -----------------
# 为了让你能够直接运行测试，我在这里模拟了一个 similarity_model 模块
class MockSimilarityModel:
    @staticmethod
    def jaccard_similarity(str1: str, str2: str) -> float:
        """模拟 Jaccard 相似度计算"""
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        if len(union) == 0:
            return 1.0
        return len(intersection) / len(union)


# 实例化模拟的模型对象
similarity_model = MockSimilarityModel()


# -----------------------------------------------------------------


def main():
    print("=== 文本相似度计算程序 ===")
    print("请依次输入两个字符串来计算它们的 Jaccard 相似度。")
    print("输入 -1 即可退出程序。\n")

    while True:
        # 接收第一个字符串
        str1 = input("请输入第一个字符串（输入 -1 退出）: ").strip()

        # 检查退出条件
        if str1 == "-1":
            print("程序已退出。")
            break

        # 接收第二个字符串
        str2 = input("请输入第二个字符串（输入 -1 退出）: ").strip()

        # 检查退出条件
        if str2 == "-1":
            print("程序已退出。")
            break

        # 调用模型计算相似度
        try:
            score = similarity_model.jaccard_similarity(str1, str2)
            # 格式化输出，保留4位小数
            print(f"👉 相似度计算结果: {score:.4f}\n")
        except Exception as e:
            print(f"❌ 计算出错: {e}\n")


if __name__ == "__main__":
    main()
