# 🎮 欢乐斗地主 - Unity 完整游戏

完整的单机斗地主游戏，支持玩家 vs 两个AI。

## 📁 项目文件

### 核心脚本 (Core)
- **Card.cs** - 卡牌定义（花色、点数、牌力值）
- **CardDeck.cs** - 牌堆管理（生成54张牌、洗牌、发牌）
- **CardHand.cs** - 手牌管理（排序、选牌）
- **GameManager.cs** - 游戏主控制（流程、回合、胜负）
- **GameRules.cs** - 游戏规则（牌型识别、大小比较）
- **GameTester.cs** - 游戏测试工具

### 玩家脚本 (Player)
- **Player.cs** - 玩家基类

### AI脚本 (AI)
- **AIPlayer.cs** - AI电脑玩家（自动出牌逻辑）

### UI脚本 (UI)
- **CardUI.cs** - 卡牌UI（点击选择）
- **GameTable.cs** - 游戏桌面管理
- **UIManager.cs** - UI管理器（界面切换、按钮事件）
- **CardSpriteManager.cs** - 卡牌图片管理

### 场景
- **DouDiZhuGame.unity** - 主游戏场景

## 🎮 游戏规则

### 牌型（从大到小）
1. **王炸** - 大王+小王（最大）
2. **炸弹** - 4张相同点数的牌
3. **单张** - 任意一张牌
4. **对子** - 2张相同点数的牌
5. **三张** - 3张相同点数的牌
6. **三带一** - 三张 + 单张
7. **三带二** - 三张 + 对子
8. **顺子** - 5张及以上连续单张（不含2和王）
9. **连对** - 3对及以上连续对子（不含2和王）
10. **飞机** - 两个及以上连续三张

### 牌力值
```
3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A < 2 < 小王 < 大王
1   2   3   4   5   6   7   8    9   10  11  12  13   14     15
```

### 游戏流程
1. **发牌** - 每人17张，留3张底牌
2. **叫地主** - 玩家选择是否叫地主
3. **确定地主** - 叫地主的玩家获得底牌
4. **出牌** - 地主先出，轮流出牌
5. **胜负** - 先出完牌的一方获胜

## 🚀 快速开始

### 1. 打开场景
```
Assets/TestAI/DouDiZhuGame.unity
```

### 2. 场景设置
参考 `DouDiZhu_SceneSetup.md` 完成详细设置。

### 3. 运行游戏
- 点击 Play 按钮
- 按 **空格键** 或点击 **开始游戏** 按钮

### 4. 操作说明
- **点击卡牌** - 选择/取消选择
- **出牌** - 点击"出牌"按钮
- **不出** - 点击"不出"按钮
- **提示** - 点击"提示"按钮

## 📝 代码命名空间

所有代码都在 `DDZ` 命名空间下：

```csharp
using DDZ;

public class MyScript : MonoBehaviour
{
    void Start()
    {
        Card card = new Card(CardSuit.Spades, CardRank.Ace);
        GameManager game = FindObjectOfType<GameManager>();
    }
}
```

## 🎯 测试功能

按 **T** 键运行测试：
- 牌堆初始化测试
- 洗牌测试
- 发牌测试
- 牌型识别测试

按 **D** 键打印调试信息：
- 当前游戏状态
- 当前玩家
- 地主信息

## 🐛 调试模式

在 GameTester 脚本中开启：
```csharp
public bool DebugMode = true;
```

将打印详细的卡牌信息和测试结果。

## 🎨 美术资源（可选）

如需美化，可添加：
- 卡牌图片（54张 + 背面）
- 游戏背景
- 按钮样式
- 音效

## 📋 已实现功能

- [x] 完整的卡牌系统
- [x] 洗牌和发牌
- [x] 叫地主流程
- [x] 回合制出牌
- [x] 牌型识别（单张、对子、三张、炸弹、王炸、顺子、连对、飞机）
- [x] 大小比较
- [x] AI自动出牌
- [x] UI管理
- [x] 胜负判定
- [x] 测试工具

## 🔧 技术细节

### Card 类
```csharp
public class Card
{
    public CardSuit Suit;    // 花色
    public CardRank Rank;    // 点数
    public int Value;        // 牌力值 (1-15)
}
```

### 游戏状态机
```csharp
public enum GameState 
{ 
    Idle,              // 空闲
    Dealing,           // 发牌中
    CallingLandlord,   // 叫地主
    Playing,           // 出牌中
    GameOver           // 游戏结束
}
```

### AI算法
- 随机叫地主
- 选择最小可管上的牌
- 优先出单张和对子
- 保留炸弹

## 📚 参考文档

- `DouDiZhu_DevGuide.md` - 开发指南
- `DouDiZhu_SceneSetup.md` - 场景设置指南

## 🎮 游戏截图

（待添加）

---
**版本**: 1.0  
**作者**: AI Assistant  
**日期**: 2026-02-11
