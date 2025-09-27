SELECT * FROM games
LIMIT 10;

SELECT BGGId, Name, YearPublished, AvgRating FROM games
WHERE YearPublished >= 2015
ORDER BY AvgRating DESC
LIMIT 10;

SELECT YearPublished,
       COUNT(*) AS NumGames,
       AVG(AvgRating) AS AvgRating,
       MIN(AvgRating) AS LowestRating,
       MAX(AvgRating) AS HighestRating
FROM games
WHERE YearPublished >= 2000
GROUP BY YearPublished
ORDER BY YearPublished;

SELECT g.Name,
       ur.Username,
       ur.Rating
FROM user_ratings ur
JOIN games g ON ur.BGGId = g.BGGId
WHERE ur.Rating >= 9
ORDER BY ur.Rating DESC, g.Name
LIMIT 10;