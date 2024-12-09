# OpenAI_Political_Compass

This is a small replication of [PoliLean](https://github.com/BunsenFeng/PoliLean). 

`main.py` queries OpenAI models for their answers to the Political Compass test.

`testing.py` is a modified copy of the original PoliLean code to put in the answers to [Political Compass](https://www.politicalcompass.org/).

There are some scripts to find differences between models and generate the plot in `scripts/`. 

Next steps include:
- [x] Add more prompts
- [ ] Incorporate more LLMs (Claude, Gemini etc.)
- [ ] Test models on Wahl-O-Mat
- [ ] Further pretrain on different German news corpora (e.g. Bild, SZ, FAZ) and see how the models opinions change

Problems:
- `testing.py` only works if the model never answered anything else than the 4 standard answers
- 

![](outputs/2024-12-02-08-40-22/political_compass_plot.png)
