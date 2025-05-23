# Hadi-Milani
AutoLISP tool for HVAC Equal Friction duct sizing in AutoCAD
# EFDS – Equal Friction Duct Sizing Tool for AutoCAD

**EFDS** is a lightweight AutoLISP-based tool designed to automate duct sizing in AutoCAD using the Equal Friction Method. It calculates and annotates duct dimensions, velocity, and pressure loss directly on duct lines based on flow input, all within AutoCAD – no external software required.

## 🔧 Features

- AutoCAD-native (runs using AutoLISP `.fas` file)
- Supports both Imperial (in, fpm, in.wg) and Metric (mm, m/s, Pa) units
- Uses Darcy-Weisbach and Colebrook-White equations (per ASHRAE Fundamentals Handbook – 2021)
- Trace-based network analysis and automatic annotation
- XData storage of calculated values
- CSV export support

## 📁 Included Files

- `EFDS.fas` – compiled AutoLISP executable (source not included)
- `Sample_Duct_Network.dwg` – sample AutoCAD drawing
- `How_To_Use.txt` – step-by-step instructions

## 🧪 How to Use

1. Open AutoCAD and load `EFDS.fas` via the `APPLOAD` command.
2. Type `EFDS` in the command line to launch the parameter input dialog.
3. Choose unit system and input parameters (air density, roughness, friction loss rate).
4. Select the starting point on the duct network.
5. Select all duct lines in the network (LWPOLYLINE or LINE).
6. The tool will:
   - Trace the network and read diffuser blocks (`FLOW RATE` attribute)
   - Calculate diameter, velocity, friction loss
   - Annotate lines with flow data in correct units
   - Store full data in XData for future access
7. Type `EX` to export results to CSV.

## 📚 Methodology

- Based entirely on the **ASHRAE Fundamentals Handbook (2021)**
- Implements:
  - Darcy-Weisbach equation
  - Colebrook-White friction factor solver
- Supports both round and rectangular ducts (with auto W/H conversion)

## ⚠️ Limitations

- Fittings (elbows, tees) are not modeled in this version
- No static regain or pressure balancing yet
- Intended for educational and early design phases

## 📄 License

This project is shared for **educational and non-commercial use only.**  
Redistribution, modification, or reverse engineering is **not permitted.**  
See `LICENSE` for details.

---

## ✉ Contact

**Hadi Milani**  
Independent HVAC Engineer – Iran  
📧 milanihadi5@gmail.com
