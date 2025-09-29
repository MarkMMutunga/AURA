# AURA (Adaptive Understanding & Reflective Assistant)

🤖 A simple terminal-based AI companion that remembers your goals and moods.

## Features

- **Goal Tracking**: Tell AURA "I want to..." and it will remember your goals
- **Mood Support**: Share how you're feeling and get encouraging responses
- **Persistent Memory**: Uses SQLite database to remember everything between sessions
- **Motivational Messages**: Get random encouragement when you need it
- **Goal Reminders**: See your saved goals every time you start AURA

## How to Use

1. **Run AURA**:
   ```bash
   python aura.py
   ```

2. **Set Goals**: 
   - "I want to learn Python"
   - "I'd like to exercise more"
   - "My goal is to read more books"

3. **Share Moods**:
   - "I feel tired"
   - "I'm feeling stressed"
   - "I feel happy today"

4. **Commands**:
   - Type `goals` to see all your saved goals
   - Type `encourage` for random motivation
   - Type `quit` to exit

## Requirements

- Python 3.6+
- No external dependencies (uses built-in sqlite3)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/AURA.git
   cd AURA
   ```

2. Run AURA:
   ```bash
   python aura.py
   ```

## Example Interaction

```
🤖 Welcome to AURA - Your Adaptive Understanding & Reflective Assistant!

💭 You: I want to learn machine learning
🤖 AURA: ✅ Great! I've added your goal: 'Learn machine learning' to your list. I'll help you remember it!

💭 You: I feel stressed about work
🤖 AURA: Stress can be overwhelming, but you're stronger than you think! 💪

💭 You: goals
🎯 Here are your current goals:
1. Learn machine learning
   📅 Added on September 29, 2025
```

## Database

AURA creates an SQLite database (`aura_memory.db`) with two tables:
- **goals**: Stores your goals with timestamps
- **moods**: Logs your mood entries

## Contributing

Feel free to fork this project and add your own features! Some ideas:
- Web interface
- Goal completion tracking
- Mood analytics
- Reminder notifications

## License

MIT License - feel free to use and modify as you wish!

## Author

**Mark Mikile Mutunga**
- Email: markmiki03@gmail.com
- Phone: +254707678643

---

Built with ❤️ to help you stay motivated and achieve your goals!

© 2025 Mark Mikile Mutunga. All rights reserved.
