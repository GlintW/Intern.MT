import tensorflow as tf
import numpy as np


## 造出测试数据
# 造出一个数组, 里面存在100个值, 把这些值当成x
x_data = np.random.rand(100).astype(np.float32)
# 然后通过"黑盒"造出根据x得到的y的值
y_data = x_data*0.1 + 0.3


## 开始使用tensorflow
# 给出a和b的假设值, 让其通过tensorflow去计算
a = tf.Variable(tf.random_uniform([1], -1000.0, 1000.0))
#b = tf.Variable(tf.zeros([1]))
b = tf.Variable(tf.random_uniform([1], -1000.0, 1000.0))
# 给出计算公式
y = x_data*a + b
# 计算每次经过假设的a和b之后得到的y值和真实的y值的差异
loss = tf.reduce_mean(tf.square(y-y_data))
# 使用"梯度下降法"(Gradient Descent)来传递误差
optimizer = tf.train.GradientDescentOptimizer(0.3)
# 使得每次的误差往更小的方向变化
train = optimizer.minimize(loss)
# 初始化所有定义
init = tf.global_variables_initializer()
# 创建会话
sess = tf.Session()
sess.run(init)
# 计算 
for step in range(1001):
    sess.run(train)
    # 每隔10次flow, 打印当前模拟的a和b的值
    if step % 10 == 0:
        print(step, sess.run(a), sess.run(b))


