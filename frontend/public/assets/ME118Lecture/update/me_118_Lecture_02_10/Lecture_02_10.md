# Lecture Source: Lecture_02_10.pdf

## Solving Second-Order Linear ODEs and Phase Plane Analysis

**Lecture Type:** mixed

### Summary
This lecture covers methods for solving second-order linear ordinary differential equations, including finding general solutions using characteristic equations and applying initial conditions. It also introduces the transformation of second-order ODEs into systems of first-order ODEs, which are then solved using eigenvalues and eigenvectors. A significant portion is dedicated to understanding and visualizing the behavior of these systems through phase plane analysis and the method of isoclines, including cases with complex eigenvalues.

### Core Topics
- Second-order linear homogeneous ODEs
- Characteristic equation
- General solutions for ODEs
- Initial conditions
- Systems of first-order ODEs
- Eigenvalues and eigenvectors
- Phase plane analysis
- Method of isoclines
- Complex eigenvalues

### Learning Objectives
1. Solve second-order linear homogeneous ODEs using the characteristic equation method.
2. Apply initial conditions to determine specific solutions for ODEs and systems.
3. Transform a second-order ODE into an equivalent system of first-order ODEs.
4. Solve systems of first-order linear ODEs using eigenvalues and eigenvectors.
5. Construct phase plane diagrams to visualize the qualitative behavior of solutions.
6. Utilize the method of isoclines to sketch phase portraits.
7. Analyze and interpret solutions involving complex eigenvalues.

### Assumed Prerequisites
- Basic calculus
- Linear algebra (matrices, eigenvalues, eigenvectors)
- First-order ordinary differential equations


## Derivations

### **Solving Second-Order ODE via State-Space and Eigenvalue Analysis**
**Stub:** Conversion of a second-order linear homogeneous ordinary differential equation (ODE) to a system of first-order ODEs and formulation of the eigenvalue problem for its solution.

**Steps:**
1. Start with the given second-order ordinary differential equation: $$\ddot{x} + 2\dot{x} - 3x = 0$$
2. Define the first state variable: Let $x = x_1$.
3. From the state variable definition, the first derivative is $\dot{x} = \dot{x}_1 = x_2$.
4. The second derivative $\ddot{x}$ can then be expressed as $\dot{x}_2$, since $\dot{x} = x_2$.
5. Substitute the state variables into the original ODE: $\dot{x}_2 + 2x_2 - 3x_1 = 0$.
6. Rearrange the substituted equation to express $\dot{x}_2$: $$\dot{x}_2 = 3x_1 - 2x_2$$
7. Combine the state variable definitions into a system of first-order differential equations:
8. $$\begin{aligned} \dot{x}_1 &= x_2 \\ \dot{x}_2 &= 3x_1 - 2x_2 \end{aligned}$$
9. Represent this system in matrix form: $$\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 3 & -2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$$
10. Assume a solution of the form $\mathbf{x}(t) = \mathbf{X}_0 e^{\lambda t}$, where $\mathbf{X}_0 = \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix}$: $$\begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} = \begin{bmatrix} x_{10} e^{\lambda t} \\ x_{20} e^{\lambda t} \end{bmatrix} = \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} e^{\lambda t}$$
11. Differentiate the assumed solution with respect to time: $$\begin{bmatrix} \dot{x}_1(t) \\ \dot{x}_2(t) \end{bmatrix} = \begin{bmatrix} x_{10} \lambda e^{\lambda t} \\ x_{20} \lambda e^{\lambda t} \end{bmatrix} = \lambda \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} e^{\lambda t}$$
12. Substitute the assumed solution and its derivative into the matrix ODE: $$\lambda \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} e^{\lambda t} = \begin{bmatrix} 0 & 1 \\ 3 & -2 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} e^{\lambda t}$$
13. Cancel the common $e^{\lambda t}$ term and rearrange to form the eigenvalue problem $A \mathbf{X}_0 = \lambda \mathbf{X}_0$: $$\lambda \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 3 & -2 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix}$$
14. Rewrite the eigenvalue problem in the form $(A - \lambda I) \mathbf{X}_0 = 0$: $$\lambda \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} - \begin{bmatrix} 0 & 1 \\ 3 & -2 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
15. Perform the matrix subtraction to obtain the characteristic matrix: $$\begin{bmatrix} \lambda & -1 \\ -3 & \lambda+2 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

**Reference:** start_page=2 end_page=2
### **Solution of a System of Linear Differential Equations**
**Stub:** Derivation of the general and particular solutions for a system of linear differential equations using eigenvalues and eigenvectors.

**Steps:**
1. For nontrivial solutions, the characteristic equation is given by:$$ \det \begin{bmatrix} \lambda & -1 \\ -3 & \lambda+2 \end{bmatrix} = 0 $$
2. Expanding the determinant yields:$$ \lambda(\lambda+2) - (-1)(-3) = 0 $$$$ \lambda^2 + 2\lambda - 3 = 0 $$
3. Factoring the quadratic equation to find the eigenvalues:$$ (\lambda+3)(\lambda-1) = 0 $$$$ \lambda = -3, \lambda = 1 $$
4. For $\lambda = -3$, find the corresponding eigenvector by solving:$$ \begin{bmatrix} -3 & -1 \\ -3 & -1 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$
5. This gives the equation $-3x_{10} - x_{20} = 0$. Letting $x_{10} = 1$, we find $x_{20} = -3$. Thus, the first part of the solution is:$$ \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} = \begin{bmatrix} 1 \\ -3 \end{bmatrix} e^{-3t} $$
6. For $\lambda = 1$, find the corresponding eigenvector by solving:$$ \begin{bmatrix} 1 & -1 \\ -3 & 3 \end{bmatrix} \begin{bmatrix} x_{10} \\ x_{20} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$
7. This gives the equation $x_{10} - x_{20} = 0$. Letting $x_{10} = 1$, we find $x_{20} = 1$. Thus, the second part of the solution is:$$ \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} e^{t} $$
8. The general solution is a linear combination of these two solutions:$$ \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} = c_1 \begin{bmatrix} 1 \\ -3 \end{bmatrix} e^{-3t} + c_2 \begin{bmatrix} 1 \\ 1 \end{bmatrix} e^{t} $$
9. Apply the initial conditions $x_1(0) = 1$ and $x_2(0) = 1$, so $\begin{bmatrix} x_1(0) \\ x_2(0) \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. Substituting into the general solution at $t=0$:$$ \begin{bmatrix} 1 \\ 1 \end{bmatrix} = c_1 \begin{bmatrix} 1 \\ -3 \end{bmatrix} + c_2 \begin{bmatrix} 1 \\ 1 \end{bmatrix} $$
10. This implies $1 = c_1 + c_2$ and $1 = -3c_1 + c_2$. Solving these equations, we find $c_1=0$ and $c_2=1$. The particular solution is:$$ \begin{bmatrix} x_1(t) \\ x_2(t) \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \end{bmatrix} e^{t} $$

**Reference:** start_page=3 end_page=3
### **Deriving Straight-Line Solutions for a System of ODEs**
**Stub:** Determine the slopes $m$ for which $x_2 = mx_1$ represents a solution path for the system $\dot{x_1} = x_2$, $\dot{x_2} = 3x_1 - 2x_2$.

**Steps:**
1. Given the system of differential equations:$$ \dot{x_1} = x_2 $$$$ \dot{x_2} = 3x_1 - 2x_2 $$
2. The slope of the trajectories in the phase plane is given by:$$ \frac{dx_2}{dx_1} = \frac{\dot{x_2}}{\dot{x_1}} = \frac{3x_1 - 2x_2}{x_2} $$
3. Assume a straight-line solution of the form $x_2 = mx_1$. Then the slope $dx_2/dx_1 = m$.
4. Substitute $x_2 = mx_1$ and $dx_2/dx_1 = m$ into the slope equation:$$ m = \frac{3x_1 - 2(mx_1)}{mx_1} $$
5. Simplify the expression by canceling $x_1$:$$ m = \frac{x_1(3 - 2m)}{x_1(m)} \implies m = \frac{3 - 2m}{m} $$
6. Rearrange the equation to form a quadratic equation in $m$:$$ m^2 = 3 - 2m $$$$ m^2 + 2m - 3 = 0 $$
7. Factor the quadratic equation to find the possible values for $m$:$$ (m+3)(m-1) = 0 $$$$ m = -3, m = 1 $$

**Reference:** start_page=4 end_page=4
### **Solution of a Second-Order Homogeneous Linear ODE with Constant Coefficients**
**Stub:** Derive the particular solution for the initial value problem: ẍ + 2ẋ + 5x = 0, x(0)=1, ẋ(0)=1.

**Steps:**
1. State the given second-order homogeneous linear ordinary differential equation and initial conditions: $$ẍ + 2ẋ + 5x = 0$$ $$x(0)=1, ẋ(0)=1$$
2. Assume a solution of the form $x = e^{λt}$ and find its derivatives: $$x = e^{λt} \implies ẋ = λe^{λt} \implies ẍ = λ^2 e^{λt}$$
3. Substitute the assumed solution into the ODE to obtain the characteristic equation: $$λ^2 e^{λt} + 2λe^{λt} + 5e^{λt} = 0$$ $$λ^2 + 2λ + 5 = 0$$
4. Solve the characteristic equation for $λ$ using the quadratic formula $λ = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$: $$λ = \frac{-2 \pm \sqrt{2^2 - 4(1)(5)}}{2}$$ $$λ = \frac{-2 \pm \sqrt{4 - 20}}{2}$$ $$λ = \frac{-2 \pm \sqrt{-16}}{2}$$ $$λ = \frac{-2 \pm 4j}{2}$$ $$λ = -1 \pm 2j$$
5. Write the general solution for the ODE with complex conjugate roots $λ = α \pm jβ$ as $x(t) = e^{αt} (A \cos(βt) + B \sin(βt))$. Here $α = -1$ and $β = 2$: $$x(t) = C_1 e^{(-1+2j)t} + C_2 e^{(-1-2j)t}$$ $$x(t) = e^{-t} (C_1 e^{2jt} + C_2 e^{-2jt})$$ $$x(t) = e^{-t} [C_1 (\cos(2t) + j\sin(2t)) + C_2 (\cos(2t) - j\sin(2t))]$$ $$x(t) = e^{-t} [(C_1 + C_2) \cos(2t) + j(C_1 - C_2) \sin(2t)]$$ Let $A = C_1 + C_2$ and $B = j(C_1 - C_2)$. Then the general real solution is: $$x(t) = e^{-t} (A \cos(2t) + B \sin(2t))$$
6. Apply the first initial condition $x(0) = 1$ to find constant $A$: $$x(0) = e^0 (A \cos(0) + B \sin(0)) = 1$$ $$1 = A(1) + B(0) \implies A = 1$$
7. Differentiate $x(t)$ with respect to $t$ to find $ẋ(t)$: $$ẋ(t) = \frac{d}{dt} [e^{-t} (A \cos(2t) + B \sin(2t))]$$ $$ẋ(t) = -e^{-t} (A \cos(2t) + B \sin(2t)) + e^{-t} (-2A \sin(2t) + 2B \cos(2t))$$
8. Apply the second initial condition $ẋ(0) = 1$ to find constant $B$: $$ẋ(0) = -e^0 (A \cos(0) + B \sin(0)) + e^0 (-2A \sin(0) + 2B \cos(0)) = 1$$ $$1 = -A(1) + 2B(1)$$ $$1 = -A + 2B$$ Substitute $A = 1$: $$1 = -1 + 2B \implies 2B = 2 \implies B = 1$$
9. Substitute the values of $A = 1$ and $B = 1$ into the general solution: $$x(t) = e^{-t} (1 \cos(2t) + 1 \sin(2t))$$ $$x(t) = e^{-t} (\cos(2t) + \sin(2t))$$
10. Convert the sinusoidal part to amplitude-phase form $R \cos(θ - φ)$ where $R = \sqrt{a^2 + b^2}$ and $φ = \arctan(b/a)$: $$R = \sqrt{1^2 + 1^2} = \sqrt{2}$$ $$φ = \arctan(1/1) = \pi/4$$ Thus, the final solution is: $$x(t) = \sqrt{2} e^{-t} \cos(2t - \pi/4)$$

**Reference:** start_page=1 end_page=1
### **Solution to a Second-Order Homogeneous Linear Differential Equation with Initial Conditions**
**Stub:** Solve the differential equation $x'' + 2x' - 3x = 0$ with initial conditions $x(0)=1$ and $x'(0)=1$ to find $x(t)$.

**Steps:**
1. The given second-order homogeneous linear differential equation is: $$x'' + 2x' - 3x = 0$$
2. Assume a solution of the form $x(t) = e^{\lambda t}$. Then the first derivative is $x'(t) = \lambda e^{\lambda t}$ and the second derivative is $x''(t) = \lambda^2 e^{\lambda t}$.
3. Substitute these into the differential equation: $$\lambda^2 e^{\lambda t} + 2\lambda e^{\lambda t} - 3e^{\lambda t} = 0$$
4. Factor out $e^{\lambda t}$ and simplify to obtain the characteristic equation: $$\lambda^2 + 2\lambda - 3 = 0$$
5. Factor the quadratic equation: $$(\lambda + 3)(\lambda - 1) = 0$$
6. The roots of the characteristic equation are $\lambda_1 = -3$ and $\lambda_2 = 1$.
7. The general solution for $x(t)$ is a linear combination of exponential terms: $$x(t) = C_1 e^{-3t} + C_2 e^{t}$$
8. Differentiate the general solution to find $x'(t)$: $$x'(t) = -3C_1 e^{-3t} + C_2 e^{t}$$
9. Apply the first initial condition $x(0)=1$: $$1 = C_1 e^{-3(0)} + C_2 e^{0} \Rightarrow 1 = C_1 + C_2$$
10. Apply the second initial condition $x'(0)=1$: $$1 = -3C_1 e^{-3(0)} + C_2 e^{0} \Rightarrow 1 = -3C_1 + C_2$$
11. We now have a system of two linear equations for $C_1$ and $C_2$: $$\begin{cases} C_1 + C_2 = 1 \\ -3C_1 + C_2 = 1 \end{cases}$$
12. Subtract the second equation from the first: $(C_1 + C_2) - (-3C_1 + C_2) = 1 - 1 \Rightarrow 4C_1 = 0 \Rightarrow C_1 = 0$.
13. Substitute $C_1 = 0$ into the first equation: $0 + C_2 = 1 \Rightarrow C_2 = 1$.
14. Substitute the values of the constants $C_1 = 0$ and $C_2 = 1$ back into the general solution: $$x(t) = 0 \cdot e^{-3t} + 1 \cdot e^{t}$$
15. The particular solution satisfying the initial conditions is: $$x(t) = e^{t}$$

**Reference:** start_page=6 end_page=6
### **Conversion of a Linear Combination of Sine and Cosine to a Single Cosine Function**
**Stub:** Transform a sum of sine and cosine terms (e.g., $A\cos(\omega t) + B\sin(\omega t)$) into the form $C\cos(\omega t - \phi)$.

**Steps:**
1. Given the coefficients (implied from context for $e^{-t}(\cos(2t) + \sin(2t))$), let: $$1 = C \cos\phi$$ $$1 = C \sin\phi$$
2. To find the amplitude $C$, square both equations and add them: $$1^2 + 1^2 = (C \cos\phi)^2 + (C \sin\phi)^2$$
3. This simplifies to: $$2 = C^2 (\cos^2\phi + \sin^2\phi)$$
4. Using the trigonometric identity $\cos^2\phi + \sin^2\phi = 1$: $$2 = C^2 \Rightarrow C = \sqrt{2}$$
5. To find the phase angle $\phi$, divide the second equation by the first: $$\frac{C \sin\phi}{C \cos\phi} = \frac{1}{1}$$
6. This simplifies to: $$\tan\phi = 1$$
7. Therefore, the principal value for $\phi$ is: $$\phi = \frac{\pi}{4}$$
8. Assuming the original expression was of the form $x(t) = e^{-t}(A\cos(2t) + B\sin(2t))$ where $A=1$ and $B=1$, the transformed expression is: $$x(t) = \sqrt{2} e^{-t} \cos(2t - \pi/4)$$

**Reference:** start_page=5 end_page=5
### **Phase Portrait Analysis of a Damped Harmonic Oscillator**
**Stub:** Analyze the phase portrait of the second-order linear ODE $\ddot{x} + 2\dot{x} + 5x = 0$.

**Steps:**
1. Convert the second-order differential equation into a system of first-order differential equations by letting $x_1 = x$ and $x_2 = \dot{x}$.
2. The system of first-order ODEs is: $\dot{x_1} = x_2$
3. $\dot{x_2} = -5x_1 - 2x_2$
4. Derive the slope of trajectories in the phase plane ($x_1, x_2$) by dividing $\dot{x_2}$ by $\dot{x_1}$: $$\frac{dx_2}{dx_1} = \frac{\dot{x_2}}{\dot{x_1}} = \frac{-5x_1 - 2x_2}{x_2}$$
5. Analyze the slope along specific lines/axes to understand the phase portrait:
6. 1) Along the $x_2$-axis ($x_1 = 0$): $$\frac{dx_2}{dx_1} = \frac{-2x_2}{x_2} = -2$$
7. 2) Along the $x_1$-axis ($x_2 = 0$): $$\frac{dx_2}{dx_1} = \frac{-5x_1}{0} \rightarrow \infty$$ (This indicates vertical tangents, except at the origin).
8. 3) Identify points where the slope is zero (horizontal tangents): $$\frac{dx_2}{dx_1} = 0 \Rightarrow -5x_1 - 2x_2 = 0 \Rightarrow x_2 = -\frac{5}{2}x_1$$
9. 4) Along the line $x_1 = x_2$: $$\frac{dx_2}{dx_1} = \frac{-5x_1 - 2x_1}{x_1} = \frac{-7x_1}{x_1} = -7$$
10. 5) Along the line $x_1 = -x_2$ (or $x_2 = -x_1$): $$\frac{dx_2}{dx_1} = \frac{-5(-x_2) - 2x_2}{x_2} = \frac{5x_2 - 2x_2}{x_2} = \frac{3x_2}{x_2} = 3$$
11. 6) Investigate for straight-line solutions of the form $x_2 = mx_1$. If such a solution exists, then $\frac{dx_2}{dx_1} = m$.
12. Substitute $x_2 = mx_1$ into the slope equation: $$m = \frac{-5x_1 - 2mx_1}{mx_1} = \frac{-5 - 2m}{m}$$
13. Rearrange to form a quadratic equation for $m$: $$m^2 = -5 - 2m \Rightarrow m^2 + 2m + 5 = 0$$
14. Calculate the discriminant $\Delta = b^2 - 4ac = (2)^2 - 4(1)(5) = 4 - 20 = -16$. Since $\Delta < 0$, there are no real roots for $m$, indicating no straight-line solutions.
15. Based on the system equations and the derived slopes, the phase portrait (diagram) illustrates a stable spiral equilibrium at the origin $(0,0)$. The arrows on the diagram indicate that trajectories spiral inwards towards the origin, which is characteristic of a damped oscillator. For instance, if $x_2 > 0$, then $\dot{x_1} = x_2 > 0$, meaning trajectories move to the right ($x_1 \uparrow$). If $x_2 < 0$, then $\dot{x_1} = x_2 < 0$, meaning trajectories move to the left ($x_1 \downarrow$). Along the $x_1$-axis ($x_2=0$), $\dot{x_2} = -5x_1$. So for $x_1 > 0$, $\dot{x_2} < 0$, implying $x_2$ decreases ($x_2 \downarrow$), which helps define the clockwise spiral direction shown in the diagram.

**Reference:** start_page=13 end_page=13
### **Phase Portrait Analysis of a Second-Order Linear ODE**
**Stub:** Derivation of the phase plane equations and slope for the system $\ddot{x} + 4x = 0$, and analysis of its behavior along specific lines.

**Steps:**
1. Given the second-order ordinary differential equation: $\ddot{x} + 4x = 0$.
2. Define state variables for phase plane representation: Let $x_1 = x$ and $x_2 = \dot{x}$.
3. Express the system in state-space form: $\dot{x_1} = \dot{x} = x_2$ and $\dot{x_2} = \ddot{x} = -4x_1$.
4. Derive the slope of the phase trajectories: $\frac{dx_2}{dx_1} = \frac{\dot{x_2}}{\dot{x_1}} = \frac{-4x_1}{x_2}$.
5. Analyze the slope along the $x_2$-axis (where $x_1 = 0$): $\frac{dx_2}{dx_1} = 0$. This indicates horizontal tangents.
6. Analyze the slope along the $x_1$-axis (where $x_2 = 0$): $\frac{dx_2}{dx_1} \rightarrow \infty$. This indicates vertical tangents.
7. Analyze the slope along the line $x_1 = x_2$: Substitute $x_1 = x_2$ into the slope equation to get $\frac{dx_2}{dx_1} = \frac{-4x_1}{x_1} = -4$.
8. Analyze the slope along the line $x_1 = -x_2$: Substitute $x_1 = -x_2$ into the slope equation to get $\frac{dx_2}{dx_1} = \frac{-4(-x_2)}{x_2} = 4$.
9. Analyze the slope along the line $x_1 = \frac{1}{4}x_2$ (or $x_2 = 4x_1$): Substitute $x_2 = 4x_1$ into the slope equation to get $\frac{dx_2}{dx_1} = \frac{-4x_1}{4x_1} = -1$.
10. The provided diagram illustrates the vector field and trajectories in the phase plane based on these derived slopes, showing an elliptical path characteristic of a simple harmonic oscillator.

**Reference:** start_page=14 end_page=14


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** In the context of a 2x2 system of linear differential equations, how do the characteristics of the system's eigenvalues fundamentally dictate the qualitative behavior of trajectories in the phase plane?

**Topics:** Eigenvalues, Phase Plane, System Dynamics

**Options:**
- Real and distinct eigenvalues always result in spiral sources or sinks.
- ✅ Complex conjugate eigenvalues with a non-zero real part lead to spiral trajectories (sinks or sources).
- Purely imaginary eigenvalues consistently indicate a saddle point.
- If all eigenvalues are positive, the origin is a stable node.

**Explanation:** Complex conjugate eigenvalues (e.g., λ = α ± iβ with α ≠ 0) introduce oscillatory behavior combined with exponential growth or decay. If α < 0, trajectories spiral inward towards the origin (spiral sink). If α > 0, trajectories spiral outward away from the origin (spiral source). This is distinct from real eigenvalues which lead to nodes or saddles, and purely imaginary eigenvalues which lead to centers.

**Reference:** start_page=4 end_page=8
### **Conceptual Question**
**Question:** What is the primary utility of employing the method of isoclines when analyzing a system of two first-order differential equations to construct its phase portrait?

**Topics:** Isoclines, Phase Portrait, Direction Fields

**Options:**
- To analytically solve the system of differential equations for explicit solutions.
- ✅ To graphically determine the regions in the phase plane where all solution trajectories share a common slope.
- To calculate the exact numerical values of the system's eigenvalues.
- To precisely locate all stable and unstable equilibrium points of the system.

**Explanation:** Isoclines are curves along which the slope dx₂/dx₁ of the trajectories is constant. By sketching several isoclines, one can efficiently determine the direction of flow for trajectories across the phase plane, thereby providing a qualitative understanding of the system's dynamics and helping to construct the phase portrait.

**Reference:** start_page=4 end_page=4
### **Conceptual Question**
**Question:** What is the primary analytical advantage gained by transforming a second-order linear ordinary differential equation into an equivalent system of two first-order linear differential equations?

**Topics:** System Transformation, State-Space, Phase Plane Analysis

**Options:**
- It simplifies the algebraic process of finding the roots of the characteristic equation.
- ✅ It allows for a direct visual representation of the system's dynamic behavior in the phase plane and the application of matrix methods.
- It eliminates the necessity of applying initial conditions to find a unique solution.
- It restricts the system to only having real eigenvalues, simplifying the solution.

**Explanation:** The transformation allows for the representation of the system using matrix notation (X' = AX), which facilitates the use of eigenvalue/eigenvector analysis. More importantly, it enables the creation of a phase portrait, a graphical tool that provides a qualitative understanding of the system's stability, equilibrium points, and trajectory behavior, which is often harder to visualize directly from a single second-order equation.

**Reference:** start_page=2 end_page=8
