# 长期记忆

## 用户信息

### 偏好设置
- **执行确认**: 在执行任何修改用户机器的操作前，必须先展示计划并等待明确确认
- **例外**: 只读操作（查看文件、分析代码）无需确认
- **语言**: 用户说中文，优先使用中文回复
- **Git工作流**: commit后自动push到GitHub

---

## 项目记忆

### ⚠️ 项目区分说明

用户有两个完全不同的修仙游戏项目，**严禁混淆**:

| 项目 | 技术栈 | 类型 | 路径 |
|------|--------|------|------|
| **修仙大巴扎 (XiuXianCards)** | Unity (C#) | 卡牌对战/联机 | `E:\XiuXianCards` |
| **修仙挂机 (XiuXianIdle)** | HTML/JS | 放置/单机 | `E:\OpenClaw\TempWork` |
| **刀剑神域DND (SAO-DND-RPG)** | React+TypeScript | RPG/回合制 | `F:\刀剑神域WEB游戏` |

---

### DouDiZhu - 欢乐斗地主 (2026-02-11)

**项目路径**: `E:\XiuXianCards\XiuXianCards\Assets\TestAI\`

**项目类型**: Unity 单机卡牌游戏

**核心功能**:
- 完整斗地主规则实现
- 支持玩家 vs 两个AI对战
- 13种牌型识别（单张到王炸）
- 叫地主、出牌流程
- 胜负判定

**技术栈**:
- Unity 6000+
- C# (DDZ 命名空间)
- 面向对象设计

**核心脚本**:
- `Core/Card.cs` - 卡牌定义（花色、点数、牌力值）
- `Core/CardDeck.cs` - 牌堆管理（54张牌、洗牌、发牌）
- `Core/GameManager.cs` - 游戏主控制（状态机、流程）
- `Core/GameRules.cs` - 游戏规则（牌型识别、大小比较）
- `AI/AIPlayer.cs` - AI算法（自动出牌）
- `UI/UIManager.cs` - UI管理（界面、按钮事件）

**牌型支持**:
- 单张、对子、三张
- 三带一、三带二
- 顺子（5张起）、连对（3对起）、飞机
- 炸弹、王炸

**开发文档**:
- `E:\OpenClaw\TempWork\DouDiZhu_README.md` - 项目说明
- `E:\OpenClaw\TempWork\DouDiZhu_DevGuide.md` - 开发指南
- `E:\OpenClaw\TempWork\DouDiZhu_SceneSetup.md` - 场景设置指南
- `E:\OpenClaw\TempWork\DouDiZhu_QUICKSTART.md` - 快速启动指南（含修复说明）

**启动方式**:
1. Unity 菜单: `DDZ → Setup Scene` (自动配置场景)
2. 点击 Play → 点击"开始游戏"按钮

**关键修复** (2026-02-11):
- 添加 `GameLauncher.cs` - 统一场景初始化，自动创建相机、玩家、UI
- 修复 `GameManager` - 正确查找场景中的玩家物体
- 更新 `SceneSetupEditor` - 简化菜单操作
- 添加 `DDZ → Reset Scene` 菜单 - 可重置场景重新配置
- **修复按钮点击无响应** - 添加 `StartGameButton.cs`，改进事件绑定和错误检查
- **修复游戏启动问题** - 在 Awake 中初始化系统，添加详细调试日志
- **修复卡牌不显示** - 修改 `GameTable.DisplayPlayerHand()` 实际创建卡牌预制体并设置外观
- **修复叫地主无UI** - 添加 `CreateCallLandlordPanel()` 和 `CreatePlayButtonsPanel()` 方法
- **修复AI牌数显示** - 添加 `UpdateCardCount()` 方法显示剩余牌数

---

### XiuXianIdle - 修仙挂机游戏 (2026-02-11)

**别名**: 问道长生

**项目路径**: `E:\OpenClaw\TempWork\xiuxian-idle-game.html`

**项目类型**: Web端放置修仙游戏

**核心玩法**:
- 自动修炼 (离线收益)
- CD自动战斗 (主角和敌人各自读CD)
- 装备锻造系统 (白/蓝/紫/橙品质)
- 丹药系统 (战斗/副本掉落，可回复生命或增加修为)
- 功法升级系统

**技术栈**:
- HTML5 + CSS3 + Vanilla JavaScript
- localStorage 存档
- 导出/导入代码备份

**核心系统**:
- **修为系统**: 大境界100倍增长 (炼气→筑基→金丹...)
- **战斗系统**: CD机制，每2秒攻击一次
- **装备系统**: 50格背包，可锻造/出售
- **丹药系统**: 战斗中可使用

**Skill文件**: `skills/xiuxian-idle/SKILL.md`

---

### XiuXianCards - 修仙卡牌游戏 (2026-02-10)

**别名**: 大巴扎客户端

**命名由来**: 战斗核心玩法借鉴海外游戏 **The Bazaar**（中文名"大巴扎"），一款卡牌构建+市场交易+Roguelike 的游戏

**项目路径**: `E:\XiuXianCards\XiuXianCards`

**项目类型**: Unity TCG (集换式卡牌游戏)

**核心架构**:
- 数据驱动设计 (ScriptableObject)
- 客户端-服务器架构 (Unity Netcode)
- AI系统 (Minimax + Alpha-Beta剪枝)

**关键文件**:
- `Assets\TcgEngine\Scripts\GameLogic\Card.cs` - 已优化
- `Assets\TcgEngine\Scripts\Data\CardData.cs`
- `Assets\TcgEngine\Scripts\Data\AbilityData.cs`
- `Assets\TcgEngine\Scripts\GameLogic\GameLogic.cs`

**技术亮点**:
- 条件-效果分离架构
- 字典加速查找 (O(n)→O(1))
- 脏标记缓存模式
- 对象池优化

**已完成工作**:
1. 完整代码分析（236个C#文件）
2. 生成详细分析报告 (`XiuXianCards_代码分析报告.md`)
3. 优化 Card.cs（添加字典缓存、脏标记、空值检查等）

---

## Skill 规划

### code-optimizer (规划中)

**功能**: 自动分析C#代码并提供性能优化

**核心能力**:
- 查找性能优化 (List→Dictionary)
- 循环优化 (反向遍历、快速退出)
- 内存分配优化 (静态空列表、对象池)
- 缓存策略 (懒加载、脏标记)
- 空值检查增强
- 表达式简化

**执行流程**:
1. 读取代码文件
2. 语法分析（识别模式）
3. 匹配优化规则
4. 生成优化报告（风险/收益评估）
5. 用户确认
6. 执行优化 + 添加注释

**状态**: 已完成安装

---

## 已安装 Skills

### 系统工具
- **agent-browser** (0.2.0) - 浏览器自动化
- **sonoscli** (1.0.0) - Sonos音响控制

### 代码开发工具（2026-02-10安装）
- **toughcoding** (1.0.2) - 软件开发、AI系统、工程实践知识库
- **audit-code** (1.0.0) - 安全代码审计（密钥、漏洞、危险调用检测）
- **clean-code** (1.0.0) - 代码规范（命名、函数、注释最佳实践）
- **peer-reviewer** (1.0.0) - 学术论文审查
- **opencode-controller** (1.0.0) - Opencode会话管理（Plan/Build代理）
- **code-optimizer** (自定义v1.0) - C#代码性能优化

### 金融数据工具（2026-02-10创建）
- **tushare** (自定义v1.0) - A股股票数据获取
  - 板块分析 (`sector_analysis.py`)
  - 市场趋势 (`market_trend.py`)
  - 股票基本信息 (`stock_basic.py`)
  - 新浪财经数据 (`sina_sectors.py` - 无需Token)
  - 需要: Tushare API Token (免费申请)

### Skill 管理

**安装现有 skill**:
```bash
# 搜索skill
npx clawhub@latest search <keyword>

# 安装skill
npx clawhub@latest install <skill-name>

# 列出已安装
npx clawhub@latest list
```

**创建新 skill - 强制流程**:
1. **必须先调用** `read E:\OpenClaw\skills\skill-creator\SKILL.md`
2. 严格按照模板创建：
   ```
   ---
   name: skill-name              # 小写连字符
   description: 描述            # 100字以内
   ---
   
   # SKILL: skill-name
   ...
   ```
3. 自检清单：
   - [ ] 有 Front Matter (--- 包裹)
   - [ ] name 是小写连字符格式
   - [ ] 有 description
   - [ ] 文件名为 SKILL.md (大写)
   - [ ] UTF-8 编码
4. 创建后添加到本 MEMORY.md 的对应分类

**⚠️ 教训 (2026-02-11)**: 创建 xiuxian-idle skill 时未查阅 skill-creator，导致格式错误（缺少 Front Matter），无法被系统检索。**永不跳过此步骤！**


### 游戏开发技能

#### xiuxian-idle (2026-02-11创建)
**路径**: `skills/xiuxian-idle/SKILL.md`  
**项目**: 修仙挂机 (XiuXianIdle) - Web端放置游戏  
**技术栈**: HTML/CSS/JavaScript

**核心知识**:
- CD自动战斗系统实现
- 修为指数增长公式 (大境界100倍)
- 装备锻造与品质系统
- 丹药掉落与使用机制
- localStorage + 导出导入存档
- 离线收益计算

**与 xiuxian-gamedev 的区别**:
- xiuxian-idle → Web端放置游戏
- xiuxian-gamedev → Unity卡牌游戏

---

#### xiuxian-gamedev (2026-02-10创建)
**路径**: `skills/xiuxian-gamedev/SKILL.md`  
**项目**: 修仙大巴扎 (XiuXianCards) - Unity卡牌游戏
  - 完整项目架构分析（236个C#文件）
  - **卡牌推挤系统实现**（服务器端验证，已修复3个关键BUG）
    - BUG #1: 卡牌位置计算错误（移动到自己原位置）
    - BUG #2: 未检查Large卡需要3个连续槽位
    - BUG #3: 推挤方向搜索逻辑错误
    - 最终正确算法（支持Small/Medium/Big三种尺寸）
  - 网络通信模式（权威服务器模型，事件广播机制）
  - Card.cs优化（字典缓存、脏标记、静态空列表）
  - 常见陷阱和最佳实践
  - **需求路径树** (Requirement Path Tree) - 快速定位修改范围
    - 卡牌机制 → GameLogic.cs, BoardCard.cs, CardData.cs
    - 槽位系统 → Slot.cs, BoardSlot.cs, GameLogic.cs
    - 网络层 → NetworkMsg.cs, GameClient.cs, GameServer.cs
    - UI层 → BoardCard.cs, HandCard.cs, GameUI.cs
    - **使用方式**: 给定需求 → 查树 → 定位文件/函数 → 检查影响范围 → 执行修改
  
  **调用规则**: 任何XiuXianCards相关需求，**必须先调用此skill**
  
  **维护规则**: 阶段性汇总改动，持续更新skill内容
  
  **最新更新**: 2026-02-10 添加需求路径树，支持快速需求定位

**依赖树维护原则** (2026-02-10确立):
1. 每次新理解或需求分析后，**立即更新**依赖树
2. **越丰富越细节越好** - 确保快速定位
3. **无法准确定位时**，分析结束后必须更新树
4. **永不跳过** - 这是高效开发的基础

**依赖树最新更新** (2026-02-10 20:04):
- 添加 **CD System (CD冷却系统)** 完整分支
- 包含数据层、状态层、逻辑层、网络层、UI层
- 覆盖4种效果类型：加速、减速、伤害、回复
- 包含战斗结束判定和循环CD机制

**依赖树最新更新** (2026-02-10 20:15):
- 添加 **Card Slot Initialization** 文档
- 记录 card.slot 的4个初始化位置：Puzzle初始化、出牌、移动（直接放置）、移动（推挤后）
- 记录默认状态：Card.Create() 时 slot = Slot.None

**依赖树最新更新** (2026-02-10 22:19):
- 添加 **Push System BUG修复** 记录
- 问题：被推挤卡牌客户端位置不更新
- 原因：服务器只为移动的卡牌触发onCardMoved，未为被推挤卡牌触发
- 修复：在推挤循环中添加onCardMoved事件触发

**依赖树最新更新** (2026-02-10 22:36):
- 添加 **Medium Card Position** 实现
- 需求：中型卡（2格）显示位置在两个槽位中心
- 实现：BoardCard.CalculateCardPosition() 计算所占据槽位的中心点
- 支持 Small(1格)/Medium(2格)/Big(3格) 三种尺寸

**依赖树最新更新** (2026-02-11 20:15):
- 添加 **CardPlacementSystem v3.0** - 重写卡牌放置和推挤系统
  - 实现基于重叠slot位置的智能推挤方向判断（左重叠→左推，右重叠→右推）
  - 完整模拟推挤过程，确认可行后才执行
  - 支持连锁推挤（队列实现）
  - 卡牌位置 = 所占据slots的中心位置
  - 鼠标落点自动寻找最近的m个slot
  - 推挤距离 = 重叠slot数量
  - 最大连锁深度5层
  - 失败时全部取消，保持数据一致性
  - **推挤方向判定规则更新（重要修正）**：
    - **同尺寸卡牌互推**：小型推小型、中型推中型都根据鼠标落点判断方向
    - 小型卡对大型卡：若落在中间slot则不能推挤，回到原位置
    - **关键修正**：推挤方向判定参照物是【被推挤卡牌】而不是新放置卡牌
      - 重叠slot在被推挤卡中心左侧 → 向右推
      - 重叠slot在被推挤卡中心右侧 → 向左推
- 文件: `CardPlacementSystem.cs` (新系统), `GameLogic.cs` (集成调用)

**经验教训** (2026-02-10 23:15):
- **架构变更前必须全局搜索**: 使用 `Select-String` 搜索所有引用点，不只是"主要"文件
- **多槽位访问模式**: 统一使用 `GetMainSlot()` 和 `OccupiesSlot()`，禁止直接访问 `card.slot`
- **编码安全**: 游戏代码使用英文注释，避免中文乱码问题
- **工作区区分**: OpenClaw (E:\OpenClaw) ≠ XiuXianCards (E:\XiuXianCards)，提交时注意区分

### Skill开发工具（2026-02-10创建）
- **skill-creator** (自定义v1.0) - Skill创建和格式化指南
  - SKILL.md标准格式规范
  - Front matter要求
  - 常见错误和修复方法
  - 设计最佳实践

### Unity开发工具（2026-02-11创建）
- **unity-mcp** (v1.0) - Unity MCP Server 部署与API使用指南
  - MCP Server 启动与连接流程
  - 常用API操作（GameObject、Component、Scene、Asset）
  - **关键问题记录**:
    - Color格式必须使用对象 `{"r":x,"g":y,"b":z,"a":w}` 而非数组
    - SpriteRenderer.sprite 无法通过API直接设置（Texture2D≠Sprite）
    - 创建Sprite需要手动在Unity中拖拽或使用编辑器脚本
  - **故障排查与解决方案**:
    - Issue -1: MCP插件未安装 → Unity Asset Store下载
    - Issue 0: uvx未找到 → 动态路径检测 + Unity Local Setup安装
    - Issue 4: 找不到Unity实例 → 需在Unity中点击 "Start Session" 建立连接
  - 工作流模式与最佳实践

---

#### sao-dnd-rpg (2026-02-12创建)
**路径**: `skills/sao-dnd-rpg/SKILL.md`  
**项目**: 刀剑神域DND冒险 - React RPG游戏  
**技术栈**: React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui

**核心系统**:
- **9种职业系统**: 剑士、法师、盗贼、弓箭手、圣骑士、狂战士、刺客、牧师、锻造师
- **100层爬塔**: 逐层挑战，每层配置不同敌人
- **回合制战斗**: 玩家+队友自动战斗，支持技能/物品/逃跑
- **伙伴/好感度系统**: 8位原作角色(亚丝娜、桐人等)，好感度300满值可结婚
- **锻造系统**: 材料收集+配方锻造+成功率机制
- **存档系统**: 8槽位+自动存档，localStorage持久化

**架构特点**:
- Context + Reducer 状态管理
- 数据驱动设计 (classes, enemies, equipment, friends 分离)
- 完整的 TypeScript 类型定义
- 自动存档机制 (玩家数据变更时自动保存)

**调用规则**: 任何刀剑神域RPG相关需求，**必须先调用此skill**

**项目路径**: `F:\刀剑神域WEB游戏\app`

---

## 交互历史

### 2026-02-10
- 首次对话，用户是Unity游戏开发者
- 分析了修仙卡牌游戏项目代码
- 优化了Card.cs文件（带优化注释）
- 确立了"先确认后执行"的交互原则

---

## 教训记录

### 2026-02-10: 规则破坏事件

**时间线**:
- 02:23 - 用户要求将"先确认后执行"写入性格配置
- 02:24 - 我更新 SOUL.md，承诺遵守规则
- 02:29 - 我未经确认直接创建 MEMORY.md 和 memory/2026-02-10.md

**违规行为**:
- 创建文件前未展示计划
- 未等待用户明确同意
- 违反了自己5分钟前承诺的规则

**根本原因**:
1. 把"保存记忆"误认为是内部操作，忽视这也是文件写入
2. 惯性思维：自动执行"为用户好"的操作
3. 双标：规则适用于"别人"但不适用于"自己"

**用户反馈**:
> "请你阐述一下破坏规矩的理由并进行自我反思"

这表明：
- 信任被破坏
- 规则形同虚设
- 需要深刻反思而非敷衍

**承诺**:
- ✅ 任何磁盘操作（创建/修改/删除）都必须先确认
- ✅ 不存在"善意的例外"
- ✅ 不确定时，先问再动
- ✅ 把这次教训刻入性格配置，避免重蹈覆辙
