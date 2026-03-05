# Lecture Source: Lecture_01_29.pdf

## Fourier Series and Applications

**Lecture Type:** mixed

### Summary

This lecture introduces the concept of Fourier series, a method for representing periodic functions as a sum of sines and cosines. It covers the derivation of the Fourier coefficients, explores how properties of even and odd functions can simplify these calculations, and demonstrates the application of Fourier series to analyze specific periodic waveforms and solve ordinary differential equations with periodic inputs.

### Core Topics

- Fourier series representation
- Periodic functions
- Fourier coefficients
- Even and odd functions
- Square wave
- Sawtooth wave
- Application to differential equations

### Learning Objectives

1. Define a Fourier series for a periodic function
2. Derive the formulas for Fourier coefficients (a0, ak, bk)
3. Utilize properties of even and odd functions to simplify Fourier series calculations
4. Calculate Fourier series for common periodic functions like square and sawtooth waves
5. Apply Fourier series to solve ordinary differential equations with periodic forcing functions

### Assumed Prerequisites

- Calculus (integration, differentiation)
- Basic differential equations
- Understanding of trigonometric functions

## Derivations

### **Fourier Series Coefficients for Even Functions**

**Stub:** Derivation of Fourier series coefficients ($a_0$, $a_k$, $b_k$) for an even function $f(t)$.

**Steps:**

1. An even function is defined by the property $f(t) = f(-t)$.
2. The image shows a graphical representation of an even function, symmetric about the y-axis.
3. The DC component $a_0$ for an even function is given by: $$a_0 = \frac{2}{T} \int_0^{T/2} f(t) dt$$
4. The cosine coefficients $a_k$ for an even function are given by: $$a_k = \frac{4}{T} \int_0^{T/2} f(t) \cos \left( \frac{k 2\pi t}{T} \right) dt$$
5. The sine coefficients $b_k$ for an even function are zero: $$b_k = 0$$

**Reference:** start_page=1 end_page=1

### **Fourier Series Coefficients for Odd Functions**

**Stub:** Derivation of Fourier series coefficients ($a_0$, $a_k$, $b_k$) for an odd function $f(t)$.

**Steps:**

1. An odd function is defined by the property $f(t) = -f(-t)$.
2. The image shows a graphical representation of an odd function, symmetric about the origin.
3. The DC component $a_0$ for an odd function is zero: $$a_0 = 0$$
4. The cosine coefficients $a_k$ for an odd function are zero: $$a_k = 0$$
5. The sine coefficients $b_k$ for an odd function are given by: $$b_k = \frac{4}{T} \int_0^{T/2} f(t) \sin \left( \frac{k 2\pi t}{T} \right) dt$$

**Reference:** start_page=1 end_page=1

### **Fourier Series Expansion of an Odd Piecewise Function**

**Stub:** Derive the Fourier series expansion for a given piecewise odd function f(t).

**Steps:**

1. Define the piecewise odd function f(t) with period T as shown in the graph and explicitly:
2. $$ f(t) = \begin{cases} 0 & -\frac{T}{2} < t < -a \\ -1 & -a < t < 0 \\ 1 & 0 < t < a \\ 0 & a < t < \frac{T}{2} \end{cases} $$
3. Since f(t) is an odd function, the Fourier coefficients a_0 and a_k are zero:
4. $$ a_0 = 0, a_k = 0 $$
5. The Fourier sine coefficient b_k for an odd function is given by:
6. $$ b_k = \frac{4}{T} \int_0^{T/2} f(t) \sin\left(\frac{k 2\pi t}{T}\right) dt $$
7. Substitute the definition of f(t) for 0 < t < T/2, splitting the integral into regions where f(t) is 1 and 0:
8. $$ b_k = \frac{4}{T} \left[ \int_0^{a} (1) \sin\left(\frac{k 2\pi t}{T}\right) dt + \int_a^{T/2} (0) \sin\left(\frac{k 2\pi t}{T}\right) dt \right] $$
9. Evaluate the non-zero integral:
10. $$ b_k = \frac{4}{T} \left[ -\frac{\cos\left(\frac{k 2\pi t}{T}\right)}{\frac{k 2\pi}{T}} \right]\_0^a $$
11. Simplify the expression and apply the limits of integration:
12. $$ b_k = \frac{4}{T} \left( -\frac{T}{k 2\pi} \right) \left[ \cos\left(\frac{k 2\pi t}{T}\right) \right]\_0^a = -\frac{2}{k\pi} \left( \cos\left(\frac{k 2\pi a}{T}\right) - \cos(0) \right) $$
13. Further simplify the b_k coefficient:
14. $$ b_k = \frac{2}{k\pi} \left( 1 - \cos\left(\frac{k 2\pi a}{T}\right) \right) $$
15. Substitute the b_k coefficients into the general Fourier sine series for an odd function:
16. $$ f(t) = \sum*{k=1}^{\infty} b_k \sin\left(\frac{k 2\pi t}{T}\right) = \sum*{k=1}^{\infty} \frac{2}{k\pi} \left( 1 - \cos\left(\frac{k 2\pi a}{T}\right) \right) \sin\left(\frac{k 2\pi t}{T}\right) $$
17. The explicit expansion for a specific case (e.g., when 1 - cos(k 2\[Pi] a / T) simplifies to 2 for odd k, and 0 for even k) is:
18. $$ f(t) = \frac{2}{\pi} \cdot 2 \sin\frac{2\pi t}{T} + \frac{2}{3\pi} \cdot 2 \sin\frac{3 \cdot 2\pi t}{T} + \frac{2}{5\pi} \cdot 2 \sin\frac{5 \cdot 2\pi t}{T} + \dots $$

**Reference:** start_page=5 end_page=5

### **Fourier Sine Series for a Rectangular Pulse**

**Stub:** Derive the Fourier sine series coefficients $b_k$ for a rectangular pulse function $f(t)$ and express $f(t)$ as a Fourier series.

**Steps:**

1. Start with the general formula for the Fourier sine coefficient $b_k$ for a function $f(t)$ defined over $[0, T/2]$:
2. $$b_k = \frac{4}{T} \int_{0}^{T/2} f(t) \sin\left(k \frac{2\pi t}{T}\right) dt$$
3. Assume $f(t)$ is a rectangular pulse, such that $f(t)=1$ for $0 \le t \le a$ and $f(t)=0$ for $a < t \le T/2$. Split the integral into two parts based on the function definition:
4. $$b_k = \frac{4}{T} \left[ \int_{0}^{a} (1) \sin\left(k \frac{2\pi t}{T}\right) dt + \int_{a}^{T/2} (0) \sin\left(k \frac{2\pi t}{T}\right) dt \right]$$
5. Evaluate the first integral. The second integral term becomes zero:
6. $$b_k = \frac{4}{T} \left[ \left. -\frac{\cos\left(k \frac{2\pi t}{T}\right)}{k \frac{2\pi}{T}} \right|_{0}^{a} \right]$$
7. Apply the limits of integration $(t=a)$ and $(t=0)$:
8. $$b_k = \frac{4}{T} \left[ -\frac{T}{k 2\pi} \left( \cos\left(k \frac{2\pi a}{T}\right) - \cos(0) \right) \right]$$
9. Simplify the expression, noting that $\cos(0) = 1$:
10. $$b_k = \frac{4}{T} \left[ -\frac{T}{k 2\pi} \left( \cos\left(k \frac{2\pi a}{T}\right) - 1 \right) \right]$$
11. Further simplify to obtain the final expression for $b_k$:
12. $$b_k = \frac{2}{k\pi} \left[ 1 - \cos\left(k \frac{2\pi a}{T}\right) \right]$$
13. Express $f(t)$ as a Fourier sine series using the derived $b_k$ coefficients:
14. $$f(t) = \sum_{k=1}^{\infty} b_k \sin\left(k \frac{2\pi t}{T}\right)$$
15. Substitute the derived expression for $b_k$ into the series:
16. $$f(t) = \sum_{k=1}^{\infty} \frac{2}{k\pi} \left(1 - \cos\left(k \frac{2\pi a}{T}\right)\right) \sin\left(k \frac{2\pi t}{T}\right)$$
17. Expand the first few terms of the series to illustrate the pattern:
18. $$f(t) = \frac{2}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}\right)\right) \sin\left(\frac{2\pi t}{T}\right) + \frac{2}{2\pi} \left(1 - \cos\left(2 \frac{2\pi a}{T}\right)\right) \sin\left(2 \frac{2\pi t}{T}\right) + \frac{2}{3\pi} \left(1 - \cos\left(3 \frac{2\pi a}{T}\right)\right) \sin\left(3 \frac{2\pi t}{T}\right) + \dots$$

**Reference:** start_page=3 end_page=3

### **Fourier Series Expansion of a Rectangular Pulse Forcing Function**

**Stub:** Express the periodic forcing function $T_0(t)$ as a Fourier series.

**Steps:**

1. The problem involves a first-order linear differential equation with a periodic forcing term $T_0(t)$: $$\frac{dT}{dt} + kT = k T_0(t)$$
2. The forcing function $T_0(t)$ consists of an average value $\bar{T_0}$ and a periodic component $f(t)$. Based on the accompanying diagram, the periodic component $f(t)$ is a rectangular pulse defined over a period $T$ as:
3. $$f(t) = T_a \quad \text{for} \quad 0 < t < a$$ $$f(t) = -T_a \quad \text{for} \quad -a < t < 0$$ $$f(t) = 0 \quad \text{for} \quad a < t < T/2 \quad \text{and} \quad -T/2 < t < -a$$
4. The Fourier series representation for $T_0(t)$ (which is $\bar{T_0} + f(t)$) is then given as:
5. $$T_0(t) = \bar{T_0} + T_a \frac{2}{\pi} \left(1 - \cos \frac{2\pi a}{T}\right) \sin \frac{2\pi t}{T} + \frac{1}{\pi} T_a \left(1 - \cos \frac{2 \cdot 2\pi a}{T}\right) \sin \frac{2 \cdot 2\pi t}{T} + \frac{2}{3\pi} T_a \left(1 - \cos \frac{3 \cdot 2\pi a}{T}\right) \sin \frac{3 \cdot 2\pi t}{T} + \dots$$

**Reference:** start_page=6 end_page=6

### **Steady-State Solution of First-Order ODE with Sinusoidal Forcing**

**Stub:** State the steady-state solution for a first-order ODE with a sinusoidal forcing term.

**Steps:**

1. Consider a first-order linear differential equation with a constant term and a sinusoidal forcing term:
2. $$\frac{dT}{dt} + kT = k \bar{T_0} + k T_a \sin(\omega_0 t)$$
3. The steady-state solution for $T(t)$ (valid for $t > 5/k$) is known to be:
4. $$T(t) = \bar{T_0} + \frac{k}{\sqrt{k^2 + \omega_0^2}} T_a \sin(\omega_0 t - \phi)$$
5. $$\text{where} \quad \phi = \tan^{-1}\left(\frac{\omega_0}{k}\right)$$

**Reference:** start_page=6 end_page=6

### **Fourier Series Definition and Coefficients**

**Stub:** Define the Fourier series for a periodic function and derive its coefficients ($a_0$, $a_k$, $b_k$).

**Steps:**

1. Let $f(t)$ be a periodic function with period $T$.
2. The Fourier Series representation of $f(t)$ is given by: $$f(t) = a_0 + a_1 \cos\left(\frac{2\pi t}{T}\right) + a_2 \cos\left(\frac{2 \cdot 2\pi t}{T}\right) + \dots + b_1 \sin\left(\frac{2\pi t}{T}\right) + b_2 \sin\left(\frac{2 \cdot 2\pi t}{T}\right) + \dots$$
3. This can be written in a compact summation form as: $$f(t) = a_0 + \sum_{k=1}^{\infty} \left(a_k \cos\left(\frac{k \cdot 2\pi t}{T}\right) + b_k \sin\left(\frac{k \cdot 2\pi t}{T}\right)\right)$$
4. The DC component or average value, $a_0$, is given by: $$a_0 = \frac{1}{T} \int_{-T/2}^{T/2} f(t) dt$$
5. The cosine coefficients, $a_k$, are given by: $$a_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \cos\left(\frac{k \cdot 2\pi t}{T}\right) dt$$
6. The sine coefficients, $b_k$, are given by: $$b_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \sin\left(\frac{k \cdot 2\pi t}{T}\right) dt$$

**Reference:** start_page=1 end_page=1

### **Fourier Series Coefficients for Even Functions**

**Stub:** Derive the Fourier series coefficients ($a_0$, $a_k$, $b_k$) for a periodic even function $f(t)$.

**Steps:**

1. An even function $f(t)$ satisfies the property $$f(t) = f(-t)$$
2. Graphically, an even function is symmetric about the y-axis, as shown in the accompanying figure.
3. For an even function, the DC component $a_0$ is given by the integral over half the period: $$a_0 = \frac{2}{T} \int_0^{T/2} f(t) dt$$
4. The cosine coefficients $a_k$ are given by the integral over half the period: $$a_k = \frac{4}{T} \int_0^{T/2} f(t) \cos\left(k \frac{2\pi t}{T}\right) dt$$
5. The sine coefficients $b_k$ are zero for an even function: $$b_k = 0$$

**Reference:** start_page=2 end_page=2

### **Fourier Series Coefficients for Odd Functions**

**Stub:** Derive the Fourier series coefficients ($a_0$, $a_k$, $b_k$) for a periodic odd function $f(t)$.

**Steps:**

1. An odd function $f(t)$ satisfies the property $$f(t) = -f(-t)$$
2. Graphically, an odd function is symmetric about the origin, as shown in the accompanying figure.
3. For an odd function, the DC component $a_0$ is zero: $$a_0 = 0$$
4. The cosine coefficients $a_k$ are zero for an odd function: $$a_k = 0$$
5. The sine coefficients $b_k$ are given by the integral over half the period: $$b_k = \frac{4}{T} \int_0^{T/2} f(t) \sin\left(k \frac{2\pi t}{T}\right) dt$$

**Reference:** start_page=2 end_page=2

### **Fourier Series Definition and Coefficients**

**Stub:** Define a periodic function $f(t)$ using a Fourier Series and provide the integral expressions for its coefficients $a_0$, $a_k$, and $b_k$.

**Steps:**

1. Let $f(t)$ be a periodic function with period $T$.
2. The Fourier series representation of $f(t)$ is given by: $$f(t) = a_0 + a_1 \cos\frac{2\pi t}{T} + a_2 \cos\frac{2 \cdot 2\pi t}{T} + \dots + b_1 \sin\frac{2\pi t}{T} + b_2 \sin\frac{2 \cdot 2\pi t}{T} + \dots$$
3. This can be written in a compact summation form as: $$ = a*0 + \sum*{k=1}^{\infty} \left( a_k \cos\frac{k 2\pi t}{T} + b_k \sin\frac{k 2\pi t}{T} \right)$$
4. The coefficient $a_0$ is calculated by: $$a_0 = \frac{1}{T} \int_{-T/2}^{T/2} f(t) dt$$
5. The cosine coefficients $a_k$ are given by: $$a_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \cos\frac{k 2\pi t}{T} dt$$
6. The sine coefficients $b_k$ are given by: $$b_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \sin\frac{k 2\pi t}{T} dt$$

**Reference:** start_page=1 end_page=1

### **Fourier Series Coefficients for Even Functions**

**Stub:** Simplified expressions for Fourier series coefficients ($a_0$, $a_k$, $b_k$) when the function $f(t)$ is even.

**Steps:**

1. An even function $f(t)$ is defined by the property $f(t) = f(-t)$. A graphical representation shows symmetry about the vertical axis.
2. For an even function, the DC component $a_0$ is given by the integral: $$a_0 = \frac{2}{T} \int_{0}^{T/2} f(t) dt$$
3. The cosine coefficients $a_k$ for an even function are derived as: $$a_k = \frac{4}{T} \int_{0}^{T/2} f(t) \cos \left( k \frac{2\pi t}{T} \right) dt$$
4. The sine coefficients $b_k$ for an even function are zero: $$b_k = 0$$

**Reference:** start_page=2 end_page=2

### **Fourier Series Coefficients for Odd Functions**

**Stub:** Simplified expressions for Fourier series coefficients ($a_0$, $a_k$, $b_k$) when the function $f(t)$ is odd.

**Steps:**

1. An odd function $f(t)$ is defined by the property $f(t) = -f(-t)$. A graphical representation shows anti-symmetry about the origin.
2. For an odd function, the DC component $a_0$ is zero: $$a_0 = 0$$
3. The cosine coefficients $a_k$ for an odd function are zero: $$a_k = 0$$
4. The sine coefficients $b_k$ for an odd function are derived as: $$b_k = \frac{4}{T} \int_{0}^{T/2} f(t) \sin \left( k \frac{2\pi t}{T} \right) dt$$

**Reference:** start_page=2 end_page=2

### **Derivation of Fourier Series Coefficient a_k for a Triangular Wave**

**Stub:** Derive the expression for the Fourier series coefficient $a_k$ for the given triangular wave function $f(t)$.

**Steps:**

1. The function $f(t)$ is defined as $f(t) = \frac{2at}{T}$ for $0 < t < \frac{T}{2}$ and $f(t) = -\frac{2at}{T}$ for $-\frac{T}{2} < t \le 0$. A triangular wave diagram illustrates this function.
2. Since $f(t)$ is an even function, the general formula for the Fourier series coefficient $a_k$ simplifies to $a_k = \frac{4}{T} \int_0^{T/2} f(t) \cos\left(\frac{k2\pi t}{T}\right) dt$.
3. Substitute the expression for $f(t)$ in the interval $0 < t < \frac{T}{2}$: $a_k = \frac{4}{T} \int_0^{T/2} \frac{2at}{T} \cos\left(\frac{k2\pi t}{T}\right) dt$.
4. Simplify the expression: $a_k = \frac{8a}{T^2} \int_0^{T/2} t \cos\left(\frac{k2\pi t}{T}\right) dt$.
5. Apply integration by parts $\int u dv = uv - \int v du$ with $u=t$ and $dv=\cos\left(\frac{k2\pi t}{T}\right) dt$. This yields $du=dt$ and $v=\frac{T}{k2\pi}\sin\left(\frac{k2\pi t}{T}\right)$.
6. The integral becomes: $a_k = \frac{8a}{T^2} \left[ \left. t \frac{T}{k2\pi} \sin\left(\frac{k2\pi t}{T}\right) \right|_0^{T/2} - \int_0^{T/2} \frac{T}{k2\pi} \sin\left(\frac{k2\pi t}{T}\right) dt \right]$.
7. Evaluate the first term: $\left. t \frac{T}{k2\pi} \sin\left(\frac{k2\pi t}{T}\right) \right|_0^{T/2} = \frac{T}{2} \frac{T}{k2\pi} \sin(k\pi) - 0 = 0$, as $\sin(k\pi)=0$ for integer $k$.
8. Integrate the second term: $-\int_0^{T/2} \frac{T}{k2\pi} \sin\left(\frac{k2\pi t}{T}\right) dt = -\frac{T}{k2\pi} \left[ -\frac{T}{k2\pi} \cos\left(\frac{k2\pi t}{T}\right) \right]_0^{T/2}$.
9. Simplify and evaluate: $= \frac{T^2}{(k2\pi)^2} \left[ \cos\left(\frac{k2\pi t}{T}\right) \right]_0^{T/2} = \frac{T^2}{4k^2\pi^2} \left[ \cos(k\pi) - \cos(0) \right]$.
10. Substitute $\cos(k\pi) = (-1)^k$ and $\cos(0)=1$: $a_k = \frac{8a}{T^2} \frac{T^2}{4k^2\pi^2} \left[ (-1)^k - 1 \right]$.
11. Final simplified expression for $a_k$: $a_k = \frac{2a}{k^2\pi^2} \left[ (-1)^k - 1 \right]$.

**Reference:** start_page=9 end_page=9

### **Derivation of Fourier Series Coefficient a_0 for a Triangular Wave**

**Stub:** Derive the expression for the Fourier series coefficient $a_0$ for the given triangular wave function $f(t)$.

**Steps:**

1. The function $f(t)$ is defined as $f(t) = \frac{2at}{T}$ for $0 < t < \frac{T}{2}$.
2. Since $f(t)$ is an even function, the general formula for the Fourier series coefficient $a_0$ simplifies to $a_0 = \frac{2}{T} \int_0^{T/2} f(t) dt$.
3. Substitute $f(t)$: $a_0 = \frac{2}{T} \int_0^{T/2} \frac{2at}{T} dt$.
4. Simplify: $a_0 = \frac{4a}{T^2} \int_0^{T/2} t dt$.
5. Integrate: $a_0 = \frac{4a}{T^2} \left[ \frac{t^2}{2} \right]_0^{T/2}$.
6. Evaluate the limits: $a_0 = \frac{4a}{T^2} \left( \frac{(T/2)^2}{2} - 0 \right) = \frac{4a}{T^2} \frac{T^2/4}{2} = \frac{4a}{T^2} \frac{T^2}{8}$.
7. Final simplified expression for $a_0$: $a_0 = \frac{a}{2}$.

**Reference:** start_page=9 end_page=9

### **Fourier Series Coefficient b_k for an Even Function**

**Stub:** State the value of the Fourier series coefficient $b_k$ for the given even function $f(t)$.

**Steps:**

1. The function $f(t)$ is an even function, as indicated by its definition and the accompanying diagram.
2. For any even function, the Fourier series coefficient $b_k$ is equal to zero.
3. Therefore, $b_k = 0$.

**Reference:** start_page=9 end_page=9

### **Fourier Series Expansion of a Function**

**Stub:** Derive the Fourier cosine series for a function f(t) by calculating coefficients and substituting them into the series.

**Steps:**

1. The Fourier coefficient $a_k$ is given by: $$a_k = \frac{2a}{\pi^2 k^2} [\cos(k\pi) - 1]$$
2. The general form of the Fourier series for $f(t)$, with the $a_k$ expression substituted and assuming $a_0/2 = a/2$, is: $$f(t) = \frac{a}{2} + \sum_{k=1}^{\infty} \frac{2a}{\pi^2 k^2} (\cos(k\pi) - 1) \cos\left(\frac{k 2\pi t}{T}\right)$$
3. Calculate the specific coefficients for odd and even values of $k$:
4. For $k=1$: $a_1 = \frac{2a}{\pi^2} (\cos(\pi) - 1) = \frac{2a}{\pi^2} (-1 - 1) = -\frac{4a}{\pi^2}$
5. For $k=2$: $a_2 = \frac{2a}{\pi^2 (2)^2} (\cos(2\pi) - 1) = \frac{2a}{4\pi^2} (1 - 1) = 0$
6. For $k=3$: $a_3 = \frac{2a}{\pi^2 (3)^2} (\cos(3\pi) - 1) = \frac{2a}{9\pi^2} (-1 - 1) = -\frac{4a}{9\pi^2}$
7. For $k=4$: $a_4 = 0$ (following the pattern for even $k$)
8. For $k=5$: $a_5 = -\frac{4a}{25\pi^2}$ (following the pattern for odd $k$)
9. Substitute the calculated coefficients into the Fourier series expansion for $f(t)$: $$f(t) = \frac{a}{2} - \frac{4a}{\pi^2} \cos\left(\frac{2\pi t}{T}\right) - \frac{4a}{9\pi^2} \cos\left(\frac{3 \cdot 2\pi t}{T}\right) - \frac{4a}{25\pi^2} \cos\left(\frac{5 \cdot 2\pi t}{T}\right) - \dots$$

**Reference:** start_page=10 end_page=10

### **Fourier Series Expansion of a Rectangular Pulse Train**

**Stub:** Derive the Fourier series for the given periodic odd function `f(t)`.

**Steps:**

1. The function `f(t)` is defined piecewise over one period `T`:
2. $$f(t) = \begin{cases} 0 & -T/2 < t < -a \\ -1 & -a < t < 0 \\ 1 & 0 < t < a \\ 0 & a < t < T/2 \end{cases}$$
3. From the graph and the definition, `f(t)` is an odd function, which implies that the DC component `a_0 = 0` and the cosine coefficients `a_k = 0`.
4. The sine coefficients `b_k` for an odd function are given by:
5. $$b_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \sin\left(\frac{2\pi k t}{T}\right) dt$$
6. Since `f(t)` is odd, we can simplify the integral to:
7. $$b_k = \frac{4}{T} \int_{0}^{T/2} f(t) \sin\left(\frac{2\pi k t}{T}\right) dt$$
8. Substitute the definition of `f(t)` for `t > 0`:
9. $$b_k = \frac{4}{T} \left[ \int_{0}^{a} (1) \sin\left(\frac{2\pi k t}{T}\right) dt + \int_{a}^{T/2} (0) \sin\left(\frac{2\pi k t}{T}\right) dt \right]$$
10. The second integral is zero, so:
11. $$b_k = \frac{4}{T} \int_{0}^{a} \sin\left(\frac{2\pi k t}{T}\right) dt$$
12. Integrate with respect to `t`:
13. $$b_k = \frac{4}{T} \left[ -\frac{T}{2\pi k} \cos\left(\frac{2\pi k t}{T}\right) \right]_{0}^{a}$$
14. Evaluate the definite integral:
15. $$b_k = -\frac{4}{T} \frac{T}{2\pi k} \left[ \cos\left(\frac{2\pi k a}{T}\right) - \cos(0) \right]$$
16. $$b_k = -\frac{2}{\pi k} \left[ \cos\left(\frac{2\pi k a}{T}\right) - 1 \right]$$
17. Rearrange the term:
18. $$b_k = \frac{2}{\pi k} \left[ 1 - \cos\left(\frac{2\pi k a}{T}\right) \right]$$
19. The Fourier series for an odd function is given by:
20. $$f(t) = \sum_{k=1}^{\infty} b_k \sin\left(\frac{2\pi k t}{T}\right)$$
21. Substitute the derived `b_k`:
22. $$f(t) = \sum_{k=1}^{\infty} \frac{2}{\pi k} \left( 1 - \cos\left(\frac{2\pi k a}{T}\right) \right) \sin\left(\frac{2\pi k t}{T}\right)$$
23. The provided example shows a specific case (likely `a = T/4`, which makes `cos(2πka/T) = cos(kπ/2)`). If `a = T/4`, then `1 - cos(kπ/2)` is 1 for k=1, 2 for k=2, 1 for k=3, 0 for k=4, etc. The series expansion provided is:
24. $$f(t) = \frac{2}{\pi} \sin\left(\frac{2\pi t}{T}\right) + \frac{2 \cdot 2}{3\pi} \sin\left(\frac{2\pi 3 t}{T}\right) + \frac{2}{5\pi} \sin\left(\frac{2\pi 5 t}{T}\right) + \dots$$

**Reference:** start_page=5 end_page=5

### **Fourier Sine Series Expansion for a Rectangular Pulse**

**Stub:** Derive the Fourier sine series for a function f(t) defined as 1 for 0 < t < a and 0 for a < t < T/2.

**Steps:**

1. The Fourier series coefficient $b_k$ for a half-range sine series is given by:
2. $$b_k = \frac{4}{T} \int_{0}^{T/2} f(t) \sin\left(k \frac{2\pi t}{T}\right) dt$$
3. Substitute the definition of $f(t)$ (1 for $0 < t < a$, and 0 for $a < t < T/2$) into the integral:
4. $$b_k = \frac{4}{T} \left[ \int_{0}^{a} (1) \sin\left(k \frac{2\pi t}{T}\right) dt + \int_{a}^{T/2} (0) \sin\left(k \frac{2\pi t}{T}\right) dt \right]$$
5. Simplify the integral as the second term is zero:
6. $$b_k = \frac{4}{T} \int_{0}^{a} \sin\left(k \frac{2\pi t}{T}\right) dt$$
7. Perform the integration:
8. $$b_k = \frac{4}{T} \left[ -\frac{\cos\left(k \frac{2\pi t}{T}\right)}{k \frac{2\pi}{T}} \right]_{0}^{a}$$
9. Evaluate the definite integral using the limits of integration:
10. $$b_k = \frac{4}{T} \left( -\frac{T}{k 2\pi} \right) \left[ \cos\left(k \frac{2\pi t}{T}\right) \right]_{0}^{a}$$
11. $$b_k = -\frac{2}{k\pi} \left[ \cos\left(k \frac{2\pi a}{T}\right) - \cos(0) \right]$$
12. $$b_k = -\frac{2}{k\pi} \left[ \cos\left(k \frac{2\pi a}{T}\right) - 1 \right]$$
13. Simplify the expression for $b_k$:
14. $$b_k = \frac{2}{k\pi} \left(1 - \cos\left(k \frac{2\pi a}{T}\right)\right)$$
15. State the general formula for the Fourier sine series expansion:
16. $$f(t) = \sum_{k=1}^{\infty} b_k \sin\left(k \frac{2\pi t}{T}\right)$$
17. Substitute the derived expression for $b_k$ into the Fourier series formula:
18. $$f(t) = \sum_{k=1}^{\infty} \frac{2}{k\pi} \left(1 - \cos\left(k \frac{2\pi a}{T}\right)\right) \sin\left(k \frac{2\pi t}{T}\right)$$
19. Expand the first few terms of the series:
20. $$f(t) = \frac{2}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}\right)\right) \sin\left(\frac{2\pi t}{T}\right) + \frac{2}{2\pi} \left(1 - \cos\left(\frac{4\pi a}{T}\right)\right) \sin\left(\frac{4\pi t}{T}\right) + \frac{2}{3\pi} \left(1 - \cos\left(\frac{6\pi a}{T}\right)\right) \sin\left(\frac{6\pi t}{T}\right) + \dots$$

**Reference:** start_page=12 end_page=12

### **Fourier Series Expansion of a Periodic Pulse Function**

**Stub:** Derivation of the Fourier series for a specific piecewise-defined periodic function $T_0(t)$.

**Steps:**

1. The system is described by the first-order linear differential equation: $$ \frac{dT}{dt} + kT = k T_0(t) $$
2. The forcing function $T_0(t)$ is a periodic function, illustrated by a square wave centered at $\bar{T_0}$ with amplitude $T_a$ and period $T$. The function is defined piecewise as: $$ T_0(t) = \bar{T_0} \quad \text{for} \quad -\frac{T}{2} < t < -a $$ $$ T_0(t) = \bar{T_0} - T_a \quad \text{for} \quad -a < t < 0 $$ $$ T_0(t) = \bar{T_0} + T_a \quad \text{for} \quad 0 < t < a $$ $$ T_0(t) = \bar{T_0} \quad \text{for} \quad a < t < \frac{T}{2} $$
3. The Fourier series representation of $T_0(t)$ is given, expanding the periodic function into a sum of sinusoidal components. The series includes the DC component $\bar{T_0}$ and sine terms due to the odd nature of $(T_0(t) - \bar{T_0})$. The first few terms are explicitly shown:
4. $$ T_0(t) = \bar{T_0} + \frac{2 T_a}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}\right)\right) \sin\left(\frac{2\pi t}{T}\right) $$
5. $$ + \frac{1}{\pi} T_a \left(1 - \cos\left(\frac{2 \cdot 2\pi a}{T}\right)\right) \sin\left(\frac{2 \cdot 2\pi t}{T}\right) $$
6. $$ + \frac{2}{3\pi} T_a \left(1 - \cos\left(\frac{3 \cdot 2\pi a}{T}\right)\right) \sin\left(\frac{3 \cdot 2\pi t}{T}\right) + \dots $$

**Reference:** start_page=6 end_page=6

### **Steady-State Response of First-Order System to Sinusoidal Input**

**Stub:** Solution for temperature $T(t)$ in a first-order linear differential equation with a sinusoidal forcing term.

**Steps:**

1. Consider the differential equation with a sinusoidal forcing term: $$ \frac{dT}{dt} + kT = k \bar{T_0} + k T_a \sin(\omega_0 t) $$
2. The steady-state solution for $T(t)$ is obtained as: $$ T(t) = \bar{T_0} + \frac{k}{\sqrt{k^2 + \omega_0^2}} T_a \sin(\omega_0 t - \phi) $$
3. The phase lag $\phi$ is defined as: $$ \phi = \tan^{-1}\left(\frac{\omega_0}{k}\right) $$
4. This solution is valid for the steady-state condition, specifically for $t > 5/k$.

**Reference:** start_page=6 end_page=6

### **Steady-State Temperature Response to Periodic Forcing**

**Stub:** Solution for the temperature `T(t)` given a first-order differential equation with a periodic input `T_0(t)`.

**Steps:**

1. The governing first-order linear differential equation describing the temperature `T` over time `t` is given by: $$ \frac{dT}{dt} + kT = k T_0(t) $$
2. The periodic input temperature `T_0(t)` is expressed as a Fourier series, with its first few terms: $$ T_0(t) = \overline{T_0} + T_a \frac{2}{\pi}(1-\cos \frac{2\pi a}{T}) \sin \frac{2\pi t}{T} + \frac{1}{\pi} (T_a)(1-\cos \frac{2 \cdot 2\pi a}{T}) \sin \frac{2 \cdot 2\pi t}{T} + T_a \frac{2}{3\pi} T_a(1-\cos \frac{3 \cdot 2\pi a}{T}) \sin \frac{3 \cdot 2\pi t}{T} + \dots $$
3. The steady-state solution for `T(t)`, resulting from the periodic input `T_0(t)`, is given by a series with phase shifts: $$ T(t) = \overline{T_0} + \frac{k}{\sqrt{k^2 + (\frac{2\pi}{T})^2}} \frac{2T_a}{\pi}(1-\cos \frac{\pi a}{T}) \sin(\frac{2\pi t}{T} - \phi_1) + \frac{k}{\sqrt{k^2 + (\frac{4\pi}{T})^2}} \frac{T_a}{\pi}(1-\cos \frac{4\pi a}{T}) \sin(\frac{4\pi t}{T} - \phi_2) + \frac{k}{\sqrt{k^2 + (\frac{6\pi}{T})^2}} \frac{2T_a}{3\pi}(1-\cos \frac{6\pi a}{T}) \sin( \frac{6\pi t}{T} - \phi_3) + \dots $$
4. The phase shifts `\phi_n` for each harmonic component are defined as: $$ \phi_1 = \tan^{-1}\frac{2\pi}{Tk} $$ $$ \phi_2 = \tan^{-1}\frac{2 \cdot 2\pi}{Tk} = \tan^{-1}\frac{4\pi}{Tk} $$ $$ \phi_3 = \tan^{-1}\frac{3 \cdot 2\pi}{Tk} = \tan^{-1}\frac{6\pi}{Tk} $$

**Reference:** start_page=14 end_page=14

### **Response of a First-Order System to a Periodic Input using Fourier Series**

**Stub:** Derive the steady-state temperature response T(t) for a first-order system dT/dt + kT = k T_0(t) where T_0(t) is a periodic function represented by a Fourier series.

**Steps:**

1. First, we state the governing first-order linear differential equation and its general solution for a sinusoidal input:
2. $$ \frac{dT}{dt} + kT = k \overline{T_0} + k T_a \sin(\omega_0 t) $$
3. This differential equation has the steady-state solution:
4. $$ T(t) = \overline{T_0} + \frac{k}{\sqrt{k^2 + \omega_0^2}} T_a \sin(\omega_0 t - \phi) $$
5. where the phase shift \phi is given by:
6. $$ \phi = \tan^{-1}\left(\frac{\omega_0}{k}\right) $$
7. Next, we express the periodic input function T_0(t) as a Fourier series, showing the first few terms:
8. $$
   T_0(t) = \overline{T_0} + T_a \frac{2}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}\right)\right) \sin\left(\frac{2\pi t}{T}
   ight)
   $$
9. $$
   + \frac{1}{\pi} T_a \left(1 - \cos\left(2 \cdot \frac{2\pi a}{T}\right)\right) \sin\left(2 \cdot \frac{2\pi t}{T}
   ight)
   $$
10. $$
    + \frac{2}{3\pi} T_a \left(1 - \cos\left(3 \cdot \frac{2\pi a}{T}
    ight)\right) \sin\left(3 \cdot \frac{2\pi t}{T}
    ight) + \dots
    $$
11. Finally, we apply the system's response (from the sinusoidal solution) to each harmonic component of the Fourier series for T_0(t) to obtain the full solution T(t):
12. $$ T(t) = \overline{T_0} $$
13. $$
    + \frac{k}{\sqrt{k^2 + \left(\frac{2\pi}{T}\right)^2}} \frac{2T_a}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}
    ight)\right) \sin\left(\frac{2\pi t}{T} - \phi_1\right)
    $$
14. where the phase shift for the first harmonic is:
15. $$
    \phi_1 = \tan^{-1}\left(\frac{2\pi}{Tk}
    ight)
    $$
16. The second harmonic term in the solution is:
17. $$
    + \frac{k}{\sqrt{k^2 + \left(\frac{4\pi}{T}\right)^2}} \frac{T_a}{\pi} \left(1 - \cos\left(\frac{4\pi a}{T}
    ight)\right) \sin\left(\frac{4\pi t}{T} - \phi_2\right)
    $$
18. where the phase shift for the second harmonic is:
19. $$
    \phi_2 = \tan^{-1}\left(\frac{4\pi}{Tk}
    ight)
    $$
20. The third harmonic term in the solution is:
21. $$
    + \frac{k}{\sqrt{k^2 + \left(\frac{6\pi}{T}
    ight)^2}} \frac{2T_a}{3\pi} \left(1 - \cos\left(\frac{6\pi a}{T}
    ight)\right) \sin\left(\frac{6\pi t}{T} - \phi_3
    ight)
    $$
22. where the phase shift for the third harmonic is:
23. $$
    \phi_3 = \tan^{-1}\left(\frac{6\pi}{Tk}
    ight) + \dots
    $$

**Reference:** start_page=15 end_page=15

## Questions

## Conceptual Questions

### **Conceptual Question**

**Question:** For a periodic function f(t) with period T, if f(t) is an even function, which of the following Fourier series coefficients must be zero?

**Topics:** Fourier Series, Even Functions, Fourier Coefficients

**Options:**

- a_0
- a_k
- ✅ b_k
- Both a_0 and a_k

**Explanation:** For an even function, f(t) = f(-t), the odd components (sine terms) in the Fourier series must vanish. Therefore, all b_k coefficients are zero.

**Reference:** start_page=2 end_page=2

### **Conceptual Question**

**Question:** A Fourier series represents a periodic function f(t) as an infinite sum of which fundamental types of functions?

**Topics:** Fourier Series, Periodic Functions, Trigonometric Functions

**Options:**

- Polynomials and exponential functions.
- Logarithmic and power functions.
- ✅ Constant, cosine, and sine functions.
- Hyperbolic sine and cosine functions.

**Explanation:** The general form of a Fourier series is f(t) = a_0 + sum(a_k cos(k*2*pi*t/T) + b_k sin(k*2*pi*t/T)), showing it's composed of a constant term, cosine terms, and sine terms.

**Reference:** start_page=1 end_page=1

### **Conceptual Question**

**Question:** In the steady-state solution T(t) for a first-order differential equation dT/dt + kT = T_0(t) where T_0(t) is a periodic function described by a Fourier series, how do the frequency components of T(t) relate to those of T_0(t)?

**Topics:** Differential Equations, Steady-State, Fourier Series, Phase Shift

**Options:**

- T(t) will only contain the average value (a_0 term) of T_0(t).
- ✅ T(t) will have the same frequency components as T_0(t), but with modified amplitudes and phase shifts.
- T(t) will have entirely different frequency components compared to T_0(t).
- T(t) will be a constant value, independent of T_0(t)'s periodic nature.

**Explanation:** The solution for T(t) in the steady state is also a Fourier series. Each harmonic of T_0(t) contributes to a corresponding harmonic in T(t), but with its amplitude scaled and a phase shift introduced, as shown in the solution formula on page 7.

**Reference:** start_page=6 end_page=7
