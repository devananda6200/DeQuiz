from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the AI model for quiz generation
print("Loading the quiz generator model...")

try:
    quiz_generator = pipeline('text-generation', model='gpt2')  # Replace with the actual model
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    quiz_generator = None  # Set to None to handle any loading failure gracefully

@app.route('/')
def home():
    print("Home route accessed.")
    return "Welcome to DeQuiz!"

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    if not quiz_generator:
        print("Model not loaded.")
        return jsonify({'error': 'Model is not loaded.'}), 500
    
    try:
        # Ensure the request is JSON
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON.'}), 415

        data = request.json
        domain = data.get('domain')
        interest = data.get('interest')
        
        print(f"Received data - Domain: {domain}, Interest: {interest}")
        
        # Ensure both domain and interest are provided
        if not domain or not interest:
            print("Domain or interest missing in request.")
            return jsonify({'error': 'Both domain and interest are required.'}), 400

        # Generate quiz
        print("Generating quiz...")
        prompt = f"Create a multiple-choice quiz with 5 questions about {domain} focusing on {interest}. Each question should have 4 options and indicate the correct answer."
        quiz = quiz_generator(prompt, max_length=250, num_return_sequences=1)
        print("Quiz generated successfully.")

        # Parse generated text into structured format
        questions = parse_quiz(quiz[0]['generated_text'])
        
        if not questions:  # Check if questions were generated
            return jsonify({'error': 'No questions generated. Please refine your request.'}), 400
        
        return jsonify({'questions': questions})
    
    except Exception as e:
        print(f"Error during quiz generation: {e}")
        return jsonify({'error': 'An error occurred during quiz generation.'}), 500

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        # Ensure the request is JSON
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON.'}), 415

        data = request.json
        answers = data.get('answers')

        if not answers:
            return jsonify({'error': 'No answers submitted.'}), 400

        # Correct answers placeholder (should match your quiz structure)
        correct_answers = {
            1: 'A',  # Example correct answers
            2: 'C',
            3: 'B',
            4: 'D',
            5: 'A'
        }

        incorrect_answers = []
        for i, user_answer in enumerate(answers, 1):
            correct_answer = correct_answers.get(i)
            if user_answer != correct_answer:
                incorrect_answers.append({
                    'question_num': i,
                    'your_answer': user_answer,
                    'correct_answer': correct_answer
                })

        summary = {
            'total_questions': len(correct_answers),
            'incorrect_answers': incorrect_answers,
            'correct_answers_count': len(correct_answers) - len(incorrect_answers)
        }

        return jsonify({'summary': summary})

    except Exception as e:
        print(f"Error during quiz submission: {e}")
        return jsonify({'error': 'An error occurred during quiz submission.'}), 500

def parse_quiz(quiz_text):
    """
    Parses the generated quiz text into a structured format.
    Assumes the format is: "Question? A) option1 B) option2 C) option3 D) option4 CorrectAnswer"
    """
    questions = []
    lines = quiz_text.strip().split('\n')  # Split into lines

    for line in lines:
        if line.strip():  # Skip empty lines
            # Split the question part to extract question and options
            question_and_options = line.split('CorrectAnswer')
            if len(question_and_options) < 2:
                continue  # Skip if not enough parts

            question_part = question_and_options[0].strip()
            correct_answer = question_and_options[1].strip() if len(question_and_options) > 1 else None

            options = question_part.split('?')[-1].strip().split(' ')
            options = [option.split(') ')[1] for option in options if ')' in option]

            if options and correct_answer:  # Ensure options and correct answer are present
                questions.append({
                    'question': question_part.split('?')[0].strip() + '?',
                    'options': options,
                    'correct_answer': correct_answer
                })

    return questions

if __name__ == '__main__':
    try:
        print("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
