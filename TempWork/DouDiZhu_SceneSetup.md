# 斗地主游戏 - Unity 场景设置指南

## 🎮 场景设置步骤

### 1. 打开场景
- 打开 `Assets/TestAI/DouDiZhuGame.unity`

### 2. 设置 GameController 物体

**在 Hierarchy 中找到或创建 GameController 物体：**

添加以下组件：
- **GameManager** (Script)
- **CardDeck** (Script)

### 3. 创建卡牌预制体

**创建 Card.prefab：**

1. 在 Hierarchy 中创建空物体，命名为 `Card`
2. 添加 SpriteRenderer 组件
3. 添加 BoxCollider2D 组件（勾选 Is Trigger）
4. 添加 CardUI 脚本
5. 拖到 Project 窗口的 `Assets/TestAI/Prefabs` 文件夹中

**Card 物体结构：**
```
Card (GameObject)
├── SpriteRenderer
├── BoxCollider2D
└── CardUI (Script)
```

### 4. 设置 GameTable 物体

**在 GameController 或其他管理物体上添加 GameTable 脚本：**

配置引用：
- PlayerHandArea → 拖拽 PlayerHand_Area 物体
- LeftAIArea → 拖拽 AI_Left_Area 物体
- RightAIArea → 拖拽 AI_Right_Area 物体
- PlayArea → 拖拽 PlayArea_Center 物体
- CardPrefab → 拖拽 Card 预制体

### 5. 设置 UI

**创建 Canvas：**

1. 右键 → UI → Canvas
2. 设置 Render Mode: Screen Space - Overlay

**创建 UI 面板：**

在 Canvas 下创建：

#### StartPanel（开始界面）
- 背景图片（可选）
- 标题文本："欢乐斗地主"
- 按钮："开始游戏" (绑定 UIManager.OnStartGame)

#### GamePanel（游戏主界面）
- 玩家信息文本（显示剩余牌数）
- 当前玩家指示
- 地主标识

#### CallLandlordPanel（叫地主面板）
- 文本："是否叫地主？"
- 按钮："叫地主" 
- 按钮："不叫"

#### PlayButtonsPanel（出牌按钮面板）
- 按钮："出牌"
- 按钮："不出"
- 按钮："提示"

#### GameOverPanel（游戏结束面板）
- 文本：显示胜负结果
- 按钮："再来一局"

### 6. 设置 UIManager

**在 GameController 上添加 UIManager 脚本：**

绑定引用：
```
UIManager:
├── StartPanel → StartPanel 物体
├── GamePanel → GamePanel 物体
├── CallLandlordPanel → CallLandlordPanel 物体
├── PlayButtonsPanel → PlayButtonsPanel 物体
├── GameOverPanel → GameOverPanel 物体
├── StartGameButton → 开始游戏按钮
├── CallLandlordButton → 叫地主按钮
├── PassCallButton → 不叫按钮
├── PlayCardsButton → 出牌按钮
├── PassButton → 不出按钮
├── HintButton → 提示按钮
├── CurrentPlayerText → 当前玩家文本
├── PlayerCardCountTexts[3] → 三个玩家的牌数文本
├── LandlordText → 地主文本
└── GameResultText → 游戏结果文本
```

### 7. 设置玩家

**在场景中创建三个玩家物体：**

1. 创建空物体 `Player_0` (真人玩家)
   - 添加 Player 脚本
   - PlayerIndex = 0
   - IsAI = false

2. 创建空物体 `Player_1` (左侧AI)
   - 添加 AIPlayer 脚本
   - PlayerIndex = 1
   - IsAI = true

3. 创建空物体 `Player_2` (右侧AI)
   - 添加 AIPlayer 脚本
   - PlayerIndex = 2
   - IsAI = true

### 8. 相机设置

**Main Camera：**
- Position: (0, 0, -10)
- Projection: Orthographic
- Size: 8

### 9. 背景设置

**Table_Background：**
- 使用 Quad 或 Sprite
- 设置颜色为深绿色 (类似扑克桌布)
- Position: (0, 0, 10)
- Scale: (20, 12, 1)

## 🎯 测试运行

1. 点击 Play 按钮
2. 点击"开始游戏"
3. 选择是否叫地主
4. 选择卡牌（点击选中，再点击取消）
5. 点击"出牌"或"不出"

## 🐛 常见问题

### 卡牌不显示
- 检查 Card 预制体是否有 SpriteRenderer
- 检查 CardSpriteManager 是否正确设置

### 无法点击卡牌
- 检查 Card 是否有 BoxCollider2D
- 检查相机是否为 Orthographic

### AI 不出牌
- 检查 AIPlayer 是否正确添加到 AI 物体
- 检查 GameManager 中的 IsAI 标志

### UI 不显示
- 检查 Canvas 的 Render Mode
- 检查 UI 物体是否在 Canvas 下

## 📋 检查清单

- [ ] GameController 有 GameManager 和 CardDeck
- [ ] Card 预制体创建完成
- [ ] GameTable 引用设置正确
- [ ] UIManager 引用设置正确
- [ ] 三个玩家物体创建并配置
- [ ] UI 面板和按钮创建
- [ ] 相机设置为 Orthographic
- [ ] 背景设置完成

## 🎨 可选优化

1. **添加卡牌图片**：创建54张卡牌的 Sprite
2. **添加音效**：出牌、叫地主、胜利音效
3. **添加动画**：卡牌移动、出牌特效
4. **美化UI**：更换按钮样式、添加背景图

---
完成以上设置后，游戏应该可以正常运行了！
