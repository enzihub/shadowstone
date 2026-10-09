def get_model():
    """Gemini model used for summaries. Needs GEMINI_API_KEY."""
    import google.generativeai as genai

    return genai.GenerativeModel("gemini-2.0-flash")
