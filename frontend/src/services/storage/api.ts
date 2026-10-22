import api from "../../config/api";

export class StorageAPI {
  static async getFileById(
    token: string,
    fileId: string,
    signal?: AbortSignal,
  ): Promise<Blob> {
    const res = await api.get<Blob>(
      `/files/${encodeURIComponent(fileId)}`,
      {
        responseType: "blob",
        signal,
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    return res.data;
  }

  static async getFileByStorageKey(
    token: string,
    storageKey: string,
    signal?: AbortSignal,
  ): Promise<Blob> {
    const res = await api.get<Blob>("/files", {
      params: { storage_key: storageKey },
      responseType: "blob",
      signal,
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.data;
  }
}
