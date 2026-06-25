# 语料索引：21 篇真实顶刊论文范本

> 用途：需要"真实范本"时（看一篇同类论文如何谋篇、如何写某章节），先查本表选定 1 篇，再去 `../Nature-essays.md` 里按标题定位**只读那一篇**，避免整篇 2150 行加载。
>
> 语料全文在 `../Nature-essays.md`（单文件，按下表 `# 标题` 检索；附行号便于跳转）。
> 期刊列标 `~` 者为按主题/风格推断，引用前建议核对原文出处。

| 行号 | 标题（在 Nature-essays.md 中检索） | 期刊/类型 | 主题 | 方法 | 可示范的写作点 |
|------|-----------------------------------|-----------|------|------|----------------|
| 1 | Habitat for Coilia nasus … maximum entropy model | ~区域渔业 | 鱼类生境 | MaxEnt / SDM | Abstract 模板B、Methods 复现细节、模型评估(AUC/TSS)写法 |
| 70 | Projected habitat preferences of commercial fish … climate change | ~渔业/海洋 | 商业鱼类分布 | SDM + RCP 情景 | 情景对比、未来分布预测句式 |
| 135 | Pesticide budgets in land and rivers | Nature | 农药归趋 | 全球过程模型 | 正刊定量收尾句（X% degraded / Y% residue / Z% reaches ocean） |
| 227 | River plastic emissions to the world's oceans | Nature Communications | 河流塑料输运 | 全球统计模型 | 空间分布句（top X rivers account for X%）、季节性峰值 |
| 307 | The State of the World's Beaches | ~Nature Communications | 海岸侵蚀 | 卫星遥感综合分析 | 综合分析句（X% of beaches eroding）、人类干预对比 |
| 422 | Climate-driven zooplankton shifts … food quality for fish | Nature Climate Change | 浮游动物群落 | trait-based 模型 | **因果链叙事**、"支持/挑战预期"句法、CEI 范例来源 |
| 536 | Plastic waste discharge … constrained by seawater observations | ~Nature/Science | 海洋塑料反演 | top-down + 集合模型 | 不确定性表达（OMs、95% CI）、观测约束反演叙事 |
| 669 | Rivers as the largest source of mercury to coastal oceans | Nature Geoscience | 河流汞输入 | 高分辨率数据集 | **NG 突破性证据**、量化对比（threefold / 0.2% vs 27%） |
| 733 | Global habitat hotspots and extinction vulnerability of terrestrial vertebrates | ~Nature | 生物多样性热点 | 全球空间分析 | 保护优先级、政策"soft"建议句（We advocate…） |
| 826 | Ecological risk assessment of marine plastic pollution | ~环境科学 | 塑料生态风险 | 风险评估框架 | 风险分级、管理含义段 |
| 930 | Predicting microplactic masses in river networks … country level | ~NC/环境 | 微塑料河网 | 高分辨率建模 | 国家级空间分辨率方法、Methods 参数完整性 |
| 1048 | Pretreatment-free SERS sensing of microplastics … Ag foams | ~分析化学/NC | 微塑料检测 | 自注意力神经网络 | 方法型 Abstract、指标密集、算法概述 |
| 1205 | Multispecies deep learning using citizen science data … | ~生态/方法 | 植物群落建模 | 深度学习 + 公民科学 | 方法优势论证、与传统方法对比 |
| 1318 | Elucidating governing factors of PFAS removal by polyamide membranes … ML | ~环境/膜 | PFAS 去除 | ML + 分子模拟 | **精准缺口声明**（property-structure-performance relationship has not been established） |
| 1422 | Forecasting the eddying ocean with a deep neural network | ~NC/Science | 海洋预报 | 深度神经网络 | AI 模型谦逊定位句（stand on the shoulders of numerical models） |
| 1538 | AI-powered spatiotemporal imputation and prediction of chlorophyll-a … | ~NC/环境 | 叶绿素预测 | 时空插补 AI | 时空缺失值处理、验证证据 |
| 1737 | Uncertainty-aware machine learning to predict non-cancer human toxicity … | ~环境/化学 | 毒性预测 | 不确定性感知 ML | **权衡(trade-off)句式**（minor decrease in accuracy while enabling…） |
| 1824 | Species distribution models are inappropriate for COVID-19 | ~NEE 评论 | SDM 误用批判 | Perspective/Commentary | **观点文结构**：让步→转折→分层论证→强结语、高密度引用 |
| 1855 | Geostationary Ocean Flow (GOFLOW): submesoscale surface currents … | ~NG/遥感 | 海表流场 | 地球静止卫星反演 | 多数据源交叉验证、观测约束 |
| 1994 | Satellite mapping reveals extensive industrial activity at sea | ~Nature | 海上工业活动 | 卫星 + 深度学习 | 强结论句（reveal previously undocumented…）、全球尺度叙事 |
| 2152 | A local-to-global emissions inventory of macroplastic pollution | ~NC/环境 | 大塑料排放清单 | 自下而上清单 | 局地到全球缩放逻辑、清单方法 |

## 按用途快速选范本

- **写 Abstract**：正刊叙事型 → 行135 / 行669；NC 指标密集型 → 行227 / 行1048。
- **写因果链 Introduction（NCC）**：行422。
- **写突破性发现（NG）**：行669 / 行1855。
- **写精准研究缺口句**：行1318 / 行422。
- **写观点/评论文（NEE Perspective）**：行1824。
- **写局限性 + 不确定性**：行536 / 行1737。
- **写 Methods 复现细节（SDM/ML）**：行1 / 行930 / 行1318。
- **写政策/管理建议（NS 风格）**：行733。
