Flask+Vue Gui for [Pocsuite3](https://github.com/knownsec/pocsuite3)

![img](https://user-images.githubusercontent.com/50647385/207260922-e6f0c040-951d-40ce-a737-921de919d74e.png)

# Install

Add the gui file to the Pocsuite3 project and place it in the same directory as cli.py

![image](https://user-images.githubusercontent.com/50647385/207257389-7d47197d-a5f0-4348-96ef-014cee15f369.png)

install requirement

```
# use other pypi mirror
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
```

# Usage

Run flask server
```shell
cd gui

# start server
python server.py
```

Run Vue gui
```shell
cd gui-vue

# install requirement
npm run install
vue-cli-service serve
```