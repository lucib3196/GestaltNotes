import api from "../config/api";

export default class NotesAPI {
  private static readonly base = "/notes";

  static async getNotes() {
    const response = await api.get(this.base);
    return response.data;
  }
}
