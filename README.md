ClearCheck Technologies — Approval Pattern Analytics

Project Overview

This project analyzes technician approval behavior for ClearCheck Technologies, a remote diagnostics company where device scans must be reviewed and approved before remote updates or upgrades are authorized.

The goal was to understand how quickly technicians approve cases, whether approvals occur unusually fast, whether approvals are concentrated in large batches, how technician behavior compares with suggested review-time benchmarks, whether a payout policy change was associated with different approval patterns, and how these findings can be communicated through an interactive management dashboard.

The analysis was completed in Python and presented through a Streamlit dashboard.

Dataset

The project uses 15 source files containing approval records for three technicians:

Gary Arnold

Juan Mendez

Matt Shawn

Total records: 64,230

Approval duration was defined as the time between consecutive approvals for the same technician. To avoid treating unobserved months as working time, approval intervals were calculated within each technician's source file.

Main Questions

How long is the gap between consecutive approvals?

How many approvals occur within 2, 5, 10, 30, and 60 seconds?

Are approval-time distributions skewed?

How often do approvals occur within the same minute or same second?

Do technician averages fall below suggested 10-, 5-, 2-, or 1-minute review benchmarks?

Do fast approvals appear to be explained by batch reviewing?

Did behavior change after the payout rate changed from $50 to $17 per approval?

Which technician patterns deserve the most management attention?

Key Findings

Technician

Median Gap

Under 10 sec

Under 30 sec

Under 60 sec

Gary Arnold

4 sec

77.21%

86.58%

91.61%

Juan Mendez

29 sec

5.19%

50.52%

80.19%

Matt Shawn

6 sec

66.43%

80.43%

87.29%

Gary Arnold showed the strongest concentration of rapid approvals, followed by Matt Shawn.

Same-Minute Activity

Gary Arnold: 80.17%

Juan Mendez: 43.75%

Matt Shawn: 72.75%

The distributions were strongly right-skewed, meaning long inactive periods increased the mean while many approvals still occurred very quickly.

Statistical Testing

One-sample t-tests were conducted against suggested average review-time benchmarks of 10, 5, 2, and 1 minute.

Gary Arnold's mean approval interval was statistically below the 10-minute benchmark:

Mean: 8.91 minutes

t-statistic: -2.65

p-value: 0.0040

Matt Shawn's mean was below 10 minutes numerically, but the result was not statistically significant. Juan Mendez's mean was above 10 minutes.

Approval Block Analysis

A new approval block was defined whenever the gap between two consecutive approvals was 10 minutes or more.

Block-level metrics included:

approvals per block

block duration

average within-block gap

observed seconds available per case

approvals per minute

fast-block ratios

pre-block time-per-case estimates

Large and fast blocks were especially visible for Gary Arnold and Matt Shawn. The batch-review explanation could not be fully verified using approval timestamps alone.

Payout Policy Analysis

The payout rate changed from $50 per approval before June 2020 to $17 per approval after June 2020.

Only Gary Arnold had observations in both payout periods.

His mean approval interval changed from 9.92 minutes before to 8.48 minutes after. His under-10-second approval rate increased from 68.75% to 80.76%.

The Welch two-sample t-test produced p = 0.1109, so the difference was not statistically significant. The analysis therefore does not conclude that the payout change caused faster approvals.

Interactive Dashboard

The Streamlit dashboard includes:

technician filtering

approval date filtering

fast-approval analysis lenses

approval-duration histograms

technician comparisons

top approval days

approval block visualizations

hour, weekday, and monthly patterns

statistical test results

payout analysis

batch-claim analysis

Technology Stack

Python

pandas

NumPy

SciPy

Plotly

Streamlit

Google Colab

GitHub

Streamlit Community Cloud

Repository Structure

clearcheck-dashboard/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── data/
    ├── approval_data.csv
    ├── block_summary.csv
    ├── batch_claim_blocks.csv
    ├── one_sample_ttests.csv
    ├── payout_summary.csv
    └── payout_ttest_result.csv

Important Limitation

Approval timestamps show when approvals occurred, not the exact amount of time a technician actively reviewed each case.

Because rejected cases, review start times, review end times, and detailed quality outcomes were not available, the results should be interpreted as evidence of workflow patterns and process-control concerns rather than proof of negligence.

Management Takeaway

Gary Arnold shows the strongest concentration of rapid approvals and high-intensity approval blocks. Matt Shawn also shows substantial fast-approval behavior, while Juan Mendez appears less extreme at the 10-second threshold.

The recommended next step is targeted audit review combined with improved system logging that captures actual case-open, review-start, review-end, and approval events.

Author

Varun Parekh
M.S. Business Analytics
Mercer University
