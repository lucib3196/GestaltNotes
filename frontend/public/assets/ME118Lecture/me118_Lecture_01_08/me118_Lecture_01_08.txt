# Lecture Source: me118_Lecture_01_08.pdf

## Population Dynamics: Difference and Differential Equations with Equilibrium Analysis

**Lecture Type:** mixed

### Summary
This lecture introduces students to the fundamental concepts of population dynamics using both first-order difference equations and continuous differential equations. It covers the identification and analysis of equilibrium points, including their stability, through graphical methods and linearization techniques, with a focus on simple population growth models.

### Core Topics
- First-order difference equations
- Equilibrium points
- Continuous population models
- Exponential growth model
- Logistic growth model
- Linearization
- Stability of equilibrium points
- Phase diagrams

### Learning Objectives
1. Analyze the behavior of first-order difference equations using graphical iterations
2. Identify equilibrium points for both difference and differential equations
3. Derive solutions for basic continuous population growth models
4. Apply linearization to determine the stability of equilibrium points
5. Interpret the dynamics of population models based on phase diagrams

### Assumed Prerequisites
- Basic calculus (differentiation, integration)
- Algebra (solving equations, quadratic formula)
- Graphing functions


## Derivations

### **Analysis of Real Roots for a Cubic Equation**
**Stub:** Determine the number of real roots for an equation of the form $x(x^2 - rx + A) = 0$ based on parameters $r$ and $A$.

**Steps:**
1. The problem considers finding the roots of a polynomial equation, implicitly $x(x^2 - rx + A) = 0$, given the mention of $x=0$ as a root and the quadratic factor.
2. One root is immediately identifiable as $x=0$.
3. The other roots are found by solving the quadratic equation $x^2 - rx + A = 0$.
4. Applying the quadratic formula, the solutions for $x$ are given by: $$x = \frac{r \pm \sqrt{r^2 - 4A}}{2}$$
5. The number of real roots depends on the discriminant of the quadratic factor, $\Delta = r^2 - 4A$.
6. Case 1: If $r^2 > 4A$ (or $r > \sqrt{2A}$), the discriminant $\Delta > 0$. This yields two distinct real roots from the quadratic formula. Combined with $x=0$, the cubic equation has three distinct real roots: $$x=0, \frac{r \pm \sqrt{r^2 - 4A}}{2}$$
7. Case 2: If $r^2 < 4A$, the discriminant $\Delta < 0$. This means the quadratic factor has two complex conjugate roots. In this scenario, the only real root of the cubic equation is $x=0$.
8. The accompanying graph visually illustrates an iterative process (e.g., fixed-point iteration $x_{n+1} = f(x_n)$), showing convergence to a fixed point. The curve labeled $r^2 < 4A$ suggests the behavior of such a function, possibly demonstrating the convergence to the single real root $x=0$ when the quadratic factor yields no additional real roots.

**Reference:** start_page=2 end_page=2
### **Derivation of the Continuous Population Growth Model**
**Stub:** Derive the differential equation for continuous population growth with a constant per capita growth rate: $\frac{dN}{dt} = rN(t)$

**Steps:**
1. Let $N(t)$ be the population at time $t$.
2. The change in population over time $\Delta t$ is $N(t + \Delta t) - N(t)$.
3. The rate of population change is $\frac{N(t + \Delta t) - N(t)}{\Delta t}$.
4. The per capita growth change is $\frac{N(t + \Delta t) - N(t)}{\Delta t \ N(t)}$.
5. Consider an example case where the per capita change is constant, denoted by $r$: $$\frac{N(t + \Delta t) - N(t)}{\Delta t \ N(t)} = r \quad (\text{const})$$
6. Take the limit as $\Delta t \to 0$ to define the derivative: $$\lim_{\Delta t \to 0} \frac{N(t + \Delta t) - N(t)}{\Delta t} \frac{1}{N(t)} = r$$
7. This limit defines the derivative $\frac{dN}{dt}$: $$\frac{dN}{dt} \frac{1}{N(t)} = r$$
8. Rearranging the equation yields the continuous population growth model: $$\frac{dN}{dt} = rN(t)$$

**Reference:** start_page=2 end_page=2
### **Derivation of Exponential Growth/Decay Equation**
**Stub:** Derive the equation $N(t) = N_0 e^{rt}$ from the differential equation $\frac{dN}{dt} = rN(t)$.

**Steps:**
1. Start with the differential equation for population change: $$\frac{dN}{dt} = rN(t)$$ with initial condition $N(0) = N_0$.
2. Separate the variables: $$\frac{dN}{N} = r dt$$
3. Integrate both sides from initial conditions ($N_0$ at $t=0$) to $N(t)$ at time $t$: $$\int_{N_0}^{N(t)} \frac{dN}{N} = \int_0^t r dt$$
4. Evaluate the definite integrals: $$\ln N \Big|_{N_0}^{N(t)} = rt$$ which simplifies to: $$\ln N(t) - \ln N_0 = rt$$
5. Apply logarithm properties to combine terms: $$\ln \frac{N(t)}{N_0} = rt$$
6. Exponentiate both sides to solve for $N(t)$: $$N(t) = N_0 e^{rt}$$

**Reference:** start_page=4 end_page=4
### **Definition of Time Constant in Exponential Decay**
**Stub:** Define the time constant $\tau$ and its relation to the exponential decay equation.

**Steps:**
1. For exponential decay, the rate constant $r$ is negative ($r < 0$) and its units are $[r] = 1/s$.
2. The time constant $\tau$ is defined as the reciprocal of the absolute value of the rate constant: $$\tau = \frac{1}{|r|}$$
3. Substituting $r = -1/\tau$ (for decay) into the exponential equation $N(t) = N_0 e^{rt}$ yields the decay form: $$N(t) = N_0 e^{-t/\tau}$$
4. This form illustrates how the population $N(t)$ decreases to $N_0 e^{-1}$ after one time constant.

**Reference:** start_page=4 end_page=4
### **Solution to a Logistic Differential Equation**
**Stub:** Derive the implicit solution for N(t) from the logistic differential equation dN/dt = (a-bN)N.

**Steps:**
1. The derivation begins with the logistic differential equation: $$\frac{dN}{dt} = (a-bN)N$$
2. Separate the variables to prepare for integration: $$\frac{dN}{N(a-bN)} = dt$$
3. Integrate both sides of the equation from initial conditions $N_0$ at $t=0$ to $N$ at time $t$: $$\int_{N_0}^{N} \frac{dN}{N(a-bN)} = \int_{0}^{t} dt$$
4. To evaluate the left-hand side integral, we use partial fraction decomposition: $$\frac{1}{N(a-bN)} = \frac{C}{N} + \frac{D}{a-bN}$$
5. Multiply by the common denominator $N(a-bN)$ to find the constants C and D: $$1 = C(a-bN) + DN$$
6. To find C, set $N=0$: $$1 = C(a-b(0)) + D(0) \Rightarrow 1 = Ca \Rightarrow C = \frac{1}{a}$$
7. To find D, set $a-bN=0$, which implies $N=\frac{a}{b}$: $$1 = C(a-b\frac{a}{b}) + D\frac{a}{b} \Rightarrow 1 = D\frac{a}{b} \Rightarrow D = \frac{b}{a}$$
8. Substitute the values of C and D back into the integral expression: $$\int_{N_0}^{N} \left(\frac{1}{aN} + \frac{b}{a(a-bN)}\right) dN = \int_{0}^{t} dt$$
9. Evaluate the integrals: $$\frac{1}{a} [\ln|N|]_{N_0}^{N} + \frac{b}{a} \left[\frac{\ln|a-bN|}{-b}\right]_{N_0}^{N} = [t]_{0}^{t}$$
10. Apply the limits of integration: $$\frac{1}{a} (\ln N - \ln N_0) - \frac{1}{a} (\ln(a-bN) - \ln(a-bN_0)) = t$$
11. Combine the logarithmic terms using logarithm properties: $$\frac{1}{a} \ln \left(\frac{N}{N_0}\right) - \frac{1}{a} \ln \left(\frac{a-bN}{a-bN_0}\right) = t$$

**Reference:** start_page=4 end_page=4
### **Derivation of Population Growth Model Solution**
**Stub:** Derive the explicit expression for N(t) in a population growth model.

**Steps:**
1. The initial equation is given as: $$\ln\left(\frac{N/N_0}{(a-bN)/(a-bN_0)}\right) = at$$
2. Rearranging the terms inside the logarithm: $$\ln\left[\left(\frac{N}{a-bN}\right)\left(\frac{a-bN_0}{N_0}\right)\right] = at$$
3. Exponentiating both sides and isolating the term involving N: $$\frac{N}{a-bN} = \left(\frac{N_0}{a-bN_0}\right)e^{at}$$
4. Defining $\alpha = \frac{N_0}{a-bN_0}$: $$\frac{N}{a-bN} = \alpha e^{at}$$
5. Multiplying both sides by $(a-bN)$ and expanding: $$N = a\alpha e^{at} - bN\alpha e^{at}$$
6. Collecting terms containing N on one side: $$N(1 + b\alpha e^{at}) = a\alpha e^{at}$$
7. Solving for N(t): $$N(t) = \frac{a\alpha e^{at}}{1 + b\alpha e^{at}}$$

**Reference:** start_page=5 end_page=5
### **Equilibrium Points of a Logistic Growth Model**
**Stub:** Derive the equilibrium points and their stability for the differential equation describing population dynamics.

**Steps:**
1. Start with the given differential equation for population N over time t, where a and b are positive constants: $$\frac{dN}{dt} = (a-bN)N = aN - bN^2$$
2. To find the equilibrium values of N, set the rate of change of N with respect to t to zero: $$\frac{dN}{dt} = 0$$
3. Substitute the expression for $$\frac{dN}{dt}$$ into the equilibrium condition: $$(a-bN)N = 0$$
4. Solve the algebraic equation for N, yielding two equilibrium points: $$N=0$$ or $$N=rac{a}{b}$$
5. Based on the phase line analysis (as illustrated by the graph of $$\frac{dN}{dt}$$ vs N), we can determine the stability of each equilibrium point.
6. The equilibrium point $$N=0$$ is an unstable equilibrium point.
7. The equilibrium point $$N=rac{a}{b}$$ is a stable equilibrium.

**Reference:** start_page=6 end_page=6
### **Linearization of a Differential Equation around an Equilibrium Point**
**Stub:** Derive the linearized form of $dN/dt = f(N)$ about the equilibrium point $N=0$ and analyze its stability.

**Steps:**
1. The general Taylor series expansion of a function $f(x)$ about $x=a$ is given by:$$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \frac{f'''(a)}{3!}(x-a)^3 + \dots$$
2. The linear approximation of $f(x)$ about $x=a$ is:$$f(x) \approx f(a) + f'(a)(x-a)$$
3. Consider the differential equation:$$\frac{dN}{dt} = f(N)$$where $f(N) = (a-bN)N = aN - bN^2$.
4. Calculate the first derivative of $f(N)$:$$f'(N) = a - 2bN$$
5. Consider the equilibrium point $N=0$. Evaluate $f(N)$ and $f'(N)$ at $N=0$:$$f(0) = (a-b(0))(0) = 0$$$$f'(0) = a - 2b(0) = a$$
6. Apply the linear approximation for $f(N)$ around $N=0$:$$f(N) \approx f(0) + f'(0)(N-0)$$
7. Substitute the evaluated values:$$f(N) \approx 0 + a(N-0) \implies f(N) \approx aN$$
8. Substitute the linearized $f(N)$ back into the differential equation:$$\frac{dN}{dt} = aN$$
9. Solve the linear ordinary differential equation:$$N(t) = N_0 e^{at}$$
10. Conclusion: If $a > 0$, $N(t)$ increases with $t$, which implies the equilibrium point $N=0$ is unstable.

**Reference:** start_page=7 end_page=7
### **Stability Analysis of an Equilibrium Point via Linearization**
**Stub:** Derivation showing that $N = a/b$ is a stable equilibrium point for a differential equation $dN/dt = f(N)$ through linearization.

**Steps:**
1. Given an equilibrium point $N = a/b$ for a system $dN/dt = f(N)$.
2. At the equilibrium point, $f(a/b) = 0$.
3. Calculate the derivative of $f(N)$ evaluated at the equilibrium point: $f'(a/b) = a - (2b)(a/b) = a - 2a = -a$.
4. Linearize $f(N)$ around $N = a/b$ using a Taylor expansion: $$f(N) = f(a/b) + f'(a/b)(N - a/b)$$
5. Substitute the values of $f(a/b)$ and $f'(a/b)$: $$f(N) = 0 + (-a)(N - a/b)$$
6. This simplifies to: $$f(N) = -a(N - a/b)$$
7. The linearized differential equation is then: $$\frac{dN}{dt} \approx -a\left(N - \frac{a}{b}\right)$$
8. Introduce a perturbation variable $\tilde{N} = N - a/b$.
9. The derivative of the perturbation variable is: $$\frac{d\tilde{N}}{dt} = \frac{d}{dt}\left(N - \frac{a}{b}\right) = \frac{dN}{dt}$$
10. Substitute $\tilde{N}$ into the linearized differential equation: $$\frac{d\tilde{N}}{dt} = -a\tilde{N}$$
11. The solution to this first-order linear ordinary differential equation is: $$\tilde{N}(t) = \tilde{N}_0 e^{-at}$$
12. If $a > 0$, then $\tilde{N}(t)$ decreases to 0 as $t \to \infty$.
13. As $\tilde{N}(t) \to 0$, it implies that $N - a/b \to 0$.
14. Therefore, $N \to a/b$ as $t \to \infty$.
15. This indicates that $N = a/b$ is a stable equilibrium point.

**Reference:** start_page=8 end_page=8
### **Stability Analysis of Equilibrium Points for a First-Order Autonomous ODE**
**Stub:** Determine the stability of equilibrium points for the differential equation $\dot{x} = (x-2)(3-x)(x-4)$.

**Steps:**
1. The given first-order autonomous ordinary differential equation is: $$\dot{x} = (x-2)(3-x)(x-4)$$
2. To find the equilibrium points, set $\dot{x} = 0$: $$(x-2)(3-x)(x-4) = 0$$
3. The equilibrium points are $x=2$, $x=3$, and $x=4$.
4. Analyze the sign of $\dot{x}$ in the intervals defined by these equilibrium points:
5. For $x < 2$: Choose $x=1.5$. $\dot{x} = (1.5-2)(3-1.5)(1.5-4) = (-0.5)(1.5)(-2.5) = 1.875 > 0$. Thus, $x$ increases.
6. For $2 < x < 3$: Choose $x=2.5$. $\dot{x} = (2.5-2)(3-2.5)(2.5-4) = (0.5)(0.5)(-1.5) = -0.375 < 0$. Thus, $x$ decreases.
7. For $3 < x < 4$: Choose $x=3.5$. $\dot{x} = (3.5-2)(3-3.5)(3.5-4) = (1.5)(-0.5)(-0.5) = 0.375 > 0$. Thus, $x$ increases.
8. For $x > 4$: Choose $x=4.5$. $\dot{x} = (4.5-2)(3-4.5)(4.5-4) = (2.5)(-1.5)(0.5) = -1.875 < 0$. Thus, $x$ decreases.
9. Based on the sign changes of $\dot{x}$ and the phase portrait (trajectories $x(t)$ vs $t$):
10. At $x=2$: $\dot{x}$ changes from positive to negative. Solutions approach $x=2$ from both sides, indicating that $x=2$ is a stable equilibrium point.
11. At $x=3$: $\dot{x}$ changes from negative to positive. Solutions move away from $x=3$ on both sides, indicating that $x=3$ is an unstable equilibrium point.
12. At $x=4$: $\dot{x}$ changes from positive to negative. Solutions approach $x=4$ from both sides, indicating that $x=4$ is a stable equilibrium point.

**Reference:** start_page=9 end_page=9
### **Stability Analysis of a First-Order Autonomous Differential Equation**
**Stub:** Determine the equilibrium points and their stability for the differential equation $\dot{x} = (x-2)(3-x)(x-4)$.

**Steps:**
1. Identify the given first-order autonomous differential equation: $$\dot{x} = (x-2)(3-x)(x-4)$$
2. Find the equilibrium points by setting $\dot{x} = 0$: $$(x-2)(3-x)(x-4) = 0$$This yields equilibrium points at $x=2$, $x=3$, and $x=4$.
3. Analyze the sign of $\dot{x}$ in the intervals defined by the equilibrium points:
4. For $x < 2$ (e.g., $x=1$): $\dot{x} = (1-2)(3-1)(1-4) = (-1)(2)(-3) = 6 > 0$.
5. For $2 < x < 3$ (e.g., $x=2.5$): $\dot{x} = (2.5-2)(3-2.5)(2.5-4) = (0.5)(0.5)(-1.5) = -0.375 < 0$.
6. For $3 < x < 4$ (e.g., $x=3.5$): $\dot{x} = (3.5-2)(3-3.5)(3.5-4) = (1.5)(-0.5)(-0.5) = 0.375 > 0$.
7. For $x > 4$ (e.g., $x=5$): $\dot{x} = (5-2)(3-5)(5-4) = (3)(-2)(1) = -6 < 0$.
8. Determine the stability of each equilibrium point based on the sign changes of $\dot{x}$ (as illustrated by the phase line graph):
9. At $x=2$: $\dot{x}$ changes from positive to negative, indicating that trajectories flow towards $x=2$. Thus, $x=2$ is a stable equilibrium point.
10. At $x=3$: $\dot{x}$ changes from negative to positive, indicating that trajectories flow away from $x=3$. Thus, $x=3$ is an unstable equilibrium point.
11. At $x=4$: $\dot{x}$ changes from positive to negative, indicating that trajectories flow towards $x=4$. Thus, $x=4$ is a stable equilibrium point.
12. The phase portrait (bottom graph) visually confirms these stability conclusions, showing solutions converging to $x=2$ and $x=4$, and diverging from $x=3$ over time $t$.

**Reference:** start_page=9 end_page=9


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** In the context of first-order difference equations of the form x_n+1 = f(x_n), how are equilibrium points graphically identified?

**Topics:** First Order Difference Equations, Equilibrium Points, Graphical Analysis

**Options:**
- The points where the graph of y = f(x_n) intersects the x-axis.
- The points where the graph of y = f(x_n) intersects the y-axis.
- ✅ The points where the graph of y = f(x_n) intersects the line y = x_n.
- The maximum or minimum points of the graph of y = f(x_n).

**Explanation:** An equilibrium point occurs when x_n+1 = x_n = x. Graphically, this means finding the intersection of the function y = f(x_n) and the identity line y = x_n.

**Reference:** start_page=1 end_page=1
### **Conceptual Question**
**Question:** Consider the continuous population models: exponential growth (dN/dt = rN) and logistic growth (dN/dt = N(a-bN)). How do their non-trivial equilibrium points (N > 0) compare?

**Topics:** Continuous Population Models, Exponential Growth, Logistic Growth

**Options:**
- Both models have a single non-trivial equilibrium point.
- Exponential growth has one non-trivial equilibrium point, while logistic growth has two.
- ✅ Exponential growth has no non-trivial equilibrium points, while logistic growth has one at N = a/b.
- Both models have no non-trivial equilibrium points.

**Explanation:** For exponential growth, dN/dt = rN implies that if N > 0, dN/dt is never zero (unless r=0), meaning no non-trivial equilibrium points. For logistic growth, dN/dt = N(a-bN) = 0 yields N=0 or N=a/b. Thus, N=a/b is the single non-trivial equilibrium point.

**Reference:** start_page=3 end_page=7
### **Conceptual Question**
**Question:** In the context of a continuous population model dN/dt = f(N), what characterizes a stable equilibrium point N*?

**Topics:** Stability Analysis, Equilibrium Points, Differential Equations

**Options:**
- If N is slightly perturbed from N*, dN/dt will push N further away from N*.
- The derivative f'(N*) evaluated at the equilibrium point is positive.
- ✅ If N is slightly greater than N*, dN/dt < 0, and if N is slightly less than N*, dN/dt > 0, causing N to return to N*.
- It is a point where the population always reaches its maximum value.

**Explanation:** A stable equilibrium point is one where small perturbations from the equilibrium cause the system to return to that point. This means if N > N*, dN/dt must be negative to decrease N, and if N < N*, dN/dt must be positive to increase N, both pushing N back towards N*. Mathematically, linearization shows that f'(N*) < 0 for stability.

**Reference:** start_page=7 end_page=9
