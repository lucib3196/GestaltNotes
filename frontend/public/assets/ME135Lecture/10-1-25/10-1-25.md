# Lecture Source: 10-1-25.pdf

## Ideal-Gas Processes: Isothermal, Adiabatic (Reversible), Polytropic and Free Expansion

**Lecture Type:** derivation-heavy

### Summary
A focused review of thermodynamic properties and specific heats for ideal gases, followed by derivations and discussion of common thermodynamic processes. The lecture covers how the first and second laws apply to isothermal, reversible adiabatic (isentropic), polytropic and free expansion processes, and shows how to compute work, heat transfer and entropy change for each case. It also situates these processes on p–v diagrams and contrasts their characteristic relations.

### Core Topics
- Thermodynamic properties (P, V, T, u, h, s)
- Specific heats Cp and Cv
- Ideal gas relations
- Entropy change for ideal gases
- Isothermal process
- Reversible adiabatic (isentropic) process
- Polytropic process
- Free (Joule) expansion
- Work and heat calculations for processes
- p–v process family and diagram

### Learning Objectives
1. explain definitions of enthalpy and entropy and the role of specific heats for ideal gases
2. derive key relations linking Cp, Cv and the ideal-gas constant for an ideal gas
3. apply the first law to compute work and heat for isothermal, adiabatic and polytropic processes
4. derive process-specific relations and identify when a process is isentropic
5. calculate entropy change for reversible and irreversible ideal-gas processes including free expansion
6. interpret and compare process paths on a p–v diagram

### Assumed Prerequisites
- basic calculus (integration and logarithms)
- introductory thermodynamics (first and second laws)
- familiarity with the ideal gas law


## Derivations

### **Reversible adiabatic (ideal gas) — relation between p, v, T and work**
**Stub:** Derive: $$p v^{\gamma}=\text{const},\quad T v^{\gamma-1}=\text{const},\quad w=\dfrac{p_1v_1-p_2v_2}{\gamma-1}$$ for a reversible adiabatic ideal gas (\(q=0\)).

**Steps:**
1. 1) Start: reversible adiabatic ⇒ $$\delta q_{rev}=0.$$ First law (per unit mass or per mole): $$\delta q-\delta w=du\Rightarrow 0-\delta w=du\Rightarrow -\delta w=du.$$
2. 2) For reversible work, $$\delta w=p\,dv\,$$ (sign convention in notes leads to $$-p\,dv=du$$). For an ideal gas, $$du=C_v\,dT.$$ So
3.    $$-p\,dv=C_v\,dT.$$
4. 3) Use ideal-gas law $$p v = R T\quad\Rightarrow\quad p=\dfrac{R T}{v}.$$ Substitute into the differential relation:
5.    $$-\dfrac{R T}{v}\,dv = C_v\,dT.$$
6. 4) Rearranged (divide by RT):
7.    $$\dfrac{C_v}{R}\dfrac{dT}{T} + \dfrac{dv}{v}=0.$$
8. 5) Integrate between states 1 and 2:
9.    $$\dfrac{C_v}{R}\ln\dfrac{T_2}{T_1} + \ln\dfrac{v_2}{v_1}=0\quad\Rightarrow\quad \ln\left[\left(\dfrac{T_2}{T_1}\right)^{C_v/R}\dfrac{v_2}{v_1}\right]=0.$$
10. 6) Exponentiate and rearrange to show the T–v relation. Using $$\dfrac{R}{C_v}=\gamma-1\quad(\text{since }C_p-C_v=R,\;\gamma= C_p/C_v),$$ we get
11.    $$T_2\,v_2^{\gamma-1}=T_1\,v_1^{\gamma-1}\quad\Rightarrow\quad T\,v^{\gamma-1}=\text{const}.$$
12. 7) From ideal gas, multiply the previous relation by appropriate power of v to get p–v relation:
13.    $$p v^{\gamma} = \left(\dfrac{R T}{v}\right) v^{\gamma} = R T v^{\gamma-1} = \text{const}.$$
14.    Therefore $$p v^{\gamma}=\text{const}.$$
15. 8) Work for a reversible adiabatic process: write $$p = C v^{-\gamma}\ (C=\text{const}).$$ Then
16.    $$w=\int_{v_1}^{v_2} p\,dv = C\int_{v_1}^{v_2} v^{-\gamma}\,dv = \dfrac{C}{-\gamma+1}\left[v^{-\gamma+1}\right]_{v_1}^{v_2}.$$
17.    Using $$C=p_1 v_1^{\gamma}$$ this becomes
18.    $$w=\dfrac{p_1 v_1 - p_2 v_2}{\gamma-1}.$$
19.    Equivalently, with ideal-gas substitution, $$w=\dfrac{mR(T_1-T_2)}{\gamma-1}.$$
20. 9) Internal energy change and entropy: for adiabatic reversible, $$\delta q=0\Rightarrow\Delta s=0\ (\text{isentropic}).$$ Also from first law used above, $$\Delta u = -w\ (\text{with sign convention used in notes}).$$
21. 10) Completeness: The derivation shown on pages 3–4 is essentially complete for an ideal gas with constant heat capacities (Cp,Cv constant). The notes assume constant Cv and ideal-gas behaviour; sign convention for work is the one used in the notes (gives -p dv = du). No boundary-condition integrals are missing for this derivation.

**Reference:** start_page=3 end_page=4
### **Entropy change for an ideal gas (general expression)**
**Stub:** Derive: $$\Delta s = C_v\ln\dfrac{T_2}{T_1} + R\ln\dfrac{v_2}{v_1} = C_p\ln\dfrac{T_2}{T_1} - R\ln\dfrac{p_2}{p_1}.$$

**Steps:**
1. 1) Start from differential entropy for a reversible change: $$ds = \dfrac{\delta q_{rev}}{T}.$$ For an ideal gas with constant heat capacities, express dq in terms of dT and dv (or dp):
2. 2) Using internal energy relation and Maxwell-type manipulations leads to the integrated forms:
3.    $$\Delta s = C_v\ln\dfrac{T_2}{T_1} + R\ln\dfrac{v_2}{v_1},$$
4.    and, using $$p v = R T$$, equivalently
5.    $$\Delta s = C_p\ln\dfrac{T_2}{T_1} - R\ln\dfrac{p_2}{p_1}.$$

**Reference:** start_page=1 end_page=2
### **Isothermal process (ideal gas): work and entropy**
**Stub:** Show for isothermal (T constant): $$p v = \text{const},\quad w = p_1 v_1 \ln\dfrac{v_2}{v_1},\quad q=w,\quad \Delta s = R\ln\dfrac{v_2}{v_1}.$$

**Steps:**
1. 1) For isothermal T1=T2 and ideal gas, $$p_1 v_1 = p_2 v_2 = m R T.$$ Thus $$p v = \text{const}.$$
2. 2) Work done: $$w=\int_{v_1}^{v_2} p\,dv = \int_{v_1}^{v_2} \dfrac{C}{v}\,dv = C\ln\dfrac{v_2}{v_1} = p_1 v_1 \ln\dfrac{v_2}{v_1}.$$
3. 3) Energy: for ideal gas $$\Delta u=0\Rightarrow q=w.$$ Entropy change for the reversible isothermal process:
4.    $$\Delta s = \dfrac{q_{rev}}{T} = R\ln\dfrac{v_2}{v_1} = -R\ln\dfrac{p_2}{p_1}.$$

**Reference:** start_page=2 end_page=2
### **Cp, Cv relation and definition of adiabatic index**
**Stub:** Show: $$C_p-C_v = R,\quad \gamma\equiv\dfrac{C_p}{C_v},\quad C_v=\dfrac{R}{\gamma-1}.$$

**Steps:**
1. 1) Definitions: $$C_p\equiv\left(\dfrac{\partial h}{\partial T}\right)_p,\quad C_v\equiv\left(\dfrac{\partial u}{\partial T}\right)_v.$$ For an ideal gas h=u+pv and p v = R T.
2. 2) Differentiate and combine to get $$C_p - C_v = R.$$ Define $$\gamma\equiv C_p/C_v$$ and rearrange to obtain $$C_v=\dfrac{R}{\gamma-1},\; C_p=\dfrac{\gamma R}{\gamma-1}.$$

**Reference:** start_page=1 end_page=1
### **Work and relations for a polytropic process (pv^n=const)**
**Stub:** For polytropic index n: $$p v^{n}=\text{const},\quad w=\dfrac{p_1 v_1 - p_2 v_2}{n-1},\quad \Delta u = C_v\Delta T,\;\Delta h = C_p\Delta T.$$

**Steps:**
1. 1) Polytropic definition: $$p v^{n}=\text{const}.$$ Using ideal-gas relations one can write $$T v^{n-1}=\text{const},\; p\sim T^{n/(n-1)},\; T\sim p^{(n-1)/n}.$$
2. 2) Work for a polytropic process (n≠1): with $$p=C v^{-n}$$ then
3.    $$w=\int_{v_1}^{v_2} p\,dv = C\int_{v_1}^{v_2} v^{-n}\,dv = \dfrac{C}{-n+1}[v^{-n+1}]_{v_1}^{v_2} = \dfrac{p_1 v_1 - p_2 v_2}{n-1}.$$
4. 3) Internal and enthalpy changes use constant heat capacities: $$\Delta u=C_v\Delta T,\quad \Delta h=C_p\Delta T.$$ Entropy: $$\Delta s = C_p\ln\dfrac{T_2}{T_1} - R\ln\dfrac{p_2}{p_1}.$$

**Reference:** start_page=5 end_page=5
### **Free (Joule) expansion — entropy change**
**Stub:** For free expansion into vacuum (no work, no heat): $$q=0,\;w=0,\;\Delta u=0\Rightarrow\Delta T=0\Rightarrow\Delta h=0;\;\Delta s=R\ln\dfrac{v_2}{v_1}.$$

**Steps:**
1. 1) Free expansion: no heat exchange and no boundary work so $$q=0,\; w=0.$$ For ideal gas, $$\Delta u=0\Rightarrow \Delta T=0\Rightarrow \Delta h=0.$$
2. 2) Initial and final states satisfy ideal-gas law, but because the process is irreversible entropy increases. Using a reversible path between the same states (isothermal) gives the entropy change
3.    $$\Delta s = -R\ln\dfrac{p_2}{p_1} = R\ln\dfrac{v_2}{v_1}.$$

**Reference:** start_page=5 end_page=5
### **Summary of special processes and pv^n forms**
**Stub:** List: constant p (n=0), isothermal (pv=const, n=1), reversible adiabatic (pv^\gamma=const, n=\gamma), polytropic pv^n=const (general).

**Steps:**
1. 1) Special cases summarized on page 6: • constant pressure: p=const ⇒ pv^0=const (n=0), • constant volume: v=const (n→∞),
2.    • isothermal: pv=const (n=1), • reversible adiabatic: pv^{\gamma}=const (n=\gamma), • polytropic: pv^{n}=const (general).
3. 2) Graphical sketch on p–v plane shows these curves and limiting behaviours (not symbolic derivation but contextual summary).

**Reference:** start_page=6 end_page=6


## Questions

## Conceptual Questions### **Conceptual Question**
**Question:** For an ideal gas undergoing a reversible isothermal expansion from V1 to V2 (T constant), which of the following statements is correct?

**Topics:** Isothermal process, Ideal gas internal energy, Entropy change

**Options:**
- ✅ The internal energy change ΔU = 0
- No heat is transferred (q = 0)
- No work is done (w = 0)
- Entropy change ΔS = 0

**Explanation:** For an ideal gas u depends only on T, so ΔU = 0 for an isothermal process. By the first law q = w (heat absorbed equals work done). The entropy change is ΔS = R ln(V2/V1), not zero unless V2 = V1.

**Reference:** start_page=2 end_page=2
 ### **Conceptual Question**
**Question:** Which value of the polytropic exponent n corresponds to a reversible adiabatic (isentropic) process for an ideal gas?

**Topics:** Reversible adiabatic process, Polytropic process, Specific heat ratio (γ)

**Options:**
- n = 1
- ✅ n = γ (gamma = Cp/Cv)
- n = 0
- n → ∞

**Explanation:** A reversible adiabatic (no heat) process for an ideal gas obeys p v^γ = constant, where γ = Cp/Cv. Thus the polytropic exponent equals γ for the adiabatic case.

**Reference:** start_page=3 end_page=4
 ### **Conceptual Question**
**Question:** Which statement correctly describes a free (Joule) expansion of an ideal gas into vacuum?

**Topics:** Free expansion, First law of thermodynamics, Entropy (irreversibility)

**Options:**
- ✅ q = 0, w = 0, ΔU = 0 and entropy increases (ΔS > 0)
- q = 0, w = 0, ΔU = 0 and entropy change ΔS = 0
- q > 0, w = 0, ΔU > 0
- w > 0, q = 0, entropy decreases

**Explanation:** In free expansion there is no heat or work exchange (q = 0, w = 0). For an ideal gas ΔU depends only on T and remains zero (no temperature change). The process is irreversible, so entropy of the gas increases (ΔS > 0).

**Reference:** start_page=5 end_page=5
