import streamlit as st
import pandas as pd
import os

st.markdown("""
<style>
    .main > div { padding-top: 2rem; }
    .main-header {
        background: linear-gradient(135deg, #d1c4e9 0%, #9575cd 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #4b306a;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(76, 51, 106, 0.08);
    }
    .question-card {
        background: #f8f5ff;
        border: 1px solid #e1bee7;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(76, 51, 106, 0.07);
    }
    .stApp[data-theme="dark"] .question-card {
        background: #4b306a;
        border: 1px solid #9575cd;
        color: #f8f5ff;
    }
    .context-box {
        background: linear-gradient(135deg, #ede7f6 0%, #fffde7 100%);
        border-left: 4px solid #9575cd;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #4b306a;
    }
    .stApp[data-theme="dark"] .context-box {
        background: linear-gradient(135deg, #6a4b8a 0%, #9575cd 100%);
        color: #fffde7;
    }
    .question-text {
        background: linear-gradient(135deg, #f3e5f5 0%, #fffde7 100%);
        padding: 1.5rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 500;
        color: #4b306a;
        margin: 1rem 0;
        border-left: 5px solid #9575cd;
    }
    .stApp[data-theme="dark"] .question-text {
        background: linear-gradient(135deg, #6a4b8a 0%, #9575cd 100%);
        color: #fffde7;
    }
    .option-container {
        background: #f8f5ff;
        border: 2px solid #d1c4e9;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .option-container:hover {
        border-color: #9575cd;
        background: #ede7f6;
        transform: translateX(5px);
    }
    .stApp[data-theme="dark"] .option-container {
        background: #6a4b8a;
        border-color: #9575cd;
        color: #fffde7;
    }
    .stApp[data-theme="dark"] .option-container:hover {
        background: #9575cd;
        border-color: #d1c4e9;
    }
    .metadata-container {
        background: linear-gradient(135deg, #ede7f6 0%, #fffde7 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #4b306a;
    }
    .stApp[data-theme="dark"] .metadata-container {
        background: linear-gradient(135deg, #6a4b8a 0%, #9575cd 100%);
        color: #fffde7;
    }
    .stButton > button {
        background: linear-gradient(135deg, #9575cd 0%, #d1c4e9 100%);
        color: #fffde7;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(76, 51, 106, 0.10);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(76, 51, 106, 0.15);
        background: linear-gradient(135deg, #7e57c2 0%, #ede7f6 100%);
        color: #4b306a;
    }
    .success-message {
        background: linear-gradient(135deg, #ede7f6 0%, #d1c4e9 100%);
        color: #4b306a;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }
    .error-message {
        background: linear-gradient(135deg, #fffde7 0%, #f8bbd0 100%);
        color: #4b306a;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 600;
    }
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #9575cd 0%, #d1c4e9 100%);
    }
    .css-1d391kg {
        background: linear-gradient(180deg, #ede7f6 0%, #fffde7 100%);
    }
    .tag-wrong {
        background: #ba68c8;
        color: #fffde7;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .tag-skipped {
        background: #9575cd;
        color: #fffde7;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .tag-none {
        background: #d1c4e9;
        color: #4b306a;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .footer-info {
        background: linear-gradient(135deg, #ede7f6 0%, #fffde7 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 2rem;
        color: #4b306a;
        font-weight: 500;
    }
    .stApp[data-theme="dark"] .footer-info {
        background: linear-gradient(135deg, #6a4b8a 0%, #9575cd 100%);
        color: #fffde7;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Meow", layout="wide", initial_sidebar_state="expanded")

try:
    df = pd.read_csv("questionbank.csv")
    df.columns = df.columns.str.strip()
    required_columns = ["Section", "QuestionText", "OptionA", "OptionB", "OptionC", "OptionD", "AnswerType", "CorrectAnswer"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required columns in CSV: {missing_cols}")
        st.error(f"Available columns: {list(df.columns)}")
        st.stop()
    if "tag" not in df.columns:
        df["tag"] = ""
    df["tag"] = df["tag"].astype(str)
except FileNotFoundError:
    st.error("questionbank.csv file not found! Please upload the file.")
    st.stop()
except Exception as e:
    st.error(f"Error loading CSV: {str(e)}")
    st.stop()

st.markdown("""
<div class="main-header">
    <h1>Meow🐾</h1>
    <p>Previous year CAT questions at your finger-tips.</p>
</div>
""", unsafe_allow_html=True)

default_states = {
    "index": 0,
    "answers": {},
    "mode": "topic-wise",
    "section": "VARC",
    "save_needed": False
}

for key, default in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.sidebar.title("Meow")
st.sidebar.markdown("---")

mode = st.sidebar.radio("Practice Mode", ["topic-wise", "full-test", "review tagged"])
available_sections = sorted(df["Section"].unique())
section = st.sidebar.selectbox("Section", available_sections)

if st.session_state.mode != mode:
    st.session_state.index = 0
    st.session_state.mode = mode
    st.rerun()
if st.session_state.section != section:
    st.session_state.index = 0
    st.session_state.section = section
    st.rerun()

try:
    if mode == "topic-wise":
        filtered_df = df[df["Section"] == section]
        qdata = filtered_df.reset_index(drop=False)
    elif mode == "review tagged":
        filtered_df = df[df["tag"].isin(["wrong", "skipped"])]
        qdata = filtered_df.reset_index(drop=False)
    else:
        sample_size = min(30, len(df))
        filtered_df = df.sample(n=sample_size, random_state=42)
        qdata = filtered_df.reset_index(drop=False)
except Exception as e:
    st.error(f"Error filtering questions: {str(e)}")
    st.stop()

if "shuffled_qdata" in st.session_state:
    qdata = st.session_state["shuffled_qdata"]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current Mode:** {mode.title()}")
st.sidebar.markdown(f"**Questions Available:** {len(qdata)}")

if mode == "review tagged":
    wrong_count = len(df[df["tag"] == "wrong"])
    skipped_count = len(df[df["tag"] == "skipped"])
    st.sidebar.markdown(f"**Wrong:** {wrong_count}")
    st.sidebar.markdown(f"**Bookmarked:** {skipped_count}")

current_idx = st.session_state.index
if len(qdata) == 0:
    st.markdown("""
    <div class="question-card">
        <h2>No Questions Found</h2>
        <p>No questions match your current selection criteria.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
if current_idx >= len(qdata):
    st.markdown(f"""
    <div class="question-card">
        <h2>Session Complete!</h2>
        <p>You've completed all {len(qdata)} questions in this session.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Restart Session"):
        st.session_state.index = 0
        st.rerun()
    st.stop()

try:
    current_row = qdata.iloc[current_idx]
    original_df_index = current_row["index"]
except IndexError:
    st.error("Error accessing question data.")
    st.stop()

st.markdown(f"<h2>Question {current_idx + 1} of {len(qdata)}</h2>", unsafe_allow_html=True)
progress = (current_idx + 1) / len(qdata)
st.progress(progress)

st.markdown(f"""
<div class="metadata-container">
    <div style="display: flex; justify-content: space-around; text-align: center;">
        <div><strong> Year:</strong> {current_row.get('Year', 'N/A')}</div>
        <div><strong> Slot:</strong> {current_row.get('Slot', 'N/A')}</div>
        <div><strong> Section:</strong> {current_row.get('Section', 'N/A')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

context_text = current_row.get("Context", "")
if isinstance(context_text, str) and context_text.strip():
    st.markdown(f"""
    <div class="context-box">
        <strong> Context:</strong><br>
        {context_text}
    </div>
    """, unsafe_allow_html=True)

question_text = current_row.get("QuestionText", "")
if question_text:
    st.markdown(f"""
    <div class="question-text">
        <strong> Question:</strong><br>
        {question_text}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="question-text">
        <strong>Question:</strong><br>
        <em>(No question text available)</em>
    </div>
    """, unsafe_allow_html=True)

image_files = current_row.get("ImageFiles", "")
if isinstance(image_files, str) and image_files.strip():
    st.markdown("**Images:**")
    separators = [",", "|", ";"]
    images = [image_files]
    for separator in separators:
        if separator in image_files:
            images = [img.strip() for img in image_files.split(separator) if img.strip()]
            break
    if images:
        img_cols = st.columns(len(images))
        for i, img_file in enumerate(images):
            if img_file.startswith("images\\") or img_file.startswith("images/"):
                img_path = img_file
            else:
                img_path = os.path.join("images", img_file)
            if os.path.exists(img_path):
                try:
                    img_cols[i].image(img_path, use_container_width=True)
                except Exception as e:
                    img_cols[i].warning(f"Could not display image: {img_file}")
            else:
                img_cols[i].warning(f"Image file not found: {img_path}")

st.markdown("---")
answer_type = current_row.get("AnswerType", "").upper()
user_selection = None
options_list = []
option_keys = ['OptionA', 'OptionB', 'OptionC', 'OptionD']
for i, key in enumerate(option_keys):
    option_text = current_row.get(key, "")
    if isinstance(option_text, str) and option_text.strip():
        option_letter = chr(65 + i)
        options_list.append(f"{option_letter}) {option_text}")

if options_list:
    st.markdown("**Options:**")
    radio_key = f"mcq_{mode}_{current_idx}_{original_df_index}"
    user_selection = st.radio(
        "Choose your answer:",
        options_list,
        key=radio_key,
        index=None
    )
else:
    text_key = f"text_{mode}_{current_idx}_{original_df_index}"
    user_selection = st.text_input(
        "Enter your answer:",
        key=text_key,
        placeholder="Type your answer here..."
    )

def check_user_answer(user_ans, correct_ans, has_options=False):
    if not user_ans or not correct_ans:
        return False
    user_clean = str(user_ans).strip().upper()
    correct_clean = str(correct_ans).strip().upper()
    if has_options:
        if user_clean.startswith(('A)', 'B)', 'C)', 'D)')):
            user_letter = user_clean[0]
        elif len(user_clean) >= 1 and user_clean[0] in 'ABCD':
            user_letter = user_clean[0]
        else:
            return False
        if len(correct_clean) == 1 and correct_clean in 'ABCD':
            return user_letter == correct_clean
        elif correct_clean.startswith(('A)', 'B)', 'C)', 'D)')):
            return user_letter == correct_clean[0]
    return user_clean == correct_clean

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Check Answer", disabled=not user_selection):
        correct_answer = str(current_row.get("CorrectAnswer", "")).strip()
        has_options = len(options_list) > 0
        is_correct = check_user_answer(user_selection, correct_answer, has_options)
        if is_correct:
            st.markdown("""
            <div class="success-message">
                🎉 Correct Answer! Well done!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-message">
                Incorrect. The correct answer is: <strong>{correct_answer}</strong>
            </div>
            """, unsafe_allow_html=True)
            df.at[original_df_index, "tag"] = "wrong"
            st.session_state.save_needed = True

with col2:
    current_tag = df.at[original_df_index, "tag"]
    is_bookmarked = current_tag == "skipped"
    if st.button("Bookmark" if not is_bookmarked else "Unbookmark"):
        df.at[original_df_index, "tag"] = "" if is_bookmarked else "skipped"
        st.session_state.save_needed = True
        st.rerun()

with col3:
    current_tag = df.at[original_df_index, "tag"]
    if current_tag == "wrong":
        st.markdown('<span class="tag-wrong">🔴 Marked Wrong</span>', unsafe_allow_html=True)
    elif current_tag == "skipped":
        st.markdown('<span class="tag-skipped">🔖 Bookmarked</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="tag-none">⚪ No Tag</span>', unsafe_allow_html=True)

st.markdown("---")
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

with nav_col1:
    if st.button("⬅️ Previous", disabled=current_idx == 0):
        st.session_state.index = max(0, current_idx - 1)
        st.rerun()

with nav_col2:
    if len(qdata) > 1:
        jump_to = st.selectbox(
            "🔄 Jump to Q:",
            range(1, len(qdata) + 1),
            index=current_idx,
            key=f"jump_{mode}"
        )
        if jump_to - 1 != current_idx:
            st.session_state.index = jump_to - 1
            st.rerun()
        if st.button("🔀 Shuffle Questions"):
            shuffled_df = qdata.sample(frac=1, random_state=None).reset_index(drop=True)
            st.session_state.index = 0
            st.session_state["shuffled_qdata"] = shuffled_df
            st.rerun()

with nav_col3:
    if st.button("Next ➡️", disabled=current_idx >= len(qdata) - 1):
        st.session_state.index = min(len(qdata) - 1, current_idx + 1)
        st.rerun()

if st.session_state.save_needed:
    try:
        df.to_csv("questionbank.csv", index=False)
        st.session_state.save_needed = False
    except Exception as e:
        st.sidebar.error(f"Failed to save progress: {str(e)}")

st.markdown(f"""
<div class="footer-info">
    <strong>Session Info:</strong> {mode.title()} Mode | 
    Section: {section if mode == 'topic-wise' else 'Mixed'} | 
    Question {current_idx + 1}/{len(qdata)}
</div>
""", unsafe_allow_html=True)

if st.sidebar.checkbox("🔧 Show Debug Info"):
    st.sidebar.json({
        "Current Index": current_idx,
        "Original DF Index": original_df_index,
        "Mode": mode,
        "Section": section,
        "Total Questions": len(qdata),
        "Answer Type": answer_type,
        "Current Tag": df.at[original_df_index, "tag"],
        "Available Options": len(options_list)
    })