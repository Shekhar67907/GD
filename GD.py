import streamlit as st
import time
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load language model for NLP tasks
nlp = spacy.load('en_core_web_sm')
analyzer = SentimentIntensityAnalyzer()

# Helper function for generating AI bot response (stub function, replace with AI model later)
def generate_bot_response(personality, topic):
    return f"As a {personality}, my thoughts on {topic} are quite strong. We should consider all aspects."

# Time management: input for discussion duration
st.title("Group Discussion Simulator")
duration = st.number_input("Set Discussion Duration (in minutes):", min_value=1, max_value=60, value=10)
st.write("Discussion topic: Global Warming")  # You can replace this with user input or AI-generated topics

# AI participants (with personalities)
bots = [{'personality': 'Optimist'}, {'personality': 'Pessimist'}, {'personality': 'Realist'}]

# Countdown Timer
if st.button("Start Discussion"):
    st.write("Discussion has started!")
    countdown_time = int(duration * 60)

    # Timer Logic
    while countdown_time:
        mins, secs = divmod(countdown_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        st.write(f"Time Remaining: {timer}")
        time.sleep(1)
        countdown_time -= 1

    st.write("Time's up!")

    # Structured discussion flow
    st.write("### Discussion Flow")
    topic = "Global Warming"  # Example topic
    for i, bot in enumerate(bots):
        st.write(f"**Bot {i+1} ({bot['personality']}):**")
        bot_response = generate_bot_response(bot['personality'], topic)
        st.write(bot_response)
        time.sleep(2)  # Delay between bots' responses
    
    # User Turn
    user_intervention = st.text_input("Your Turn! Add your thoughts:")
    if user_intervention:
        st.write(f"**User:** {user_intervention}")
    
    # Fluency Assessment (using sentiment analysis as proxy for fluency)
    def analyze_fluency(user_response):
        score = analyzer.polarity_scores(user_response)
        filler_words = ['um', 'uh', 'like', 'you know']
        fillers_detected = [word for word in filler_words if word in user_response]
        return score, fillers_detected

    # Vocabulary Analysis (counting unique words)
    def assess_vocabulary(text):
        doc = nlp(text)
        words = set([token.text for token in doc if token.is_alpha])
        return len(words), words

    # If the user provided input, analyze fluency and vocabulary
    if user_intervention:
        fluency_score, fillers = analyze_fluency(user_intervention)
        word_count, words_used = assess_vocabulary(user_intervention)

        # Show evaluation results
        st.write("### Evaluation")
        st.write(f"Fluency Score: {fluency_score['compound']}")
        st.write(f"Filler Words Detected: {fillers}")
        st.write(f"Unique Words Used: {word_count}")
        st.write(f"Words: {words_used}")

        # Overall performance score (simple combination of fluency and vocabulary)
        overall_score = (fluency_score['compound'] * 50) + (word_count * 50 / 100)
        st.write(f"Overall Performance Score: {overall_score:.2f}/100")

        # Generate feedback report
        def generate_feedback_report(fluency_score, word_count, fillers):
            strengths = []
            improvements = []

            if fluency_score['compound'] > 0.5:
                strengths.append("Clear and coherent speech.")
            else:
                improvements.append("Work on delivering clearer sentences.")
            
            if len(fillers) > 0:
                improvements.append(f"Try to reduce filler words: {fillers}")
            else:
                strengths.append("Minimal use of filler words.")
            
            if word_count > 50:
                strengths.append("Great vocabulary usage.")
            else:
                improvements.append("Expand your vocabulary for more precise articulation.")
            
            return strengths, improvements

        # Display feedback
        strengths, improvements = generate_feedback_report(fluency_score, word_count, fillers)
        st.write("### Feedback Report")
        st.write("**Strengths:**")
        for strength in strengths:
            st.write(f"- {strength}")
        st.write("**Areas for Improvement:**")
        for improvement in improvements:
            st.write(f"- {improvement}")
