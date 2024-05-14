import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# openai-key 설정
OPENAI_KEY = os.getenv('OPENAI_KEY')
GPT_MODEL = "gpt-4-turbo"

def search_related_information(subject, content):
    # 예시 반환 값
    related_info = "이 과목에 관련된 기본 개념과 중요 포인트는 다음과 같습니다: [관련 정보]"
    return related_info

def post_gpt_with_search(system_content, user_content, model_name, subject, study_content):
    try:
        client = OpenAI(api_key=OPENAI_KEY)  # 클라이언트 인스턴스화
        
        # 과목별 학습 내용에 기반하여 관련 정보 검색
        related_info = search_related_information(subject, study_content)
        
        # 'messages' 인자 구성
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
            {"role": "system", "content": related_info}  # 검색된 정보를 추가
        ]
        # 새로운 인터페이스 사용
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,  # 여기에 'messages' 인자를 제공
            max_tokens=3000,
            temperature=0.5
        )
        answer = completion.choices[0].message.content.strip()
        print("gpt 답변: " + answer)
        return answer
    except Exception as e:
        print(e)
        return None
    
# 프롬프트 작성 
def post_gpt(system_content, user_content, model_name):
    try:
        client = OpenAI(api_key=OPENAI_KEY)  # 클라이언트 인스턴스화
        # 'messages' 인자 구성
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
        # 새로운 인터페이스 사용
        completion = client.chat.completions.create(  # 클래스 이름 변경
            model=model_name,
            messages=messages,  # 여기에 'messages' 인자를 제공
            max_tokens=3000,
            temperature=0.5
            # 'stop' 인자는 필요에 따라 설정
        )
        answer = completion.choices[0].message.content.strip()
        print("gpt 답변: " + answer)
        return answer
    except Exception as e:
        print(e)
        return None    

def create_study_advice_prompt(prompt):
    system_content = "You are an advanced AI designed to provide study advice and generate quizzes for revision based on the study schedule and topics provided."
    pre_prompt = "한국어로 답변해줘; 사용자가 공부 계획을 제시했을 때, 각 과목별로 학습 시간에 대한 조언을 해주고, 과목별로 복습 테스트를 제공해줘;\n\n"
    langchain_prompt = (
        "Study plan advice and quiz generation: The user has provided a study plan with specific subjects and time allocations. Provide advice on the study time for each subject and generate a quiz for revision."
    )
    answer = post_gpt(system_content, pre_prompt + langchain_prompt + prompt, GPT_MODEL)

    if answer is None or not isinstance(answer, str):
        raise ValueError("GPT API의 응답이 올바르지 않습니다.")
    
    return [answer]