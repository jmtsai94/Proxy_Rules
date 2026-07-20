# Proxy Rules (AI.list)

这是一个自动获取、去重合并并转换为 **Quantumult X** 格式的 AI 分流规则集仓库。通过 GitHub Actions 每天自动更新。

## 🌟 包含的规则源
规则从以下上游源定时抓取并合并：
1. **666OS/rules**: `AI.txt` (Mihomo 格式)
2. **blackmatrix7/ios_rule_script**: `Gemini.list` (Quantumult X 格式)
3. **ddgksf2013/filter**: `Ai.yaml` (Clash 格式)
4. **fmz200/wool_scripts**: `AI.list` (Loon 格式)

## ⚡ 转换与优化说明
* **双列无策略格式**：合并后的规则移除了最后一列的策略名称（例如直接输出 `HOST-SUFFIX,domain.com`，而非 `HOST-SUFFIX,domain.com,Proxy`）。这大大减小了规则文件的体积，并且**完全不限制您的分流策略选择**。
* **规则排序**：规则按照类型（`HOST` -> `HOST-SUFFIX` -> `HOST-KEYWORD` -> `IP-CIDR` -> `IP6-CIDR` -> `USER-AGENT`）分组，并且在各分组内部按字母升序排序，以符合 Quantumult X 的最佳匹配性能要求。

## ⚙️ 在 Quantumult X 中引用
请将以下链接添加到您的 Quantumult X **分流（Filter） -> 引用（Resource）** 中：

```text
https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/AI.list
```

### 💡 重要提示
因为规则文件内不带策略，您**必须**在 Quantumult X 引入该资源时，为它指定一个“策略偏好 (force-policy)”。例如在配置文件中写：
```text
https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/AI.list, tag=AI Rules, force-policy=您的代理策略组, update-interval=86400, enabled=true
```
或者在 App 界面中长按该订阅资源，进入设置将“策略偏好”绑定到您的代理策略组中。

## 🤖 自动化更新机制
* **自动更新**：GitHub Actions 将在每天的 **北京时间中午 12:00 (04:00 UTC)** 自动运行脚本并推送到本仓库。
* **手动触发**：您也可以在 GitHub 仓库的 **Actions** 标签页中，选择 **Auto Update Proxy Rules** 工作流并点击 **Run workflow** 手动触发更新。
