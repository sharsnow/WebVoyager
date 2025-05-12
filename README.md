# WebVoyager
## github網址  
https://github.com/sharsnow/WebVoyager/tree/muti-agent  

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

## 修改內容 

### main.py
將生成的RAG的內容加入至prompt，以便在進行生成指令及操作步驟會產生符合需求的結果。
`rag_results = search_rag(query=task['ques'], api_key=args.api_key,logger=task_logger)
    manual = generate_instruction_manual(api_key=args.api_key,
                                            task_goal=task['ques'], filtered_results=rag_results, logger=task_logger,
                                            instruction_format="text_steps")`
