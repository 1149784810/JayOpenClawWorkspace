# xiuxian-gamedev

Development knowledge base for XiuXianCards (修仙卡牌/大巴扎客户端) Unity TCG project.

## Quick Reference

| Key | Value |
|-----|-------|
| **Project** | XiuXianCards (修仙卡牌) |
| **Alias** | 大巴扎客户端 (The Bazaar Client) |
| **Engine** | Unity |
| **Networking** | Unity Netcode |
| **Path** | `E:\XiuXianCards\XiuXianCards` |

## Core Systems

- **Slot-based board**: 10 slots per player, x:1-10, y:1, p:0/1
- **Card push system**: Mouse offset determines push direction
- **Card sizes**: Small(1), Medium(2), Big(3) slots
- **Authoritative server**: All logic validated server-side

## When to Use

Use this skill for:
- Implementing new card mechanics
- Debugging push system issues
- Adding network functionality
- Optimizing game logic
- Understanding codebase structure

## Key Files

| File | Purpose |
|------|---------|
| `GameLogic/GameLogic.cs` | Core rules, push algorithm |
| `GameLogic/Card.cs` | Card data, optimized caching |
| `GameLogic/Slot.cs` | Slot coordinate system |
| `GameClient/BoardCard.cs` | Visuals, drag/drop, timeout |
| `GameServer/GameServer.cs` | Request handling |
| `Network/NetworkMsg.cs` | Message structures |

## Documentation

- `SKILL.md` - Complete architecture and implementation guide

## Usage Example

When user asks about card push system:
```
[Invoke xiuxian-gamedev skill]
→ Reference push system implementation
→ Check mouse offset calculation
→ Verify server-side validation
→ Apply timeout pattern
```

## Related

- Original game: The Bazaar
- Pattern: Authoritative Server
- Optimization: Dictionary caching, static empty lists
