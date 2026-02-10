---
name: xiuxian-gamedev
description: Development knowledge base for XiuXianCards (修仙卡牌/大巴扎客户端) Unity TCG project
---

# SKILL: xiuxian-gamedev

Development knowledge base for XiuXianCards (修仙卡牌/大巴扎客户端) - a Unity-based TCG with slot-based card pushing mechanics inspired by The Bazaar.

## When to Invoke

Use this skill when working on:
- XiuXianCards (修仙卡牌) game project
- Unity Netcode-based card games
- Slot-based card mechanics
- Client-server architecture for TCG
- Card push system implementations
- Game logic optimization for Unity TCG

## Project Overview

**Project Name**: XiuXianCards (修仙卡牌)  
**Alias**: 大巴扎客户端 (The Bazaar Client)  
**Engine**: Unity  
**Networking**: Unity Netcode for GameObjects  
**Type**: Trading Card Game (TCG) with slot-based board

**Project Path**: `E:\XiuXianCards\XiuXianCards`

## Architecture

### Core Systems

| System | Technology | Files |
|--------|-----------|-------|
| Game Logic | Data-driven (ScriptableObject) | `GameLogic/Game.cs`, `Card.cs`, `Slot.cs` |
| Networking | Unity Netcode | `Network/`, `GameClient/`, `GameServer/` |
| AI | Minimax + Alpha-Beta Pruning | `AI/` |
| Data | ScriptableObject | `Data/CardData.cs`, `AbilityData.cs` |

### Key Design Patterns

1. **Data-Driven Design**: Card data in ScriptableObjects
2. **Client-Server Architecture**: Authoritative server model
3. **Component-Based**: Modular card abilities and effects
4. **Event-Driven**: UnityEvents for game state changes

## Codebase Analysis Summary

### Structure (236 C# Files)

```
Assets/TcgEngine/Scripts/
├── GameLogic/          # Core game rules (server-side)
│   ├── Game.cs        # Game state
│   ├── Card.cs        # Card data + optimized caching
│   ├── Slot.cs        # Slot position system
│   └── GameLogic.cs   # Rule execution
├── GameClient/        # Client-side visuals
│   ├── BoardCard.cs   # Card visual + drag/drop
│   ├── GameClient.cs  # Network client
│   └── BoardSlot.cs   # Slot visuals
├── GameServer/        # Server-side logic
│   └── GameServer.cs  # Request handling
├── Data/              # ScriptableObject data
│   ├── CardData.cs    # Card definitions
│   └── AbilityData.cs # Ability definitions
└── Network/           # Network messages
    └── NetworkMsg.cs  # Message structures
```

### Critical Classes

#### Card.cs - Optimized Implementation

**Key Features**:
- Dictionary cache for O(1) trait/status lookup
- Dirty flag pattern for lazy initialization
- Static empty lists to reduce GC
- Null-safe accessors

**Optimized Methods**:
```csharp
// Fast lookup using dictionary
public CardTrait GetTrait(string id)
{
    EnsureDictsInitialized();
    return trait_dict.TryGetValue(id, out var trait) ? trait : null;
}

// Static empty lists
private static readonly List<CardTrait> EmptyTraitList = new List<CardTrait>();
```

#### CardData.cs

**Card Types**:
```csharp
public enum CardType
{
    None = 0,
    Hero = 5,         // 英雄
    Character = 10,   // 角色
    Spell = 20,       // 法术
    Artifact = 30,    // 神器
    Secret = 40,      // 奥秘
    Equipment = 50    // 装备
}
```

**Card Sizes** (for push system):
```csharp
public enum CardSize
{
    Small = 1,   // 1 slot
    Medium,      // 2 slots
    Big          // 3 slots
}
```

#### Slot.cs (Simplified)

**Coordinate System** (2026-02-10 简化):
- `x`: 1-10 (槽位位置)
- ~~`y`: 已删除~~
- ~~`p`: 已删除~~

**简化说明**: Slot 结构已简化为只包含 x 坐标，y 和 p 字段已删除。后续玩家区分逻辑将在其他地方处理。

**更新（2026-02-10）**: 添加 `SlotType type` 字段，用于区分不同区域（场景/背包/玩家等）。相等判断同时检查 x 和 type。

**Key Methods**:
```csharp
public static int x_min = 1;
public static int x_max = 10;

// 构造函数支持 slotType
public Slot(int x, SlotType type = SlotType.CardStorage)

// 相等判断同时判断 x 和 type
public static bool operator ==(Slot slot1, Slot slot2)
{
    return slot1.x == slot2.x && slot1.type == slot2.type;
}

public bool IsValid() => x >= x_min && x <= x_max;
public bool IsInRangeX(Slot slot, int range) => Mathf.Abs(x - slot.x) <= range;
```

## Card Push System

### Overview

When dragging a card to an occupied slot, existing cards are pushed to make space based on mouse release position.

### Mechanic

| Mouse Position | Push Direction | Logic |
|---------------|----------------|-------|
| Right of slot center | Left | `mouseOffsetX >= 0` → pushLeft = true |
| Left of slot center | Right | `mouseOffsetX < 0` → pushLeft = false |

### Card Sizes

| Size | Slots | Cards |
|------|-------|-------|
| Small | 1 | Standard cards |
| Medium | 2 | Large cards |
| Big | 3 | Massive cards |

### Implementation

#### Files Modified

1. **NetworkMsg.cs** - Extended message
```csharp
public class MsgPlayCard : INetworkSerializable
{
    public string card_uid;
    public Slot slot;
    public float mouseOffsetX;  // NEW
    public SlotType slotType;   // NEW
}
```

2. **GameClient.cs** - Send with offset
```csharp
public void MoveCard(Card card, Slot slot, SlotType type, float mouseOffsetX)
{
    MsgPlayCard mdata = new MsgPlayCard();
    mdata.card_uid = card.uid;
    mdata.slot = slot;
    mdata.slotType = type;
    mdata.mouseOffsetX = mouseOffsetX;  // Send to server
    SendAction(GameAction.Move, mdata);
}
```

3. **GameServer.cs** - Receive and process
```csharp
public void ReceiveMove(ClientData client, SerializedData sdata)
{
    MsgPlayCard msg = sdata.Get<MsgPlayCard>();
    // ... validation ...
    gameplay.MoveCard(card, msg.slot, msg.mouseOffsetX, msg.slotType);
}
```

4. **GameLogic.cs** - Authoritative logic
```csharp
public virtual void MoveCard(Card card, Slot slot, 
    float mouseOffsetX = 0f, SlotType slotType = SlotType.CardStorage)
{
    int cardSize = GetCardSize(card);
    bool pushLeft = mouseOffsetX >= 0;
    
    // Try to find push slots
    if (!TryGetPushSlots(card, slot, cardSize, pushLeft, 
        out var cardsToPush, out var targetSlots))
    {
        return; // Not enough space
    }
    
    // Execute push
    for (int i = cardsToPush.Count - 1; i >= 0; i--)
        cardsToPush[i].slot = targetSlots[i];
    
    card.slot = slot;
    onCardMoved?.Invoke(card, slot);
}
```

5. **BoardCard.cs** - Client handling
```csharp
public void MoveCardToCorrectSlot()
{
    Vector3 mousePos = board.MousePosOnBoard();
    BoardSlot curSlot = GetNearestSlot(mousePos);
    
    float mouseOffsetX = mousePos.x - curSlot.transform.position.x;
    
    // Save for timeout rollback
    pendingStartPos = transform.position;
    isWaitingForServer = true;
    
    GameClient.Get().MoveCard(logicCard, curSlot.GetSlot(), 
        curSlot.type, mouseOffsetX);
}

void Update()
{
    if (isWaitingForServer)
    {
        pendingMoveTimer -= Time.deltaTime;
        
        if (logicCard.slot == pendingTargetSlot)
            isWaitingForServer = false; // Success
        else if (pendingMoveTimer <= 0f)
        {
            // Timeout - bounce back
            transform.position = pendingStartPos;
            isWaitingForServer = false;
        }
    }
}
```

### Correct Implementation (Fixed Version)

**⚠️ Important**: The first implementation had a critical bug. Here's the correct version:

```csharp
public virtual void MoveCard(Card card, Slot slot, float mouseOffsetX = 0f, SlotType slotType = SlotType.CardStorage)
{
    if (card == null || !slot.IsValid())
        return;

    // 1. Get card size (1/2/3 slots)
    int cardSize = GetCardSize(card);
    
    // 2. Determine push direction
    bool pushLeft = mouseOffsetX >= 0;
    int direction = pushLeft ? -1 : 1;
    
    // 3. Check if target slot and subsequent slots are available
    // For Big cards (3 slots), need to check slot, slot+1, slot+2
    bool canPlaceDirectly = true;
    List<Card> blockingCards = new List<Card>();
    
    for (int i = 0; i < cardSize; i++)
    {
        int checkX = slot.x + (i * direction);
        
        // Boundary check
        if (checkX < Slot.x_min || checkX > Slot.x_max)
        {
            canPlaceDirectly = false;
            break;
        }
        
        Slot checkSlot = new Slot(checkX, slot.y, slot.p);
        Card cardAtSlot = game_data.GetSlotCard(checkSlot);
        
        if (cardAtSlot != null && cardAtSlot.uid != card.uid)
        {
            canPlaceDirectly = false;
            blockingCards.Add(cardAtSlot);
        }
    }
    
    // 4. If all slots empty, place directly
    if (canPlaceDirectly && blockingCards.Count == 0)
    {
        card.slot = slot;
        RefreshData();
        onCardMoved?.Invoke(card, slot);
        return;
    }
    
    // 5. Need to push - find enough empty slots
    int emptySlotsNeeded = cardSize;
    int emptySlotsFound = 0;
    int checkX = slot.x + (cardSize * direction);
    HashSet<Card> cardsToPushSet = new HashSet<Card>(blockingCards);
    
    while (checkX >= Slot.x_min && checkX <= Slot.x_max)
    {
        Slot checkSlot = new Slot(checkX, slot.y, slot.p);
        Card cardAtSlot = game_data.GetSlotCard(checkSlot);
        
        if (cardAtSlot == null)
        {
            emptySlotsFound++;
            if (emptySlotsFound >= emptySlotsNeeded)
                break;
        }
        else if (cardAtSlot.uid != card.uid)
        {
            cardsToPushSet.Add(cardAtSlot);
        }
        
        checkX += direction;
    }
    
    // 6. Not enough space
    if (emptySlotsFound < emptySlotsNeeded)
        return;
    
    // 7. Push cards outward by cardSize positions
    List<Card> cardsToPush = new List<Card>(cardsToPushSet);
    cardsToPush.Sort((a, b) => pushLeft ? b.slot.x.CompareTo(a.slot.x) : a.slot.x.CompareTo(b.slot.x));
    
    for (int i = cardsToPush.Count - 1; i >= 0; i--)
    {
        Card cardToPush = cardsToPush[i];
        int targetX = pushLeft ? cardToPush.slot.x - cardSize : cardToPush.slot.x + cardSize;
        
        if (targetX < Slot.x_min || targetX > Slot.x_max)
            return; // Out of bounds
        
        cardToPush.slot = new Slot(targetX, slot.y, slot.p);
    }
    
    // 8. Place moving card
    card.slot = slot;
    RefreshData();
    onCardMoved?.Invoke(card, slot);
}
```

### Development Lessons Learned

#### Bug #1: Cards Not Actually Moving
**Problem**: Formula calculated target position as the card's current position
```csharp
// WRONG
targetX = targetSlot.x - emptySlotsNeeded - i;  // Card at 2 -> target 2
```

**Fix**: Calculate based on card's current position, not target slot
```csharp
// CORRECT
targetX = cardToPush.slot.x - cardSize;  // Card at 2 -> target 2-cardSize
```

#### Bug #2: Not Checking Card Size for Empty Slots
**Problem**: Only checked if target slot was empty, ignored Large cards need 3 slots
```csharp
// WRONG
if (existingCard == null) {
    card.slot = slot;  // Large card needs 3 slots!
    return;
}
```

**Fix**: Check all required slots
```csharp
// CORRECT
for (int i = 0; i < cardSize; i++) {
    int checkX = slot.x + (i * direction);
    // Check this slot...
}
```

#### Bug #3: Wrong Search Direction
**Problem**: Started searching from wrong position, leading to incorrect push chain

**Fix**: Always search from the "far end" of where the card will expand

### Network Synchronization Flow

```
GameLogic.MoveCard()
    ↓
RefreshData() → onRefresh?.Invoke()
onCardMoved?.Invoke(card, slot)
    ↓
GameServer (subscribed to events)
    ↓
OnCardMoved() → SendToAll(GameAction.CardMoved)
RefreshAll() → SendToAll(GameAction.RefreshAll)
    ↓
All Clients receive update
    ↓
BoardCard.OnMove() → Update position
```

**Key Points**:
- Server is authoritative - all calculations happen server-side
- Client sends: card_uid, target_slot, mouse_offset
- Server broadcasts: final positions to all clients
- Client has 0.5s timeout - if no update, bounce back to original position

### Old Algorithm (Deprecated)
        
        Slot checkSlot = new Slot(checkX, targetSlot.y, targetSlot.p);
        Card existing = game_data.GetSlotCard(checkSlot);
        
        if (existing == null)
            emptyFound++;
        else if (existing.uid != movingCard.uid)
        {
            cardsToPush.Add(existing);
            targetSlots.Add(checkSlot);
        }
        
        checkX += direction;
    }
    
    // Calculate final positions
    for (int i = 0; i < cardsToPush.Count; i++)
    {
        int targetX = pushLeft ? 
            targetSlot.x - emptyNeeded - i : 
            targetSlot.x + emptyNeeded + i;
        
        if (targetX < Slot.x_min || targetX > Slot.x_max)
            return false;
        
        targetSlots[i] = new Slot(targetX, targetSlot.y, targetSlot.p);
    }
    
    return true;
}
```

## Networking Patterns

### Authoritative Server Model

```
Client                    Server
  |                         |
  |---- Move Request -----> |
  |    (card, slot, offset) |
  |                         | Validate
  |                         | Execute
  |                         | Broadcast
  |<--- State Update -------|
  |    (all card positions) |
  |                         |
```

### Anti-Cheat Design

- Client only sends input (mouse offset)
- Server calculates all positions
- Client handles timeout/rollback
- No game state trust on client

## Optimization Techniques Applied

### 1. Dictionary Caching (Card.cs)
```csharp
// O(1) lookup instead of O(n)
private Dictionary<string, CardTrait> trait_dict;
private bool dicts_dirty = true;

private void EnsureDictsInitialized()
{
    if (!dicts_dirty) return;
    trait_dict = new Dictionary<string, CardTrait>();
    foreach (var trait in traits)
        trait_dict[trait.id] = trait;
    dicts_dirty = false;
}
```

### 2. Static Empty Lists
```csharp
// Prevent GC allocation
private static readonly List<CardTrait> EmptyTraitList = new List<CardTrait>();

public List<CardTrait> GetTraits()
{
    return traits.Count > 0 ? traits : EmptyTraitList;
}
```

### 3. Lazy Initialization
```csharp
private CardData data = null;

public CardData CardData
{
    get
    {
        if (data == null)
            data = CardData.Get(card_id);
        return data;
    }
}
```

## Common Pitfalls

### 1. Duplicate Method Names
When adding to MonoBehaviour classes, check for existing:
```csharp
// BAD - Duplicate Update()
void Update() { /* existing */ }
void Update() { /* new - CONFLICT! */ }

// GOOD - Merge into existing
void Update()
{
    // existing code
    // new code
}
```

### 2. Missing Using Statements
```csharp
// Required when using SlotType, CardSize enums
using TcgEngine;
```

### 3. Reference vs UID Comparison
```csharp
// WRONG - Reference may be cloned
if (cardAtSlot == movingCard)

// CORRECT - UID is stable
if (cardAtSlot.uid == movingCard.uid)
```

### 4. File Encoding
- Use English comments to avoid encoding issues
- Or ensure consistent UTF-8 encoding

## Testing Checklist

### Push System Tests
- [ ] Small card pushes 1 card
- [ ] Medium card pushes 2 cards
- [ ] Big card pushes 3 cards
- [ ] Push to left boundary (fail)
- [ ] Push to right boundary (fail)
- [ ] Just enough space (success)
- [ ] Network timeout handling
- [ ] Cheat attempt rejection

### General Tests
- [ ] Card play validation
- [ ] Attack targeting
- [ ] Ability casting
- [ ] Equipment attachment
- [ ] Turn transitions
- [ ] Win/lose conditions

## References

- **Inspiration**: The Bazaar (大巴扎)
- **Engine**: Unity 2022+
- **Networking**: Unity Netcode for GameObjects
- **AI**: Minimax with Alpha-Beta pruning

## Requirement Path Tree (需求路径树)

> **Purpose**: Given a requirement (需求A), quickly locate files and functions to modify.  
> **Rule**: When modifying functions, ensure backward compatibility for all call sites.

### 🔄 Maintenance Principle (维护原则)

**CRITICAL**: After each new understanding or requirement analysis:
1. ✅ **Update the tree immediately** - Add new branches, files, functions
2. ✅ **Be as detailed as possible** - More specific = better future lookup
3. ✅ **Ensure complete coverage** - Every requirement should have a path
4. ✅ **If cannot locate precisely** - Update tree after analysis ends

**Never skip tree updates** - This is the foundation for efficient development!

### Tree Structure

```
需求A
├── Feature Type
│   ├── Card Mechanics (卡牌机制)
│   │   ├── Push System (推挤系统)
│   │   │   ├── Files: GameLogic.cs, GameClient.cs, GameServer.cs
│   │   │   ├── Functions: MoveCard(), TryGetPushSlots()
│   │   │   ├── BUG Fixed (2026-02-10 22:19):
│   │   │   │   **Problem**: Pushed cards not updating position on client
│   │   │   │   **Root Cause**: Server only triggered onCardMoved for the moved card,
│   │   │   │                  not for the pushed cards
│   │   │   │   **Fix**: Added onCardMoved?.Invoke(cardToPush, cardToPush.slot) 
│   │   │   │            inside the push loop (GameLogic.cs)
│   │   │   ├── BUG Fixed (2026-02-10 23:25):
│   │   │   │   **Problem**: Push system not working after multi-slot refactor
│   │   │   │   **Root Cause 1**: Push distance used cardSize instead of 1
│   │   │   │   - Wrong: newMainX = mainSlot.x - cardSize
│   │   │   │   - Correct: newMainX = mainSlot.x - 1
│   │   │   │   **Root Cause 2**: Missing conflict detection between pushed cards
│   │   │   │   - Added: HashSet<Slot> validation before push execution
│   │   │   │   **Files**: GameLogic.cs TryPushCards() method
│   │   │   ├── Medium Card Position (2026-02-10 22:36):
│   │   │   │   **Requirement**: Medium card (2 slots) center position at center of 2 slots
│   │   │   │   **Implementation**: BoardCard.CalculateCardPosition()
│   │   │   │   ```csharp
│   │   │   │   // Calculate center between first and last occupied slot
│   │   │   │   int cardSize = GetCardSize(card); // 1/2/3
│   │   │   │   int lastSlotX = slot.x + (cardSize - 1);
│   │   │   │   Vector3 centerPos = (firstSlotPos + lastSlotPos) / 2f;
│   │   │   │   ```
│   │   │   │   **Files**: BoardCard.cs - OnMove(), CalculateCardPosition(), GetCardSize()
│   │   │   └── Impact: Slot.cs equality operators, Network serialization
│   │   │
│   │   ├── Card Play (出牌)
│   │   │   ├── Files: GameLogic.cs, BoardCard.cs
│   │   │   ├── Functions: CanPlayCard(), PlayCard()
│   │   │   └── Impact: Cost validation, Slot validation
│   │   │
│   │   ├── Attack System (攻击系统)
│   │   │   ├── Files: GameLogic.cs, BoardCard.cs
│   │   │   ├── Functions: CanAttackTarget(), AttackCard()
│   │   │   └── Impact: Range check, Damage calculation
│   │   │
│   │   ├── Ability System (技能系统)
│   │   │   ├── Files: AbilityData.cs, Card.cs, GameLogic.cs
│   │   │   ├── Functions: TriggerAbility(), CanCastAbility()
│   │   │   └── Impact: Effect resolution, Target validation
│   │   │
│   │   └── CD System (CD冷却系统) [2026-02-10新增]
│   │       ├── Data Files: CardData.cs
│   │       │   └── Fields: cooldown, cooldown_init, trigger_type, trigger_value, loop_cd
│   │       ├── State Files: Card.cs
│   │       │   └── Fields: current_cd, cd_active
│   │       │   └── Methods: StartCD(), DecreaseCD(), OnCDComplete(), ResetCD()
│   │       ├── Logic Files: GameLogic.cs
│   │       │   ├── Methods: 
│   │       │   │   - InitializeCardCDs() [战斗开始初始化]
│   │       │   │   - ProcessCardCDs() [每回合CD处理]
│   │       │   │   - ExecuteCDEffect() [CD效果执行 - 核心]
│   │       │   │   - GetLeftNeighbor(), GetRightNeighbor() [获取相邻卡牌]
│   │       │   │   - CheckBattleEnd() [检查战斗结束]
│   │       │   └── Trigger Effects:
│   │       │       - Accelerate: 加速相邻卡牌CD
│   │       │       - Slow: 减速敌方卡牌CD
│   │       │       - Damage: 对敌方造成伤害
│   │       │       - Heal: 对己方回复生命
│   │       ├── Network Files: NetworkMsg.cs, GameServer.cs, GameClient.cs
│   │       │   ├── Messages: MsgCDUpdate, MsgCDEffect
│   │       │   └── Events: CD数值变化广播, CD效果触发广播
│   │       └── UI Files: BoardCard.cs
│   │           └── Methods: ShowCDIndicator(), PlayCDEffectAnimation()
│   │
│   ├── Slot System (槽位系统)
│   │   ├── Files: Slot.cs, BoardSlot.cs
│   │   ├── Functions: 
│   │   │   - Slot.Get(), Slot.GetAll()
│   │   │   - BoardSlot.GetSlot(), GetLeftSlot(), GetRightSlot()
│   │   ├── Multi-Slot Impact [2026-02-10]:
│   │   │   - Cards can occupy multiple slots (1-3 based on CardSize)
│   │   │   - Slot comparison: Use Card.OccupiesSlot() instead of slot ==
│   │   │   - Slot retrieval: Use Card.GetMainSlot() instead of card.slot
│   │   │   - Medium cards: Mouse-axis determines which 2 slots
│   │   │   - Big cards: Center slot + left/right neighbors
│   │   │   - Boundary validation required for all multi-slot cards
│   │   ├── Impact:
│   │   │   - All Slot constructors in GameLogic.cs
│   │   │   - Network serialization in Slot.cs
│   │   │   - Equality operators (== and !=)
│   │   │   - Card.OccupiesSlot() for slot occupancy checks
│   │   └── Backward Compatibility:
│   │       - Always use named parameters or full parameter list
│   │       - Update ALL call sites: Search "new Slot("
│   │       - Use Card.GetMainSlot() instead of direct slot access
│   │
│   └── Card Data (卡牌数据)
│       ├── Files: CardData.cs, Card.cs
│       ├── Functions: 
│       │   - CardData.Get()
│       │   - Card.Get()
│       │   - Card.Create()
│       ├── Multi-Slot Card System (多槽位卡牌系统) [2026-02-10重大更新]:
│       │   **Architecture Change**: Card.slot → Card.slots[] List<Slot>
│       │   
│       │   **Core Concept**: Cards occupy 1-3 slots based on CardSize (Small=1, Medium=2, Big=3)
│       │   
│       │   **New Methods in Card.cs**:
│       │   ```csharp
│       │   public Slot GetMainSlot()           // Returns slots[0] or Slot.None
│       │   public bool OccupiesSlot(Slot s)    // Check if card occupies specific slot
│       │   public void SetSlots(List<Slot> s)  // Set all occupied slots + update legacy slot field
│       │   public int GetCardSize()            // Returns 1/2/3 based on CardData.size
│       │   ```
│       │   
│       │   **Access Pattern Rules** (MANDATORY):
│       │   - ❌ NEVER use: `if (card.slot == targetSlot)`
│       │   - ✅ ALWAYS use: `if (card.GetMainSlot() == targetSlot)`
│       │   - ❌ NEVER use: `if (card.slot == slot)` for occupancy check
│       │   - ✅ ALWAYS use: `if (card.OccupiesSlot(slot))`
│       │   
│       │   **Files to Update When Modifying Card Slot**:
│       │   - Card.cs - Add slots field, GetMainSlot(), OccupiesSlot(), SetSlots(), GetCardSize()
│       │   - Game.cs - GetSlotCard() uses OccupiesSlot() instead of slot comparison
│       │   - Player.cs - GetSlotCard() uses OccupiesSlot()
│       │   - GameLogic.cs - CalculateTargetSlots(), PlaceCardAtSlots(), TryPushCards()
│       │   - BoardCard.cs - CalculateMediumCardTargetSlot() for mouse-axis detection
│       │   - AILogic.cs - Use GetMainSlot() for equipment targeting
│       │   - ConditionSelf.cs - Use GetMainSlot() for slot comparison
│       │   
│       │   **Medium Card Logic** (Mouse Axis Detection):
│       │   ```csharp
│       │   // Calculate which pair of slots based on mouse position relative to mid-axes
│       │   // Left of left-mid-axis: would need x-2 and x-1 (check boundary)
│       │   // Between mid-axes: use left pair (x-1 and x)
│       │   // Right of right-mid-axis: use right pair (x and x+1)
│       │   // At boundary (x=1 or x=max): INVALID, return to original position
│       │   ```
│       │   
│       │   **Big Card Logic** (Center + Neighbors):
│       │   - Occupies: center slot + left neighbor + right neighbor
│       │   - Boundary check: requires x-1 >= min AND x+1 <= max
│       │   - At boundary: INVALID, cannot place
│       │   
│       │   **Network Compatibility**:
│       │   - Keep `slot` field for serialization (SetSlots() auto-updates it)
│       │   - slot = slots[0] (main slot)
│       │   - All network messages continue using slot field
│       │   
│       │   **Pre-Flight Checklist** (BEFORE any slot-related change):
│       │   ```powershell
│       │   # Search ALL references first
│       │   Select-String -Path "Assets" -Pattern "card\.slot\b" -Include *.cs
│       │   ```
│       │   - Update ALL files in search results
│       │   - Use GetMainSlot() for slot comparison
│       │   - Use OccupiesSlot() for occupancy check
│       │   
│       │   **Common Pitfalls**:
│       │   1. Forgetting to update Player.GetSlotCard() → OccupiesSlot()
│       │   2. Forgetting to update AILogic equipment targeting → GetMainSlot()
│       │   3. Direct slot comparison in condition checks → GetMainSlot()
│       │   4. Encoding issues when editing files (use English comments only)
│       │   
│       ├── Card Slot Initialization (card.slot 初始化位置):
│       │   **Default State**: Card.Create() → slot = Slot.None (x=0, type=CardStorage)
│       │   
│       │   **1. Puzzle/Level Initialization** (GameLogic.cs:331):
│       │   ```csharp
│       │   foreach (DeckCardSlot card in puzzle.board_cards)
│       │   {
│       │       Card acard = Card.Create(card.card, variant, player);
│       │       acard.slot = new Slot(card.slot.x, SlotType.CardStorage);
│       │   }
│       │   ```
│       │   
│       │   **2. Play Card to Board** (GameLogic.cs:382):
│       │   ```csharp
│       │   public virtual void PlayCard(Card card, Slot slot)
│       │   {
│       │       card.slot = slot;  // 出牌时设置槽位
│       │   }
│       │   ```
│       │   
│       │   **3. Move Card (Direct Place)** (GameLogic.cs:432):
│       │   ```csharp
│       │   if (canPlaceDirectly && blockingCards.Count == 0)
│       │   {
│       │       card.slot = slot;  // 移动时设置槽位
│       │   }
│       │   ```
│       │   
│       │   **4. Move Card (After Push)** (GameLogic.cs:512):
│       │   ```csharp
│       │   // 推动其他卡牌后，最后放置移动的卡牌
│       │   card.slot = slot;  // 推挤后设置槽位
│       │   ```
│       ├── Impact: 
│       │   - All card instantiation
│       │   - Serialization
│       └── Backward Compatibility:
│           - Static dictionary caching pattern
│
├── Network Layer (网络层)
│   ├── Message Definitions (消息定义)
│   │   ├── Files: NetworkMsg.cs
│   │   ├── Functions: Serialize(), Deserialize()
│   │   └── Impact: 
│   │       - ALL message handlers in GameClient.cs, GameServer.cs
│   │       - Protocol compatibility (version matching)
│   │
│   ├── Client-Server Communication (通信)
│   │   ├── Files: GameClient.cs, GameServer.cs
│   │   ├── Functions:
│   │   │   - SendToServer(), SendToAll()
│   │   │   - RegisterRefresh(), OnRefreshXxx()
│   │   └── Impact: 
│   │       - Event subscription/unsubscription
│   │       - Network delivery type selection
│   │
│   └── State Synchronization (状态同步)
│       ├── Files: GameLogic.cs
│       ├── Functions: RefreshData(), onRefresh event
│       └── Impact: 
│           - All UI update subscriptions
│           - Board card position updates
│
└── UI Layer (界面层)
    ├── Board Visualization (棋盘显示)
    │   ├── Files: BoardCard.cs, BoardSlot.cs
    │   ├── Functions: 
    │   │   - OnMove(), OnSummon()
    │   │   - UpdatePosition(), UpdateState()
    │   └── Impact: 
    │       - Transform updates
    │       - Animation triggers
    │
    ├── Hand Cards (手牌)
    │   ├── Files: HandCard.cs
    │   ├── Functions: 
    │   │   - StartDrag(), EndDrag()
    │   │   - UpdatePosition()
    │   └── Impact: 
    │       - Drag state management
    │       - Mouse event handling
    │
    └── Game UI (游戏UI)
        ├── Files: GameUI.cs, UIPanel.cs
        ├── Functions: 
        │   - ShowPanel(), HidePanel()
        │   - RefreshUI()
        └── Impact: 
            - Panel state transitions
            - Event listener cleanup
```

### Quick Reference by Requirement

#### If modifying `Slot` struct
```
1. Update Slot.cs:
   - Constructor(s)
   - NetworkSerialize()
   - Equality operators (== and !=)
   - Equals() and GetHashCode()

2. Search and update ALL "new Slot(" in:
   ✓ GameLogic.cs (4 locations)
   ✓ BoardSlot.cs (3 locations)
   ✓ BoardSlotGroup.cs (1 location)
   ✓ BoardSlotPlayer.cs (1 location)
   ✓ AILogic.cs (1 location)

3. Test impact on:
   ✓ GetSlotCard() in Game.cs
   ✓ All Slot equality comparisons
```

#### If adding new Card Mechanic
```
1. Define data in CardData.cs
2. Implement logic in GameLogic.cs
3. Add validation in CanXxx() functions
4. Update GameClient.cs for UI feedback
5. Add to GameServer.cs for server validation
6. Test network sync with RefreshData()
```

#### If implementing Multi-Slot Card System (多槽位卡牌系统)
```
⚠️ MAJOR ARCHITECTURE CHANGE - Follow strictly!

PRE-FLIGHT (Before starting):
  Search ALL references: Select-String -Path "Assets" -Pattern "card\.slot\b" -Include *.cs

1. Card.cs - Core Changes:
   ✓ Add field: public List<Slot> slots = new List<Slot>();
   ✓ Add method: public Slot GetMainSlot() → slots[0] or Slot.None
   ✓ Add method: public bool OccupiesSlot(Slot s) → slots.Contains(s)
   ✓ Add method: public void SetSlots(List<Slot> s) → updates slots + legacy slot field
   ✓ Add method: public int GetCardSize() → 1/2/3 based on CardData.size

2. Game.cs - Slot Lookup:
   ✓ Change: GetSlotCard() uses card.OccupiesSlot(slot) instead of card.slot == slot

3. Player.cs - Slot Lookup:
   ✓ Change: GetSlotCard() uses card.OccupiesSlot(slot)

4. GameLogic.cs - Complete Rewrite:
   ✓ Replace MoveCard() with multi-slot aware version
   ✓ Add CalculateTargetSlots(Slot target, int size, SlotType) → List<Slot>
   ✓ Add PlaceCardAtSlots(Card, List<Slot>, Player)
   ✓ Add TryPushCards() with multi-slot push logic
   ✓ Update PlayCard() to use CalculateTargetSlots()

5. BoardCard.cs - Medium Card Mouse Detection:
   ✓ Add CalculateMediumCardTargetSlot(BoardSlot, Vector3) → Slot
     - Uses mid-axis detection for slot pair selection
     - Returns Slot.None if at boundary (invalid)
   ✓ Add GetSlotSpacing() for mid-axis calculation
   ✓ Update MoveCardToCorrectSlot() for medium card special handling
   ✓ Update OnMove() to use CalculateCardPositionFromSlots()

6. AILogic.cs - Equipment Targeting:
   ✓ Change: tcard.slot → tcard.GetMainSlot()

7. ConditionSelf.cs - Slot Comparison:
   ✓ Change: caster.slot → caster.GetMainSlot()

8. Encoding Safety:
   ✓ Use English comments ONLY to avoid garbled text
   ✓ Verify file readability after each edit

ACCESS PATTERN RULES (MANDATORY):
  ❌ NEVER: if (card.slot == targetSlot)
  ✅ ALWAYS: if (card.GetMainSlot() == targetSlot)
  ❌ NEVER: if (card.slot == slot)  // for occupancy
  ✅ ALWAYS: if (card.OccupiesSlot(slot))

NETWORK COMPATIBILITY:
  ✓ Keep legacy 'slot' field for serialization
  ✓ SetSlots() auto-updates: slot = slots[0]
  ✓ All network messages continue using slot field

BOUNDARY HANDLING:
  Medium card at x=1 or x=max → INVALID (return to original position)
  Big card needs x-1 >= min AND x+1 <= max → Check before placement
```

#### If adding CD System (CD冷却系统)
```
1. Data Definition (CardData.cs):
   ✓ Add: cooldown, cooldown_init, trigger_type, trigger_value, loop_cd

2. State Management (Card.cs):
   ✓ Add fields: current_cd, cd_active
   ✓ Add methods: StartCD(), DecreaseCD(), OnCDComplete(), ResetCD()

3. Core Logic (GameLogic.cs):
   ✓ Add InitializeCardCDs() - Call at battle start
   ✓ Add ProcessCardCDs() - Call at end of each turn
   ✓ Add ExecuteCDEffect() - Handle 4 effect types
   ✓ Add GetLeftNeighbor(), GetRightNeighbor() - For adjacent cards
   ✓ Add CheckBattleEnd() - Check HP <= 0

4. Network Layer:
   ✓ Add MsgCDUpdate (NetworkMsg.cs) - Sync CD value
   ✓ Add MsgCDEffect (NetworkMsg.cs) - Broadcast effect trigger
   ✓ Update GameServer.cs - Validate CD logic
   ✓ Update GameClient.cs - Handle CD messages

5. UI Layer (BoardCard.cs):
   ✓ Add ShowCDIndicator() - Display CD number
   ✓ Add PlayCDEffectAnimation() - Visual feedback

6. Effect Types to Implement:
   ✓ Accelerate: Reduce adjacent cards CD
   ✓ Slow: Increase enemy cards CD
   ✓ Damage: Deal damage to opponent player
   ✓ Heal: Restore HP to friendly player

7. Battle End Condition:
   ✓ Check after Damage effect: if HP <= 0, end battle
   ✓ Loop CD if loop_cd=true until battle ends
```

#### If modifying Network Messages
```
1. Update Msg definition in NetworkMsg.cs
2. Add handler in GameClient.cs (if server→client)
3. Add handler in GameServer.cs (if client→server)
4. Register handler in constructor
5. Test with both client and server builds
```

### Impact Analysis Template

When modifying a function, check:

1. **Direct Callers**: Who calls this function?
   ```powershell
   # Search in PowerShell
   Select-String -Path "E:\XiuXianCards\XiuXianCards\Assets" -Pattern "FunctionName\(" -Include *.cs
   ```

2. **Event Subscribers**: Who subscribes to this event?
   ```csharp
   // Search for += and -=
   gameplay.onRefresh += Handler;  // Subscribe
   gameplay.onRefresh -= Handler;  // Unsubscribe
   ```

3. **Virtual Overrides**: Who overrides this?
   ```csharp
   // Search for override keyword
   public override void FunctionName()
   ```

4. **Network Impact**: Does this affect network sync?
   - Check if function triggers RefreshData() or events
   - Verify serialized data consistency

## Changelog

### v1.1 (2026-02-10 22:48)
- **MAJOR**: Card.slot → Card.slots[] array refactoring
  - Support multi-slot cards (Small=1, Medium=2, Big=3)
  - Medium card: mouse-axis based slot selection
  - Big card: center slot + neighbors
  - Boundary validation for all card sizes
  - Network compatibility maintained (slot field preserved)
  - Files modified: Card.cs, Game.cs, GameLogic.cs, BoardCard.cs, Player.cs, AILogic.cs, ConditionSelf.cs
- **Fixes (2026-02-10 23:00)**:
  - Fixed all card.slot references to use GetMainSlot() or OccupiesSlot()
  - Fixed Player.GetSlotCard() to use OccupiesSlot()
  - Fixed AILogic equipment target slot checking
  - Fixed ConditionSelf target slot comparison

### v1.0 (2026-02-10)
- Initial skill creation
- Card push system implementation
- Codebase analysis and optimization notes
- Network architecture documentation
- Requirement path tree for quick feature lookup
