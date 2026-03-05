# Lecture Source: me118_Lecture_01_20.pdf

## Modeling Transient Systems: Heat Transfer and Pollution

**Lecture Type:** derivation-heavy

### Summary
This lecture introduces the application of first-order ordinary differential equations to model transient phenomena in physical systems. It covers the derivation of the heat transfer equation for an object cooling or heating in an environment (Newton's Law of Cooling) and develops a box model to analyze the dynamic concentration of pollutants in a city. The lecture also explores different analytical methods for solving these types of differential equations, including separable equations, integrating factors, and undetermined coefficients.

### Core Topics
- Transient system modeling
- Heat transfer
- Newton's Law of Cooling
- Pollution box models
- Mass balance
- Conservation of energy
- First-order ordinary differential equations
- Solution methods for ODEs

### Learning Objectives
1. Formulate differential equations to describe transient heat transfer phenomena
2. Derive the temperature-time relationship for an object based on Newton's Law of Cooling
3. Construct a box model to represent pollutant concentration changes in an environment
4. Derive the concentration-time relationship for pollutants using a mass balance approach
5. Apply analytical techniques (e.g., integrating factors, undetermined coefficients) to solve first-order linear ordinary differential equations
6. Interpret the transient behavior of systems modeled by first-order differential equations

### Assumed Prerequisites
- Calculus
- Basic physics principles (conservation laws)


## Derivations

### **Derivation of Temperature Profile using Newton's Law of Cooling**
**Stub:** Derive the temperature as a function of time, T(t), based on Newton's Law of Cooling: $$T(t) = T_0 + (T_i - T_0)e^{-kt}$$

**Steps:**
1. Start with the energy balance equation, representing Newton's Law of Cooling, where m is mass, c_p is specific heat, h is heat transfer coefficient, A_s is surface area, T is current temperature, and T_0 is ambient temperature: $$m c_p \frac{dT}{dt} = -h A_s (T-T_0)$$
2. Simplify by defining a constant $k = \frac{h A_s}{m c_p}$: $$\frac{dT}{dt} = -k(T-T_0)$$
3. Separate variables to prepare for integration: $$\frac{dT}{T-T_0} = -k dt$$
4. Integrate both sides from the initial temperature $T_i$ at time $t=0$ to the current temperature $T$ at time $t$: $$\int_{T_i}^{T} \frac{dT}{T-T_0} = \int_{0}^{t} -k dt$$
5. Perform the integration, yielding natural logarithms: $$[\ln(T-T_0)]_{T_i}^{T} = -kt$$
6. Apply the limits of integration: $$\ln(T-T_0) - \ln(T_i-T_0) = -kt$$
7. Combine the logarithmic terms using logarithm properties: $$\ln\left(\frac{T-T_0}{T_i-T_0}\right) = -kt$$
8. Exponentiate both sides to remove the natural logarithm: $$\frac{T-T_0}{T_i-T_0} = e^{-kt}$$
9. Rearrange the equation to solve for the temperature as a function of time, T(t): $$T(t) = T_0 + (T_i-T_0)e^{-kt}$$
10. This can also be expressed as a weighted average of initial and ambient temperatures: $$T(t) = T_i e^{-kt} + T_0 (1-e^{-kt})$$
11. Verify boundary conditions: At $t=0$, $T(0) = T_0 + (T_i-T_0)e^0 = T_0 + T_i - T_0 = T_i$. As $t \to \infty$, $T(\infty) = T_0 + (T_i-T_0)e^{-\infty} = T_0 + 0 = T_0$.

**Reference:** start_page=2 end_page=3
### **Derivation of Pollutant Concentration Equation in a Box Model**
**Stub:** Derive the differential equation for pollutant concentration C(t) in a box model: $$\frac{dC}{dt} = \frac{C_0 u}{L} - \frac{C u}{L} + \frac{q_g}{H} - k_D C$$

**Steps:**
1. Define the box model parameters: L (length), W (width), H (height), u (wind speed), C_0 (background concentration), C(t) (pollutant concentration), q_g (pollutant generation rate per unit area), k_D (pollutant destruction constant).
2. Start with the general mass balance equation for the pollutant within the box: $$m_{in} - m_{out} + m_{gen} - m_{destroyed} = \frac{dm}{dt}$$
3. Express the mass inflow rate due to wind: $$m_{in} = C_0 \cdot (WHu)$$
4. Express the mass outflow rate due to wind: $$m_{out} = C \cdot (WHu)$$
5. Express the mass generation rate within the box: $$m_{gen} = q_g \cdot (LW)$$
6. Express the mass destruction rate (assuming first-order kinetics): $$m_{destroyed} = k_D \cdot (C \cdot WLH)$$
7. Express the rate of change of mass within the box: $$\frac{dm}{dt} = \frac{d}{dt} (C \cdot WLH) = WLH \frac{dC}{dt}$$ (assuming W, L, H are constant)
8. Substitute all the individual rate terms into the mass balance equation: $$C_0 WHu - C WHu + q_g LW - k_D C WLH = WLH \frac{dC}{dt}$$
9. Divide the entire equation by the volume of the box (WLH) to obtain the rate of change of concentration: $$\frac{C_0 WHu}{WLH} - \frac{C WHu}{WLH} + \frac{q_g LW}{WLH} - \frac{k_D C WLH}{WLH} = \frac{WLH}{WLH} \frac{dC}{dt}$$
10. Simplify the terms to arrive at the final differential equation for pollutant concentration: $$\frac{dC}{dt} = \frac{C_0 u}{L} - \frac{C u}{L} + \frac{q_g}{H} - k_D C$$

**Reference:** start_page=4 end_page=4
### **Solution of a First-Order Linear ODE for Temperature with Time-Varying Forcing**
**Stub:** Solving the differential equation $\frac{dT}{dt} + kT = k T_0(t)$ where $T_0(t)$ is a linear function of time, using the method of undetermined coefficients to find the coefficients $A$ and $B$ for the particular solution.

**Steps:**
1. The initial differential equation for temperature $T$ is given as: $$\frac{dT}{dt} = -k(T - T_0)$$
2. Rearranging into the standard linear first-order ODE form yields: $$\frac{dT}{dt} + kT = kT_0$$
3. The initial condition for temperature is: $$T(0) = T_i$$
4. From the provided graph, the ambient temperature $T_0$ is observed to vary linearly with time $t$ from $T_i$ to $T_f$ over a duration $b$. This can be expressed as: $$T_0(t) = \frac{T_f - T_i}{b} t + T_i$$
5. Substituting the expression for $T_0(t)$ into the ODE results in: $$\frac{dT}{dt} + kT = k\left(\frac{T_f - T_i}{b} t + T_i\right)$$ This equation is noted as 'Not Separable'.
6. To solve this non-homogeneous ODE, the method of undetermined coefficients is applied. First, the homogeneous solution $T_C(t)$ is found from: $$\frac{dT}{dt} + kT = 0$$
7. The homogeneous solution is: $$T_C(t) = C_1 e^{-kt}$$
8. For the particular solution $T_P(t)$, since the forcing term $k((T_f - T_i)/b \cdot t + T_i)$ is linear in $t$, we assume a form: $$T_P(t) = At + B$$
9. Differentiating $T_P(t)$ with respect to $t$ gives: $$\frac{dT_P}{dt} = A$$
10. Substitute $T_P(t)$ and $\frac{dT_P}{dt}$ into the non-homogeneous ODE: $$A + k(At + B) = k\frac{T_f - T_i}{b} t + kT_i$$
11. Equate the coefficients of the linear term ($t$) on both sides: $$kA = k\frac{T_f - T_i}{b}$$
12. Solving for $A$ yields: $$A = \frac{T_f - T_i}{b}$$
13. Equate the constant terms on both sides: $$A + kB = kT_i$$

**Reference:** start_page=5 end_page=5
### **First-Order Linear ODE for Concentration C**
**Stub:** Set up the first-order linear ordinary differential equation for concentration $C$ with an initial condition.

**Steps:**
1. The initial expression for the rate of change of concentration $C$ is given as: $$\frac{dC}{dt} = -\left(k_D + \frac{u}{L}\right)C + \frac{q_g}{H} + \frac{C_0 u}{L}$$
2. Rearranging this into the standard linear first-order ODE form $\frac{dC}{dt} + P(t)C = Q(t)$ yields: $$\frac{dC}{dt} + \left(k_D + \frac{u}{L}\right)C = \frac{q_g}{H} + \frac{C_0 u}{L}$$
3. The initial condition for concentration $C$ is given as: $$C(0) = C_0$$

**Reference:** start_page=4 end_page=4
### **Solution of First-Order Linear Differential Equation for Temperature T(t) with Linear Source Term**
**Stub:** Derive the temperature T(t) as a function of time from the differential equation $$dT/dt + kT = k T_i + k(T_f - T_i)/b t$$ with initial condition $$T(0) = T_i$$.

**Steps:**
1. Start with the first-order linear differential equation: $$\frac{dT}{dt} + kT = k T_i + \frac{k(T_f - T_i)}{b} t$$
2. Multiply the equation by the integrating factor $$e^{kt}$$: $$e^{kt}\frac{dT}{dt} + k e^{kt} T = k T_i e^{kt} + \frac{k(T_f - T_i)}{b} t e^{kt}$$
3. Recognize the left side as the derivative of the product $$T e^{kt}$$: $$\frac{d}{dt}(T e^{kt}) = k T_i e^{kt} + \frac{k(T_f - T_i)}{b} t e^{kt}$$
4. Integrate both sides from $$0$$ to $$t$$: $$\int_{0}^{t} d(T e^{k\tau}) = \int_{0}^{t} \left(k T_i e^{k\tau} + \frac{k(T_f - T_i)}{b} \tau e^{k\tau}\right) d\tau$$
5. Evaluate the left integral and separate the right-hand side integrals: $$T(t) e^{kt} - T(0) = k T_i \int_{0}^{t} e^{k\tau} d\tau + \frac{k(T_f - T_i)}{b} \int_{0}^{t} \tau e^{k\tau} d\tau$$
6. Evaluate the first integral: $$k T_i \int_{0}^{t} e^{k\tau} d\tau = T_i (e^{kt} - 1)$$
7. Evaluate the second integral using integration by parts: $$\int_{0}^{t} \tau e^{k\tau} d\tau = \frac{t}{k} e^{kt} - \frac{1}{k^2} (e^{kt} - 1)$$
8. Substitute $$T(0) = T_i$$ and the evaluated integrals back into the equation: $$T(t) e^{kt} - T_i = T_i (e^{kt} - 1) + \frac{k(T_f - T_i)}{b} \left[\frac{t}{k} e^{kt} - \frac{1}{k^2} (e^{kt} - 1)\right]$$
9. Rearrange and simplify to solve for $$T(t)$$: $$T(t) = T_i + \frac{T_f - T_i}{b} t + \frac{T_f - T_i}{bk} (e^{-kt} - 1)$$

**Reference:** start_page=6 end_page=8
### **Integration by Parts of t e^(kt)**
**Stub:** Evaluate the definite integral $$\int_{0}^{t} \tau e^{k\tau} d\tau$$ using integration by parts.

**Steps:**
1. Apply integration by parts $$\int u dv = uv - \int v du$$ with $$u = \tau$$ and $$dv = e^{k\tau} d\tau$$.
2. This yields $$du = d\tau$$ and $$v = (1/k) e^{k\tau}$$.
3. The integral becomes: $$\left[\frac{\tau}{k} e^{k\tau}\right]_{0}^{t} - \int_{0}^{t} \frac{1}{k} e^{k\tau} d\tau$$
4. Evaluate the terms: $$\frac{t}{k} e^{kt} - \frac{1}{k} \left[\frac{1}{k} e^{k\tau}\right]_{0}^{t}$$
5. Simplify to the final result: $$\frac{t}{k} e^{kt} - \frac{1}{k^2} (e^{kt} - 1)$$

**Reference:** start_page=7 end_page=7
### **Partial Derivation for T(t) with Exponentially Decaying Source Term**
**Stub:** Partially derive the expression for $$T(t)$$ from the differential equation $$\frac{dT}{dt} + kT = k(T_s)$$ where $$T_s = T_i e^{-\beta t} + T_f (1 - e^{-\beta t})$$.

**Steps:**
1. State the initial differential equation: $$\frac{dT}{dt} + kT = k(T_s)$$
2. Substitute the expression for $$T_s$$: $$\frac{dT}{dt} + kT = k \left(T_i e^{-\beta t} + T_f (1 - e^{-\beta t})\right)$$
3. Rearrange the right-hand side: $$\frac{dT}{dt} + kT = k T_f + k(T_i - T_f) e^{-\beta t}$$
4. Multiply by the integrating factor $$e^{kt}$$: $$e^{kt}\frac{dT}{dt} + k T e^{kt} = k T_f e^{kt} + k(T_i - T_f) e^{(k-\beta)t}$$
5. Recognize the left side as the derivative of the product $$T e^{kt}$$: $$\frac{d}{dt}(T e^{kt}) = k T_f e^{kt} + k(T_i - T_f) e^{(k-\beta)t}$$
6. Integrate both sides from $$0$$ to $$t$$: $$\int d(T e^{k\tau}) = \int_{0}^{t} k T_f e^{k\tau} d\tau + \int_{0}^{t} k(T_i - T_f) e^{(k-\beta)\tau} d\tau$$
7. Evaluate the integrals and apply an assumed initial condition $$T(0) = T_i$$: $$T(t)e^{kt} - T_i = T_f (e^{kt} - 1) + \frac{k(T_i - T_f)}{k-\beta} (e^{(k-\beta)t} - 1)$$

**Reference:** start_page=9 end_page=9
### **Temperature Evolution in Two Limiting Cases**
**Stub:** Simplify the general temperature evolution equation $T(t)$ for the limiting cases $k \gg \beta$ and $k \ll \beta$.

**Steps:**
1. The initial general equation for temperature $T(t)$ is given by: $$T(t) = T_i e^{-kt} + T_f (1 - e^{-kt}) + \frac{k}{k - \beta} (T_i - T_f) [e^{-\beta t} - e^{-kt}]$$
2. Case I: When $k \gg \beta$. In this limit, $k - \beta \approx k$. Also, $e^{-kt}$ decays much faster than $e^{-\beta t}$, so for sufficiently large $t$, $e^{-kt} \approx 0$ in the difference term. The equation becomes: $$T(t) \approx T_f + \frac{k}{k} (T_i - T_f) [e^{-\beta t} - 0]$$
3. Simplifying Case I further: $$T(t) = T_f + (T_i - T_f) e^{-\beta t}$$
4. Case II: When $k \ll \beta$. In this limit, $k - \beta \approx -\beta$. Also, $e^{-\beta t}$ decays much faster than $e^{-kt}$, so for sufficiently large $t$, $e^{-\beta t} \approx 0$ in the difference term. The equation becomes: $$T(t) = T_i e^{-kt} + T_f (1 - e^{-kt}) + \frac{k}{-\beta} (T_i - T_f) [0 - e^{-kt}]$$
5. Simplifying Case II further: $$T(t) = T_i e^{-kt} + T_f (1 - e^{-kt}) + \frac{k}{\beta} (T_i - T_f) e^{-kt}$$

**Reference:** start_page=10 end_page=10


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** Which set of factors, according to the lecture on heat transfer from a solid, determines the instantaneous rate of temperature change of an object cooling in an oven?

**Topics:** Newton's Law of Cooling, Convective Heat Transfer, Rate of Change

**Options:**
- Only the initial temperature of the object and the final temperature of the oven.
- ✅ The mass, specific heat, surface area of the object, the heat transfer coefficient, and the current temperature difference between the object and the oven.
- The volume of the object, the density of the oven air, and the duration of heating.
- The material's thermal conductivity, the oven's internal volume, and the object's color.

**Explanation:** The fundamental equation for the rate of temperature change is m C_p dT/dt = -h A_s (T - T_0). This shows that the rate dT/dt is directly dependent on the object's mass (m), specific heat (C_p), surface area (A_s), the heat transfer coefficient (h), and the instantaneous temperature difference between the object (T) and the oven (T_0).

**Reference:** start_page=1 end_page=2
### **Conceptual Question**
**Question:** In the box model for modeling pollution in a city, which of the following components represents a source of pollutant mass within the defined control volume?

**Topics:** Box Model, Mass Balance, Pollutant Sources

**Options:**
- The advective outflow of pollutant due to wind speed.
- The decay or destruction of pollutant by chemical reactions.
- ✅ The background concentration of pollutant entering with the wind and the pollutant generation rate per unit area within the box.
- The diffusion of pollutant across the top boundary of the box.

**Explanation:** The mass balance equation for the box model includes terms for pollutant inflow (m_in_dot = C_0 u WH) due to background concentration and wind, and pollutant generation (m_gen_dot = q_g LW) within the box. These are the primary source terms for pollutant mass.

**Reference:** start_page=4 end_page=4
### **Conceptual Question**
**Question:** Both the heat transfer from a solid and the box model for pollution result in first-order ordinary differential equations with exponential solutions. What is the primary significance of this exponential behavior in understanding these systems?

**Topics:** First-Order ODEs, Exponential Functions, System Dynamics

**Options:**
- It signifies that the systems will always exhibit oscillating behavior around a mean value.
- It indicates a constant rate of change regardless of the current state of the system.
- ✅ It describes how the system's quantity (temperature or concentration) gradually approaches a steady-state or equilibrium value over time.
- It implies that external forces are continuously acting to maintain a non-changing state.

**Explanation:** Exponential functions, particularly those involving e^(-kt), are characteristic solutions for first-order systems. They describe a transient response where the system property (temperature or concentration) changes over time at a rate proportional to the difference from its equilibrium or steady-state value, eventually reaching that state asymptotically.

**Reference:** start_page=2 end_page=5
