---
name: xiuxian-idle
description: Web端放置修仙游戏开发指南 - CD战斗、修为系统、装备锻造、丹药系统
---

# SKILL: xiuxian-idle

> ⚠️ **重要区分**: 本项目 (XiuXianIdle) 是 **Web端HTML放置游戏**，与 Unity 项目 **修仙大巴扎 (XiuXianCards)** 完全不同，请勿混淆！

## 项目概览

**类型**: Web端放置修仙游戏  
**技术栈**: HTML5 + CSS3 + Vanilla JavaScript  
**核心玩法**: 自动修炼、CD战斗、装备锻造、丹药系统  
**存档方式**: localStorage + 导出/导入代码

---

## 核心系统架构

### 1. 游戏循环 (Game Loop)

```javascript
// 100ms 循环 - 自动修炼 + 战斗逻辑
function gameLoop() {
    // 自动修炼
    const baseSpeed = 5 + gameData.player.realm * 2;
    gameData.player.cultivation += baseSpeed * 0.1;
    
    // CD战斗更新
    if (gameData.combat.inCombat) updateCombat();
    
    // 技能CD递减
    gameData.skills.forEach(s => { if (s.cd > 0) s.cd -= 0.1; });
    
    updateUI();
}
```

**关键点**:
- 使用 `setInterval(gameLoop, 100)` 实现0.1秒精度
- 所有时间敏感计算基于累计增量，非时间戳

---

### 2. CD自动战斗系统

**设计原则**: 玩家只需触发战斗，攻击自动进行

```javascript
// 战斗核心逻辑
function updateCombat() {
    // CD进度（每2秒攻击一次）
    gameData.combat.playerCd += playerAspd;
    gameData.combat.enemyCd += enemy.aspd;
    
    // 玩家攻击
    if (gameData.combat.playerCd >= 2) {
        gameData.combat.playerCd = 0;
        const dmg = Math.max(1, playerAtk - enemyDef);
        enemy.hp -= dmg;
        // 自动释放技能
        if (skillReady) useSkill(skill);
    }
    
    // 敌人攻击
    if (gameData.combat.enemyCd >= 2) {
        gameData.combat.enemyCd = 0;
        const dmg = Math.max(1, enemyAtk - playerDef);
        player.hp -= dmg;
    }
    
    updateCombatUI(); // 立即更新血条
}
```

**实现细节**:
- 进入战斗时 `updateCombatUI()` 立即初始化血条
- 每次伤害/治疗后立即更新显示
- 技能释放后同步更新UI

---

### 3. 修为系统 - 大境界指数增长

**公式设计**:
```javascript
function getReqCultivation() {
    const base = 50;
    const stageMultiplier = Math.pow(1.5, stage - 1);  // 小境界1.5倍
    const realmMultiplier = Math.pow(100, realm);       // 大境界100倍
    return Math.floor(base * stageMultiplier * realmMultiplier);
}
```

**数值示例**:
| 境界 | 修为需求 |
|------|---------|
| 炼气一重 | 50 |
| 炼气十重 | 1,922 |
| 筑基一重 | 5,000 (100×) |
| 筑基十重 | 192,200 |
| 金丹一重 | 500,000 (100×) |
| 金丹十重 | 19,220,000 |
| 元婴一重 | 50,000,000 |

**突破机制**:
- 成功: 扣除当前阶段全部修为，进入下一阶段
- 失败: 损失30%修为
- 突破丹: +30%成功率

---

### 4. 装备系统

**数据结构**:
```javascript
{
    id: timestamp,
    name: "史诗铁剑",
    type: "weapon",      // weapon/armor/accessory
    rarity: "epic",      // common/rare/epic/legendary
    atk: 15,             // 武器属性
    def: 0,              // 防具属性
    hp: 0                // 饰品属性
}
```

**品质倍率**:
| 品质 | 倍率 | 售价 |
|------|------|------|
| 普通(白) | 1× | 5灵石 |
| 稀有(蓝) | 1.5× | 15灵石 |
| 史诗(紫) | 2× | 40灵石 |
| 传说(橙) | 3× | 100灵石 |

**锻造系统**:
- 消耗: 20灵石 + 10灵草（饰品30灵石）
- 品质概率: 50%白 / 30%蓝 / 15%紫 / 5%橙
- 属性范围: 基础值 × 品质倍率

---

### 5. 丹药系统

**丹药类型**:
```javascript
const pillTypes = [
    { id: 'healSmall', name: '回春丹', effect: 'heal', value: 30, desc: '回复30%生命' },
    { id: 'healMedium', name: '生肌丹', effect: 'heal', value: 50 },
    { id: 'cultivationSmall', name: '聚气丹', effect: 'cultivation', value: 50 }
];
```

**掉落机制**:
- 战斗: 30%-70%概率掉落（根据敌人强度）
- 副本: 70%概率掉落
- 品质随敌人强度提升

**使用方式**:
- 背包→丹药分页
- 战斗中也可使用（回复生命）

---

### 6. 存档系统

**双轨存档**:

1. **自动存档 (localStorage)**
```javascript
function saveGame() {
    gameData.lastOnline = Date.now();
    localStorage.setItem('xiuxianIdle', JSON.stringify(gameData));
}
// 每10秒自动保存
setInterval(saveGame, 10000);
```

2. **导出/导入 (文本代码)**
```javascript
// 导出 - 处理中文编码
function exportSave() {
    const json = JSON.stringify(gameData);
    const data = btoa(encodeURIComponent(json).replace(/%([0-9A-F]{2})/g, 
        (match, p1) => String.fromCharCode('0x' + p1)));
    return data; // Base64编码，可复制
}

// 导入 - 解码中文
function importSave(code) {
    const json = decodeURIComponent(atob(code).split('').map(c => 
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
    Object.assign(gameData, JSON.parse(json));
}
```

**关键点**:
- `btoa` 不支持中文，需要 `encodeURIComponent` 转换
- 技能升级后立即 `saveGame()`，避免延迟丢失
- 深度合并函数确保存档兼容性

---

### 7. UI 结构最佳实践

**Tab 切换系统**:
```html
<!-- 一级菜单 -->
<div class="tabs">
    <div class="tab active" onclick="switchTab('cultivation')">修炼</div>
    <div class="tab" onclick="switchTab('bag')">背包</div>
    <div class="tab" onclick="switchTab('forge')">锻造</div>
</div>

<!-- 背包内二级菜单 -->
<div class="tab-content" id="bag">
    <div class="tabs">
        <div class="tab active" onclick="switchBagTab('equipment')">装备</div>
        <div class="tab" onclick="switchBagTab('pills')">丹药</div>
    </div>
</div>
```

**避免闪烁**:
- 背包渲染不要放在 `updateUI()` 的100ms循环中
- 只在数据变化时（获得/出售装备）调用 `renderBag()`

---

### 8. 进度条实现

**CSS 结构**:
```css
.progress-bar {
    width: 100%;
    height: 20px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
    background: linear-gradient(90deg, #e94560, #ff6b6b);
}
```

**JS 更新**:
```javascript
document.getElementById('cultivationBar').style.width = 
    `${Math.min(100, cultivation / reqCult * 100)}%`;
```

**注意**: `.progress-fill` 必须设置 `background`，否则有宽度也看不到颜色

---

### 9. 离线收益计算

```javascript
function calculateOfflineReward() {
    const offline = (Date.now() - gameData.lastOnline) / 1000;
    const maxOffline = 12 * 3600;  // 最多12小时
    const actual = Math.min(offline, maxOffline);
    const reward = Math.floor(actual * cultivationPerSecond);
    gameData.player.cultivation += reward;
}
```

---

## 常见陷阱与解决方案

| 问题 | 原因 | 解决 |
|------|------|------|
| 背包闪烁 | `renderBag()` 在100ms循环中 | 只在数据变化时渲染 |
| 装备无法穿戴 | id类型不匹配(字符串vs数字) | `id = Number(id)` |
| 进度条不显示 | `.progress-fill` 无背景色 | 添加 `background` |
| 功法等级丢失 | `initSkills()` 重置等级 | 合并存档数据而非覆盖 |
| 中文存档失败 | `btoa` 不支持中文 | `encodeURIComponent` 转换 |
| 出售已装备 | 未检查装备状态 | `isEquipped()` 过滤 |
| 丹药点击无效 | id字符串引号问题 | 使用 `JSON.stringify(id)` |

---

## 快速参考：需求定位

| 需求类型 | 文件/函数 |
|---------|----------|
| 战斗逻辑 | `updateCombat()`, `winCombat()` |
| 装备掉落 | `dropEquipment()`, `forgeItem()` |
| 丹药系统 | `dropPill()`, `usePill()` |
| 修为计算 | `getReqCultivation()`, `breakthrough()` |
| UI更新 | `updateUI()`, `updateCombatUI()` |
| 存档系统 | `saveGame()`, `loadGame()`, `exportSave()` |
| 背包渲染 | `renderBag()`, `renderPills()` |

---

## 项目区别 (重要！)

| 特性 | 修仙挂机 (XiuXianIdle) | 修仙大巴扎 (XiuXianCards) |
|------|----------------------|-------------------------|
| 平台 | Web (HTML/JS) | Unity (C#) |
| 类型 | 放置/单机 | 卡牌对战/联机 |
| 战斗 | CD自动战斗 | 卡牌策略 |
| 存档 | localStorage | 服务器/本地文件 |
| 核心 | 修炼、装备、丹药 | 卡牌、槽位、推挤 |

**永远不要混淆两个项目的代码和架构！**
