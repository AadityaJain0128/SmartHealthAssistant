<template>
  <div class="chat-wrapper">
    <div class="chat-container" ref="chatContainer">
      <div class="empty-chat" v-if="!chats.length">
        <p>Start a conversation !</p>
      </div>
      <div v-for="(chat, index) in chats" :key="index" :class="['chat-message', chat.username === 'You' ? 'user' : 'bot']">
        <strong>{{ chat.username }}:</strong> {{ chat.message }}
      </div>
    </div>

    <div class="chat-input">
      <textarea
        v-model="message"
        placeholder="Type a message..."
        @keyup.enter="sendMessage"
      ></textarea>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chats: [],
      message: "",
      token: localStorage.getItem("token"),
    };
  },
  async mounted() {
    await this.fetchChats();
    this.scrollToBottom();
  },
  methods: {
    async fetchChats() {
      try {
        const response = await this.$http.get("/chats",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
              "ngrok-skip-browser-warning": "69420"
            }
          });

        this.chats = response.data.chats.map(chat => [
          { username: "You", message: chat.message },
          { username: "MediBuddy", message: chat.response },
        ]).flat();

        this.$nextTick(() => this.scrollToBottom());
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    },
    async sendMessage() {
      if (!this.message.trim()) return;

      try {
        const response = await this.$http.post("/chat",
          { message: this.message },
          { headers: { Authorization: `Bearer ${this.token}` } }
        );

        this.chats.push({ username: "You", message: this.message });
        this.chats.push({ username: "MediBuddy", message: response.data.response });

        this.message = "";
        this.$nextTick(() => this.scrollToBottom());
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContainer = this.$refs.chatContainer;
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      });
    }
  }
};
</script>

<style>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 90vh;
  /* max-width: 500px; */
  margin: auto;
  border: 1px solid #ddd;
  background: #f9f9f9;
  border-radius: 10px;
  overflow: hidden;
  width: 120vh;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #fff;
  height: 400px;
}

.chat-message {
  padding: 8px 12px;
  margin: 5px 0;
  border-radius: 15px;
  max-width: 100%;
  word-wrap: break-word;
  white-space: pre-wrap; /* Preserve new lines in the message text */
}

.user {
  background: #007bff;
  color: white;
  align-self: flex-end;
  text-align: right;
}

.bot {
  background: #e5e5ea;
  color: black;
  align-self: flex-start;
  text-align: left;
}

.chat-input {
  display: flex;
  padding: 10px;
  background: #fff;
  border-top: 1px solid #ddd;
  align-items: center; /* Ensure items are centered vertically */
  height: 50px; /* Set a fixed height for the input container */
}

.chat-input textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
  margin-right: 10px; /* Add margin to the right of the input */
  height: 100%; /* Ensure the input field takes the full height of the container */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
  width: 85%;
}

.chat-input button {
  padding: 10px 15px;
  border: none;
  background: #007bff;
  color: white;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: 0.3s;
  height: 100%; /* Ensure the button takes the full height of the container */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
  width: 15%;
}

.chat-input button:hover {
  background: #0056b3;
}

.empty-chat {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #aaa; /* Muted text color */
  font-style: italic;
}
</style>