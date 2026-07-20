# Proxy Rules

这是一个自动获取、去重合并并转换为 **Quantumult X** 格式的分流规则集仓库。通过 GitHub Actions 每天自动更新。

## 🌟 包含的规则集

所有生成的规则文件均保存在 **`Rules/`** 文件夹下。以下是每个规则集的说明及上游源：

### 1. `AI.list` (AI 规则)
* **上游源**：
  * `666OS/rules` (AI.txt)
  * `blackmatrix7/ios_rule_script` (Gemini.list)
  * `ddgksf2013/filter` (Ai.yaml)
  * `fmz200/wool_scripts` (AI.list)

### 2. `Streaming.list` (流媒体规则)
* **上游源**：
  * `ddgksf2013/Filter` (Streaming.list)
  * `blackmatrix7/ios_rule_script` (Netflix.list, Disney.list, TikTok.list)

### 3. `Proxy.list` (常用代理规则)
* **上游源**：
  * `blackmatrix7/ios_rule_script` (Proxy.list, Google.list, Spotify.list, GitHub.list)
  * `ConnersHua/RuleGo` (Proxy.list)

### 4. `direct.list` (直连/修复规则)
* **上游源**：
  * `blackmatrix7/ios_rule_script` (WeChat.list)
  * `ConnersHua/RuleGo` (Direct+.list)
  * `ddgksf2013/Filter` (Unbreak.list)
  * `fmz200/wool_scripts` (filterFix.list)

### 5. `Crypto.list` (加密货币规则)
* **上游源**：
  * `blackmatrix7/ios_rule_script` (Crypto.list, Cryptocurrency.list)

---

## ⚡ 转换与优化说明
* **双列无策略格式**：所有合并后的规则均移除了最后一列的策略名称（例如直接输出 `HOST-SUFFIX,domain.com`，而非 `HOST-SUFFIX,domain.com,Proxy`）。这大大减小了规则文件的体积，并且**完全不限制您的分流策略选择**。
* **规则排序**：规则按照类型（`HOST` -> `HOST-SUFFIX` -> `HOST-KEYWORD` -> `IP-CIDR` -> `IP6-CIDR` -> `USER-AGENT`）分组，并且在各分组内部按字母升序排序，以符合 Quantumult X 的最佳匹配性能要求。

---

## ⚙️ 在 Quantumult X 中引用
请在 Quantumult X **分流（Filter） -> 引用（Resource）** 中添加对应规则的 Raw 链接。

**引用链接列表**：
* **AI 规则**：
  `https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/AI.list`
* **流媒体规则**：
  `https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/Streaming.list`
* **常用代理规则**：
  `https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/Proxy.list`
* **直连规则**：
  `https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/direct.list`
* **加密货币规则**：
  `https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/Crypto.list`

### 💡 重要提示
因为规则文件内不带策略，您**必须**在 Quantumult X 引入该资源时，为它指定一个“策略偏好 (force-policy)”。例如在配置文件中写：
```text
https://raw.githubusercontent.com/jmtsai94/Proxy_Rules/main/Rules/Proxy.list, tag=Proxy Rules, force-policy=您的代理策略组, update-interval=86400, enabled=true
```
或者在 App 界面中长按该订阅资源，进入设置将“策略偏好”绑定到对应的策略组中（如 `direct.list` 绑定到 `DIRECT`，`Proxy.list` 绑定到代理组）。

---

## 🤖 自动化更新机制
* **自动更新**：GitHub Actions 将在每天的 **北京时间中午 12:00 (04:00 UTC)** 自动运行脚本并推送到本仓库。
* **手动触发**：您也可以在 GitHub 仓库的 **Actions** 标签页中，选择 **Auto Update Proxy Rules** 工作流并点击 **Run workflow** 手动触发更新。
