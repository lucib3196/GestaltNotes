# Lecture Source: me118_Lecture_01_13.pdf

## Dynamical Systems Analysis and Physical Modeling with Differential Equations

**Lecture Type:** mixed

### Summary
This lecture introduces the analysis of one-dimensional autonomous dynamical systems, focusing on identifying equilibrium points and determining their stability using phase line diagrams and linearization. It then applies differential equations to model various physical phenomena, including the draining of a tank based on Bernoulli's principle, and the motion of a particle under gravity, considering both free fall and movement in a resistive medium, culminating in the concept of terminal velocity.

### Core Topics
- Equilibrium points
- Stability analysis
- Phase line diagrams
- Linearization of dynamical systems
- Tank draining problem
- Bernoulli's equation
- Motion of a particle
- Free fall
- Linear drag
- Terminal velocity

### Learning Objectives
1. Analyze the stability of equilibrium points for one-dimensional autonomous differential equations
2. Interpret phase line diagrams to understand system behavior
3. Apply linearization techniques to determine stability
4. Formulate differential equations to model physical systems like a draining tank
5. Solve differential equations for particle motion under gravity
6. Derive the velocity profile for a particle moving in a resistive medium
7. Define and calculate terminal velocity

### Assumed Prerequisites
- Basic calculus
- Basic differential equations
- Newtonian mechanics


## Derivations

### **Linearization of a Nonlinear Ordinary Differential Equation**
**Stub:** Linearize a given nonlinear ordinary differential equation around its equilibrium points to analyze stability.

**Steps:**
1. Given the nonlinear ODE: $$ẋ = (2-x)(x+1)(x-4)$$
2. Define the right-hand side as a function: $$f(x) = (2-x)(x+1)(x-4)$$
3. Calculate the derivative of f(x): $$f'(x) = -(x+1)(x-4) + (2-x)(x-4) + (2-x)(x+1)$$
4. Apply the Taylor series approximation for linearization around an equilibrium point $$x_{eq}$$: $$f(x) ≈ f(x_{eq}) + f'(x_{eq})(x - x_{eq})$$
5. For an equilibrium point, $$f(x_{eq}) = 0$$. Thus, $$dx/dt ≈ f'(x_{eq})(x - x_{eq})$$.
6. Consider the equilibrium point $$x_{eq} = -1$$.
7. Evaluate the derivative at $$x_{eq} = -1$$: $$f'(-1) = -( -1+1 )(-1-4) + (2-(-1))(-1-4) + (2-(-1))(-1+1) = 0 + (3)(-5) + 0 = -15$$
8. Substitute into the linearized equation: $$dx/dt = -15(x - (-1))$$
9. Define the deviation variable $$~x = x - (-1)$$ from the equilibrium point. Then, $$d~x/dt = dx/dt$$.
10. The linearized ODE becomes: $$d~x/dt = -15~x$$
11. The solution is an exponential decay: $$~x(t) = e^{-15t}~x(0)$$
12. As $$t → ∞$$, $$~x(t) → 0$$, implying $$x → -1$$. The equilibrium point $$x = -1$$ is stable.
13. Consider another equilibrium point $$x_{eq} = 2$$.
14. Evaluate the derivative at $$x_{eq} = 2$$: $$f'(2) = -(2+1)(2-4) + (2-2)(2-4) + (2-2)(2+1) = -(3)(-2) + 0 + 0 = 6$$
15. Substitute into the linearized equation: $$dx/dt = 6(x - 2)$$
16. Define the deviation variable $$~x = x - 2$$ from the equilibrium point. Then, $$d~x/dt = dx/dt$$.
17. The linearized ODE becomes: $$d~x/dt = 6~x$$
18. The solution is an exponential growth: $$~x(t) = ~x(0)e^{6t}$$
19. As $$t → ∞$$, $$~x(t)$$ diverges, implying $$x$$ moves away from $$2$$. The equilibrium point $$x = 2$$ is unstable.

**Reference:** start_page=2 end_page=2
### **Dynamics of a Draining Tank and Steady-State Height**
**Stub:** Derive the differential equation governing the height of liquid in a tank with inflow and an outflow orifice, and determine the steady-state height.

**Steps:**
1. Apply the principle of conservation of mass to the tank system: $$ṁ_{in} - ṁ_{out} = dm_{tank}/dt$$
2. Relate mass flow rate (ṁ) to volume flow rate (V̇) using density (ρ): $$m = ρV$$ so $$ṁ = ρV̇$$
3. The inflow volume rate is given as $$V̇_{in}$$.
4. The outflow volume rate through an orifice is $$V̇_{out} = A_o V_{velocity}$$, where $$A_o$$ is the orifice area.
5. The outflow velocity is given by Torricelli's law, a consequence of Bernoulli's equation: $$V_{velocity} = \sqrt{2gh}$$, where $$h$$ is the liquid height.
6. The volume of liquid in the tank is $$V_{tank} = A_t h$$, where $$A_t$$ is the tank's cross-sectional area.
7. Substitute these expressions into the conservation of mass equation, assuming constant density ρ: $$ρV̇_{in} - ρA_o\sqrt{2gh} = d/dt (ρA_t h)$$
8. Divide by ρ (assuming constant density for incompressible fluid): $$V̇_{in} - A_o\sqrt{2gh} = A_t dh/dt$$
9. Rearrange to find the differential equation for the height $$h$$: $$dh/dt = (V̇_{in} / A_t) - (A_o\sqrt{2g} / A_t)\sqrt{h}$$
10. Define constants for simplification: $$\alpha = V̇_{in} / A_t$$ and $$\beta = A_o\sqrt{2g} / A_t$$
11. The differential equation for height becomes: $$dh/dt = \alpha - \beta\sqrt{h}$$
12. To find the steady-state height, set $$dh/dt = 0$$ (no change in height over time).
13. This yields: $$\alpha - \beta\sqrt{h} = 0$$
14. Solve for $$h$$: $$\sqrt{h} = \alpha / \beta$$
15. Therefore, the steady-state height is: $$h = (\alpha / \beta)^2$$
16. Substitute back the definitions of $$\alpha$$ and $$\beta$$: $$h = \left( \frac{V̇_{in} / A_t}{A_o\sqrt{2g} / A_t} \right)^2$$
17. Simplify the expression for steady-state height: $$h = \left( \frac{V̇_{in}}{A_o\sqrt{2g}} \right)^2$$ which can also be written as $$h = \frac{(V̇_{in})^2}{A_o^2 \cdot 2g}$$

**Reference:** start_page=3 end_page=3
### **Kinematic Equations for Constant Acceleration (Free Fall)**
**Stub:** Derivation of velocity and position equations for a particle under constant gravitational acceleration: $v(t) = v_0 + gt$ and $x = v_0 t + \frac{1}{2}gt^2$.

**Steps:**
1. The definitions of velocity and acceleration are: $v = \frac{dx}{dt}$ and $a = \frac{dv}{dt}$.
2. From the free-body diagram of a particle of mass $m$ under gravity $g$ (downwards), the net force in the y-direction is $\sum F_y = ma$.
3. Since the only force is gravity, $ma = mg$.
4. This implies that the acceleration of the particle is $a = g$.
5. Substitute $a=g$ into the acceleration definition: $\frac{dv}{dt} = g$.
6. Integrate both sides with respect to time, from initial velocity $v_0$ to final velocity $v$ and from initial time $0$ to final time $t$: $\int_{v_0}^{v} dv = \int_{0}^{t} g dt$.
7. Evaluating the integrals gives $v - v_0 = gt$.
8. Rearranging the terms yields the velocity as a function of time: $v(t) = v_0 + gt$.
9. Now, substitute the derived velocity equation into the definition of velocity: $\frac{dx}{dt} = v = v_0 + gt$.
10. Integrate both sides with respect to time, from initial position $x_0=0$ to final position $x$ and from initial time $0$ to final time $t$: $\int_{0}^{x} dx = \int_{0}^{t} (v_0 + gt) dt$.
11. Evaluating the integrals gives $x - 0 = v_0 t + \frac{gt^2}{2} \Big|_0^t$.
12. This simplifies to the position as a function of time: $x = v_0 t + \frac{gt^2}{2}$.

**Reference:** start_page=4 end_page=4
### **Motion of a Particle Projected Upwards in a Resistive Medium**
**Stub:** Derivation of the velocity v(t) for a particle projected upwards in a medium with linear drag.

**Steps:**
1. Applying Newton's second law, the net force on the particle is given by the sum of gravitational force and resistive force: $$m\frac{dv}{dt} = -mg - F_R$$
2. Assuming a linear drag force, $F_R = bv$, where $b$ is the drag coefficient: $$m\frac{dv}{dt} = -mg - bv$$
3. Factor out the negative sign: $$m\frac{dv}{dt} = -(mg + bv)$$
4. Divide by $m$ to isolate the acceleration term: $$\frac{dv}{dt} = -\left(g + \frac{b}{m}v\right)$$
5. Separate variables for integration: $$\frac{dv}{g + \frac{b}{m}v} = -dt$$
6. Integrate both sides with limits from $v_0$ to $v$ for velocity and from $0$ to $t$ for time: $$\int_{v_0}^{v} \frac{dv}{g + \frac{b}{m}v} = \int_{0}^{t} -dt$$
7. Perform the integration. The left side integrates to $\frac{1}{b/m}\ln\left(g + \frac{b}{m}v\right)$ and the right side integrates to $-t$: $$\frac{\ln\left(g + \frac{b}{m}v\right)\Big|_{v_0}^{v}}{b/m} = -t$$
8. Apply the limits of integration for the logarithm: $$\ln\left(\frac{g + \frac{b}{m}v}{g + \frac{b}{m}v_0}\right) = -\frac{b}{m}t$$
9. Exponentiate both sides to remove the natural logarithm: $$\frac{g + \frac{b}{m}v}{g + \frac{b}{m}v_0} = e^{-\frac{b}{m}t}$$
10. Rearrange the equation to solve for $v$: $$g + \frac{b}{m}v = \left(g + \frac{b}{m}v_0\right)e^{-\frac{b}{m}t}$$
11. Isolate $v$: $$v = \frac{m}{b}\left(-g + \left(g + \frac{b}{m}v_0\right)e^{-\frac{b}{m}t}\right)$$

**Reference:** start_page=6 end_page=6
### **Solution of First-Order Non-Linear ODE for h(t)**
**Stub:** Derive the implicit solution for h(t) from dh/dt = alpha - beta*sqrt(h).

**Steps:**
1. State the initial differential equation: $$\frac{dh}{dt} = \alpha - \beta\sqrt{h}$$
2. Recognize the form f(h)g(t) with $$f(h) = \alpha - \beta\sqrt{h}$$ and $$g(t) = 1$$
3. Separate variables and integrate both sides: $$\int_{h_0}^{h} \frac{dh}{\alpha - \beta\sqrt{h}} = \int_{0}^{t} dt$$
4. Introduce a substitution to simplify the integral on the left side: $$Let\ u = \frac{\beta}{\alpha}\sqrt{h}$$
5. From the substitution, express $$\sqrt{h}$$ and $$h$$ in terms of $$u$$: $$\sqrt{h} = \frac{\alpha}{\beta}u$$ and $$h = \left(\frac{\alpha}{\beta}\right)^2 u^2$$
6. Differentiate $$h$$ with respect to $$u$$ to find $$dh$$: $$dh = 2 \left(\frac{\alpha}{\beta}\right)^2 u\ du$$
7. Substitute $$h$$ and $$dh$$ into the integral: $$\int \frac{2 \left(\frac{\alpha}{\beta}\right)^2 u\ du}{\alpha - \beta\left(\frac{\alpha}{\beta}\right)u} = \int \frac{2 \frac{\alpha^2}{\beta^2} u\ du}{\alpha - \alpha u} = \int \frac{2 \frac{\alpha^2}{\beta^2} u\ du}{\alpha(1-u)}$$
8. Simplify the integrand: $$\frac{2\alpha}{\beta^2} \int \frac{u}{1-u}\ du = t$$
9. Determine the limits of integration for $$u$$: When $$h = h_0$$, $$u = \frac{\beta}{\alpha}\sqrt{h_0}$$; When $$h = h$$, $$u = \frac{\beta}{\alpha}\sqrt{h}$$
10. Set up the definite integral with the new limits: $$\frac{2\alpha}{\beta^2} \int_{\frac{\beta}{\alpha}\sqrt{h_0}}^{\frac{\beta}{\alpha}\sqrt{h}} \frac{u}{1-u}\ du = t$$
11. Evaluate the indefinite integral of $$u/(1-u)$$: $$\int \frac{u}{1-u}\ du = -\int \frac{u}{u-1}\ du = -\int \left(\frac{u-1+1}{u-1}\right)\ du = -\int \left(1 + \frac{1}{u-1}\right)\ du$$
12. Complete the integration: $$= -(u + \ln|u-1|)$$
13. Apply the limits of integration to the result: $$-\frac{2\alpha}{\beta^2} \left[u + \ln|u-1|\right]_{\frac{\beta}{\alpha}\sqrt{h_0}}^{\frac{\beta}{\alpha}\sqrt{h}} = t$$
14. Substitute the limits and rearrange the terms: $$\left(\frac{\beta}{\alpha}\sqrt{h} - \frac{\beta}{\alpha}\sqrt{h_0}\right) + \left(\ln\left|\frac{\beta}{\alpha}\sqrt{h}-1\right| - \ln\left|\frac{\beta}{\alpha}\sqrt{h_0}-1\right|\right) = -\frac{\beta^2}{2\alpha}t$$
15. Combine the logarithmic terms: $$\frac{\beta}{\alpha}(\sqrt{h} - \sqrt{h_0}) + \ln\left(\frac{|\frac{\beta}{\alpha}\sqrt{h}-1|}{|\frac{\beta}{\alpha}\sqrt{h_0}-1|}\right) = -\frac{\beta^2}{2\alpha}t$$

**Reference:** start_page=4 end_page=7
### **Solution of a Definite Integral and Algebraic Rearrangement**
**Stub:** Derivation of an implicit relationship between variables $h$, $h_0$, and $t$ from a definite integral.

**Steps:**
1. The derivation begins with the indefinite integral: $$\int \frac{u}{1-u} du$$
2. Rewrite the denominator by factoring out -1: $$= -\int \frac{u}{u-1} du$$
3. Manipulate the numerator to facilitate integration by adding and subtracting 1: $$= -\int \left(\frac{u-1+1}{u-1}\right) du$$
4. Split the fraction into two terms: $$= -\int \left(1 + \frac{1}{u-1}\right) du$$
5. Perform the integration: $$= -(u + \ln(u-1))$$
6. The integrated expression is then shown as part of a definite integral evaluation, with a coefficient and limits of integration related to physical parameters $h$ and $h_0$, set equal to $t$: $$-\frac{2\alpha}{\beta^2} (u + \ln(u-1)) \Bigg|_{\frac{\beta}{\alpha}\sqrt{h_0}}^{\frac{\beta}{\alpha}\sqrt{h}} = t$$
7. Evaluate the expression at the upper and lower limits, and rearrange the terms to solve for $t$: $$\left(\frac{\beta}{\alpha}\sqrt{h} - \frac{\beta}{\alpha}\sqrt{h_0}\right) + \ln\left(\frac{\frac{\beta}{\alpha}\sqrt{h}-1}{\frac{\beta}{\alpha}\sqrt{h_0}-1}\right) = -\frac{\beta^2}{2\alpha} t$$

**Reference:** start_page=7 end_page=7


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** Given a one-dimensional dynamical system x_dot = f(x), how can the stability of a fixed point x_eq be determined using the derivative of f(x) at that point?

**Topics:** Fixed points, Stability analysis, Linearization

**Options:**
- ✅ If f'(x_eq) < 0, the fixed point is stable.
- If f'(x_eq) > 0, the fixed point is stable.
- If f'(x_eq) = 0, the fixed point is stable.
- Stability cannot be determined from f'(x_eq) alone; higher-order derivatives are always required.

**Explanation:** The stability of a fixed point x_eq for a 1D system x_dot = f(x) is determined by the sign of f'(x_eq). If f'(x_eq) < 0, small perturbations from x_eq decay, making it a stable fixed point. If f'(x_eq) > 0, small perturbations grow, making it unstable. If f'(x_eq) = 0, higher-order terms are needed.

**Reference:** start_page=1 end_page=2
### **Conceptual Question**
**Question:** For the tank draining problem described in the lecture, what condition must be met to find the equilibrium height (h_eq) of the liquid in the tank?

**Topics:** Differential equations, Equilibrium points, Tank draining

**Options:**
- The inflow rate (V_in) must be zero.
- The outflow rate (A_0 * sqrt(2gh)) must be zero.
- ✅ The rate of change of height (dh/dt) must be zero.
- The tank must be completely empty (h=0).

**Explanation:** An equilibrium height occurs when the net change in liquid volume over time is zero, meaning the inflow rate equals the outflow rate. Mathematically, this corresponds to setting the derivative of height with respect to time, dh/dt, to zero.

**Reference:** start_page=3 end_page=3
### **Conceptual Question**
**Question:** In the motion of a particle projected upwards in a resistive medium (linear drag), what does the terminal velocity (v_t) represent, and how is it related to the forces acting on the particle?

**Topics:** Resistive forces, Terminal velocity, Newton's laws

**Options:**
- The initial velocity of the particle, where drag is negligible.
- ✅ The maximum velocity the particle can achieve when falling, where drag balances gravity.
- The velocity at which the particle instantaneously stops before falling.
- A theoretical value that is never actually reached due to continuous acceleration.

**Explanation:** Terminal velocity (v_t) is the constant speed that a freely falling object eventually reaches when the resistance of the medium through which it is falling prevents further acceleration. At terminal velocity, the gravitational force (mg) is perfectly balanced by the drag force (bv), resulting in zero net force and thus zero acceleration.

**Reference:** start_page=6 end_page=7
