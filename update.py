import re

with open('d:/Study/Computer Networks/FinalCCNProject/README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Step 5
old_step_5 = '''### Step 5 - Inject Features into AnyLogic Model

`powershell
cd injection_scripts
python inject_multi_dashboard.py
python inject_rl_and_gan.py
cd ..
`

This automates the injection of four native Java Swing dashboards and reinforcement learning intelligent hooks into the AnyLogic XML file.'''
new_step_5 = '''### Step 5 - Inject Features into AnyLogic Model

To guarantee the model has all final improvements completely applied (including the new BiLSTM tweaks), run the entire injection sequence:

`powershell
cd injection_scripts
python inject_multi_dashboard.py
python inject_rl_and_gan.py
python inject_v2_upgrades.py
python inject_v3_fixes.py
python inject_v4_final.py
python inject_v5_safe_tweaks.py
python inject_v6_bilstm_tweak.py
cd ..
`

This automates the injection of four native Java Swing dashboards, reinforcement learning, and chronologically applies all model stability fixes directly into the AnyLogic XML file.'''
text = text.replace(old_step_5, new_step_5)

# Replace step 9 3)
text = re.sub(r'3\) cd injection_scripts && python inject_multi_dashboard.py && python inject_rl_and_gan.py', r'3) cd injection_scripts && python inject_multi_dashboard.py && python inject_rl_and_gan.py && python inject_v2_upgrades.py && python inject_v3_fixes.py && python inject_v4_final.py && python inject_v5_safe_tweaks.py && python inject_v6_bilstm_tweak.py', text)

with open('d:/Study/Computer Networks/FinalCCNProject/README.md', 'w', encoding='utf-8') as f:
    f.write(text)

with open('d:/Study/Computer Networks/FinalCCNProject/report/project_runbook.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

old_tex_block = '''\\begin{terminalBox}[(XML Mutation Engine)]
cd injection\\_scripts
python inject\\_multi\\_dashboard.py
python inject\\_rl\\_and\\_gan.py
cd ..
\\end{terminalBox}

\\textbf{What exactly did this do?}
\\begin{itemize}
    \\item \\texttt{inject\\_multi\\_dashboard.py}: Modified the AnyLogic startup sequence to automatically spawn four independent \\textbf{Java Swing windows} when the simulation starts (\\texttt{LatencyDash}, \\texttt{SecurityDash}, \\texttt{TelemetryDash}, and \\texttt{EnergyDash}). This proves visualization can be handled flawlessly inside the AnyLogic JVM.
    \\item \\texttt{inject\\_rl\\_and\\_gan.py}: Hooked the Tabular Q-Learning agent (\\texttt{QTableBalancer.java}) into the Gateway objects, allowing it to modify flow durations natively during simulation runtime.
\\end{itemize}'''

new_tex_block = '''To guarantee the model has all final improvements completely applied (including the new BiLSTM tweaks), you must run the entire injection sequence chronologically:

\\begin{terminalBox}[(XML Mutation Engine)]
cd injection\\_scripts
python inject\\_multi\\_dashboard.py
python inject\\_rl\\_and\\_gan.py
python inject\\_v2\\_upgrades.py
python inject\\_v3\\_fixes.py
python inject\\_v4\\_final.py
python inject\\_v5\\_safe\\_tweaks.py
python inject\\_v6\\_bilstm\\_tweak.py
cd ..
\\end{terminalBox}

\\textbf{What exactly did this do?}
\\begin{itemize}
    \\item \\texttt{inject\\_multi\\_dashboard.py}: Modified the AnyLogic startup sequence to automatically spawn four independent \\textbf{Java Swing windows} when the simulation starts.
    \\item \\texttt{inject\\_rl\\_and\\_gan.py}: Hooked the Tabular Q-Learning agent (\\texttt{QTableBalancer.java}) into the Gateway objects.
    \\item \\texttt{inject\\_v2}-\\texttt{v6}: Sequentially apply all the final model stability fixes up to the new BiLSTM tweak directly into the XML structure.
\\end{itemize}'''

tex = tex.replace(old_tex_block, new_tex_block)

with open('d:/Study/Computer Networks/FinalCCNProject/report/project_runbook.tex', 'w', encoding='utf-8') as f:
    f.write(tex)

