#!/usr/bin/env python3
"""
AURA (Adaptive Understanding & Reflective Assistant)
A simple terminal-based AI companion that remembers user goals and moods.

Author: Mark Mikile Mutunga
Email: markmiki03@gmail.com
Phone: +254707678643
Copyright (c) 2025 Mark Mikile Mutunga. All rights reserved.

This software is licensed under the MIT License.
See the LICENSE file for full license text.
"""

#==============================================================================
# Copyright (c) 2025 Mark Mikile Mutunga
# 
# Author: Mark Mikile Mutunga
# Email: markmiki03@gmail.com
# Phone: +254707678643
# 
# Licensed under the MIT License
# See LICENSE file for details
#==============================================================================

import sqlite3
import datetime
import re
import random

class AURA:
    def __init__(self):
        """Initialize AURA with database connection and setup."""
        self.db_name = "aura_memory.db"
        self.setup_database()
        
        # Empathetic mood responses (single, more personal responses)
        self.mood_responses = {
            "tired": "I hear you. 💙 Maybe a quick rest or even a 5-minute stretch could help.",
            "stressed": "That sounds tough 😔. How about taking things one step at a time?",
            "unmotivated": "I get it. Small wins count too! Try doing just one tiny task.",
            "happy": "Love to hear that! 🎉 Keep riding that wave of positivity.",
            "sad": "I understand that feeling 💙. It's okay to feel sad - your emotions are valid.",
            "anxious": "Anxiety is really hard 😰. Try taking a few deep breaths with me.",
            "overwhelmed": "That sounds really overwhelming 😓. Let's break it down into smaller pieces.",
            "frustrated": "Frustration is tough 😤. Take a moment to breathe and reset.",
            "lonely": "I'm here with you 🤗. You're not alone in this journey.",
            "excited": "Your excitement is contagious! ✨ What's got you feeling so good?",
            "worried": "I can sense your worry 😟. Let's focus on what you can control right now.",
            "confused": "Confusion is normal when learning something new 🤔. Take it step by step.",
            "default": "Thanks for sharing that. Remember, I'm here to keep you moving forward 💡."
        }
    
    def setup_database(self):
        """Create database tables if they don't exist."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Create goals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_text TEXT NOT NULL,
                    date_added TEXT NOT NULL,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Create moods table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mood TEXT NOT NULL,
                    description TEXT,
                    date_logged TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print("🤖 AURA database initialized successfully!")
            
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
    
    def add_goal(self, goal_text):
        """Store a new goal in the database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Clean up the goal text (remove "I want to" prefix)
            clean_goal = re.sub(r'^(i want to|i\'d like to|i would like to)\s*', '', goal_text.lower()).strip()
            clean_goal = clean_goal.capitalize()
            
            cursor.execute('''
                INSERT INTO goals (goal_text, date_added)
                VALUES (?, ?)
            ''', (clean_goal, datetime.datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return f"✅ Great! I've added your goal: '{clean_goal}' to your list. I'll help you remember it!"
            
        except sqlite3.Error as e:
            return f"❌ Error saving goal: {e}"
    
    def add_mood(self, mood, description=""):
        """Store a mood entry in the database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO moods (mood, description, date_logged)
                VALUES (?, ?, ?)
            ''', (mood, description, datetime.datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            print(f"❌ Error saving mood: {e}")
            return False
    
    def get_goals(self):
        """Retrieve all active goals from the database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT goal_text, date_added FROM goals 
                WHERE status = 'active' 
                ORDER BY date_added DESC
            ''')
            
            goals = cursor.fetchall()
            conn.close()
            
            return goals
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving goals: {e}")
            return []
    
    def detect_goal(self, user_input):
        """Check if user input contains a goal statement."""
        goal_patterns = [
            r'\bi want to\b',
            r'\bi\'d like to\b',
            r'\bi would like to\b',
            r'\bmy goal is to\b',
            r'\bi plan to\b',
            r'\bi hope to\b'
        ]
        
        for pattern in goal_patterns:
            if re.search(pattern, user_input.lower()):
                return True
        return False
    
    def detect_mood(self, user_input):
        """Detect mood keywords in user input and return appropriate empathetic response."""
        user_lower = user_input.lower()
        
        # Check for explicit mood indicators first (I feel, I'm, etc.)
        mood_indicators = ["i feel", "i'm feeling", "i am feeling", "feeling", "i am", "i'm"]
        has_mood_indicator = any(phrase in user_lower for phrase in mood_indicators)
        
        # Look for mood keywords in the input
        detected_mood = None
        for mood in self.mood_responses.keys():
            if mood != "default" and mood in user_lower:
                detected_mood = mood
                break
        
        # If we found a mood or have mood indicators, provide a response
        if detected_mood:
            # Log the mood in database
            self.add_mood(detected_mood, user_input)
            return self.mood_responses[detected_mood]
        elif has_mood_indicator:
            # User is expressing a mood but we don't have a specific response
            # Log it as "other" and use default response
            self.add_mood("other", user_input)
            return self.mood_responses["default"]
        
        # No mood detected
        return None
    
    def show_startup_goals(self):
        """Display stored goals when AURA starts."""
        goals = self.get_goals()
        
        if goals:
            print("\n🎯 Here are your current goals:")
            print("=" * 40)
            for i, (goal, date_added) in enumerate(goals, 1):
                # Format date nicely
                try:
                    date_obj = datetime.datetime.fromisoformat(date_added)
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = "Recently"
                
                print(f"{i}. {goal}")
                print(f"   📅 Added on {formatted_date}")
                print()
        else:
            print("\n📋 You don't have any goals yet. Tell me something you want to achieve!")
    
    def get_random_encouragement(self):
        """Return a random encouraging message."""
        encouragements = [
            "You're doing great! Keep going! 🌟",
            "Every small step counts towards your goals! 👣",
            "I believe in you and your abilities! 💪",
            "Progress, not perfection. You're on the right track! 🛤️",
            "Your dedication is inspiring! ✨",
            "Remember: you're stronger than your challenges! 🦾"
        ]
        return random.choice(encouragements)
    
    def run(self):
        """Main chat loop for AURA."""
        print("🤖 Welcome to AURA - Your Adaptive Understanding & Reflective Assistant!")
        print("💡 Tell me your goals (e.g., 'I want to learn Python') or share how you're feeling.")
        print("💬 Type 'quit' to exit, 'goals' to see your goals, or 'encourage' for motivation.\n")
        
        # Show existing goals on startup
        self.show_startup_goals()
        
        while True:
            try:
                user_input = input("\n💭 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'quit':
                    print("\n🤖 AURA: Goodbye! Remember, I'll be here to help you achieve your goals! 👋")
                    break
                elif user_input.lower() == 'goals':
                    self.show_startup_goals()
                    continue
                elif user_input.lower() == 'encourage':
                    print(f"\n🤖 AURA: {self.get_random_encouragement()}")
                    continue
                
                # Check if it's a goal
                if self.detect_goal(user_input):
                    response = self.add_goal(user_input)
                    print(f"\n🤖 AURA: {response}")
                
                # Check if it's a mood
                elif mood_response := self.detect_mood(user_input):
                    print(f"\n🤖 AURA: {mood_response}")
                
                # General conversation
                else:
                    responses = [
                        "I'm here to listen! Tell me more about what's on your mind. 🤔",
                        "That's interesting! How can I help you with that? 💭",
                        "I understand. Is there a goal you'd like to work towards? 🎯",
                        "Thanks for sharing! How are you feeling about things? 😊",
                        "I'm always here to help you stay motivated! What's next? 🚀"
                    ]
                    print(f"\n🤖 AURA: {random.choice(responses)}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 AURA: Goodbye! Take care and remember your goals! 👋")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("🤖 AURA: Let's keep going! What would you like to talk about?")

if __name__ == "__main__":
    # Create and run AURA
    aura = AURA()
    aura.run()
