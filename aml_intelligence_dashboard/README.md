# AML Intelligence Dashboard — Team 9812BA55

Ready-to-deploy Streamlit dashboard for the AML alert-escalation hackathon.

## What is already included

- `app.py` — complete dashboard
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — dark fintech theme
- `data/dashboard_train.csv` — lightweight labeled dashboard data
- `data/dashboard_test.csv` — lightweight hidden-test predictions
- original competition artifacts used by the dashboard
- validated V2 model summary and feature importance

## Local run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown by Streamlit, usually `http://localhost:8501`.

## Deploy with Streamlit Community Cloud

1. Create a GitHub repository, for example `aml-intelligence-dashboard`.
2. Upload the **contents of this folder** to the repository root.
3. Make sure `app.py`, `requirements.txt`, `.streamlit/`, and `data/` are committed.
4. Go to Streamlit Community Cloud.
5. Create a new app from your GitHub repository.
6. Choose:
   - Repository: your new repo
   - Branch: `main`
   - Main file path: `app.py`
7. Deploy.
8. Open the public app URL and test every navigation page.
9. Submit that public URL to the hackathon.

## Final pre-submission checks

- App opens without login.
- Overview loads.
- Exploratory Analysis loads.
- Risk Explorer works for both Train and Hidden test.
- Model Intelligence shows V2 ROC-AUC = 0.624116.
- Methodology page loads.
- No raw transaction/customer records are exposed.
- Public URL works in an incognito/private browser window.

## Important

The train Risk Explorer uses the OOF artifact currently available in the project as a demonstration score.
The headline validated benchmark uses the stronger V2 score summary.
If a stronger Championship OOF file becomes available later, the dashboard can be upgraded, but this package is already deployable now.
