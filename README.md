Phrasn: Bridging Educational Gaps Through Language

Phrasn means "question" in Hindi, and our mission is to make high-quality education accessible to students in their native languages.

Inspiration - https://www.brookings.edu/articles/radical-inclusion-means-teaching-children-in-a-language-they-understand/ ; https://www.isas.nus.edu.sg/papers/language-barriers-inequalities-of-indias-national-education-policy/

In today’s world, education remains a powerful tool for social mobility, yet access to quality learning resources is starkly unequal. This gap is particularly evident in underprivileged communities, where students often face insurmountable barriers to accessing the best educational materials and resources. These barriers are further exacerbated for non-English-speaking students, who must contend not only with a lack of resources but also with language obstacles that limit their learning potential. Lack of academic progress causes students to drop out, hampering their chances of economic success - which for them is moving out of poverty.

The impact of Phrasn goes beyond individual students; it’s about creating a ripple effect that can transform entire communities. Education is the key to breaking the cycle of poverty, and by making high-quality learning accessible to those who need it most, we’re laying the foundation for a brighter, more equitable future. 

Phrasn currently supports the following languages:

    English (en)
    Español (es)
    Swahili (sw)
    Chinese (zh)
    Hindi (hi)
    Bengali (bn)
    Arabic (ar)
    Hausa (ha)
    Amharic (am)
    Indonesian (id)



References:
Book used for RAG - https://openstax.org/details/books/physics/
Coding resources - https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/use-cases / Gemini AI chatbot


Main branch is the one we want to use for submission - the commits were for removing keys

I created an oauth2 branch and made changes not to keys and json file - since my keys were pushed to prod - my access was revoked. 

No functionality change between main or Oauth2 Changes - only changes to app.py, config.py, requirements, and helperCreatedEmbeddings to remove hardcoded access to the keys and to reduce vertex ai costs.

Main Branch

The main branch is intended for submission due to the deadline. If you’re testing this branch, you'll need the following setup:

    Gemini Key: Obtain an API key from the Google Cloud Console for Gemini.
    Vertex AI Key: Set up Vertex AI and obtain the necessary API key.
    IAM JSON File: Generate a service account JSON file with the appropriate IAM permissions.
    OAuth2 Setup: Configure Google OAuth2 to allow users to authenticate with your app.

After setting up the above, you can run the app locally or deploy it using your preferred cloud provider.

OAuth2 Branch

Changes in this branch focus on securing access by removing hardcoded keys and JSON files, and to reduce Vertex AI costs. There is no functionality change between the main and OAuth2 branches.

Test the app using the OAuth2 branch - https://phrasnai.onrender.com/ 

Sorry, for the confusion and I completely understand that this issue was my fault - but I would appreciate any feedback on the app since this is the first time I have built something with AI/GEMINI and actually pushed it to production.

The docs for gemini are great and setting it up is easy - but vertex ai and some google cloud products do have documentation but finding them is difficult, reddit and gemini chatbot/community actually helped me figure out quite a few issues. (not a developer - so maybe I am not good at navigating the documentation)

Attaching the screenshot from the email from google cloud:

<img width="907" alt="image" src="https://github.com/user-attachments/assets/ced77876-7fdd-4892-a6b1-aadca4d28f4d">

