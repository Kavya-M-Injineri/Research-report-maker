import uuid

class Gateway:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id, task_description):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "task": task_description,
            "history": [],
            "status": "initialized"
        }
        return session_id

    def update_session(self, session_id, message, role="user"):
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "role": role,
                "content": message
            })
            return True
        return False

    def get_session_context(self, session_id):
        return self.sessions.get(session_id, {})
