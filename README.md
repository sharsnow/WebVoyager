# WebVoyager
## github網址  
[https://github.com/sharsnow/WebVoyager/tree/RAG](https://github.com/sharsnow/WebVoyager/tree/RAG)
## AI agnet 操作

python .\main.py  --api_key "API_KEY" --api_model gpt-4o --max_iter 10

## 主題
**旅遊小助手**

1. 幫助旅客尋找合適的飯店
2. 尋找旅客適合的景點
3. 提供當地的天氣預報

## 更新後主要使用到的目錄

my_project/  
├── RAG/  
│   ├── __init__.py   
│   ├── chroma_db/  
│   ├── booking_screenshot.png  
│   ├── booking_screenshot2.png  
│   ├── travel_screenshot1.png  
│   ├── travel_screenshot2.png  
│   ├── weather_screenshot.png  
│   ├── visual_descriptions.md  
│   ├── instruction_manual_generator.py  
│   └── rag_processor.py  
├── main.py  
└── run.py   


---
## 新增內容 (RAG)
- 增加三種任務的不同畫面  
- 根據不同畫面提供agent操作畫面時，需要進行操作的輸入、點擊或是存取
- 將RAG生成後的資料放入chroma_db

添加RAG資料夾主要負責處理有關RAG相關的操作
- visual_descriptions.md  
    透過markdown將任務會使用到的操作流程及方式進行說明並附上畫面，以方便後續agent更了解如何進行操作
- chroma_db/
    RAG產生後的結果
- .png
    給visual_descriptions.md來了解畫面樣式說明
- instruction_manual_generator
    根據檢索結果生成清楚的行動步驟或答案
- rag_processor
    從知識庫中檢索visual_descriptions.md  
    處理資料的向量化、索引、相似度搜尋（RAG 流程）  
    把檢索到的相關資訊傳遞instruction_manual_generator  

提取並保存如下 Metadata 提高檢索精度至agent.log保存    
- 任務目標 (Task Goal)：   
    - 查詢 5 月 15 日高雄市的天氣。  
- 檢索結果 (Manual Retrieval Results)：  
    - 找到的內容來自 visual_descriptions.md，包括以下操作指引：  
- 操作步驟 (Steps):   
    1. 開啟網頁瀏覽器並前往提供台灣城市天氣資訊的網站。  
    2. 找到搜尋欄或地區選擇下拉選單。
    3. 選擇或輸入「高雄市」作為目標地點。
    4. 使用網站的行事曆功能選擇日期「5 月 15 日」。
    5. 點擊搜尋或提交按鈕，查詢高雄市 5 月 15 日的天氣。
    6. 查看結果，獲取該天的溫度、濕度、降雨機率以及任何天氣警示。
- 最終回答 (Answer):
    - 高雄市 5 月 15 日的天氣為: 白天氣溫 26-32°C，晚上氣溫 27-30°C。
---
## 修改內容 

### main.py
將生成的RAG的內容加入至prompt，以便在進行生成指令及操作步驟會產生符合需求的結果。
`rag_results = search_rag(query=task['ques'], api_key=args.api_key,logger=task_logger)
    manual = generate_instruction_manual(api_key=args.api_key,
                                            task_goal=task['ques'], filtered_results=rag_results, logger=task_logger,
                                            instruction_format="text_steps")`
