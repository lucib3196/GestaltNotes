# Lecture Source: me118_Lecture_01_15.pdf

## Application of Conservation Laws and Differential Equations in Fluid Mechanics and Heat Transfer

**Lecture Type:** mixed

### Summary
This lecture explores the application of fundamental conservation principles, specifically mass conservation for fluid flow and energy conservation for heat transfer, to model dynamic physical systems. It covers the derivation of governing differential equations for a draining tank and a cooling object, and illustrates various mathematical techniques for solving these equations to predict system behavior over time.

### Core Topics
- Mass conservation
- Bernoulli's equation
- Fluid flow
- Tank draining
- Conservation of energy
- Heat transfer
- Convection
- Radiation
- Linearization of non-linear terms
- First-order ordinary differential equations
- Separation of variables
- Integrating factors
- Method of undetermined coefficients
- Time constant

### Learning Objectives
1. Apply mass conservation to analyze fluid flow problems
2. Utilize Bernoulli's equation to determine fluid velocities
3. Derive differential equations for the height of liquid in a draining tank
4. Apply the conservation of energy principle to transient heat transfer problems
5. Formulate differential equations for the temperature of a cooling object under convection and radiation
6. Linearize non-linear terms in differential equations for analytical solutions
7. Solve first-order ordinary differential equations using separation of variables
8. Solve first-order ordinary differential equations using integrating factors
9. Solve first-order ordinary differential equations using the method of undetermined coefficients
10. Interpret the time constant in transient system responses

### Assumed Prerequisites
- Basic calculus
- Basic physics
- Introductory differential equations


## Derivations

### **Draining of a Horizontal Cylindrical Tank**
**Stub:** Derivation of the liquid height H(t) as a function of time for a horizontal cylindrical tank draining through an orifice.

**Steps:**
1. The volume of liquid in a horizontal cylindrical tank of radius R and length L at height H is given by:
2. $$ V = R^2 L \cos^{-1}\left(\frac{R-H}{R}\right) - \frac{L}{2} (R-H) \sqrt{2HR - H^2} $$
3. Differentiate the volume V with respect to time t to find the rate of change of volume, dV/dt:
4. $$ \frac{dV}{dt} = \frac{d}{dt} \left( R^2 L \cos^{-1}\left(\frac{R-H}{R}\right) - \frac{L}{2} (R-H) \sqrt{2HR - H^2} \right) $$
5. The differentiation simplifies to the product of the liquid surface area and dH/dt:
6. $$ \frac{dV}{dt} = 2L \sqrt{2HR - H^2} \frac{dH}{dt} $$
7. Apply the principle of conservation of volume for the draining tank, where \(\dot{V}_{in}\) is inflow and \(\dot{V}_{out}\) is outflow:
8. $$ \frac{dV}{dt} = \dot{V}_{in} - \dot{V}_{out} $$
9. Substitute the derived dV/dt and Torricelli's Law for \(\dot{V}_{out} = A_0 \sqrt{2gH}\), assuming \(\dot{V}_{in} = 0\):
10. $$ 2L \sqrt{2HR - H^2} \frac{dH}{dt} = - A_0 \sqrt{2gH} $$
11. Rearrange the differential equation for integration:
12. $$ \frac{\sqrt{2HR - H^2}}{\sqrt{H}} dH = - \frac{A_0 \sqrt{2g}}{2L} dt $$
13. Simplify the left side and constant on the right side:
14. $$ \sqrt{2R - H} dH = - \frac{A_0 \sqrt{g/2}}{L} dt $$
15. Integrate both sides from initial height \(H_0\) to \(H\) and from time \(0\) to \(t\):
16. $$ \int_{H_0}^{H} \sqrt{2R - H} dH = - \frac{A_0 \sqrt{g/2}}{L} \int_{0}^{t} dt $$
17. Perform the integration:
18. $$ \left[ -\frac{2}{3} (2R - H)^{3/2} \right]_{H_0}^{H} = - \frac{A_0 \sqrt{g/2}}{L} t $$
19. $$ -\frac{2}{3} (2R - H)^{3/2} + \frac{2}{3} (2R - H_0)^{3/2} = - \frac{A_0 \sqrt{g/2}}{L} t $$
20. Solve for \(H(t)\) as a function of time:
21. $$ (2R - H)^{3/2} = (2R - H_0)^{3/2} + \frac{3 A_0 \sqrt{g/2}}{L} t $$
22. $$ H(t) = 2R - \left( (2R - H_0)^{3/2} + \frac{3 A_0 \sqrt{g/2}}{L} t \right)^{2/3} $$

**Reference:** start_page=2 end_page=4
### **General Conservation of Energy Equation**
**Stub:** States the general energy balance for a system including heat, work, and generation terms.

**Steps:**
1. The general conservation of energy equation is given by:
2. $$ \dot{E}_{in} - \dot{E}_{out} + \dot{Q} + \dot{W} + \dot{E}_{generated} = \frac{dE}{dt} $$

**Reference:** start_page=5 end_page=5
### **Rate of Change of Internal Energy**
**Stub:** Derives the rate of change of internal energy in terms of mass, specific heat, and temperature change, often used when \(\dot{Q} = dE/dt\).

**Steps:**
1. For a system where only heat transfer changes internal energy:
2. $$ \dot{Q} = \frac{dE}{dt} $$
3. The rate of change of internal energy for a material of mass m and specific heat \(C_p\) is:
4. $$ \frac{dE}{dt} = \frac{d(m C_p T)}{dt} = m C_p \frac{dT}{dt} $$

**Reference:** start_page=5 end_page=5
### **Convective Heat Transfer Rate**
**Stub:** Defines the rate of heat transfer due to convection, dependent on a heat transfer coefficient, surface area, and temperature difference.

**Steps:**
1. The rate of convective heat transfer is given by Newton's Law of Cooling:
2. $$ \dot{Q}_{conv} = h A (T - T_0) $$
3. where \(h\) is the convective heat transfer coefficient, \(A\) is the surface area, and \(T - T_0\) is the temperature difference.

**Reference:** start_page=5 end_page=5
### **Radiative Heat Transfer Rate (Stefan-Boltzmann Law)**
**Stub:** Defines the rate of heat transfer due to thermal radiation based on the Stefan-Boltzmann law, involving emissivity, surface area, and absolute temperatures.

**Steps:**
1. The rate of radiative heat transfer is given by the Stefan-Boltzmann Law:
2. $$ \dot{Q}_{rad} = \sigma \epsilon A (T^4 - T_0^4) $$
3. where \(\sigma\) is the Stefan-Boltzmann constant, \(\epsilon\) is the emissivity, \(A\) is the surface area, and \(T\) and \(T_0\) are absolute temperatures.

**Reference:** start_page=5 end_page=5
### **Rate of Change of Volume in a Horizontal Cylindrical Tank**
**Stub:** Derive the expression for the rate of change of liquid volume (dV/dt) in a horizontal cylindrical tank as a function of liquid height (H).

**Steps:**
1. Begin with the general mass balance equation, which simplifies to a volume balance for incompressible flow:$$\dot{m}_{in} - \dot{m}_{out} = \frac{dm}{dt} \Rightarrow \frac{dV}{dt} = \dot{V}_{in} - \dot{V}_{out}$$
2. The outflow rate is expressed using the area of the outlet ($A_o$) and the velocity of water ($V_{velocity of water}$), which can be determined from Bernoulli's equation for a free outflow:$$\dot{V}_{out} = A_o V_{velocity of water} = A_o \sqrt{2gH}$$
3. The volume ($V$) of liquid in a horizontal cylindrical tank of length ($L$) and radius ($R$) at a liquid height ($H$) is given by the product of the liquid cross-sectional area and the length. The cross-sectional area is the area of a circular segment:$$V = L \left[R^2 \cos^{-1}\left(\frac{R-H}{R}\right) - (R-H)\sqrt{2HR - H^2}\right]$$Note: This corrects an apparent error in the handwritten notes where a factor of 1/2 was present in the second term of the volume formula.
4. Differentiate the volume $V$ with respect to time $t$ to find $\frac{dV}{dt}$:$$\frac{dV}{dt} = L \frac{d}{dt} \left[R^2 \cos^{-1}\left(\frac{R-H}{R}\right) - (R-H)\sqrt{2HR - H^2}\right]$$
5. Differentiate the first term, $R^2 \cos^{-1}\left(\frac{R-H}{R}\right)$, with respect to $t$:$$\frac{d}{dt}\left(R^2 \cos^{-1}\left(\frac{R-H}{R}\right)\right) = R^2 \left(-\frac{1}{\sqrt{1 - \left(\frac{R-H}{R}\right)^2}}\right) \left(-\frac{1}{R}\frac{dH}{dt}\right) = \frac{R^2 \dot{H}}{\sqrt{2HR - H^2}}$$
6. Differentiate the second term, $(R-H)\sqrt{2HR - H^2}$, with respect to $t$ using the product rule:$$\frac{d}{dt}\left((R-H)\sqrt{2HR - H^2}\right) = (-\dot{H})\sqrt{2HR - H^2} + (R-H)\left(\frac{(R-H)\dot{H}}{\sqrt{2HR - H^2}}\right) = \frac{(R^2 - 4RH + 2H^2)\dot{H}}{\sqrt{2HR - H^2}}$$
7. Combine the differentiated terms to get the full expression for $\frac{dV}{dt}$:$$\frac{dV}{dt} = L \left[\frac{R^2 \dot{H}}{\sqrt{2HR - H^2}} - \frac{(R^2 - 4RH + 2H^2)\dot{H}}{\sqrt{2HR - H^2}}\right]$$
8. Simplify the expression by combining the numerators:$$\frac{dV}{dt} = L \frac{\dot{H}}{\sqrt{2HR - H^2}} [R^2 - (R^2 - 4RH + 2H^2)] = L \frac{\dot{H}}{\sqrt{2HR - H^2}} [4RH - 2H^2]$$
9. Further simplify the expression:$$\frac{dV}{dt} = L \frac{\dot{H} (2H)(2R - H)}{\sqrt{H(2R - H)}} = 2 L \dot{H} \sqrt{H(2R - H)} = 2 L \dot{H} \sqrt{2RH - H^2}$$

**Reference:** start_page=6 end_page=7
### **Volume Balance Equation for Tank**
**Stub:** Derive the differential form of the volume balance for an incompressible fluid in a tank.

**Steps:**
1. Start with the mass balance equation: $$\dot{m}_{in} - \dot{m}_{out} = \frac{dm}{dt}$$
2. For an incompressible fluid, density $\rho$ is constant, so $m = \rho V$. Substituting this into the mass balance: $$\rho \dot{V}_{in} - \rho \dot{V}_{out} = \frac{d(\rho V)}{dt}$$
3. Since $\rho$ is constant, it can be taken out of the derivative and cancelled: $$\dot{V}_{in} - \dot{V}_{out} = \frac{dV}{dt}$$

**Reference:** start_page=6 end_page=6
### **Outflow Velocity using Bernoulli's Equation**
**Stub:** Determine the velocity of water flowing out of an orifice at depth H using Bernoulli's principle.

**Steps:**
1. The outflow rate $$\dot{V}_{out}$$ is given by the product of the outlet area $A_o$ and the average outflow velocity $V_{velocity of water}$: $$\dot{V}_{out} = A_o V_{velocity of water}$$
2. Applying Bernoulli's equation between the free surface of the liquid and the outlet, assuming negligible velocity at the free surface and atmospheric pressure at both points, the velocity can be expressed as: $$V_{velocity of water} = \sqrt{2gH}$$
3. Therefore, the outflow rate is: $$\dot{V}_{out} = A_o \sqrt{2gH}$$

**Reference:** start_page=6 end_page=6
### **Differential Equation for Draining Spherical Tank (Alternate Approach)**
**Stub:** Derivation of the differential equation dH/dt for the height of liquid in a spherical tank draining through an orifice, leading to an integral form.

**Steps:**
1. Begin with the geometric definition of the diameter AC of a circular liquid surface at height H from the bottom of a sphere of radius R. AC = 2 CD. Using the Pythagorean theorem, CD = sqrt(R^2 - (R-H)^2), which simplifies to AC = 2 sqrt(2RH - H^2).
2. Define the differential volume dV of a horizontal liquid slice as dV = (AC) dH L, where L is a constant. Substituting the expression for AC gives dV = 2 sqrt(2RH - H^2) dH L.
3. Express the rate of change of volume with respect to time as dV/dt = 2 sqrt(2RH - H^2) (dH/dt) L.
4. Apply the principle of conservation of volume, dV/dt = V_in_dot - V_out_dot. Using Torricelli's Law for outflow, V_out_dot = A_0 sqrt(2gH), where A_0 is the orifice area. Equating these expressions yields 2 sqrt(2RH - H^2) (dH/dt) L = V_in_dot - A_0 sqrt(2gH).
5. Consider the scenario with no inflow (V_in_dot = 0), which simplifies the equation to 2 sqrt(2RH - H^2) (dH/dt) L = - A_0 sqrt(2gH).
6. Attempt to separate variables for integration, resulting in the expression (sqrt(2RH - H^2)/H) dH 
eq - (A_0 sqrt(2g) dt)/L^2. This step contains an apparent inconsistency with the not-equal symbol and the L^2 term. The subsequent integral is presented as integral(sqrt(2R-H) dH) = - (A_0/L) integral_0^t(sqrt(2g/H) dt). The left side is missing a factor, and H is incorrectly placed inside the dt integral on the right side, indicating an incomplete or erroneous setup for integration.

**Reference:** start_page=3 end_page=3
### **Height as a Function of Time**
**Stub:** Derive the expression for $H(t)$ from an integrated differential equation.

**Steps:**
1. The result of integrating an expression, with limits applied from $H_0$ to $H$: $$\frac{(2R-H)^{3/2}}{-3/2} \Big|_{H_0}^H = -\frac{A_0}{L}\sqrt{\frac{g}{2}} t$$
2. Applying the limits of integration and multiplying by $-\frac{3}{2}$: $$(2R-H)^{3/2} - (2R-H_0)^{3/2} = \frac{3}{2} \frac{A_0}{L}\sqrt{\frac{g}{2}} t$$
3. Isolating the term involving $H$: $$(2R-H)^{3/2} = (2R-H_0)^{3/2} + \frac{3}{2} \frac{A_0}{L}\sqrt{\frac{g}{2}} t$$
4. Solving for $H(t)$ by raising both sides to the $2/3$ power and rearranging: $$H(t) = 2R - \left((2R-H_0)^{3/2} + \frac{3}{2} \frac{A_0}{L}\sqrt{\frac{g}{2}} t\right)^{2/3}$$

**Reference:** start_page=4 end_page=4
### **Conservation of Energy and Heat Transfer Components**
**Stub:** Derive the rate of heat transfer components (convection and radiation) from the general conservation of energy equation for a specific system.

**Steps:**
1. The general conservation of energy equation for a control volume is given by $$\dot{E}_{in} - \dot{E}_{out} + \dot{Q} + \dot{W} + \dot{E}_{generated} = \frac{dE}{dt}$$ where $\dot{E}_{in}$ and $\dot{E}_{out}$ are energy inflow/outflow, $\dot{Q}$ is heat transfer, $\dot{W}$ is work done, $\dot{E}_{generated}$ is energy generated, and $\frac{dE}{dt}$ is the rate of change of total energy within the control volume.
2. Consider a system (an oven containing a mass $m$ of material with specific heat $C_p$ and surface area $A$) where there is no mass flow ($\dot{E}_{in}=0, \dot{E}_{out}=0$), no work done ($\dot{W}=0$), and no energy generation ($\dot{E}_{generated}=0$). Only heat transfer $\dot{Q}$ is present.
3. Under these conditions, the conservation of energy equation simplifies to $$\dot{Q} = \frac{dE}{dt}$$
4. The change in internal energy $dE$ for a material of mass $m$ and specific heat $C_p$ at temperature $T$ is given by $$dE = d(m C_p T)$$
5. Therefore, the rate of change of internal energy is $$\frac{dE}{dt} = m C_p \frac{dT}{dt}$$
6. The total heat transfer rate $\dot{Q}$ can be decomposed into convective and radiative components: $\dot{Q} = \dot{Q}_{conv} + \dot{Q}_{rad}$.
7. Convective heat transfer is given by $$\dot{Q}_{conv} = h A (T - T_0)$$ where $h$ is the heat transfer convective coefficient, $A$ is the surface area, and $(T - T_0)$ is the temperature difference.
8. Radiative heat transfer is given by the Stefan-Boltzmann law: $$\dot{Q}_{rad} = \sigma A \epsilon (T^4 - T_0^4)$$ where $\sigma$ is the Stefan-Boltzmann constant ($5.67 \times 10^{-8} W m^{-2} K^{-4}$), $A$ is the surface area, $\epsilon$ is the emissivity, and $T$ and $T_0$ are absolute temperatures.

**Reference:** start_page=5 end_page=5
### **Linearization of Combined Convection and Radiation Heat Transfer Equation**
**Stub:** Derive the linearized differential equation for temperature change due to combined convection and radiation heat transfer, approximating the fourth-order term.

**Steps:**
1. Starting with the energy balance equation: $$mc_p \frac{dT}{dt} = \dot{Q}$$
2. Expressing the heat transfer rate (Q) as a sum of convection and radiation terms: $$mc_p \frac{dT}{dt} = -(hA(T-T_0) + \sigma A \epsilon (T^4 - T_0^4))$$
3. Rearranging to isolate the rate of temperature change: $$\frac{dT}{dt} = -\frac{1}{mc_p} (hA(T-T_0) + \sigma A \epsilon (T^4 - T_0^4))$$
4. Let the non-linear heat transfer function be: $$f(T) = hA(T-T_0) + \sigma A \epsilon (T^4 - T_0^4)$$
5. Linearize the function f(T) about the reference temperature T_0 using a Taylor series expansion: $$f(T) \approx f(T_0) + f'(T_0)(T-T_0)$$
6. Evaluate f(T) at T_0: $$f(T_0) = hA(T_0-T_0) + \sigma A \epsilon (T_0^4 - T_0^4) = 0$$
7. Calculate the first derivative of f(T) with respect to T: $$f'(T) = \frac{d}{dT}[hA(T-T_0) + \sigma A \epsilon (T^4 - T_0^4)] = hA + 4\sigma A \epsilon T^3$$
8. Evaluate the derivative at T_0: $$f'(T_0) = hA + 4\sigma A \epsilon T_0^3$$
9. Substitute f(T_0) and f'(T_0) back into the linearized expression for f(T): $$f(T) \approx (hA + 4\sigma A \epsilon T_0^3)(T-T_0)$$
10. Substitute the linearized f(T) back into the differential equation for dT/dt: $$\frac{dT}{dt} = -\frac{1}{mc_p} (hA + 4\sigma A \epsilon T_0^3)(T-T_0)$$
11. Define a constant k for simplification: $$k \triangleq \frac{hA + 4\sigma A \epsilon T_0^3}{mc_p}$$
12. The final linearized differential equation is: $$\frac{dT}{dt} = -k(T-T_0)$$

**Reference:** start_page=56 end_page=56


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** According to the lecture material, which principle is primarily used to determine the velocity of water flowing out of a tank through an outlet, and how is this velocity related to the fluid height?

**Topics:** Fluid Dynamics, Bernoulli's Equation, Tank Drainage

**Options:**
- Archimedes' principle; velocity is inversely proportional to the fluid height.
- Pascal's principle; velocity is directly proportional to the pressure at the outlet.
- ✅ Bernoulli's equation; velocity is proportional to the square root of the fluid height.
- Newton's second law; velocity is proportional to the mass of the fluid.

**Explanation:** The lecture material explicitly states that the velocity of water flowing out of the tank (Vout) is derived from Bernoulli's equation and is given by V = sqrt(2gH), indicating a direct proportionality to the square root of the fluid height (H).

**Reference:** start_page=1 end_page=1
### **Conceptual Question**
**Question:** In the context of the oven heating/cooling problem presented, what are the two primary modes of heat transfer considered for the object inside the oven, and how do their dependencies on temperature differ?

**Topics:** Heat Transfer, Convection, Radiation

**Options:**
- Conduction and Evaporation; conduction is dominant at high temperatures.
- ✅ Convection and Radiation; convection depends linearly on temperature difference, while radiation depends on the fourth power of absolute temperature.
- Conduction and Convection; conduction occurs through the oven walls, convection within the air.
- Radiation and Phase Change; radiation is significant, but phase change is not considered for the object's temperature change.

**Explanation:** The lecture material identifies two primary modes of heat transfer for the oven problem: convection, represented by Q_conv = hA(T-T0), and radiation, represented by Q_rad = sigma A epsilon (T^4 - T0^4). Convection is linear with temperature difference, while radiation is non-linear, depending on the fourth power of absolute temperature.

**Reference:** start_page=5 end_page=5
### **Conceptual Question**
**Question:** Why is the T^4 term in the heat transfer equation often linearized around a reference temperature (T0), and what is the physical significance of the resulting 'k' value in the simplified equation dT/dt = -k(T-T0)?

**Topics:** Linearization, Heat Transfer Coefficients, Time Constant

**Options:**
- To simplify calculations for conduction; 'k' represents the thermal conductivity of the material.
- ✅ To approximate the non-linear radiation term for easier analytical solution of the differential equation; 'k' is related to the inverse of the thermal time constant, indicating the rate of temperature change.
- To account for heat generation within the system; 'k' represents the rate of internal energy production.
- To make the equation applicable only to very low temperatures; 'k' is a universal constant.

**Explanation:** The T^4 term from radiation is non-linear, making the differential equation difficult to solve directly. Linearizing it around a reference temperature T0 simplifies the equation to a first-order linear form, dT/dt = -k(T-T0). The 'k' value in this linearized equation is the inverse of the thermal time constant (tau = 1/k), which characterizes how quickly the system's temperature approaches the ambient temperature.

**Reference:** start_page=6 end_page=9
