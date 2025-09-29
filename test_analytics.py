import sys
sys.path.append('.')

from app import WebAURA

# Initialize WebAURA
web_aura = WebAURA()

print("=== Testing Mood Analytics ===")
try:
    mood_data = web_aura.get_mood_analytics()
    print("Mood Data:")
    print(f"Mood counts: {mood_data['mood_counts']}")
    print(f"Mood trends: {mood_data['mood_trends']}")
    print(f"Total entries: {mood_data['total_entries']}")
except Exception as e:
    print(f"Error in mood analytics: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Progress Analytics ===")
try:
    progress_data = web_aura.get_goal_progress_analytics()
    print("Progress Data:")
    print(f"Goal progress: {progress_data['goal_progress']}")
    print(f"Progress trends: {progress_data['progress_trends']}")
    print(f"Total progress entries: {progress_data['total_progress_entries']}")
except Exception as e:
    print(f"Error in progress analytics: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing /data endpoint ===")
try:
    import json
    from flask import Flask
    app = Flask(__name__)
    
    with app.app_context():
        # Mock request context
        mood_data = web_aura.get_mood_analytics()
        progress_data = web_aura.get_goal_progress_analytics()
        
        response_data = {
            'success': True,
            'mood_data': mood_data,
            'progress_data': progress_data
        }
        
        print("Full JSON response:")
        print(json.dumps(response_data, indent=2))
        
except Exception as e:
    print(f"Error creating response: {e}")
    import traceback
    traceback.print_exc()
