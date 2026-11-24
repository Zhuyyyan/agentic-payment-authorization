# GitHub公开展示

公开仓库：[Zhuyyyan/agentic-payment-authorization](https://github.com/Zhuyyyan/agentic-payment-authorization)。默认分支为`main`。

公开版已整理：源码、论文PDF/DOCX、理解辅助稿、图表、汇总结果、文献元数据和复现说明。第三方文献全文、老师原始作业文件、完整大体积日志及交付压缩包均不进入Git历史。全部示例交易为合成数据。

项目已于2026年11月24日公开发布。首次发布提交为`1f1dd5b23508b89c60aa9b21b90e5f0461aee968`，已通过只读远程分支核对。后续完善记录保存在Git提交历史中。

## 公开范围与核验记录

公开`outputs/logs/verification.json`和`outputs/logs/native_render_audit.json`两份轻量核验记录：前者记录运行环境、源文件摘要及结果复核，后者记录论文分页、字号和文档摘要。完整逐笔日志继续保留在本地；其余日志仍由忽略规则排除。

本次发布收尾仅调整文档、忽略规则和仓库元数据，不修改授权策略、数据生成过程、阈值、权重或实验结果。论文中的主实验与追加稳健性比较保持原值；数值一致性另通过结果表、源文件及文稿摘要核对。

## 后续更新

现有仓库无需重复创建。在本项目文件夹修改并验证后运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\publish.ps1
```

如Git要求登录，请在Git Credential Manager打开的正常GitHub登录窗口完成。无需把密码或令牌发给助手。脚本只添加预设远程地址并推送main分支，不读取或打印凭据，不强制覆盖远程历史。

`-CreateRepository`仅供首次创建其他新副本时使用，不适用于这个已经存在的仓库。
