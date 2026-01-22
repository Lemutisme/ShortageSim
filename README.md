# ShortageSim: Simulating Drug Shortages under Information Asymmetry

## 📋 Overview

ShortageSim is a comprehensive multi-agent simulation framework that models pharmaceutical supply chain dynamics during drug shortage events. By leveraging Large Language Models (LLMs) to power agent decision-making, the system captures realistic responses to regulatory signals and market conditions under information asymmetry.

This work is accepted by The 40th Annual AAAI Conference on Artificial Intelligence (AAAI-26).
**📄 Paper**: [arXiv:2509.01813](https://arxiv.org/abs/2509.01813)  

### 🎯 Research Motivation

Drug shortages regularly disrupt patient care and impose major costs on health systems worldwide. While the U.S. Food and Drug Administration (FDA) issues alerts about potential shortages, the effectiveness of these interventions remains poorly understood due to:

* **Information Asymmetry** : FDA cannot observe individual manufacturers' inventory levels or buyers' procurement plans. Different stakeholders have access to different information:
  - Manufacturers know their own capacity, but not others'
  - Buyers see aggregate supply but not individual manufacturer statuses
  - Regulators see aggregated metrics only
* **Strategic Behavior** : Alerts may trigger stockpiling, potentially exacerbating shortages
* **Complex Interactions** : Multiple stakeholders with conflicting objectives

ShortageSim addresses these challenges by simulating realistic agent behaviors under partial information and evaluating policy interventions through counterfactual analysis.

## 🚀 Key Features

* **🧠 LLM-Powered Agents** : Manufacturers, buyers, and FDA regulators with sophisticated decision-making under partial information* 
* **🤖 Multi-Provider LLM Support** : Supports GPT-4o, Gemini 2.5 Flash, Claude Sonnet 4.5, and DeepSeek V3.2 Exp
* **📊 Realistic Market Dynamics** : Supply disruptions, capacity investments, and demand allocation
* **🏛️ Policy Evaluation** : Test reactive vs proactive FDA intervention strategies
* **📈 Ground Truth Validation** : Calibrated against historical FDA shortage data
* **📝 Comprehensive Logging** : Detailed tracking of all decisions and market states
* **🔧 Modular Architecture** : Easily extensible for new agent types and behaviors

## 📦 Installation

### Setup

```bash
# Install dependencies
conda create -n ShortageSim python=3.12
conda activate ShortageSim
pip install -r requirements.txt

# Set up your API keys (we support OpenAI, Gemini, Claude, and DeepSeek)
# You can use one or multiple providers - the framework will use the configured provider
export OPENAI_API_KEY="your-openai-key-here"        # For Openai model, e.g., GPT-4o
export GEMINI_API_KEY="your-gemini-key-here"        # For Gemini model, e.g., Gemini 2.5 Flash
export ANTHROPIC_API_KEY="your-claude-key-here"     # For Anthropic model, e.g., Claude Sonnet 4.5
export DEEPSEEK_API_KEY="your-deepseek-key-here"    # For Deepseek model, e.g., DeepSeek V3.2 Exp

# Run setup test to verify installation
python src/test_setup.py # default test is OpenAI
python src/test_setup.py --providers openai anthropic gemini deepseek # test all providers
```

## 🎮 Usage

### 🔗 Test on Our Web Interface!

```
python web/shortagesim.py
```

![Web](figures/shortagesim_web.png)

### Running Experiments

```bash
# Single simulation with disruption
python src/main.py

# Ground truth validation experiments
python src/main.py gt_experiment_disc    # For discontinued cases
python src/main.py gt_experiment_nodisc  # For non-discontinued cases

# Comparative study across different market conditions
python src/main.py comparative

# Policy effectiveness test: compare reactive and proactive FDA policies
python src/main.py policy

# Use different LLM providers and models
# We support OpenAI (GPT-4o), Anthropic (Claude Sonnet 4.5), Google (Gemini 2.5 Flash), and DeepSeek (V3.2 Exp)
python src/main.py --provider anthropic --model claude-sonnet-4-5-20250929  # Claude Sonnet 4.5
python src/main.py --provider gemini --model gemini-2.5-flash               # Gemini 2.5 Flash
python src/main.py --provider deepseek --model deepseek-chat                # DeepSeek V3.2 Exp
python src/main.py --provider openai --model gpt-4o                         # GPT-4o (default)

## Input number of manufacturers
python src/main.py --n_manufacturers 4

## Customize number of LLM temperature
python src/main.py --llm_temperature 0.5

## Choose FDA policy type from reactive(default) or proactive
python src/main.py --fda_mode proactive

## Combined Custom Scenario (Manufacturers, Periods, and Disruption)
python src/main.py single --n_manufacturers 6 --n_periods 12 --disruption_probability 0.05

## Define Custom Market Share Distribution (Requires --n_manufacturers)
# Note: The list size for --market_share must match the value of --n_manufacturers.
python src/main.py single --n_manufacturers 3 --market_share 0.6,0.3,0.1
```

## 🏗️ System Architecture

![System Architecture](figures/system_overview.png "System Architecture")

### Core Components

1. **Environment Module** : Manages market dynamics, disruptions, and state transitions
2. **Agent System** : LLM-powered decision makers (manufacturers, buyers, FDA)
3. **Information Flow** : Controls inter-agent communication and enforces information asymmetry
4. **Simulation Controller** : Orchestrates execution and comprehensive logging

### Agent Decision Pipeline

Each agent follows a two-stage LLM pipeline:

```
Stage 1: Collector & Analyst
├── Input: Raw market context and signals
├── Process: Extract structured state via LLM
└── Output: JSON with analyzed market conditions

Stage 2: Decision Maker  
├── Input: Structured analysis from Stage 1
├── Process: Strategic decision-making via LLM
└── Output: Action + detailed reasoning
```

## 📊 Market Mechanics

### Disruption Modeling

* **Probability** : $\lambda = 0.05$ per manufacturer per period
* **Magnitude** : $\delta = 20\\%$ capacity reduction
* **Duration** : U{1, ...,n} periods
* **Recovery** : Gradual capacity restoration

### Supply-Demand Allocation

1. Initial allocation by market share: $D_t * market\\_share$ per manufacturer
2. Disrupted firms produce: $\min(capacity, allocation)$
3. Unfilled demand redistributed to healthy firms
4. Market shortage calculated as: $\max(0, D_t - total\\_supply)$

### Agent Objectives

| Agent                  | Role                  | Objective                             | Key Decisions                         |
| ---------------------- | --------------------- | ------------------------------------- | ------------------------------------- |
| **Manufacturer** | Pharmaceutical CEO    | Maximize profit while managing risk   | Capacity investment (0-30% expansion) |
| **Buyer**        | Healthcare consortium | Minimize costs (purchase + stockout)  | Order quantity adjustment             |
| **FDA**          | Regulatory agency     | Minimize shortage duration & severity | Issue public announcements            |

## 📈 Evaluation Metrics

### Primary Metrics

1. **Resolution-Lag Percentage (RLP)** : Measures how closely simulation resolves shortages compared to historical data. Positive values indicate simulation resolves later than ground truth, negative values indicate earlier resolution.

$$
RLP = \frac{t_{sim} - t_{GT}}{t_{GT}} \times 100\\%
$$

where $t_{sim}$ is the simulation resolution time and $t_{GT}$ is the ground truth resolution time.

2. **FDA Intervention Percentage (FIP)** : Fraction of periods with FDA announcements, measuring regulatory activity frequency.

### Baseline Comparison

ShortageSim is evaluated against a **zero-shot baseline** that directly predicts complete shortage trajectories using LLM without multi-agent simulation. The zero-shot baseline:
- Takes the same initial shortage scenario as input
- Uses a single LLM call to predict the entire trajectory (shortage percentage over time)
- Does not model agent interactions or information asymmetry
- Serves as a direct trajectory prediction baseline without simulation dynamics

In contrast, ShortageSim:
- Models realistic agent behaviors and strategic interactions
- Captures information asymmetry through agent-specific observations
- Simulates market dynamics period-by-period with agent decisions
- Enables counterfactual policy analysis

### Performance Results

ShortageSim demonstrates strong alignment with historical data, reducing resolution lag by up to **84%** compared to zero-shot baseline methods under GPT-4o for FDA-Disc cases. Results are consistent across different LLM providers.

| LLM Model | Method | Dataset  | RLP (%) (mean ± std) | FIP (%) (mean ± std) |
| -------- | --------- | --------- | ----------- | -------------------- |
| GPT-4o | ShortageSim | FDA-Disc |  **4.5 ± 3.4**          | 82.6 ± 3.0           |
| GPT-4o | Zero-shot | FDA-Disc |  -28.3 ± 0.2          | 92.9 ± 0.1  |
| Claude Sonnet 4.5 | ShortageSim | FDA-Disc |  -9.4 ± 1.4         | -69.1 ± 2.3        |
| Claude Sonnet 4.5 | Zero-shot | FDA-Disc |  -32.7 ± 0.5         | -75.9 ± 0.7        |

## 🔬 Experimental Framework

### Ground Truth Validation

The framework includes comprehensive validation against **51 historical FDA shortage trajectories** from 2023-2024 with detailed cause annotations, drawn from a larger dataset of **2,925 FDA-reported drug shortage events**:

```python
# Load ground truth data
df = pd.read_csv("data/GT_Disc.csv")

# Run validation experiments
results = await run_gt_experiments(
    df, 
    n_simulations=3,      # Multiple runs per case
    export_dir="gt_evaluation"
)
```

The validation demonstrates that ShortageSim captures realistic agent behaviors and market dynamics, with agents interpreting regulatory announcements, inferring hidden market states, and making strategic decisions under information asymmetry.

### Customizing Agent Behaviors

Modify agent prompts in `src/prompts.py`:

```python
def get_manufacturer_prompts():
    return {
        "system_template": """You are the CEO of a pharmaceutical company...""",
        "user_template": """Current market state: {market_context}...""",
        "expected_keys": ["investment_decision", "reasoning"]
    }
```

## 📊 Logging and Analysis

The framework includes comprehensive logging at multiple levels:

```python
simulation_logs/
└── session_20250102_143022/
    ├── simulation_log.json      # Complete event log
    ├── market_states.json       # Period-by-period states
    ├── agent_decisions.json     # All agent decisions
    └── summary_metrics.json     # Aggregate results
```

## 🎯 Key Contributions

* **Agent modeling under partial information**: Agents interpret regulatory announcements, infer hidden market states, and make strategic decisions instead of assuming full rationality or full transparency
* **Information asymmetry built in**: Different agents have access to different information, reflecting real-world constraints
* **Empirical alignment**: ShortageSim shows much closer alignment with actual historical trajectories, especially for disruption-driven cases, reducing resolution lag by up to **84%** compared to baseline methods
* **Counterfactual policy analysis**: The framework allows experimenting with different regulatory communication designs (e.g., proactive vs. reactive alerts), showing that early warnings can sometimes trigger stockpiling, which has trade-offs

## 🤝 Contributing

We welcome contributions! Areas of particular interest:

* [ ] Multi-drug market extensions
* [ ] International supply chain modeling
* [ ] Additional LLM backends
* [ ] Interactive visualization dashboard

## Citation

If you use ShortageSim in your research, please cite:

```bibtex
@misc{ShortageSim2025,
      title={ShortageSim: Simulating Drug Shortages under Information Asymmetry}, 
      author={Mingxuan Cui and Yilan Jiang and Duo Zhou and Cheng Qian and Yuji Zhang and Qiong Wang},
      year={2025},
      eprint={2509.01813},
      archivePrefix={arXiv},
      primaryClass={cs.MA},
      url={https://arxiv.org/abs/2509.01813}, 
}
```
