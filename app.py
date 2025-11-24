import streamlit as st
import sys
import os
import json

# Add the src folder to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scoring import (check_salutation, check_keyword_presence, check_flow, 
                    calculate_speech_rate, check_grammar, check_vocabulary_richness,
                    check_filler_words, check_sentiment)

# page config
st.set_page_config(page_title="Speech Grader", layout="wide")

def main():
    # Header
    st.title("🎓 Speech Grader ")
    st.write("Analyze student self-introductions and get detailed feedback")
    
    # Input section
    st.subheader("Enter Student's Self-Introduction")
    
    transcript_text = st.text_area(
        "Paste the transcript text below:",
        height=200,
        placeholder="Example: Hello everyone, my name is Akash. I am 14 years old and study in class 9...",
        help="Paste the student's self-introduction text here"
    )
    
    # Duration input
    col1, col2 = st.columns(2)
    with col1:
        duration_seconds = st.number_input(
            "Speech Duration (seconds):",
            min_value=1,
            max_value=600,
            value=60,
            help="Enter how long the speech took in seconds"
        )
    
    # Analyze button
    analyze_clicked = st.button("Analyze Speech", type="primary", use_container_width=True)
    
    if analyze_clicked:
        if transcript_text.strip():
            with st.spinner("Analyzing speech..."):
                try:
                    # Run all analyses
                    salutation_score, salutation_feedback = check_salutation(transcript_text)
                    must_score, good_score, keyword_feedback = check_keyword_presence(transcript_text)
                    flow_score, flow_feedback = check_flow(transcript_text)
                    speech_score, wpm, speech_feedback = calculate_speech_rate(transcript_text, duration_seconds)
                    grammar_score, error_count, grammar_feedback = check_grammar(transcript_text)
                    vocab_score, ttr, vocab_feedback = check_vocabulary_richness(transcript_text)
                    filler_score, filler_rate, filler_feedback = check_filler_words(transcript_text)
                    sentiment_score, positivity, sentiment_feedback = check_sentiment(transcript_text)
                    
                    # Calculate totals
                    content_score = salutation_score + must_score + good_score + flow_score
                    language_score = grammar_score + vocab_score
                    delivery_score = speech_score + filler_score + sentiment_score
                    total_score = content_score + language_score + delivery_score
                    
                    # Display results
                    st.subheader("📊 Analysis Results")
                    
                    # Overall score
                    st.metric("Overall Score", f"{total_score}/100")
                    
                    # Score breakdown in columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Content & Structure", f"{content_score}/40")
                    with col2:
                        st.metric("Language & Grammar", f"{language_score}/20")
                    with col3:
                        st.metric("Delivery & Style", f"{delivery_score}/40")
                    
                    # Detailed results with better formatting
                    st.subheader("Detailed Feedback")
                    
                    # Content & Structure
                    st.write("**🧩 Content & Structure**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**(1) Salutation:** {salutation_score}/5")
                        st.write(f"*{salutation_feedback}*")
                        st.write("---")

                        
                        st.write(f"**(2) Flow & Structure:** {flow_score}/5")
                        st.write(f"*{flow_feedback}*")
                        st.write("---")

                    with col2:
                        st.write(f"**(3) Good-to-have Keywords:** {good_score}/10")
                        st.write("---")

                        st.write(f"**(4) Must-have Keywords:** {must_score}/20")
                        st.write("---")
                    
                    if keyword_feedback and keyword_feedback != "All essential information included":
                        st.info(f"**Keywords Feedback:** {keyword_feedback}")
                    
                    st.write("---")
                    
                    # Delivery & Style
                    st.write("**🎯 Delivery & Style**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**(1) Speech Rate:** {speech_score}/10")
                        st.write(f"*{speech_feedback}*")
                        st.write("---")

                        st.write(f"**(2) Grammar:** {grammar_score}/10")
                        st.write(f"*{grammar_feedback}*")
                        st.write("---")

                        st.write(f"**(3) Vocabulary:** {vocab_score}/10")
                        st.write(f"*{vocab_feedback}*")

                    with col2:
                        st.write(f"**(4) Clarity (Filler Words):** {filler_score}/15")
                        st.write(f"*{filler_feedback}*")
                        st.write("---")

                        st.write(f"**(5) Engagement (Sentiment):** {sentiment_score}/15")
                        st.write(f"*{sentiment_feedback}*")
                    
                    
                    # Improvement suggestions
                    st.write("---")
                    st.write("**💡 Suggestions for Improvement**")
                    
                    suggestions = []
                    if salutation_score < 3:
                        suggestions.append("• Start with a proper greeting like 'Hello everyone' or 'Good morning'")
                    if must_score < 16:
                        suggestions.append("• Include all basic details: name, age, school, family, hobbies")
                    if good_score < 6:
                        suggestions.append("• Add personal touches like dreams, fun facts, or special family details")
                    if speech_score < 8:
                        suggestions.append("• Practice speaking at a steady pace (110-140 words per minute)")
                    if grammar_score < 8:
                        suggestions.append("• Review basic grammar rules for spoken English")
                    if vocab_score < 8:
                        suggestions.append("• Use more varied vocabulary in your speech")
                    if filler_score < 12:
                        suggestions.append("• Reduce filler words like 'um', 'uh', 'like' for clearer speech")
                    if sentiment_score < 12:
                        suggestions.append("• Show more enthusiasm and positivity in your delivery")
                    
                    if suggestions:
                        for suggestion in suggestions:
                            st.write(suggestion)
                    else:
                        st.success("🎉 Excellent performance! Keep up the good work!")

                    # JSON Output Section
                    st.write("---")
                    st.subheader("📄 JSON Output")
                    
                    # Create the JSON structure
                    output_data = {
                        "overall_score": total_score,
                        "word_count": len(transcript_text.split()),
                        "criteria": [
                            {
                                "criterion": "Content & Structure",
                                "score": content_score,
                                "max_score": 40,
                                "components": [
                                    {"name": "Salutation", "score": salutation_score, "max_score": 5, "feedback": salutation_feedback},
                                    {"name": "Must-have Keywords", "score": must_score, "max_score": 20, "feedback": keyword_feedback},
                                    {"name": "Good-to-have Keywords", "score": good_score, "max_score": 10, "feedback": keyword_feedback},
                                    {"name": "Flow", "score": flow_score, "max_score": 5, "feedback": flow_feedback}
                                ]
                            },
                            {
                                "criterion": "Delivery & Style", 
                                "score": delivery_score,
                                "max_score": 60,
                                "components": [
                                    {"name": "Speech Rate", "score": speech_score, "max_score": 10, "feedback": speech_feedback},
                                    {"name": "Grammar", "score": grammar_score, "max_score": 10, "feedback": grammar_feedback},
                                    {"name": "Vocabulary", "score": vocab_score, "max_score": 10, "feedback": vocab_feedback},
                                    {"name": "Filler Words", "score": filler_score, "max_score": 15, "feedback": filler_feedback},
                                    {"name": "Sentiment", "score": sentiment_score, "max_score": 15, "feedback": sentiment_feedback}
                                ]
                            }
                        ],
                        "improvement_suggestions": suggestions
                    }

                    # Display JSON in expandable section
                    with st.expander("View JSON Output", expanded=False):
                        st.json(output_data)

                    # Download button for JSON
                    json_str = json.dumps(output_data, indent=2)
                    st.download_button(
                        label="📥 Download JSON Results",
                        data=json_str,
                        file_name="speech_analysis_results.json",
                        mime="application/json",
                        use_container_width=True
                    )
                        
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                    st.info("Please check your input and try again.")
        
        else:
            st.error("Please enter some text to analyze.")


if __name__ == "__main__":
    main()