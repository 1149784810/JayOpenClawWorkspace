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

### Tree Structure

```
需求A
├── Feature Type
│   ├── Card Mechanics (卡牌机制)
│   │   ├── Push System (推挤系统)
│   │   │   ├── Files: GameLogic.cs, GameClient.cs, GameServer.cs
│   │   │   ├── Functions: MoveCard(), TryGetPushSlots()
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
│   │   └── Ability System (技能系统)
│   │       ├── Files: AbilityData.cs, Card.cs, GameLogic.cs
│   │       ├── Functions: TriggerAbility(), CanCastAbility()
│   │       └── Impact: Effect resolution, Target validation
│   │
│   ├── Slot System (槽位系统)
│   │   ├── Files: Slot.cs, BoardSlot.cs
│   │   ├── Functions: 
│   │   │   - Slot.Get(), Slot.GetAll()
│   │   │   - BoardSlot.GetSlot(), GetLeftSlot(), GetRightSlot()
│   │   ├── Impact:
│   │   │   - All Slot constructors in GameLogic.cs
│   │   │   - Network serialization in Slot.cs
│   │   │   - Equality operators (== and !=)
│   │   └── Backward Compatibility:
│   │       - Always use named parameters or full parameter list
│   │       - Update ALL call sites: Search "new Slot("
│   │
│   └── Card Data (卡牌数据)
│       ├── Files: CardData.cs, Card.cs
│       ├── Functions: 
│       │   - CardData.Get()
│       │   - Card.Get()
│       │   - Card.Create()
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

### v1.0 (2026-02-10)
- Initial skill creation
- Card push system implementation
- Codebase analysis and optimization notes
- Network architecture documentation
- Requirement path tree for quick feature lookup
