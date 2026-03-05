# Lecture Source: Lecture_02_03.pdf

## Solving Linear Homogeneous ODEs and Damped Mass-Spring Systems

**Lecture Type:** mixed

### Summary
The lecture introduces methods for solving linear homogeneous ordinary differential equations of various orders, emphasizing the characteristic equation approach. It applies these solution techniques to model and analyze the dynamic behavior of mass-damper-spring systems, categorizing their responses based on damping levels (overdamped, underdamped, critically damped). Additionally, it covers the conversion of higher-order ODEs into systems of first-order ODEs and their solution using eigenvalue decomposition and matrix methods.

### Core Topics
- Linear homogeneous ordinary differential equations
- Characteristic equations
- Mass-damper-spring systems
- Damping types
- Overdamped response
- Underdamped response
- Critically damped response
- Systems of first-order ODEs
- Eigenvalue problems
- Matrix diagonalization

### Learning Objectives
1. Solve linear homogeneous ordinary differential equations of first, second, and third order
2. Model mass-damper-spring systems
3. Classify the dynamic response of damped systems as overdamped, underdamped, or critically damped
4. Determine the time-domain solution for damped mass-spring systems under different damping conditions
5. Convert higher-order ODEs into systems of first-order ODEs
6. Solve systems of linear ODEs using eigenvalues and eigenvectors
7. Apply matrix diagonalization to solve systems of ODEs

### Assumed Prerequisites
- Differential calculus
- Linear algebra
- Basic mechanics (forces, Newton's laws)


## Derivations

### **Solution to First-Order Linear Homogeneous ODE**
**Stub:** Derive the general solution for $$\frac{dx}{dt} + kx = 0$$

**Steps:**
1. Start with the first-order linear homogeneous ordinary differential equation (ODE): $$\frac{dx}{dt} + kx = 0$$
2. Assume a solution of the exponential form: $$x(t) = e^{\lambda t}$$
3. Calculate the first derivative of the assumed solution with respect to time: $$\frac{dx}{dt} = \lambda e^{\lambda t}$$
4. Substitute $x(t)$ and $\frac{dx}{dt}$ into the original ODE: $$\lambda e^{\lambda t} + k e^{\lambda t} = 0$$
5. Factor out the common term $e^{\lambda t}$: $$e^{\lambda t} (\lambda + k) = 0$$
6. Since $e^{\lambda t}$ is never zero, the characteristic equation must be satisfied: $$\lambda + k = 0$$
7. Solve for the characteristic root $\lambda$: $$\lambda = -k$$
8. Substitute the value of $\lambda$ back into the assumed solution to obtain the general solution: $$x(t) = e^{-kt}$$

**Reference:** start_page=1 end_page=1
### **Form of Second-Order Linear Homogeneous ODE**
**Stub:** Statement of the general form of a second-order linear homogeneous ODE: $$\frac{d^2x}{dt^2} + a\frac{dx}{dt} + bx = 0$$

**Steps:**
1. The general form of a second-order linear homogeneous ODE is given as: $$\frac{d^2x}{dt^2} + a\frac{dx}{dt} + bx = 0$$
2. To solve this type of ODE, one typically assumes a solution of the form: $$x(t) = e^{\lambda t}$$ to find the characteristic equation.

**Reference:** start_page=1 end_page=1
### **Form of Third-Order Linear Homogeneous ODE**
**Stub:** Statement of the general form of a third-order linear homogeneous ODE: $$\frac{d^3x}{dt^3} + a\frac{d^2x}{dt^2} + b\frac{dx}{dt} + cx = 0$$

**Steps:**
1. The general form of a third-order linear homogeneous ODE is presented as: $$\frac{d^3x}{dt^3} + a\frac{d^2x}{dt^2} + b\frac{dx}{dt} + cx = 0$$
2. Similar to lower-order ODEs, a solution of the form $x(t) = e^{\lambda t}$ would be assumed to derive the characteristic equation for this higher-order system.

**Reference:** start_page=1 end_page=1
### **Definition and Application of Derivative Operator D**
**Stub:** Define the derivative operator $D$ and demonstrate its application to an exponential function $e^{\lambda t}$.

**Steps:**
1. The derivative operator $D$ is defined as the first derivative with respect to time: $$D \equiv \frac{d}{dt}$$
2. Applying the derivative operator $D$ to an exponential function $e^{\lambda t}$ yields: $$D(e^{\lambda t}) = \lambda e^{\lambda t}$$

**Reference:** start_page=1 end_page=1
### **Solution of First-Order Linear Homogeneous ODE using Exponential Ansatz**
**Stub:** Derive the solution for the first-order linear homogeneous ordinary differential equation $\frac{dx}{dt} + kx = 0$ by assuming an exponential form $x(t) = e^{\lambda t}$.

**Steps:**
1. Consider the first-order linear homogeneous ODE: $$\frac{dx}{dt} + kx = 0$$
2. Assume a solution of the form: $$x(t) = e^{\lambda t}$$
3. Calculate the first derivative of the assumed solution: $$\dot{x}(t) = \frac{d}{dt}(e^{\lambda t}) = \lambda e^{\lambda t}$$
4. Substitute $x(t)$ and $\frac{dx}{dt}$ back into the original ODE: $$\lambda e^{\lambda t} + k e^{\lambda t} = 0$$
5. Factor out $e^{\lambda t}$: $$e^{\lambda t}(\lambda + k) = 0$$
6. Since $e^{\lambda t}$ is never zero, the characteristic equation is: $$\lambda + k = 0$$
7. Solve for $\lambda$: $$\lambda = -k$$
8. Substitute the value of $\lambda$ back into the assumed solution to obtain the particular solution: $$x(t) = e^{-kt}$$

**Reference:** start_page=1 end_page=1
### **Definition and Application of the Derivative Operator**
**Stub:** Define the derivative operator $D$ and show its action on an exponential function $e^{\lambda t}$.

**Steps:**
1. Define the derivative operator $D$: $$D \equiv \frac{d}{dt}$$
2. Apply the derivative operator to an exponential function $e^{\lambda t}$: $$D(e^{\lambda t}) = \frac{d}{dt}(e^{\lambda t}) = \lambda e^{\lambda t}$$

**Reference:** start_page=1 end_page=1
### **Equation of Motion for a Linear Mass-Damper-Spring System**
**Stub:** $$m\ddot{x} + c\dot{x} + kx = 0$$

**Steps:**
1. Apply Newton's Second Law for forces in the x-direction: $$\Sigma F_x = ma_x$$
2. From the free-body diagram, the forces acting on the mass are the spring force $F_k$ and the damping force $F_D$, both opposing the direction of positive displacement: $$ma_x = -F_k - F_D$$
3. Assume a linear spring, where the spring force is given by Hooke's Law: $$F_k = kx$$
4. Assume linear viscous damping, where the damping force is proportional to the velocity: $$F_D = c\dot{x}$$
5. Substitute the expressions for $F_k$ and $F_D$ into the equation of motion, noting that $a_x = \ddot{x}$: $$m\ddot{x} = -kx - c\dot{x}$$
6. Rearrange the equation into the standard form for a second-order linear ordinary differential equation: $$m\ddot{x} + c\dot{x} + kx = 0$$
7. The initial conditions for the system are given as $x(0) = x_0$ and $\dot{x}(0) = \dot{x}_0$.

**Reference:** start_page=2 end_page=2
### **Vertical Force Balance for Mass**
**Stub:** $$N = W$$

**Steps:**
1. Apply Newton's Second Law for forces in the y-direction: $$\Sigma F_y = ma_y$$
2. Assuming no vertical acceleration ($a_y = 0$), the sum of vertical forces is zero: $$\Sigma F_y = 0$$
3. Identify the vertical forces: Normal force $N$ acting upwards and Weight $W$ acting downwards: $$N - W = 0$$
4. Therefore, the normal force equals the weight: $$N = W$$

**Reference:** start_page=2 end_page=2
### **Linear Spring Force (Hooke's Law)**
**Stub:** $$F_k = kx$$

**Steps:**
1. The spring force $F_k$ is proportional to the displacement $x$: $$F_k \sim x$$
2. For a linear spring, this relationship is defined by Hooke's Law: $$F_k = kx$$

**Reference:** start_page=2 end_page=2
### **Hardening Spring Force**
**Stub:** $$F_k = k_1x + k_2x^3$$

**Steps:**
1. For a hardening spring, the force $F_k$ exhibits a non-linear relationship with displacement $x$: $$F_k = k_1x + k_2x^3$$

**Reference:** start_page=2 end_page=2
### **Coulomb Friction Force**
**Stub:** $$F = \mu_k N$$

**Steps:**
1. Coulomb friction force $F$ is proportional to the normal force $N$: $$F \sim N$$
2. The magnitude of Coulomb friction is given by the coefficient of kinetic friction $\mu_k$ multiplied by the normal force: $$F = \mu_k N$$

**Reference:** start_page=2 end_page=2
### **Viscous (Linear) Damping Force**
**Stub:** $$F = c\dot{x}$$

**Steps:**
1. Viscous damping force $F$ is proportional to the velocity $V$: $$F \sim V$$
2. For linear viscous damping, this is expressed with a damping coefficient $c$: $$F = cV$$
3. Since velocity $V$ is the time derivative of displacement $x$, this can be written as: $$F = c\dot{x}$$

**Reference:** start_page=2 end_page=2
### **Quadratic Damping (Drag Force)**
**Stub:** $$F = b\dot{x}^2$$

**Steps:**
1. Quadratic damping force $F$, often associated with drag, is proportional to the square of the velocity $V$: $$F \sim V^2$$
2. This relationship is expressed with a drag coefficient $b$: $$F = bV^2$$
3. Substituting velocity as the time derivative of displacement: $$F = b\dot{x}^2$$

**Reference:** start_page=2 end_page=2
### **Solution of Damped Harmonic Oscillator Characteristic Equation**
**Stub:** Derive the roots of the characteristic equation for the second-order linear differential equation $m\ddot{x} + c\dot{x} + kx = 0$ and classify the damping cases.

**Steps:**
1. The initial second-order linear homogeneous differential equation is given as: $$m\ddot{x} + c\dot{x} + kx = 0$$
2. Assume a solution of the form $x(t) = e^{\lambda t}$.
3. Calculate the first and second derivatives of the assumed solution: $$\dot{x}(t) = \lambda e^{\lambda t}$$$$\ddot{x}(t) = \lambda^2 e^{\lambda t}$$
4. Substitute $x(t)$, $\dot{x}(t)$, and $\ddot{x}(t)$ into the differential equation: $$m\lambda^2 e^{\lambda t} + c\lambda e^{\lambda t} + k e^{\lambda t} = 0$$
5. Factor out $e^{\lambda t}$ (since $e^{\lambda t} \neq 0$): $$e^{\lambda t}(m\lambda^2 + c\lambda + k) = 0$$
6. This leads to the characteristic equation: $$m\lambda^2 + c\lambda + k = 0$$
7. Solve for $\lambda$ using the quadratic formula: $$\lambda = \frac{-c \pm \sqrt{c^2 - 4mk}}{2m}$$
8. Rearrange the expression for $\lambda$ by dividing the numerator and denominator by $2m$ inside the square root: $$\lambda = \frac{-c}{2m} \pm \sqrt{\frac{c^2}{4m^2} - \frac{4mk}{4m^2}}$$$$\lambda = -\frac{c}{2m} \pm \sqrt{\left(\frac{c}{2m}\right)^2 - \frac{k}{m}}$$
9. Case I: The term under the square root is positive, leading to two distinct real roots (overdamped case): $$\left(\frac{c}{2m}\right)^2 - \frac{k}{m} > 0 \implies \frac{c^2}{4m^2} > \frac{k}{m}$$
10. Case II: The term under the square root is negative, leading to complex conjugate roots (underdamped case): $$\left(\frac{c}{2m}\right)^2 - \frac{k}{m} < 0 \implies \frac{c^2}{4m^2} < \frac{k}{m}$$
11. Case III: The term under the square root is zero, leading to one repeated real root (critically damped case): $$\left(\frac{c}{2m}\right)^2 = \frac{k}{m}$$

**Reference:** start_page=3 end_page=3
### **Solution for an Overdamped Second-Order System**
**Stub:** Derive the displacement $x(t)$ for an overdamped system given initial conditions.

**Steps:**
1. Define Case I (Overdamped) condition: $(\frac{C}{2m})^2 - \frac{k}{m} > 0$, which implies two real roots.
2. The two real roots of the characteristic equation are $\lambda_1 = -\frac{C}{2m} + \sqrt{(\frac{C}{2m})^2 - \frac{k}{m}}$ and $\lambda_2 = -\frac{C}{2m} - \sqrt{(\frac{C}{2m})^2 - \frac{k}{m}}$.
3. The general solution for the displacement $x(t)$ is $x(t) = c_1 e^{\lambda_1 t} + c_2 e^{\lambda_2 t}$.
4. The time derivative of the general solution is $\dot{x}(t) = \lambda_1 c_1 e^{\lambda_1 t} + \lambda_2 c_2 e^{\lambda_2 t}$.
5. Applying initial conditions (IC) at $t=0$: $x(0) = x_0 = c_1 + c_2$ and $\dot{x}(0) = \dot{x}_0 = \lambda_1 c_1 + \lambda_2 c_2$.
6. These form a system of linear equations for $c_1$ and $c_2$: $\begin{bmatrix} 1 & 1 \ \lambda_1 & \lambda_2 \end{bmatrix} \begin{bmatrix} c_1 \ c_2 \end{bmatrix} = \begin{bmatrix} x_0 \ \dot{x}_0 \end{bmatrix}$.
7. Solving for $c_1$: $c_1 = \frac{\begin{vmatrix} x_0 & 1 \ \dot{x}_0 & \lambda_2 \end{vmatrix}}{\begin{vmatrix} 1 & 1 \ \lambda_1 & \lambda_2 \end{vmatrix}} = \frac{x_0 \lambda_2 - \dot{x}_0}{\lambda_2 - \lambda_1}$.
8. Solving for $c_2$: $c_2 = \frac{\begin{vmatrix} 1 & x_0 \ \lambda_1 & \dot{x}_0 \end{vmatrix}}{\begin{vmatrix} 1 & 1 \ \lambda_1 & \lambda_2 \end{vmatrix}} = \frac{\dot{x}_0 - \lambda_1 x_0}{\lambda_2 - \lambda_1}$.
9. Substituting $c_1$ and $c_2$ back into the general solution, and replacing $\lambda_1, \lambda_2$ in the exponents with their full expressions, yields the overdamped solution for $x(t)$: $x(t) = \left(\frac{x_0 \lambda_2 - \dot{x}_0}{\lambda_2 - \lambda_1}\right) e^{\left(-\frac{C}{2m} + \sqrt{(\frac{C}{2m})^2 - \frac{k}{m}}\right)t} + \left(\frac{\dot{x}_0 - \lambda_1 x_0}{\lambda_2 - \lambda_1}\right) e^{\left(-\frac{C}{2m} - \sqrt{(\frac{C}{2m})^2 - \frac{k}{m}}\right)t}$.
10. The accompanying graph illustrates the typical exponentially decaying behavior of an overdamped system, where displacement $x$ approaches zero over time $t$ without oscillation.

**Reference:** start_page=4 end_page=4
### **Solution of Second-Order Linear Homogeneous ODE for Mass-Damper-Spring System (Underdamped Case)**
**Stub:** Derive the general solution $x(t) = e^{-c/2m t} P \cos(\omega_d t - \phi)$ for an underdamped mass-damper-spring system.

**Steps:**
1. The equation of motion for a mass-damper-spring system is derived from Newton's second law and force definitions (Hooke's law for spring, viscous damping for damper): $$m\ddot{x} + c\dot{x} + kx = 0$$
2. Assume an exponential solution of the form $x(t) = e^{\lambda t}$. Taking derivatives, $\dot{x}(t) = \lambda e^{\lambda t}$ and $\ddot{x}(t) = \lambda^2 e^{\lambda t}$.
3. Substitute these into the equation of motion to obtain the characteristic equation: $m\lambda^2 e^{\lambda t} + c\lambda e^{\lambda t} + k e^{\lambda t} = 0 \Rightarrow m\lambda^2 + c\lambda + k = 0$.
4. Solve for $\lambda$ using the quadratic formula: $$\lambda = \frac{-c \pm \sqrt{c^2 - 4mk}}{2m}$$
5. Rearrange the expression for $\lambda$: $$\lambda = -\frac{c}{2m} \pm \sqrt{(\frac{c}{2m})^2 - \frac{k}{m}}$$
6. For the Underdamped Case (Case II), the discriminant is negative: $(\frac{c}{2m})^2 - \frac{k}{m} < 0$. This means the term under the square root is negative.
7. Rewrite $\lambda$ using $j = \sqrt{-1}$: $$\lambda = -\frac{c}{2m} \pm \sqrt{-1 \left(\frac{k}{m} - (\frac{c}{2m})^2\right)} = -\frac{c}{2m} \pm j \sqrt{\frac{k}{m} - (\frac{c}{2m})^2}$$
8. Define the damped natural frequency $\omega_d \triangleq \sqrt{\frac{k}{m} - (\frac{c}{2m})^2}$.
9. The two complex conjugate roots are $\lambda_1 = -\frac{c}{2m} + j\omega_d$ and $\lambda_2 = -\frac{c}{2m} - j\omega_d$.
10. The general solution for $x(t)$ is a linear combination of these exponential terms: $x(t) = c_1 e^{\lambda_1 t} + c_2 e^{\lambda_2 t}$.
11. Substitute $\lambda_1$ and $\lambda_2$: $$x(t) = c_1 e^{(-\frac{c}{2m} + j\omega_d)t} + c_2 e^{(-\frac{c}{2m} - j\omega_d)t}$$
12. Factor out the real exponential term: $$x(t) = e^{-\frac{c}{2m}t} [c_1 e^{j\omega_d t} + c_2 e^{-j\omega_d t}]$$
13. Apply Euler's formula ($e^{\pm j\theta} = \cos\theta \pm j\sin\theta$): $$x(t) = e^{-\frac{c}{2m}t} [c_1 (\cos(\omega_d t) + j\sin(\omega_d t)) + c_2 (\cos(\omega_d t) - j\sin(\omega_d t))]$$
14. Group the cosine and sine terms: $$x(t) = e^{-\frac{c}{2m}t} [(c_1+c_2)\cos(\omega_d t) + j(c_1-c_2)\sin(\omega_d t)]$$
15. Define new real constants $A \triangleq c_1+c_2$ and $B \triangleq j(c_1-c_2)$ (assuming $c_1, c_2$ are complex conjugates for real $x(t)$).
16. The solution becomes: $$x(t) = e^{-\frac{c}{2m}t} [A\cos(\omega_d t) + B\sin(\omega_d t)]$$
17. Apply initial condition $x(0) = x_0$: $x_0 = e^0 [A\cos(0) + B\sin(0)] \Rightarrow x_0 = A$.
18. Differentiate $x(t)$ to find $\dot{x}(t)$: $\dot{x}(t) = -\frac{c}{2m} e^{-\frac{c}{2m}t} (A\cos(\omega_d t) + B\sin(\omega_d t)) + e^{-\frac{c}{2m}t} (-A\omega_d\sin(\omega_d t) + B\omega_d\cos(\omega_d t))$
19. Apply initial condition $\dot{x}(0) = \dot{x}_0$: $\dot{x}_0 = -\frac{c}{2m} A + B\omega_d$.
20. Substitute $A=x_0$ and solve for $B$: $\dot{x}_0 = -\frac{c}{2m} x_0 + B\omega_d \Rightarrow B = \frac{1}{\omega_d}(\dot{x}_0 + \frac{c}{2m}x_0)$.
21. The solution can be expressed in amplitude-phase form by letting $A = P\cos\phi$ and $B = P\sin\phi$.
22. From $A=x_0$ and $B=\frac{1}{\omega_d}(\dot{x}_0 + \frac{c}{2m}x_0)$, we find the amplitude: $$P = \sqrt{x_0^2 + \left(\frac{\dot{x}_0 + \frac{c}{2m}x_0}{\omega_d}\right)^2}$$
23. The phase angle is: $$\phi = \tan^{-1}\left(\frac{B}{A}\right) = \tan^{-1}\left(\frac{\dot{x}_0 + \frac{c}{2m}x_0}{\omega_d x_0}\right)$$
24. The final solution for the underdamped case is: $$x(t) = e^{-\frac{c}{2m}t} P \cos(\omega_d t - \phi)$$

**Reference:** start_page=5 end_page=11
### **Equation of Motion for Mass-Damper-Spring System**
**Stub:** Derive the second-order linear homogeneous ordinary differential equation $m\ddot{x} + c\dot{x} + kx = 0$.

**Steps:**
1. Consider a mass $m$ attached to a spring with stiffness $k$ and a damper with damping coefficient $c$. A free-body diagram shows forces acting on the mass.
2. Apply Newton's second law in the x-direction: $\sum F_x = m a_x = m\ddot{x}$.
3. The spring force is $F_k = -kx$ (Hooke's law, assuming linear spring).
4. The damping force is $F_D = -c\dot{x}$ (Viscous damping, assuming linear damping).
5. Summing forces: $m\ddot{x} = -kx - c\dot{x}$.
6. Rearrange into standard form: $m\ddot{x} + c\dot{x} + kx = 0$.

**Reference:** start_page=7 end_page=7
### **Characteristic Equation and Roots for Second-Order ODE**
**Stub:** Solve the characteristic equation $m\lambda^2 + c\lambda + k = 0$ for its roots $\lambda$.

**Steps:**
1. Given the differential equation $m\ddot{x} + c\dot{x} + kx = 0$.
2. Assume a solution of the form $x(t) = e^{\lambda t}$.
3. Calculate the first and second derivatives: $\dot{x}(t) = \lambda e^{\lambda t}$ and $\ddot{x}(t) = \lambda^2 e^{\lambda t}$.
4. Substitute these into the ODE: $m(\lambda^2 e^{\lambda t}) + c(\lambda e^{\lambda t}) + k(e^{\lambda t}) = 0$.
5. Factor out $e^{\lambda t}$: $e^{\lambda t}(m\lambda^2 + c\lambda + k) = 0$. Since $e^{\lambda t} \neq 0$, we must have the characteristic equation: $m\lambda^2 + c\lambda + k = 0$.
6. Apply the quadratic formula to find the roots $\lambda$: $$\lambda = \frac{-c \pm \sqrt{c^2 - 4mk}}{2m}$$
7. This can be rewritten as: $$\lambda = -\frac{c}{2m} \pm \sqrt{(\frac{c}{2m})^2 - \frac{k}{m}}$$

**Reference:** start_page=8 end_page=8
### **Solution for Overdamped System (Case I)**
**Stub:** Derive the general solution for an overdamped mass-damper-spring system, $x(t) = c_1 e^{\lambda_1 t} + c_2 e^{\lambda_2 t}$ with constants $c_1, c_2$ determined by initial conditions.

**Steps:**
1. For Case I (Overdamped), the discriminant is positive: $(\frac{c}{2m})^2 - \frac{k}{m} > 0$. This yields two distinct real roots for $\lambda$: $\lambda_1 = -\frac{c}{2m} + \sqrt{(\frac{c}{2m})^2 - \frac{k}{m}}$ and $\lambda_2 = -\frac{c}{2m} - \sqrt{(\frac{c}{2m})^2 - \frac{k}{m}}$.
2. The general solution is a linear combination of these exponential terms: $x(t) = c_1 e^{\lambda_1 t} + c_2 e^{\lambda_2 t}$.
3. Apply initial condition $x(0) = x_0$: $x_0 = c_1 e^0 + c_2 e^0 \Rightarrow x_0 = c_1 + c_2$.
4. Calculate the derivative: $\dot{x}(t) = c_1 \lambda_1 e^{\lambda_1 t} + c_2 \lambda_2 e^{\lambda_2 t}$.
5. Apply initial condition $\dot{x}(0) = \dot{x}_0$: $\dot{x}_0 = c_1 \lambda_1 + c_2 \lambda_2$.
6. Solving the system of linear equations for $c_1$ and $c_2$ using Cramer's rule or substitution:
7. $$c_1 = \frac{x_0 \lambda_2 - \dot{x}_0}{\lambda_2 - \lambda_1}$$
8. $$c_2 = \frac{\dot{x}_0 - \lambda_1 x_0}{\lambda_2 - \lambda_1}$$
9. Substitute $c_1$ and $c_2$ back into the general solution to get the full expression for $x(t)$ for the overdamped case.

**Reference:** start_page=9 end_page=9
### **Solution for Critically Damped System with Initial Conditions**
**Stub:** Derive the displacement function $$x(t)$$ for a critically damped system given initial displacement $$X_0$$ and initial velocity $$\dot{X}_0$$.

**Steps:**
1. Define the condition for a critically damped system: $$c^2/(4m) = k/m$$.
2. The characteristic equation roots are given by $$\lambda = -c/(2m) \pm \sqrt{c^2/(4m^2) - k/m}$$.
3. Applying the critically damped condition ($$c^2/(4m) = k/m$$), the term under the square root becomes zero, leading to repeated roots: $$\lambda_1, \lambda_2 = -c/(2m)$$.
4. The general solution for a critically damped system is: $$x(t) = (C_1 + C_2 t)e^{-ct/(2m)}$$.
5. Differentiate the general solution to find the velocity: $$\dot{x}(t) = C_2 e^{-ct/(2m)} - (c/(2m))e^{-ct/(2m)}(C_1 + C_2 t)$$.
6. Apply the initial condition for displacement at $$t=0$$: $$x(0) = X_0 = C_1$$.
7. Apply the initial condition for velocity at $$t=0$$: $$\dot{x}(0) = \dot{X}_0 = C_2 - (c/(2m))C_1$$.
8. Substitute $$C_1 = X_0$$ into the initial velocity equation and solve for $$C_2$$: $$C_2 = \dot{X}_0 + (c/(2m))X_0$$.
9. Substitute the expressions for $$C_1$$ and $$C_2$$ back into the general solution to obtain the particular solution: $$x(t) = \left( X_0 + \left( \dot{X}_0 + \frac{c}{2m} X_0 \right) t \right) e^{-ct/(2m)}$$.
10. The accompanying graph illustrates the exponential decay of displacement over time for a critically damped system.

**Reference:** start_page=18 end_page=18
### **Solution of a Second-Order Homogeneous ODE with Initial Conditions**
**Stub:** Derive the particular solution x(t) for the differential equation $$\ddot{x} + 5\dot{x} + 4x = 0$$ with $$x(0)=1$$ and $$\dot{x}(0)=0$$.

**Steps:**
1. The problem begins with the second-order linear homogeneous differential equation $$\ddot{x} + 5\dot{x} + 4x = 0$$ and initial conditions $$x(0)=1$$ and $$\dot{x}(0)=0$$.
2. Assume a solution of the form $$x = e^{\lambda t}$$, then its derivatives are $$\dot{x}(t) = \lambda e^{\lambda t}$$ and $$\ddot{x}(t) = \lambda^2 e^{\lambda t}$$.
3. Substituting these into the differential equation yields the characteristic equation: $$\lambda^2 + 5\lambda + 4 = 0$$.
4. Factoring the characteristic equation gives $$(\lambda+4)(\lambda+1)=0$$, leading to the distinct real roots $$\lambda = -4$$ and $$\lambda = -1$$.
5. The general solution for $$x(t)$$ is thus $$x(t) = c_1 e^{-t} + c_2 e^{-4t}$$ (labeled as the general solution).
6. The derivative of the general solution is $$\dot{x}(t) = -c_1 e^{-t} - 4c_2 e^{-4t}$$.
7. Applying the initial conditions $$x(0)=1$$ and $$\dot{x}(0)=0$$ forms a system of linear equations for $$c_1$$ and $$c_2$$: $$c_1 + c_2 = 1$$ and $$-c_1 - 4c_2 = 0$$.
8. Solving for $$c_1$$ using Cramer's rule, as shown: $$c_1 = \frac{\begin{vmatrix} 1 & 1 \\ 0 & 4 \end{vmatrix}}{3} = \frac{4}{3}$$.
9. Solving for $$c_2$$ using Cramer's rule, as shown: $$c_2 = \frac{\begin{vmatrix} 1 & 1 \\ -1 & 0 \end{vmatrix}}{3} = \frac{1}{3}$$.
10. Substituting the determined constants $$c_1 = 4/3$$ and $$c_2 = 1/3$$ into the general solution yields the particular solution: $$x(t) = \frac{4}{3} e^{-t} + \frac{1}{3} e^{-4t}$$.

**Reference:** start_page=19 end_page=19
### **Transformation of Second-Order ODE to State-Space and Eigenvalue Problem Setup**
**Stub:** Convert a second-order ordinary differential equation into a system of first-order differential equations in state-space form, and set up the eigenvalue problem for its solution.

**Steps:**
1. Start with the given second-order differential equation: $$\ddot{x} + 5\dot{x} + 4x = 0$$
2. Define state variables: $$x_1 = x$$ and $$x_2 = \dot{x}$$.
3. From the definition of $$x_2$$, it follows that $$\dot{x_1} = x_2$$.
4. Since $$x_2 = \dot{x}$$, then $$\dot{x_2} = \ddot{x}$$.
5. Substitute the state variables and their derivatives back into the original differential equation: $$\dot{x_2} + 5x_2 + 4x_1 = 0$$.
6. Rearrange the equation for $$\dot{x_2}$$: $$\dot{x_2} = -4x_1 - 5x_2$$.
7. Combine the first-order equations into a system:
8. $$\begin{cases} \dot{x_1} = x_2 \\ \dot{x_2} = -4x_1 - 5x_2 \end{cases}$$
9. Express the system of first-order differential equations in matrix form:
10. $$\begin{bmatrix} \dot{x_1} \\ \dot{x_2} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -4 & -5 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$$
11. Assume solutions of the form $$x_1 = X_1 e^{\lambda t}$$ and $$x_2 = X_2 e^{\lambda t}$$. The goal is to solve for $$\lambda$$, $$X_1$$, and $$X_2$$.
12. Differentiate the assumed solutions with respect to $$t$$: $$\dot{x_1} = X_1 \lambda e^{\lambda t}$$ and $$\dot{x_2} = X_2 \lambda e^{\lambda t}$$.
13. Substitute the assumed solutions and their derivatives into the matrix equation:
14. $$\begin{bmatrix} X_1 \lambda e^{\lambda t} \\ X_2 \lambda e^{\lambda t} \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -4 & -5 \end{bmatrix} \begin{bmatrix} X_1 e^{\lambda t} \\ X_2 e^{\lambda t} \end{bmatrix}$$
15. Factor out $$e^{\lambda t}$$ from both sides and simplify to obtain the eigenvalue problem:
16. $$\lambda \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ -4 & -5 \end{bmatrix} \begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$$

**Reference:** start_page=20 end_page=20
### **Eigenvalue Calculation for a 2x2 Matrix**
**Stub:** Derive the eigenvalues for the matrix A where $A = \begin{pmatrix} 0 & 1 \\ -4 & -5 \end{pmatrix}$.

**Steps:**
1. Start with the eigenvalue equation: $\lambda \begin{pmatrix} X_1 \\ X_2 \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ -4 & -5 \end{pmatrix} \begin{pmatrix} X_1 \\ X_2 \end{pmatrix}$.
2. Rewrite the equation by introducing the identity matrix: $\begin{pmatrix} \lambda & 0 \\ 0 & \lambda \end{pmatrix} \begin{pmatrix} X_1 \\ X_2 \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ -4 & -5 \end{pmatrix} \begin{pmatrix} X_1 \\ X_2 \end{pmatrix}$.
3. Rearrange the equation to the form $(A - \lambda I)X = 0$: $$\left( \begin{pmatrix} 0 & 1 \\ -4 & -5 \end{pmatrix} - \begin{pmatrix} \lambda & 0 \\ 0 & \lambda \end{pmatrix} \right) \begin{pmatrix} X_1 \\ X_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$
4. Simplify the matrix subtraction to get the characteristic matrix: $$\begin{pmatrix} -\lambda & 1 \\ -4 & -5-\lambda \end{pmatrix} \begin{pmatrix} X_1 \\ X_2 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$
5. For a non-trivial solution for $X = \begin{pmatrix} X_1 \\ X_2 \end{pmatrix}$, the determinant of the characteristic matrix must be zero: $$\begin{vmatrix} -\lambda & 1 \\ -4 & -5-\lambda \end{vmatrix} = 0$$
6. Calculate the determinant: $(-\lambda)(-5-\lambda) - (1)(-4) = 0$.
7. Expand the expression: $5\lambda + \lambda^2 + 4 = 0$, which is the characteristic polynomial.
8. Rearrange to standard quadratic form: $\lambda^2 + 5\lambda + 4 = 0$.
9. Factor the quadratic equation: $(\lambda + 4)(\lambda + 1) = 0$.
10. Solve for $\lambda$ to find the eigenvalues: $\lambda = -4, \lambda = -1$.

**Reference:** start_page=21 end_page=21
### **Solving a System of Linear Differential Equations with Initial Conditions**
**Stub:** Derive the particular solution to a system of linear differential equations using eigenvalues, eigenvectors, and initial conditions.

**Steps:**
1. For eigenvalue $\lambda = -1$: The system for the eigenvector is given by the matrix equation $$ \begin{bmatrix} 1 & 1 \\ -4 & -4 \end{bmatrix} \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$ This implies $X_1 + X_2 = 0$. Setting $X_1 = 1$ yields $X_2 = -1$. The corresponding solution component is $$\begin{bmatrix} 1 \\ -1 \end{bmatrix} e^{-t} $$
2. For eigenvalue $\lambda = -4$: The system for the eigenvector is given by the matrix equation $$ \begin{bmatrix} 4 & 1 \\ -4 & -1 \end{bmatrix} \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$ This implies $4X_1 + X_2 = 0$. Setting $X_1 = 1$ yields $X_2 = -4$. The corresponding solution component is $$\begin{bmatrix} 1 \\ -4 \end{bmatrix} e^{-4t} $$
3. The general solution, which is a linear combination of the individual solution components, is: $$ \begin{bmatrix} X_1 \\ X_2 \end{bmatrix} = C_1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} e^{-t} + C_2 \begin{bmatrix} 1 \\ -4 \end{bmatrix} e^{-4t} $$
4. Initial Conditions: The problem specifies initial conditions $X(0) = X_0$ and $\dot{X}(0) = \dot{X}_0$. Specifically, the initial state vector is given as $$\begin{bmatrix} X_1(0) \\ X_2(0) \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} $$
5. Applying Initial Conditions to find $C_1$ and $C_2$: Substitute $t=0$ into the general solution and equate it to the initial condition vector: $$ C_1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} + C_2 \begin{bmatrix} 1 \\ -4 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} $$ This system is then represented by the matrix equation: $$ \begin{bmatrix} 1 & 4 \\ -1 & -1 \end{bmatrix} \begin{bmatrix} C_1 \\ C_2 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix} $$ From solving this system, the constants are found to be $C_1 = 4/3$ and $C_2 = 1/3$.
6. Particular Solution: Substitute the calculated values of $C_1$ and $C_2$ back into the general solution to obtain the particular solution: $$ \begin{bmatrix} X_1(t) \\ X_2(t) \end{bmatrix} = \frac{4}{3} \begin{bmatrix} 1 \\ -1 \end{bmatrix} e^{-t} + \frac{1}{3} \begin{bmatrix} 1 \\ -4 \end{bmatrix} e^{-4t} $$ The final expression for $X_1(t)$ is: $$ X_1(t) = \frac{4}{3} e^{-t} + \frac{1}{3} e^{-4t} $$

**Reference:** start_page=22 end_page=22
### **Solving a System of Linear ODEs by Diagonalization**
**Stub:** Derive the solution for the system $\dot{x} = Ax$ using matrix diagonalization.

**Steps:**
1. Define the matrix $A = \begin{pmatrix} 0 & 1 \\ -4 & 5 \end{pmatrix}$ and its diagonal decomposition $A = V \Lambda V^{-1}$. The decomposition is given as $A = \frac{1}{3} \begin{pmatrix} 1 & -1 \\ 1 & 4 \end{pmatrix} \begin{pmatrix} -1 & 0 \\ 0 & -4 \end{pmatrix} \begin{pmatrix} 4 & 1 \\ -1 & -1 \end{pmatrix}$. This is noted as the "Diagonal Decomposition of A."
2. Calculate the inverse of the matrix $V$: $V^{-1} = -\frac{1}{3} \begin{pmatrix} -4 & -1 \\ -1 & 1 \end{pmatrix} = \begin{pmatrix} 4/3 & 1/3 \\ 1/3 & -1/3 \end{pmatrix} = \frac{1}{3} \begin{pmatrix} 4 & 1 \\ 1 & -1 \end{pmatrix}$.
3. Consider the system of linear ordinary differential equations: $\dot{x} = Ax$.
4. Introduce a change of variables by letting $x = Vy$.
5. Differentiate $x$ with respect to time to get $\dot{x} = V\dot{y}$.
6. Substitute $\dot{x}$ and $x$ into the original system: $V\dot{y} = AVy$.
7. Multiply both sides by $V^{-1}$ from the left: $V^{-1}V\dot{y} = V^{-1}AVy \implies I\dot{y} = V^{-1}AVy \implies \dot{y} = V^{-1}AVy$.
8. Recall that if $A = V \Lambda V^{-1}$, then $\Lambda = V^{-1}AV$. This is shown as $V^{-1}AV = V^{-1}(V \Lambda V^{-1})V = (V^{-1}V)\Lambda(V^{-1}V) = I\Lambda I = \Lambda$.
9. Substitute $\Lambda$ into the transformed system: $\dot{y} = \Lambda y$.
10. Using the identified diagonal matrix $\Lambda = \begin{pmatrix} -1 & 0 \\ 0 & -4 \end{pmatrix}$, the system becomes $\begin{pmatrix} \dot{y}_1 \\ \dot{y}_2 \end{pmatrix} = \begin{pmatrix} -1 & 0 \\ 0 & -4 \end{pmatrix} \begin{pmatrix} y_1 \\ y_2 \end{pmatrix}$.
11. This uncouples into two separate first-order linear differential equations: $\dot{y}_1 = -y_1$ and $\dot{y}_2 = -4y_2$.
12. Solve these differential equations: $y_1(t) = C_1 e^{-t}$ and $y_2(t) = C_2 e^{-4t}$.
13. The solution for $y(t)$ is therefore: $y(t) = \begin{pmatrix} C_1 e^{-t} \\ C_2 e^{-4t} \end{pmatrix}$.

**Reference:** start_page=23 end_page=23


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** For a mass-damper-spring system described by the equation mx'' + cx' + kx = 0, which condition on the system parameters (m, c, k) leads to an underdamped response?

**Topics:** Damping types, Second-order linear ODEs, Characteristic equation

**Options:**
- c^2 - 4km > 0
- c^2 - 4km = 0
- ✅ c^2 - 4km < 0
- c = 0

**Explanation:** The nature of the damping (overdamped, critically damped, or underdamped) is determined by the discriminant of the characteristic equation, which is c^2 - 4km. An underdamped system occurs when the discriminant is negative (c^2 - 4km < 0), leading to complex conjugate roots and oscillatory decay.

**Reference:** start_page=3 end_page=3
### **Conceptual Question**
**Question:** What is the general form of the solution x(t) for an overdamped mass-damper-spring system (mx'' + cx' + kx = 0)?

**Topics:** Overdamped systems, General solution, Exponential functions

**Options:**
- x(t) = (c1 + c2t)e^(λt)
- x(t) = e^(-ct/(2m)) (A cos(ωdt) + B sin(ωdt))
- ✅ x(t) = c1e^(λ1t) + c2e^(λ2t), where λ1 and λ2 are distinct real roots.
- x(t) = A cos(ωt) + B sin(ωt)

**Explanation:** In an overdamped system (Case I), the characteristic equation yields two distinct real roots (λ1, λ2) because c^2 - 4km > 0. The general solution is a linear combination of two exponential functions, x(t) = c1e^(λ1t) + c2e^(λ2t), indicating a decay to equilibrium without oscillation.

**Reference:** start_page=4 end_page=4
### **Conceptual Question**
**Question:** A mass-damper-spring system returns to its equilibrium position as quickly as possible without oscillating. Which type of damping is this system exhibiting?

**Topics:** Damping characteristics, System response, Critically damped

**Options:**
- Overdamped
- Underdamped
- ✅ Critically Damped
- Undamped

**Explanation:** A critically damped system (Case III) is characterized by the fastest possible return to equilibrium without any oscillations. This occurs when the discriminant of the characteristic equation is exactly zero (c^2 - 4km = 0), leading to repeated real roots.

**Reference:** start_page=6 end_page=6
