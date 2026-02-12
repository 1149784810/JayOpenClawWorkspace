# 欢乐斗地主 - Unity 项目开发指南

> **命名空间**: 所有代码都在 `DDZ` 命名空间下，避免与其他代码冲突。

```csharp
namespace DDZ
{
    public class Card { ... }
}
```

## 📁 项目结构

```
Assets/TestAI/
├── Scripts/
│   ├── Core/
│   │   ├── Card.cs         - 单张卡牌定义 (花色、点数、牌力值)
│   │   ├── CardDeck.cs     - 牌堆管理 (生成、洗牌、发牌)
│   │   ├── CardHand.cs     - 手牌管理 (排序、选牌、出牌)
│   │   ├── GameManager.cs  - 游戏主控制 (流程、回合、胜负)
│   │   └── GameRules.cs    - 游戏规则验证 (牌型、大小比较)
│   ├── Player/
│   │   └── Player.cs       - 玩家基类
│   ├── AI/
│   │   └── AIPlayer.cs     - AI电脑玩家
│   └── UI/
│       ├── CardUI.cs       - 卡牌显示控制
│       └── GameTable.cs    - 游戏桌面UI
├── Sprites/
│   ├── Cards/              - 卡牌图片资源
│   └── UI/                 - 界面图片资源
├── Prefabs/                - 预制体
├── Audio/                  - 音频资源
├── Resources/              - 资源文件
└── DouDiZhuGame.unity     - 主场景
```

## 🎮 场景结构

已创建的场景物体:
- **Table_Background** - 游戏桌面背景
- **PlayerHand_Area** - 玩家手牌区域 (底部)
- **AI_Left_Area** - 左侧AI玩家区域
- **AI_Right_Area** - 右侧AI玩家区域
- **PlayArea_Center** - 中央出牌区域
- **GameController** - 游戏控制管理器

## 📝 下一步开发任务

### 1. 完善 Card.cs
```csharp
namespace DouDiZhu
{
    public enum CardSuit { Spades, Hearts, Clubs, Diamonds, None }
    public enum CardRank 
    { 
        Three, Four, Five, Six, Seven, Eight, Nine, Ten, 
        Jack, Queen, King, Ace, Two, JokerSmall, JokerBig 
    }
    
    [System.Serializable]
    public class Card
    {
        public CardSuit Suit;
        public CardRank Rank;
        public int Value; // 牌力值 3=1 ... 大王=15
        
        // 构造函数、ToString() 等
    }
}
```

### 2. 实现 CardDeck.cs (牌堆)
```csharp
public class CardDeck : MonoBehaviour
{
    private List<Card> cards = new List<Card>();
    
    void Start()
    {
        InitializeDeck();
        Shuffle();
    }
    
    void InitializeDeck()
    {
        // 创建54张牌
        // 4种花色 x 13个点数 + 2张王牌
    }
    
    void Shuffle()
    {
        // 洗牌算法
    }
    
    public List<Card> Deal(int count)
    {
        // 发指定数量的牌
    }
}
```

### 3. 实现 GameRules.cs (规则验证)
支持的牌型:
- 单张
- 对子
- 三张
- 三带一
- 三带二
- 顺子 (5张起)
- 连对 (3对起)
- 飞机
- 炸弹 (4张)
- 王炸 (大小王)

### 4. 实现 GameManager.cs (游戏流程)
```csharp
public class GameManager : MonoBehaviour
{
    public enum GameState { Dealing, Calling, Playing, End }
    public GameState CurrentState;
    
    public Player[] Players; // 3个玩家
    public int CurrentPlayerIndex;
    public List<Card> LastPlayedCards;
    
    void Start()
    {
        StartGame();
    }
    
    void StartGame()
    {
        // 1. 洗牌发牌 (每人17张，留3张底牌)
        // 2. 叫地主
        // 3. 开始出牌回合
    }
}
```

### 5. 创建卡牌预制体
- 创建 Card.prefab
- 添加 SpriteRenderer
- 添加 BoxCollider2D (点击检测)
- 添加 CardUI 脚本

### 6. UI界面
需要制作的UI:
- [ ] 开始游戏按钮
- [ ] 叫地主/不叫按钮
- [ ] 出牌/不出/提示按钮
- [ ] 玩家信息显示 (头像、名字、剩余牌数)
- [ ] 牌型提示显示
- [ ] 游戏结果界面

## 🎨 美术资源需求

### 卡牌图片 (54张)
- 黑桃 ♠ A-K (13张)
- 红心 ♥ A-K (13张)
- 梅花 ♣ A-K (13张)
- 方块 ♦ A-K (13张)
- 小王、大王 (2张)
- 卡牌背面 (1张)

### UI图片
- 游戏桌面背景
- 按钮样式
- 玩家头像框
- 计时器

## 🔧 关键技术点

### 卡牌点击选择
```csharp
void OnMouseDown()
{
    isSelected = !isSelected;
    // 向上移动一点表示选中
    transform.position += isSelected ? Vector3.up * 0.5f : Vector3.down * 0.5f;
}
```

### 牌型判断
```csharp
public bool IsValidPlay(List<Card> cards, List<Card> lastPlay)
{
    // 1. 判断cards是什么牌型
    // 2. 与lastPlay比较大小
    // 3. 返回是否可出
}
```

### AI算法思路
```csharp
public List<Card> AIPlay(List<Card> hand, List<Card> lastPlay)
{
    // 简单AI策略:
    // 1. 如果能管上，选择最小的能管上的牌
    // 2. 如果管不上，选择不出
    // 3. 优先出单张、对子，保留炸弹
}
```

## 📋 开发检查清单

- [x] 创建项目结构
- [x] 创建基础脚本文件
- [x] 创建场景结构
- [ ] 完善 Card.cs 类
- [ ] 实现 CardDeck (洗牌发牌)
- [ ] 实现 GameRules (规则验证)
- [ ] 实现 GameManager (游戏流程)
- [ ] 制作卡牌预制体
- [ ] 实现 CardUI (卡牌交互)
- [ ] 制作基础UI界面
- [ ] 添加卡牌图片资源
- [ ] 测试单机游戏流程
- [ ] 优化AI算法

## 🚀 快速开始

1. 打开场景: `Assets/TestAI/DouDiZhuGame.unity`
2. 给 GameController 物体添加 GameManager 脚本
3. 在 PlayerHand_Area 下创建卡牌预制体
4. 运行测试

---
祝开发顺利！
