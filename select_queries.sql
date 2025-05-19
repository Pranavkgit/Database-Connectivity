SELECT l.name, COUNT(m.id) as maximum
FROM assgn.Match as m,league as l
WHERE m.league_id = l.id and m.date LIKE '%2016%'
GROUP BY l.name
ORDER BY maximum DESC  LIMIT 1;

SELECT t.team_long_name AS team, l.name as name, m.season as season, greatest(m.home_team_goal,m.away_team_goal) AS maximum_goals
FROM assgn.Match as m,Team as t,League as l where
m.home_team_api_id = t.team_api_id OR m.away_team_api_id = t.team_api_id and  m.league_id = l.id
ORDER BY maximum_goals DESC LIMIT 10;

SELECT p.player_name, COUNT(m.id) AS matches_scored
FROM assgn.Match as m,Player as p,Team as t
WHERE m.goal LIKE CONCAT('%', p.player_api_id, '%') and (m.home_team_api_id = t.team_api_id OR m.away_team_api_id = t.team_api_id) and
t.team_long_name = 'Manchester United' AND m.date LIKE '%2008%'
GROUP BY p.player_name
ORDER BY matches_scored DESC LIMIT 2;

SELECT COUNT(m.id) AS total
FROM assgn.Match m, team as t
where( m.home_team_api_id = t.team_api_id OR m.away_team_api_id = t.team_api_id )and
t.team_long_name = 'Manchester United' AND m.date LIKE '%2011%';

SELECT p.player_name, COUNT(m.id) AS away_matches, p.id,p.player_api_id,p.player_name,p.player_fifa_api_id,p.birthday,p.height,p.weight
FROM assgn.Match as m, player as p,team as t
where p.player_api_id IN (
    m.away_player_1, m.away_player_2, m.away_player_3, m.away_player_4, m.away_player_5,
    m.away_player_6, m.away_player_7, m.away_player_8, m.away_player_9, m.away_player_10, m.away_player_11
) and m.away_team_api_id = t.team_api_id
and t.team_long_name = 'Manchester United' AND m.season = '2008/2009'
GROUP BY p.player_name
ORDER BY away_matches DESC
LIMIT 1;