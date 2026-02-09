# Test Fixed Push Algorithm

def test_push_algorithm():
    print('=' * 60)
    print('Fixed Algorithm Verification')
    print('=' * 60)
    print()
    
    # Test: Card A at slot 2, place at slot 3, push left
    print('Test: Card A at slot 2, target slot 3, push left')
    print()
    
    # Initial state
    slots = {1: None, 2: 'Card A', 3: 'Existing'}
    target_x = 3
    push_left = True
    direction = -1
    
    print('Initial state:')
    for x in [1, 2, 3]:
        content = slots[x] if slots[x] else 'Empty'
        print('  Slot %d: %s' % (x, content))
    print()
    
    # Step 1: Find empty slot
    print('Step 1: Find empty slot')
    check_x = target_x + direction  # Start from slot next to target
    empty_slot = None
    
    while 1 <= check_x <= 10:
        content = slots.get(check_x)
        status = content if content else 'Empty'
        print('  Check slot %d: %s' % (check_x, status))
        
        if content is None:
            empty_slot = check_x
            print('  -> Found empty slot at %d' % check_x)
            break
        check_x += direction
    
    if empty_slot is None:
        print('  No empty slot - FAIL')
        return
    
    print()
    
    # Step 2: Collect cards in chain
    print('Step 2: Collect cards in chain')
    cards_in_chain = []
    check_x = empty_slot - direction  # Start from slot before empty
    
    while check_x != target_x:
        card = slots.get(check_x)
        if card:
            cards_in_chain.append((card, check_x))
            print('  Add %s from slot %d' % (card, check_x))
        check_x -= direction
    
    # Add card at target
    target_card = slots[target_x]
    cards_in_chain.append((target_card, target_x))
    print('  Add %s from target slot %d' % (target_card, target_x))
    print('  Chain: %s' % [c[0] for c in cards_in_chain])
    print()
    
    # Step 3: Move cards
    print('Step 3: Move cards')
    for i in range(len(cards_in_chain)):
        card, old_pos = cards_in_chain[i]
        
        if i == 0:
            new_pos = empty_slot
        else:
            new_pos = cards_in_chain[i-1][1]  # Previous card's old position
        
        print('  %s: slot %d -> slot %d' % (card, old_pos, new_pos))
        slots[old_pos] = None
        slots[new_pos] = card
    
    print()
    print('Step 4: Place new card')
    slots[target_x] = 'New Card'
    print('  New Card placed at slot %d' % target_x)
    print()
    
    # Final state
    print('Final state:')
    for x in [1, 2, 3]:
        content = slots[x] if slots[x] else 'Empty'
        print('  Slot %d: %s' % (x, content))
    
    print()
    # Verify
    if slots[1] == 'Card A' and slots[2] == 'Existing' and slots[3] == 'New Card':
        print('SUCCESS: Cards correctly pushed!')
    else:
        print('FAIL: Unexpected final state')
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    test_push_algorithm()
