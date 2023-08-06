# from cloudplatform_sdks.tencentcloud_models import TencentCfs
# # from cloudplatform_sdks.alicloud_models import AliCdnDomain
#
# if __name__ == '__main__':
#     # resp = TencentCfs.create(Zone="ap-shanghai-2", NetInterface="VPC", PGroupId="pgroupbasic", Protocol="NFS",
#     #                   FsName="CYAN_test", VpcId="vpc-lo3ingay", SubnetId="subnet-gmow4lhv")
#     # print(resp)
#     # resp = TencentCfs.list()
#     # print(resp)
#     # print(resp[0].delete())
#     # TencentCfs.create()
#     cfs_list = TencentCfs.list()
#     print(cfs_list[0].delete())

import random


def get_random_string(n):
    arr = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
    return ''.join([random.choice(arr) for _ in range(n)])


'''
1.
对接各大云平台，整合云平台之间的差异性，抽象出共同的地方，适配不同的地方。
针对云资源组件的开发确定了一套开发模式，获取AK-生成Client-调用API-异常处理
以ORM的思想封装了各类云资源，在代码种对应一个类，类的方法实现创建，对象的方法实现卸除，对象的属性映射关系，同时利用代理模式实现了对获取AK和生成Client的封装，开源了cloudplatform-sdks。
    - 生成蓝图，蓝图是yaml结构的文件，里面定义了部署的节点的生命周期和属性，需要通过cloudify的dsl语言去解析蓝图。
    - 基于cloudify编排系统，基于节点之间的依赖关系，按拓扑序去执行各个节点的生命周期，例如创建、卸除、启动、停止。
2.
从代码review-jenkins各组成项目打包-jenkins完整的ansible整包-触发jenkins ansible整包的一键部署-最后由测试人员jenkins触发IT自动化测试。
3.
golang项目是针对在网络分区的情况下去实现对云资源的管理。典型的例子就是常见的银行系统下，两个网络分区，需要有一台虚机同时拥有双网卡，通过在虚机上安装agent来实现tcp报文的转发。
Saas上的产品需要管理如VC、阿里云Vpc下的云资源。
'''
print(get_random_string(6))
#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdknas.request.v20170626.DescribeAccessGroupsRequest import DescribeAccessGroupsRequest

client = AcsClient('LTAI4GL6pbRU2huDhHUfCSqQ', 'z2MFvYolcr9m6LqF24Z2e9Ye3ZR5Js', 'cn-hangzhou')

request = DescribeAccessGroupsRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))