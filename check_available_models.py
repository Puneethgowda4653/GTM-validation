"""
Check Available Gemini Models
Run this script to see which models are available for your API key
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    api_key = input("Enter your Gemini API key: ").strip()

if not api_key:
    print("❌ API key is required. Exiting.")
    exit(1)

# Configure API
print("🔍 Checking available models...\n")
genai.configure(api_key=api_key)

try:
    # List all models
    print("=" * 80)
    print("AVAILABLE GEMINI MODELS")
    print("=" * 80)
    
    models_found = False
    generation_models = []
    
    for model in genai.list_models():
        models_found = True
        
        # Check if model supports content generation
        if 'generateContent' in model.supported_generation_methods:
            generation_models.append(model)
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Input Token Limit: {model.input_token_limit:,}")
            print(f"   Output Token Limit: {model.output_token_limit:,}")
            print(f"   Supported Methods: {', '.join(model.supported_generation_methods)}")
    
    if not models_found:
        print("\n❌ No models found. Check your API key.")
    else:
        print("\n" + "=" * 80)
        print("RECOMMENDED MODELS FOR GTM VALIDATION")
        print("=" * 80)
        
        # Recommend models
        recommended = []
        for model in generation_models:
            model_id = model.name.split('/')[-1]
            if 'pro' in model_id.lower() or 'flash' in model_id.lower():
                recommended.append(model_id)
        
        if recommended:
            print("\nAdd one of these to your .env file:\n")
            for model_name in recommended:
                print(f"   GEMINI_MODEL={model_name}")
        
        print("\n" + "=" * 80)
        print("COPY THIS TO YOUR .env FILE")
        print("=" * 80)
        if recommended:
            print(f"\nGEMINI_MODEL={recommended[0]}")
        print("\n✅ Done! Use the model name in your .env file")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("  - Invalid API key")
    print("  - No internet connection")
    print("  - API access not enabled")
    print("\nCheck your API key at: https://aistudio.google.com/app/apikey")