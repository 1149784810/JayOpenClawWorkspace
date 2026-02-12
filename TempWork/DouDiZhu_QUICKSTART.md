# 🚀 斗地主游戏 - 快速启动指南（已修复）

## ✅ 最新修复内容

1. **添加了相机自动创建** - GameLauncher 会自动创建并配置相机
2. **修复了游戏启动问题** - 改进了 GameManager 的初始化逻辑
3. **添加了 GameLauncher** - 新的统一启动器，处理所有初始化

---

## 🎮 如何运行游戏

### 方法 1：使用 Unity 编辑器菜单（推荐）

1. **打开 Unity**
   ```
   项目: E:\XiuXianCards\XiuXianCards
   场景: Assets/TestAI/DouDiZhuGame.unity
   ```

2. **等待脚本编译完成**（看 Unity 右下角）

3. **在菜单栏点击：**
   ```
   DDZ → Setup Scene
   ```

4. **查看控制台输出**，确认显示：
   ```
   ✓ Main Camera 已创建
   ✓ 相机配置完成
   ✓ 创建 GameManager
   ✓ 创建 CardDeck
   ...
   ✓ 游戏区域设置完成
   ✓ 玩家设置完成
   ✓ 背景创建完成
   ✓ UI 设置完成
   === 斗地主游戏初始化完成 ===
   ```

5. **点击 Play 按钮**

6. **点击"开始游戏"按钮**开始游戏

---

### 如果菜单方式不工作

**尝试方法 2：手动创建 GameController**

1. 在 Hierarchy 右键 → **Create Empty**
2. 命名为 **"GameController"**
3. 添加组件：
   - **GameLauncher** (Script)
   - **GameManager** (Script)
   - **CardDeck** (Script)
4. 在 GameLauncher 组件上勾选 **"Auto Initialize"**
5. 点击 Play

---

## 🎯 游戏操作

| 操作 | 说明 |
|------|------|
| 点击"开始游戏" | 开始新游戏 |
| 空格键 | 快捷键开始游戏 |
| 点击卡牌 | 选择/取消选择 |
| 出牌按钮 | 出选中的牌 |
| 不出按钮 | 跳过本轮 |

---

## 🔧 故障排除

### Q: 点击"开始游戏"没反应？

**检查清单：**
- [ ] GameController 是否有 GameManager 组件
- [ ] GameController 是否有 CardDeck 组件
- [ ] 控制台是否有红色错误信息

**修复方法：**
1. 删除 GameController 物体
2. 重新运行 `DDZ → Setup Scene`

### Q: 屏幕是黑色的？

**原因：** 相机未创建

**修复：**
- 确保运行了 `DDZ → Setup Scene`
- 或手动创建相机：
  1. GameObject → Camera
  2. Position: (0, 0, -10)
  3. Projection: Orthographic
  4. Size: 8

### Q: 看不到玩家手牌？

**原因：** 场景物体未正确创建

**修复：**
```
DDZ → Reset Scene    (重置场景)
DDZ → Setup Scene    (重新设置)
```

### Q: 菜单 DDZ 没有出现？

**原因：** 脚本编译错误或 Editor 文件夹问题

**修复：**
1. 检查 Console 窗口是否有编译错误
2. 确保文件存在：`Assets/TestAI/Scripts/Editor/SceneSetupEditor.cs`

---

## 📋 检查清单（运行前）

确保以下都已完成：

- [ ] Unity 打开项目
- [ ] 打开场景 DouDiZhuGame.unity
- [ ] 脚本编译完成（无错误）
- [ ] 运行了 DDZ → Setup Scene
- [ ] 控制台显示"初始化完成"
- [ ] 点击 Play 按钮
- [ ] 看到"开始游戏"按钮

---

## 🎮 确认游戏正常工作

如果看到以下界面，说明设置成功：

```
┌─────────────────────────┐
│                         │
│      欢乐斗地主          │
│                         │
│   [   开始游戏   ]      │
│                         │
└─────────────────────────┘
```

点击"开始游戏"后：
1. 面板消失
2. 看到绿色桌面背景
3. 控制台显示发牌信息
4. 出现"叫地主"按钮

---

## 📁 重要文件

确保这些文件存在：

```
Assets/TestAI/Scripts/Core/
├── GameManager.cs      ✓
├── CardDeck.cs         ✓
├── GameLauncher.cs     ✓ (新！)
└── ...

Assets/TestAI/Scripts/Editor/
└── SceneSetupEditor.cs ✓
```

---

## 🔄 如果还是不行

### 完全重置方法：

1. 保存场景（Ctrl+S）
2. 关闭 Unity
3. 重新打开 Unity
4. 运行 `DDZ → Reset Scene`
5. 运行 `DDZ → Setup Scene`
6. 保存（Ctrl+S）
7. 点击 Play

---

**版本**: 1.1 (已修复相机和启动问题)  
**更新日期**: 2026-02-11
