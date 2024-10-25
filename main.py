from ai21 import AI21Client
from ai21.models.chat import ChatMessage
import json

# AI21 API 클라이언트 초기화
api_key = "MlZ1l5ny8vkbkWvAzs3c1hYKNNAkN7YQ"  # 실제 API 키
client = AI21Client(api_key=api_key)


def chat_with_ai21():
    # 대화 기록을 저장할 리스트
    conversation_history = []

    print("챗봇에 질문을 입력하세요 (종료하려면 'exit' 입력):")
    while True:
        # 사용자 입력 받기 (한글 입력 지원)
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # 대화 기록에 사용자 메시지 추가
        conversation_history.append(
            ChatMessage(
                role="user",
                content=user_input
            )
        )

        # AI21 API 호출로 응답 생성
        try:
            response = client.chat.completions.create(
                model="jamba-instruct-preview",  # 사용 가능한 모델 이름
                messages=conversation_history,
                temperature=0.7,  # 다양성과 창의성을 높이기 위한 설정
                top_p=0.9,  # 높은 확률의 단어 선택을 위한 설정
                maxTokens=150  # 응답의 최대 토큰 수
            )

            # 전체 응답 JSON 출력 (디버깅용)
            response_json = response.to_json()
            print("Raw Response JSON:", response_json)

            # 응답에서 텍스트 추출
            if isinstance(response_json, str):
                # JSON 문자열을 파싱하여 딕셔너리로 변환
                response_json = json.loads(response_json)

            try:
                # 'choices' 키가 있는지 확인
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    # 'message' -> 'content' 구조로 응답 추출
                    ai_response = response_json['choices'][0]['message']['content'].strip()
                else:
                    ai_response = "유효한 응답을 받지 못했습니다."
            except KeyError as e:
                ai_response = f"KeyError: {e}"

            # 대화 기록에 AI 응답 추가
            conversation_history.append(
                ChatMessage(
                    role="assistant",
                    content=ai_response
                )
            )

            # AI의 응답 출력
            print(f"Bot: {ai_response}")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    chat_with_ai21()
