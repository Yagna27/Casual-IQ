# 🧠 CausalIQ – No-Code Causal Inference Platform

CausalIQ is a drag-and-drop web app that empowers policymakers, researchers, and analysts to estimate causal impacts without writing code. Built using Streamlit, DoWhy, and Pyvis, it lets you visually define causal assumptions via DAGs and run causal effect estimations with ease.

## 🎯 Features

- 📁 Upload your own CSV dataset
- 🔄 Define variables and causal links interactively
- 🔗 Construct and visualize causal DAGs
- 🧪 Estimate treatment effects using DoWhy
- 📊 Intuitive UI — no coding needed

## 🧰 Tech Stack & Techniques

| Component              | Details                                                  |
|------------------------|----------------------------------------------------------|
| **Framework**          | Streamlit                                                |
| **Causal Inference**   | DoWhy (structural causal modeling, backdoor adjustment)  |
| **DAG Visualization**  | Pyvis + NetworkX                                         |
| **Estimation Method**  | Linear Regression (via backdoor criterion)               |
| **Optional Extension** | Plug in EconML for advanced ML-based causal estimators   |
