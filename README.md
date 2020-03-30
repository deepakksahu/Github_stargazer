We would like to be able to analyze the Star Count over time of github repositories. For this, we need to generate a dataset containing the relevant information in an easily processable format. We would like you to write code to extract star count information from a GitHub repository and create the dataset with this information. We are interested in how many people "starred" a given repository per time interval.

**Solution to Technical Task for a position of Data Engineer @ Marley Spoon**

**Description:**

We would like to be able to analyze the Star Count over time of github repositories. For this, we need to generate a dataset containing the relevant information in an easily processable format. We would like you to write code to extract star count information from a GitHub repository and create the dataset with this information. We are interested in how many people "starred" a given repository per time interval.
You do not need to group the data per time interval but allow another team to define the interval and easily group the data.

**Approach:**
1. Create a class which will consist of all the API calls.
2. In the **main.py** create an object for the class and use the same
   for any api call.
3. Modularise the code according to their functioning.
4. Add logging for better debugging.
5. Add required comments to increase the readability of the code.
6. Add the docker file to containerize the solution.
7. Add all the dependency in requirements.txt.
8. Write the DF to s3 as well as postgres.
9. Add the airflow DAG consider we have k8s to spin pods.

**Command:**  
`python main.py  --configs '{"repo_name":"grab/hackathon","password":"R4#h8j9!c22kwxV","username":"useyourmail@gmail.com","s3_output_location": "s3://marleyspoon_datalake/github_analysis/" }'`

**Config:**  
*A variable to be created in Airflow named: starcounter_conf*

       {"repo_name":"grab/hackathon","password":"R4#h8j9!c22kwxV",  
       "username":"useyourmail@gmail.com",  
       "s3_output_location": "s3://marleyspoon_datalake/github_analysis/" }

**Deployment:**  
Image (named *star-data-ingestion*) to be build using Jenkins and and update in the airflow variable  *mspoon_images_config*

Schedule in the DAG is for everyday.

*P.S : All the scheduling assumption as per the current env. I am working. This can very accordingly.*

