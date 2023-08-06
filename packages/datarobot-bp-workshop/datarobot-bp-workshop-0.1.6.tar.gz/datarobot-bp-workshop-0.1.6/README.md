# blueprint-workshop
[Official Documentation](https://blueprint-workshop.datarobot.com)

Construct, modify, and execute blueprints from the comfort, flexibility, and power of Python.

![Simple Example](./.github/Blueprint-Workshop-Preview.png)

### Prerequisites
- Ensure your DataRobot account has enabled:
  - `GRAYBOX_DISABLED` (Show Uncensored Blueprints)
  - `ENABLE_CUSTOMIZABLE_BLUEPRINTS` (Enable Customizable Blueprints)

### Installation
1. `mkvirtualenv -p python3.7 blueprint-workshop`
2. `sudo apt-get install graphviz` or `brew install graphviz`
3. `pip install datarobot-bp-workshop`

(Recommended):
1. `pip install jupyterlab`
2. From a folder where you'd like to save your scripts: `jupyter-lab .`
