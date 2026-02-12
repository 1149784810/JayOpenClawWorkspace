# 🐛 斗地主游戏 - 故障排查指南

## 问题：点击"开始游戏"按钮没有反应

### 排查步骤

#### 步骤1：检查控制台输出

打开 Unity 的 **Console** 窗口 (Ctrl+Shift+C)，查看是否有红色错误信息。

**应该看到的正常输出：**
```
=== 斗地主游戏初始化开始 ===
✓ Main Camera 已创建
✓ 相机配置完成
✓ 创建 GameManager
✓ 创建 CardDeck
...
=== 斗地主游戏初始化完成 ===
```

**如果看到错误：**
- ❌ "GameManager not found" - GameManager 组件缺失
- ❌ "CardDeck not found" - CardDeck 组件缺失
- ❌ "Players not initialized" - 玩家未正确初始化

#### 步骤2：检查 GameController

在 Hierarchy 窗口中：

1. 找到 **GameController** 物体
2. 检查 Inspector 中是否有以下组件：
   - ✓ GameManager
   - ✓ CardDeck
   - ✓ GameLauncher
   - ✓ SimpleGameStarter

**如果缺少组件：**
- 手动添加缺失的组件
- 或重新运行 `DDZ → Setup Scene`

#### 步骤3：检查按钮事件绑定

1. 在 Hierarchy 中找到 **Canvas → StartPanel → StartButton**
2. 在 Inspector 中查看 **Button** 组件
3. 检查 **On Click ()** 事件是否已绑定

**正确的事件绑定：**
```
On Click ()
├─ Runtime Only
├─ GameController (GameObject)
└─ GameLauncher.StartGame
```

**如果事件未绑定：**
1. 点击 "+" 添加事件
2. 拖拽 GameController 到槽位
3. 选择 GameLauncher → StartGame()

#### 步骤4：检查 GameManager 状态

按 **D** 键（如果 SimpleGameStarter 已添加）查看调试信息。

或在 GameController 的 GameManager 组件上检查：
- CurrentState: **Idle** (应该是 Idle 才能开始)
- CardDeck: 不为 null
- Players: 长度为 3

#### 步骤5：手动修复

如果上述检查都正常但仍无法启动，尝试以下修复：

**修复方法1：重新设置场景**
```
DDZ → Reset Scene
DDZ → Setup Scene
```

**修复方法2：手动调用开始游戏**
1. 选中 GameController
2. 在 Inspector 中找到 GameManager 组件
3. 右键点击组件标题 → **StartGame**

**修复方法3：使用空格键**
运行游戏后，直接按 **空格键** 开始游戏。

---

## 常见问题

### Q: 控制台显示 "GameManager is null"

**原因：** GameController 上没有 GameManager 组件

**修复：**
1. 选中 GameController
2. Inspector → Add Component → GameManager

### Q: 控制台显示 "CardDeck is null"

**原因：** CardDeck 组件缺失或未正确初始化

**修复：**
```csharp
// 在 GameController 上执行：
CardDeck deck = GetComponent<CardDeck>();
if (deck == null) {
    deck = gameObject.AddComponent<CardDeck>();
}
deck.InitializeDeck();
```

### Q: 按钮点击有反应但游戏不开始

**原因：** GameManager.CurrentState 不是 Idle

**检查：**
1. 选中 GameController
2. 查看 GameManager 组件的 CurrentState
3. 如果不是 Idle，说明游戏已经在运行或出错了

**修复：**
```
DDZ → Reset Scene
DDZ → Setup Scene
```

### Q: 看到 "开始游戏" 按钮但点击无反应

**原因：** 按钮事件未正确绑定

**修复方法1（自动）：**
```
DDZ → Reset Scene
DDZ → Setup Scene
```

**修复方法2（手动）：**
1. 选中 StartButton
2. 在 Button 组件中移除 On Click 事件
3. 添加新事件：
   - 拖拽 GameController 到槽位
   - 选择 GameLauncher → StartGame()

### Q: 游戏开始时报错 "Object reference not set"

**原因：** 某个对象为 null（通常是 Players 或 CardDeck）

**排查：**
1. 检查 GameManager 的 Players 数组
2. 检查每个 Player 是否有 CardHand 组件
3. 检查 CardDeck 是否已初始化

---

## 调试命令

### 在控制台输入（仅编辑器）

**开始游戏：**
```csharp
FindObjectOfType<GameManager>().StartGame();
```

**检查状态：**
```csharp
var gm = FindObjectOfType<GameManager>();
Debug.Log($"State: {gm.CurrentState}, Players: {gm.Players.Length}");
```

**重新初始化：**
```csharp
FindObjectOfType<GameLauncher>().InitializeGame();
```

---

## 完整重置

如果所有方法都无效，执行完整重置：

1. **保存场景** (Ctrl+S)
2. **关闭 Unity**
3. **重新打开 Unity**
4. **打开场景** (DouDiZhuGame.unity)
5. **等待编译完成**
6. **执行：**
   ```
   DDZ → Reset Scene
   DDZ → Setup Scene
   ```
7. **保存** (Ctrl+S)
8. **点击 Play**
9. **按空格键** 或点击"开始游戏"

---

## 验证清单

确保以下都正确：

- [ ] GameController 存在于场景中
- [ ] GameController 有 GameManager 组件
- [ ] GameController 有 CardDeck 组件
- [ ] GameController 有 GameLauncher 组件
- [ ] Canvas 存在于场景中
- [ ] StartPanel → StartButton 有 OnClick 事件
- [ ] 控制台无红色错误
- [ ] 按空格键可以开始游戏

---

如果仍有问题，请复制控制台的完整错误信息以便进一步排查。
