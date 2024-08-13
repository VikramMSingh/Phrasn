Main branch is the one we want to use for submission - the commits were for removing keys

I created an oauth2 branch and made changes not to code but keys and json file - since my keys were pushed to prod - my access was revoked. 

No functionality change between main or Oauth2 Changes - only changes to app.py, config.py, requirements, and helperCreatedEmbeddings to remove hardcoded access to the keys and new keys created by me

If you test using the main branch - you will need a gemini key, json file for IAM, and oauth2 google setup 

If you want to test using the Oauth2 branch - please use this link https://phrasnai.onrender.com/ 

Sorry, for the confusion and I completely understand that this issue was my fault - but I would appreciate any feedback on the app since this is the first time I have built something with LLM or even gemini.

The docs for gemini are great and setting it up is easy - but vertex ai and some google cloud products do have documentation but finding them is difficult, reddit and gemini actually helped me figure out quite a few issues. 

Attaching the screenshot from the email from google cloud:

<img width="907" alt="image" src="https://github.com/user-attachments/assets/ced77876-7fdd-4892-a6b1-aadca4d28f4d">

