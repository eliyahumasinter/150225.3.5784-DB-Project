CREATE TYPE public.field AS ENUM
    ('emergencyMedicine', 'travelMedicine', 'occupationalHealth', 'publicHealth', 'mentalHealth', 'firstAid', 'airportClinic');

CREATE TYPE public.crew_type AS ENUM
    ('rampAgent', 'baggageHandler', 'technician', 'fueler', 'cleaner', 'gse', 'caterer', 'security', 'supervisor', 'tugger');

CREATE TYPE public.cargo_type AS ENUM
    ('checked', 'carryOn', 'personal', 'special', 'fragile', 'equipment');

CREATE TABLE IF NOT EXISTS public.luggage
(
    tag integer NOT NULL,
    weight float,
    type cargo_type,
    "aircraftId" integer,
    "carouselId" integer,
    CONSTRAINT luggage_pkey PRIMARY KEY (tag)
);

CREATE TABLE IF NOT EXISTS public.carousel
(
    "carouselId" integer NOT NULL,
    "flightId" integer,
    size integer,
    terminal integer,
    iata character varying COLLATE pg_catalog."default",
    CONSTRAINT carousel_pkey PRIMARY KEY ("carouselId")
);


CREATE TABLE IF NOT EXISTS public.employee
(
    "empId" integer NOT NULL,
    "firstName" character varying COLLATE pg_catalog."default",
    "lastName" character varying COLLATE pg_catalog."default",
    wage float,
    dob date,
    address character varying COLLATE pg_catalog."default",
    "empDate" date,
    CONSTRAINT employee_pkey PRIMARY KEY ("empId")
);

CREATE TABLE IF NOT EXISTS public.attendant
(
    -- Inherited from table public.employee: "empId" integer NOT NULL,
    -- Inherited from table public.employee: "firstName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "lastName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: wage integer,
    -- Inherited from table public.employee: dob date,
    -- Inherited from table public.employee: address character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "empDate" date
)
    INHERITS (public.employee);

CREATE TABLE IF NOT EXISTS public.pilot
(
    -- Inherited from table public.employee: "empId" integer NOT NULL,
    -- Inherited from table public.employee: "firstName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "lastName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: wage integer,
    -- Inherited from table public.employee: dob date,
    -- Inherited from table public.employee: address character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "empDate" date,
    "flightHours" float
)
    INHERITS (public.employee);

CREATE TABLE IF NOT EXISTS public.medic
(
    -- Inherited from table public.employee: "empId" integer NOT NULL,
    -- Inherited from table public.employee: "firstName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "lastName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: wage integer,
    -- Inherited from table public.employee: dob date,
    -- Inherited from table public.employee: address character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "empDate" date,
    field field
)
    INHERITS (public.employee);

CREATE TABLE IF NOT EXISTS public.ground_crew
(
    -- Inherited from table public.employee: "empId" integer NOT NULL,
    -- Inherited from table public.employee: "firstName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "lastName" character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: wage integer,
    -- Inherited from table public.employee: dob date,
    -- Inherited from table public.employee: address character varying COLLATE pg_catalog."default",
    -- Inherited from table public.employee: "empDate" date,
    type crew_type
)
    INHERITS (public.employee);