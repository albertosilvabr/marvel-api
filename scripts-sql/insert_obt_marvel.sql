INSERT INTO obt_marvel
SELECT ch.id          AS character_Id
     , ch.name        AS character_name
     , ch.description AS character_description
     , ch.modified    AS character_modified
     , c.id           AS comic_id
     , c.title        AS title_comic
     , c.formatt 
  FROM `characters` ch INNER JOIN comics c ON ch.id = c.characterId 
 GROUP BY ch.id 
     , ch.name
     , ch.description
     , ch.modified
     , c.id 
     , c.title
     , c.formatt
     