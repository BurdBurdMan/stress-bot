from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
import random

# Centralized joke list to avoid duplication
JOKES = [
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "What do you call a fake noodle? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why don’t eggs tell jokes? They’d crack each other up!",
    "Why did the coffee file a police report? It got mugged!",
    "What do you call a snowman with a six-pack? An abdominal snowman!",
    "Why don’t oysters donate to charity? Because they’re shellfish!",
    "What do you call a dinosaur with an extensive vocabulary? A thesaurus!",
    "Why did the bicycle fall over? Because it was two-tired!"
]

class ActionTellJoke(Action):
    def name(self):
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Get slots
        disliked_jokes = tracker.get_slot("disliked_jokes") or []
        joke_count = tracker.get_slot("joke_count") or 0

        # Filter available jokes
        available_jokes = [j for i, j in enumerate(JOKES) if i not in disliked_jokes]
        
        if not available_jokes:
            dispatcher.utter_message("Whoa, I’m out of fresh jokes! You’ve heard ‘em all. How about a chill tip instead?")
            return [{"event": "slot", "name": "joke_count", "value": joke_count}]

        # Pick a joke
        joke = random.choice(available_jokes)
        joke_index = JOKES.index(joke)
        joke_count += 1

        # Add a welcome twist for the first joke
        if joke_count == 1:
            dispatcher.utter_message("Hey, welcome to the giggle zone! Here’s your first joke: " + joke)
        else:
            dispatcher.utter_message(joke)

        # Update slots
        return [
            {"event": "slot", "name": "last_joke_index", "value": joke_index},
            {"event": "slot", "name": "joke_count", "value": joke_count}
        ]

class ActionHandleDislike(Action):
    def name(self):
        return "action_handle_dislike"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Get slots
        last_joke_index = tracker.get_slot("last_joke_index")
        disliked_jokes = tracker.get_slot("disliked_jokes") or []
        joke_count = tracker.get_slot("joke_count") or 0

        # Mark the last joke as disliked
        if last_joke_index is not None and last_joke_index >= 0 and last_joke_index not in disliked_jokes:
            disliked_jokes.append(last_joke_index)

        # Filter available jokes
        available_jokes = [j for i, j in enumerate(JOKES) if i not in disliked_jokes]
        
        if available_jokes:
            new_joke = random.choice(available_jokes)
            new_joke_index = JOKES.index(new_joke)
            joke_count += 1
            dispatcher.utter_message(f"Got it, no repeats of that one! Here’s a fresh shot: {new_joke}")
            return [
                {"event": "slot", "name": "disliked_jokes", "value": disliked_jokes},
                {"event": "slot", "name": "last_joke_index", "value": new_joke_index},
                {"event": "slot", "name": "joke_count", "value": joke_count}
            ]
        else:
            dispatcher.utter_message("Yikes, I’m tapped out on new jokes! Want a tip to unwind?")
            return [
                {"event": "slot", "name": "disliked_jokes", "value": disliked_jokes},
                {"event": "slot", "name": "joke_count", "value": joke_count}
            ]

class ActionProvideTip(Action):
    def name(self):
        return "action_provide_tip"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        tips = [
            "Take a few deep breaths—it’s like a reset button for your brain!",
            "Step outside for a quick walk—fresh air’s your secret weapon.",
            "Crank up your favorite tune—music’s a instant vibe-lifter.",
            "Sip some water and stretch—small moves, big relief!"
        ]
        tip = random.choice(tips)
        dispatcher.utter_message(f"Here’s a little stress-buster: {tip}")
        return []

class ActionBreathingExercise(Action):
    def name(self):
        return "action_breathing_exercise"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        dispatcher.utter_message("Time to chill! Inhale deep for 4 seconds, hold it for 4, exhale slow for 4. Let’s do it—feel the calm yet?")
        return []