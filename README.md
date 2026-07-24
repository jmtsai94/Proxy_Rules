# Proxy Rules

这是一个自动获取、去重合并并转换为 **Quantumult X** 格式的分流规则集仓库。通过 GitHub Actions 每天自动更新。

> [!NOTE]
> 仓库现已更新并转移至新用户名下，所有订阅链接已更新为 `xcaiii`。

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

### 6. `advertising.list` (广告拦截规则)
* **上游源**：
  * `fmz200/wool_scripts` (filter.list)

### 7. `apple.list` (Apple 苹果服务规则)
* **上游源**：
  * `blackmatrix7/ios_rule_script` (Apple.list)

### 8. `HK_Broker.list` (港股券商规则 - 富途/长桥/老虎等)
* **上游源**：
  * `LingJingMaster/Shadowrocket-Rules` (HK_Broker.list)
  * 本地源文件 `Rules/Source/Filter_HKBroker.snippet` (富途/长桥/老虎等规则)

---

## ⚡ 转换与优化说明
* **三列格式符合规范**：所有规则自动补齐对应的文件名作为第三列策略占位符（例如 `HOST-SUFFIX,domain.com,AI`），彻底解决 Quantumult X 引入远程订阅时报 `Invalid Line` 错误的问题。您依然可以在 Quantumult X 界面中自由将占位符绑定到任何您想要的策略组中（或者使用链接后面的 `force-policy` 参数强制指定）。
* **规则排序**：规则按照类型（`HOST` -> `HOST-SUFFIX` -> `HOST-KEYWORD` -> `IP-CIDR` -> `IP6-CIDR` -> `USER-AGENT`）分组，并且在各分组内部按字母升序排序，以符合 Quantumult X 的最佳匹配性能要求。

---

## ⚙️ 在 Quantumult X 中引用
请在 Quantumult X **分流（Filter） -> 引用（Resource）** 中添加对应规则的 Raw 链接。

**订阅链接列表**：
* **AI 规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/AI.list`
* **流媒体规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/Streaming.list`
* **常用代理规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/Proxy.list`
* **直连规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/direct.list`
* **加密货币规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/Crypto.list`
* **广告拦截规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/advertising.list`
* **苹果服务规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/apple.list`
* **港股券商规则**：
  `https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/HK_Broker.list`

### 💡 重要提示
引入这些资源时，您需要为其指定对应的“策略偏好 (force-policy)”，比如：
```text
https://raw.githubusercontent.com/xcaiii/Proxy_Rules/main/Rules/Proxy.list, tag=Proxy Rules, force-policy=您的代理策略组, update-interval=86400, enabled=true
```

---

## 🤖 自动化更新机制
* **自动更新**：GitHub Actions 将在每天的 **北京时间中午 12:00 (04:00 UTC)** 自动运行脚本并推送到本仓库。
* **手动触发**：您也可以在 GitHub 仓库 of **Actions** 标签页中，选择 **Auto Update Proxy Rules** 工作流并点击 **Run workflow** 手动触发更新。
