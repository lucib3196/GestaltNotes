# Lecture Source: me118_Lecture_01_22.pdf

## First-Order System Response to Sinusoidal Forcing

**Lecture Type:** derivation-heavy

### Summary
This lecture explores the methods for solving first-order linear differential equations, with a particular emphasis on systems subjected to various forcing functions, including constant, linearly increasing, exponential, and especially sinusoidal inputs. It covers the integrating factor method and the method of undetermined coefficients to derive the full solution, analyzing both the transient and steady-state behaviors of the system.

### Core Topics
- First-order linear differential equations
- Integrating factor method
- Method of undetermined coefficients
- Homogeneous solutions
- Particular solutions
- Transient response
- Steady-state response
- Sinusoidal forcing functions
- Complex exponential method
- Frequency response
- Phase shift

### Learning Objectives
1. Solve first-order linear differential equations using the integrating factor method.
2. Apply the method of undetermined coefficients to solve first-order linear differential equations.
3. Distinguish between homogeneous, particular, transient, and steady-state solutions.
4. Derive the total solution for a first-order system under sinusoidal forcing.
5. Analyze the amplitude and phase response of a first-order system to sinusoidal inputs.

### Assumed Prerequisites
- Basic calculus
- Introduction to differential equations
- Complex numbers


## Derivations

### **Formulation of Newton's Law of Cooling with Sinusoidal Ambient Temperature**
**Stub:** Express the ambient temperature $T_o(t)$ in a sinusoidal form and set up the differential equation for temperature $T(t)$.

**Steps:**
1. The governing differential equation for temperature change, likely representing Newton's Law of Cooling, is given by $$ \frac{dT}{dt} + kT = kT_o $$
2. Consider the scenario where the ambient temperature $T_o$ is a sinusoidal function of time, as illustrated by the graph showing $T_o(t)$ oscillating around a mean temperature $\bar{T_o}$ with an amplitude $T_a$ and a period of oscillation $T_p$.
3. The sinusoidal ambient temperature function can be expressed as $$ T_o(t) = \bar{T_o} + T_a \sin(\frac{2\pi}{T_p}t) $$
4. The angular frequency $\omega_o$ is defined in terms of the period $T_p$ as $$ \omega_o \equiv \frac{2\pi}{T_p} $$
5. Substituting the angular frequency into the expression for $T_o(t)$ yields the final form of the sinusoidal ambient temperature: $$ T_o(t) = \bar{T_o} + T_a \sin(\omega_o t) $$

**Reference:** start_page=0 end_page=0
### **Solution of First-Order Linear Differential Equation with Sinusoidal Forcing**
**Stub:** Derive the temperature T(t) as a function of time for a system described by dT/dt + kT = k(T_0 + T_a sin(wt)).

**Steps:**
1. The initial differential equation for temperature T is given as $$\frac{dT}{dt} + kT = k(T_0 + T_a \sin(\omega t))$$
2. The integrating factor is determined to be $$e^{kt}$$
3. Multiplying the differential equation by the integrating factor yields $$e^{kt} \frac{dT}{dt} + k e^{kt} T = k T_0 e^{kt} + k T_a \sin(\omega t) e^{kt}$$
4. The left-hand side is expressed as the derivative of a product: $$\frac{d}{dt} (T e^{kt}) = k T_0 e^{kt} + k T_a \sin(\omega t) e^{kt}$$
5. Integrating both sides, assuming an initial condition T(0)=T_0 for the constant term on the left, and evaluating the integral of the constant term: $$T(t) e^{kt} - T_0 = T_0 e^{kt} - T_0 + k T_a \int \sin(\omega t) e^{kt} dt$$
6. The integral $$I = \int e^{kt} \sin(\omega t) dt$$ is solved using integration by parts. First application: $$I = -\frac{e^{kt} \cos(\omega t)}{\omega} + \int \frac{k e^{kt} \cos(\omega t)}{\omega} dt$$
7. Second application of integration by parts to the remaining integral: $$I = -\frac{e^{kt} \cos(\omega t)}{\omega} + \frac{k}{\omega} \left( \frac{e^{kt} \sin(\omega t)}{\omega} - \frac{k}{\omega} \int e^{kt} \sin(\omega t) dt \right)$$
8. Rearranging terms to group I: $$I = -\frac{e^{kt} \cos(\omega t)}{\omega} + \frac{k e^{kt} \sin(\omega t)}{\omega^2} - \frac{k^2}{\omega^2} I$$
9. Factoring I: $$I \left(1 + \frac{k^2}{\omega^2}\right) = -\frac{e^{kt} \cos(\omega t)}{\omega} + \frac{k e^{kt} \sin(\omega t)}{\omega^2}$$
10. Solving for I: $$I = \frac{k e^{kt} \sin(\omega t) - \omega e^{kt} \cos(\omega t)}{k^2+\omega^2}$$
11. Substituting I back into the expression for T(t)e^(kt) and isolating T(t) to get the final solution, incorporating an initial temperature T_e and showing transient behavior: $$T(t) = T_0 + T_e - T_0 e^{-kt} + \frac{k T_a \omega}{k^2+\omega^2} e^{-kt} \cos(\omega t) + \frac{k T_a k}{k^2+\omega^2} e^{-kt} \sin(\omega t)$$

**Reference:** start_page=2 end_page=3
### **Solving First-Order Linear ODE using Undetermined Coefficients**
**Stub:** Derive the solution for a first-order linear non-homogeneous ordinary differential equation with a sinusoidal forcing term and an initial condition.

**Steps:**
1. The given non-homogeneous first-order linear ordinary differential equation is: $$\frac{dT}{dt} + kT = k T_a \sin(\omega t)$$
2. First, solve the homogeneous part of the ODE: $$\frac{dT}{dt} + kT = 0$$
3. The solution to the homogeneous equation is found by separation of variables or direct integration, leading to: $$T_H(t) = C_1 e^{-kt}$$ where $C_1$ is an arbitrary constant.
4. Assume a particular solution for the non-homogeneous equation in the form: $$T_P(t) = A + B \cos(\omega t) + C_2 \sin(\omega t)$$
5. Calculate the derivative of the particular solution: $$\frac{dT_P}{dt} = -B \omega \sin(\omega t) + C_2 \omega \cos(\omega t)$$
6. Substitute $T_P(t)$ and $\frac{dT_P}{dt}$ into the original non-homogeneous ODE: $$-B \omega \sin(\omega t) + C_2 \omega \cos(\omega t) + k(A + B \cos(\omega t) + C_2 \sin(\omega t)) = k T_a \sin(\omega t)$$
7. Group terms by constant, $\cos(\omega t)$, and $\sin(\omega t)$: $$kA + (C_2 \omega + kB) \cos(\omega t) + (-B \omega + kC_2) \sin(\omega t) = k T_a \sin(\omega t)$$
8. Equate coefficients on both sides of the equation:
9. For the constant term: $$kA = 0 \implies A = 0$$
10. For the $\cos(\omega t)$ term: $$C_2 \omega + kB = 0$$
11. For the $\sin(\omega t)$ term: $$-B \omega + kC_2 = k T_a$$
12. From the $\cos(\omega t)$ coefficient equation, express $B$ in terms of $C_2$: $$B = -\frac{C_2 \omega}{k}$$
13. Substitute this expression for $B$ into the $\sin(\omega t)$ coefficient equation: $$- \left(-\frac{C_2 \omega}{k}\right) \omega + kC_2 = k T_a$$
14. Simplify and solve for $C_2$: $$\frac{C_2 \omega^2}{k} + kC_2 = k T_a \implies C_2 \left(\frac{\omega^2 + k^2}{k}\right) = k T_a \implies C_2 = \frac{k^2 T_a}{k^2 + \omega^2}$$
15. Substitute $C_2$ back to find $B$: $$B = -\frac{1}{k} \left(\frac{k^2 T_a}{k^2 + \omega^2}\right) \omega = -\frac{k \omega T_a}{k^2 + \omega^2}$$
16. The particular solution, based on the derived coefficients (and noting the form presented in the lecture material on page 4 which includes a $T_0$ term not explicitly derived from the ODE as written on page 3): $$T_P(t) = T_0 + \frac{k^2 T_a}{k^2 + \omega^2} \sin(\omega t) - \frac{k \omega T_a}{k^2 + \omega^2} \cos(\omega t)$$
17. The general solution is the sum of the homogeneous and particular solutions: $$T(t) = T_H(t) + T_P(t)$$
18. Substituting the expressions for $T_H(t)$ and $T_P(t)$: $$T(t) = C_1 e^{-kt} + T_0 + \frac{k^2 T_a}{k^2 + \omega^2} \sin(\omega t) - \frac{k \omega T_a}{k^2 + \omega^2} \cos(\omega t)$$
19. Apply the initial condition $T(0) = T_c$ to find the constant $C_1$: $$T_c = C_1 e^0 + T_0 + \frac{k^2 T_a}{k^2 + \omega^2} \sin(0) - \frac{k \omega T_a}{k^2 + \omega^2} \cos(0)$$
20. Simplify the initial condition equation: $$T_c = C_1 + T_0 - \frac{k \omega T_a}{k^2 + \omega^2}$$
21. Solve for $C_1$: $$C_1 = (T_c - T_0) + \frac{k \omega T_a}{k^2 + \omega^2}$$
22. Substitute the expression for $C_1$ back into the general solution to obtain the final solution satisfying the initial condition: $$T(t) = \left( (T_c - T_0) + \frac{k \omega T_a}{k^2 + \omega^2} \right) e^{-kt} + T_0 + \frac{k^2 T_a}{k^2 + \omega^2} \sin(\omega t) - \frac{k \omega T_a}{k^2 + \omega^2} \cos(\omega t)$$

**Reference:** start_page=3 end_page=4
### **Temperature Response of a First-Order System to Sinusoidal Input**
**Stub:** Derive the steady-state temperature response T(t) for a system governed by a first-order linear differential equation with a complex exponential forcing function, leading to a phase-shifted sinusoidal output.

**Steps:**
1. Start with the first-order linear differential equation representing the system's temperature dynamics: $$dT/dt + kT = k(T₀ + Tₐe^{jωt})$$
2. Identify the integrating factor for the differential equation: $$e^{\int k dt} = e^{kt}$$
3. Multiply the differential equation by the integrating factor and integrate both sides: $$\int d(T e^{kt}) = \int k(T₀ + Tₐe^{jωt})e^{kt} dt$$
4. Perform the integration: $$T(t)e^{kt} - T(0) = k T₀ \frac{e^{kt}}{k} + k Tₐ \frac{e^{(k+jω)t}}{k+jω}$$
5. Rearrange to solve for T(t), including the transient and particular solutions: $$T(t) = T₀ + \frac{k Tₐ}{k+jω} e^{jωt} + \left(T(0) - T₀ - \frac{k Tₐ}{k+jω}\right)e^{-kt}$$
6. Simplify the complex coefficient $$\frac{1}{k+jω}$$ by multiplying the numerator and denominator by its conjugate: $$\frac{1}{k+jω} = \frac{k-jω}{(k+jω)(k-jω)} = \frac{k-jω}{k^2+ω^2}$$
7. Substitute the simplified complex coefficient into the particular solution. As t approaches infinity, the transient term $$\left(T(0) - T₀ - \frac{k Tₐ}{k+jω}\right)e^{-kt}$$ approaches zero, leaving the steady-state solution: $$T(t)_{ss} = T₀ + \frac{k Tₐ}{k^2+ω^2}(k-jω)e^{jωt}$$
8. To express the steady-state solution in a real sinusoidal form, we consider the real part of the complex exponential response. Using the trigonometric identity $k \sin(\omega t) - \omega \cos(\omega t) = \sqrt{k^2+\omega^2} \sin(\omega t - \phi)$, where $$\phi = \arctan(\omega/k)$$ (from $k = C \cos \phi$ and $$\omega = C \sin \phi$$), we can transform the steady-state term.
9. The final steady-state temperature response, expressed as a real sinusoidal function with a phase shift, is: $$T(t) = T₀ + \frac{k Tₐ}{\sqrt{k^2+ω^2}} \sin(ωt - \phi)$$
10. Analyze the system's amplitude and phase response at different frequencies: At $$\omega = 0$$ (DC), the phase $$\phi = 0$$ and the amplitude factor $$\frac{k}{\sqrt{k^2+ω^2}} = 1$$. At $$\omega = k$$, the phase $$\phi = \pi/4$$ and the amplitude factor $$\frac{k}{\sqrt{k^2+ω^2}} = \frac{1}{\sqrt{2}}$$. As $$\omega \to \infty$$, the phase $$\phi \to \pi/2$$ and the amplitude factor $$\frac{k}{\sqrt{k^2+ω^2}} \to 0$$.

**Reference:** start_page=5 end_page=8
### **Trigonometric Identity for Phase Shift**
**Stub:** Derive the transformation of a linear combination of sine and cosine functions into a single phase-shifted sine function: $k \sin(\omega t) - \omega \cos(\omega t) = C \sin(\omega t - \phi)$.

**Steps:**
1. Start with the linear combination of sine and cosine: $$k \sin(\omega t) - \omega \cos(\omega t)$$
2. Define new variables C and $$\phi$$ such that $k = C \cos \phi$$ and $$\omega = C \sin \phi$$.
3. From these definitions, we can find C and $$\phi$$: $$C = \sqrt{k^2+\omega^2}$$ and $$\tan \phi = \omega/k \implies \phi = \arctan(\omega/k)$$
4. Substitute the definitions of k and $$\omega$$ into the original expression: $$(C \cos \phi) \sin(\omega t) - (C \sin \phi) \cos(\omega t)$$
5. Factor out C: $$C (\cos \phi \sin(\omega t) - \sin \phi \cos(\omega t))$$
6. Apply the trigonometric identity for the sine of a difference, $$\sin(A-B) = \sin A \cos B - \cos A \sin B$$: $$C \sin(\omega t - \phi)$$

**Reference:** start_page=7 end_page=7


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** What physical phenomenon does the differential equation dT/dt + kT = kTo(t) describe, and what do the parameters k and To(t) represent?

**Topics:** Newton's Law of Cooling, Heat Transfer, System Parameters

**Options:**
- Describes fluid flow; k is viscosity, To(t) is flow rate.
- Describes chemical reaction kinetics; k is reaction rate, To(t) is reactant concentration.
- ✅ Describes the heating or cooling of an object; k is the thermal coupling constant, To(t) is the ambient temperature.
- Describes electrical circuit behavior; k is resistance, To(t) is voltage.

**Explanation:** The equation is a form of Newton's Law of Cooling (or heating). dT/dt is the rate of temperature change of an object, k represents how strongly the object's temperature is coupled to the ambient temperature (thermal coupling constant), and To(t) is the time-varying ambient temperature.

**Reference:** start_page=1 end_page=1
### **Conceptual Question**
**Question:** When the ambient temperature To(t) is a sinusoidal function, To_bar + Ta sin(ω0t), the general solution for the object's temperature T(t) consists of two main parts. What are these parts and their characteristics?

**Topics:** Transient Response, Steady-State Response, Sinusoidal Forcing

**Options:**
- A constantly increasing term and a decaying exponential term.
- ✅ A homogeneous solution that decays over time (transient) and a particular solution that oscillates with the same frequency as the ambient temperature (steady-state).
- A homogeneous solution that oscillates and a particular solution that remains constant.
- Two exponential terms, one increasing and one decreasing.

**Explanation:** The general solution for T(t) is the sum of a homogeneous solution and a particular solution. The homogeneous solution (C e^(-kt)) represents the transient response that decays to zero over time. The particular solution, for a sinusoidal input, is a steady-state sinusoidal oscillation at the same frequency as the ambient temperature, but potentially with a different amplitude and a phase shift.

**Reference:** start_page=5 end_page=7
### **Conceptual Question**
**Question:** Based on the frequency response curve shown in the lecture, what happens to the amplitude of the object's temperature oscillations relative to the ambient temperature oscillations as the frequency ω0 of the ambient temperature increases significantly?

**Topics:** Frequency Response, Amplitude Attenuation, Phase Shift

**Options:**
- The amplitude of the object's temperature oscillations increases and leads the ambient temperature.
- ✅ The amplitude of the object's temperature oscillations decreases and lags the ambient temperature by approximately π/2.
- The amplitude of the object's temperature oscillations remains constant, but the phase shift becomes zero.
- The amplitude of the object's temperature oscillations matches the ambient temperature perfectly.

**Explanation:** As the frequency ω0 of the ambient temperature oscillation increases significantly (approaching infinity), the amplitude ratio k / sqrt(k^2 + ω0^2) approaches 0, indicating that the object's temperature oscillations are heavily attenuated. Simultaneously, the phase shift φ = tan^(-1)(ω0/k) approaches π/2, meaning the object's temperature lags the ambient temperature by approximately π/2.

**Reference:** start_page=8 end_page=8
