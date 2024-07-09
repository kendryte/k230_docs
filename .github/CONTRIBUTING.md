# 贡献指南

首先感谢您参与本开源项目，在您提交issue和pull request之前请认真阅读本指南

在提交pull request时一定要关联相应的issue，如果没有相应issue，请先创建issue
关于pull request关联issue，GitHub支持自动和手动关联，具体操作请参考[Link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)

issue和pull request填写时都支持Markdown，关于GitHub的Markdown语法和扩展请参考[GitHub Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github)

## 提交issue

1. 打开issue界面 [issue](https://github.com/kendryte/k230_docs/issues)
1. 查看issue列表中是否已经存在相似issue，如果没有请点击`New issue`按钮
1. 根据您的问题类型，选择不同的issue模板
1. 填写必须项后(带红色\*标记)，点击`Submit new issue`按钮完成提交

## 提交pull request

1. Fork本仓库到您的github
1. Clone仓库到您本地
1. 您可以基于`main`分支创建新分支并添加更改`git checkout -b newbranch -l main`
1. 提交您的更改到您的github
1. 进入您的github仓库点击`Pull request`按钮后点击`New pull request`按钮
1. 选择`base repository`为`kendryte/k230_docs`，选择`base`为`main`，选择`head repository`为`yourname/k230_docs`，选择`compare`为`newbranch`
1. 根据pull request模板要求填写您的描述
1. 点击`Create pull request`完成提交

> 如果您对以上流程还有不清楚的地方请参考[GitHub PR Flow](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests)

## Markdown检查

本项目会对上传的Markdown文件进行格式化检查和内部引用链接检查，如果不符合格式要求或存在不能访问的链接，导致PR不能被merge，因此提交PR前请确保您已在本地进行过检查。
格式检查工具使用的是`markdownlint`，规则配置文件是[markdownlint.json](../.markdownlint.json)。本地可使用`vscode`安装`markdownlint`来进行在线检查和格式化。也可以使用`markdownlint-cli`工具进行检查，执行如下命令：

```shell
docker run -v $PWD:/workdir davidanson/markdownlint-cli2:v0.13.0 "**/*.md"
```

您也可以在提交PR之前，先push到您GitHub仓库的`check`分支进行CI检查，避免重复修改PR
