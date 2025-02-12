### mall_web
一个基于python + peewee,Nacos、Consul 、Redis、RocketMQ、Grpc, jaeger, kong的微服务电商商城服务端端系统，采用主流的互联网技术架构、支持集群部署、服务注册和发现以及拥有完整的订单流程等，代码完全开源，没有任何二次封装。本项目客户端由go实现，请移步[mall_web](https://github.com/setking/mall_web)



### 特性
- 基于 peewee API 框架，提供了丰富的支持
- 使用mysql作为数据库
- 使用yapi作为接口文档
- 使用grpc作为微服务通信基础
- 使用loguru作为日志库
- 使用consul作为注册中心和服务发现
- 使用nacos作为配置中心
- 使用redis作为分布式缓存
- 接入jaeger+OpenTelemetry链路追供功能
- 使用kong作为网关
- 接入jenkins实现自动化部署
- 使用RocketMQ作为消息队列

### 基本功能
- 用户服务
- 库存服务
- 商品服务
- 订单服务
- 购物车服务

### 目录结构

```azure
mall_srv
goods_srv -- 商品服务
  ├─handler  -- grpc接口配置
  ├─logs  -- 日志
  ├─model  -- mysql数据模型
  ├─nacos-data  -- nacos配置信息
  ├─proto  -- protobuf文件存储地址
  ├─settings  -- 项目全局设置
  ├─testy  -- 接口测试
  └─server.py  -- 服务入口


inventory_srv -- 库存服务
  ├─handler  -- grpc接口配置
  ├─logs  -- 日志
  ├─model  -- mysql数据模型
  ├─nacos-data  -- nacos配置信息
  ├─proto  -- protobuf文件存储地址
  ├─settings  -- 项目全局设置
  ├─testy  -- 接口测试
  └─server.py  -- 服务入口
    
order_srv -- 订单服务
  ├─handler  -- grpc接口配置
  ├─logs  -- 日志
  ├─model  -- mysql数据模型
  ├─nacos-data  -- nacos配置信息
  ├─proto  -- protobuf文件存储地址
  ├─settings  -- 项目全局设置
  ├─testy  -- 接口测试
  └─server.py  -- 服务入口
  
user_srv -- 用户服务
  ├─handler  -- grpc接口配置
  ├─logs  -- 日志
  ├─model  -- mysql数据模型
  ├─nacos-data  -- nacos配置信息
  ├─proto  -- protobuf文件存储地址
  ├─settings  -- 项目全局设置
  ├─testy  -- 接口测试
  └─server.py  -- 服务入口
    
userop_srv -- 购物车服务
  ├─handler  -- grpc接口配置
  ├─logs  -- 日志
  ├─model  -- mysql数据模型
  ├─nacos-data  -- nacos配置信息
  ├─proto  -- protobuf文件存储地址
  ├─settings  -- 项目全局设置
  ├─testy  -- 接口测试
  └─server.py  -- 服务入口
```
