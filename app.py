#!/usr/bin/env python3
"""
AURA Web Interface
A Flask web application for AURA (Adaptive Understanding & Reflective Assistant)

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

from flask import Flask, render_template, request, jsonify, session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import sqlite3
import datetime
import re
import random
import os
import atexit

# Import the AURA class from our existing module
from aura import AURA

app = Flask(__name__)
app.secret_key = 'aura-web-secret-key-2025'  # Required for sessions

# Initialize the background scheduler
scheduler = BackgroundScheduler()
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

class WebAURA(AURA):
    """
    Web version of AURA that adapts the terminal-based AURA for web interface.
    Inherits all functionality from AURA but modifies interactive methods.
    """
    
    def __init__(self):
        """Initialize WebAURA with all AURA functionality."""
        super().__init__()
        # Track if this is the user's first interaction
        self.first_interaction = True
    
    def process_message(self, user_input):
        """
        Process a user message and return AURA's response.
        This replaces the terminal-based run() method for web interface.
        """
        user_input = user_input.strip()
        
        if not user_input:
            return "I'm here to listen! What's on your mind? 🤔"
        
        # Handle special commands
        if user_input.lower() == 'goals':
            return self.get_goals_display()
        elif user_input.lower() == 'encourage':
            return self.get_random_encouragement()
        
        # Check if it's a goal
        if self.detect_goal(user_input):
            return self.add_goal(user_input)
        
        # Check if it's a mood
        mood_response = self.detect_mood(user_input)
        if mood_response:
            return mood_response
        
        # General conversation
        responses = [
            "I'm here to listen! Tell me more about what's on your mind. 🤔",
            "That's interesting! How can I help you with that? 💭",
            "I understand. Is there a goal you'd like to work towards? 🎯",
            "Thanks for sharing! How are you feeling about things? 😊",
            "I'm always here to help you stay motivated! What's next? 🚀"
        ]
        return random.choice(responses)
    
    def get_goals_display(self):
        """Get formatted goals display for web interface."""
        goals = self.get_goals()
        
        if goals:
            result = "🎯 Here are your current goals:\n\n"
            for i, (goal, date_added) in enumerate(goals, 1):
                try:
                    date_obj = datetime.datetime.fromisoformat(date_added)
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = "Recently"
                
                result += f"{i}. {goal}\n"
                result += f"   📅 Added on {formatted_date}\n\n"
            return result
        else:
            return "📋 You don't have any goals yet. Tell me something you want to achieve!"
    
    def get_initial_greeting(self):
        """Get the initial greeting with goals and pending reminders for new sessions."""
        greeting = "🤖 Welcome to AURA - Your Adaptive Understanding & Reflective Assistant!\n\n"
        
        # Check for pending reminders first
        reminders = self.get_unread_reminders()
        if reminders:
            greeting += "🔔 You have pending reminders:\n\n"
            for reminder_id, message, created_at, goal_text in reminders:
                try:
                    date_obj = datetime.datetime.fromisoformat(created_at)
                    formatted_time = date_obj.strftime("%I:%M %p")
                except:
                    formatted_time = "Recently"
                
                greeting += f"• {message}\n"
                greeting += f"  📅 {formatted_time}\n\n"
                
                # Mark reminder as read since we're showing it
                self.mark_reminder_read(reminder_id)
            
            greeting += "---\n\n"
        
        # Show goals if they exist
        goals = self.get_goals()
        if goals:
            greeting += "🎯 Welcome back! Here are your current goals:\n\n"
            for i, (goal, date_added) in enumerate(goals, 1):
                try:
                    date_obj = datetime.datetime.fromisoformat(date_added)
                    formatted_date = date_obj.strftime("%B %d, %Y")
                except:
                    formatted_date = "Recently"
                
                greeting += f"{i}. {goal}\n"
                greeting += f"   📅 Added on {formatted_date}\n\n"
            
            greeting += "💭 These goals are here to guide and motivate you today!\n\n"
        else:
            greeting += "📋 I don't see any goals yet. Tell me something you want to achieve!\n\n"
        
        greeting += "💡 You can:\n"
        greeting += "• Share your goals (e.g., 'I want to learn Python')\n"
        greeting += "• Tell me how you're feeling\n"
        greeting += "• Type 'goals' to see your goals\n"
        greeting += "• Type 'encourage' for motivation\n\n"
        greeting += "How are you feeling today? 🌟"
        
        return greeting

# Create a global WebAURA instance
web_aura = WebAURA()

# =============================================================================
# SCHEDULER FUNCTIONS FOR DAILY REMINDERS
# =============================================================================

def create_daily_reminder_job():
    """
    Scheduled job function that creates daily reminders.
    This runs in the background and generates reminder messages for users' goals.
    """
    try:
        print("🔔 Running daily reminder job...")
        
        # Create a reminder using the global AURA instance
        success = web_aura.create_daily_reminder()
        
        if success:
            print("✅ Daily reminder created successfully!")
        else:
            print("ℹ️  No goals found or reminder creation failed.")
            
    except Exception as e:
        print(f"❌ Error in daily reminder job: {e}")

# Schedule the daily reminder job
# For testing: runs every 2 minutes
# For production: change to every 24 hours using cron trigger
scheduler.add_job(
    func=create_daily_reminder_job,
    trigger=IntervalTrigger(minutes=2),  # Change to hours=24 for daily
    id='daily_reminder_job',
    name='Create daily goal reminders',
    replace_existing=True
)

print("📅 Daily reminder scheduler initialized (every 2 minutes for testing)")
print("💡 Change to hours=24 for production use")

@app.route('/')
def home():
    """Serve the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the web interface."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'response': "I'm here to listen! What's on your mind? 🤔"})
        
        # Check if this is the first message in the session
        if 'first_message' not in session:
            session['first_message'] = False
            # For first message, provide initial greeting but still process the message
            initial_greeting = web_aura.get_initial_greeting()
            user_response = web_aura.process_message(user_message)
            
            # Combine greeting and response
            full_response = f"{initial_greeting}\n\n---\n\nYou said: \"{user_message}\"\n\n{user_response}"
            return jsonify({'response': full_response})
        
        # Process the message normally
        response = web_aura.process_message(user_message)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': f"Sorry, something went wrong: {str(e)}"})

@app.route('/reset')
def reset_session():
    """Reset the chat session."""
    session.clear()
    return jsonify({'status': 'Session reset'})

@app.route('/check-reminders')
def check_reminders():
    """Check for new unread reminders and return them."""
    try:
        reminders = web_aura.get_unread_reminders()
        
        if reminders:
            # Format reminders for display
            reminder_messages = []
            for reminder_id, message, created_at, goal_text in reminders:
                try:
                    date_obj = datetime.datetime.fromisoformat(created_at)
                    formatted_time = date_obj.strftime("%I:%M %p")
                except:
                    formatted_time = "Recently"
                
                reminder_messages.append({
                    'id': reminder_id,
                    'message': message,
                    'time': formatted_time,
                    'goal': goal_text
                })
                
                # Mark as read since we're showing it
                web_aura.mark_reminder_read(reminder_id)
            
            return jsonify({
                'has_reminders': True,
                'reminders': reminder_messages
            })
        else:
            return jsonify({
                'has_reminders': False,
                'reminders': []
            })
            
    except Exception as e:
        return jsonify({
            'has_reminders': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌐 Starting AURA Web Interface...")
    print("🚀 AURA will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
