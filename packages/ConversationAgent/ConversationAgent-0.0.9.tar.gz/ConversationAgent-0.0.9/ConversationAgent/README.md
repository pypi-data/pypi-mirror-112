
## Using
### 購票系統範例 
```
bot_json = {
  "__MAIN_STAGES__": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』",
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
      },
      "is_fits": [
        [
          "(月票|1280|長期票|定期票)+",
          "set_level"
        ],
        [
          "(單程票|單程|一次)+",
          "set_level"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "set_level",
          "月票",
          "_月票_"
        ],
        [
          "set_level",
          "1280",
          "_月票_"
        ],
        [
          "set_level",
          "長期票",
          "_月票_"
        ],
        [
          "set_level",
          "定期票",
          "_月票_"
        ],
        [
          "set_level",
          "單程票",
          "_單程票_"
        ],
        [
          "set_level",
          "單程",
          "_單程票_"
        ],
        [
          "set_level",
          "一次",
          "_單程票_"
        ]
      ]
    }
  ],
  "_月票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
      },
      "is_fits": [
        [
          "(是|好的|好|沒問題)+$",
          "user_status"
        ],
        [
          "(否|不|不行|不要|不好)+$",
          "user_status"
        ]
      ]
    }
  ],
  "_單程票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "",
        "sys_reply_q2": "",
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
      },
      "is_fits": [],
      "__DISSABLE_Q1__": True
    }
  ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = ""
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "哪裡有廁所"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
```

### 購票+問答系統範例 
```
bot_json = {
  "__MAIN_STAGES__": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "哈囉請問要做什麼？ 目前提供『問答』和『訂票』服務",
        "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
        "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
      },
      "is_fits": [
        [
          "(問答|問題|詢問)+",
          "selected_service"
        ],
        [
          "(訂票|票價|買票)+",
          "selected_service"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "selected_service",
          "訂票",
          "_訂票_"
        ],
        [
          "selected_service",
          "買票",
          "_訂票_"
        ],
        [
          "selected_service",
          "票價",
          "_訂票_"
        ],
        [
          "selected_service",
          "問答",
          "_問答_"
        ],
        [
          "selected_service",
          "問題",
          "_問答_"
        ],
        [
          "selected_service",
          "詢問",
          "_問答_"
        ]
      ]
    }
  ],
  "_問答_": [
    {
      "stage_type": "__QA_STAGE__",
      "corpus": {
        "廁所在哪裡": "這裡沒有廁所",
        "詢問處在哪裡": "這裡沒有詢問處",
        "診所在哪裡": "這裡沒有診所",
      },
      "question": {
        "sys_reply_q1": "請問有什麼問題呢？",
        "sys_reply_q2": "",
        "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
      },
      "is_fits": []
    }
  ],
  "_訂票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』",
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
      },
      "is_fits": [
        [
          "(月票|1280|長期票|定期票)+",
          "set_level"
        ],
        [
          "(單程票|單程|一次)+",
          "set_level"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "set_level",
          "月票",
          "_月票_"
        ],
        [
          "set_level",
          "1280",
          "_月票_"
        ],
        [
          "set_level",
          "長期票",
          "_月票_"
        ],
        [
          "set_level",
          "定期票",
          "_月票_"
        ],
        [
          "set_level",
          "單程票",
          "_單程票_"
        ],
        [
          "set_level",
          "單程",
          "_單程票_"
        ],
        [
          "set_level",
          "一次",
          "_單程票_"
        ]
      ]
    }
  ],
  "_月票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
      },
      "is_fits": [
        [
          "(是|好的|好|沒問題)+$",
          "user_status"
        ],
        [
          "(否|不|不行|不要|不好)+$",
          "user_status"
        ]
      ]
    }
  ],
  "_單程票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "",
        "sys_reply_q2": "",
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
      },
      "is_fits": [],
      "__DISSABLE_Q1__": True
    }
  ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "我要月票"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "好"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
```
