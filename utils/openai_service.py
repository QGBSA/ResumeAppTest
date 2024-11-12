from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def get_ats_score(resume_text, job_description_text):
    ats_prompt = load_prompt('prompts/ats_score_rule.txt')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You are an ATS score evaluator. Your task is to analyze the resume against the job description.\
             Provide a score from 1 to 10 based on how well the resume matches the job description,\
             along with detailed feedback on areas that need improvement. Always give your score on the first line and then \
             provide feedback in subsequent lines."},
            {"role": "user", 
             "content": f"Scoring Rules:\n{ats_prompt}\nResume:\n{resume_text}\n\nJob Description:\n{job_description_text}\n\nPlease provide an ATS score and feedback based on the evaluation rules. Returned score format is always 'ATS Score: X/Y', X is the score, Y is 10"}
        ],
        temperature=0.3,
    )
    score_feedback = response.choices[0].message.content
    score, feedback = parse_score_feedback(score_feedback)
    return score, feedback

def parse_score_feedback(score_feedback):
    # Split the input into lines
    parts = score_feedback.strip().splitlines()
    
    # Extract the score from the first line
    # Assuming the format is always "ATS Score: X/Y"
    score_str = parts[0].replace('ATS Score:', '').strip()  # Remove 'ATS Score:' and whitespace
    score = int(score_str.split('/')[0])  # Get the numerator part

    feedback = '\n'.join(parts[1:])  # Join the remaining parts for feedback
    
    return score, feedback


def fine_tune_resume(resume_text, job_description_text):
    optimization_prompt = load_prompt('prompts/resume_optimization_rule.txt')  # Load optimization rules
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You are a resume optimization assistant. Your task is to fine-tune the resume to make it ATS-friendly\
             based on the job description provided. Make necessary adjustments and provide an updated resume."},
            {"role": "user", 
             "content": f"Rules for fine-tuning:\n{optimization_prompt}\nResume:\n{resume_text}\n\nJob Description:\n{job_description_text}\n\nPlease fine-tune the resume."}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content

def generate_cover_letter(resume_text, job_description_text):
    cover_letter_prompt = load_prompt('prompts/cover_letter_rule.txt')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You are a cover letter generator. Your task is to create a personalized cover letter\
             Do not add in your own content. It should be based on the resume and job description provided only."},
            {"role": "user", 
             "content": f"Rules for writing cover letter:\n{cover_letter_prompt}\nResume:\n{resume_text}\n\nJob Description:\n{job_description_text}\n\nPlease generate a cover letter."}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content


def analyze_job_posting(job_description_text):
    analysis_prompt = load_prompt('prompts/job_analysis_rule.txt')  # Load analysis rules
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You are a job posting analysis assistant. Your task is to analyze the job description provided\
             and provide insights or suggestions for candidates."},
            {"role": "user", 
             "content": f"Analysis Rules:\n{analysis_prompt}\nJob Description:\n{job_description_text}\n\nPlease provide an analysis."}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content