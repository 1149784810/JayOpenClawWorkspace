---
name: sao-dnd-rpg
description: 刀剑神域DND风格RPG游戏开发指南 - React+TypeScript+Vite技术栈
---

# SKILL: sao-dnd-rpg

## 项目概述

**刀剑神域DND冒险** 是一个基于 React + TypeScript + Vite 的网页RPG游戏，采用龙与地下城(DND)规则系统，融合刀剑神域世界观。

### 核心特性

| 特性 | 说明 |
|------|------|
| 9种职业系统 | 剑士、法师、盗贼、弓箭手、圣骑士、狂战士、刺客、牧师、锻造师 |
| 100层爬塔 | 逐层挑战，每层有不同敌人和BOSS |
| 回合制战斗 | 玩家+队友 vs 敌人，支持技能释放 |
| 伙伴系统 | 8位原作角色，好感度系统，可结婚 |
| 锻造系统 | 材料收集，装备锻造，成功率机制 |
| 存档系统 | 8个槽位 + 自动存档，localStorage持久化 |

---

## 技术栈

```
核心框架:
├── React 19          - UI组件
├── TypeScript        - 类型安全
├── Vite              - 构建工具
├── Tailwind CSS      - 样式系统
└── shadcn/ui         - UI组件库 (基于Radix UI)

状态管理:
├── React Context     - 全局状态
├── useReducer        - 状态更新逻辑
└── localStorage      - 存档持久化

辅助库:
├── Lucide React      - 图标系统
├── Recharts          - 数据可视化
├── Zod               - 表单验证
└── React Hook Form   - 表单处理
```

---

## 项目结构

```
app/src/
├── components/
│   ├── scenes/           # 场景组件
│   │   ├── TownScene.tsx      # 城镇
│   │   ├── DungeonScene.tsx   # 地牢探索
│   │   ├── ForgeScene.tsx     # 锻造系统
│   │   ├── FriendsScene.tsx   # 伙伴/好感度
│   │   ├── InventoryScene.tsx # 背包
│   │   ├── SkillsScene.tsx    # 技能/天赋
│   │   └── CharacterScene.tsx # 角色信息
│   ├── ui/               # shadcn/ui 基础组件
│   ├── BattleSystem.tsx  # 战斗系统
│   ├── CharacterCreation.tsx  # 角色创建
│   ├── GameLayout.tsx    # 游戏主布局
│   └── TitleScreen.tsx   # 标题画面
├── context/
│   └── GameContext.tsx   # 游戏状态管理 (核心)
├── data/
│   ├── classes.ts        # 职业定义
│   ├── enemies.ts        # 敌人数据库
│   ├── equipment.ts      # 装备数据
│   ├── friends.ts        # 伙伴数据
│   ├── skills.ts         # 技能数据
│   ├── materials.ts      # 材料数据
│   ├── forgeRecipes.ts   # 锻造配方
│   └── floorEnemies.ts   # 楼层敌人配置
├── types/
│   └── game.ts           # TypeScript类型定义
├── utils/
│   └── audio.ts          # 音频管理
└── hooks/
    └── use-mobile.ts     # 响应式钩子
```

---

## 核心架构

### 1. 状态管理 (GameContext)

```typescript
// 游戏状态结构
interface GameState {
  player: Player | null;           // 玩家数据
  isGameStarted: boolean;          // 游戏是否开始
  isInCharacterCreation: boolean;  // 是否在创建角色
  currentScene: SceneType;         // 当前场景
  currentBattle?: BattleState;     // 战斗状态
  currentSaveSlot: number;         // 当前存档槽位
  gameTime: { day, hour, minute }; // 游戏时间
}

// Action类型 (使用Reducer模式)
type GameAction =
  | { type: 'START_GAME' }
  | { type: 'CREATE_CHARACTER'; payload: { name, classType } }
  | { type: 'SET_SCENE'; payload: SceneType }
  | { type: 'ADD_EXP'; payload: number }
  | { type: 'START_BATTLE'; payload: Enemy }
  | { type: 'END_BATTLE'; payload: { result, rewards } }
  | ...
```

**关键设计**:
- Reducer 处理所有状态变更逻辑
- Context 提供全局访问
- useEffect 实现自动存档
- 存档使用 localStorage，8个槽位

### 2. 职业系统

```typescript
// 职业定义
interface ClassDefinition {
  id: ClassType;
  name: string;
  description: string;
  baseStats: Stats;        // 初始属性
  statGrowth: Stats;       // 每级成长
  skills: Skill[];         // 职业技能
  equipmentTypes: EquipmentType[];  // 可用装备类型
  startingBlueprints: ForgeRecipe[]; // 开局锻造蓝图
}

// 9种职业
enum ClassType {
  SWORDSMAN = 'swordsman',  // 剑士 - 平衡型
  MAGE = 'mage',            // 法师 - 高魔攻
  ROGUE = 'rogue',          // 盗贼 - 高暴击
  ARCHER = 'archer',        // 弓箭手 - 远程
  PALADIN = 'paladin',      // 圣骑士 - 坦克
  BERSERKER = 'berserker',  // 狂战士 - 高攻击
  ASSASSIN = 'assassin',    // 刺客 - 高爆发
  PRIEST = 'priest',        // 牧师 - 治疗
  BLACKSMITH = 'blacksmith',// 锻造师 - 装备强化
}
```

### 3. 战斗系统

**战斗流程**:
1. 遭遇敌人 → dispatch({ type: 'START_BATTLE', payload: enemy })
2. 玩家回合 → 选择攻击/技能/物品/逃跑
3. 队友回合 → 自动攻击（基于好感度加成）
4. 敌人回合 → AI自动攻击
5. 战斗结束 → dispatch({ type: 'END_BATTLE', payload: { result, rewards } })

**伤害计算公式**:
```typescript
// 物理伤害
const damageMultiplier = 100 / (100 + defense);
const damage = attack * damageMultiplier * (0.9 + Math.random() * 0.2);

// 队友伤害（好感度加成）
const relationshipBonus = 1 + ((member.affection || 0) / 200);
```

### 4. 伙伴/好感度系统

```typescript
interface Friend {
  id: string;
  name: string;              // 角色名
  level: number;             // 等级
  affection: number;         // 好感度 (0-300)
  relationshipStage: RelationshipStage;  // 关系阶段
  skills: { name, power }[]; // 技能
  unlocked: boolean;         // 是否解锁
  isInParty: boolean;        // 是否在队伍中
}

// 关系阶段
enum RelationshipStage {
  STRANGER = 'stranger',       // 陌生人 (0-59)
  ACQUAINTANCE = 'acquaintance', // 相识 (60-119)
  FRIEND = 'friend',           // 朋友 (120-179)
  CLOSE_FRIEND = 'close_friend', // 挚友 (180-239)
  ROMANTIC = 'romantic',       // 恋人 (240-299)
  MARRIED = 'married',         // 伴侣 (300)
}

// 好感度获取方式
- 每日交谈: +5/次 (上限3次/天)
- 赠送礼物: +10~30 (取决于礼物偏好)
- 组队战斗: +2/场
```

### 5. 装备/锻造系统

```typescript
// 装备品质 (6级)
enum EquipmentRarity {
  COMMON = 'common',        // 普通 (白)
  UNCOMMON = 'uncommon',    // 优秀 (绿)
  RARE = 'rare',            // 稀有 (蓝)
  EPIC = 'epic',            // 史诗 (紫)
  LEGENDARY = 'legendary',  // 传说 (橙)
  MYTHIC = 'mythic',        // 神话 (红)
}

// 锻造配方
interface ForgeRecipe {
  id: string;
  result: Equipment;
  materials: { material: Material; quantity: number }[];
  goldCost: number;
  successRate: number;  // 成功率 (0-100)
  requiredLevel: number;
}
```

### 6. 存档系统

```typescript
// 存档数据结构
interface SaveData {
  slot: number;
  name: string;
  player: Player;
  gameState: GameState;
  saveTime: number;
  version: string;
}

// 存档槽位
const SAVE_SLOTS = 8;
const AUTO_SAVE_SLOT = 0;  // 槽位0为自动存档

// 存档管理函数
- getAllSaves(): SaveData[]      // 获取所有存档
- getSaveBySlot(slot): SaveData  // 获取指定存档
- saveToSlot(slot, state, name?) // 保存到指定槽位
- deleteSave(slot)               // 删除存档
```

---

## 关键文件说明

### GameContext.tsx (核心)
- 位置: `src/context/GameContext.tsx`
- 职责: 全局状态管理、Reducer逻辑、存档操作
- 关键函数:
  - `gameReducer()` - 处理所有Action
  - `saveToSlot()` - 存档保存
  - 自动升级检查 useEffect
  - 自动存档 useEffect

### types/game.ts (类型定义)
- 位置: `src/types/game.ts`
- 职责: 所有TypeScript类型/接口定义
- 关键类型:
  - `Player`, `GameState`, `BattleState`
  - `Equipment`, `Skill`, `Friend`, `Enemy`
  - `Stats`, `CombatStats`

### 数据文件 (data/)
所有游戏数据分离在独立文件中，便于修改和扩展:
- `classes.ts` - 9种职业完整定义
- `enemies.ts` - 按楼层分类的敌人数据库
- `equipment.ts` - 按部位分类的装备数据
- `friends.ts` - 8位伙伴的完整数据
- `skills.ts` - 职业技能定义
- `forgeRecipes.ts` - 锻造配方

---

## 开发规范

### 添加新职业

1. 在 `types/game.ts` 添加 ClassType
2. 在 `data/classes.ts` 定义 ClassDefinition
3. 创建职业初始蓝图 (startingBlueprints)
4. 在 `data/skills.ts` 添加职业技能

```typescript
// 示例: 添加新职业
const newClass: ClassDefinition = {
  id: ClassType.NEW_CLASS,
  name: '新职业',
  baseStats: { strength: 10, agility: 10, ... },
  statGrowth: { strength: 2, agility: 2, ... },
  startingBlueprints: [...],
  ...
};
```

### 添加新敌人

1. 在 `data/enemies.ts` 使用 createEnemy() 辅助函数
2. 添加到对应楼层数组

```typescript
// 示例: 添加敌人
createEnemy(
  'enemy_id',
  '敌人名称',
  '描述',
  EnemyType.NORMAL,
  level,
  floor,
  { hp, mp, attack, defense, speed },
  [createDrop(materials.goblin_fang, 50)],
  expReward,
  goldReward,
  '🎭',
  ElementType.FIRE
);
```

### 添加新伙伴

1. 在 `data/friends.ts` 添加 Friend 对象
2. 设置解锁条件 (unlocked, location)
3. 定义技能 (skills)
4. 准备头像图片 (public/images/friends/)

### 修改战斗公式

战斗公式在 `BattleSystem.tsx`:
```typescript
// calculateDamage 函数
const damageMultiplier = 100 / (100 + defense);
const damage = attack * damageMultiplier * variance;
```

---

## 常见开发任务

### 1. 修改游戏平衡

**调整升级经验**:
```typescript
// GameContext.tsx 中的 ADD_EXP action
newExpToNext = Math.floor(newExpToNext * 1.2);  // 修改系数
```

**调整敌人强度**:
```typescript
// data/enemies.ts 中修改 stats
{ hp: 100, attack: 20, defense: 10, ... }
```

### 2. 添加新场景

1. 创建场景组件 `components/scenes/NewScene.tsx`
2. 在 `types/game.ts` 添加 SceneType
3. 在 `App.tsx` 添加场景渲染
4. 在 `GameLayout.tsx` 添加导航按钮

### 3. 修改UI主题

主题配置在:
- `tailwind.config.js` - Tailwind配置
- `index.css` - 全局CSS变量
- `App.css` - 组件样式

### 4. 添加音效

```typescript
// utils/audio.ts
audioManager.play('sound_effect_name');
```

---

## 构建与部署

### 本地开发
```bash
cd app
npm install
npm run dev      # 启动开发服务器
```

### 构建生产版本
```bash
npm run build    # 输出到 dist/ 目录
```

### 部署到 GitHub Pages
1. 构建项目: `npm run build`
2. 将 `dist/` 目录内容推送到 gh-pages 分支
3. 或通过 GitHub Actions 自动部署

---

## 扩展建议

### 短期扩展
- 添加更多伙伴 (原作角色)
- 增加楼层数量 (100层以上)
- 添加更多装备和锻造配方
- 实现天赋树系统 (目前为占位)

### 中期扩展
- 添加多人联机功能
- 实现公会系统
- 添加 PvP 竞技场
- 实现交易系统

### 长期扩展
- 后端服务 (存档云同步)
- 移动端适配优化
- 3D战斗场景
- 剧情分支系统

---

## 注意事项

1. **类型安全**: 所有数据修改都需要更新对应的 TypeScript 类型
2. **存档兼容**: 修改数据结构时需要考虑旧存档兼容性
3. **性能**: 敌人数据量大，使用懒加载或分页
4. **状态更新**: 始终通过 dispatch 修改状态，不要直接修改
5. **图片资源**: 所有图片放在 `public/` 目录下

---

## 相关文件路径

```
项目根目录: F:\刀剑神域WEB游戏\app
关键文件:
├── src/App.tsx              # 应用入口
├── src/context/GameContext.tsx  # 核心状态管理
├── src/types/game.ts        # 类型定义
├── src/data/                # 所有游戏数据
│   ├── classes.ts
│   ├── enemies.ts
│   ├── equipment.ts
│   ├── friends.ts
│   └── skills.ts
├── src/components/BattleSystem.tsx  # 战斗系统
└── src/components/scenes/   # 所有场景组件
```
