# GitHub公开展示

目标账号：Zhuyyyan。目标仓库名：agentic-payment-authorization。

公开版已整理：源码、论文PDF/DOCX、理解辅助稿、图表、汇总结果、文献元数据和复现说明。第三方文献全文、老师原始作业文件、完整大体积日志及交付压缩包均不进入Git历史。全部示例交易为合成数据。

由于自动审批服务持续超时，代理尚未创建或推送远程仓库。目标地址不是已发布成功的证明。

## 若代理无法恢复访问

1. 在GitHub创建仓库，名称填 `agentic-payment-authorization`，Owner选`Zhuyyyan`，可见性选 **Public**。不要勾选自动添加README、gitignore或许可证，避免与本地初始提交冲突。
2. 在本项目文件夹的PowerShell运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\publish.ps1
```

如Git要求登录，请在Git Credential Manager打开的正常GitHub登录窗口完成。无需把密码或令牌发给助手。脚本只添加预设远程地址并推送main分支，不读取或打印凭据，不强制覆盖远程历史。

若本机已有GitHub CLI且已登录，也可运行 `powershell -ExecutionPolicy Bypass -File .\publish.ps1 -CreateRepository`，一次完成公开仓库创建及推送。
