import json

with open("30_results/analysis_results.json") as f:
    results = json.load(f)

gap_mean = round(results["gap_mean"], 2)
rural_count = results["neg_rucc_counts"].get("rural", 0)
unemp = round(results["neg_means"]["unemployment_rate"], 2)
uninsured = round(results["neg_means"]["uninsured"], 2)

latex = f"""
\\documentclass[11pt]{{article}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{setspace}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{float}}

\\setstretch{{1.15}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{1em}}

\\begin{{document}}

\\begin{{center}}
\\textbf{{Mental Health Access and Underidentified Need in North Carolina}} \\\\
IDS 541 \\\\
Ra'Kira Nelson \\\\
\\today
\\end{{center}}

\\section*{{1.1 Stakeholders}}

This memo is written for policymakers and analysts at the North Carolina Department of Health and Human Services (NC DHHS). These stakeholders are responsible for allocating mental health resources, identifying underserved populations, and designing targeted interventions across counties. Because resource allocation decisions rely heavily on county-level indicators, the accuracy of these measures directly determines how effectively mental health needs are identified and addressed.

\\section*{{1.2 Executive Summary}}

Mental health policy frequently prioritizes areas with limited provider access under the assumption that these areas exhibit higher unmet need. However, these decisions are typically based on observed measures of distress, which may not fully reflect underlying conditions in environments where access to care is constrained.

This analysis evaluates whether counties with lower provider access exhibit observed distress levels that are lower than expected given their socioeconomic and environmental characteristics. A predictive model trained on high-access counties is used to estimate expected distress.

Across low-access counties, the average prediction gap is approximately \\textbf{{{gap_mean}}}, suggesting that observed distress generally aligns with expectations. However, this average masks important variation. A small number of counties—Cherokee, Brunswick, Clay, Graham, and Ashe—exhibit substantially negative prediction gaps, indicating that observed distress may underrepresent true need.

These findings suggest that current allocation strategies are broadly effective but may overlook specific counties where need is less visible. Targeted adjustments, rather than broad policy changes, are therefore warranted.

\\section*{{1.3 Decisions To Be Made}}

NC DHHS must determine whether its current approach to identifying high-need areas adequately captures variation in mental health burden across counties.

First, the agency must decide whether model-based estimates of expected distress should be incorporated alongside observed measures. This would allow policymakers to identify counties where need may be underrepresented.

Second, policymakers must determine whether targeted interventions should be directed toward counties identified as having large negative prediction gaps, rather than applying uniform policy adjustments across all low-access areas.

\\section*{{1.4 Background and Motivation}}

Mental health policy in the United States has increasingly focused on addressing provider shortages through programs such as Mental Health Professional Shortage Area (MHPSA) designations. These programs aim to direct funding and workforce incentives toward regions with insufficient provider availability.

While these initiatives have improved access, they rely heavily on observable indicators such as reported distress and service utilization. In low-access environments, these measures may underestimate true need due to limited screening, diagnosis, and treatment access.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.9\\linewidth]{{30_results/figures/fig1_provider_access_map.png}}
\\caption{{Mental health providers per 100,000 residents (left) and observed distress (right).}}
\\end{{figure}}

The mismatch between provider access and observed distress motivates this analysis.

\\section*{{1.5 Methodology}}

A linear regression model is used to estimate expected distress based on county-level characteristics including unemployment, insurance coverage, income, and environmental conditions.

The model is trained on high-access counties, where observed distress is more likely to reflect underlying conditions.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.7\\linewidth]{{30_results/figures/fig2_model_validation_high_access.png}}
\\caption{{Observed vs predicted distress in high-access counties.}}
\\end{{figure}}

The model is then applied to low-access counties. The prediction gap is defined as:

\\[
\\text{{Prediction Gap}} = \\text{{Observed}} - \\text{{Predicted}}
\\]

\\section*{{1.6 Results}}

Figure 3 presents the spatial distribution of prediction gaps across low-access counties.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.9\\linewidth]{{30_results/figures/fig3_prediction_gap_map.png}}
\\caption{{Prediction gap across counties.}}
\\end{{figure}}

Most counties exhibit values near zero, indicating alignment between observed and expected distress. However, several counties show large negative gaps, suggesting potential underidentification of need.

Figure 4 evaluates whether this discrepancy reflects a systematic issue.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.7\\linewidth]{{30_results/figures/fig4_prediction_gap_scatter.png}}
\\caption{{Prediction gap vs expected distress.}}
\\end{{figure}}

The absence of a clear trend indicates that discrepancies are not consistent across counties. This suggests that current methods of identifying need are not fundamentally flawed. Instead, the issue appears localized to specific counties rather than widespread across all low-access areas.

\\section*{{1.7 Implications for Policy}}

While most counties are appropriately characterized by observed distress, a subset deviates substantially. These counties represent the most important cases for policy intervention.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.8\\linewidth]{{30_results/figures/fig5_top_counties_gap.png}}
\\caption{{Counties with largest positive and negative prediction gaps.}}
\\end{{figure}}

As shown in Figure 5, Cherokee, Brunswick, Clay, Graham, and Ashe counties exhibit the largest negative prediction gaps. These counties should be prioritized for targeted intervention.

Among these counties, {rural_count} are rural. They also exhibit higher unemployment ({unemp}\\%) and higher uninsured rates ({uninsured}\\%), suggesting that structural barriers contribute both to underlying distress and to its underidentification.

Rather than implementing broad statewide changes, NC DHHS should focus on targeted strategies in these counties. These may include expanding screening programs, increasing outreach, and providing incentives to attract mental health providers.

Incorporating model-based indicators into decision-making would allow policymakers to identify these counties more systematically and allocate resources more effectively.

\\section*{{1.8 Conclusion}}

This analysis demonstrates that underestimation of mental health need is not widespread across all low-access counties, but instead concentrated in a small number of locations.

By identifying these counties, policymakers can move beyond broad assumptions about access and target interventions more precisely, improving both efficiency and effectiveness of mental health policy.

\\end{{document}}
"""

with open("40_docs/final_memo.tex", "w") as f:
    f.write(latex)
