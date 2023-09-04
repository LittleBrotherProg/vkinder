<h1 align = center>Командная курсовая работа<br>VKibder</h1>
<h3 align = right>Developed by</h3>
<p align = right>Ivan Dolinkin</p>
<p align = right>Grigory Kaplin</p>
<h2 align = center>Documentation</h2>
<ol>
  <li>Getting started</li>
  <p>Before you start working with vkinder you need to install additional libraries </p>
  <p>Type the command "pip install -r requirements.txt" into the console</p>
  <p>Now we need to create a database on postgresql</p>
  <p>In the terminal, run the command: createdb -U postgres vkinder_db</p>
  <p>And the last point you need to go to vkinder/database/ and start the file create_tables.py to create tables in the database</p>
  <p>In the .env file, specify your data for connecting to the database</p>
  <p>Environment variables are used in the program. In the file handlers.py, line 28. Here instead of os.getenv('vkinder') you should insert the group token. And also in the file action.py instead of os.getenv('USERVK') you need to insert the token from your page.</p>
  <li>Bot fields
    <ol type="1">
      <li>main.py</li>
      <p>The main.py file is used to launch the bot</p>
      <li>handlers.py</li>
      <p>Handlers.py contains handlers that help the bot understand what action it needs to process now</p>
      <li>creation.py</li>
      <p>This file is responsible for creating the keyboard. In the next releases the following functions will be added to the file: finding photos by maximal likes, collecting data to form a dating user card</p>
      <li>action.py</li>
      <p>The file is responsible for requests to API_VK and returning the obtained results from executed requests</p>
      <li>database
        <ol type="1">
          <li>create_tables.py</li>
          <p>Creates tables in the database</p>
          <li>add.py</li>
          <p>Responsible for all database queries to add new records</p>
          <li>update.pu</li>
          <p>Responsible for all database queries to update data</p>
          <li>get.py</li>
          <p>Responsible for all queries to retrieve data from the database</p>
          <li>delete.py</li>
          <p>Responsible for all queries to remove data from the database</p>
          <li>button.py</li>
          <p>to speed up the work with the database, the file contains functions in each of which the necessary queries for the bot buttons are combined</p>
        </ol>
      </li>
    </ul>
  </li>
  <li>Working with the bot
    <ol type="1">
      <li>To access the bot, follow the link and join the group       
          <link>https://vk.com/invite/IBK0E2s</link></li>
      <li>Click on the "Сообщение" button to the right of the group name and go into a dialog with the bot</li>
      <li>Click the button "Начать"</li>
      <li>Next, the bot will say hello to you and ask you to enter the data to register you.</li>
      <li>After registration you will see the main functionality of the bot, which consists of the following buttons
        <ol type="1">
          <li>"Начать знакомства"</li>
          <p>The bot performs the function of searching for people for dating by your age and city, which you specified during registration. After the search function is completed, the bot will send you the first card of the found user according to the criteria described above and open new features in the form of new buttons.
            <ol type="1">
              <li>"Следующий"</li>
              <p>when the button is pressed, the bot will switch to the card of the next found user</p>
              <li>"❤"</li>
              <p>when the button is pressed, it will save the user in the database as a favoriteuser</p>
              <li>"🚫"</li>
              <p>When clicked, will add the user to the blacklist. After adding this user will not appear in your search.</p>
              <li>"Главное меню"</li>
              <p>Returns you to the main menu</p>
            </ol>
          </p>
          <li>"Понравившиися"</li>
          <p>Opens a list of users you like with the following buttons
            <ol type="1">
              <li>"Следующий"</li>
              <p>when the button is pressed, the bot will switch to the map of the next favorite                   user</p>
              <li>"💔"</li>
              <p>The button should remove the user from the list of liked but in the final                       testing of this version showed unstable operation and has been disabled and is waiting for its finalization</p>
              <li>"Главное меню"</li>
              <p>Returns you to the main menu</p>
            </ol>
          </p>
          <li>"Чёрный список"</li>
          <p>The button should show people from the black list and give an opportunity to remove them from it. At the moment the functionality is not developed and is expected in the next version.</p>
          <li>"Изменить данные"</li>
          <p>The button should allow you to change the data you entered during registration, but it doesn't work yet.</p>
        </ol>
      </li>
    </ol>
  </li>
</ol>
