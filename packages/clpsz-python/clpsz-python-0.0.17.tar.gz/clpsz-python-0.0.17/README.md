# clpsz
clpsz python libs and tools

## publish
python setup publish

两种twine命令使用方式
1. twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
   1. 方式1需要在命令行输入账号密码
2. twine upload -r public dist/*
   1. 方式2直接使用~/.pypirc里面的配置
