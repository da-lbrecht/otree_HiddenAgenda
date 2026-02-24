# Mitigating Manipulation in Committees: Experiment Codebase

This repository contains the oTree implementation of the **group estimation experiment** used in my research project:

**Albrecht, David. _Mitigating manipulation in committees: Just let them talk!_**  
Working paper (SSRN): https://ssrn.com/abstract=5994274

## Research context

Many high-stakes decisions are made by small groups (committees, boards, and teams). This project studies how group interaction format and strategic manipulation incentives affect:

- objective judgment accuracy,
- information sharing,
- and perceived trustworthiness.

The broader paper compares two interaction formats:

1. **Face-to-face (FTF)** interaction in video calls.
2. **Delphi-style** structured, pseudonymous interaction.

Both are tested with and without **hidden agendas** (private side-payment incentives for manipulation).

## What this repository implements

This repository implements the **first experimental part** (group estimation experiment):

- Groups of **4 participants**
- **10 payoff-relevant rounds** plus a trial round
- Probabilistic judgment task (ladybird random-walk target event)
- A **2x2 treatment design** (interaction format × hidden agenda incentives)

### Treatment apps in code

- `vc_ftf`: Face-to-face (video chat), no hidden agenda incentives
- `vc_ftf_hiddenagenda`: Face-to-face (video chat), with hidden agenda incentives
- `delphi_accountable`: Delphi-style structured interaction, no hidden agenda incentives
- `delphi_hiddenagenda_accountable`: Delphi-style structured interaction, with hidden agenda incentives

Additional app folders (`delphi`, `delphi_hiddenagenda`) are included as related/legacy variants.

## Experimental flow (implemented)

Across treatments, participants complete:

1. Welcome and instructions
2. Attention checks (with live validation and retry logic)
3. Trial round
4. 10 randomized estimation rounds
5. Post-experiment questionnaire (demographics, work experience, strategy, perceived reliability/satisfaction, honesty module)
6. Payoff screen

### Key design mechanics reflected in code

- **Round randomization**: task order is shuffled per participant (`round_displayed`).
- **Partial information structure**: each participant sees a different information slice of each random-walk instance.
- **Delphi condition**: first estimate + qualitative reasoning, pseudonymous review of all members’ inputs, second estimate, then aggregate group estimate.
- **FTF condition**: live video discussion and consensus entry.
- **Manipulation incentives**: in hidden-agenda treatments, specific group members receive additional private incentives tied to directional outcomes.
- **Payoffs**: group accuracy and hidden-agenda bonuses are calculated in-app using the implemented scoring logic and round-level outcomes.

## Technical implementation highlights

- Built with **oTree 5.4.1**.
- Uses **live pages / real-time messaging** for synchronization and interaction state.
- Captures rich process data (timing, round-level estimates, reasoning text, disagreement/timeouts, questionnaire responses, payoff components).
- Includes deployment scaffolding (`Procfile`) for `otree prodserver` worker/web processes.

## Local setup

### 1) Clone

```bash
git clone git@github.com:da-lbrecht/otree_HiddenAgenda.git
cd otree_HiddenAgenda
```

### 2) Python environment and dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3) Run locally

```bash
otree devserver
```

Then open: http://localhost:8000/

## Configuration notes

- Session configurations are defined in `settings.py`.
- Current active configs include the four treatment apps listed above.
- `OTREE_ADMIN_PASSWORD` should be set via environment variable for admin access.
- For production-style runs, use the process model shown in `Procfile`.

## Citation

If you use this codebase for academic work, please cite:

Albrecht, David. _Mitigating manipulation in committees: Just let them talk!_ Working paper. SSRN: https://ssrn.com/abstract=5994274

## License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. See `LICENSE`.
