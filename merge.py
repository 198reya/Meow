import pandas as pd

# ——— VARC ———
varc = pd.read_csv("varc_master.csv")
varc["Section"] = "VARC"
varc["Context"] = varc["passage"]
varc["QuestionText"] = varc["question"]
varc["OptionA"] = varc["option_A"]
varc["OptionB"] = varc["option_B"]
varc["OptionC"] = varc["option_C"]
varc["OptionD"] = varc["option_D"]
varc["AnswerType"] = "MCQ"
varc["ImageFiles"] = ""

varc_final = varc[[
    "year", "slot", "Section", "Context", "QuestionText",
    "OptionA", "OptionB", "OptionC", "OptionD",
    "AnswerType", "CorrectAnswer", "ImageFiles"
]].rename(columns={
    "year": "Year",
    "slot": "Slot",
    "CorrectAnswer": "CorrectAnswer"
})

# ——— QUANT ———
quant = pd.read_csv("quant_master.csv")
quant["Section"] = "Quant"
quant["Context"] = quant["Topic"]
quant["QuestionText"] = quant["Question"]
quant["ImageFiles"] = ""

opts = quant["Options"].str.split("|", expand=True)
quant["OptionA"] = opts[0].str.strip()
quant["OptionB"] = opts[1].str.strip()
quant["OptionC"] = opts[2].str.strip()
quant["OptionD"] = opts[3].str.strip()

quant_final = quant[[
    "Year", "Slot", "Section", "Context", "QuestionText",
    "OptionA", "OptionB", "OptionC", "OptionD",
    "AnswerType", "CorrectAnswer", "ImageFiles"
]]

# ——— DILR ———
dilr = pd.read_csv("dilr_master.csv")
dilr["Section"] = "DI-LR"
dilr["Context"] = dilr["ScenarioText"]
dilr["QuestionText"] = dilr["QuestionText"]

opts = dilr["Options"].str.split("|", expand=True)
dilr["OptionA"] = opts[0].str.strip()
dilr["OptionB"] = opts[1].str.strip()
dilr["OptionC"] = opts[2].str.strip()
dilr["OptionD"] = opts[3].str.strip()

dilr_final = dilr[[
    "Year", "Slot", "Section", "Context", "QuestionText",
    "OptionA", "OptionB", "OptionC", "OptionD",
    "AnswerType", "CorrectAnswer", "ImageFiles"
]]

# ——— MERGE ALL ———
merged = pd.concat([varc_final, quant_final, dilr_final], ignore_index=True)

# Clean up blanks
merged = merged.fillna("")
for col in ["OptionA", "OptionB", "OptionC", "OptionD", "CorrectAnswer"]:
    merged[col] = merged[col].astype(str).str.strip()

merged.to_csv("questionbank.csv", index=False)
print(f" Merged {len(merged)} questions into questionbank.csv")
