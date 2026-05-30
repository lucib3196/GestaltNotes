export interface ThreadCreate {
  thread_id?: string | null;
  user_id?: string | null;
  course_id?: string | null;
  title?: string | null;
  agent?: string | null;
}

export interface Thread {
  id: string;
  user_id: string;
  course_id: string | null;
  title: string | null;
  agent: string | null;
  created_at: string;
  updated_at: string;
}

export interface MessageCreate {
  role: string;
  content: string;
}

export interface Message {
  id: string;
  thread_id: string;
  role: string;
  content: string;
  created_at: string;
}


export interface ThreadUpdate{
  title: string
}