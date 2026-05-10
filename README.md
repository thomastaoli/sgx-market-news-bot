# SGX Market Open News Bot  

An automated newsroom bot that fetches SGX market data every trading morning, generates a Chinese-language market opening brief, and emails it automatically through GitHub Actions.

# 撰写新交所即时新闻

每个交易日的开市和闭市时间自动抓取新交所（SGX）市场数据，生成华文股市开市与闭市简讯，并通过 GitHub Actions 自动发送邮件给早报财经。

---

# Features  
- Fetches live SGX market statistics from SGX APIs
- Retrieves Straits Times Index (STI) data
- Extracts STI constituent stock performance
- Automatically identifies:
  - Top gainers
  - Top losers
  - Advancers / decliners
  - STI breadth
- Retrieves Asia-Pacific market index performance
- Converts numbers into Chinese newsroom style
- Generates Chinese-language market opening and closing briefs
- Sends stories automatically by email
- Runs automatically every weekday via GitHub Actions
- Uses Singapore timezone (SGT)
- Designed for newsroom automation workflows

# 功能
- 自动抓取 SGX 实时市场数据
- 获取海峡时报指数（STI）数据
- 提取 STI 成份股表现
- 自动识别：
  - 涨幅最大股
  - 跌幅最大股
  - 上升股 / 下跌股
  - 海指涨跌分布
- 自动抓取亚太主要市场指数表现
- 自动转换为早报财经新闻格式
- 自动生成华文开市与闭市简讯
- 自动发送邮件
- 通过 GitHub Actions 于每个交易日自动运行
- 使用新加坡时间（SGT）
- 为财经新闻编辑部自动化流程设计
