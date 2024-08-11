# 🍵 Stage 1
### Data Generation
🗒️ For more specific cases: [data_gen.py](Stage%201/pyenv/data_gen.py) \
🗒️ Main gen file:           [generate_data.py](Stage%201/pyenv/generate_data.py) \
🗒️ Contains random data:    [rand_data.py](Stage%201/pyenv/rand_data.py)

### Insert Files
🗒️ Attendants: [attendant.sql](Stage%201/init_sql/attendant.sql) \
🗒️ Carousels: [carousel.sql](Stage%201/init_sql/carousel.sql) \
🗒️ Carousel-Aircrafts: [carousel_aircraft.sql](Stage%201/init_sql/carousel_aircraft.sql) \
🗒️ Ground Crew: [ground_crew.sql](Stage%201/init_sql/ground_crew.sql) \
🗒️ Luggage: [luggage.sql](Stage%201/init_sql/luggage.sql) \
🗒️ Medic: [medic.sql](Stage%201/init_sql/attendant.sql) \
🗒️ Pilot: [pilot.sql](Stage%201/init_sql/pilot.sql) 

### ERD
<img src="Stage%201/ERD.png" width="700" />

### DSD
<img src="Stage%201/fixeddsd1.png" width="700"> 

- Due to 3NF, Carousel_Aircraft was created to fix the problem where aircraft_rn could only be assigned once to a specific carousel, but vice versa is allowed (a carousel can service a few planes)
- An aircraft can have multiple luggage 
- Employee will hold the aggregation of all the workers

### Example: count of 3 tables
```sql
SELECT COUNT(*) AS count, 'Carousels' AS table_name FROM carousel
UNION ALL
SELECT COUNT(*) AS count, 'Luggages' AS table_name FROM luggage
UNION ALL
SELECT COUNT(*) AS count, 'Employees' AS table_name FROM employee
```

Running the query results in:
```
 count  | table_name
--------+------------
   3000 | Carousels
 170000 | Luggages
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
SELECT aircraft_rn, count(weight) AS total FROM
(
	SELECT aircraft_rn, weight FROM luggage
)
GROUP BY aircraft_rn
ORDER BY total DESC
LIMIT 1;


-- get pilots who have more than 2000 flight hours and are younger than 30 and legally hired
SELECT
	first_name,
	last_name,
	(current_date - dob)/365 as age,
	flight_hours,
	(current_date - hire_date)/365 as emp_years,
	(current_date - dob)/365 - (current_date - hire_date)/365 as hiring_age
FROM
	pilot
WHERE
	(current_date - dob)/365 BETWEEN 18 AND 30 AND -- 18 <= age <= 30
	flight_hours >= 2000 AND
	(current_date - dob)/365 - (current_date - hire_date)/365 >= 18; -- must have been hired above 18


-- get employees who live in Florida, Massachusettes and Tennessee and make more than 100k/year
SELECT * FROM employee
WHERE wage > 100000
      AND
      (address ~~ '%FL%' OR
	   address ~~ '%MA%' OR
	   address ~~ '%TN%');


-- get top 10 busiest airports:
SELECT * FROM
(
	SELECT iata, count(*) AS total
	FROM
	(
		SELECT iata FROM carousel
	)
	GROUP BY iata
	ORDER BY total DESC
)
LIMIT 10;

-- compensate all employees who earn less than 60000k with a $1000 bonus
UPDATE employee
SET wage = wage + 1000
WHERE wage <= 60000
RETURNING *;

-- change terminal 10 to 9 in PEK
UPDATE carousel
SET terminal = 9
WHERE iata = 'PEK' AND terminal = 10
RETURNING *;

-- remove employee who were not 2 at the time of their hiring
DELETE from employee
WHERE
	(current_date - dob)/365 - (current_date - hire_date)/365 < 3
RETURNING *;

-- remove pilots who have more than 1500 flight hours and are only employed for a year
DELETE from pilot
WHERE flight_hours > 1500 AND
 	 (current_date - hire_date)/365 <= 1
RETURNING *;
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
WHERE first_name LIKE FORMAT('%%%s%%', $1) AND last_name LIKE FORMAT('%%%s%%', $2);
-- example usage:
EXECUTE search_emp_name('Raquel', 'Bolton');


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
EXECUTE min_carousel_load(1000);


-- get the cargo distribution of a plane
PREPARE plane_cargo_dist(text) AS
SELECT
    l_type AS type,
	round(
		AVG(amount) / (
			SELECT SUM(amount) FROM
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
EXECUTE plane_cargo_dist('N-368UF');


-- get the load and number of flights bound to a certain airport (iata)
PREPARE dest_load_count(text) AS
SELECT dest, sum, count FROM -- iata with its weights
(
	SELECT dest, SUM(total_kg) FROM
	(
		-- dest and its weight
		SELECT iata AS dest, total_kg FROM
		(
			-- planes their kg with their carousel
			SELECT rn, total_kg, carousel_id FROM
			(
				-- planes and their kg
				SELECT aircraft_rn AS rn, COUNT(weight) AS total_kg
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
EXECUTE dest_load_count('TLV');
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
    terminal BETWEEN 1 AND 10
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

# 🍵 Stage 3
### Queries
#### (i) 
* Count Luggage by Type for Each Carousel
* Retrieve Luggage Details with Carousel Information
* Find the top 10 highest earners from the attendant, pilot, medic, and ground_crew tables

#### (ii)
```sql
SELECT * FROM
(
	SELECT c.carousel_id, l.type, COUNT(l.tag) AS luggage_count
	FROM Carousel c
	LEFT JOIN carousel_aircraft ca
		ON c.carousel_id = ca.carousel_id
	LEFT JOIN Luggage l
		ON ca.aircraft_rn = l.aircraft_rn
	GROUP BY c.carousel_id, l.type
	Order BY c.carousel_id
)
WHERE type IS NOT NULL;
```
We select from carousel by joining it with carousel_aircraft (on carousel ids) and with luggages (on aircraft_rn) and grouping by the id and type (and then counting how many of those in each pairing

```sql
SELECT * FROM
(
	SELECT l.tag, l.type, l.weight, c.carousel_id, c.capacity, c.terminal, c.iata
	FROM public.luggage l
	LEFT JOIN public.carousel_aircraft ca
		ON l.aircraft_rn = ca.aircraft_rn
	LEFT JOIN public.carousel c
		ON ca.carousel_id = c.carousel_id
)
WHERE iata IS NOT NULL;
```
Select from the joining of luggage with carousel_aircraft and carousels (based on their respective shared column)

```sql
(
	SELECT emp_id, first_name, last_name, wage, 'Attendant' AS employee_type
	FROM public.attendant
	ORDER BY wage DESC LIMIT 10
)
UNION ALL
(
	SELECT emp_id, first_name, last_name, wage, 'Pilot' AS employee_type
	FROM public.pilot ORDER BY wage DESC LIMIT 10
)
UNION ALL
(
	SELECT emp_id, first_name, last_name, wage, 'Medic' AS employee_type
	FROM public.medic ORDER BY wage DESC LIMIT 10
)
UNION ALL
(
	SELECT emp_id, first_name, last_name, wage, 'Ground Crew' AS employee_type
	FROM public.ground_crew ORDER BY wage DESC LIMIT 10
)
ORDER BY wage DESC;
```
From each table we select the top 10 earners, union them and order by the wage

### Views and Visualizations
```sql

-- 1)
-- This will create a view containing all over paid attendants 
-- defined as getting paid more than $100/hr and having worked less than 5 years
create or replace view overPaidAttendants as 
	select "firstName", "lastName", "wage", "empDate", "dob"
	from attendant
	where "wage" > 100 and "empDate" > CURRENT_DATE - INTERVAL '5 year';
	
-- Get all flight attendants that we can force to retire (older than 65) that we pay too much
select "firstName", "lastName", "dob" from overPaidAttendants 
where DATE_ADD("dob", INTERVAL '65 YEAR') < CURRENT_DATE;

-- Get the number of overpaid flight attendants based on ages of 5 year increments
SELECT
  FLOOR(EXTRACT(YEAR FROM CURRENT_DATE) / 5) * 5  -
  FLOOR(EXTRACT(YEAR FROM dob) / 5) * 5 AS age_range,
  COUNT(*) AS number_of_people
FROM overpaidattendants
GROUP BY FLOOR(EXTRACT(YEAR FROM CURRENT_DATE) / 5) * 5  -
  FLOOR(EXTRACT(YEAR FROM dob) / 5) * 5
ORDER BY age_range;
```

![Overpaid flight attendants by age](https://github.com/user-attachments/assets/711e4b28-6e77-4c19-9ecc-0438cecfb0fe)
```sql
-- Fire (delete) all flight attendants that meet the above criteria 
delete from attendant 
where ("firstName", "lastName") in (select "firstName", "lastName" from overPaidAttendants where DATE_ADD("dob", INTERVAL '65 YEAR') < CURRENT_DATE);



-- 2)
--Dulles International Airport wants to find all of their carousels that have a capacity less than 50
create or replace view SmallCapacityCarouselsAtDulles as 
	select "carouselId", "size"
	from carousel
	where iata='IAD' and size<50;

-- Get how many carousels need to be upgraded
select count("carouselId") from SmallCapacityCarouselsAtDulles;

-- Perform upgrade on all such carousels by updating them to a capacity of 100
update SmallCapacityCarouselsAtDulles
set size=100
where "carouselId" in (select "carouselId" from SmallCapacityCarouselsAtDulles);



 
-- 3)
-- Create a view that has all equipment luggage
create or replace view equipmentLuggage as 
	select tag, weight from luggage
	where type='equipment' WITH CHECK OPTION;

	
-- Count the number of heavy equipment luggage
select count(*) from equipmentLuggage where weight> 95;

-- Get all equipment tag ids where the weight is greater than 95
select tag from equipmentLuggage where weight> 95;

-- Remove all heavy equipment pieces of luggage between 100 and 200
delete from equipmentLuggage where tag>100 and tag <200 and weight >50;


--4)
-- Create a view with all company employees contact info
create view contacts as 
	select "empId", "firstName", "lastName", "address"
	from employee with check option;
	
	
-- Get all company employees from the state of Alabama
select * from contacts where address LIKE '%AL,%';

-- Get the number of employees that live in each type of street ending (road, ave, st, lane, circle, court, other)
SELECT
  CASE
    WHEN LOWER(address) LIKE '%road%' OR LOWER(address) LIKE '%rd%' THEN 'Road/Rd'
    WHEN LOWER(address) LIKE '%avenue%' OR LOWER(address) LIKE '%ave%' THEN 'Avenue/Ave'
    WHEN LOWER(address) LIKE '%drive%' THEN 'Drive'
    WHEN LOWER(address) LIKE '%street%' OR LOWER(address) LIKE '%st%' THEN 'Street/St'
    WHEN LOWER(address) LIKE '%lane%' THEN 'Lane'
    WHEN LOWER(address) LIKE '%circle%' THEN 'Circle'
    WHEN LOWER(address) LIKE '%court%' THEN 'Court'
    ELSE 'Other'
  END AS street_type,
  COUNT(*) AS number_of_people
FROM contacts
GROUP BY 
  CASE
    WHEN LOWER(address) LIKE '%road%' OR LOWER(address) LIKE '%rd%' THEN 'Road/Rd'
    WHEN LOWER(address) LIKE '%avenue%' OR LOWER(address) LIKE '%ave%' THEN 'Avenue/Ave'
    WHEN LOWER(address) LIKE '%drive%' THEN 'Drive'
    WHEN LOWER(address) LIKE '%street%' OR LOWER(address) LIKE '%st%' THEN 'Street/St'
    WHEN LOWER(address) LIKE '%lane%' THEN 'Lane'
    WHEN LOWER(address) LIKE '%circle%' THEN 'Circle'
    WHEN LOWER(address) LIKE '%court%' THEN 'Court'
    ELSE 'Other'
  END
ORDER BY street_type;
```

![What type of street name employees live on](https://github.com/user-attachments/assets/c11f9b2a-abfc-4d5e-8e29-7a6c0031b25b)

```sql
-- Add a new employee from Alabama
insert into contacts ("empId", "firstName", "lastName", "address") values (99999, 'Eliyahu', 'Masinter', '1234 address Ave., Los Angeles, CA, 12345');

```


### Functions 
#### (a)
```sql
CREATE OR REPLACE FUNCTION CalcDestLoadCount(dest_iata text)
RETURNS TABLE(dest text, total_kg numeric, plane_count bigint) AS $$
BEGIN
    RETURN QUERY
    SELECT CAST(c.iata AS text) AS dest, CAST(SUM(l.weight) AS numeric) AS total_kg, COUNT(ca.aircraft_rn) AS plane_count
    FROM luggage l
    JOIN carousel_aircraft ca ON l.aircraft_rn = ca.aircraft_rn
    JOIN carousel c ON ca.carousel_id = c.carousel_id
    WHERE c.iata = dest_iata
    GROUP BY c.iata;
END;
$$ LANGUAGE plpgsql;

-- Example:
SELECT * FROM CalcDestLoadCount('TLV');
```

```sql
CREATE OR REPLACE FUNCTION GetCarouselLuggageCounts()
RETURNS TABLE (
    carousel_id integer,
    type cargo_type,
    luggage_count bigint
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.carousel_id, l.type, COUNT(l.tag) AS luggage_count
    FROM Carousel c
    LEFT JOIN carousel_aircraft ca ON c.carousel_id = ca.carousel_id
    LEFT JOIN Luggage l ON ca.aircraft_rn = l.aircraft_rn
    GROUP BY c.carousel_id, l.type
	HAVING Count(l.tag) > 0
    ORDER BY c.carousel_id;
END;
$$ LANGUAGE plpgsql;

-- Example
SELECT * FROM GetCarouselLuggageCounts();
```

```sql
CREATE OR REPLACE FUNCTION GetLuggageDetailsWithCarousel()
RETURNS TABLE (
    tag integer,
    type cargo_type,
    weight float,
    carousel_id integer,
    capacity integer,
    terminal integer,
    iata character varying
) AS $$
BEGIN
    RETURN QUERY
    SELECT l.tag, l.type, l.weight, c.carousel_id, c.capacity, c.terminal, c.iata
    FROM public.luggage l
    LEFT JOIN public.carousel_aircraft ca ON l.aircraft_rn = ca.aircraft_rn
    LEFT JOIN public.carousel c ON ca.carousel_id = c.carousel_id
    WHERE c.iata IS NOT NULL;

END;
$$ LANGUAGE plpgsql;

-- Example
SELECT * FROM GetLuggageDetailsWithCarousel();
```

```sql
DROP FUNCTION MinCarouselLoad(minimum_weight int);

CREATE OR REPLACE FUNCTION MinCarouselLoad(minimum_weight int)
RETURNS TABLE (
    carousel_id int,
    kg int
) AS $$
BEGIN
    RETURN QUERY
    SELECT ct.carousel_id, SUM(ct.total)::int AS kg
    FROM (
        SELECT ca.carousel_id, SUM(l.weight) AS total
        FROM public.luggage l
        JOIN public.carousel_aircraft ca ON l.aircraft_rn = ca.aircraft_rn
        GROUP BY ca.carousel_id
    ) AS ct
    GROUP BY ct.carousel_id
    HAVING SUM(ct.total) >= minimum_weight
    ORDER BY kg DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM MinCarouselLoad(100);
```

#### (b)
```sql
FUNCTION GetCarouselLuggageCounts()
FUNCTION CalcDestLoadCount(dest_iata text)
FUNCTION GetLuggageDetailsWithCarousel()
FUNCTION min_carousel_load(minimum_weight integer)
FUNCTION MinCarouselLoad(minimum_weight int)
```
[Functions.sql](Stage%203/Functions.sql)

#### (c)
[Queries.sql](Stage%203/queries.sql)

#### (d)
[Timings.log](Stage%203/timings.log)
```sql
airline=# SELECT * FROM CalcDestLoadCount('TLV');
Time: 4.332 ms

airline=# SELECT * FROM GetCarouselLuggageCounts();
Time: 48.317 ms

airline=# SELECT * FROM GetLuggageDetailsWithCarousel();
Time: 99.640 ms

airline=# SELECT * FROM MinCarouselLoad(100);
Time: 32.048 ms
```

# 🍵 Stage 4
#### Preparation
Cloning the other database:
```git
git clone https://github.com/ephmonster/miniProjectDatabase
```
Getting the files from Git-LFS
```git
git lfs fetch
```

![image](https://github.com/user-attachments/assets/7364ac6e-1c2d-4bc2-a418-dcf853dc3add)
* The other database had an airplane table which we would be able to connect to aircraft_rn in our database
* Since there is no aircraft_rn column, we can arbitrarily add it
* Problem: our aircraft_rn goes to 500; there are 12000+ airplanes in the external table..
* Solution: we'll just assign the active rn's to 500 of the airplanes, and the rest can be easily generated with our python script 

```python
conn = psycopg2.connect(**config)
print('Connected to the PostgreSQL server.')
cur = conn.cursor()

sql = '''ALTER TABLE airplane
	 ADD COLUMN aircraft_rn character varying;'''
cur.execute(sql)
conn.commit()

sql = '''SELECT count(*) FROM airplane;'''
cur.execute(sql)
count = cur.fetchall()[0][0]
print(str(count))

for sn in range(count-1):
    sql = f"UPDATE airplane SET aircraft_rn = '{random_registration_num()}' WHERE serialnumber = {sn};"
    cur.execute(sql)
    conn.commit()
```

## Queries and Views

For our first view, we used an outer join so that we only get airports that have at least one tug and carousel. If we wanted all airports we could have used an inner join instead.
```sql
-- Create a view showing which airports have what equipment.
create or replace view airport_equipment as SELECT
    COALESCE(t.location, c.iata) AS location,
    COALESCE(t.tug_count, 0) AS tug_count,
    COALESCE(c.carousel_count, 0) AS carousel_count
FROM
    (SELECT location, COUNT(*) AS tug_count FROM airplanetug GROUP BY location) t
FULL OUTER JOIN
    (SELECT iata, COUNT(*) AS carousel_count FROM carousel GROUP BY iata) c
ON t.location = c.iata;
```
Result of creating the view.

![Screenshot 2024-08-07 111201](https://github.com/user-attachments/assets/f72d50f1-c381-4467-a4bc-12dd9f26b985)

The select statement queries our view to find the average number of pieces of equipment from all the airports. 
```sql
-- Calculate the average number of tugs and carousels at all airports.
SELECT
    AVG(tug_count) AS average_tugs,
    AVG(carousel_count) AS average_carousels
FROM airport_equipment;
```
With result

![Screenshot 2024-08-07 111454](https://github.com/user-attachments/assets/820e6681-3575-4aa3-9456-a8767b83d9e1)

We delete all airports that don’t have at least 175 carousels.  Because we use aggregation and a join, we can not directly delete from the view as you see below.

![Screenshot 2024-08-07 112211](https://github.com/user-attachments/assets/19f0ef05-7aed-43a1-818c-4fdc891bc643)

Instead, we delete from the original table and query from the view
```
-- Delete all carousels from airports that have fewer than 150 carousels.
DELETE FROM carousel
WHERE iata IN (
    SELECT location
    FROM airport_equipment
    WHERE carousel_count < 150
);
```
There are 169 airports in the view before we do this.

![Screenshot 2024-08-07 111641](https://github.com/user-attachments/assets/037716f7-010c-431a-bedd-6d7453ea61a5)

And only 109 afterward, so we removed 60 airports from the view.

![Screenshot 2024-08-07 112446](https://github.com/user-attachments/assets/42558a17-538c-4963-bbd6-248eda744ed7)

For the second query, we find out how much weight each airplane has carried by using our table of luggage and their table of airplane.
```sql
-- For each airplane, sum up the total luggage weight for that airplane
create or replace view airplane_weight as SELECT
    a.aircraft_rn,
    COALESCE(SUM(l.weight), 0) AS total_weight
FROM
    airplane a
LEFT JOIN
    luggage l ON a.aircraft_rn = l.aircraft_rn
GROUP BY
    a.aircraft_rn
ORDER BY
    total_weight DESC;
```
Result of creating the view

![Screenshot 2024-08-07 212130](https://github.com/user-attachments/assets/174da689-dea3-475a-9cdc-d7253fcec75a)


Now we query to find out how much weight in total there is for each make and model of airplane.

```sql
--Get the total weight by make and model of airplane
SELECT
    a.makeandmodel,
    SUM(l.total_weight) AS total_weight
FROM
    airplane a
JOIN
    airplane_weight aw
ON
    a.aircraft_rn = aw.aircraft_rn
GROUP BY
    a.makeandmodel;
```

![Screenshot 2024-08-07 212809](https://github.com/user-attachments/assets/5383f702-8bb0-4609-94dd-2b128d2ae229)


Now we delete all airplanes that don’t have any luggage associated with them.
```
-- Delete all airplanes that have no luggage weight data.
DELETE FROM airplane
WHERE aircraft_rn NOT IN (
    SELECT aircraft_rn
    FROM airplane_weight
);
```
![Screenshot 2024-08-07 213020](https://github.com/user-attachments/assets/70baf44b-855d-499d-bbf3-d14d0f51d07b)

### Queries

1)  We get the top 10 airports that have the most airplane tugs

![Screenshot 2024-08-07 113705](https://github.com/user-attachments/assets/7607f537-88c9-45d0-897e-fb8a972e7f2f)


2) Finding the total number of tugs and carousels across all airports

![Screenshot 2024-08-07 113814](https://github.com/user-attachments/assets/d40b971c-96fc-4560-acfb-165a2d7ef24b)


3) Retrieve the top 5 aircraft models with the highest total luggage weight along with their average luggage weight per aircraft.

![Screenshot 2024-08-07 213409](https://github.com/user-attachments/assets/db9a00c2-73fc-47ef-85de-fcaecd44a7f4)


4)  This query deletes all luggage that is heavier than 50 pounds and is on an  airplane model "Embraer E175".

![Screenshot 2024-08-07 213803](https://github.com/user-attachments/assets/cd21b523-3a2d-4eab-8694-00fbca9748db)




After adding the data:\
![image](https://github.com/user-attachments/assets/f12c1947-0c8e-4233-a4ba-b096329452e7)

Enabling the link:
```sql
CREATE EXTENSION postgres_fdw;
```

```sql
CREATE SERVER fdw_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'localhost', dbname 'airline-equipment', port '5432');
CREATE USER MAPPING FOR amiga SERVER fdw_server OPTIONS (user 'amiga', password '');
IMPORT FOREIGN SCHEMA public FROM SERVER fdw_server INTO public;
```

```txt
                   List of relations
 Schema |         Name         |     Type      | Owner
--------+----------------------+---------------+-------
 public | airbusa319           | foreign table | amiga
 public | airplane             | foreign table | amiga
 public | airplanetug          | foreign table | amiga
 public | airplanetype         | foreign table | amiga
 public | attendant            | table         | amiga
 public | carousel             | table         | amiga
 public | carousel_aircraft    | table         | amiga
 public | employee             | table         | amiga
 public | fuelingtruck         | foreign table | amiga
 public | fuelstock            | foreign table | amiga
 public | fueltype             | foreign table | amiga
 public | gate                 | foreign table | amiga
 public | ground_crew          | table         | amiga
 public | jetbridge            | foreign table | amiga
 public | landingtakingoff     | foreign table | amiga
 public | lax_bridges          | foreign table | amiga
 public | lax_runways          | foreign table | amiga
 public | luggage              | table         | amiga
 public | medic                | table         | amiga
 public | pilot                | table         | amiga
 public | runway               | foreign table | amiga
 public | takeoffs5            | foreign table | amiga
 public | truckload            | foreign table | amiga
 public | truckload_05_27_23   | foreign table | amiga
 public | truckload_2024_04_28 | foreign table | amiga
 public | tugs                 | foreign table | amiga
 public | used                 | foreign table | amiga
```

### ERD
Original\
![original](https://github.com/user-attachments/assets/9dba22ba-986d-4ee4-811d-8f89d2329e06)

External
![external](https://github.com/user-attachments/assets/b7e5b958-51ed-4e8a-aa51-3706c28169bc)

Combined
![combined](https://github.com/user-attachments/assets/f3a3fd28-43e5-43b5-abf7-dccebc57895b)

* Since the Airplane entity was changed, we added an ```aircraft_rn``` field
* The Carousel_Aircraft table was changed to a relationship between Airplane and Carousel
* The database can now reference Airplanes instead of just the ```aircraft_rn``` we used until now


