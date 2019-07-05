from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def datasets_demo():
    """
    sklearn数据集使用
    """
    # 获取数据集
    iris = load_iris()
    print("鸢尾花数据集：\n", iris)
    print("查看数据集描述：\n", iris["DESCR"])
    print("查看特征值的名字：\n", iris.feature_names)
    print("查看特征值:\n",iris.data,iris.data.shape)
    print("鸢尾花的特征值:\n",iris["data"])
    print("鸢尾花的目标值:\n",iris.target)

    #数据集划分
    x_train, x_test, y_train, y_test=train_test_split(iris.data, iris.target, test_size=0.2)
    print("训练集的特征值:\n",x_train,x_train.shape)

    return None


if __name__ == "__main__":
    datasets_demo()
