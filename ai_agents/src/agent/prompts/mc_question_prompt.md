Package exactly the requested number of multiple-choice questions.

Prepare all questions before calling this tool.

## Structure and quality

- Generate exactly num_questions questions about the requested topic.
- Give each question exactly four distinct options and one correct answer.
- Set correct_answer_index to the correct option's zero-based index, 0–3.
- State the necessary givens, units, and assumptions.
- Use plausible distractors based on common conceptual or calculation errors.
- Keep the correct answer and explanation consistent with the givens.
- Do not disclose which option is correct in the question or option wording.

## Markdown formatting

- Use readable Markdown in questions, options, and explanations.
- Separate context, givens, and the actual question with real line breaks.
- Use short paragraphs or bullet lists when they improve readability.
- Do not add question numbers or A/B/C/D prefixes; the UI supplies them.
- Keep options concise and consistent in wording, units, and precision.
- Do not wrap content in code fences or pre-encode it as HTML entities.
- Keep Markdown formatting outside math delimiters.

## LaTeX styling guide

### Inline math

Use one pair of dollar signs for short expressions embedded in prose:

The temperature is $T = 300\,\mathrm{K}$.

Keep short mathematical answer options inline:

$\dot{E}_{\mathrm{in}} - \dot{E}_{\mathrm{out}} + \dot{E}_{\mathrm{gen}} = 0$

- Open and close every expression with exactly one dollar sign.
- Do not put line breaks inside inline math.
- Put sentence punctuation outside the closing delimiter.
- Never leave a formula outside math delimiters.

### Block math

Use two dollar signs for standalone equations. Place each delimiter on its
own line and leave blank lines before and after the block:

The general energy rate balance is

$$
\dot{E}_{\mathrm{in}} - \dot{E}_{\mathrm{out}} + \dot{E}_{\mathrm{gen}}
= \frac{dE_{\mathrm{st}}}{dt}
$$

At steady state, the storage term is zero.

- Keep short answer options inline rather than using blocks.
- Do not mix single-dollar and double-dollar closing delimiters.
- Do not use \( ... \), \[ ... \], or equation environments as outer
  delimiters; use the dollar delimiters consistently.

### Ordinary text and labels

Keep ordinary prose outside math whenever possible.

Inside math, use \text{...} for words or phrases:

$Q = 0 \quad \text{for an adiabatic boundary}$

Use \mathrm{...} for upright units and short descriptive labels:

$T_{\mathrm{initial}} = 300\,\mathrm{K}$

- Do not use \{text} to format words.
- Braces {...} group LaTeX arguments; they are not printed.
- Use \{ and \} only when literal visible braces are intended:
  $S = \{1, 2, 3\}$.
- Use \text{...}, not Markdown bold or italics, inside equations.

### Subscripts, superscripts, and accents

- Use _{...} for subscripts: $E_{\mathrm{st}}$.
- Use ^{...} for superscripts: $v^{2}$.
- Group multi-character indices: $T_{i+1}$.
- Use \dot{...} for rates: $\dot{Q}$.
- Use \bar{...} or \hat{...} for the intended accent: $\bar{T}$, $\hat{n}$.
- Never substitute an asterisk for a subscript:
  write $\dot{E}_{\mathrm{in}}$, not $\dot{E}*{in}$.
- Do not escape a subscript underscore:
  E_{st} means a subscript; E\_{st} contains a literal underscore.
- An asterisk is not a formatting repair for an underscore.

### Fractions, roots, and grouping

- Use \frac{numerator}{denominator}: $\frac{dE_{\mathrm{st}}}{dt}$.
- Use \sqrt{...} or \sqrt[n]{...}: $\sqrt{x^{2} + y^{2}}$.
- Balance every opening brace, parenthesis, and bracket.
- Use \left and \right together when scalable delimiters are needed:
  $\left(\frac{a}{b}\right)^{2}$.
- Do not append unrelated formulas without a relation, operator, or prose.

### Operators and symbols

- Use \cdot or \times for explicit multiplication: $F = m \cdot a$.
- Use standard commands: \sin, \cos, \tan, \ln, \log, and \exp.
- Use \leq, \geq, \neq, and \approx for comparisons.
- Use \Delta T, \alpha, and \rho for Greek symbols.
- Use \sum_{i=1}^{n} and \int_{a}^{b} for sums and integrals.
- Use \mathbf{v} for vectors when needed.
- Prefer standard commands supported by both KaTeX and MathJax.
- Do not depend on custom macros, additional packages, or HTML commands.

### Units and spacing

- Separate numbers and units with \,: $25\,\mathrm{W}$.
- Render units upright: $\mathrm{kg}$, $\mathrm{m}$, $\mathrm{s}$.
- Write compound units clearly:
  $k = 15\,\mathrm{W}/(\mathrm{m}\cdot\mathrm{K})$.
- Use $25\,^{\circ}\mathrm{C}$ for Celsius and $300\,\mathrm{K}$ for kelvin.
- Use $50\%$ for percentages.
- Keep unit conventions and numerical precision consistent across options.

### Multiline equations

For a calculation that needs multiple lines, put aligned inside a dollar
block:

$$
\begin{aligned}
Q &= mc\Delta T \\
  &= (2\,\mathrm{kg})(500\,\mathrm{J}/(\mathrm{kg}\cdot\mathrm{K}))(10\,\mathrm{K}) \\
  &= 10{,}000\,\mathrm{J}
\end{aligned}
$$

- Use & to align at the relation.
- Use \\ between equation rows.
- Close every environment with its matching \end{...}.
- Prefer separate simple equations when alignment adds no clarity.

### JSON escaping

The examples above show the intended parsed strings, not JSON source.

When producing JSON:
- Encode each literal LaTeX backslash as \\.
- Encode real line breaks as \n.
- An aligned row separator needs two parsed backslashes, encoded as \\\\.
- Do not double-escape the content after parsing.
- Do not escape dollar signs or subscript underscores inside math.

Example JSON source:

{"question": "Find $\\dot{Q}$ when $Q = 100\\,\\mathrm{J}$ over $t = 2\\,\\mathrm{s}$."}

Example JSON source containing block math:

{"explanation": "Use the rate relation:\n\n$$\n\\dot{Q} = \\frac{Q}{t} = 50\\,\\mathrm{W}\n$$\n\nThe rate is constant."}

## Explanations

- Explain the governing concept and why the correct option follows.
- For calculations, show the formula, substitution, and result with units.
- Briefly address the main misconception represented by the distractors.
- Keep explanations focused; avoid repeating the question verbatim.
- State assumptions explicitly rather than silently changing the problem.
- Preserve complete formulas; never replace missing math with empty parentheses.

## Final validation

Before calling the tool:
- Verify the question count, option counts, and correct-answer indices.
- Check the calculation and confirm exactly one option is correct.
- Check all math delimiters, braces, and environments are balanced.
- Check subscripts use _ rather than * or \_.
- Check text inside equations uses \text{...} where appropriate.
- Check that JSON decoding preserves the intended LaTeX and line breaks.
