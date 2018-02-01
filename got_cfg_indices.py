import subprocess
import re
"""
nvdisasm可以获得控制流图，但是如果直接获得整个图的，会很大无法展示，可以指定函数展示，但是需要执行函数的index。由于不知道index从哪里获得，这里用这个文件获得fun和index的对应关系
"""

# 我晕，这到底是什么的个数。。根本体会不到。只能先写大一点范围。
fun_nums = 50

fun_map_cfg = [False for i in range(fun_nums + 1)]
reg = re.compile("subgraph \"(.+)\"")


def run_nvdisasm(i):
    # 参数应该是每个参数一个引号括起来
    out_bytes = subprocess.check_output(
        ['/usr/local/cuda-9.1/bin/nvdisasm', "-c", "-cfg",
         "/home/find/mega/cppcode/cuda_workspace/srad.origin/sass/main.sm_50.cubin",
         '-fun', '%d' % i])
    out_text = out_bytes.decode('utf-8')
    result = reg.findall(out_text)
    if result:
        return result[0]
    else:
        # print("序号%d fun无法显示" % i)
        return None


def get_cfg_indices():
    for i in range(1, fun_nums + 1):
        try:

            fun_map_cfg[i] = run_nvdisasm(i)
        except subprocess.CalledProcessError as e:
            out_bytes = e.output  # Output generated before error
            code = e.returncode  # Return code
            print(e)


get_cfg_indices()
youxiao = 0
for i, val in enumerate(fun_map_cfg):
    print("%d:%s" % (i, val))
    if val:
        youxiao += 1
print(youxiao)
