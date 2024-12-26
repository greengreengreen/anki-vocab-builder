Project description: 

MVP: Given a csv file with a list of words, the user should be able to create a deck of anki cards. 
At the front side of the anki card, the user should see a quiz question for the word/phrase. The quiz should be able to be audible. 
At the back side of the anki card, the user should see the pronunciation, meaning of the word, example sentences of the word, and generate an image to explain the word. 


For the content generation such as quiz, meaning, example sentences, and image, I plan to generate using open ai developer API. 
For audio, what to use? 

A few questions: 
What is the desired format that anki requires so that users can have cloze? I.e. quiz questions? 
Must have quiz. 
How do we plan to download audios for both quiz questions and pronunciation? Yes. 
How to make the sourcing easy? A csv file is fine for now, but no one use a csv file daily. Ideally, if the user right clicks a word, we should be able to add the word. 
Can assume users want to add the word anytime, but we only batch generate flashcards. So there need to be somewhere staging the words which wait to be generated. Should we use our raspberry pi here? 
Using raspberry pi is optionally. Priotize on having a mvp. 
What about other kinds of deck? Things that have different patterns than vocabulary decks? 
Let me describe the pattern difference. 
Vocab decks: I would copy the word from anywhere and then expect chatgpt/openAI to find me quiz and example sentences, explanations. 
Tech decks: I would usually start with reading a blog or a chapter in some books, and then I summazie the content somewhere. And I want to quiz myself. 
What is your priority? 
First build the voab deck automation. And then we extend to tech decks. 
