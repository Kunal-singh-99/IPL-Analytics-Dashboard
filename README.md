# 🏏 IPL Data Analysis (2008–2026)

**What do 1,243 IPL matches say about toss luck, chasing, home fortresses and the MI–CSK rivalry?**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kunal-ipl-analytics-dashboard.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c)
![Seaborn](https://img.shields.io/badge/Seaborn-4c72b0)

### 🔴 Live demo: **[Open the interactive app →](https://kunal-ipl-analytics-dashboard.streamlit.app/)**

<!-- Add a screenshot or a short GIF of the app here, e.g. ![App preview](assets/app-preview.gif) -->

---

## 📌 Overview

An end-to-end exploratory data analysis of every IPL match from 2008 to 2026:

**raw CSV → cleaning in Pandas → analysis and charts (Matplotlib, Seaborn) → interactive Streamlit app**

The project answers six questions about franchises, tosses, chasing, venues, home advantage and rivalries, and wraps two of the analyses in reusable functions so anyone can explore any city or any pair of teams. The live app also includes a match-winner predictor built with multiple linear regression. The findings were also shared as a 12-slide LinkedIn carousel (`IPL-Data-Analysis-Carousel.pdf`).

**Skills demonstrated:** data cleaning, EDA, data visualization, regression modeling, reusable function design, Streamlit deployment, communicating insights.

## ❓ Questions and answers

| # | Question | What the data says |
|---|----------|--------------------|
| 1 | Which franchises have dominated? | **Mumbai Indians (155 wins)** and **Chennai Super Kings (148)** lead, followed by Royal Challengers Bengaluru (143), Kolkata Knight Riders (140) and Punjab Kings (126). |
| 2 | Does winning the toss matter? | Barely. Toss winners won **628 of 1,243 matches (50.5%)**, or 51.6% of the 1,218 matches that produced a result. That is close to a coin flip. |
| 3 | Is chasing better than defending? | Yes, modestly. Chasing teams won **54.2%** of decisive matches versus **45.8%** for teams defending a total (660 vs 558 of 1,218). |
| 4 | Which venues favor batting? | **Narendra Modi Stadium** and **Brabourne Stadium** produce the highest first-innings totals (around 180 on average, minimum 20 matches). Sharjah, Sheikh Zayed and Dr DY Patil are the lowest (roughly 157–160). |
| 5 | Which teams dominate at home? | **CSK at Chepauk**: 55 wins from 84 matches in Chennai, nearly 7× the next best team there (Mumbai Indians, 8 wins). |
| 6 | How close is MI vs CSK? | A near-perfect split: **MI 21 – 20 CSK** across 41 decisive matches (51.2% vs 48.8%). |

**Two more findings from the notebook**

- **Toss strategy has flipped.** Captains chose to field first in 66.4% of all tosses. In most seasons up to 2013 only 35–55% did (2011 is the exception); since 2016 it has been 70% or more in every season except the 2020 UAE edition (55%).
- **Most Player of the Match awards:** AB de Villiers (25), then CH Gayle and V Kohli (22 each).

## 🖥️ The Streamlit app

The app turns the notebook into something anyone can explore without writing code:

- **Home-ground view:** pick a city and see which franchises have won the most matches there (`analyze_fortress`)
- **Head-to-head view:** pick any two franchises and see their record and win split (`analyze_rivalry`)
- **Headline charts:** franchise wins, toss impact, chase vs defend, venue scoring
- **Match-winner predictor:** a multiple linear regression model estimates the winner from the match inputs

<!-- TODO: edit this list so it matches the pages and sections in your app -->

You can also call the functions directly in the notebook:

```python
analyze_fortress('Chennai')
analyze_rivalry('Mumbai Indians', 'Chennai Super Kings')
```

## 🧹 Data cleaning

Everything below lives in `Data_Cleaning.ipynb` and produces `final_dataset.csv`.

| Issue in the raw data | How it was handled |
|-----------------------|--------------------|
| `date` stored as text (day-first) | Parsed to a datetime column |
| `match_number` missing for 74 matches (playoffs and finals) | Filled sequentially from the previous match number |
| `winner` missing for 25 matches | Labeled `Tie` (16) or `No Result` (9) from `result_type` |
| `player_of_match` missing for 9 matches (all no-results) | Filled with `N/A` |
| Franchises renamed over the years (19 team names) | Merged into 15 franchises: Delhi Daredevils → Delhi Capitals, Kings XI Punjab → Punjab Kings, Royal Challengers Bangalore → Royal Challengers Bengaluru, Rising Pune Supergiants → Rising Pune Supergiant |
| Same stadium under several names | Standardized, e.g. Feroz Shah Kotla → Arun Jaitley Stadium, Sardar Patel Stadium (Motera) → Narendra Modi Stadium; city suffixes such as ", Mumbai" removed |
| Inconsistent city spelling | Bangalore → Bengaluru |

## 📦 Data

- `IPL_Matches_Data_2008_2026.csv`: raw match-level data, 1,243 matches × 31 columns (teams, venue, toss, scores, result and margin, player of the match, officials, playing XIs)
- `final_dataset.csv`: the cleaned version used by the notebook and the app
- **Source:** _[add the link to the dataset you downloaded]_

## 🗂️ Repository structure

<!-- app.py and requirements.txt are assumed names: rename them to match your repo -->
```
IPL-Data-Analysis/
├── app.py                          # Streamlit app
├── requirements.txt
├── Data_Cleaning.ipynb             # raw data → cleaned dataset
├── Analysis.ipynb                  # EDA, charts and the reusable analysis functions
├── IPL_Matches_Data_2008_2026.csv  # raw data
├── final_dataset.csv               # cleaned data
├── IPL-Data-Analysis-Carousel.pdf  # 12-slide LinkedIn carousel
└── README.md
```

## ⚙️ Run it locally

```bash
git clone https://github.com/Kunal-singh-99/IPL-Data-Analysis.git
cd IPL-Data-Analysis
pip install -r requirements.txt     # streamlit, pandas, matplotlib, seaborn
streamlit run app.py
```

To explore the notebooks instead: `jupyter notebook Analysis.ipynb`.

## 📝 Methodology notes and limitations

- **Chase vs defend** uses the 1,218 matches that produced a result; the 16 ties and 9 no-results are excluded. The toss figure above is shown with both denominators (all 1,243 matches, and the 1,218 with a result).
- **"Home"** is approximated by the match city (for example Chennai for CSK). The fortress view counts raw wins, so it reflects how many matches a team hosted as well as how often it won them.
- **Venue averages** require at least 20 matches at the venue.
- **Franchises** are tracked under their current names. Defunct teams (Deccan Chargers, Kochi Tuskers Kerala, Pune Warriors, Gujarat Lions, Rising Pune Supergiant) stay separate.
- **Source coverage:** season counts follow the source file (for example 2024 has 71 matches against 74 scheduled), and matches at the Dubai and Sharjah venues have no city in the source (`Unknown`), so city-level views leave them out.
- **Small samples:** head-to-head records and venue averages can swing with a handful of matches. Read them as tendencies, not guarantees.

## 🛣️ Roadmap

- [ ] Compare the regression model with logistic regression (a natural fit for a win/lose outcome) and report test-set accuracy against a simple baseline
- [ ] Add significance tests (binomial test and confidence intervals) for the toss and chase results
- [ ] Home-vs-away win percentage for every franchise, not just total wins
- [ ] Fill the missing city for Dubai and Sharjah venues and merge the remaining stadium aliases
- [ ] Season filter in the app
- [ ] Simple win-probability model (toss decision, venue, batting first)

## 👤 Author

**Kunal Jadon**: BCA student and aspiring data analyst, Delhi, India
[LinkedIn](https://www.linkedin.com/in/kunal-jadon-a9796735b) · [GitHub](https://github.com/Kunal-singh-99) · [LeetCode](https://leetcode.com/u/kunal_singh_69/)
