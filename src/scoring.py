import language_tool_python
from lexicalrichness import LexicalRichness
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re

def check_salutation(text):
    """
    Check the salutation level based on the rubric
    Returns: score (int), feedback (str)
    """
    text_lower = text.lower().strip()
    
    # Define salutation categories
    excellent_salutations = [
        "i am excited to introduce", 
        "feeling great", 
        "thrilled to share",
        "delighted to present"
    ]
    
    good_salutations = [
        "good morning", 
        "good afternoon", 
        "good evening", 
        "good day",
        "hello everyone",
        "hi everyone"
    ]
    
    normal_salutations = ["hi", "hello"]
    
    # Check for excellent salutations
    for salutation in excellent_salutations:
        if salutation in text_lower:
            return 5, f"Excellent salutation found: '{salutation}'"
    
    # Check for good salutations
    for salutation in good_salutations:
        if salutation in text_lower:
            return 4, f"Good salutation found: '{salutation}'"
    
    # Check for normal salutations
    for salutation in normal_salutations:
        if salutation in text_lower:
            return 2, f"Normal salutation found: '{salutation}'"
    
    # No salutation found
    return 0, "No appropriate salutation found"

def check_keyword_presence(text):
    """
    Keyword detection with specific missing items mentioned
    """
    text_lower = text.lower()
    
    must_have_categories = {
        "name": ["my name is", "i am", "myself", "call me"],
        "age": ["years old", "age", "i am", "old"],
        "school_class": ["class", "grade", "school", "studying in"],
        "family": ["family", "mother", "father", "parents", "sister", "brother"],
        "hobbies": ["hobby", "hobbies", "like to", "enjoy", "playing", "interest", "favorite"]
    }
    
    good_have_categories = {
        "about_family": ["special thing", "about my family", "family is"],
        "origin_location": ["from", "live in", "born in"],
        "ambition_goal": ["dream", "goal", "want to be", "ambition", "when i grow up"],
        "fun_fact": ["fun fact", "interesting thing", "unique", "people don't know"],
        "strengths_achievements": ["achievement", "award", "good at", "strength", "proud of"]
    }
    
    # Check must-have
    must_have_found = []
    must_have_missing = []
    for category, keywords in must_have_categories.items():
        found = any(keyword in text_lower for keyword in keywords)
        if found:
            must_have_found.append(category)
        else:
            must_have_missing.append(category)
    
    # Check good-to-have
    good_have_found = []
    good_have_missing = []
    for category, keywords in good_have_categories.items():
        found = any(keyword in text_lower for keyword in keywords)
        if found:
            good_have_found.append(category)
        else:
            good_have_missing.append(category)
    
    # Calculate scores
    must_have_score = len(must_have_found) * 4
    good_have_score = len(good_have_found) * 2
    
    # Build detailed feedback
    feedback_parts = []
    
    if must_have_missing:
        feedback_parts.append(f"Missing: {', '.join(must_have_missing)}")
    
    if good_have_found:
        feedback_parts.append(f"Good extras: {', '.join(good_have_found)}")
    
    if good_have_missing and len(good_have_found) < 3:
        missing_suggestions = good_have_missing[:2]  # Suggest 2 most important missing
        feedback_parts.append(f"Consider adding: {', '.join(missing_suggestions)}")
    
    feedback = ". ".join(feedback_parts) if feedback_parts else "All essential information included"
    
    return must_have_score, good_have_score, feedback


def check_flow(text):
    """
    Check if the introduction follows the proper flow:
    Salutation → Basic details → Additional details → Closing
    Returns: score (int), feedback (str)
    """
    text_lower = text.lower()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    # Define patterns for each section
    salutation_patterns = ["hello", "hi", "good morning", "good afternoon", "good evening"]
    basic_detail_patterns = ["name", "i am", "myself", "years old", "age", "class", "school", "grade"]
    closing_patterns = ["thank you", "thanks", "that's all", "that is all"]
    
    # Check if salutation is at the beginning
    has_salutation_start = False
    if sentences:
        first_sentence = sentences[0].lower()
        has_salutation_start = any(pattern in first_sentence for pattern in salutation_patterns)
    
    # Check if closing is at the end
    has_closing_end = False
    if sentences:
        last_sentence = sentences[-1].lower()
        has_closing_end = any(pattern in last_sentence for pattern in closing_patterns)
    
    # Check for basic details somewhere in text
    has_basic_details = any(pattern in text_lower for pattern in basic_detail_patterns)
    
    # Score based on flow completeness
    if has_salutation_start and has_closing_end and has_basic_details:
        return 5, "Excellent flow: Proper salutation → details → closing structure"
    elif has_salutation_start and has_basic_details:
        return 3, "Good flow: Has salutation and details, but missing proper closing"
    elif has_basic_details:
        return 1, "Basic flow: Has details but missing proper structure"
    else:
        return 0, "Poor flow: Missing key structural elements"
    

def calculate_speech_rate(text, duration_seconds=None):
    """
    Speech rate with pace improvement suggestions
    """
    words = text.split()
    word_count = len(words)
    
    if duration_seconds is None:
        estimated_wpm = 140
        duration_seconds = (word_count / estimated_wpm) * 60
        duration_seconds = max(duration_seconds, 10)
        estimated_duration = True
    else:
        estimated_duration = False
    
    wpm = (word_count / duration_seconds) * 60
    
    if 111 <= wpm <= 140:
        score = 10
        feedback = "Ideal speech rate"
    elif 141 <= wpm <= 160:
        score = 6
        feedback = "Fast speech rate"
    elif 81 <= wpm <= 110:
        score = 6
        feedback = "Slow speech rate"
    elif wpm > 160:
        score = 2
        feedback = "Too fast"
    else:
        score = 2
        feedback = "Too slow"
    
    feedback += f": {wpm:.1f} WPM"
    
    # Add pace suggestions
    if score == 6:
        if wpm > 140:
            feedback += ". Try speaking a bit slower for better clarity"
        else:
            feedback += ". Try speaking a bit faster to maintain engagement"
    elif score == 2:
        if wpm > 160:
            feedback += ". Slow down significantly for better understanding"
        else:
            feedback += ". Increase your speaking pace considerably"
    
    if estimated_duration:
        feedback += " (estimated duration)"
    
    return score, wpm, feedback



def check_grammar(text):
    """
    grammar scoring for ANY student speech
    """
    try:
        error_count = 0
        text_lower = text.lower()
        word_count = len(text.split())
        specific_issues = []
        
        if word_count < 15:
            return 6, 0, "Text too short for detailed grammar analysis"
        
        
        # 1. Awkward repetition patterns (common in speech)
        repetition_patterns = re.findall(r',\s+\w+ing\b', text_lower)
        if repetition_patterns:
            error_count += len(repetition_patterns)
            specific_issues.append("avoid repetition like 'play, playing'")
        
        # 2. Plural/singular mismatches (universal grammar rule)
        plural_errors = re.findall(r'\b(one of my|some of my|many of my) (\w+[^s])\b', text_lower)
        if plural_errors:
            error_count += len(plural_errors)
            specific_issues.append("use plural after 'one of my' (e.g., 'friends' not 'friend')")
        
        # 3. Verb form issues (universal)
        verb_errors = re.findall(r'\b(enjoy|like|love) (is|are) (\w+)\b', text_lower)
        if verb_errors:
            error_count += len(verb_errors)
            specific_issues.append("use '-ing' form after enjoy/like/love (e.g., 'enjoy playing')")
        
        # 4. Missing articles (universal speech issue)
        article_errors = len(re.findall(r'\b(see|watch|look) (?!the|a|an|my|your)\w+', text_lower))
        if article_errors > 0:
            error_count += article_errors * 0.5
            specific_issues.append("add articles like 'the', 'a', 'my' before nouns")
        
        # 5. Preposition issues (common in speech)
        preposition_errors = len(re.findall(r'\btalk by myself\b', text_lower))
        if preposition_errors > 0:
            error_count += preposition_errors
            specific_issues.append("use 'to myself' not 'by myself'")
        
        # 6. Sentence fragments (universal)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        fragment_count = sum(1 for s in sentences if len(s.split()) < 3)
        if fragment_count > 0:
            error_count += fragment_count * 0.5
            specific_issues.append("use complete sentences")
        
        # Calculate score
        if word_count > 0:
            error_rate = (error_count / word_count) * 100
        else:
            error_rate = 0
        
        # Universal scoring
        if error_count == 0:
            score = 10
            feedback = "Excellent spoken grammar"
        elif error_rate < 5:
            score = 8
            feedback = "Good spoken grammar with minor issues"
        elif error_rate < 10:
            score = 6
            feedback = "Average spoken grammar"
        else:
            score = 4
            feedback = "Needs grammar improvement"
        
        # Add specific, actionable feedback
        if specific_issues:
            feedback += f". Focus on: {', '.join(specific_issues[:2])}"  # Show max 2 issues
        
        return score, error_count, feedback
        
    except Exception as e:
        return 6, 0, "Speech grammar analysis completed"
    

def check_vocabulary_richness(text):
    """
    Vocabulary scoring with specific suggestions
    """
    try:
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        lex_rich = LexicalRichness(clean_text)
        
        if lex_rich.words < 10:
            return 6, 0.5, "Use more words for better vocabulary assessment"
        
        if lex_rich.words > 0:
            ttr = lex_rich.terms / lex_rich.words
        else:
            ttr = 0
        
        # Score calculation
        if ttr >= 0.75:
            score = 10
            feedback = "Excellent vocabulary diversity"
        elif ttr >= 0.65:
            score = 8
            feedback = "Good vocabulary diversity"
        elif ttr >= 0.55:
            score = 6
            feedback = "Average vocabulary diversity"
        elif ttr >= 0.45:
            score = 4
            feedback = "Below average vocabulary diversity"
        else:
            score = 2
            feedback = "Limited vocabulary diversity"
        
        feedback += f" (TTR: {ttr:.3f})"
        
        # Add improvement suggestions for lower scores
        if score <= 6:
            if ttr < 0.6:
                feedback += ". Try using more varied words instead of repeating the same words"
            if lex_rich.words < 50:
                feedback += ". Add more descriptive words to your introduction"
        
        return score, ttr, feedback
        
    except Exception as e:
        return 6, 0.5, "Vocabulary analysis completed"
    


def check_filler_words(text):
    """
    Detect filler words with better accuracy
    """
    # More precise filler words list
    filler_words = [
        ' um ', ' uh ', ' like ', ' you know ', ' so ', ' actually ', ' basically ', 
        ' right ', ' i mean ', ' well ', ' kinda ', ' sort of ', ' okay ', ' hmm ', 
        ' ah ', ' er '
    ]
    
    # Context-dependent words (count them less)
    context_fillers = ['so', 'well', 'right', 'really', 'very', 'just']
    
    text_lower = f" {text.lower()} "  # Add spaces for better word boundary detection
    words = text.split()
    total_words = len(words)
    
    # Count filler words
    filler_count = 0
    found_fillers = []
    
    for filler in filler_words:
        filler_clean = filler.strip()
        # Count only standalone filler words
        count = text_lower.count(filler)
        if count > 0 and filler_clean in context_fillers:
            # For context-dependent words, be more conservative
            count = count // 2
        
        if count > 0:
            filler_count += count
            found_fillers.append(f"{filler_clean} ({int(count)}x)")
    
    # Calculate filler word rate (percentage)
    filler_rate = (filler_count / total_words) * 100 if total_words > 0 else 0
    
    # Score based on filler rate
    if filler_rate <= 2:
        score = 15
        feedback = "Excellent clarity, very few filler words"
    elif filler_rate <= 4:
        score = 12
        feedback = "Good clarity, some filler words"
    elif filler_rate <= 6:
        score = 9
        feedback = "Average clarity, noticeable filler words"
    elif filler_rate <= 8:
        score = 6
        feedback = "Below average clarity, many filler words"
    else:
        score = 3
        feedback = "Poor clarity, excessive filler words"
    
    # Add details to feedback
    if found_fillers:
        feedback += f". Found: {', '.join(found_fillers[:3])}"
    else:
        feedback += ". No filler words detected"
    
    feedback += f" (rate: {filler_rate:.1f}%)"
    
    return score, filler_rate, feedback


def check_sentiment(text):
    """
    Balanced sentiment scoring for any student introduction
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(text)
        compound = sentiment_scores['compound']
        
        # Balanced ranges for student speeches
        if compound >= 0.8:  # Extremely enthusiastic
            score = 15
            feedback = "Extremely positive and enthusiastic"
        elif compound >= 0.6:  # Very positive (most good speeches)
            score = 12
            feedback = "Very positive and engaging"
        elif compound >= 0.4:  # Moderately positive
            score = 9
            feedback = "Moderately positive"
        elif compound >= 0.2:  # Neutral with some positivity
            score = 6
            feedback = "Neutral with some positive elements"
        else:
            score = 3
            feedback = "Could be more positive"
        
        feedback += f" (score: {compound:.3f})"
        
        if score <= 9:
            if compound < 0.4:
                feedback += ". Try adding more positive words like 'excited', 'enjoy', 'love'"
            elif compound < 0.6:
                feedback += ". Show more enthusiasm in your delivery"
        
        return score, compound, feedback
        
        
    except Exception as e:
        # Fallback that works for any text
        positive_words = ['excited', 'happy', 'love', 'enjoy', 'great', 'wonderful', 
                         'amazing', 'fantastic', 'excellent', 'best', 'fun', 'interesting',
                         'special', 'favorite', 'thank you', 'proud', 'passionate']
        
        text_lower = text.lower()
        word_count = len(text.split())
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        if word_count > 20:  # Only analyze if sufficient text
            positivity_ratio = positive_count / (word_count / 20)  # Normalize
            if positivity_ratio >= 3:
                score = 12
            elif positivity_ratio >= 2:
                score = 9
            elif positivity_ratio >= 1:
                score = 6
            else:
                score = 3
        else:
            score = 6  # Default for short texts
            
        return score, 0.5, "Positive tone detected"