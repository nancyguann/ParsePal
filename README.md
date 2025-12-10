# ParsePal
An extensible framework for natural language processing

---

## About ParsePal

Propaganda has birthed movements and driven chagne throughout history. With the abundance of information readily available in the moden age, it is important to identify propganda when it appears an understand how it works. The main goal of this project is to dissect historic speeches and identify the mthods used to persaude its audience. 

---

## Speeches

* Winston Churchill - We Shall Fight on the Beaches
* Franklin D. Roosevelt - Day of Infamy
* Ronald Reagan - Evil Empire
* George W. Bush - Axis of Evil
* Saddam Hussein - Invasion of Kuwait
* Adolf Hitler - Invasion of Poland
* Vladimir Putin - Invasion of Ukraine
* Benito Mussolini - Rome 1941

---

##  Process and Methods

The Text-to-Word Sankey diagram shows the most common words in each speech, with the thickness of the connection representing the count of that word in the text. A list of "stop words" were accounted for to remove commonly used words like pronouns and articles.

The subplots highlight the emotional appeals throughout each speech. The four emotions accounted for are fear, anger, hope, and pride. In a separate file, there is a dictionary with a list of words pertaining to each emotion, and more matches in the speech correspond to a higher score for that category. 

The multi-dimensional bubble plot accounts for the aggression, certainty, emotional intensity, and overall elxical diversity. Like the subplots, words are matched to a dictionary of specific words, and more matches equates to a higher score. 

---

##  Findings and Analysis

* Most common emotional appeals: fear, hope, and pride
* Most emotional appeal overall: FDR's Day of Infamy
* Almost all speeches had relatively low lexical diversity, except for FDR's
* Heavy use of patriotism and a gradual increase of emotional appeals as speeches progressed

---

### Conclusion and Next Steps

The speeches that differed the most were from FDR and Hitler, which coincidentally corresponds to the Allied and Axis powers in World War II. Repetition, or low lexical diversity is frequently used in propaganda in order to create memorable and repeatable messages for the masses. FDR's speech had the highest lexical diversity and emotional appeal level, suggesting it to be more of a report rather than propaganda. Nationalism is universit and frequently used in every speech. 

In the future, speeches from current leaders could be analyzed to see the trends of modern day propaganda and if they have evolved from the past. Speeches could also all be from democratic or authoritarian leaders to create a more ideologicall-localized analysis of propaganda patterns. 
