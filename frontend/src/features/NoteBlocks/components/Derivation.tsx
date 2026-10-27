import Markdown from "../../../components/Markdown/MarkdownRenderer";
import type { DerivationContent } from "../schemas";
import { Equation, ListSection, Section, SourcePages } from "./shared";

export default function Derivation({ content }: { content: DerivationContent }) {
  return (
    <div className="space-y-4">
      <div className="text-base font-semibold"><Markdown>{content.title}</Markdown></div>
      <p className="text-xs text-text-muted">Completeness: {content.completeness}</p>
      <Markdown>{content.description}</Markdown>
      <ListSection title="Assumptions" items={content.assumptions} />
      {content.symbols.length > 0 && (
        <Section title="Symbols">
          <ul className="space-y-2">
            {content.symbols.map((symbol, index) => (
              <li key={index}>
                <Markdown>{`$${symbol.symbol}$: ${symbol.meaning}`}</Markdown>
              </li>
            ))}
          </ul>
        </Section>
      )}
      {content.steps.length > 0 ? (
        <Section title="Derivation steps">
          <ol className="list-decimal space-y-4 pl-5">
            {content.steps.map((step, index) => (
              <li key={index} className="min-w-0 space-y-2">
                <Markdown>{step.explanation}</Markdown>
                <Equation latex={step.equation_latex} />
                {step.rule_used !== null && (
                  <Section title="Rule"><Markdown>{step.rule_used}</Markdown></Section>
                )}
                <SourcePages reference={step.reference} />
              </li>
            ))}
          </ol>
        </Section>
      ) : <p className="text-sm text-text-muted">No source-supported steps were extracted.</p>}
      {content.result_latex !== null && (
        <Section title="Result"><Equation latex={content.result_latex} /></Section>
      )}
      <ListSection title="Missing or unclear information" items={content.gaps} />
      <SourcePages reference={content.reference} />
    </div>
  );
}
