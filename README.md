# API-Project-Chat Sentiment Analysis Service

**Description:** Analyze the `public` chat messages (like slack public channels) of a team and create sentiment metrics of the different people on the team. 

## API Endpoints

API created with this endpoints:

api_get.py
### 1. GET
- requests.get('http://localhost:8080/').json()
  - **Returns:** All the information about the users in each chat on the API.
- requests.get('http://0.0.0.0:8080/usernames').json()
  - **Returns:** All the usersnames in the chats of the API.
- requests.get('http://localhost:8080/chats').json()
  - **Returns:** All the existing chats of the API.
- requests.get('http://localhost:8080/chat/x/list').json()
  - **Returns:** All the messages from the chat x.
- requests.get('http://localhost:8080/chat/x/sentiment').json()
  - **Returns:** The sentiment evaluation of each text in chat x and the average feeling in that chat.

api_post.py
### 2. POST
- `/user/create` 
  - **Purpose:** Create a user and save into DB
  - **Params:** `username` the user name
  - **Returns:** the new `user_id` created
  Raises an error if the user name already exists
- `/chat/x/adduser` 
  - **Purpose:** Add a user to a chat x
  - **Params:** `user_id`
  - **Returns:** `chat_id` where the user has been added
- `/chat/<chat_id>/addmessage` 
  - **Purpose:** Add a message to the conversation.
  - **Params:**
    - `chat_id`: Chat to store message
    - `user_id`: the user that writes the message
    - `text`: Message text
  - **Returns:** the new `message_id` of the added message.

recommending.py
### 3. GET
- `/user/<user_id>/recommend`  
  - **Purpose:** Recommend friend to this user based on chat contents
  - **Returns:** json array with top 3 similar users
  Raises an error if the sentiments from that user haven't been analyzed (because either the user doesn't exist of the sentiments aren't loaded in the DB)


