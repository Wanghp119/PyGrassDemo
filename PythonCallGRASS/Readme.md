# Python Call GRASS Steps

> 我所用的版本Python：2.7
>             GRASS：7.0.0
- 1. 首先需要将\GRASS\etc\python文件夹下的grass文件夹整个复制到你所用Python文件夹下的\Lib\site-packages中。
- 2. 代码可参考CallGrass.py，这里调用GRASS中的算法是通过GRASS-Python接口进行的。通过代码设置好GRASS运行环境，包括GISBASE，GISDBASE，Location，Mapset等（这里的Location是临时生成的，代码运行结束后会被删除以防止数据冗余），便可以根据所需要的编写自己算法。


## Reference
- [Python Grass 配置](https://blog.csdn.net/hnyzwtf/article/details/52313795)
