# 탈모 진단 챗봇 [자라나모]
> 카카오톡을 통해 손쉽게 자신의 탈모 진행 단계를 진단받을 수 있는 챗봇 서비스  

- 사용자는 챗봇을 통해 두피 이미지를 보내면, 자신의 탈모 단계를 확인할 수 있다.
- 추가로 설문(문진)을 완료하면 자신의 두피 상태에 맞는 제품을 추천받을 수 있다. 
- 탈모 관련 궁금증을 해결할 수 있는 QnA를 제공한다.  


## 프로젝트 개요  
- 개발 인원: 총 5명  
- 개발 기간: 2022.09 ~ 2022.12(3달)
- 개발 환경: jupyter notebook(AI model), Kakao openbuilder(Chatbot), flask(Server), mysql(DB) 
- 본인 역할: 문진 AI 모델 생성(50%), flask API 설계(70%)   

### 개발 배경
<img src = "https://user-images.githubusercontent.com/74487747/226972974-005091f9-e4d3-4a2d-8d93-98283465fd64.png" width="700" >

### 시스템 구상도
<img src = "https://user-images.githubusercontent.com/74487747/226972776-afa12ad7-13b3-4898-bd75-58860f973110.png" width="700" > 

### 시나리오
<img src = "https://user-images.githubusercontent.com/74487747/226973244-dc0515af-d605-40bd-b358-fcb02be28fb2.png" width="700" > 

### AI 모델 활용
<img src = "https://user-images.githubusercontent.com/74487747/226973534-511726ec-8f10-4959-8ff4-4e578b6c3fb4.png" width="700" >

## 시연
### 1. 두피 이미지로 탈모 단계 진단
- 사용자는 두피 이미지 전송을 통해 탈모 단계를 진단받을 수 있으며, 사용자는 분석 결과에 대한 피드백을 보낼 수 있다. 
<img src = "https://user-images.githubusercontent.com/74487747/227072390-43da253f-7408-465e-b39c-15598dbd4b2e.png" width="700" >

### 2. 10개 설문(문진)으로 제품 추천
- 탈모 단계를 진단 받은 사용자는 추가 설문을 완료하면 제품 추천을 받을 수 있다.
<img src = "https://user-images.githubusercontent.com/74487747/227073225-5f9c2c6f-8618-412a-8ae1-043b0892175c.png" width="500" >  
<img src = "https://user-images.githubusercontent.com/74487747/227073336-577d1f86-ca66-4d68-ae6d-79ffb54faa09.png" width="500" >  

### 3. Q&A
- Q&A를 통해 질문을 입력하고, 관련도가 높은 3개의 질문과 답변을 볼 수 있다.
<img src = "https://user-images.githubusercontent.com/74487747/227071414-cb439bd3-2df6-4915-8066-a9bf02448080.png" width="700" >  

<img src = "https://user-images.githubusercontent.com/74487747/227076971-972a76c9-1d9f-49c1-a445-60d6f21e9c8e.gif " width="700" >



