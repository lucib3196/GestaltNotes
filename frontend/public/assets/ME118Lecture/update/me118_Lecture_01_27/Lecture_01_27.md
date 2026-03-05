# Lecture Source: Lecture_01_27.pdf

## First-Order System Response to Periodic Forcing and Fourier Series

**Lecture Type:** derivation-heavy

### Summary
This lecture explores how first-order linear systems respond to time-varying inputs. It details the process of solving first-order differential equations for sinusoidal forcing functions using techniques like integrating factors and complex exponentials to determine the system's steady-state response, including amplitude and phase shift. Additionally, the lecture introduces Fourier series as a powerful tool to represent general periodic functions as a sum of sines and cosines, enabling the analysis of system response to more complex periodic inputs.

### Core Topics
- First-order linear differential equations
- Integrating factors
- Sinusoidal forcing functions
- Complex exponential method
- Homogeneous and particular solutions
- Steady-state response
- Phase shift
- Fourier series
- Fourier coefficients
- Even and odd functions
- Periodic signal decomposition

### Learning Objectives
1. Solve first-order linear ordinary differential equations for sinusoidal forcing functions.
2. Apply the method of integrating factors to solve first-order ODEs.
3. Utilize complex exponentials to determine the steady-state response of a system to sinusoidal inputs.
4. Explain the concepts of amplitude response and phase shift in system analysis.
5. Define and identify even and odd functions and their properties in integration.
6. Derive the formulas for Fourier coefficients (a_0, a_k, b_k).
7. Calculate the Fourier series representation for given periodic functions, such as square waves.

### Assumed Prerequisites
- Differential calculus
- Integral calculus
- Basic complex numbers
- Trigonometric identities


## Derivations

### **Solution of a First-Order Linear Differential Equation with Oscillatory Forcing**
**Stub:** Derive the temperature function $T(t)$ from the differential equation $\frac{dT}{dt} + KT = K T_0(t)$ with the forcing function $T_0(t) = \bar{T_0} + T_a \sin(\omega_0 t)$ and initial condition $T(0) = T_i$.

**Steps:**
1. The initial first-order linear differential equation is given as: $$\frac{dT}{dt} + KT = K T_0(t)$$
2. The forcing function $T_0(t)$ is defined, incorporating a steady component $\bar{T_0}$ and an oscillatory component with amplitude $T_a$ and angular frequency $\omega_0$: $$T_0(t) = \bar{T_0} + T_a \sin(\omega_0 t)$$
3. The initial condition for the temperature at $t=0$ is: $$T(0) = T_i$$
4. Substitute the expression for $T_0(t)$ into the differential equation: $$\frac{dT}{dt} + KT = K \bar{T_0} + K T_a \sin(\omega_0 t)$$
5. Euler's formula is recalled to facilitate the handling of the oscillatory term using complex exponentials: $$e^{j\theta} = \cos\theta + j\sin\theta$$ $$\sin\theta = \text{Im}(e^{j\theta})$$ (The derivation proceeds by replacing $\sin(\omega_0 t)$ with $e^{j\omega_0 t}$, implying a solution for the complex response and taking the imaginary part later, or focusing on a specific complex exponential forcing.)
6. The differential equation is rewritten with the oscillatory term represented by a complex exponential: $$\frac{dT}{dt} + KT = K \bar{T_0} + K T_a e^{j\omega_0 t}$$
7. The integrating factor for the linear first-order ODE is found by $e^{\int K dt}$: $$\text{Integrating factor} = e^{Kt}$$
8. Multiply the entire differential equation by the integrating factor $e^{Kt}$: $$e^{Kt} \frac{dT}{dt} + K T e^{Kt} = K \bar{T_0} e^{Kt} + K T_a e^{j\omega_0 t} e^{Kt}$$
9. The left-hand side is recognized as the derivative of the product $(T e^{Kt})$, and the exponents on the right-hand side are combined: $$\frac{d}{dt}(T e^{Kt}) = K \bar{T_0} e^{Kt} + K T_a e^{(K + j\omega_0)t}$$
10. Integrate both sides of the equation from $t=0$ to $t$: $$\int_{0}^{t} d(T e^{Kt}) = \int_{0}^{t} K \bar{T_0} e^{Kt} dt + \int_{0}^{t} K T_a e^{(K + j\omega_0)t} dt$$
11. Evaluate the definite integrals: $$[T e^{Kt}]_{0}^{t} = K \bar{T_0} \left[ \frac{e^{Kt}}{K} \right]_{0}^{t} + K T_a \left[ \frac{e^{(K + j\omega_0)t}}{K + j\omega_0} \right]_{0}^{t}$$
12. Apply the limits of integration and substitute the initial condition $T(0) = T_i$: $$T(t) e^{Kt} - T(0) e^{K \cdot 0} = \bar{T_0} (e^{Kt} - e^{K \cdot 0}) + \frac{K T_a}{K + j\omega_0} (e^{(K + j\omega_0)t} - e^{(K + j\omega_0) \cdot 0})$$
13. Simplify the expression using $e^0 = 1$ and $T(0) = T_i$: $$T(t) e^{Kt} - T_i = \bar{T_0} (e^{Kt} - 1) + \frac{K T_a}{K + j\omega_0} (e^{(K + j\omega_0)t} - 1)$$

**Reference:** start_page=1 end_page=1
### **Steady-State Temperature Response from Oscillatory Input**
**Stub:** Derive the simplified, real-valued expression for T(t) for t >> 5/k by taking the imaginary part of the complex exponential forcing term.

**Steps:**
1. Start with the initial temperature expression: $$T(t) = T_c e^{-kt} + \bar{T_0}(1-e^{-kt}) + \frac{k}{k+j\omega_0} T_a (e^{j\omega_0 t} - e^{-kt})$$
2. For $$t > 5/k$$, the transient exponential terms $$e^{-kt}$$ decay to zero. The expression for T(t) simplifies to: $$T(t) \approx \bar{T_0} + \frac{k T_a}{k+j\omega_0} e^{j\omega_0 t}$$
3. Focus on the complex term: $$\frac{k}{k+j\omega_0} e^{j\omega_0 t}$$
4. Express the exponential using Euler's formula: $$e^{j\omega_0 t} = \cos(\omega_0 t) + j\sin(\omega_0 t)$$
5. Rationalize the complex coefficient $$\frac{k}{k+j\omega_0}$$ by multiplying by its conjugate: $$\frac{k}{k+j\omega_0} = \frac{k}{k+j\omega_0} \frac{k-j\omega_0}{k-j\omega_0} = \frac{k(k-j\omega_0)}{k^2+\omega_0^2}$$
6. Substitute the rationalized coefficient and Euler's formula into the complex term and expand the product: $$\frac{k}{k+j\omega_0} e^{j\omega_0 t} = \frac{k(k-j\omega_0)}{k^2+\omega_0^2} (\cos(\omega_0 t) + j\sin(\omega_0 t))$$
7. Expand the product to separate real and imaginary components: $$\frac{k}{k^2+\omega_0^2} [k\cos(\omega_0 t) + k j\sin(\omega_0 t) - j\omega_0\cos(\omega_0 t) - j^2\omega_0\sin(\omega_0 t)]$$
8. Simplify using $$j^2 = -1$$ and group terms: $$\frac{k}{k^2+\omega_0^2} [(k\cos(\omega_0 t) + \omega_0\sin(\omega_0 t)) + j(k\sin(\omega_0 t) - \omega_0\cos(\omega_0 t))]$$
9. Take the imaginary part of this expression, as indicated by the derivation's objective and the final form of T(t): $$Im\left(\frac{k}{k+j\omega_0} e^{j\omega_0 t}\right) = \frac{k}{k^2+\omega_0^2} (k\sin(\omega_0 t) - \omega_0\cos(\omega_0 t))$$
10. Substitute this imaginary part, scaled by $$T_a$$, back into the simplified T(t) expression to obtain the steady-state response: $$T(t) = \bar{T_0} + \frac{k T_a}{k^2+\omega_0^2} (k\sin(\omega_0 t) - \omega_0\cos(\omega_0 t))$$

**Reference:** start_page=2 end_page=2
### **General Complex Number Rationalization**
**Stub:** Derive the general formula for rationalizing a complex fraction: $$\frac{1}{x+jy} = \frac{x-jy}{x^2+y^2}$$

**Steps:**
1. Start with a complex number in the denominator: $$Z = x+jy$$
2. To rationalize, multiply the fraction by the complex conjugate of the denominator: $$\frac{1}{x+jy} = \frac{1}{x+jy} \frac{x-jy}{x-jy}$$
3. Perform the multiplication in the numerator and denominator: $$\frac{x-jy}{(x+jy)(x-jy)} = \frac{x-jy}{x^2 - (jy)^2} = \frac{x-jy}{x^2+y^2}$$
4. Separate into real and imaginary parts: $$\frac{x}{x^2+y^2} - j\frac{y}{x^2+y^2}$$

**Reference:** start_page=2 end_page=2
### **Conversion of a Linear Combination of Sine and Cosine into a Single Sine Wave**
**Stub:** Derive the expression for $k \sin(\omega_0 t) - \omega_0 \cos(\omega_0 t)$ in the form $C \sin(\omega_0 t - \phi)$, and determine $C$ and $\phi$.

**Steps:**
1. We begin with the expression to be transformed: $$k \sin(\omega_0 t) - \omega_0 \cos(\omega_0 t)$$
2. We want to express this in the phase-shifted sinusoidal form: $$C \sin(\omega_0 t - \phi)$$
3. Expand the target form using the sine angle subtraction identity: $$C \sin(\omega_0 t - \phi) = C (\sin(\omega_0 t) \cos(\phi) - \cos(\omega_0 t) \sin(\phi))$$
4. Equate the coefficients of $\sin(\omega_0 t)$ and $\cos(\omega_0 t)$ from both expressions: Let $k = C \cos(\phi)$ and $\omega_0 = C \sin(\phi)$.
5. To solve for $C$, square both equations and add them: $$(C \cos(\phi))^2 + (C \sin(\phi))^2 = k^2 + \omega_0^2$$ This simplifies to: $$C^2 (\cos^2(\phi) + \sin^2(\phi)) = k^2 + \omega_0^2$$
6. Using the trigonometric identity $\cos^2(\phi) + \sin^2(\phi) = 1$: $$C^2 = k^2 + \omega_0^2$$
7. Taking the square root, we find $C$: $$C = \sqrt{k^2 + \omega_0^2}$$(Note: The image implies a positive root for $C$)
8. To solve for $\phi$, divide the two coefficient equations: $$\frac{C \sin(\phi)}{C \cos(\phi)} = \frac{\omega_0}{k}$$
9. This simplifies to: $$\tan(\phi) = \frac{\omega_0}{k}$$
10. Taking the inverse tangent, we find $\phi$: $$\phi = \tan^{-1}\left(\frac{\omega_0}{k}\right)$$
11. Substituting the derived $C$ and $\phi$ back into the transformed expression, we get: $$k \sin(\omega_0 t) - \omega_0 \cos(\omega_0 t) = \sqrt{k^2 + \omega_0^2} \sin\left(\omega_0 t - \tan^{-1}\left(\frac{\omega_0}{k}\right)\right)$$

**Reference:** start_page=3 end_page=3
### **Solution of First-Order Linear ODE for Temperature**
**Stub:** Derive the general solution for $T(t)$ from the differential equation $\frac{dT}{dt} + kT = k\bar{T}_0 + k T_a e^{j\omega_0 t}$ with initial condition $T(0) = T_i$.

**Steps:**
1. Given the first-order linear ordinary differential equation: $$\frac{dT}{dt} + kT = k\bar{T}_0 + k T_a e^{j\omega_0 t}$$
2. Solve the homogeneous equation: $$\frac{dT}{dt} + kT = 0$$ which yields the homogeneous solution: $$T_h(t) = C e^{-kt}$$
3. Assume a particular solution of the form: $$T_p(t) = A + B e^{j\omega_0 t}$$
4. Calculate the derivative of the particular solution: $$\frac{dT_p}{dt} = B(j\omega_0) e^{j\omega_0 t}$$
5. Substitute $T_p(t)$ and $\frac{dT_p}{dt}$ into the original differential equation: $$B(j\omega_0) e^{j\omega_0 t} + k(A + B e^{j\omega_0 t}) = k\bar{T}_0 + k T_a e^{j\omega_0 t}$$
6. Equate the constant terms to find $A$: $$kA = k\bar{T}_0 \implies A = \bar{T}_0$$
7. Equate the coefficients of the exponential terms to find $B$: $$B j\omega_0 + k B = k T_a \implies B(k + j\omega_0) = k T_a \implies B = \frac{k T_a}{k + j\omega_0}$$
8. The particular solution is therefore: $$T_p(t) = \bar{T}_0 + \frac{k T_a}{k + j\omega_0} e^{j\omega_0 t}$$
9. The general solution is the sum of the homogeneous and particular solutions: $$T(t) = T_h(t) + T_p(t) = C e^{-kt} + \bar{T}_0 + \frac{k T_a}{k + j\omega_0} e^{j\omega_0 t}$$
10. Apply the initial condition $T(0) = T_i$: $$T_i = C e^{-k(0)} + \bar{T}_0 + \frac{k T_a}{k + j\omega_0} e^{j\omega_0 (0)}$$ which simplifies to: $$T_i = C + \bar{T}_0 + \frac{k T_a}{k + j\omega_0}$$
11. Solve for the constant $C$: $$C = T_i - \bar{T}_0 - \frac{k T_a}{k + j\omega_0}$$
12. Substitute $C$ back into the general solution to obtain the final solution: $$T(t) = \left(T_i - \bar{T}_0 - \frac{k T_a}{k + j\omega_0}\right) e^{-kt} + \bar{T}_0 + \frac{k T_a}{k + j\omega_0} e^{j\omega_0 t}$$
13. An alternative form of the final solution can be written as: $$T(t) = T_i e^{-kt} + \bar{T}_0 (1 - e^{-kt}) + \frac{k T_a}{k + j\omega_0} e^{j\omega_0 t} - \frac{k T_a}{k + j\omega_0} e^{-kt}$$

**Reference:** start_page=3 end_page=3
### **Imaginary Part of a Complex Exponential Expression**
**Stub:** Derive the imaginary part of the complex exponential expression: Im(k/(k+jω₀) * e^(jω₀t))

**Steps:**
1. Start with the complex expression: $$ \frac{k}{k+j\omega_0} e^{j\omega_0 t} $$
2. Convert the complex denominator $k+j\omega_0$ into its polar form. From the right-angled triangle, where $k$ is the adjacent side and $\omega_0$ is the opposite side to angle $\phi$, the hypotenuse is $\sqrt{k^2+\omega_0^2}$ and $\phi = \tan^{-1}(\omega_0/k)$. Thus, we have: $$ k+j\omega_0 = \sqrt{k^2+\omega_0^2} e^{j\phi} = \sqrt{k^2+\omega_0^2} e^{j \tan^{-1}\left(\frac{\omega_0}{k}\right)} $$
3. Substitute the polar form of the denominator back into the original expression: $$ \frac{k}{k+j\omega_0} e^{j\omega_0 t} = \frac{k}{\sqrt{k^2+\omega_0^2} e^{j\phi}} e^{j\omega_0 t} $$
4. Combine the exponential terms by subtracting the phase angle $\phi$ from the time-dependent phase $\omega_0 t$: $$ = \frac{k}{\sqrt{k^2+\omega_0^2}} e^{j(\omega_0 t - \phi)} $$
5. Apply Euler's formula, $e^{j\theta} = \cos(\theta) + j \sin(\theta)$, to expand the exponential term: $$ = \frac{k}{\sqrt{k^2+\omega_0^2}} \left( \cos(\omega_0 t - \phi) + j \sin(\omega_0 t - \phi) \right) $$
6. Take the imaginary part of the resulting complex number, which corresponds to the term multiplied by $j$: $$ \text{Im}\left( \frac{k}{k+j\omega_0} e^{j\omega_0 t} \right) = \frac{k}{\sqrt{k^2+\omega_0^2}} \sin(\omega_0 t - \phi) $$

**Reference:** start_page=4 end_page=4
### **Integral Property of Even Functions over Symmetric Intervals**
**Stub:** Derive the property that the integral of an even function f(t) over a symmetric interval [-T, T] is equal to twice the integral from 0 to T: $$\int_{-T}^{T} f(t) dt = 2 \int_{0}^{T} f(t) dt$$

**Steps:**
1. Begin by splitting the integral over the symmetric interval $$\int_{-T}^{T} f(t) dt$$ into two parts: $$\int_{-T}^{T} f(t) dt = \int_{-T}^{0} f(t) dt + \int_{0}^{T} f(t) dt$$
2. For the first integral, $$\int_{-T}^{0} f(t) dt$$ , perform a substitution. Let $$u = -t$$ , which implies $$du = -dt$$. The limits of integration change from $$t=-T$$ to $$u=T$$ and from $$t=0$$ to $$u=0$$. The integral becomes $$\int_{T}^{0} f(-u) (-du)$$
3. Reverse the limits of integration, which introduces a negative sign that cancels with the $$-du$$ term: $$\int_{T}^{0} f(-u) (-du) = \int_{0}^{T} f(-u) du$$
4. Since $$f(t)$$ is an even function, by definition $$f(t) = f(-t)$$. Therefore, $$f(-u) = f(u)$$. The first integral simplifies to $$\int_{0}^{T} f(u) du$$
5. Substitute this result back into the original split integral: $$\int_{-T}^{T} f(t) dt = \int_{0}^{T} f(u) du + \int_{0}^{T} f(t) dt$$
6. Since $$u$$ is a dummy variable of integration, it can be replaced by $$t$$. Combine the two identical integrals to obtain the final result: $$\int_{-T}^{T} f(t) dt = 2 \int_{0}^{T} f(t) dt$$

**Reference:** start_page=5 end_page=5
### **Integral Property of Odd Functions**
**Stub:** The integral of an odd function f(t) over a symmetric interval [-a, a] is zero: $$\int_{-a}^{a} f(t) dt = 0$$

**Steps:**
1. The property that the integral of an odd function over a symmetric interval is zero is stated: $$\int_{-a}^{a} f(t) dt = 0$$ . No explicit derivation steps are shown, but it is a direct consequence of the definition of an odd function ($$f(t) = -f(-t)$$) and the same substitution method used for even functions.

**Reference:** start_page=5 end_page=5
### **Fourier Series Coefficients for Even Functions**
**Stub:** Simplified Fourier series coefficients for an even function f(t).

**Steps:**
1. If f(t) is an even function:
2. The DC component a_0 is given by: $$a_0 = \frac{2}{T} \int_0^{T/2} f(t) dt$$
3. The cosine coefficients a_k are given by: $$a_k = \frac{4}{T} \int_0^{T/2} f(t) \cos\left(k \frac{2\pi t}{T}\right) dt$$
4. The sine coefficients b_k are zero: $$b_k = 0$$

**Reference:** start_page=6 end_page=6
### **Fourier Series Coefficients for Odd Functions**
**Stub:** Simplified Fourier series coefficients for an odd function f(t).

**Steps:**
1. If f(t) is an odd function:
2. The DC component a_0 is zero: $$a_0 = 0$$
3. The cosine coefficients a_k are zero: $$a_k = 0$$
4. The sine coefficients b_k are given by: $$b_k = \frac{4}{T} \int_0^{T/2} f(t) \sin\left(k \frac{2\pi t}{T}\right) dt$$

**Reference:** start_page=6 end_page=6
### **Frequency Response of a First-Order System**
**Stub:** Analysis of the steady-state amplitude and phase shift for a system subjected to a sinusoidal input.

**Steps:**
1. The input signal is given by: $$T_0(t) = \bar{T_0} + T_a \sin(\omega_0 t)$$
2. The corresponding output response is expressed as: $$T(t) = \bar{T_0} + \frac{T_a k}{\sqrt{k^2 + \omega_0^2}} \sin(\omega_0 t - \phi)$$
3. Considering the case where the DC offset is zero: $$\text{let } \bar{T_0} = 0 \implies T_0(t) = T_a \sin(\omega_0 t)$$
4. The simplified output signal becomes: $$T(t) = \frac{T_a k}{\sqrt{k^2 + \omega_0^2}} \sin(\omega_0 t - \phi)$$
5. The magnitude (amplitude) of the output response is identified as: $$|T| = \frac{T_a k}{\sqrt{k^2 + \omega_0^2}}$$ A plot illustrates this magnitude decreasing with increasing $$\omega_0$$, characteristic of a low-pass filter.
6. The phase shift of the output relative to the input is: $$\phi = \tan^{-1}\left(\frac{\omega_0}{k}\right)$$ A plot shows the phase shift increasing with $$\omega_0$$ from 0 to $$\pi/2$$.
7. Analyzing the magnitude $|T|$ in limiting cases:
8. As $$\omega_0 \to 0$$, the magnitude approaches: $$|T| \to T_a$$
9. As $$\omega_0 \to \infty$$, the magnitude approximates: $$|T| \approx \frac{T_a k}{\omega_0} \to 0$$
10. At $$\omega_0 = k$$, the magnitude is: $$|T| = \frac{T_a k}{\sqrt{k^2 + k^2}} = \frac{T_a k}{\sqrt{2k^2}} = \frac{T_a}{\sqrt{2}}$$ This point is often referred to as the cutoff frequency.
11. Analyzing the phase shift $$\phi$$ in limiting cases:
12. As $$\omega_0 \to 0$$, the phase shift approaches: $$\phi \to 0$$
13. As $$\omega_0 \to \infty$$, the phase shift approaches: $$\phi \to \frac{\pi}{2}$$
14. At $$\omega_0 = k$$, the phase shift is: $$\phi = \frac{\pi}{4}$$

**Reference:** start_page=1 end_page=1
### **Fourier Series Expansion and Coefficients**
**Stub:** Derive the Fourier series expansion for a periodic function f(t) and its coefficients.

**Steps:**
1. Let f(t) be a periodic function with period T.
2. The function f(t) can be expressed as a sum of sines and cosines:
3. $$f(t) = a_0 + a_1 \cos \frac{2\pi t}{T} + a_2 \cos \frac{2 \cdot 2\pi t}{T} + a_3 \cos \frac{3 \cdot 2\pi t}{T} + \dots + b_1 \sin \frac{2\pi t}{T} + b_2 \sin \frac{2 \cdot 2\pi t}{T} + b_3 \sin \frac{3 \cdot 2\pi t}{T} + \dots$$
4. This can be written in a compact summation form as:
5. $$f(t) = a_0 + \sum_{k=1}^{\infty} a_k \cos \left(k \frac{2\pi t}{T}\right) + \sum_{k=1}^{\infty} b_k \sin \left(k \frac{2\pi t}{T}\right)$$
6. The coefficient $a_0$ is given by:
7. $$a_0 = \frac{1}{T} \int_{-T/2}^{T/2} f(t) dt$$
8. The coefficient $a_k$ for $k \ge 1$ is given by:
9. $$a_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \cos \left(k \frac{2\pi t}{T}\right) dt$$
10. The coefficient $b_k$ for $k \ge 1$ is given by:
11. $$b_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \sin \left(k \frac{2\pi t}{T}\right) dt$$

**Reference:** start_page=8 end_page=8
### **Fourier Coefficient a0 for a Rectangular Pulse**
**Stub:** Derive the DC component a0 of the Fourier series for a periodic rectangular pulse.

**Steps:**
1. The function f(t) is defined as a periodic rectangular pulse with amplitude 1 for $0 < t < a$ and 0 otherwise within the period T. Specifically: $$f(t) = \begin{cases} 0 & -T/2 < t < 0 \\ 1 & 0 < t < a \\ 0 & a < t < T/2 \end{cases}$$
2. The formula for the Fourier coefficient a0 is: $$a_0 = \frac{1}{T} \int_{-T/2}^{T/2} f(t) dt$$
3. Split the integral over the defined intervals of f(t): $$a_0 = \frac{1}{T} \left[ \int_{-T/2}^{0} f(t) dt + \int_{0}^{a} f(t) dt + \int_{a}^{T/2} f(t) dt \right]$$
4. Substitute the values of f(t) into the integral: $$a_0 = \frac{1}{T} \left[ \int_{-T/2}^{0} 0 dt + \int_{0}^{a} 1 dt + \int_{a}^{T/2} 0 dt \right]$$
5. Simplify and evaluate the remaining integral: $$a_0 = \frac{1}{T} \left[ \int_{0}^{a} 1 dt \right] = \frac{1}{T} [t]_{0}^{a}$$
6. Apply the limits of integration to find the final expression for a0: $$a_0 = \frac{a}{T}$$

**Reference:** start_page=1 end_page=1
### **Fourier Cosine Coefficient ak for a Rectangular Pulse**
**Stub:** Derive the ak Fourier cosine coefficient for a periodic rectangular pulse.

**Steps:**
1. The function f(t) is defined as a periodic rectangular pulse with amplitude 1 for $0 < t < a$ and 0 otherwise within the period T.
2. The formula for the Fourier coefficient ak is: $$a_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \cos\left(\frac{2\pi k t}{T}\right) dt$$
3. Split the integral over the defined intervals of f(t) and substitute f(t) values: $$a_k = \frac{2}{T} \left[ \int_{-T/2}^{0} 0 \cdot \cos\left(\frac{2\pi k t}{T}\right) dt + \int_{0}^{a} 1 \cdot \cos\left(\frac{2\pi k t}{T}\right) dt + \int_{a}^{T/2} 0 \cdot \cos\left(\frac{2\pi k t}{T}\right) dt \right]$$
4. Simplify the integral as only the term from 0 to a is non-zero: $$a_k = \frac{2}{T} \int_{0}^{a} \cos\left(\frac{2\pi k t}{T}\right) dt$$
5. Evaluate the integral of the cosine function: $$a_k = \frac{2}{T} \left[ \frac{\sin\left(\frac{2\pi k t}{T}\right)}{\frac{2\pi k}{T}} \right]_{0}^{a}$$
6. Apply the limits of integration: $$a_k = \frac{2}{T} \frac{T}{2\pi k} \left[ \sin\left(\frac{2\pi k a}{T}\right) - \sin(0) \right]$$
7. Simplify to find the final expression for ak: $$a_k = \frac{1}{\pi k} \sin\left(\frac{2\pi k a}{T}\right)$$

**Reference:** start_page=1 end_page=1
### **Fourier Sine Coefficient bk for a Rectangular Pulse**
**Stub:** Derive the bk Fourier sine coefficient for a periodic rectangular pulse.

**Steps:**
1. The function f(t) is defined as a periodic rectangular pulse with amplitude 1 for $0 < t < a$ and 0 otherwise within the period T.
2. The formula for the Fourier coefficient bk is: $$b_k = \frac{2}{T} \int_{-T/2}^{T/2} f(t) \sin\left(\frac{2\pi k t}{T}\right) dt$$
3. Split the integral over the defined intervals of f(t) and substitute f(t) values: $$b_k = \frac{2}{T} \left[ \int_{-T/2}^{0} 0 \cdot \sin\left(\frac{2\pi k t}{T}\right) dt + \int_{0}^{a} 1 \cdot \sin\left(\frac{2\pi k t}{T}\right) dt + \int_{a}^{T/2} 0 \cdot \sin\left(\frac{2\pi k t}{T}\right) dt \right]$$
4. Simplify the integral as only the term from 0 to a is non-zero: $$b_k = \frac{2}{T} \int_{0}^{a} \sin\left(\frac{2\pi k t}{T}\right) dt$$
5. Evaluate the integral of the sine function: $$b_k = \frac{2}{T} \left[ -\frac{\cos\left(\frac{2\pi k t}{T}\right)}{\frac{2\pi k}{T}} \right]_{0}^{a}$$
6. Apply the limits of integration: $$b_k = \frac{2}{T} \left( -\frac{T}{2\pi k} \right) \left[ \cos\left(\frac{2\pi k a}{T}\right) - \cos(0) \right]$$
7. Simplify and rearrange to find the final expression for bk: $$b_k = -\frac{1}{\pi k} \left[ \cos\left(\frac{2\pi k a}{T}\right) - 1 \right] = \frac{1}{\pi k} \left( 1 - \cos\left(\frac{2\pi k a}{T}\right) \right)$$

**Reference:** start_page=1 end_page=1
### **Fourier Series Expansion**
**Stub:** Expression of a periodic function f(t) as a Fourier series, detailing its coefficients.

**Steps:**
1. The function $f(t)$ is expressed as a Fourier series, starting with a constant term and subsequent cosine terms, where specific terms are identified with labels $a_1, a_2, a_3, \dots$:$$f(t) = \frac{a}{T} + \underbrace{\frac{1}{\pi} \sin\left(\frac{2\pi a}{T}\right) \cos\left(\frac{2\pi t}{T}\right)}_{a_1} + \underbrace{\frac{1}{2\pi} \sin\left(\frac{2 \cdot 2\pi a}{T}\right) \cos\left(\frac{2 \cdot 2\pi t}{T}\right)}_{a_2} + \underbrace{\frac{1}{3\pi} \sin\left(\frac{3 \cdot 2\pi a}{T}\right) \cos\left(\frac{3 \cdot 2\pi t}{T}\right)}_{a_3} + \dots$$
2. The series continues with the sine terms, including their respective coefficients:$$+ \frac{1}{\pi} \left(1 - \cos\left(\frac{2\pi a}{T}\right)\right) \sin\left(\frac{2\pi t}{T}\right) + \frac{1}{2\pi} \left(1 - \cos\left(\frac{2 \cdot 2\pi a}{T}\right)\right) \sin\left(\frac{2 \cdot 2\pi t}{T}\right) + \frac{1}{3\pi} \left(1 - \cos\left(\frac{3 \cdot 2\pi a}{T}\right)\right) \sin\left(\frac{3 \cdot 2\pi t}{T}\right) + \dots$$

**Reference:** start_page=10 end_page=10


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** For a first-order thermal system subjected to a sinusoidal temperature input, how do the amplitude and phase of the steady-state temperature response change as the frequency of the input sinusoid (w_0) increases from a very low value to a very high value?

**Topics:** First-order system, Frequency response, Phase lag

**Options:**
- Amplitude increases and phase lag decreases.
- ✅ Amplitude decreases and phase lag increases.
- Amplitude remains constant and phase lag remains constant.
- Amplitude first increases then decreases, and phase lag first decreases then increases.

**Explanation:** From the graphs on page 7, as the input frequency (w_0) increases, the magnitude |T| of the response decreases, indicating that the system's ability to follow rapid temperature changes diminishes. Simultaneously, the phase lag phi increases from 0 to pi/2, meaning the system's response falls further behind the input signal as the frequency increases.

**Reference:** start_page=7 end_page=7
### **Conceptual Question**
**Question:** If a periodic function f(t) is known to be an odd function, which of the following statements about its Fourier series representation is true?

**Topics:** Odd functions, Fourier series, Fourier coefficients

**Options:**
- ✅ All cosine coefficients (a_k) are zero, and the constant term (a_0) is zero.
- All sine coefficients (b_k) are zero, and the constant term (a_0) is zero.
- Only the a_0 term is non-zero.
- All coefficients (a_k, b_k, a_0) are potentially non-zero.

**Explanation:** For an odd function f(t), f(-t) = -f(t). The a_k coefficients involve the integral of f(t)cos(...). Since cos(...) is an even function, f(t)cos(...) is an odd function (odd x even = odd). The integral of an odd function over a symmetric interval (-T/2 to T/2) is zero, thus all a_k (for k>=1) are zero. Similarly, a_0 (the average value) is also zero for an odd function integrated over a symmetric interval centered at zero. The b_k coefficients involve f(t)sin(...). Since sin(...) is an odd function, f(t)sin(...) is an even function (odd x odd = even), leading to non-zero b_k coefficients.

**Reference:** start_page=6 end_page=6
### **Conceptual Question**
**Question:** The general solution for a first-order linear ordinary differential equation with a sinusoidal forcing term consists of two main parts. What are these parts and what do they represent?

**Topics:** First-order ODE, Homogeneous solution, Particular solution, Transient response, Steady-state response

**Options:**
- A decaying exponential (transient response) and a constant term (DC offset).
- ✅ A decaying exponential (transient response) and a sinusoidal term (steady-state response).
- A constant term (DC offset) and a growing exponential (unstable response).
- Two sinusoidal terms with different frequencies.

**Explanation:** The general solution T(t) for a first-order linear ODE is the sum of the homogeneous solution T_h(t) and the particular solution T_p(t). The homogeneous solution, T_h(t) = C e^(-kt), represents the transient response that decays over time. The particular solution, T_p(t), represents the steady-state response, which for a sinusoidal forcing term will be a sinusoidal oscillation at the same frequency as the input, potentially with a phase shift and a DC offset.

**Reference:** start_page=4 end_page=4
