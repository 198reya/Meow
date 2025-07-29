import pandas as pd

# Load existing question bank
try:
    questionbank = pd.read_csv("questionbank.csv")
except FileNotFoundError:
    print("⚠️ questionbank.csv not found - creating new one")
    questionbank = pd.DataFrame()

# Remove existing VARC questions (if any exist)
if not questionbank.empty:
    updated_bank = questionbank[questionbank["Section"] != "VARC"].copy()
else:
    updated_bank = pd.DataFrame()

# Load and prepare new VARC data
varc = pd.read_csv("varc_master.csv")

# Transform VARC data to match question bank format
varc["Section"] = "VARC"
varc["Context"] = varc["passage"]
varc["QuestionText"] = varc["question"]

# Handle options - check if they're already split or need splitting
if "options" in varc.columns:
    opts = varc["options"].str.split("|", expand=True)
    varc["OptionA"] = opts[0].str.strip()
    varc["OptionB"] = opts[1].str.strip()
    varc["OptionC"] = opts[2].str.strip()
    varc["OptionD"] = opts[3].str.strip()
else:
    # If options already come as separate columns
    for opt_col in ["OptionA", "OptionB", "OptionC", "OptionD"]:
        if opt_col not in varc.columns:
            varc[opt_col] = ""

# Add missing ImageFiles column if it doesn't exist
if "ImageFiles" not in varc.columns:
    varc["ImageFiles"] = ""

# Select and rename columns
varc_final = varc[[
    "year", "slot", "Section", "Context", "QuestionText",
    "OptionA", "OptionB", "OptionC", "OptionD",
    "answer_type", "correct_answer", "ImageFiles"
]].rename(columns={
    "year": "Year",
    "slot": "Slot",
    "answer_type": "AnswerType",
    "correct_answer": "CorrectAnswer"
})

# Merge with existing data
final_bank = pd.concat([updated_bank, varc_final], ignore_index=True)

# Clean and standardize
final_bank = final_bank.fillna("")
for col in ["OptionA", "OptionB", "OptionC", "OptionD", "CorrectAnswer"]:
    final_bank[col] = final_bank[col].astype(str).str.strip()

# Save updated question bank
final_bank.to_csv("questionbank_updated.csv", index=False)

print("\n📊 Update Summary:")
print(f"Total questions in new bank: {len(final_bank)}")
if not questionbank.empty:
    print(f"→ Kept {len(updated_bank)} existing non-VARC questions")
print(f"→ Added {len(varc_final)} new VARC questions")

print("\n✅ Successfully created questionbank_updated.csv")