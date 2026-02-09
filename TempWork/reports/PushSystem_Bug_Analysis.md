# Push System Bug Analysis Report

## BUG 确认

**问题**: 推挤算法计算出的目标位置有误，导致被推的卡牌实际上没有移动。

### 具体场景

```
初始状态:
Slot:    [1]    [2]      [3]
         Empty  Card A   Target

操作: 在Slot 3放置新卡，向左推挤

预期结果:
Slot:    [1]      [2]      [3]
         Card A   Empty    New Card

实际结果 (BUG):
Slot:    [1]      [2]      [3]
         Empty    Card A   New Card

Card A没有被推动！
```

### Bug Location

文件: `GameLogic.cs`  
方法: `TryGetPushSlots`  
行号: 计算 targetX 的部分

```csharp
// WRONG FORMULA
int targetX = pushLeft ? 
    targetSlot.x - emptySlotsNeeded - i : 
    targetSlot.x + emptySlotsNeeded + i;
```

### Root Cause

**错误计算**:
- targetSlot.x = 3
- emptySlotsNeeded = 1  
- i = 0
- targetX = 3 - 1 - 0 = **2**

但Card A已经在slot 2了！所以"移动"到2实际上没有动。

### Correct Logic

被推卡牌的新位置应该基于：
1. 从targetSlot往推挤方向数
2. 每个卡牌按顺序占据下一个可用位置

对于上面的例子：
- 空位在slot 1
- Card A应该被推到slot 1
- 所以targetX应该是1，不是2

## Fix Required

### Option 1: Simplified Fix

在MoveCard中，放置新卡之前先清空targetSlot：

```csharp
public virtual void MoveCard(Card card, Slot slot, float mouseOffsetX = 0f, ...)
{
    // ... existing code ...
    
    if (!TryGetPushSlots(...))
        return;
    
    // FIX: Clear the target slot first by moving existing card to temp
    Card existingCard = game_data.GetSlotCard(slot);
    if (existingCard != null)
    {
        // Find first empty slot in push direction
        Slot tempSlot = FindFirstEmptySlot(slot, pushLeft);
        existingCard.slot = tempSlot;
    }
    
    // Now place the new card
    card.slot = slot;
    
    // Then move other cards in the push chain
    for (int i = cardsToPush.Count - 1; i >= 0; i--)
    {
        cardsToPush[i].slot = targetSlots[i];
    }
}
```

### Option 2: Fix TryGetPushSlots Logic

重新设计算法：

```csharp
private bool TryGetPushSlots(Card movingCard, Slot targetSlot, int cardSize, bool pushLeft, 
    List<Card> cardsToPush, List<Slot> targetSlots)
{
    cardsToPush.Clear();
    targetSlots.Clear();
    
    int direction = pushLeft ? -1 : 1;
    int checkX = targetSlot.x;  // Start from target slot itself
    int slotsNeeded = cardSize;
    int emptySlotsFound = 0;
    
    // First, check if target slot is occupied
    Card existingAtTarget = game_data.GetSlotCard(targetSlot);
    if (existingAtTarget != null && existingAtTarget.uid != movingCard.uid)
    {
        cardsToPush.Add(existingAtTarget);
    }
    else
    {
        emptySlotsFound++;
    }
    
    // Continue scanning
    checkX += direction;
    
    while (emptySlotsFound < slotsNeeded)
    {
        if (checkX < Slot.x_min || checkX > Slot.x_max)
            return false;
        
        Slot checkSlot = new Slot(checkX, targetSlot.y, targetSlot.p);
        Card cardAtSlot = game_data.GetSlotCard(checkSlot);
        
        if (cardAtSlot == null)
        {
            emptySlotsFound++;
        }
        else if (cardAtSlot.uid != movingCard.uid)
        {
            cardsToPush.Add(cardAtSlot);
        }
        
        checkX += direction;
    }
    
    // Calculate target positions
    // cardsToPush[0] is closest to target, should go to first empty
    // cardsToPush[1] should go to second empty, etc.
    int targetPosition = targetSlot.x + (direction * cardSize);
    for (int i = 0; i < cardsToPush.Count; i++)
    {
        if (targetPosition < Slot.x_min || targetPosition > Slot.x_max)
            return false;
        
        targetSlots.Add(new Slot(targetPosition, targetSlot.y, targetSlot.p));
        targetPosition += direction;
    }
    
    return true;
}
```

## Test Cases to Verify

1. Basic push left (Card at 2, target 3) -> Card should move to 1
2. Basic push right (Card at 4, target 3) -> Card should move to 5  
3. Chain push (Cards at 1,2,3, target 4) -> Cards move to 0(fail),1,2
4. Medium card (needs 2 slots)
5. Big card (needs 3 slots)
6. Boundary conditions

## Recommendation

Use **Option 2** (Fix TryGetPushSlots) for cleaner code, or implement **Option 1** as quick fix.
