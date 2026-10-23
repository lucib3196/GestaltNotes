export function setItemsById<T extends { id: string }>(
  items: T[],
): Record<string, T> {
  const byId: Record<string, T> = {};
  for (const item of items) {
    if (!item.id) continue;
    byId[item.id] = item;
  }
  return byId;
}
