# VEXlib


![License](https://img.shields.io/badge/license-MIT-green.svg) ![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-orange) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome to the VEXLib Framework!  
This project brings together simulation tools, a really cool code push and log sync tool, comprehensive unit & integration testing, log visualization,
and lots of utilities to make VEX V5 robot development easier and more fun.

---

## 📂 Project Structure

Here's a quick tour of what's included:

- **`src/`** — Core robot code: autonomous routines, drivetrain logic, odometry, and subsystem modules.
- **`sim/`** — Simulation tools for example a pathfinding algorithm and PID analysis tools.
- **`tests/`** — Unit tests to make sure everything works reliably.
- **`deploy/`** — The deployment script and its configurations, allowing the user to upload code to the robot using an SD card (More reliable than uploading large amounts of code over he USB protocol).
- **`util/`** — Handy utilities: friction testers, serial communication tests, and more.
- **`logs/`** — Recorded logs from drivetrain, and other robot subsystems, automatically synced from the robot by the "deploy" script every time you push code!
- **`assets/`** — An extra folder including anything you want (SVG Logos and a script to render them to pngs by default) on the robot to display or use, pushed to the robot with the code.
- **`docs/`** — Generated documentation files and help pages (You are currently viewing this).

---

## 🚀 Getting Started

<tabs group="IDE">
    <tab id="PYCHARM" title="Pycharm (Pro / Community)" group-key="PYCHARM">
        Getting started with VEXLib and Pycharm, I HIGHLY recommend PyCharm for this project, it integrates very nicely, from the preconfigured run configurations to the in-IDE graph display. (You can even get the professional version for <a href="https://www.jetbrains.com/shop/eform/students">free</a> if you are a student or a teacher)
        <img src="PyCharm Run Configurations.png" alt="PyCharm run configurations" height="400"/>
        <img src="Graph Visualization.png" alt="PyCharm Graph Visualization" height="400"/>
    </tab>
    <tab id="VSCODE" title="Visual studio code" group-key="VSCODE">
        Getting Started with VEXLib and Visual studio code, While I dislike VSCode, it is a very popular IDE, and I have included some basic instructions for getting started with it.
    </tab>
    <tab id="NONE" title="No IDE! give me the raw terminal" group-key="NONE">
        Getting started with VEXLib and no IDE
    </tab>
</tabs>


1. **Clone the repository:**
  ```sh
  git clone https://github.com/deekb/VEXLib
  cd VEXLib
  ```
2. **(Optional) Set up a virtual environment:**
  <tabs>
<tab id="CMD" title="Windows (CMD)">
<code-block lang="Batch">
  python -m venv venv
  .\venv\Scripts\activate.bat
</code-block>
</tab>
<tab id="PS" title="Windows (Powershell)">
<code-block lang="Batch">
  python -m venv venv
  .\venv\Scripts\activate.ps1
</code-block>
</tab>
<tab id="BASH" title="Linux / Mac (Bash)">
<code-block lang="SH">
  python -m venv venv
  source venv/bin/activate.sh
</code-block>
</tab>
<tab id="ZSH" title="Linux / Mac (Zsh)">
<code-block lang="SH">
  python -m venv venv
  source venv/bin/activate.zsh
</code-block>
</tab>
<tab id="Fish" title="Linux / Mac (Fish)">
<code-block lang="SH">
  python -m venv venv
  source venv/bin/activate.fish
</code-block>
</tab>
</tabs>

3. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Push the example code to the robot**
  ```shell
  python3 -m deploy
  ```
you should see something similar to this, this is the deployment script running, by default it will look for a removable storage medium with the string `VEX` in the name and push code to that, for configuration edit `/deploy/config.ini`:

```
⠏ Searching for SD card...
```
5.**Upload `src/userpy.py` to the vex brain**
Open the [VEX V5 code editor](https://codev5.vex.com/), create a new text project, and copy and upload the
<resource src="userpy.py"/> file to any slot the vex brain.
> The VEX V5 Code Editor will likely give you a message that it can not find and import the `main` module, this is expected, as the `main` module is on the SD card and not part of the standard vex library. This is a limitation of the VEX V5 Code Editor, and it will not affect the functionality of the code.
> {style="note"}



---

## Key Files

- `src/main.py` — Main entry point for running the robot code.
- `analyze_PID_test.py` — Analyze PID controller tests.
- `sim/DjikstraPathfindingTest.py` — Run Dijkstra's algorithm in a simulated map.
- `util/timeseries_analysis.py` — Analyze performance data from logs.

---

## Features

- Log recording and visualization
- Generic Odometry and drivetrain controller algorithm
- Rich documentation and testing suite

---

## Documentation

Offline help documentation can be found in the `docs/` folder — open `docs/index.html` for this page!

---

## Contributing

I'd love for you to contribute!  
Here are some great ways to help:

- Fix bugs
- Add / Improve simulations
- Expand the documentation
- Write tests

Feel free to open Issues or submit Pull Requests!

---

## TODOs / Future Improvements

- [x] Add `README.md`
- [x] Generate `requirements.txt`
- [x] Clean up stale code
- [ ] Full test coverage for /VEXLib
- [ ] Fully documented
- [ ] Polish documentation styling
- [ ] Usability testing and improvements

---


## Contact

Have questions? Ideas?  
Open an issue or email: **derek.m.baier@gmail.com**