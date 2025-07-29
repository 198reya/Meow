# Meow: CAT Practice App

A Streamlit web app for practicing previous year CAT questions conveniently.

## Features

- Topic-wise, full-test, and review tagged practice modes
- Bookmark and tag questions as "wrong" or "skipped"
- Shuffle questions for randomized practice
- Progress bar and session info
- Displays question metadata, context, options, and images

## Getting Started

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

### Installation

1. Clone or download this repository.
2. Place your `questionbank.csv` file in the project folder.
3. Add your question images to the `images` folder.

### Running the App

Open a terminal in the project directory and run:

```bash
streamlit run app.py
```

### CSV Format

Your `questionbank.csv` should include these columns:

- `Section`
- `QuestionText`
- `OptionA`, `OptionB`, `OptionC`, `OptionD`
- `AnswerType`
- `CorrectAnswer`
- `Context` (optional)
- `ImageFiles` (optional, e.g. `images/2022_slot1_scen2_1.jpg`)
- `Year`, `Slot` (optional)
- `tag` (optional, will be created if missing)

## Customization

- Change the color scheme in `app.py` (CSS section) for your own aesthetic.
- Add or modify questions and images as needed.

## Troubleshooting

- If images do not load, check the paths in `ImageFiles` and ensure files exist in the `images` folder.
- If you see a pandas dtype warning, make sure the `tag` column is present and set to string type.

