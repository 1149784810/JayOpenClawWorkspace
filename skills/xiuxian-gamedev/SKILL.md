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

#### Slot.cs

**Coordinate System**:
- `x`: 1-10 (slot position)
- `y`: 1 (row, currently single row)
- `p`: 0/1 (player ID)

**Key Methods**:
```csharp
public static int x_min = 1;
public static int x_max = 10;

public bool IsValid() => x >= x_min && x <= x_max && y >= y_min && y <= y_max;
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

### Algorithm: TryGetPushSlots

```csharp
private bool TryGetPushSlots(Card movingCard, Slot targetSlot, 
    int cardSize, bool pushLeft, List<Card> cardsToPush, List<Slot> targetSlots)
{
    int direction = pushLeft ? -1 : 1;
    int checkX = pushLeft ? targetSlot.x - 1 : targetSlot.x + 1;
    int emptyNeeded = cardSize;
    int emptyFound = 0;
    
    while (emptyFound < emptyNeeded)
    {
        if (checkX < Slot.x_min || checkX > Slot.x_max)
            return false; // Boundary
        
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

## Changelog

### v1.0 (2026-02-10)
- Initial skill creation
- Card push system implementation
- Codebase analysis and optimization notes
- Network architecture documentation
