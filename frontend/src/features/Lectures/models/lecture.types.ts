export type FileEntry = { path: string; url: string; parent?: string | null };
export type GroupedFiles = Record<string, FileEntry[]>;
