import json

with open("30_results/analysis_results.json") as f:
    results = json.load(f)

gap_mean = round(results["gap_mean"], 2)
rural_count_neg = results["neg_rucc_counts"].get("rural", 0)
rural_count_pos = results["pos_rucc_counts"].get("rural", 0)
total_counties = results["neg_rucc_counts"].get("rural", 0) + results[
    "neg_rucc_counts"
].get("metro", 0)
uninsured = round(results["neg_means"]["uninsured"], 2)

latex = f"""
\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{setspace}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{float}}
\\usepackage{{subcaption}}

\\setstretch{{1.15}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{1em}}

\\begin{{document}}

\\begin{{center}}
\\textbf{{Mental Health Access and Underidentified Need in North Carolina Counties}} \\\\
IDS 541 \\\\
Ra'Kira Nelson \\\\
\\today
\\end{{center}}

\\section*{{1.1 Stakeholders}}

This memo is written for policymakers and analysts at the North Carolina Department of Health and Human Services (NC DHHS). These stakeholders are responsible for allocating mental health resources, identifying underserved populations, and designing targeted interventions across counties. Because resource allocation decisions rely heavily on county-level indicators, the accuracy of these measures directly determines how effectively mental health needs are identified and addressed.

\\section*{{1.2 Executive Summary}}

Mental health policy frequently prioritizes areas with limited provider access under the assumption that these areas exhibit higher unmet need. However, these decisions are typically based on observed measures of distress, such as providers per capita, which may not fully reflect underlying conditions in environments where access to care is constrained. In counties with limited access to mental health care, data used to measure mental health burden may under-represent true need, making these counties less visible in the data. This analysis evaluates whether counties with lower provider access exhibit observed distress levels that are lower than expected given their socioeconomic and environmental characteristics. 

A predictive model trained on counties with high access to mental healthcare providers, under the assumption that observed distress more closely reflects underlying need in these areas, is used to estimate expected distress. Across low-access counties, the average prediction gap is approximately \\textbf{{{gap_mean}}}, suggesting that observed distress is, on average, close to expected levels. However, this average obscures meaningful differences across counties.. A small number of counties, including Cherokee, Brunswick, Clay, Graham, and Ashe, exhibit substantially negative prediction gaps, indicating that observed distress may likely understates true underlying need.

These findings suggest that current allocation strategies are broadly effective but may overlook specific counties where need is less visible. Targeted adjustments, rather than broad policy changes, are therefore warranted.

\\section*{{1.3 Decisions To Be Made}}

NC DHHS must determine whether its current approach to identifying high-need areas adequately captures variation in mental health burden across counties. While many current strategies rely on observed distress, this analysis suggests that these measures may fail to identify some counties where underlying need is higher than it appears, creating a risk of misallocating resources. 

First, the agency must decide whether model-based estimates of expected distress should be incorporated alongside observed measures when identifying high-need areas. Incorporating these estimates would allow policymakers to systematically identify counties where observed distress understates likely need, improving the precision of resource allocation decisions. 

Second, policymakers must determine whether interventions should be targeted specifically toward counties with large negative prediction gaps, rather than applying uniform policy adjustments across all low-access areas. A targeted approach would prioritize counties where need is most likely under-identified, allowing NC DHHS to direct limited resources toward the areas where they are likely to have the greatest impact. 

\\section*{{1.4 Background and Motivation}}

Mental health policy in the United States has increasingly focused on addressing provider shortages through programs such as Mental Health Professional Shortage Area (MHPSA) designations. These programs aim to direct funding and workforce incentives toward regions with insufficient provider availability. As a result, resource allocation decisions are often based on observable indicators of need, such as reported distress and service utilization. 

However, these measures may not reflect underlying mental health burden equally well across counties. In low-access counties, observed distress may appear lower not because need is lower, but because of limitations in how distress is measured or reported. It could also be the case that low-access counties may have observed stress that appears higher than expected because of underlying socioeconomic and environmental differences, such as the urbanization of the area, median household income, or even access to exercise opportunities. As a result, observed measures may not consistently reflect underlying need, which can lead to some counties being overlooked while others may appear higher-need than they actually are. 

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.9\\linewidth]{{30_results/figures/fig1_provider_access_map.png}}
\\caption{{Mental health providers per 100,000 residents (left) and observed mental health distress (right) across North Carolina counties.}}
\\end{{figure}}

\\textbf{{Figure 1}} illustrates this mismatch by comparing provider access and observed distress across counties. While some low-access counties exhibit relatively low levels of observed distress, others show higher distress despite similar levels of access, indicating that observed measures do not consistently align with access-based expectations. This inconsistency motivates the need for a more systematic approach to identifying counties where need may be less visible in the data. 

This memo addresses the following question: Which counties in North Carolina may be overlooked if policymakers rely only on observed measures of mental health distress? More specifically, do counties with limited provider access exhibit levels of observed distress that are lower than expected given their socioeconomic and environmental characteristics? 

By identifying counties where observed distress appears lower than expected, this analysis aims to highlight places where mental health need may be less visible in the data, and where current allocation strategies may fail to fully capture underlying demand for services, with a focus on identifying counties that may require greater policy attention

\\section*{{1.5 Methodology}}

A county-level dataset for North Carolina was constructed by combining multiple public data sources, including CDC PLACES data, County Health Rankings, and USDA rural-urban classifications. These data were merged and cleaned to create a consistent set of county-level predictors capturing economic conditions, access to resources, and environmental factors. Specifically, these include unemployment rate, uninsured rate, access to exercise opportunities, social associations, air pollution, median household income (log-transformed), and rurality indicators. 

To evaluate how well observed distress reflects underlying need, counties were divided into high-access and low-access groups based on the median number of mental health providers per 100,000 residents. Counties above the median were classified as high-access, while those below were classified as low-access. 

A linear regression model was then used to estimate expected levels of mental health distress, the outcome variable. The model was trained exclusively on high-access counties, under the assumption that observed distress in these areas more closely reflects underlying need. The model predicts observed distress as a function of county-level characteristics, including unemployment, insurance coverage, income, as well as environmental conditions. Model performance was evaluated within the high-access sample using a train-test split to assess predictive accuracy and ensure that the model provides a reasonable approximation of observed distress in these counties. The final model was then estimated using the full high-access sample to generate the most stable predictions. 

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.7\\linewidth]{{30_results/figures/fig2_model_validation_high_access.png}}
\\caption{{Observed versus predicted mental health distress in high-access counties. Points are closely aligned along the 45-degree line, indicating that the model provides a reasonable fit and can approximate observed distress based on county-level characteristics.}}
\\end{{figure}}

In the analysis, this trained model was applied to low-access counties to generate predicted (expected) levels of distress. The difference between observed and predicted distress is defined as the prediction gap: 

\\[
\\text{{Prediction Gap}} = \\text{{Observed}} - \\text{{Predicted}}
\\]

Negative values of this gap indicate counties where observed distress is lower than expected, suggesting that need may be less visible in the data. Positive values indicate the opposite pattern. 

\\section*{{1.6 Results}}

Figure 3 presents the spatial distribution of prediction gaps across low-access counties and the relationship between expected distress and the prediction gap.

\\begin{{figure}}[H]
\\centering

\\begin{{subfigure}}{{0.57\\linewidth}}
    \\centering
    \\includegraphics[width=\\linewidth]{{30_results/figures/fig3_prediction_gap_map.png}}
    \\caption{{Prediction gap across counties}}
\\end{{subfigure}}
\\hfill
\\begin{{subfigure}}{{0.42\\linewidth}}
    \\centering
    \\includegraphics[width=\\linewidth]{{30_results/figures/fig4_prediction_gap_scatter.png}}
    \\caption{{Prediction gap vs expected distress}}
\\end{{subfigure}}

\\caption{{Prediction gaps across low-access counties. Panel (a) shows the spatial distribution of the gap, while Panel (b) shows the relationship between expected distress and the prediction gap.}}
\\end{{figure}}

\\textbf{{Figure 3(a)}} shows how prediction gaps vary across low-access counties. The distribution includes both positive and negative values, indicating that observed distress is sometimes higher and sometimes lower than expected. This suggests that observed measures do not consistently overstate or understate underlying need across these counties. However, several counties exhibit notably negative prediction gaps, indicating that observed distress is lower than expected in those locations. These counties represent cases where underlying need may be less visible in the data. 

\\textbf{{Figure 3(b)}} shows the relationship between expected distress and the prediction gap, with further shows no clear systematic relationship between the two variables, as counties with both high and low expected distress exhibit a range of positive and negative gaps. This indicates that discrepancies between observed and expected distress are not driven by the overall level of expected distress but instead vary across counties in a less predictable way. 

Taken together, these results suggest that, across low-access counties, observed distress is not systematically biased in one direction relative to expected levels. This contrasts with the initial expectation that low-access counties would consistently exhibit lower-than-expected distress. Instead, the results indicate a more balanced pattern, where observed measures sometimes align with, exceed, or fall below expected values. 

Despite this overall pattern, a subset of counties exhibits substantially negative prediction gaps. These counties are of particular importance, as they represent locations where observed distress may understate underlying need and where current allocation strategies may fail to fully capture mental health burden

\\section*{{1.8 Conclusion}}

While most counties are appropriately characterized by observed distress, a subset deviates substantially. These counties represent the most important cases for policy intervention.

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.8\\linewidth]{{30_results/figures/fig5_top_counties_gap.png}}
\\caption{{Counties with the largest positive and negative prediction gaps. Counties with large negative gaps represent locations where observed distress is substantially lower than expected, while counties with gaps indicate areas where observed distress exceeds model-based expectations.}}
\\end{{figure}}

As shown in \\textbf{{Figure 4}}, Cherokee, Brunswick, Clay, Graham, and Ashe counties exhibit the largest negative prediction gaps and should be prioritized for targeted intervention. Notably, {rural_count_neg} of these {total_counties} counties are classified as rural. In contrast, among the {total_counties} counties with the largest positive prediction gaps, only {rural_count_pos} are rural, with the remainder split between metro and mid-sized counties. This pattern suggests that under-identified mental health needs may be more concentrated in rural, low-access areas. 

Rather than implementing broad statewide changes, NC DHHS should focus on targeted strategies in these counties. These may include expanding screening programs, increasing outreach, and improving access to mental health services. Incorporating model-based indicators into decision-making would allow policymakers to identify these counties more systematically and allocate resources more effectively. 

Overall, this analysis shows that differences between observed and expected distress are not widespread across all low-access counties, but instead concentrated in a small number of locations. By identifying these counties, policymakers can move beyond broad assumptions about access and direct resources toward areas where need is most likely to be under-identified, improving both the efficiency and effectiveness of mental health policy. 

\\clearpage

\\renewcommand{{\\thefigure}}{{A\\arabic{{figure}}}}
\\setcounter{{figure}}{{0}}

\\section*{{Appendix}}

\\subsection*{{Figure A1: Model Residual Diagnostics}}

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.75\\linewidth]{{30_results/figures/figA4_model_residuals.png}}
\\caption{{Residuals from the regression model trained on high-access counties using a 80-20 training/test split.}}
\\end{{figure}}

This figure provides additional validation of the modeling approach used in the analysis. The residuals are centered around zero with no clear systematic pattern, suggesting that the model provides a reasonable fit to the data and does not exhibit strong bias across the range of predicted values. This suggests that linear specification is appropriate for capturing the relationship between county characteristics and observed distress in high-access counties.

\\subsection*{{Figure A2: Prediction Gap by Rural-Urban Classification (RUCC)}}

\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.75\\linewidth]{{30_results/figures/figA3_gap_by_rucc_scatter.png}}
\\caption{{Prediction gap of low-access counties plotted against expected distress, with counties colored by Rural-Urban Classification (RUCC).}}
\\end{{figure}}

This figure provides additional context on how prediction gaps vary across counties by rural-urban classification. While prediction gaps appear across all county types, the most negative gaps are more concentrated among rural counties. In contrast, counties with positive prediction gaps are more evenly distributed across metro, mid-sized, and rural categories. 

This pattern suggests that cases where observed distress falls below expected levels are more likely to occur in rural, low-access areas. As a result, rural counties are disproportionately represented among those where underlying need may be less visible in the data, supporting the focus on targeted intervention in these areas.

\\end{{document}}
"""

with open("40_docs/final_memo.tex", "w") as f:
    f.write(latex)
