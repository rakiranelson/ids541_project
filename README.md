# Final project for IDS541

**Data Science Memo found here: [Final Memo](40_docs/final_memo.pdf)**

## Project Overview

This project examines whether observed mental health distress across North Carolina counties accurately reflects underlying need.

A predictive model is trained using high-access counties to estimate expected levels of distress based on socioeconomic and environmental factors. This model is then applied to low-access counties to identify gaps between observed and expected distress.

The results highlight a small number of counties where observed distress is substantially lower than expected, suggesting that need may be underestimated in these areas. These findings are used to inform targeted policy recommendations.

---

## How to Reproduce

All results, figures, and the memo can be reproduced by running the pipeline from the project root:

```bash
python 10_code/17_pipeline.py