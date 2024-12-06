const baseUrl = 'http://127.0.0.1:8000/chat/'
const chatIntro = document.getElementById('chat-intro')
const chatBox = document.getElementById('chat-view')
const chatName = document.getElementById('chat-name')
const chatInput = document.querySelector(".chat-input-section input");
const chatSendButton = document.querySelector(".chat-input-section .chat-send")
const chatContainer = document.querySelector(".chat-conversation")
const chatView = document.getElementById("chat-messages");
const requestUser =  JSON.parse(document.getElementById('user').textContent)

// chatIntro.classList.add('d-none')
// chatBox.classList.remove('d-none')

class ChatSocket {
  constructor(id) {
    this.roomId = id 
    this.url = 'ws://' + window.location.host + '/ws/chat/' + this.roomId + '/';
    this.chatSocket = new WebSocket(this.url);
    this.chatSocket.onopen = this.handleOpen;
    this.chatSocket.onmessage = this.handleMessage;
    this.chatSocket.onclose = this.handleClose;
    this.chatSocket.onerror = this.handleError;
  }

  handleOpen = () => {
    console.log('Connected to chat room:', this.roomId);
    // currentId = this.roomId
  };

  handleMessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Message received:', data);

    switch (data.type) {
      case 'online_count':
        document.getElementById('count').textContent = `Online: ${data.count}`
        break;

      case 'chat_message':
        formatMessage(data.time, data.user, data.message)
        break;
      
      case 'add_user':
          addUser(data.message)
      default:
        break;
    }

    
  }

  sendMessage(message){
    this.chatSocket.send(JSON.stringify({ message }))
    // console.log('Message sent:', message);
  }

  handleClose = () => {
    console.error('ChatSocket closed unexpectedly');
  };

  handleError = (error) => {
    console.error('WebSocket error:', error);
  };
}

const addUser = (message)=>{
  const newMessage = document.createElement("li");
  const content = `
    <div class="chat-day-title">
        <span class="title">${message}</span>
    </div>
  `;
  newMessage.innerHTML = content;
  chatView.appendChild(newMessage);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}


const formatMessage = (time, user, message)=>{
    const date = new Date(time);
    const formattedTime = date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      });
    const newMessage = document.createElement('li');
    const chatSender = user    
    chatSender === requestUser ? newMessage.classList.add('right'): newMessage
    newMessageContent = `
    <div class="conversation-list">
        <div class="chat-avatar">
            <div class="bg-dark">AD</div>
        </div>

        <div class="user-chat-content">
            <div class="ctext-wrap">
                    <div class="ctext-wrap-content">
                        <p class="mb-0">
                            ${message}
                        </p>
                        <p class="chat-time mb-0">
                            <i class="ri-time-line align-middle"></i>
                                <span class="align-middle">${formattedTime}</span>
                        </p>                            
                    </div>

                    <div class="dropdown align-self-start">
                        <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true"
                            aria-expanded="false">
                                <i class="ri-more-2-fill"></i>
                        </a>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="#">                                       
                                Copy
                                <i class="ri-file-copy-line float-end text-muted"></i></a>
                            <a class="dropdown-item" href="#"> 
                                Save
                                <i class="ri-save-line float-end text-muted"></i>
                            </a>
                            <a class="dropdown-item" href="#">Forward
                                <i class="ri-chat-forward-line float-end text-muted"></i>
                            </a>
                            <a class="dropdown-item" href="#">
                                Delete
                                <i class="ri-delete-bin-line float-end text-muted"></i>
                            </a>
                        </div>
                    </div>
            </div>
            <div class="conversation-name">${user}</div>
        </div>
    </div>
  `   
    const clean = DOMPurify.sanitize(newMessageContent)
    newMessage.innerHTML = clean;
    chatView.appendChild(newMessage)
    chatContainer.scrollTop = chatContainer.scrollHeight
}

const renderMessages = (messageList)=>{
  JSON.parse(messageList).forEach(element => {
    formatMessage(element.fields.date_sent, element.fields.sender, element.fields.body)
  });
}

async function openChat(id){
    const url = baseUrl + id
    try {
        const chatroom = await fetch(url)
        if (!chatroom.ok) {
            throw new Error("Error fetching data");
        }
        const data = await chatroom.json()        
        console.log(data)
        document.querySelector('.ri-user-add-line').id = id
        const description = document.getElementById('chat-desc');
        description.textContent = data.room_desc

        document.getElementById('chat-sidebar-name').textContent = data.room_name
        document.getElementById('creator-name').textContent = data.room_creator
        document.getElementById('date-created').textContent = data.room_date_created
        document.getElementById('about-name').textContent = data.room_name

        chatIntro.classList.add('d-none')
        chatBox.classList.remove('d-none')
        chatName.textContent = data.room_name

        chatView.innerHTML = '';

        renderMessages(data.messages)

        chatInput.focus();

        const chatInstance = new ChatSocket(id);
        chatInstance.handleOpen

        chatSendButton.addEventListener('click',()=>{
          const message = chatInput.value
          if (message) {
              chatInstance.sendMessage(message)
          }
          chatInput.value = ''
          chatInput.focus(); 
      })

      chatInput.addEventListener('keypress', (e)=>{
            if (e.key === 'Enter') {
                e.preventDefault()
                chatSendButton.click();
            }
            chatInput.focus()
        })
        document.dispatchEvent(new Event('chatOpened'));
    } catch (error) {
      console.log(error)
    }
}


