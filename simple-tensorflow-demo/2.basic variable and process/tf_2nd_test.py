import tensorflow as tf
import numpy as np


def ori_add():
    x = 1
    y = 2
    z = 3
    add = x + y
    mul = y * z
    print(add, mul)

def tf_add():
    x = tf.Variable(1)  # x是常量
    y = tf.placeholder(tf.int32)  # 假设我们不知道y的值, 先占位
    z = tf.placeholder(tf.int32)  # 假设我们不知道z的值, 先占位
    add = tf.add(x, y)
    mul = tf.multiply(y, z)
    init = tf.global_variables_initializer()  # 初始化所有的tf.Variable
    with tf.Session() as sess:
        sess.run(init)
        result = sess.run([add, mul], feed_dict={y: 2, z: 3})  # 通过feed传递值, sess可以一次取回多个tensor
        print(result)

if __name__ == "__main__":
    ori_add()
    tf_add()

