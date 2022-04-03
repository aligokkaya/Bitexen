# Bitexen-Code-Challenge

Bitexen Code Challenge  
Task Definition  
Basically we want to create an order-book tracker service. It works with market code  
like ​ BTC/TRY ​ and uses the last transactions in the API endpoint.  
● Requirements (​ Must have ​ ):  
○ Read data from our order-book endpoint for every five seconds and keep the required part into the database.  
○ Create statistics from data for the different resolutions and save it  
continuously.
■ We want to see following statistic points of work for target
market:  
● Minimum price  
● Maximum price  
● Average price  
● Total volume  
■ Resolution set of statistics:  
● Daily  
● Weekly  
● Monthly  
○ We are waiting to create your own job scheduler for the above items.  
● Optional Requirements (​ Nice to have ​ ):  
○ Publish statistics over API  
○ Dockerize project  
○ Write unit tests  
General Rules  
● Write in any programming language and design your tech-stack as you prefer.  
● Write documentation for service.  
● Upload your code into git providers like Github, Gitlab or Bitbucket. When you
are ready, notify by email and give access to us for the code review process.  
Please make your repository private . ​  
● We are waiting for you to return with an estimation for the task after receiving  
email. It depends on you. But we expect you to keep up with the estimation.  
  
  
  
  
  
  
  
for flask   
docker build ./ --tag bitexen  
docker run --restart always -d --network=host --name bitexendeploy bitexen  

  
for FASTAPI  
docker build ./ --tag bitexenfastapi  
docker run --restart always -d --network=host --name fastdeploy bitexenfastapi  

