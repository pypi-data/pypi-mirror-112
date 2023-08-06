# Example Package

sentry==21.6.1
oss2==2.14.0

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
> 测试命令行工具
```
tfd a1 a2
```

> 测试脚本内容
```
    >>> import sentry_oss_nodestore
    >>> sentry_oss_nodestore.__version__
```

> 用法，配置
```
SENTRY_NODESTORE = 'sentry_oss_nodestore.backend.OSSNodeStorage'
SENTRY_NODESTORE_OPTIONS = {
    'bucket_name': 'tt-sentry',
    'endpoint': 'oss-us-east-1-internal.aliyuncs.com',
    'aws_access_key_id': '1111',
    'aws_secret_access_key': '1111'
}
    
```