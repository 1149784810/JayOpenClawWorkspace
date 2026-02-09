using System;
using System.Collections.Generic;
using NUnit.Framework;
using TcgEngine;
using TcgEngine.Gameplay;

namespace Tests
{
    /// <summary>
    /// Unit tests for Card Push System
    /// 检测推挤算法的各种问题
    /// </summary>
    public class PushSystemTests
    {
        private Game game;
        private GameLogic gameplay;
        private Player player0;
        private Player player1;

        [SetUp]
        public void Setup()
        {
            game = new Game("test-game", 2);
            gameplay = new GameLogic(game);
            
            player0 = new Player(0);
            player1 = new Player(1);
            game.players[0] = player0;
            game.players[1] = player1;
            
            game.state = GameState.Play;
            game.first_player = 0;
            game.current_player = 0;
        }

        // ==================== Helper Methods ====================
        
        private Card CreateCard(string id, CardSize size, int playerId)
        {
            var cardData = new CardData
            {
                id = id,
                size = size
            };
            var card = Card.Create(cardData, VariantData.GetDefault(), game.GetPlayer(playerId));
            card.uid = $"card_{id}_{Guid.NewGuid().ToString().Substring(0, 8)}";
            return card;
        }

        private void PlaceCardOnSlot(Card card, int x, int playerId)
        {
            Slot slot = new Slot(x, 1, Slot.GetP(playerId));
            card.slot = slot;
            game.GetPlayer(playerId).cards_board.Add(card);
        }

        // ==================== Test Case 1: Basic Push Left ====================
        
        [Test]
        public void Test_SmallCard_PushLeft_OneCard()
        {
            // Setup: [Empty] [Card A] [Target Slot 3]
            // Place card A at slot 2
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 2, 0);
            
            // Create moving card (Small)
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            
            // Target slot 3, push left (mouse on right side)
            Slot targetSlot = new Slot(3, 1, Slot.GetP(0));
            float mouseOffsetX = 0.5f; // Positive = push left
            
            // Execute
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            // Verify
            Assert.AreEqual(targetSlot, movingCard.slot, "Moving card should be at target slot");
            Assert.AreEqual(1, cardA.slot.x, "Card A should be pushed to slot 1");
            
            Console.WriteLine("✅ Test 1 PASSED: Small card push left works");
        }

        // ==================== Test Case 2: Medium Card Needs 2 Slots ====================
        
        [Test]
        public void Test_MediumCard_NeedsTwoSlots_PushLeft()
        {
            // Setup: [Empty] [Card A] [Target Slot 3-4 needed]
            // Medium card needs slots 3 AND 4
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 2, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Medium, 0);
            
            Slot targetSlot = new Slot(3, 1, Slot.GetP(0));
            float mouseOffsetX = 0.5f; // Push left
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            // Medium card occupies slots 3 and 4
            // Card A should be pushed to slot 1
            Assert.AreEqual(targetSlot, movingCard.slot, "Medium card should be at slot 3");
            Assert.AreEqual(1, cardA.slot.x, "Card A should be pushed to slot 1");
            
            Console.WriteLine("✅ Test 2 PASSED: Medium card push works");
        }

        // ==================== Test Case 3: Chain Push ====================
        
        [Test]
        public void Test_ChainPush_ThreeCards()
        {
            // Setup: [Card C] [Card B] [Card A] [Target Slot 4]
            // All should be pushed left
            var cardC = CreateCard("C", CardSize.Small, 0);
            var cardB = CreateCard("B", CardSize.Small, 0);
            var cardA = CreateCard("A", CardSize.Small, 0);
            
            PlaceCardOnSlot(cardC, 1, 0);
            PlaceCardOnSlot(cardB, 2, 0);
            PlaceCardOnSlot(cardA, 3, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            Slot targetSlot = new Slot(4, 1, Slot.GetP(0));
            float mouseOffsetX = 0.5f; // Push left
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            Assert.AreEqual(targetSlot, movingCard.slot, "Moving card at slot 4");
            Assert.AreEqual(3, cardA.slot.x, "Card A pushed to slot 3");
            Assert.AreEqual(2, cardB.slot.x, "Card B pushed to slot 2");
            Assert.AreEqual(1, cardC.slot.x, "Card C stays at slot 1");
            
            Console.WriteLine("✅ Test 3 PASSED: Chain push works");
        }

        // ==================== Test Case 4: No Space - Should Fail ====================
        
        [Test]
        public void Test_NoSpace_PushFails()
        {
            // Setup: [Card A at slot 1] [Target Slot 2] - pushing left but no space
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 1, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            Slot originalSlot = movingCard.slot;
            
            Slot targetSlot = new Slot(2, 1, Slot.GetP(0));
            float mouseOffsetX = 0.5f; // Push left - but slot 1 is occupied, no space left of it
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            // Should fail - no space to push
            Assert.AreNotEqual(targetSlot, movingCard.slot, "Move should fail - no space");
            
            Console.WriteLine("✅ Test 4 PASSED: No space correctly fails");
        }

        // ==================== Test Case 5: Empty Slot - Direct Placement ====================
        
        [Test]
        public void Test_EmptySlot_DirectPlacement()
        {
            // Setup: [Empty] [Target Slot 5] [Empty]
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            
            Slot targetSlot = new Slot(5, 1, Slot.GetP(0));
            float mouseOffsetX = 0.5f;
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            Assert.AreEqual(targetSlot, movingCard.slot, "Should place directly on empty slot");
            
            Console.WriteLine("✅ Test 5 PASSED: Direct placement works");
        }

        // ==================== Test Case 6: Push Right ====================
        
        [Test]
        public void Test_PushRight_Basic()
        {
            // Setup: [Target Slot 3] [Card A] [Empty]
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 4, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            
            Slot targetSlot = new Slot(3, 1, Slot.GetP(0));
            float mouseOffsetX = -0.5f; // Negative = push right
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            Assert.AreEqual(targetSlot, movingCard.slot, "Moving card at slot 3");
            Assert.AreEqual(5, cardA.slot.x, "Card A pushed right to slot 5");
            
            Console.WriteLine("✅ Test 6 PASSED: Push right works");
        }

        // ==================== Test Case 7: Medium Card At Boundary ====================
        
        [Test]
        public void Test_MediumCard_AtBoundary_Fail()
        {
            // Setup: [Card A at slot 9] [Target Slot 10]
            // Medium card needs slots 10 AND 11 - but 11 is out of bounds
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 9, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Medium, 0);
            
            Slot targetSlot = new Slot(10, 1, Slot.GetP(0));
            float mouseOffsetX = -0.5f; // Push right - but no slot 11
            
            gameplay.MoveCard(movingCard, targetSlot, mouseOffsetX, SlotType.CardStorage);
            
            // Should fail - no room for 2-slot card at boundary
            Assert.AreNotEqual(targetSlot, movingCard.slot, "Should fail - boundary issue");
            
            Console.WriteLine("✅ Test 7 PASSED: Boundary check works");
        }

        // ==================== Debug Test: Inspect Algorithm ====================
        
        [Test]
        public void Debug_TryGetPushSlots()
        {
            // Setup simple scenario
            var cardA = CreateCard("A", CardSize.Small, 0);
            PlaceCardOnSlot(cardA, 2, 0);
            
            var movingCard = CreateCard("Moving", CardSize.Small, 0);
            Slot targetSlot = new Slot(3, 1, Slot.GetP(0));
            
            List<Card> cardsToPush = new List<Card>();
            List<Slot> targetSlots = new List<Slot>();
            
            // Call private method via reflection or make it internal for testing
            // For now, let's just trace through manually
            
            Console.WriteLine("Debug Info:");
            Console.WriteLine($"Target slot: x={targetSlot.x}");
            Console.WriteLine($"Card A position: x={cardA.slot.x}");
            Console.WriteLine($"Push left: checkX starts at {targetSlot.x - 1}");
            
            // Simulate algorithm
            int cardSize = 1; // Small
            bool pushLeft = true;
            int direction = pushLeft ? -1 : 1;
            int checkX = pushLeft ? targetSlot.x - 1 : targetSlot.x + 1;
            
            Console.WriteLine($"Direction: {direction}");
            Console.WriteLine($"Starting checkX: {checkX}");
            Console.WriteLine($"Will check slot {checkX} first");
            
            // The first check is at slot 2, which has Card A
            // So cardsToPush gets Card A
            // Then checkX becomes 1
            // Slot 1 is empty, so emptyFound becomes 1
            // emptyNeeded is 1, so loop exits
            // Then calculate target for Card A: targetX = 3 - 1 - 0 = 2
            // Wait, that would put Card A back at slot 2!
            
            int targetX = targetSlot.x - cardSize - 0;
            Console.WriteLine($"Calculated targetX for pushed card: {targetX}");
            Console.WriteLine($"Card A would be moved to slot {targetX}");
            
            if (targetX == cardA.slot.x)
            {
                Console.WriteLine("❌ BUG FOUND: Pushed card stays at same position!");
                Console.WriteLine("Algorithm calculates targetX incorrectly");
            }
        }
    }
}
