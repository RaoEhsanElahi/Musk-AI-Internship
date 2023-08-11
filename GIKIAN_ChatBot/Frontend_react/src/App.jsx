import { useState } from 'react'
import './App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
const API_KEY = "Your Key";


function App() {
  const [messages, setMessages] = useState([
    {
      message: "Hello I am GIKIAN your personal assistant.",
      sender: "GIKIAN"
    }
  ])

  const handleSend = async (message) => {
    const newMessage = {
      message: message,
      sender: "user",
      direction: "outgoing",
    };
  
    setMessages([...messages, newMessage]);
    setTyping(true);
  
    try {
      const response = await processMessageToFastApi(newMessage);
  
      const chatbotResponse = {
        message: response.response,
        sender: "Chatbot",
        direction: "incoming",
      };
  
      setMessages((prevMessages) => [...prevMessages, chatbotResponse]);
  
      setTyping(false);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  async function processMessageToFastApi(message) {
    const apiMessage = {
      role: "user",
      content: message.message,
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(apiMessage),
      });
  
      // Parse the JSON response body
      const responseData = await response.json();
      console.log("Response Data:", responseData);
  
      return responseData;
    } catch (error) {
      console.error("Error:", error);
      throw error;
    }
  }

  return (
    <div className='App'>
      <div style = {{position: "relative", height: "800px", width: "700px"}}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator = {typing ? <TypingIndicator content="GIKIAN is Typing..." /> : null}>
              {messages.map((message, i) => {
                return <Message key={i} model = {message} />
              })}
            </MessageList>
            <MessageInput placeholder='Ask your questions here.' onSend={handleSend}/>
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
)
}

export default App