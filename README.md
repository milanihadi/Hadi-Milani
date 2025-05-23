# EFDS – Equal Friction Duct Sizing Tool for AutoCAD

**EFDS** is a lightweight AutoLISP tool that automates duct sizing directly in AutoCAD using the Equal Friction Method. It is designed for use in early design stages and educational contexts, especially for engineers working with VAV systems.

---

## 🚀 Key Features

- Runs inside AutoCAD (no Revit or external plug-ins)
- Supports **IP (in, fpm, in.wg)** and **SI (mm, m/s, Pa, L/s)** units
- Calculates:
  - Flow, diameter, velocity
  - Friction loss using **Darcy–Weisbach** and **Colebrook–White** equations
- Annotates lines and stores results as **XData**
- Exports data to `.CSV` via the `EX` command

---

## 📁 Files Included

- `EFDS.fas` – Compiled AutoLISP tool
- `Sample_Duct_Network.dwg` – Example drawing for testing
- `How_To_Use.txt` – Step-by-step usage guide
- `LICENSE` – CC BY-NC-ND 4.0 license

---

## 🔧 How to Use

1. Open AutoCAD  
2. Load `EFDS.fas` via `APPLOAD`
3. Type `EFDS` in the command line  
4. In the dialog, enter:
   - Unit system: IP or SI
   - Air density, duct roughness, friction rate
   - Text settings (font, color, layer, height)
5. Click OK
6. Select:
   - A **starting point** on a duct line
   - Then **select all duct lines** in the network
7. The tool will:
   - Trace the duct path
   - Read flow rate from diffuser blocks (with attribute `"FLOW RATE"`)
   - Calculate diameter, velocity, and pressure drop
   - Annotate results in drawing
   - Store values in XData
8. Use `EX` command to export a CSV report

---

## 📚 Methodology

All equations and logic are based on:

**ASHRAE Fundamentals Handbook – 2021 Edition**

- **Darcy–Weisbach equation** for pressure loss
- **Colebrook–White equation** for friction factor
- Conversion support between SI and IP
- Supports circular and rectangular ducts

---

## ⚠️ Limitations

- No fittings (elbows, tees, reducers) are modeled in this version
- No static regain or system balancing
- Not intended for final detail design or construction documentation

---

## 📌 Roadmap

Planned future development:

- Fitting-based loss calculation using attributes or node types
- Static regain and constant velocity methods
- Support for fan and exhaust system sizing
- Graphical summaries and interactive dashboards
- Educational version for HVAC training

---

## 📩 Contact

**Hadi Milani**  
Independent HVAC Engineer – Iran  
📧 milanihadi5@gmail.com

---

## 🔒 License

Shared under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)  
© 2025 – For educational and non-commercial use only
