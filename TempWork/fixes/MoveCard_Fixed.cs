# 修复后的 MoveCard 方法

```csharp
public virtual void MoveCard(Card card, Slot slot, float mouseOffsetX = 0f, SlotType slotType = SlotType.CardStorage)
{
    if (card == null || !slot.IsValid())
        return;

    // Get card size (how many slots it needs)
    int cardSize = GetCardSize(card);
    
    // Determine push direction: positive offset = right side, push left; negative = left side, push right
    bool pushLeft = mouseOffsetX >= 0;
    
    // Check if target slot has a card
    Card existingCard = game_data.GetSlotCard(slot);

    if (existingCard == null || existingCard.uid == card.uid)
    {
        // Slot is empty, move directly
        card.slot = slot;
        RefreshData();
        onCardMoved?.Invoke(card, slot);
        return;
    }

    // Slot occupied, need to execute push algorithm
    int direction = pushLeft ? -1 : 1;  // -1=left, +1=right
    
    // Step 1: Find the first empty slot in push direction
    // Start checking from the slot next to target slot
    int checkX = slot.x + direction;
    Slot emptySlot = Slot.None;
    
    while (checkX >= Slot.x_min && checkX <= Slot.x_max)
    {
        Slot checkSlot = new Slot(checkX, slot.y, slot.p);
        Card cardAtSlot = game_data.GetSlotCard(checkSlot);
        
        if (cardAtSlot == null)
        {
            // Found empty slot
            emptySlot = checkSlot;
            break;
        }
        
        checkX += direction;
    }
    
    // If no empty slot found, cannot push
    if (emptySlot == Slot.None)
        return;
    
    // Step 2: Collect all cards in the push chain (from empty slot back to target)
    List<Card> cardsInChain = new List<Card>();
    checkX = emptySlot.x - direction;  // Start from slot before empty
    
    while (checkX != slot.x)
    {
        Slot checkSlot = new Slot(checkX, slot.y, slot.p);
        Card cardAtSlot = game_data.GetSlotCard(checkSlot);
        if (cardAtSlot != null && cardAtSlot.uid != card.uid)
            cardsInChain.Add(cardAtSlot);
        checkX -= direction;
    }
    
    // Add the card at target slot
    cardsInChain.Add(existingCard);
    
    // Step 3: Move cards (from empty slot side toward target)
    // Each card moves to the position of the card that was "behind" it
    for (int i = 0; i < cardsInChain.Count; i++)
    {
        Card cardToMove = cardsInChain[i];
        Slot newSlot;
        
        if (i == 0)
        {
            // First card (closest to empty slot) moves to empty slot
            newSlot = emptySlot;
        }
        else
        {
            // Other cards move to where the previous card was
            newSlot = cardsInChain[i - 1].slot;
        }
        
        cardToMove.slot = newSlot;
    }
    
    // Step 4: Finally place the moving card at target slot
    card.slot = slot;
    
    RefreshData();
    onCardMoved?.Invoke(card, slot);
}
```

## 算法解释

### 示例：Card A at slot 2, place at slot 3, push left

**Step 1: Find empty slot**
- Start from slot 2 (3 + (-1) = 2)
- Slot 2 has Card A, continue
- Check slot 1 (2 + (-1) = 1)  
- Slot 1 is empty! emptySlot = slot 1

**Step 2: Collect cards in chain**
- Start from slot before empty (slot 2)
- Add Card A to cardsInChain
- Move toward target (slot 2 - (-1) = slot 3, but stop at target)
- Add existingCard (at target slot 3) to cardsInChain
- Result: cardsInChain = [Card A, existingCard]

**Step 3: Move cards**
- Card A (index 0): moves to emptySlot (slot 1)
- existingCard (index 1): moves to Card A's old position (slot 2)

**Step 4: Place new card**
- New card at slot 3

**Final state:**
- Slot 1: Card A (pushed from 2)
- Slot 2: existingCard (pushed from 3)  
- Slot 3: New card (placed)

## 关键修复点

1. **从target slot旁边开始找空位**，而不是target slot本身
2. **从空位往回收集卡牌**，确保正确的推动顺序
3. **按顺序移动**：离空位最近的卡先动，依次填补空位
