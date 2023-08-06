### 说明

BBCloud内部使用的Python工具包

```shell
# 安装依赖
pip3 install -r requirements.txt

# 编译
python3 setup.py sdist bdist_wheel
# 发布
python3 -m twine upload --repository pypi dist/*
```