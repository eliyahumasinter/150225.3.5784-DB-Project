# 🍵 Stage 1
### ERD
<img src="Stage%201/ERD.png" width="700" />

### DSD
<img src="https://github.com/eliyahumasinter/150225.3.5784-DB-Project/assets/70181151/3601c803-cf47-4d91-9cd3-85310194dbca">

### Example: count of 3 tables
```sql
SELECT COUNT(*) AS count, 'Carousel' AS table_name FROM carousel
union all
SELECT COUNT(*) AS count, 'Luggage' AS table_name FROM luggage
union all
SELECT COUNT(*) AS count, 'Employees' AS table_name FROM employee
```

Running the query results in:
```
 count  | table_name
--------+------------
   3000 | Carousel
 170000 | Luggage
   7495 | Employees
(3 rows)
```

### Database Dump
<img src="https://github.com/eliyahumasinter/150225.3.5784-DB-Project/assets/70181151/4509e11b-f24c-454f-a3ee-f5ba4f5b9a08">

### 📊 Extras 
#### Pilot wages based on experience (note: 2000 hours is considered senior level)
<img src="Stage%202/graphs/pilot_wages_to_fh.png" width="750" />

#### Airports ordered by activity
<img src="Stage%202/graphs/busiest_iata.png" width="750" />

# 🍵 Stage 2

### Back up
#### (1) 
```
pg_dump -v -f C:\Users\Eden\Desktop\backupPSQL.log -U Eden -d airline 2> C:\Users\Eden\Desktop\backupPSQL.log
```
📋 Log file: [backupSQL.log](Stage%202/backupSQL.log)

#### (2) 
```
pg_dump -v -f C:\Users\Eden\Desktop\backupPSQL.tar -U Eden -d airline 2> C:\Users\Eden\Desktop\backupPSQL.log
```
```
pg_restore -v --clean -U Eden -d airline C:\Users\Eden\Desktop\backupPSQL.tar 2>> C:\Users\Eden\Desktop\backupPSQL.log
```
📋 Log file: [backupPSQL.log](Stage%202/backupPSQL.log)

### Queries
#### (i) 
- get most encumbered plane and its total cargo weight
- get pilots who have more than 2000 flight hours and are younger than 30 and legally hired
- get employees who live in Florida, Massachusettes and Tennessee and make more than 100k/year
- get top 10 busiest airports:
- compensate all employees who earn less than 60000k with a $1000 bonus
- change terminal 10 to 9 in PEK
- remove employee who were not 2 at the time of their hiring
- remove pilots who have more than 1500 flight hours and are only employed for a year

#### (ii)
```sql
-- get most encumbered plane and its total cargo weight
select aircraft_rn, count(weight) as total from
(
	select aircraft_rn, weight from luggage
)
group by aircraft_rn
order by total desc
limit 1;


-- get pilots who have more than 2000 flight hours and are younger than 30 and legally hired
select
	first_name,
	last_name,
	(current_date - dob)/365 as age,
	flight_hours,
	(current_date - hire_date)/365 as emp_years,
	(current_date - dob)/365 - (current_date - hire_date)/365 as hiring_age
from
	pilot
where
	(current_date - dob)/365 between 18 and 30 and -- 18 <= age <= 30
	flight_hours >= 2000 and
	(current_date - dob)/365 - (current_date - hire_date)/365 >= 18; -- must have been hired above 18


-- get employees who live in Florida, Massachusettes and Tennessee and make more than 100k/year
select * from employee
where wage > 100000
      and
      (address ~~ '%FL%' or
	   address ~~ '%MA%' or
	   address ~~ '%TN%');


-- get top 10 busiest airports:
select * from
(
	select iata, count(*) as total
	from
	(
		select iata from carousel
	)
	group by iata
	order by total desc
)
limit 10;
SELECT  pg_current_logfile();

-- compensate all employees who earn less than 60000k with a $1000 bonus
UPDATE employee
SET wage = wage + 1000
WHERE wage <= 60000
RETURNING *;

-- change terminal 10 to 9 in PEK
update carousel
set terminal = 9
where iata = 'PEK' and terminal = 10
returning *;

-- remove employee who were not 2 at the time of their hiring
delete from employee
where
	(current_date - dob)/365 - (current_date - hire_date)/365 < 3
returning *;

-- remove pilots who have more than 1500 flight hours and are only employed for a year
delete from pilot
where flight_hours > 1500 and
 	 (current_date - hire_date)/365 <= 1
returning *;
```

#### (iii)
📋 Log file: [queries.log](Stage%202/queries.log)

### Parametrized queries
#### (a)
- get employees whose names sort of match a certain first/last name
- get the carousel with a load above some weight
- get the cargo distribution of a plane
- get the load and number of flights bound to a certain airport (IATA)

#### (b)
```sql
-- get employee whose names sort of match a certain first/last name
PREPARE search_emp_name (text, text) AS
SELECT *
FROM employee
WHERE first_name like FORMAT('%%%s%%', $1) AND last_name like FORMAT('%%%s%%', $2);
-- example usage:
execute search_emp_name('Raquel', 'Bolton');


-- get the carousel with a load > some amount
PREPARE min_carousel_load(int) AS
SELECT carousel_id, SUM(total) as kg FROM
(
	SELECT carousel_id, total FROM
	(
		SELECT aircraft_rn as rn, COUNT(weight) AS total 
		FROM luggage
		GROUP BY aircraft_rn
		ORDER BY total DESC
	)
	INNER JOIN carousel_aircraft
		ON rn = carousel_aircraft.aircraft_rn
)
GROUP BY carousel_id
HAVING SUM(total) >= $1
ORDER BY kg desc;
-- example usage:
execute min_carousel_load(1000);


-- get the cargo distribution of a plane
PREPARE plane_cargo_dist(text) AS
SELECT
    l_type AS type,
	round(
		AVG(amount) / (
			SELECT SUM(amount) FROM
			(
				SELECT type as l_type, count(type) AS amount FROM
				(
					SELECT l.aircraft_rn, l.type FROM
					(
						SELECT * FROM luggage
						WHERE aircraft_rn = $1

					) AS l
					JOIN carousel_aircraft
						ON l.aircraft_rn = carousel_aircraft.aircraft_rn
				)
				GROUP BY type
			)
		), 2
	) AS percent
FROM
(
	SELECT type AS l_type, count(type) AS amount FROM
	(
		SELECT l.aircraft_rn, l.type FROM
		(
			SELECT * FROM luggage
			WHERE aircraft_rn = $1

		) AS l
		JOIN carousel_aircraft
			ON l.aircraft_rn = carousel_aircraft.aircraft_rn
	)
	GROUP BY type
)
GROUP BY l_type;
-- example usage
execute plane_cargo_dist('N-368UF');


-- get the load and number of flights bound to a certain airport (iata)
PREPARE dest_load_count(text) AS
SELECT dest, sum, count FROM -- iata with its weights
(
	SELECT dest, SUM(total_kg) FROM
	(
		-- dest and its weight
		SELECT iata as dest, total_kg FROM
		(
			-- planes their kg with their carousel
			SELECT rn, total_kg, carousel_id FROM
			(
				-- planes and their kg
				SELECT aircraft_rn as rn, COUNT(weight) AS total_kg
				FROM luggage
				GROUP BY aircraft_rn
			)
			JOIN carousel_aircraft
				ON rn = carousel_aircraft.aircraft_rn
		) AS x
		JOIN carousel
			ON x.carousel_id = carousel.carousel_id
	)
	GROUP BY dest
	HAVING dest = $1
)
JOIN
(
	-- iata with its plane count
	SELECT iata, COUNT(iata) FROM carousel_aircraft
	JOIN carousel
		ON carousel_aircraft.carousel_id = carousel.carousel_id
	GROUP BY iata
	HAVING iata = $1
)
	ON dest = iata;
-- example usage
execute dest_load_count('TLV');
```

#### (c)
📋 Timings and Logs: [paramsqueries.log](Stage%202/paramsqueries.log)

### Indexed structures
#### (A)
```sql
create index employee_names on employee(first_name, last_name);
create index carousel_ids on carousel(carousel_id);
create index luggage_plane on luggage(aircraft_rn);
```

#### (B)
```sql
execute search_emp_name('Edw','L');
Time: 1.869 ms

execute min_carousel_load(500);
Time: 21.064 ms

execute plane_cargo_dist('N-368UF');
Time: 1.655 ms

execute dest_load_count('CGK');
Time: 20.927 ms
```

#### (C)
```sql
execute search_emp_name('Edw','L');
Prev Time: 2.173 ms

execute min_carousel_load(500);
Prev Time: 21.505 ms

execute plane_cargo_dist('N-368UF');
Prev Time: 19.372 ms

execute dest_load_count('CGK');
Prev Time: 22.112 ms
```

#### (D)
📋 Log file: [constraints.log](Stage%202/constraints.log)

### Constraints
#### (1)
```sql
ALTER TABLE employee ADD CONSTRAINT age_constraint CHECK
(
	(current_date - dob)/365 >= 18
);

ALTER TABLE employee ADD CONSTRAINT id_constraint UNIQUE (emp_id);

ALTER TABLE pilot ADD CONSTRAINT fhours_empdays_ratio CHECK
(
    -- flight_hours <= (employment days) * daily avg
	flight_hours <= (current_date - hire_date) * 2.302
);

ALTER TABLE carousel ADD CONSTRAINT cid_constraint UNIQUE (carousel_id);

ALTER TABLE carousel ADD CONSTRAINT terminal_constraint CHECK
(
    terminal between 1 and 10
);

ALTER TABLE carousel ADD CONSTRAINT capacity_constraint CHECK
(
    capacity between 800 and 3000
);

ALTER TABLE carousel_aircraft ADD CONSTRAINT rn_constraint CHECK
(
    -- N-000AA to N-999ZZ
    aircraft_rn ~ '^N-\d{3}[A-Z]{2}'
);

ALTER TABLE luggage ADD CONSTRAINT rn_constraint CHECK
(
    -- N-000AA to N-999ZZ
    aircraft_rn ~ '^N-\d{3}[A-Z]{2}'
);
```

#### (2)
```sql
DELETE FROM pilot
WHERE flight_hours > (current_date - hire_date) * 2.302;
DELETE 268
Time: 4.150 ms

INSERT INTO pilot ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date", "flight_hours") VALUES (207, 'Lee', 'Chandler', 332236.2, '2014/6/20', '305 Broderick Place, Panama City Beach, FL, 32413', '2002/9/4', '18062');
ERROR:  new row for relation "pilot" violates check constraint "age_constraint"
DETAIL:  Failing row contains (207, Lee, Chandler, 332236.2, 2014-06-20, 305 Broderick Place, Panama City Beach, FL, 32413, 2002-09-04, 18062).
Time: 11.564 ms

INSERT INTO pilot ("emp_id", "first_name", "last_name", "wage", "dob", "address", "hire_date", "flight_hours") VALUES (207, 'Lee', 'Chandler', 332236.2, '1960/6/20', '305 Broderick Place, Panama City Beach, FL, 32413', '2000/9/4', '20026');
ERROR:  new row for relation "pilot" violates check constraint "fhours_empdays_ratio"
DETAIL:  Failing row contains (207, Lee, Chandler, 332236.2, 1960-06-20, 305 Broderick Place, Panama City Beach, FL, 32413, 2000-09-04, 20026).
Time: 12.054 ms

INSERT INTO carousel_aircraft VALUES (2285, 'X-207JQ');
ERROR:  new row for relation "carousel_aircraft" violates check constraint "rn_constraint"
DETAIL:  Failing row contains (2285, X-207JQ).
Time: 7.327 ms

INSERT INTO carousel VALUES (3, 1520, 13, 'BLR');
ERROR:  new row for relation "carousel" violates check constraint "terminal_constraint"
DETAIL:  Failing row contains (3, 1520, 13, BLR).
Time: 7.226 ms
```

#### (3)
For the pilot error, there were some pilots whose accrued flight hours was larger than the average flight hours for a given pilot during the same period. Hence, this would be a clerical error (maybe even purposeful - since more hours = hire salary).

#### (4)
```sql
ALTER TABLE employee ADD CONSTRAINT age_constraint CHECK
(
	(current_date - dob) >= 18 * 365
);
```
- This will check if the age of an employee is greater than 18

```sql
ALTER TABLE pilot ADD CONSTRAINT fhours_empdays_ratio CHECK
(
	flight_hours <= (current_date - hire_date) * 2.302
);
```
- Flight_hours must be <= (employment days) * daily avg 
- Daily average is calculated by 840 (avg hrs/month) divided by 365

```sql
ALTER TABLE carousel ADD CONSTRAINT terminal_constraint CHECK
(
    terminal between 1 and 10
);
```
- Max terminal # between 1 and 10

```sql
ALTER TABLE carousel_aircraft ADD CONSTRAINT rn_constraint CHECK
(
    aircraft_rn ~ '^N-\d{3}[A-Z]{2}'
);
```
- Using regex, we can constrain aircraft_rn to be between N-000AA and N-999ZZ as stated here:
<a href="https://en.wikipedia.org/wiki/Aircraft_registration#United_States">US Aircraft Registration</a>
