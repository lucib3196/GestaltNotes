# Lecture Source: me118_Lecture_01_06.pdf

## Introduction to Difference Equations and Applications

**Lecture Type:** mixed

### Summary
This lecture introduces difference equations, contrasting them with ordinary differential equations and their classifications. It demonstrates how to formulate and solve first-order difference equations to model real-world scenarios such as bank account balances and population dynamics. The lecture also explores the qualitative behavior of these equations, including monotonic and oscillatory solutions, and introduces a graphical method for analyzing their dynamics.

### Core Topics
- Difference equations
- Ordinary differential equations classification
- First-order difference equations
- Bank account model
- Population model
- Behavior of linear difference equations
- Monotonic growth and decay
- Oscillatory solutions
- Cobweb method

### Learning Objectives
1. Distinguish between difference equations and ordinary differential equations.
2. Classify ordinary differential equations based on order, linearity, and initial/boundary conditions.
3. Formulate a first-order difference equation to model financial and biological phenomena.
4. Derive the general solution for a first-order linear difference equation.
5. Apply difference equations to solve practical problems, such as calculating required deposits.
6. Analyze the qualitative behavior of first-order linear difference equations based on their parameters.
7. Utilize the cobweb method to graphically visualize the dynamics of a first-order difference equation.

### Assumed Prerequisites
- Basic algebra
- Understanding of series, particularly geometric series
- Basic graphing concepts


## Derivations

### **General Formula for Bank Account Balance with Equal Deposits and Withdrawals**
**Stub:** Derive $B(n) = B_0(1+i)^n$ for a bank account where deposits equal withdrawals.

**Steps:**
1. Let $B(n)$ be the balance in a bank account at time period $n$. The initial difference equation for the balance at time $n+1$ is $B(n+1) = B(n) + iB(n) + d - w$, where $iB(n)$ is interest, $d$ is deposits, and $w$ is withdrawals.
2. This equation can be rearranged into a first-order difference equation: $B(n+1) = B(n)(1+i) + (d-w)$.
3. Consider the specific case where deposits equal withdrawals, i.e., $d=w$. The difference equation simplifies to $B(n+1) = B(n)(1+i)$.
4. Let the initial balance at time $n=0$ be $B(0) = B_0$.
5. For $n=0$: $B(0+1) = B(0)(1+i) \Rightarrow B(1) = B_0(1+i)$.
6. For $n=1$: $B(1+1) = B(1)(1+i) \Rightarrow B(2) = B_0(1+i)(1+i) = B_0(1+i)^2$.
7. For $n=2$: $B(2+1) = B(2)(1+i) \Rightarrow B(3) = B_0(1+i)^2(1+i) = B_0(1+i)^3$.
8. Observing the pattern, the general formula for the balance at any time $n$ is $B(n) = B_0(1+i)^n$.

**Reference:** start_page=2 end_page=2
### **Equilibrium Balance for a Bank Account**
**Stub:** Derive the equilibrium balance $B(n) = -\frac{(d-w)}{i}$ for a bank account.

**Steps:**
1. The first-order difference equation for the bank account balance is given as $B(n+1) = B(n)(1+i) + (d-w)$.
2. For a system to be in equilibrium, the balance must remain constant over time, meaning $B(n+1) = B(n)$.
3. Substituting the equilibrium condition into the difference equation: $B(n) = B(n)(1+i) + (d-w)$.
4. Expand the right side: $B(n) = B(n) + iB(n) + (d-w)$.
5. Subtract $B(n)$ from both sides: $0 = iB(n) + (d-w)$.
6. Rearranging to solve for $B(n)$: $iB(n) = -(d-w)$.
7. Thus, the equilibrium balance is $B(n) = -\frac{(d-w)}{i}$.

**Reference:** start_page=2 end_page=2
### **General Solution for a Linear First-Order Recurrence Relation**
**Stub:** Derive the explicit formula for B(n) given the recurrence relation B(n+1) = B(n)(1+i) + d and initial condition B(0) = B_0.

**Steps:**
1. Given the recurrence relation: $$B(n+1) = B(n)(1+i) + d$$ with initial condition $$B(0) = B_0$$ and parameters $$w=0, d = constant$$.
2. For n=0: $$B(1) = B(0)(1+i) + d = B_0(1+i) + d$$
3. For n=1: $$B(2) = B(1)(1+i) + d = (B_0(1+i) + d)(1+i) + d = B_0(1+i)^2 + d(1+i) + d$$
4. For n=2: $$B(3) = B(2)(1+i) + d = (B_0(1+i)^2 + d(1+i) + d)(1+i) + d = B_0(1+i)^3 + d(1+i)^2 + d(1+i) + d$$
5. Observing the pattern, for n=4: $$B(4) = B_0(1+i)^4 + d(1+i)^3 + d(1+i)^2 + d(1+i) + d$$
6. Generalizing the pattern for B(n): $$B(n) = B_0(1+i)^n + d \sum_{j=0}^{n-1} (1+i)^j$$
7. Let's define the sum as S: $$S = \sum_{j=0}^{n-1} (1+i)^j$$
8. Let \alpha = (1+i). Then $$S = \sum_{j=0}^{n-1} \alpha^j$$
9. Write out the series for S: $$S = 1 + \alpha + \alpha^2 + ... + \alpha^{n-1} \quad (1)$$
10. Multiply S by \alpha: $$\alpha S = \alpha + \alpha^2 + \alpha^3 + ... + \alpha^n \quad (2)$$
11. Subtract equation (1) from equation (2): $$\alpha S - S = (\alpha + \alpha^2 + ... + \alpha^n) - (1 + \alpha + ... + \alpha^{n-1})$$
12. This simplifies to: $$S(\alpha - 1) = \alpha^n - 1$$
13. Solve for S: $$S = \frac{\alpha^n - 1}{\alpha - 1}$$
14. Substitute back \alpha = (1+i): $$S = \frac{(1+i)^n - 1}{(1+i) - 1} = \frac{(1+i)^n - 1}{i}$$
15. Substitute the expression for S back into the general formula for B(n): $$B(n) = B_0(1+i)^n + d \frac{(1+i)^n - 1}{i}$$

**Reference:** start_page=1 end_page=1
### **Derivation of Future Value with Regular Deposits (Annuity Formula)**
**Stub:** Derive the formula for B(n), the balance at time n, given an initial balance B(0), a constant interest rate i, and regular deposits d.

**Steps:**
1. Given the initial conditions: w = 0 (likely representing withdrawals), d = constant (representing regular deposits), and B(0) = B_0 (initial balance).
2. The recursive relation for the balance B(n+1) at time n+1, based on the balance B(n) at time n, is given by: $$B(n+1) = B(n)(1+i) + d$$
3. Expand the relation for n=0: $$B(1) = B(0)(1+i) + d = B_0(1+i) + d$$
4. Expand the relation for n=1: $$B(2) = B(1)(1+i) + d = (B_0(1+i) + d)(1+i) + d = B_0(1+i)^2 + d(1+i) + d$$
5. Expand the relation for n=2: $$B(3) = B(2)(1+i) + d = (B_0(1+i)^2 + d(1+i) + d)(1+i) + d = B_0(1+i)^3 + d(1+i)^2 + d(1+i) + d$$
6. From the pattern, the balance at time n can be expressed as: $$B(n) = B_0(1+i)^n + d ig( (1+i)^{n-1} + (1+i)^{n-2} + \dots + (1+i)^1 + (1+i)^0 ig)$$ This can be written using summation notation: $$B(n) = B_0(1+i)^n + d \sum_{j=0}^{n-1} (1+i)^j$$
7. Let S represent the geometric series: $$S = \sum_{j=0}^{n-1} (1+i)^j$$
8. Define \alpha = (1+i). Then the sum S becomes: $$S = \sum_{j=0}^{n-1} \alpha^j = 1 + \alpha + \alpha^2 + \dots + \alpha^{n-1}$$ (Equation 1)
9. Multiply Equation 1 by \alpha: $$\alpha S = \alpha + \alpha^2 + \alpha^3 + \dots + \alpha^n$$ (Equation 2)
10. Subtract Equation 1 from Equation 2: $$\alpha S - S = (\alpha + \alpha^2 + \dots + \alpha^n) - (1 + \alpha + \dots + \alpha^{n-1})$$ This simplifies to: $$S(\alpha - 1) = \alpha^n - 1$$
11. Solve for S: $$S = \frac{\alpha^n - 1}{\alpha - 1}$$
12. Substitute back \alpha = (1+i): $$S = \frac{(1+i)^n - 1}{(1+i) - 1} = \frac{(1+i)^n - 1}{i}$$
13. Substitute the derived sum S back into the expression for B(n): $$B(n) = B_0(1+i)^n + d \frac{(1+i)^n - 1}{i}$$

**Reference:** start_page=5 end_page=5
### **Calculation of Annual Deposit for Future College Cost**
**Stub:** Derive the required annual deposit 'd' to accumulate a specific future value 'B(n)' in an account with zero initial balance and a given interest rate.

**Steps:**
1. State the future value of an annuity formula, which includes an initial lump sum and periodic deposits: $$B(n) = B_0 (1+i)^n + d \frac{(1+i)^n - 1}{i}$$
2. Identify the given parameters from the problem statement: College cost is $100K (so $B(18) = 100$ in thousands), the interest rate is $i = 5\% = 0.05$ per year, the number of years is $n = 18$, and the starting balance is $B_0 = 0$.
3. Substitute the known values into the formula: $$100 = 0 + d \frac{(1+0.05)^{18} - 1}{0.05}$$
4. Simplify the expression: $$100 = d \frac{(1.05)^{18} - 1}{0.05}$$
5. Solve for $d$: $$d = 3554/year$$

**Reference:** start_page=4 end_page=4
### **Discrete Population Growth Model (Exponential)**
**Stub:** Derive the discrete exponential growth formula P(n) = P_0(1+r)^n.

**Steps:**
1. Define P(n) as the population at time n. The population at time n+1 is given by the initial population plus births, minus deaths, plus immigration, minus emigration: $$P(n+1) = P(n) + (b-d)P(n) + I - E$$ where b is birth rate, d is death rate, I is immigration, and E is emigration.
2. Define the net growth rate r as the difference between birth and death rates: $$r \triangleq b-d$$
3. Define net migration M as the difference between immigration and emigration: $$M \triangleq I - E$$
4. Substitute r and M into the population model equation: $$P(n+1) = P(n) + rP(n) + M$$
5. Factor out P(n): $$P(n+1) = P(n)(1+r) + M$$
6. Consider the special case where net migration is zero (M=0) and the initial population at time n=0 is P_0: $$M=0, P(0)=P_0$$
7. Under this condition, the recurrence relation becomes: $$P(n+1) = P(n)(1+r)$$ This is the core recurrence for exponential growth.
8. Applying the recurrence relation for n=0: $$P(1) = P(0)(1+r) = P_0(1+r)$$
9. Applying for n=1: $$P(2) = P(1)(1+r)$$
10. Substitute P(1): $$P(2) = P_0(1+r)(1+r) = P_0(1+r)^2$$
11. By induction, the population at any time n can be expressed as: $$P(n) = P_0(1+r)^n$$ This is the discrete exponential growth formula.

**Reference:** start_page=5 end_page=5


## Questions



## Conceptual Questions

### **Conceptual Question**
**Question:** Based on the provided lecture material, which of the following is NOT a primary classification category for Ordinary Differential Equations (ODEs)?

**Topics:** Differential Equations, Classification, Ordinary Differential Equations

**Options:**
- Initial Value Problems
- Boundary Value Problems
- ✅ Partial Differential Equations
- Systems of ODEs

**Explanation:** Page 1 classifies Ordinary Differential Equations (ODEs) into Initial Value and Boundary Value problems, and further by order (1st, 2nd, etc.), linearity (linear, non-linear), and as systems of ODEs. Partial Differential Equations (PDEs) are a different type of differential equation, distinct from ODEs, and not a sub-classification of ODEs.

**Reference:** start_page=1 end_page=1
### **Conceptual Question**
**Question:** In the derived solution for the bank account balance with an initial deposit B_0, constant interest rate 'i', and constant deposits 'd' (B(n) = B_0 (1+i)^n + d * ((1+i)^n - 1) / i), what does the term 'B_0 (1+i)^n' represent?

**Topics:** Difference Equations, Financial Models, Compound Interest

**Options:**
- The total amount from all future deposits.
- ✅ The accumulated value of the initial deposit B_0 after 'n' periods, without any further deposits.
- The total interest earned over 'n' periods.
- The equilibrium balance of the account.

**Explanation:** The term B_0 (1+i)^n represents the accumulated value of the initial deposit B_0 compounded over 'n' periods at an interest rate 'i', assuming no further deposits or withdrawals are made. The second term, d * ((1+i)^n - 1) / i, accounts for the accumulated value of the constant deposits 'd'.

**Reference:** start_page=3 end_page=4
### **Conceptual Question**
**Question:** Consider the simplified population model P(n) = P_0 * alpha^n. If the parameter 'alpha' is between -1 and 0 (i.e., -1 < alpha < 0), what behavior does the population exhibit over time?

**Topics:** Population Dynamics, Stability Analysis, Discrete Dynamical Systems

**Options:**
- Monotonically increasing.
- Monotonically decreasing.
- ✅ Convergent oscillation.
- Divergent oscillation.

**Explanation:** As shown on page 6 of the lecture material (point 5), when -1 < alpha < 0, the term alpha^n will alternate in sign for consecutive 'n' and its magnitude will decrease towards zero as 'n' increases. This results in a convergent oscillation, where the population values alternate and approach zero.

**Reference:** start_page=6 end_page=6
