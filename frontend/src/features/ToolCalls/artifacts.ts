export function isArtifact(art: unknown) {
  return typeof art === "object" && art !== null;
}

export function getArtifactData(art: unknown) {
  return isArtifact(art) && "data" in art ? art.data : undefined;
}
export function getArtifactKind(art: unknown): string | undefined {
  if (isArtifact(art) && "kind" in art && typeof art.kind === "string") {
    return art.kind;
  }

  return undefined;
}
