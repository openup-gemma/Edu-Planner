from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from intoGPT import create_study_advice_prompt, create_study_advice_prompt_with_search, search_related_information

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

class RequestStudyPlan(BaseModel):
    content: str  # 사용자의 공부 계획을 담을 필드

@app.post("/get-study-advice")
def get_study_advice(data: RequestStudyPlan):
    try:
        if not data.content:
            raise HTTPException(status_code=400, detail="Request content is empty")

        content = create_study_advice_prompt(data.content)
        response_data = {
            "status": 200,
            "data": content
        }
    except Exception as e:
        response_data = {
            "status": 500,
            "data": "An error occurred while processing the request."
        }
    return JSONResponse(content=response_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)