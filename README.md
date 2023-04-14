# Title: Movie Recommendation

- ToDO!
  {add test badges here, all projects you build from here on out will have tests, therefore you should have github workflow badges at the top of your repositories: [Github Workflow Badges](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)}

## Requirements / Purpose

- Purpose of project: I wanted to improve my skills with Python and Jupyter Notebook. This project allowed me to use a variety of libraries such as numpy, pandas, and sklearn, and then recommends movies using cosine similarity.
  I wanted to explore data cleaning, and how recommendation systems work. This project was an amazing experiance and was some of the most fun ive had problem solving.

---

## Build Steps

- Run the whole notebook
- Use the function callback of recommend('MOVIE_TITLE') where 'MOVIE_TITLE' is the title of the movie you have watched recently.
- Use genre_recommendation to look at collaborative choice of best movie, within the given genres

---

## Design Goals / Approach

- I implemented a simple recommendation system on a smaller dataset (4000) so I could see how different factors influenced the outcome.

---

## Features

- Takes in a movie that a user has watched and returns a list of recommended movies.
- If the movie submitted by the user is not found in the df then a message is printed to prompt them to try another movie.
- Can also receive recommendations based on genres inputted

---

## Known issues

- None that I am aware of, if you find any please let me know!

---

## Future Goals

- I would love to explore different weights on different aspects! Seeing how that would change the outcome for example weighting genre highly and director to a lesser extent.
- I want to explore collaborative filtering and additionally create a user which stores all the movies they've watched and gives them a recommendation based on their total watch history
- I would love to see a user recommendation and apply time deprecation (e.g after 10 movies a movie loses weight).

---

## Change logs

### 30/03/2023

- First implementation added, explored results when the vector took in the first three actors in the credits versus the lead actor. Found from personal preference and peer review (family and friends) that accuracy improved when we used the first three actors over one actor.

### 14/04/2023

- Added a genre recommendation system which takes in a list of genres and will filter the data frame for movies with those genres and sort them by highest collaborative average rating

## What did you struggle with?

- When creating new_movies_df I was receiving a warning that I was not modifying the original df and was modifying a copy. This was what I was intending but didn't know that I needed to be specific in my intent by declaring .copy() to remove the warning.
