 MetaboSim: Modular Metabolic Simulation Toolkit

**MetaboSim** is an open-source pipeline to simulate, analyze, and visualize perturbations across human metabolic networks. Inspired by Recon3D and tailored for integration with omics data, MetaboSim bridges deep biology with accessible tech.

## 📦 Modules Overview

1. **input_loader/** – load gene lists, models, and drug-target data
2. **parser_engine/** – parse metabolic models into reaction graphs
3. **core_model/** – build stoichiometric matrices
4. **simulator/** – perform FBA, knockouts, and drug perturbations
5. **analyzer/** – flux variability and bottleneck analysis
6. **contextualizer/** – integrate expression or variant data
7. **output/** – export results to JSON/CSV/SBML
8. **visualizer/** – generate interactive plots

## 🚀 Quickstart
```bash
pip install -r requirements.txt
python app.py  # launches Streamlit UI
# or
python run_simulation.py --genes genes.txt --map recon3d.sbml --knockout TP53 --drug_targets drugs.csv --output_json results.json
```

## 👥 Audience
* Systems biologists
* Bioinformaticians
* Synthetic biology engineers
* Clinical researchers

## 📚 License
MIT License

## 📖 Citation
Kwatra B. (2025). MetaboSim: An Open Framework for Metabolic Network Simulation.
