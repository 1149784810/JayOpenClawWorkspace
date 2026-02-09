# C# 优化模式库

本文件记录常见的 C# 性能优化模式，供 code-optimizer Skill 参考使用。

---

## 1. 查找性能优化

### 1.1 List → Dictionary

**问题**: 线性搜索时间复杂度 O(n)

```csharp
// 优化前
public CardTrait GetTrait(string id)
{
    foreach (CardTrait trait in traits)
        if (trait.id == id) return trait;
    return null;
}

public bool HasTrait(string id)
{
    return GetTrait(id) != null;  // O(n)
}
```

**优化**: 使用字典实现 O(1) 查找

```csharp
// 优化后
[System.NonSerialized] private Dictionary<string, CardTrait> trait_dict;

private void EnsureDictsInitialized()
{
    if (trait_dict != null) return;
    trait_dict = new Dictionary<string, CardTrait>(traits.Count);
    foreach (var trait in traits)
        trait_dict[trait.id] = trait;
}

// 优化点：使用字典替代线性搜索，O(n)→O(1)
public CardTrait GetTrait(string id)
{
    EnsureDictsInitialized();
    trait_dict.TryGetValue(id, out CardTrait trait);
    return trait;
}

// 优化点：字典 ContainsKey 也是 O(1)
public bool HasTrait(string id)
{
    EnsureDictsInitialized();
    return trait_dict.ContainsKey(id);
}
```

**适用场景**:
- 查找操作频繁（每帧或每次交互都调用）
- 数据量 > 10 个元素
- 数据相对稳定，不频繁增删

---

## 2. 缓存策略

### 2.1 脏标记模式 (Dirty Flag)

**问题**: 每次调用都重新计算/重建

```csharp
// 优化前
public List<AbilityData> GetAbilities()
{
    var list = new List<AbilityData>();
    foreach (var id in abilities)
        list.Add(AbilityData.Get(id));
    return list;
}
```

**优化**: 脏标记 + 延迟重建

```csharp
// 优化后
[System.NonSerialized] private List<AbilityData> abilities_data = null;
[System.NonSerialized] private bool abilities_dirty = true;

// 优化点：使用脏标记模式，避免频繁重建
public List<AbilityData> GetAbilities()
{
    if (abilities_data == null || abilities_dirty)
    {
        RebuildAbilitiesCache();
    }
    return abilities_data;
}

private void RebuildAbilitiesCache()
{
    abilities_data = new List<AbilityData>(abilities.Count);
    foreach (var id in abilities)
    {
        AbilityData ability = AbilityData.Get(id);
        if (ability != null)
            abilities_data.Add(ability);
    }
    abilities_dirty = false;
}

// 修改时标记脏
public void AddAbility(AbilityData ability)
{
    abilities.Add(ability.id);
    abilities_dirty = true;  // 标记需要重建
}
```

**适用场景**:
- 获取操作远多于修改操作
- 构建成本较高
- 数据一致性要求允许延迟更新

---

## 3. 内存分配优化

### 3.1 静态空列表

**问题**: 频繁返回空列表产生 GC 压力

```csharp
// 优化前
public List<Card> GetCards()
{
    if (cards.Count == 0)
        return new List<Card>();  // 每次 GC 分配
    return cards;
}
```

**优化**: 复用静态空列表

```csharp
// 优化后
// 优化点：静态空列表避免频繁创建临时对象，减少 GC 压力
private static readonly List<Card> EmptyList = new List<Card>();

public List<Card> GetCards()
{
    if (cards.Count == 0)
        return EmptyList;  // 无 GC 分配
    return cards;
}
```

**变体 - 方法重载避免 GC**:

```csharp
// 优化点：提供无 GC 分配的方法重载，由调用方提供结果容器
public void GetCards(List<Card> result)
{
    if (result == null) return;
    result.Clear();
    result.AddRange(cards);
}
```

**适用场景**:
- 方法可能返回空结果
- 被频繁调用（每帧）
- 对 GC 敏感（如游戏主循环）

---

## 4. 循环优化

### 4.1 反向遍历删除

**问题**: 正向遍历删除元素导致索引错乱

```csharp
// 优化前（有 Bug）
public void RemoveStatus(CardStatusType type)
{
    for (int i = 0; i < status.Count; i++)  // 正向遍历
    {
        if (status[i].type == type)
        {
            status.RemoveAt(i);  // 删除后，后面的元素前移，会跳过下一个
        }
    }
}
```

**优化**: 反向遍历

```csharp
// 优化后
// 优化点：反向遍历列表删除元素，避免删除后索引错乱
public void RemoveStatus(CardStatusType type)
{
    for (int i = status.Count - 1; i >= 0; i--)
    {
        if (status[i].type == type)
        {
            status.RemoveAt(i);
            // 删除后 i--，下一个要检查的元素仍在正确位置
        }
    }
}
```

**替代方案**:

```csharp
// Linq 方式（简洁但略慢）
status.RemoveAll(s => s.type == type);
```

---

## 5. 空值检查优化

### 5.1 卫语句提前返回

**问题**: 嵌套层级过深

```csharp
// 优化前
public void ProcessCard(Card card)
{
    if (card != null)
    {
        if (card.CardData != null)
        {
            if (card.CardData.abilities != null)
            {
                // 实际逻辑
            }
        }
    }
}
```

**优化**: 卫语句

```csharp
// 优化后
public void ProcessCard(Card card)
{
    // 优化点：全面的空值检查，提前发现问题避免空引用异常
    if (card == null) return;
    if (card.CardData == null) return;
    if (card.CardData.abilities == null) return;
    
    // 实际逻辑（无嵌套）
}

// 或合并检查
public void ProcessCard(Card card)
{
    if (card?.CardData?.abilities == null) return;
    // 实际逻辑
}
```

---

## 6. 表达式简化

### 6.1 表达式体方法

**问题**: 简单方法的冗长写法

```csharp
// 优化前
public int GetAttack()
{
    return Mathf.Max(attack + attack_ongoing, 0);
}

public bool CanAttack(bool skip_cost = false)
{
    if (skip_cost)
        return true;
    return !exhausted;
}
```

**优化**: 表达式体

```csharp
// 优化后
// 优化点：使用表达式体简化单语句方法
public int GetAttack() => Mathf.Max(attack + attack_ongoing, 0);

// 优化点：使用表达式体简化简单条件判断
public bool CanAttack(bool skip_cost = false) => skip_cost || !exhausted;
```

**适用场景**:
- 单行返回语句
- 简单条件判断
- 属性 getter

---

## 7. 延迟初始化

### 7.1 懒加载模式

**问题**: 构造函数中初始化所有资源

```csharp
// 优化前
public class GameManager
{
    private Texture2D largeTexture;
    
    public GameManager()
    {
        largeTexture = LoadTexture("2k_texture.png");  // 启动时加载
    }
}
```

**优化**: 首次使用时加载

```csharp
// 优化后
public class GameManager
{
    private Texture2D _largeTexture;
    
    // 优化点：延迟初始化，首次使用时加载
    public Texture2D LargeTexture
    {
        get
        {
            if (_largeTexture == null)
                _largeTexture = LoadTexture("2k_texture.png");
            return _largeTexture;
        }
    }
}
```

---

## 8. Unity 专属优化

### 8.1 序列化与缓存

**问题**: Unity 网络传输后反序列化丢失非序列化数据

```csharp
// 优化前
[System.NonSerialized] private List<AbilityData> abilities_data;

public List<AbilityData> GetAbilities()
{
    return abilities_data;  // 网络传输后可能为 null
}
```

**优化**: 自动重建缓存

```csharp
// 优化后
[System.NonSerialized] private List<AbilityData> abilities_data = null;
[System.NonSerialized] private bool abilities_dirty = true;

// 优化点：自动处理网络传输后的反序列化，延迟重建缓存
public List<AbilityData> GetAbilities()
{
    if (abilities_data == null || abilities_dirty)
    {
        RebuildAbilitiesCache();
    }
    return abilities_data;
}
```

---

## 9. 代码组织

### 9.1 Region 分区

**建议**: 大文件按功能分区

```csharp
#region 初始化与清理
// 构造函数、初始化、清理方法
#endregion

#region 属性计算
// GetAttack, GetHP 等计算属性
#endregion

#region 特性管理
// SetTrait, GetTrait, HasTrait 等
#endregion

#region 状态管理
// AddStatus, RemoveStatus 等
#endregion

#region 能力管理
// AddAbility, GetAbilities 等
#endregion

#region 克隆方法
// Clone, CloneNew 等
#endregion
```

---

## 10. TryGetValue 模式

### 10.1 避免双重查找

**问题**: ContainsKey + 索引器 两次查找

```csharp
// 优化前（两次查找）
if (dict.ContainsKey(key))
{
    var value = dict[key];  // 第二次查找
    // 使用 value
}
```

**优化**: 单次查找

```csharp
// 优化后
// 优化点：使用 TryGetValue 替代 ContainsKey + 索引器，减少两次查找
if (dict.TryGetValue(key, out var value))
{
    // 使用 value
}
```

---

## 优化检查清单

使用此 Skill 时，按以下顺序检查代码：

- [ ] 是否有频繁的线性搜索（List.Contains/Find）？
- [ ] 是否有重复计算/重建的列表？
- [ ] 是否频繁返回空集合？
- [ ] 循环中是否有删除操作？
- [ ] 方法参数是否做了空值检查？
- [ ] 单语句方法是否可用表达式体？
- [ ] 资源是否可延迟加载？
- [ ] Unity 非序列化字段是否需要重建逻辑？

---

*Last updated: 2026-02-10*
*Based on: Card.cs optimization experience in XiuXianCards project*
