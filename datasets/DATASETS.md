Datasets

This project is built on a set of complementary datasets selected to balance scientific reliability with practical, user accessible inputs. All model training and experimentation were completed using Google Colab GPU resources. The full training workflow, preprocessing steps, and evaluation details can be found in the notebook titled MyHealthPal_AI.ipynb located in this directory.

1. Health Demographics Dataset (DEMO_J.xpt, CDC NHANES 2017 to 2018)

Source:
https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&CycleBeginYear=2017

Content:
Age, gender, race, education, income level, family size, and marital status

Sample Size:
Approximately nine thousand adults, representative of the United States population

Purpose:
This dataset offers a broad demographic foundation that reflects real world diversity. It allows the system to make predictions grounded in population patterns rather than narrow clinical samples.

2. Physical Measurements Dataset (BMX_J.xpt, CDC NHANES 2017 to 2018)

Source:
https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Examination&CycleBeginYear=2017

Content:
Height, weight, BMI, waist circumference, and other standardized physical measurements

Purpose:
These measurements align with information users can easily record at home. This makes the system practical while still anchored in clinically collected data.

3. Cardiovascular Disease Validation Dataset (framingham.csv)

Source:
https://www.kaggle.com/datasets/aasheesh200/framingham-heart-study-dataset

Content:
Long term cardiovascular outcomes and related risk factors

Purpose:
This dataset is used for validating heart disease predictions over time. The Framingham study is well known for its long duration and strong predictive value, making it suitable for testing the reliability of our models.

Risk Prediction Models

The system evaluates three major health domains: obesity, diabetes, and heart disease. Each model is adapted from methods used in prior research, with adjustments that allow users to provide only simple, accessible information while preserving meaningful predictive performance.

Obesity Risk Prediction

Reference Approach:
BMI analysis methods used in prior studies

Model:
Random Forest, chosen due to strong results reported in related research

Inputs:
Age, gender, height, weight, and activity level

Outputs:
Obesity risk score and BMI category classification

Diabetes Risk Prediction

Reference Approach:
Methodology described by Manwal and colleagues

Model:
Support Vector Machine, validated at an accuracy of 77.29 percent in the referenced study

Inputs:
Age, gender, BMI, family history, and activity level

Outputs:
Diabetes risk score with preventive guidance

Heart Disease Risk Prediction

Reference Approach:
Cardiovascular assessment framework outlined by Kumar and colleagues

Model:
Random Forest, validated at an accuracy of 98 percent

Inputs:
Age, gender, BMI, family history, and activity level

Outputs:
Cardiovascular risk score with recommended lifestyle actions

Preprocessing and Model Reliability

Several techniques were used to ensure that the models behave consistently and remain accurate across different subsets of the data.

Data Cleaning and Missing Value Handling

Dataset entries were reviewed for missing or incorrect values. Invalid entries were corrected when possible or removed if they could compromise accuracy.

Feature Scaling and Normalization

All continuous inputs were scaled so that no single numerical range would dominate the model simply due to magnitude differences.

Cross Validation

The data was repeatedly partitioned into training and testing groups to confirm that each model performs reliably across various samples rather than a single split.

Why These Datasets Improve Prediction Quality

By combining NHANES demographic and physical measurement data with long term cardiovascular outcomes from the Framingham Heart Study, the system gains several advantages:

Nationally Representative Data

NHANES reflects the entire United States population, which provides wider applicability than studies based on small clinical groups.

Long Term Validation

Framingham data tests heart disease predictions over an extended timeline, which is more informative than one time or short term health records.

User Friendly Inputs

The models use only six broadly accessible features while still maintaining reliable prediction quality.

Unified Assessment

All three risk assessments use the same input set. This creates a streamlined user experience and consistent interpretation.

Health Evaluation and Scoring Framework

The platform presents results in an integrated format so users can clearly understand their health profile.

Obesity Risk Evaluation

Based on BMI and activity level, with results translated into familiar classifications.

Diabetes Risk Evaluation

Generated using an SVM trained on broad population data, providing an accessible estimate of potential diabetes risk.

Heart Disease Evaluation

Based on a Random Forest model validated on long term cardiovascular outcomes.

Scoring Scale

Risk is displayed using a consistent scale from 0 to 100 for all three domains. Color based presentation is used for clarity:

• 0 to 25: Low risk, maintain current habits with minor improvements
• 26 to 50: Moderate risk, consider targeted lifestyle changes
• 51 to 75: High risk, medical consultation is advisable
• 76 to 100: Very high risk, immediate professional attention recommended
