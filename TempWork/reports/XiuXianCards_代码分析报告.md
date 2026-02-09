# 修仙卡牌游戏 (XiuXianCards) - 核心功能总结报告

## 一、项目概述

这是一个基于 Unity 开发的修仙主题集换式卡牌游戏 (TCG)，采用数据驱动架构设计。游戏支持单人对战AI、本地多人、在线P2P对战和专用服务器模式。核心玩法围绕卡牌召唤、法术释放、装备系统和技能连锁展开，融入了修仙题材的特色元素（如飞行、冻结、加速等状态效果）。

### 主要特性
- **卡牌类型**：英雄(Hero)、角色(Character)、法术(Spell)、神器(Artifact)、秘密(Secret)、装备(Equipment)
- **状态系统**：冻结、加速、减速、飞行、翻面、多重触发等修仙特色状态
- **游戏模式**：单人冒险、AI对战、在线匹配、观战模式
- **网络架构**：支持离线模式、P2P主机、专用服务器

---

## 二、核心架构分析

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        表现层 (UI/FX)                        │
│              (CardUI, GameBoard, FX, Animations)              │
├─────────────────────────────────────────────────────────────┤
│                       客户端 (GameClient)                     │
│         (网络消息接收、游戏数据同步、用户输入处理)              │
├─────────────────────────────────────────────────────────────┤
│                      服务器 (GameServer)                      │
│      (游戏逻辑执行、AI控制、状态同步、匹配管理)                │
├─────────────────────────────────────────────────────────────┤
│                       游戏逻辑 (GameLogic)                    │
│     (回合管理、卡牌操作、战斗结算、能力触发)                   │
├─────────────────────────────────────────────────────────────┤
│                      数据层 (Data/Resources)                  │
│  (CardData, AbilityData, EffectData, ConditionData, etc.)   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 关键设计模式

1. **数据驱动设计**：所有卡牌、能力、效果均通过 ScriptableObject 配置
2. **组件化效果系统**：效果、条件、过滤器均可独立配置和组合
3. **事件驱动架构**：使用 UnityEvent 和委托处理游戏事件
4. **对象池模式**：AI计算和特效使用对象池优化性能
5. **状态机模式**：游戏状态、回合阶段使用枚举状态机管理

---

## 三、各模块功能详解

### 3.1 AI系统

#### 3.1.1 架构设计

| 类名 | 功能 |
|------|------|
| `AIPlayer` | AI玩家基类，定义AI更新接口 |
| `AIPlayerRandom` | 随机AI，用于测试 |
| `AIPlayerMM` | Minimax算法AI，主要对战AI |
| `AILogic` | 核心AI逻辑，实现Minimax算法 |
| `AIHeuristic` | 启发式评估函数 |

#### 3.1.2 Minimax算法实现

```csharp
// 核心参数
ai_depth = 3;           // 搜索深度（回合数）
ai_depth_wide = 1;      // 宽搜索深度
actions_per_turn = 2;   // 每回合最大行动数
nodes_per_action = 4;   // 每个行动评估节点数

// Alpha-Beta剪枝优化
- AI玩家：最大化启发值，更新alpha
- 对手玩家：最小化启发值，更新beta
- 剪枝条件：alpha >= beta
```

#### 3.1.3 启发式评估

评估因素包括：
- 场上卡牌价值 (board_card_value = 20)
- 手牌价值 (hand_card_value = 5)
- 玩家HP价值 (player_hp_value = 4)
- 卡牌攻击力/生命值
- 状态效果价值
- 击杀奖励

AI等级1-10通过 `heuristic_modifier` 随机扰动实现，等级越低随机性越大。

---

### 3.2 网络系统

#### 3.2.1 架构层次

```
┌─────────────────────────────────────┐
│          TcgNetwork                 │  ← 网络管理主类
│  (连接管理、消息路由、状态监控)        │
├─────────────────────────────────────┤
│         NetworkMessaging            │  ← 消息收发层
│    (消息监听、发送、序列化)            │
├─────────────────────────────────────┤
│         TcgTransport                │  ← 传输层封装
│      (Unity Netcode Transport)      │
├─────────────────────────────────────┤
│         Authenticator               │  ← 认证层
│   (Local/API/Test 三种模式)          │
└─────────────────────────────────────┘
```

#### 3.2.2 消息类型

**客户端→服务器 (Commands)**：
- `PlayCard` - 打出卡牌
- `Attack` / `AttackPlayer` - 攻击
- `CastAbility` - 施放能力
- `SelectCard/Player/Slot/Choice` - 选择目标
- `EndTurn` - 结束回合

**服务器→客户端 (Refresh)**：
- `RefreshAll` - 全量数据同步
- `CardPlayed` / `CardSummoned` - 卡牌事件
- `AbilityTrigger` / `AbilityTargetX` - 能力事件
- `AttackStart` / `AttackEnd` - 攻击事件

#### 3.2.3 游戏服务器 (GameServer)

- **游戏生命周期管理**：创建、开始、结束、超时处理
- **玩家管理**：连接、断开、准备状态、AI玩家
- **命令队列**：解析并执行客户端命令
- **状态同步**：向所有客户端广播游戏状态

---

### 3.3 条件系统 (Condition System)

#### 3.3.1 设计原理

条件系统用于判断能力是否可以触发或目标是否合法。采用**策略模式**，每种条件继承 `ConditionData` 基类。

#### 3.3.2 条件类型

| 条件类 | 功能 |
|--------|------|
| `ConditionCardType` | 卡牌类型、阵营、特性检查 |
| `ConditionCardPile` | 卡牌所在区域检查（手牌/场上/牌库等） |
| `ConditionStat` | 属性值比较（攻击/生命/法力） |
| `ConditionStatus` | 状态效果检查 |
| `ConditionSlotEmpty` | 空位检查 |
| `ConditionSlotRange` | 距离/范围检查 |
| `ConditionTurn` | 回合数检查 |
| `ConditionOwner` | 所有者检查 |
| `ConditionTrait` | 特性检查 |

#### 3.3.3 比较操作符

```csharp
// 整数比较
Equal, NotEqual, GreaterEqual, LessEqual, Greater, Less

// 布尔比较
IsTrue, IsFalse
```

---

### 3.4 效果系统 (Effect System)

#### 3.4.1 设计原理

效果系统采用**多态+数据驱动**设计，每种效果继承 `EffectData` 基类，通过虚方法实现不同目标类型的效果。

#### 3.4.2 效果类型

| 效果类 | 功能 |
|--------|------|
| `EffectDamage` | 造成伤害 |
| `EffectHeal` | 治疗 |
| `EffectDraw` | 抽牌 |
| `EffectDiscard` | 弃牌 |
| `EffectSummon` | 召唤卡牌 |
| `EffectCreate` | 创建新卡 |
| `EffectTransform` | 变形 |
| `EffectAddStat` | 增减属性 |
| `EffectAddTrait` | 添加特性 |
| `EffectAddAbility` | 添加能力 |
| `EffectAddStatus` | 添加状态 |
| `EffectMana` | 法力操作 |
| `EffectAttack` | 强制攻击 |
| `EffectDestroy` | 摧毁卡牌 |
| `EffectSendPile` | 移动卡牌区域 |
| `EffectShuffle` | 洗牌 |
| `EffectRoll` | 随机骰子 |
| `EffectRepeat` | 重复效果 |

#### 3.4.3 效果执行流程

```csharp
// 1. 能力触发
ability.DoEffects(logic, caster);

// 2. 根据目标类型选择重载
effect.DoEffect(logic, ability, caster);           // 无目标
effect.DoEffect(logic, ability, caster, target);   // 卡牌目标
effect.DoEffect(logic, ability, caster, player);   // 玩家目标
effect.DoEffect(logic, ability, caster, slot);     // 位置目标

// 3. 持续效果 (Ongoing)
effect.DoOngoingEffect(logic, ability, caster, target);
```

---

### 3.5 能力系统 (Ability System)

#### 3.5.1 能力数据结构

```csharp
public class AbilityData : ScriptableObject
{
    public AbilityTrigger trigger;          // 触发时机
    public ConditionData[] conditions_trigger;  // 触发条件
    public AbilityTarget target;            // 目标类型
    public ConditionData[] conditions_target;   // 目标条件
    public FilterData[] filters_target;     // 目标过滤器
    public EffectData[] effects;            // 效果列表
    public StatusData[] status;             // 附加状态
    public AbilityData[] chain_abilities;   // 连锁能力
    public int mana_cost;                   // 法力消耗
    public bool exhaust;                    // 是否消耗行动
}
```

#### 3.5.2 触发时机 (AbilityTrigger)

| 触发时机 | 说明 |
|----------|------|
| `Ongoing` | 持续生效 |
| `Activate` | 主动激活 |
| `OnPlay` | 打出时 |
| `OnPlayOther` | 其他卡牌打出时 |
| `StartOfTurn` / `EndOfTurn` | 回合开始/结束 |
| `OnBeforeAttack` / `OnAfterAttack` | 攻击前/后 |
| `OnBeforeDefend` / `OnAfterDefend` | 被攻击前/后 |
| `OnKill` | 击杀时 |
| `OnDeath` / `OnDeathOther` | 死亡/其他死亡 |

#### 3.5.3 目标类型 (AbilityTarget)

| 目标类型 | 说明 |
|----------|------|
| `Self` | 自身 |
| `PlayerSelf` / `PlayerOpponent` / `AllPlayers` | 玩家目标 |
| `AllCardsBoard` / `AllCardsHand` / `AllCardsAllPiles` | 卡牌群体 |
| `SelectTarget` | 选择目标（需要玩家选择） |
| `CardSelector` | 卡牌选择器 |
| `ChoiceSelector` | 选项选择器 |
| `PlayTarget` | 打出目标 |
| `LastPlayed` / `LastDestroyed` / `LastTargeted` | 最近卡牌引用 |

---

### 3.6 数据系统

#### 3.6.1 卡牌数据 (CardData)

```csharp
public class CardData : ScriptableObject
{
    public string id;
    public string title;
    public CardType type;           // 卡牌类型
    public TeamData team;           // 阵营
    public RarityData rarity;       // 稀有度
    public int mana;                // 法力消耗
    public int attack;              // 攻击力
    public int hp;                  // 生命值
    
    public TraitData[] traits;      // 特性
    public TraitStat[] stats;       // 属性值
    public AbilityData[] abilities; // 能力列表
    
    // 特效资源
    public GameObject spawn_fx, death_fx, attack_fx, damage_fx, idle_fx;
    public AudioClip spawn_audio, death_audio, attack_audio, damage_audio;
}
```

#### 3.6.2 运行时卡牌 (Card)

```csharp
public class Card
{
    public string card_id;      // 卡牌数据ID
    public string uid;          // 实例唯一ID
    public int player_id;       // 所属玩家
    public Slot slot;           // 所在位置
    public bool exhausted;      // 是否行动过
    public int damage;          // 已受伤害
    
    // 属性（基础+持续效果）
    public int mana, attack, hp;
    public int mana_ongoing, attack_ongoing, hp_ongoing;
    
    // 特性、状态、能力
    public List<CardTrait> traits, ongoing_traits;
    public List<CardStatus> status, ongoing_status;
    public List<string> abilities, abilities_ongoing;
    
    public string equipped_uid; // 装备UID
}
```

#### 3.6.3 玩家数据 (Player)

```csharp
public class Player
{
    public int player_id;
    public string username;
    public bool is_ai;
    public int ai_level;
    
    public int hp, hp_max;
    public int mana, mana_max;
    public int kill_count;
    
    // 卡牌区域
    public List<Card> cards_deck;      // 牌库
    public List<Card> cards_hand;      // 手牌
    public List<Card> cards_board;     // 场上
    public List<Card> cards_equip;     // 装备区
    public List<Card> cards_discard;   // 弃牌堆
    public List<Card> cards_secret;    // 秘密区
    public List<Card> cards_temp;      // 临时区
    
    public Card hero;  // 英雄卡
}
```

---

### 3.7 游戏逻辑系统 (GameLogic)

#### 3.7.1 核心职责

- **回合管理**：开始回合、主阶段、结束回合
- **资源管理**：抽牌、法力恢复
- **卡牌操作**：打出、移动、召唤、变形、弃置
- **战斗结算**：攻击、伤害、击杀
- **能力触发**：时机判断、条件检查、效果执行
- **选择器处理**：目标选择、卡牌选择、选项选择

#### 3.7.2 游戏流程

```
1. 游戏开始 (StartGame)
   └─ 设置玩家HP/法力
   └─ 抽起始手牌
   └─ 先手玩家获得硬币（如果是后手）
   └─ 触发游戏开始事件

2. 回合开始 (StartTurn)
   └─ 清除回合数据
   └─ 抽牌（每回合）
   └─ 增加法力上限
   └─ 重置法力
   └─ 触发回合开始事件
   └─ 进入主阶段

3. 主阶段 (Main Phase)
   └─ 玩家可以：
      ├─ 打出卡牌
      ├─ 攻击敌方卡牌/玩家
      ├─ 施放能力
      ├─ 移动卡牌（如规则允许）
      └─ 结束回合

4. 回合结束 (EndTurn)
   └─ 减少状态持续时间
   └─ 触发回合结束能力
   └─ 进入下一回合
```

---

### 3.8 UI系统

#### 3.8.1 主要UI组件

| 类名 | 功能 |
|------|------|
| `CardUI` | 卡牌显示组件 |
| `GameBoard` | 游戏主界面 |
| `HandCard` | 手牌显示 |
| `BoardCard` | 场上卡牌显示 |
| `PlayerControls` | 玩家控制面板 |
| `AbilityButton` | 能力按钮 |
| `ChatUI` | 聊天界面 |
| `CardSelector` | 卡牌选择器 |
| `ChoiceSelector` | 选项选择器 |

#### 3.8.2 菜单系统

| 类名 | 功能 |
|------|------|
| `MainMenu` | 主菜单 |
| `LoginMenu` | 登录界面 |
| `CollectionPanel` | 卡牌收藏 |
| `DeckLine` | 卡组列表项 |
| `MatchmakingPanel` | 匹配界面 |
| `AdventurePanel` | 冒险模式 |

---

## 四、关键技术亮点

### 4.1 数据驱动设计

**优势**：
- 卡牌、能力、效果全部可配置，无需修改代码
- 策划可以通过Unity Inspector配置新卡牌
- 支持热更新卡牌数据

**实现**：
```csharp
[CreateAssetMenu(fileName = "card", menuName = "TcgEngine/CardData")]
public class CardData : ScriptableObject { ... }

// 加载所有卡牌数据
public static void Load(string folder = "")
{
    card_list.AddRange(Resources.LoadAll<CardData>(folder));
    foreach (CardData card in card_list)
        card_dict.Add(card.id, card);
}
```

### 4.2 AI的Minimax+AlphaBeta剪枝

```csharp
// AI尝试最大化启发值
if (player_id == ai_player_id)
{
    if (child_node.hvalue > parent.hvalue)
    {
        parent.best_child = child_node;
        parent.hvalue = child_node.hvalue;
        parent.alpha = Mathf.Max(parent.alpha, parent.hvalue);
    }
}
// 对手尝试最小化启发值
else
{
    if (child_node.hvalue < parent.hvalue)
    {
        parent.best_child = child_node;
        parent.hvalue = child_node.hvalue;
        parent.beta = Mathf.Min(parent.beta, parent.hvalue);
    }
}

// Alpha-Beta剪枝
if (node.alpha >= node.beta) return;
```

### 4.3 网络同步机制

**状态同步策略**：
- 服务器权威：所有逻辑在服务器执行
- 增量同步：只发送变化的数据（如卡牌打出、攻击等事件）
- 全量同步：`RefreshAll` 定期同步完整游戏状态，防止客户端丢失同步

**消息队列**：
```csharp
// 解析中的动作排队，避免并发问题
if (gameplay.IsResolving())
{
    queued_actions.Enqueue(action);
}
else
{
    ExecuteAction(type, client, sdata);
}
```

### 4.4 效果系统的灵活性

**多态执行**：
```csharp
// 同一个能力可以对不同目标类型执行不同逻辑
public override void DoEffect(GameLogic logic, AbilityData ability, Card caster, Card target)
public override void DoEffect(GameLogic logic, AbilityData ability, Card caster, Player target)
public override void DoEffect(GameLogic logic, AbilityData ability, Card caster, Slot target)
```

**效果组合**：
- 通过数组配置多个效果
- 支持效果连锁（chain_abilities）
- 支持条件过滤和排序

### 4.5 状态效果的持续与临时

```csharp
// 持续效果（Ongoing）vs 临时效果（Status）
public List<CardStatus> status;         // 有持续时间的状态
public List<CardStatus> ongoing_status; // 持续生效的状态（如光环）

// 回合结束减少持续时间
public virtual void ReduceStatusDurations()
{
    for (int i = status.Count - 1; i >= 0; i--)
    {
        if (!status[i].permanent)
        {
            status[i].duration -= 1;
            if (status[i].duration <= 0)
                status.RemoveAt(i);
        }
    }
}
```

### 4.6 修仙特色状态系统

项目融入修仙主题的特色状态：

| 状态 | ID | 说明 |
|------|-----|------|
| 冻结 | Frozen | 无法行动 |
| 加速 | SpeedUp | 行动加速 |
| 减速 | SpeedDown | 行动减缓 |
| 飞行 | Flying | 可越过障碍 |
| 翻面 | FlipOver | 隐藏/显示 |
| 多重触发 | MultiActing | 多次触发能力 |

---

## 五、总结

这个修仙卡牌游戏项目具有以下特点：

1. **架构清晰**：数据层、逻辑层、网络层、表现层分离明确
2. **高度可配置**：几乎所有游戏内容都可通过ScriptableObject配置
3. **AI智能**：采用Minimax+AlphaBeta剪枝算法，支持多级难度
4. **网络完善**：支持离线、P2P、专用服务器多种模式
5. **扩展性强**：效果、条件、过滤器均可独立扩展
6. **修仙特色**：融入了中国修仙文化元素的状态系统

项目代码质量较高，使用了多种设计模式，结构清晰，易于维护和扩展。

---

*报告生成时间：2026-02-10*
*分析文件数：236个C#文件（核心模块约25个）*
