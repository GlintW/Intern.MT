import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


## 参数
# 学习率, 太小则每次optimizer变化很小, 学习速度慢; 太大则可能导致过度学习, 最终结果不准确
learning_rate = 0.01
# 隐藏层深度
training_epochs = 2000
# 打印的节点层
display_step = 50


## 构造训练数据
## numpy.asarray将list/turple转成矩阵
train_X = np.asarray([3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167, 7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1])
train_Y = np.asarray([1.7, 2.76, 2.09, 3.19, 1.694, 1.573, 3.366, 2.596, 2.53, 1.221, 2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3])
## shape得到矩阵每个维的大小, 这里是一维, 所以等同于len(train_X)
n_samples = train_X.shape[0]

# 绘图
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)  # 3个1分别代表, 将画布分拆成1行, 1列, 图画建立在第1块分拆的部分上.
plt.plot(train_X, train_Y, 'bo', label='training data')  # b是blue, o代表原点, -代表是直线, +代表星星
#plt.legend()
#plt.show()


## 定义常量
X = tf.placeholder("float")
Y = tf.placeholder("float")


## 定义神经层
def add_layer(inputs, activation_function=None):

    ## 定义Weight和biases (使用numpy库生成正态分布随机数)
    weights = tf.Variable(np.random.randn(), name="weights")
    biases = tf.Variable(np.random.randn(), name="biases")

    ## 模拟的激励函数结果, X * weights + biases
    activation = tf.add(tf.multiply(X, weights), biases)

    if activation_function is None:
        outputs = activation
    else:
        outputs = activation_function(activation)
    return outputs


## 定义隐藏层, 使用tensorflow自带的激励函数tf.nn.relu
shadow = add_layer(X, activation_function=tf.nn.relu)
#shadow = add_layer(X, activation_function=None)


## 定义输出层
prediction = add_layer(shadow, activation_function=None)


## 优化每次的误差
## (激励结果 - Y) ^ 2 / (2 * 矩阵大小)
## tensorflow.reduce_sum 用于矩阵求和(对tensor的维度求和)
'''
根据tensorflow文档, ReductionTensorFlow provides several operations that you can use to perform common math computations that reduce various dimensions of a tensor.
reduce_xxx, 都是把某一个维度上这一序列的数缩减到一个(求和/求平均值). 也即是使用reduction_indices参数来指定使用某个方法对输入的矩阵进行降维.
对于二维矩阵输入, reduction_indices=0按列降维, reduction_indices=1按行降维.

# 'x' is [[1, 1, 1]
#         [1, 1, 1]]
tf.reduce_sum(x) ==> 6
tf.reduce_sum(x, 0) ==> [2, 2, 2]
tf.reduce_sum(x, 1) ==> [3, 3]
tf.reduce_sum(x, 1, keep_dims=True) ==> [[3], [3]]
tf.reduce_sum(x, [0, 1]) ==> 6

# python console:
a = [1, 1, 1, 1, 1, 1]
b = np.asarray(a)
c = tf.reduce_sum(b)
sess.run(tf.reduce_sum(b))  ==>  6
'''
## 这个算法到底是为什么?
cost = tf.reduce_sum(tf.pow(prediction - Y, 2)) / (2 * n_samples)
## GradientDescentOptimizer是梯度下降法的优化器, 可查阅"最速下降法".
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

## 初始化变量
init = tf.global_variables_initializer()

## 进入Session
with tf.Session() as sess:
    sess.run(init)

    ## 开始训练
    for epoch in range(training_epochs):
        ## zip合并两个turple或list
        # a = [1, 2, 3]
        # b = ["li", "xiong", "yu"]
        # zip(a, b)  ==>  [(1, 'li'), (2, 'xiong'), (3, 'yu')]  结果是一个zip对象而不是list/turple
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        ## 分步打印结果
        if epoch % display_step == 0:
            print("Epoch: %d, cost=%.9f" % (epoch + 1, sess.run(cost, feed_dict={X: train_X, Y:train_Y})))
            # 逐次打印新的函数图象
            try:
                ax.lines.remove(lines[0])
            except Exception:
                pass
            prediction_Y = sess.run(prediction, feed_dict={X: train_X})
            lines = ax.plot(train_X, prediction_Y, 'r-', lw = 5)
            plt.pause(1)

    print("Done!")
    print("cost=%.9f" % sess.run(cost, feed_dict={X: train_X, Y:train_Y}))

    #plt.plot(train_X, sess.run(weights) * train_X + sess.run(biases), label='fitted line')

